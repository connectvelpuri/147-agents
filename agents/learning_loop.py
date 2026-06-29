#!/usr/bin/env python3
"""
Agent Learning Loop System
==========================
A feedback-driven mechanism where agents learn from outcomes.
Implements: OutcomeRecorder -> PatternExtractor -> PromptOptimizer -> LearningLoop

Production-grade Python with SQLite storage, scoring system (1-5), and full cycle orchestration.
"""

import sqlite3
import json
import time
import threading
import re
import logging
import os
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple, Callable
from datetime import datetime, timezone
from collections import defaultdict, Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("learning_loop")
logger.setLevel(logging.INFO)
_ch = logging.StreamHandler()
_ch.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
))
if not logger.handlers:
    logger.addHandler(_ch)

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class AgentResponse:
    """Represents a single agent response/action."""
    agent_id: str
    prompt_used: str
    response_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    outcome_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Outcome:
    """Feedback outcome for an agent response. Score 1-5."""
    response_id: int
    score: int            # 1-5
    label: str            # "good" | "bad" | "neutral"  (mapped from score)
    feedback_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    outcome_id: Optional[int] = None

    def __post_init__(self):
        if not 1 <= self.score <= 5:
            raise ValueError(f"Score must be between 1 and 5, got {self.score}")
        # auto-derive label if not explicitly set
        if self.label not in ("good", "bad", "neutral"):
            self.label = self._derive_label(self.score)

    @staticmethod
    def _derive_label(score: int) -> str:
        if score >= 4:
            return "good"
        elif score <= 2:
            return "bad"
        else:
            return "neutral"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Pattern:
    """A learned pattern from outcome analysis."""
    pattern_id: Optional[int] = None
    pattern_type: str = ""          # "good_pattern", "bad_pattern", "neutral_pattern"
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    avg_score: float = 0.0
    confidence: float = 0.0         # 0.0 - 1.0
    sample_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PromptSuggestion:
    """A suggested improvement to an agent prompt."""
    suggestion_id: Optional[int] = None
    agent_id: str = ""
    original_prompt_snippet: str = ""
    suggested_change: str = ""
    rationale: str = ""
    expected_impact: str = ""
    priority: str = "medium"        # "high", "medium", "low"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Database Manager
# ---------------------------------------------------------------------------

class DatabaseManager:
    """Thread-safe SQLite database manager for persisting outcomes and patterns."""

    def __init__(self, db_path: str = "learning_loop.db"):
        self.db_path = db_path
        self._local = threading.local()
        self._lock = threading.Lock()
        self._init_schema()

    def _get_conn(self) -> sqlite3.Connection:
        """Get a thread-local connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA foreign_keys=ON")
        return self._local.conn

    def _init_schema(self) -> None:
        """Create tables if they don't exist."""
        schema = """
        CREATE TABLE IF NOT EXISTS agent_responses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id    TEXT NOT NULL,
            prompt_used TEXT NOT NULL,
            response_text TEXT NOT NULL,
            context     TEXT DEFAULT '{}',
            timestamp   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS outcomes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            response_id INTEGER NOT NULL,
            score       INTEGER NOT NULL CHECK(score >= 1 AND score <= 5),
            label       TEXT NOT NULL DEFAULT 'neutral',
            feedback_text TEXT DEFAULT '',
            metadata    TEXT DEFAULT '{}',
            timestamp   TEXT NOT NULL,
            FOREIGN KEY (response_id) REFERENCES agent_responses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS patterns (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT NOT NULL,
            description TEXT NOT NULL,
            keywords    TEXT DEFAULT '[]',
            avg_score   REAL DEFAULT 0.0,
            confidence  REAL DEFAULT 0.0,
            sample_count INTEGER DEFAULT 0,
            created_at  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS prompt_suggestions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id    TEXT NOT NULL,
            original_prompt_snippet TEXT NOT NULL,
            suggested_change TEXT NOT NULL,
            rationale   TEXT DEFAULT '',
            expected_impact TEXT DEFAULT '',
            priority    TEXT DEFAULT 'medium',
            created_at  TEXT NOT NULL,
            applied     INTEGER DEFAULT 0
        );

        CREATE INDEX IF NOT EXISTS idx_outcomes_response ON outcomes(response_id);
        CREATE INDEX IF NOT EXISTS idx_outcomes_score   ON outcomes(score);
        CREATE INDEX IF NOT EXISTS idx_outcomes_label   ON outcomes(label);
        CREATE INDEX IF NOT EXISTS idx_patterns_type    ON patterns(pattern_type);
        CREATE INDEX IF NOT EXISTS idx_suggestions_agent ON prompt_suggestions(agent_id);
        """
        with self._lock:
            conn = self._get_conn()
            conn.executescript(schema)
            conn.commit()

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a write query with thread safety."""
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Fetch a single row as dict."""
        conn = self._get_conn()
        row = conn.execute(sql, params).fetchone()
        if row is None:
            return None
        return dict(row)

    def fetchall(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Fetch all rows as dicts."""
        conn = self._get_conn()
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        """Close all connections for this thread."""
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None


# ---------------------------------------------------------------------------
# 1. OutcomeRecorder
# ---------------------------------------------------------------------------

class OutcomeRecorder:
    """Records every agent response with outcome feedback (good/bad/score 1-5)."""

    def __init__(self, db: Optional[DatabaseManager] = None, db_path: str = "learning_loop.db"):
        self.db = db or DatabaseManager(db_path)

    def record_response(self, response: AgentResponse) -> int:
        """Record an agent response and return its ID."""
        context_json = json.dumps(response.context)
        cursor = self.db.execute(
            """INSERT INTO agent_responses (agent_id, prompt_used, response_text, context, timestamp)
               VALUES (?, ?, ?, ?, ?)""",
            (response.agent_id, response.prompt_used, response.response_text,
             context_json, response.timestamp)
        )
        response.outcome_id = cursor.lastrowid
        logger.info(f"Recorded response ID={response.outcome_id} for agent '{response.agent_id}'")
        return response.outcome_id

    def record_outcome(self, outcome: Outcome) -> int:
        """Record an outcome (score + feedback) for a previous response."""
        metadata_json = json.dumps(outcome.metadata)
        cursor = self.db.execute(
            """INSERT INTO outcomes (response_id, score, label, feedback_text, metadata, timestamp)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (outcome.response_id, outcome.score, outcome.label,
             outcome.feedback_text, metadata_json, outcome.timestamp)
        )
        outcome.outcome_id = cursor.lastrowid
        logger.info(
            f"Recorded outcome ID={outcome.outcome_id} for response ID={outcome.response_id} "
            f"(score={outcome.score}, label={outcome.label})"
        )
        return outcome.outcome_id

    def record(self, agent_id: str, prompt_used: str, response_text: str,
               score: int, feedback_text: str = "",
               label: Optional[str] = None,
               context: Optional[Dict[str, Any]] = None) -> Tuple[int, int]:
        """Convenience: record a response and its outcome in one call.

        Returns:
            Tuple of (response_id, outcome_id)
        """
        if label is None:
            label = Outcome._derive_label(score)

        resp = AgentResponse(
            agent_id=agent_id,
            prompt_used=prompt_used,
            response_text=response_text,
            context=context or {},
        )
        response_id = self.record_response(resp)

        outcome = Outcome(
            response_id=response_id,
            score=score,
            label=label,
            feedback_text=feedback_text,
        )
        outcome_id = self.record_outcome(outcome)
        return response_id, outcome_id

    def get_response(self, response_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a recorded response by ID."""
        return self.db.fetchone("SELECT * FROM agent_responses WHERE id = ?", (response_id,))

    def get_outcome(self, outcome_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve an outcome by ID."""
        return self.db.fetchone("SELECT * FROM outcomes WHERE id = ?", (outcome_id,))

    def get_outcomes_for_response(self, response_id: int) -> List[Dict[str, Any]]:
        """Get all outcomes for a given response."""
        return self.db.fetchall(
            "SELECT * FROM outcomes WHERE response_id = ? ORDER BY timestamp", (response_id,)
        )

    def get_all_responses(self, agent_id: Optional[str] = None,
                          limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get responses, optionally filtered by agent_id."""
        if agent_id:
            return self.db.fetchall(
                "SELECT * FROM agent_responses WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (agent_id, limit, offset)
            )
        return self.db.fetchall(
            "SELECT * FROM agent_responses ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )

    def get_all_outcomes(self, label: Optional[str] = None,
                         limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get outcomes, optionally filtered by label (good/bad/neutral)."""
        if label:
            return self.db.fetchall(
                "SELECT * FROM outcomes WHERE label = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                (label, limit, offset)
            )
        return self.db.fetchall(
            "SELECT * FROM outcomes ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )

    def get_stats(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get aggregate statistics about outcomes, optionally per agent."""
        if agent_id:
            row = self.db.fetchone(
                """SELECT COUNT(*) as total,
                          AVG(o.score) as avg_score,
                          SUM(CASE WHEN o.label='good' THEN 1 ELSE 0 END) as good_count,
                          SUM(CASE WHEN o.label='bad' THEN 1 ELSE 0 END) as bad_count,
                          SUM(CASE WHEN o.label='neutral' THEN 1 ELSE 0 END) as neutral_count
                   FROM outcomes o
                   JOIN agent_responses r ON r.id = o.response_id
                   WHERE r.agent_id = ?""",
                (agent_id,)
            )
        else:
            row = self.db.fetchone(
                """SELECT COUNT(*) as total,
                          AVG(score) as avg_score,
                          SUM(CASE WHEN label='good' THEN 1 ELSE 0 END) as good_count,
                          SUM(CASE WHEN label='bad' THEN 1 ELSE 0 END) as bad_count,
                          SUM(CASE WHEN label='neutral' THEN 1 ELSE 0 END) as neutral_count
                   FROM outcomes"""
            )
        if row is None:
            return {"total": 0, "avg_score": 0.0, "good_count": 0, "bad_count": 0, "neutral_count": 0}
        return dict(row)


# ---------------------------------------------------------------------------
# 2. PatternExtractor
# ---------------------------------------------------------------------------

class PatternExtractor:
    """Analyzes outcomes to find patterns — what worked, what failed."""

    def __init__(self, db: Optional[DatabaseManager] = None, db_path: str = "learning_loop.db"):
        self.db = db or DatabaseManager(db_path)

    # ---- Stop words for keyword extraction ----
    _STOP_WORDS: set = {
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "can", "could", "should", "may", "might", "shall", "this",
        "that", "these", "those", "it", "its", "they", "them", "their",
        "we", "us", "our", "you", "your", "he", "she", "him", "her", "his",
        "not", "no", "nor", "so", "if", "then", "else", "when", "where",
        "why", "how", "all", "each", "every", "both", "few", "more", "most",
        "some", "any", "none", "i", "me", "my", "myself", "please", "just",
        "very", "too", "much", "many", "also", "well", "get", "got", "make",
        "made", "use", "used", "using", "like", "would", "should", "could",
        "need", "try", "tried", "trying", "want", "wanted", "looking",
    }

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Split text into lowercase tokens, removing punctuation."""
        tokens = re.findall(r"[a-zA-Z]\w+", text.lower())
        return tokens

    def _extract_keywords(self, texts: List[str], top_n: int = 10) -> List[str]:
        """Extract most frequent meaningful keywords from a list of texts."""
        counter: Counter = Counter()
        for text in texts:
            tokens = self._tokenize(text)
            for token in tokens:
                if token not in self._STOP_WORDS and len(token) > 2:
                    counter[token] += 1
        # Return top N keywords
        return [word for word, _ in counter.most_common(top_n)]

    def extract_patterns(self, agent_id: Optional[str] = None,
                         min_samples: int = 3) -> List[Pattern]:
        """Analyze outcomes and extract patterns.  Returns list of Pattern objects
        for good, bad, and neutral outcomes.

        Patterns are persisted to the database.
        """
        patterns: List[Pattern] = []

        for label in ("good", "bad", "neutral"):
            pattern = self._analyze_label(label, agent_id, min_samples)
            if pattern is not None:
                patterns.append(pattern)
                self._persist_pattern(pattern)

        return patterns

    def _analyze_label(self, label: str, agent_id: Optional[str],
                       min_samples: int) -> Optional[Pattern]:
        """Analyze outcomes for a specific label and extract a pattern."""
        # Build query
        if agent_id:
            rows = self.db.fetchall(
                """SELECT r.response_text, r.prompt_used, o.score, o.feedback_text
                   FROM outcomes o
                   JOIN agent_responses r ON r.id = o.response_id
                   WHERE o.label = ? AND r.agent_id = ?
                   ORDER BY o.timestamp DESC""",
                (label, agent_id)
            )
        else:
            rows = self.db.fetchall(
                """SELECT r.response_text, r.prompt_used, o.score, o.feedback_text, r.agent_id
                   FROM outcomes o
                   JOIN agent_responses r ON r.id = o.response_id
                   WHERE o.label = ?
                   ORDER BY o.timestamp DESC""",
                (label,)
            )

        if len(rows) < min_samples:
            logger.info(
                f"Not enough {label} samples ({len(rows)} < {min_samples}) to extract pattern"
            )
            return None

        scores = [r["score"] for r in rows]
        avg_score = sum(scores) / len(scores)

        # Extract keywords from responses and feedback
        texts_to_analyze = []
        for r in rows:
            texts_to_analyze.append(r["response_text"])
            texts_to_analyze.append(r["prompt_used"])
            if r.get("feedback_text"):
                texts_to_analyze.append(r["feedback_text"])

        keywords = self._extract_keywords(texts_to_analyze)

        # Build description
        label_desc = {
            "good": "What worked well - high-scoring agent responses",
            "bad": "What failed - low-scoring agent responses",
            "neutral": "Mixed or neutral agent responses",
        }
        description = (
            f"{label_desc.get(label, label)}: "
            f"average score {avg_score:.2f} across {len(rows)} samples. "
            f"Keywords: {', '.join(keywords[:6])}"
        )

        # Confidence based on sample size (diminishing returns)
        confidence = min(1.0, len(rows) / 20.0)

        return Pattern(
            pattern_type=f"{label}_pattern",
            description=description,
            keywords=keywords,
            avg_score=avg_score,
            confidence=round(confidence, 3),
            sample_count=len(rows),
        )

    def _persist_pattern(self, pattern: Pattern) -> int:
        """Save a pattern to the database."""
        keywords_json = json.dumps(pattern.keywords)
        cursor = self.db.execute(
            """INSERT INTO patterns (pattern_type, description, keywords, avg_score, confidence, sample_count, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (pattern.pattern_type, pattern.description, keywords_json,
             pattern.avg_score, pattern.confidence, pattern.sample_count,
             pattern.created_at)
        )
        pattern.pattern_id = cursor.lastrowid
        return pattern.pattern_id

    def get_stored_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve stored patterns, optionally filtering by type."""
        if pattern_type:
            return self.db.fetchall(
                "SELECT * FROM patterns WHERE pattern_type = ? ORDER BY confidence DESC",
                (pattern_type,)
            )
        return self.db.fetchall("SELECT * FROM patterns ORDER BY confidence DESC")

    def get_latest_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent patterns."""
        return self.db.fetchall(
            "SELECT * FROM patterns ORDER BY created_at DESC LIMIT ?", (limit,)
        )


# ---------------------------------------------------------------------------
# 3. PromptOptimizer
# ---------------------------------------------------------------------------

class PromptOptimizer:
    """Suggests improvements to agent prompts based on extracted patterns."""

    def __init__(self, db: Optional[DatabaseManager] = None, db_path: str = "learning_loop.db"):
        self.db = db or DatabaseManager(db_path)

    def generate_suggestions(self, agent_id: str,
                             patterns: Optional[List[Pattern]] = None) -> List[PromptSuggestion]:
        """Generate prompt improvement suggestions from patterns.

        If patterns is None, loads latest patterns from the database.
        Returns list of PromptSuggestion objects (also persisted).
        """
        if patterns is None:
            extractor = PatternExtractor(self.db)
            stored = extractor.get_stored_patterns()
            patterns = []
            for p in stored:
                patterns.append(Pattern(
                    pattern_id=p["id"],
                    pattern_type=p["pattern_type"],
                    description=p["description"],
                    keywords=json.loads(p["keywords"]) if isinstance(p["keywords"], str) else p["keywords"],
                    avg_score=p["avg_score"],
                    confidence=p["confidence"],
                    sample_count=p["sample_count"],
                    created_at=p["created_at"],
                ))

        if not patterns:
            logger.info("No patterns available to generate suggestions")
            return []

        suggestions: List[PromptSuggestion] = []

        for pattern in patterns:
            suggestion = self._build_suggestion(agent_id, pattern)
            if suggestion is not None:
                suggestions.append(suggestion)
                self._persist_suggestion(suggestion)
                logger.info(
                    f"Generated suggestion for agent '{agent_id}': "
                    f"{suggestion.suggested_change[:60]}..."
                )

        return suggestions

    def _build_suggestion(self, agent_id: str, pattern: Pattern) -> Optional[PromptSuggestion]:
        """Build a single prompt suggestion from a pattern."""
        if pattern.pattern_type == "good_pattern":
            return PromptSuggestion(
                agent_id=agent_id,
                original_prompt_snippet="(general prompt structure)",
                suggested_change=(
                    f"Reinforce successful strategies: continue using approaches "
                    f"related to keywords: {', '.join(pattern.keywords[:5])}. "
                    f"These patterns scored {pattern.avg_score:.1f}/5 on average."
                ),
                rationale=(
                    f"High-scoring pattern detected with confidence {pattern.confidence:.0%}. "
                    f"Encourage agent to replicate these behaviors."
                ),
                expected_impact="Maintain or improve current performance levels",
                priority="medium" if pattern.confidence < 0.5 else "high",
            )

        elif pattern.pattern_type == "bad_pattern":
            return PromptSuggestion(
                agent_id=agent_id,
                original_prompt_snippet="(general prompt structure)",
                suggested_change=(
                    f"Avoid or refactor strategies related to: "
                    f"{', '.join(pattern.keywords[:5])}. "
                    f"These patterns scored only {pattern.avg_score:.1f}/5 on average."
                ),
                rationale=(
                    f"Low-scoring pattern detected with confidence {pattern.confidence:.0%}. "
                    f"Agent instructions should explicitly discourage these approaches."
                ),
                expected_impact="Reduce failure rate and improve average scores",
                priority="high",
            )

        elif pattern.pattern_type == "neutral_pattern":
            return PromptSuggestion(
                agent_id=agent_id,
                original_prompt_snippet="(general prompt structure)",
                suggested_change=(
                    f"Consider refining approach for: "
                    f"{', '.join(pattern.keywords[:5])}. "
                    f"These responses scored {pattern.avg_score:.1f}/5 - room for improvement."
                ),
                rationale=(
                    f"Neutral pattern detected with confidence {pattern.confidence:.0%}. "
                    f"Minor prompt adjustments may shift these to positive outcomes."
                ),
                expected_impact="Incremental improvement in response quality",
                priority="low",
            )

        return None

    def _persist_suggestion(self, suggestion: PromptSuggestion) -> int:
        """Save a suggestion to the database."""
        cursor = self.db.execute(
            """INSERT INTO prompt_suggestions
               (agent_id, original_prompt_snippet, suggested_change, rationale,
                expected_impact, priority, created_at, applied)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (suggestion.agent_id, suggestion.original_prompt_snippet,
             suggestion.suggested_change, suggestion.rationale,
             suggestion.expected_impact, suggestion.priority,
             suggestion.created_at, int(suggestion.applied))
        )
        suggestion.suggestion_id = cursor.lastrowid
        return suggestion.suggestion_id

    def get_suggestions(self, agent_id: Optional[str] = None,
                        only_unapplied: bool = True) -> List[Dict[str, Any]]:
        """Retrieve suggestions, optionally filtering by agent and applied status."""
        if agent_id and only_unapplied:
            return self.db.fetchall(
                "SELECT * FROM prompt_suggestions WHERE agent_id = ? AND applied = 0 ORDER BY priority DESC, created_at DESC",
                (agent_id,)
            )
        elif agent_id:
            return self.db.fetchall(
                "SELECT * FROM prompt_suggestions WHERE agent_id = ? ORDER BY created_at DESC",
                (agent_id,)
            )
        elif only_unapplied:
            return self.db.fetchall(
                "SELECT * FROM prompt_suggestions WHERE applied = 0 ORDER BY priority DESC, created_at DESC"
            )
        return self.db.fetchall("SELECT * FROM prompt_suggestions ORDER BY created_at DESC")

    def mark_applied(self, suggestion_id: int) -> bool:
        """Mark a suggestion as having been applied."""
        cursor = self.db.execute(
            "UPDATE prompt_suggestions SET applied = 1 WHERE id = ?", (suggestion_id,)
        )
        return cursor.rowcount > 0


# ---------------------------------------------------------------------------
# 4. LearningLoop
# ---------------------------------------------------------------------------

class LearningLoop:
    """Orchestrates the full learning cycle:
    execute -> record -> analyze -> improve -> redeploy.
    """

    def __init__(
        self,
        agent_executor: Optional[Callable[[str, str], str]] = None,
        db_path: str = "learning_loop.db",
        agent_id: str = "default_agent",
    ):
        self.db = DatabaseManager(db_path)
        self.recorder = OutcomeRecorder(self.db)
        self.extractor = PatternExtractor(self.db)
        self.optimizer = PromptOptimizer(self.db)
        self.agent_executor = agent_executor
        self.agent_id = agent_id
        self.current_prompt: str = ""
        self.cycle_count: int = 0
        self._running = False
        self._stop_event = threading.Event()

    def set_agent_executor(self, executor: Callable[[str, str], str]) -> None:
        """Set or replace the agent executor function.

        The executor signature: fn(agent_id: str, prompt: str) -> str
        It should return the agent's response text.
        """
        self.agent_executor = executor

    def set_agent_id(self, agent_id: str) -> None:
        """Set the agent identifier."""
        self.agent_id = agent_id

    def set_prompt(self, prompt: str) -> None:
        """Set the current prompt to use for agent execution."""
        self.current_prompt = prompt

    def get_optimized_prompt(self) -> str:
        """Get the current prompt, potentially augmented with learned improvements."""
        return self.current_prompt

    # ----- Single cycle -----

    def run_cycle(
        self,
        score: int,
        feedback_text: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run one full cycle: execute -> record -> analyze -> improve.

        Args:
            score: Human-provided score (1-5) for the agent's response.
            feedback_text: Optional textual feedback.
            context: Optional context dict for the response.

        Returns:
            Dict with cycle results including response_id, outcome_id,
            extracted patterns, and generated suggestions.
        """
        if not self.agent_executor:
            raise RuntimeError(
                "No agent_executor set. Call set_agent_executor() or pass one to __init__."
            )
        if not self.current_prompt:
            raise RuntimeError(
                "No prompt set. Call set_prompt() or set current_prompt before running a cycle."
            )

        self.cycle_count += 1
        cycle_id = self.cycle_count
        logger.info(f"=== Learning Loop Cycle #{cycle_id} (agent: {self.agent_id}) ===")

        # 1. EXECUTE: Run the agent with the current prompt
        logger.info("Executing agent...")
        response_text = self.agent_executor(self.agent_id, self.current_prompt)

        # 2. RECORD: Save the response and outcome
        logger.info("Recording response and outcome...")
        response_id, outcome_id = self.recorder.record(
            agent_id=self.agent_id,
            prompt_used=self.current_prompt,
            response_text=response_text,
            score=score,
            feedback_text=feedback_text,
            context=context or {},
        )

        # 3. ANALYZE: Extract patterns from outcomes
        logger.info("Analyzing outcomes for patterns...")
        patterns = self.extractor.extract_patterns(agent_id=self.agent_id)

        # 4. IMPROVE: Generate prompt suggestions from patterns
        logger.info("Generating prompt improvement suggestions...")
        suggestions = self.optimizer.generate_suggestions(
            agent_id=self.agent_id,
            patterns=patterns,
        )

        # 5. REDEPLOY: Apply high-priority suggestions to the prompt
        updated_prompt = self._apply_suggestions(suggestions)

        result = {
            "cycle": cycle_id,
            "agent_id": self.agent_id,
            "response_id": response_id,
            "outcome_id": outcome_id,
            "response_text": response_text,
            "score": score,
            "patterns": [p.to_dict() for p in patterns],
            "suggestions": [s.to_dict() for s in suggestions],
            "prompt_before": self.current_prompt,
            "prompt_after": updated_prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        logger.info(f"Cycle #{cycle_id} complete (score={score}, patterns={len(patterns)}, suggestions={len(suggestions)})")
        return result

    def _apply_suggestions(self, suggestions: List[PromptSuggestion]) -> str:
        """Integrate high-priority suggestions into the current prompt."""
        if not suggestions or not self.current_prompt:
            return self.current_prompt

        # Collect high-priority suggestions
        high_priority = [s for s in suggestions if s.priority == "high"]
        if not high_priority:
            return self.current_prompt

        # Build an "improvements" section to append to the prompt
        improvements = []
        for s in high_priority[:3]:  # Apply top 3 high-priority
            improvements.append(f"- {s.suggested_change}")
            self.optimizer.mark_applied(s.suggestion_id)

        if improvements:
            improvement_block = (
                "\n\n[LEARNING LOOP FEEDBACK - Applied Improvements]\n"
                + "\n".join(improvements)
                + "\n[/LEARNING LOOP FEEDBACK]"
            )
            updated = self.current_prompt + improvement_block
            self.current_prompt = updated
            logger.info(f"Applied {len(improvements)} high-priority improvement(s) to prompt")
        else:
            logger.info("No high-priority suggestions to apply")

        return self.current_prompt

    # ----- Automated cycle running -----

    def run_auto_cycle(
        self,
        scorer: Callable[[str, str, str], int],
        feedback_fn: Optional[Callable[[str, str, str], str]] = None,
        context_fn: Optional[Callable[[str, str, str], Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Run a cycle with automated scoring and feedback.

        Args:
            scorer: Function(agent_id, prompt, response) -> int (1-5).
            feedback_fn: Optional Function(agent_id, prompt, response) -> str.
            context_fn: Optional Function(agent_id, prompt, response) -> dict.

        Returns:
            Dict with cycle results.
        """
        if not self.agent_executor:
            raise RuntimeError("No agent_executor set.")
        if not self.current_prompt:
            raise RuntimeError("No prompt set.")

        # Execute
        response_text = self.agent_executor(self.agent_id, self.current_prompt)

        # Score
        score = scorer(self.agent_id, self.current_prompt, response_text)
        if not 1 <= score <= 5:
            raise ValueError(f"Scorer returned invalid score: {score}")

        # Feedback
        feedback = feedback_fn(self.agent_id, self.current_prompt, response_text) if feedback_fn else ""

        # Context
        context = context_fn(self.agent_id, self.current_prompt, response_text) if context_fn else {}

        # Now run a normal cycle using these values
        # We'll do it manually to avoid double-execution
        self.cycle_count += 1
        cycle_id = self.cycle_count
        logger.info(f"=== Auto Learning Loop Cycle #{cycle_id} (agent: {self.agent_id}) ===")

        # Record
        response_id, outcome_id = self.recorder.record(
            agent_id=self.agent_id,
            prompt_used=self.current_prompt,
            response_text=response_text,
            score=score,
            feedback_text=feedback,
            context=context,
        )

        # Analyze
        patterns = self.extractor.extract_patterns(agent_id=self.agent_id)

        # Improve
        suggestions = self.optimizer.generate_suggestions(
            agent_id=self.agent_id,
            patterns=patterns,
        )

        # Redeploy
        updated_prompt = self._apply_suggestions(suggestions)

        return {
            "cycle": cycle_id,
            "agent_id": self.agent_id,
            "response_id": response_id,
            "outcome_id": outcome_id,
            "response_text": response_text,
            "score": score,
            "patterns": [p.to_dict() for p in patterns],
            "suggestions": [s.to_dict() for s in suggestions],
            "prompt_before": self.current_prompt if updated_prompt != self.current_prompt else self.current_prompt,
            "prompt_after": updated_prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ----- Continuous loop -----

    def run_continuous(
        self,
        scorer: Callable[[str, str, str], int],
        feedback_fn: Optional[Callable[[str, str, str], str]] = None,
        context_fn: Optional[Callable[[str, str, str], Dict[str, Any]]] = None,
        interval_seconds: float = 60.0,
        max_cycles: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Run learning cycles continuously until stopped or max_cycles reached.

        Args:
            scorer: Function(agent_id, prompt, response) -> int.
            feedback_fn: Optional feedback function.
            context_fn: Optional context function.
            interval_seconds: Time between cycles.
            max_cycles: Maximum number of cycles to run (None = infinite).

        Returns:
            List of cycle result dicts.
        """
        if max_cycles is not None and max_cycles <= 0:
            logger.warning("max_cycles <= 0, returning empty results")
            return []

        self._running = True
        self._stop_event.clear()
        results: List[Dict[str, Any]] = []

        logger.info(
            f"Starting continuous learning loop (interval={interval_seconds}s, "
            f"max_cycles={max_cycles or 'unlimited'})"
        )

        try:
            while self._running and not self._stop_event.is_set():
                result = self.run_auto_cycle(scorer, feedback_fn, context_fn)
                results.append(result)

                if max_cycles is not None and len(results) >= max_cycles:
                    logger.info(f"Reached max_cycles={max_cycles}, stopping")
                    break

                if self._running and not self._stop_event.is_set():
                    self._stop_event.wait(interval_seconds)

        except KeyboardInterrupt:
            logger.info("Continuous loop interrupted")
        finally:
            self._running = False

        return results

    def stop_continuous(self) -> None:
        """Signal the continuous loop to stop gracefully."""
        self._running = False
        self._stop_event.set()
        logger.info("Continuous loop stop signaled")

    # ----- Reporting -----

    def get_cycle_summary(self, limit: int = 5) -> Dict[str, Any]:
        """Get a summary of the learning loop's state and recent activity."""
        stats = self.recorder.get_stats(agent_id=self.agent_id)
        recent_outcomes = self.recorder.get_all_outcomes(limit=limit)
        top_patterns = self.extractor.get_latest_patterns(limit=3)
        pending_suggestions = self.optimizer.get_suggestions(
            agent_id=self.agent_id, only_unapplied=True
        )

        return {
            "agent_id": self.agent_id,
            "cycle_count": self.cycle_count,
            "stats": stats,
            "recent_outcomes": recent_outcomes,
            "top_patterns": top_patterns,
            "pending_suggestions": len(pending_suggestions),
            "prompt_length": len(self.current_prompt),
            "is_running": self._running,
        }

    def close(self) -> None:
        """Close database connections."""
        self.db.close()
        logger.info("Learning loop database connections closed")


# ---------------------------------------------------------------------------
# Demo / Test
# ---------------------------------------------------------------------------

def _demo_executor(agent_id: str, prompt: str) -> str:
    """Simple demo executor that returns a canned response based on the prompt."""
    import random
    responses = [
        f"I analyzed the request: {prompt[:50]}... Here are my recommendations.",
        f"Based on your query about '{prompt[:40]}', I suggest the following approach.",
        f"After careful consideration of '{prompt[:45]}', I recommend alternative strategies.",
        f"The data indicates that '{prompt[:35]}' requires immediate attention.",
        f"I've processed '{prompt[:30]}' and found several actionable insights.",
    ]
    return random.choice(responses)


def _demo_scorer(agent_id: str, prompt: str, response: str) -> int:
    """Simple demo scorer - higher scores for longer responses containing certain keywords."""
    import random
    base = 3
    if len(response) > 80:
        base += 1
    if "recommend" in response.lower():
        base += 1
    if "analyzed" in response.lower():
        base += 1
    # Add some randomness for variety
    base += random.choice([-1, 0, 0, 1])
    return max(1, min(5, base))


def demo() -> None:
    """Run a demonstration of the learning loop."""
    print("=" * 70)
    print("  AGENT LEARNING LOOP - DEMONSTRATION")
    print("=" * 70)

    # Use a temporary database for demo
    db_path = "demo_learning_loop.db"

    # Clean up previous demo
    if os.path.exists(db_path):
        os.remove(db_path)

    loop = LearningLoop(
        agent_executor=_demo_executor,
        db_path=db_path,
        agent_id="demo_agent",
    )
    loop.set_prompt("You are a helpful sales assistant. Respond to customer inquiries professionally.")

    print(f"\nAgent ID: {loop.agent_id}")
    print(f"Initial prompt: {loop.current_prompt[:60]}...")
    print(f"\nRunning 5 manual cycles...\n")

    scores = [4, 2, 5, 3, 4]
    feedbacks = [
        "Great response, very thorough",
        "Too vague, needs more specifics",
        "Excellent analysis and recommendations",
        "Adequate but could be more detailed",
        "Good work, clear and actionable",
    ]

    for i in range(5):
        print(f"--- Cycle {i+1} ---")
        result = loop.run_cycle(
            score=scores[i],
            feedback_text=feedbacks[i],
            context={"query": f"Customer inquiry #{i+1}"},
        )
        print(f"  Score: {result['score']}")
        print(f"  Patterns found: {len(result['patterns'])}")
        print(f"  Suggestions generated: {len(result['suggestions'])}")
        print()

    print("--- Final Summary ---")
    summary = loop.get_cycle_summary()
    print(f"  Total cycles: {summary['cycle_count']}")
    print(f"  Stats: {summary['stats']}")
    print(f"  Pending suggestions: {summary['pending_suggestions']}")
    print(f"  Prompt length: {summary['prompt_length']} chars")
    print(f"\nImproved prompt:\n{loop.get_optimized_prompt()}\n")

    # Show stored patterns
    print("--- Stored Patterns ---")
    for p in loop.extractor.get_stored_patterns():
        print(f"  [{p['pattern_type']}] conf={p['confidence']:.0%}, samples={p['sample_count']}, score={p['avg_score']:.1f}")
        print(f"    {p['description'][:100]}...")

    # Show suggestions
    print("\n--- Suggestions ---")
    for s in loop.optimizer.get_suggestions():
        print(f"  [{s['priority']}] {s['suggested_change'][:80]}...")
        print(f"    Rationale: {s['rationale'][:80]}...")

    loop.close()

    # Cleanup demo db
    if os.path.exists(db_path):
        os.remove(db_path)

    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
