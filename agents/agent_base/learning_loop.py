"""
Agent Self-Improvement Learning Loop System
============================================

A complete learning loop for autonomous agent improvement. The loop enables agents to:

  1. Generate output
  2. Evaluate output against quality criteria (5 dimensions)
  3. Analyze low-scoring runs and derive corrective lessons
  4. Persist lessons in SQLite for cross-agent sharing
  5. Automatically inject relevant lessons into future prompts
  6. Reflect across all stored lessons to identify systemic patterns

Classes:
    QualityScorer     — Scores agent outputs 0–10 on five quality dimensions.
    ExperienceReplay  — Stores and replays past experiences with attention weights.
    LessonStore       — Persists lessons in SQLite, supports cross-agent sharing.
    LearningLoop      — Orchestrates the full self-improvement cycle.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import textwrap
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DIMENSIONS = ("relevance", "accuracy", "completeness", "actionability", "methodology")
"""The five quality dimensions used by the default scorer."""

MAX_SCORE = 10
"""Maximum score for any single dimension."""

MIN_SCORE = 0
"""Minimum score for any single dimension."""

LOW_SCORE_THRESHOLD = 5
"""Scores at or below this threshold trigger automatic lesson generation."""

DEFAULT_DB_PATH = "~/.hermes/learning_loop.db"
"""Default SQLite database path for lesson persistence."""

MAX_LESSONS_INJECTED = 5
"""Maximum number of lessons injected into a single prompt."""

SCORE_WEIGHT_DEFAULT = {
    "relevance": 1.0,
    "accuracy": 1.0,
    "completeness": 1.0,
    "actionability": 1.0,
    "methodology": 1.0,
}
"""Default equal weights for the composite quality score."""

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class QualityScore:
    """Container for a multi-dimensional quality evaluation.

    Attributes:
        relevance:     How relevant the output is to the prompt/context (0-10).
        accuracy:      Factual correctness and absence of errors (0-10).
        completeness:  Whether the output addresses all parts of the request (0-10).
        actionability: How easily the output can be acted upon (0-10).
        methodology:   Quality of reasoning, structure, and approach (0-10).
        metadata:      Optional dict for scorer-specific extra data (e.g. sub-scores).
        timestamp:     Unix timestamp when the score was recorded.
    """

    relevance: float = 0.0
    accuracy: float = 0.0
    completeness: float = 0.0
    actionability: float = 0.0
    methodology: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        """Clamp all dimension scores to [MIN_SCORE, MAX_SCORE]."""
        for dim in DEFAULT_DIMENSIONS:
            raw = getattr(self, dim)
            clamped = max(MIN_SCORE, min(MAX_SCORE, float(raw)))
            object.__setattr__(self, dim, clamped)

    def is_low(self, threshold: float = LOW_SCORE_THRESHOLD) -> bool:
        """Return True if any dimension falls at or below *threshold*."""
        return any(getattr(self, dim) <= threshold for dim in DEFAULT_DIMENSIONS)

    def composite(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Weighted average of all five dimensions.

        Args:
            weights: Per-dimension weights (defaults to equal weighting).

        Returns:
            Composite score in [0, 10].
        """
        w = weights or SCORE_WEIGHT_DEFAULT
        total_weight = sum(w.get(d, 1.0) for d in DEFAULT_DIMENSIONS)
        weighted_sum = sum(getattr(self, d) * w.get(d, 1.0) for d in DEFAULT_DIMENSIONS)
        return weighted_sum / total_weight

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-safe dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QualityScore":
        """Deserialize from a dictionary (safe for JSON round-trips)."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def __str__(self) -> str:
        parts = [f"{d}={getattr(self, d):.1f}" for d in DEFAULT_DIMENSIONS]
        return f"QualityScore({', '.join(parts)}, composite={self.composite():.1f})"


@dataclass
class Experience:
    """A single agent run captured for learning.

    Attributes:
        experience_id: Unique identifier (UUID4).
        agent_id:      Identifier of the agent that generated the output.
        prompt:        The input prompt or context.
        output:        The output generated by the agent.
        score:         Quality evaluation of the output.
        analysis:      Free-text analysis of shortcomings (if score was low).
        lesson:        The corrective lesson derived from this experience.
        tags:          Arbitrary tags for categorisation and search.
        timestamp:     Unix timestamp when the experience was recorded.
        metadata:      Additional structured data (e.g. model, temperature).
    """

    experience_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    agent_id: str = ""
    prompt: str = ""
    output: str = ""
    score: Optional[QualityScore] = None
    analysis: str = ""
    lesson: str = ""
    tags: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-safe dictionary."""
        d = asdict(self)
        d["score"] = self.score.to_dict() if self.score else None
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experience":
        """Deserialize from a dictionary."""
        score_data = data.pop("score", None)
        exp = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        if score_data:
            exp.score = QualityScore.from_dict(score_data)
        return exp


# ---------------------------------------------------------------------------
# QualityScorer
# ---------------------------------------------------------------------------


class QualityScorer:
    """Evaluates agent output on five quality dimensions.

    Each dimension is scored 0-10.  By default a simple heuristic scorer is
    used, but callers may supply a custom *scorer_fn* for LLM-based or more
    sophisticated evaluation.

    The five dimensions are:
      - **relevance**:     Does the output directly address the prompt?
      - **accuracy**:      Are facts, code, and statements correct?
      - **completeness**:  Does it cover all aspects of the request?
      - **actionability**: Can the user (or another agent) act on this directly?
      - **methodology**:   Is the reasoning / structure sound?

    Usage::

        scorer = QualityScorer()
        score = scorer.score(prompt="Write a Python sort function",
                             output="def sort(lst): return sorted(lst)")
        print(score.composite())
    """

    def __init__(
        self,
        scorer_fn: Optional[Callable[[str, str], Dict[str, float]]] = None,
        weights: Optional[Dict[str, float]] = None,
    ) -> None:
        """Initialize the QualityScorer.

        Args:
            scorer_fn: Optional custom scoring function that accepts
                ``(prompt, output)`` and returns a dict with keys for each
                dimension.  If ``None``, a simple rule-based heuristic is used.
            weights: Per-dimension weights for the composite score. Defaults
                to equal weighting.
        """
        self._scorer_fn = scorer_fn or self._default_scorer
        self._weights = weights or SCORE_WEIGHT_DEFAULT
        self._call_count: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(
        self,
        prompt: str,
        output: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> QualityScore:
        """Score *output* given *prompt*.

        Args:
            prompt:   The original prompt / context.
            output:   The agent's generated output.
            metadata: Optional extra data to attach to the score (e.g. model
                      name, temperature, token count).

        Returns:
            A :class:`QualityScore` instance.
        """
        self._call_count += 1
        raw = self._scorer_fn(prompt, output)
        raw = {k: float(v) for k, v in raw.items() if k in DEFAULT_DIMENSIONS}
        # Fill missing dimensions with 0
        for dim in DEFAULT_DIMENSIONS:
            raw.setdefault(dim, 0.0)
        raw["metadata"] = metadata or {}
        return QualityScore(**raw)

    def score_batch(
        self,
        pairs: Sequence[Tuple[str, str]],
        metadata_list: Optional[Sequence[Optional[Dict[str, Any]]]] = None,
    ) -> List[QualityScore]:
        """Score multiple prompt/output pairs at once.

        Args:
            pairs:         Sequence of ``(prompt, output)`` tuples.
            metadata_list: Optional per-item metadata.

        Returns:
            List of :class:`QualityScore` instances.
        """
        results: List[QualityScore] = []
        mlist = metadata_list or [None] * len(pairs)
        for (prompt, output), meta in zip(pairs, mlist):
            results.append(self.score(prompt, output, meta))
        return results

    @property
    def call_count(self) -> int:
        """Total number of scoring calls made through this instance."""
        return self._call_count

    # ------------------------------------------------------------------
    # Default heuristic scorer
    # ------------------------------------------------------------------

    @staticmethod
    def _default_scorer(prompt: str, output: str) -> Dict[str, float]:
        """Simple rule-based scorer for demonstration / CI use.

        **Important**: For production use, replace with an LLM-based or
        carefully tuned custom scorer.  The heuristic below is intentionally
        simplistic and will not capture semantic quality accurately.

        Heuristics used:
          - Relevance   : presence of prompt keywords in the output.
          - Accuracy    : placeholder - always returns 8.0 (requires LLM).
          - Completeness: output length ratio relative to prompt length
                          (capped so very long outputs don't dominate).
          - Actionability: presence of code blocks, bullet lists, or
                           numbered steps.
          - Methodology : structural cues (headings, numbered sections,
                          markdown formatting).
        """
        scores: Dict[str, float] = {}

        # --- relevance: keyword overlap -----------------------------------
        prompt_words = set(prompt.lower().split())
        output_words = set(output.lower().split())
        if prompt_words:
            overlap = len(prompt_words & output_words) / len(prompt_words)
        else:
            overlap = 0.0
        scores["relevance"] = round(overlap * MAX_SCORE, 1)

        # --- accuracy: placeholder ----------------------------------------
        scores["accuracy"] = 8.0

        # --- completeness: length ratio heuristic -------------------------
        prompt_len = len(prompt.split())
        output_len = len(output.split())
        if prompt_len == 0:
            ratio = 1.0
        else:
            ratio = min(output_len / prompt_len, 2.0) / 2.0  # normalised 0-1
        scores["completeness"] = round(ratio * MAX_SCORE, 1)

        # --- actionability: structural cues --------------------------------
        actionable_cues = 0
        if "```" in output:
            actionable_cues += 3
        if output.count("- ") > 2:
            actionable_cues += 2
        if any(output.startswith(str(n) + ".") for n in range(1, 10)):
            actionable_cues += 2
        if "|" in output and "---" in output:  # markdown table
            actionable_cues += 1
        scores["actionability"] = round(min(actionable_cues, MAX_SCORE), 1)

        # --- methodology: structure ---------------------------------------
        method_cues = 0
        if "##" in output or "**" in output:
            method_cues += 2
        if output.count("\n\n") > 3:
            method_cues += 2
        if any(marker in output for marker in ("1.", "2.", "3.", "First", "Second")):
            method_cues += 3
        if output.count("```") >= 2:
            method_cues += 2
        scores["methodology"] = round(min(method_cues, MAX_SCORE), 1)

        return scores


# ---------------------------------------------------------------------------
# ExperienceReplay
# ---------------------------------------------------------------------------


class ExperienceReplay:
    """Stores and replays past agent experiences for training / fine-tuning.

    Inspired by experience replay in reinforcement learning, this buffer
    retains past ``(prompt, output, score)`` triples and supports weighted
    sampling so that low-scoring (high-learning-value) experiences are
    replayed more often.

    Features:
      - Fixed-size circular buffer (FIFO eviction).
      - Weighted sampling where low-scoring experiences have higher weight.
      - Optional decay factor to gradually prioritise newer experiences.
      - Batch retrieval for replay-augmented prompting.

    Usage::

        replay = ExperienceReplay(capacity=1000)
        replay.add(experience)
        batch = replay.sample(batch_size=5, strategy="weighted")
    """

    def __init__(
        self,
        capacity: int = 10_000,
        decay: float = 0.99,
        default_weight: float = 2.0,
    ) -> None:
        """Initialize the replay buffer.

        Args:
            capacity: Maximum number of experiences to retain (FIFO).
            decay:    Multiplicative decay factor applied to sampling weights
                      each time a new experience is added (to age older ones).
            default_weight: Base weight for experiences lacking a score.
        """
        self._capacity = max(capacity, 1)
        self._decay = decay
        self._default_weight = default_weight
        self._buffer: List[Experience] = []
        self._weights: List[float] = []
        self._lock = Lock()
        self._total_added: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, experience: Experience) -> None:
        """Append a single experience to the buffer.

        If the buffer is at capacity, the oldest experience is evicted (FIFO).
        A decay factor is applied to all existing weights to gradually
        deprioritise older entries.
        """
        with self._lock:
            if len(self._buffer) >= self._capacity:
                self._buffer.pop(0)
                self._weights.pop(0)

            # Compute initial weight: lower composite score => higher weight
            if experience.score is not None:
                composite = experience.score.composite()
                # Invert: low score => high weight; floor at 1.0
                w = max(1.0, (MAX_SCORE - composite) + 1.0)
            else:
                w = self._default_weight

            # Decay existing weights
            self._weights = [w * self._decay for w in self._weights]

            self._buffer.append(experience)
            self._weights.append(w)
            self._total_added += 1

    def add_batch(self, experiences: Sequence[Experience]) -> None:
        """Add multiple experiences in one call."""
        for exp in experiences:
            self.add(exp)

    def sample(
        self,
        batch_size: int = 5,
        strategy: str = "weighted",
    ) -> List[Experience]:
        """Sample a batch of experiences from the buffer.

        Args:
            batch_size: Number of experiences to sample.
            strategy:   One of ``"weighted"`` (probabilistic by inverse-score),
                        ``"recent"`` (most recent first), or ``"uniform"``.

        Returns:
            List of sampled experiences (may be shorter than *batch_size* if
            the buffer has fewer items).
        """
        with self._lock:
            n = len(self._buffer)
            if n == 0:
                return []
            k = min(batch_size, n)

            if strategy == "recent":
                return list(reversed(self._buffer[-k:]))
            elif strategy == "uniform":
                import random
                return random.sample(self._buffer, k)
            else:  # weighted
                import random
                total = sum(self._weights)
                if total == 0:
                    probs = [1.0 / n] * n
                else:
                    probs = [w / total for w in self._weights]
                indices = list(range(n))
                chosen = random.choices(indices, weights=probs, k=k)
                return [self._buffer[i] for i in chosen]

    def sample_for_prompt(
        self,
        prompt: str,
        batch_size: int = 3,
        strategy: str = "weighted",
    ) -> List[Experience]:
        """Sample experiences relevant to *prompt* by keyword overlap.

        This is useful for retrieving past lessons that relate to the
        current task before injecting them into a prompt.
        """
        prompt_words = set(prompt.lower().split())
        scored: List[Tuple[float, int]] = []

        with self._lock:
            for idx, exp in enumerate(self._buffer):
                exp_words = set(exp.prompt.lower().split())
                overlap = len(prompt_words & exp_words)
                if overlap > 0:
                    score_val = overlap + self._weights[idx] * 0.1
                    scored.append((score_val, idx))

        if not scored:
            return []

        scored.sort(key=lambda x: x[0], reverse=True)
        top_indices = [idx for _, idx in scored[:batch_size]]
        return [self._buffer[i] for i in top_indices]

    def clear(self) -> None:
        """Remove all experiences from the buffer."""
        with self._lock:
            self._buffer.clear()
            self._weights.clear()

    @property
    def size(self) -> int:
        """Current number of experiences in the buffer."""
        return len(self._buffer)

    @property
    def total_added(self) -> int:
        """Total experiences ever added (including evicted ones)."""
        return self._total_added

    def stats(self) -> Dict[str, Any]:
        """Return summary statistics about the buffer.

        Returns:
            Dict with keys: size, capacity, total_added, avg_composite_score,
            min_score, max_score, dimension_averages.
        """
        with self._lock:
            n = len(self._buffer)
            if n == 0:
                return {"size": 0, "capacity": self._capacity, "total_added": self._total_added}

            composites = []
            dim_sums: Dict[str, float] = {d: 0.0 for d in DEFAULT_DIMENSIONS}
            for exp in self._buffer:
                if exp.score:
                    composites.append(exp.score.composite())
                    for d in DEFAULT_DIMENSIONS:
                        dim_sums[d] += getattr(exp.score, d)

            return {
                "size": n,
                "capacity": self._capacity,
                "total_added": self._total_added,
                "avg_composite_score": sum(composites) / len(composites) if composites else 0.0,
                "min_score": min(composites) if composites else 0.0,
                "max_score": max(composites) if composites else 0.0,
                "dimension_averages": {
                    d: round(dim_sums[d] / n, 2) for d in DEFAULT_DIMENSIONS
                },
            }


# ---------------------------------------------------------------------------
# LessonStore
# ---------------------------------------------------------------------------


class LessonStore:
    """Persistent SQLite-backed store for agent lessons with cross-agent sharing.

    A *lesson* is a corrective insight derived from a low-scoring run.  Lessons
    are stored in a local SQLite database and can be:

      - Queried by agent, tag, dimension, or time range.
      - Shared across agents (each lesson carries an ``agent_id``).
      - Automatically injected into future prompts as context.
      - Reflected upon to detect systemic weaknesses.

    Database schema::

        lessons (
            id              TEXT PRIMARY KEY,
            agent_id        TEXT NOT NULL,
            prompt          TEXT NOT NULL,
            output          TEXT,
            lesson_text     TEXT NOT NULL,
            analysis        TEXT,
            dimension       TEXT,
            score_composite REAL,
            tags            TEXT,          -- JSON array
            created_at      REAL,
            updated_at      REAL,
            shared_count    INTEGER DEFAULT 0,
            metadata        TEXT           -- JSON object
        )

    Usage::

        store = LessonStore(db_path="~/my_lessons.db")
        store.save(experience)
        lessons = store.query(agent_id="agent-42", tags=["code"])
        context = store.format_for_prompt(prompt="write a sort function")
    """

    _instance: Optional["LessonStore"] = None
    _instance_lock: Lock = Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "LessonStore":
        """Singleton per database path (not strictly enforced, but advised)."""
        return super().__new__(cls)

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Connect to (or create) the SQLite lesson database.

        Args:
            db_path: Filesystem path to the SQLite database file.  If ``None``,
                     uses ``DEFAULT_DB_PATH``.  ``~`` is expanded to the user's
                     home directory.  Parent directories are created if needed.
        """
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._db_path = self._resolve_path(db_path or DEFAULT_DB_PATH)
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._conn: sqlite3.Connection = self._create_connection()
        self._lock = Lock()
        self._create_schema()
        self._initialized = True
        logger.info("LessonStore initialised at %s", self._db_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(self, experience: Experience) -> str:
        """Persist a lesson from an experience.

        If the experience has a non-empty *lesson* field, it is saved.
        Otherwise, no row is inserted (the method returns an empty string).

        Args:
            experience: The experience to extract a lesson from.

        Returns:
            The lesson ID if a lesson was saved, or an empty string.
        """
        lesson_text = experience.lesson
        if not lesson_text or not lesson_text.strip():
            return ""

        lesson_id = uuid.uuid4().hex
        now = time.time()

        with self._lock:
            self._conn.execute(
                """
                INSERT INTO lessons
                    (id, agent_id, prompt, output, lesson_text, analysis,
                     dimension, score_composite, tags, created_at, updated_at,
                     shared_count, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lesson_id,
                    experience.agent_id,
                    experience.prompt[:10_000],
                    experience.output[:50_000] if experience.output else "",
                    lesson_text,
                    experience.analysis[:20_000] if experience.analysis else "",
                    self._infer_dimension(experience),
                    experience.score.composite() if experience.score else None,
                    json.dumps(experience.tags),
                    now,
                    now,
                    0,
                    json.dumps(experience.metadata),
                ),
            )
            self._conn.commit()

        logger.debug("Saved lesson %s for agent %s", lesson_id, experience.agent_id)
        return lesson_id

    def query(
        self,
        agent_id: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        dimensions: Optional[Sequence[str]] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        since: Optional[float] = None,
        until: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
        order_by: str = "created_at DESC",
    ) -> List[Dict[str, Any]]:
        """Search stored lessons with flexible filters.

        Args:
            agent_id:   Filter by agent identifier.
            tags:       Filter by tags (any match; AND logic with multiple tags).
            dimensions: Filter by quality dimension (any match).
            min_score:  Minimum composite score (inclusive).
            max_score:  Maximum composite score (inclusive).
            since:      Unix timestamp -- include only lessons created at or after.
            until:      Unix timestamp -- include only lessons created before or at.
            limit:      Maximum rows to return.
            offset:     Row offset for pagination.
            order_by:   SQL ``ORDER BY`` clause (sanitised to allowed values).

        Returns:
            List of lesson dicts.
        """
        # Build WHERE clause
        conditions: List[str] = []
        params: List[Any] = []

        if agent_id is not None:
            conditions.append("agent_id = ?")
            params.append(agent_id)

        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")

        if dimensions:
            dim_conditions = " OR ".join("dimension = ?" for _ in dimensions)
            conditions.append(f"({dim_conditions})")
            params.extend(dimensions)

        if min_score is not None:
            conditions.append("score_composite >= ?")
            params.append(min_score)

        if max_score is not None:
            conditions.append("score_composite <= ?")
            params.append(max_score)

        if since is not None:
            conditions.append("created_at >= ?")
            params.append(since)

        if until is not None:
            conditions.append("created_at <= ?")
            params.append(until)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # Sanitise ORDER BY
        allowed_orders = {
            "created_at DESC", "created_at ASC",
            "updated_at DESC", "updated_at ASC",
            "score_composite DESC", "score_composite ASC",
            "shared_count DESC", "shared_count ASC",
        }
        if order_by not in allowed_orders and not order_by.startswith("created_at"):
            order_by = "created_at DESC"

        sql = f"""
            SELECT id, agent_id, prompt, output, lesson_text, analysis,
                   dimension, score_composite, tags, created_at, updated_at,
                   shared_count, metadata
            FROM lessons
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def query_by_tag(self, tag: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Convenience method to query lessons by a single tag."""
        return self.query(tags=[tag], limit=limit)

    def get_lesson(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single lesson by its ID."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM lessons WHERE id = ?", (lesson_id,)
            ).fetchone()
        return self._row_to_dict(row) if row else None

    def share_lesson(self, lesson_id: str, target_agent_id: str) -> bool:
        """Share a lesson with another agent by creating a tagged copy.

        This increments the ``shared_count`` on the original lesson and
        inserts a new row with the same content but the target agent's ID
        and a ``shared`` tag.

        Args:
            lesson_id:      The ID of the lesson to share.
            target_agent_id: The recipient agent's identifier.

        Returns:
            ``True`` if sharing succeeded, ``False`` if the lesson was not found.
        """
        lesson = self.get_lesson(lesson_id)
        if lesson is None:
            return False

        new_id = uuid.uuid4().hex
        now = time.time()
        existing_tags: List[str] = json.loads(lesson.get("tags", "[]") or "[]")
        updated_tags = list(set(existing_tags + ["shared", f"shared_by:{lesson['agent_id']}"]))

        with self._lock:
            self._conn.execute(
                """
                INSERT INTO lessons
                    (id, agent_id, prompt, output, lesson_text, analysis,
                     dimension, score_composite, tags, created_at, updated_at,
                     shared_count, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """,
                (
                    new_id,
                    target_agent_id,
                    lesson["prompt"],
                    lesson["output"],
                    lesson["lesson_text"],
                    lesson["analysis"],
                    lesson["dimension"],
                    lesson["score_composite"],
                    json.dumps(updated_tags),
                    now,
                    now,
                    json.dumps(lesson.get("metadata", {})),
                ),
            )
            # Increment shared_count on original
            self._conn.execute(
                "UPDATE lessons SET shared_count = shared_count + 1 WHERE id = ?",
                (lesson_id,),
            )
            self._conn.commit()

        logger.info(
            "Shared lesson %s from %s to %s",
            lesson_id,
            lesson["agent_id"],
            target_agent_id,
        )
        return True

    def share_batch(
        self, lesson_ids: Sequence[str], target_agent_id: str
    ) -> Dict[str, bool]:
        """Share multiple lessons at once.

        Returns:
            Dict mapping lesson_id -> success boolean.
        """
        return {lid: self.share_lesson(lid, target_agent_id) for lid in lesson_ids}

    def format_for_prompt(
        self,
        prompt: str,
        agent_id: Optional[str] = None,
        max_lessons: int = MAX_LESSONS_INJECTED,
    ) -> str:
        """Retrieve and format relevant lessons as prompt context.

        Lessons are selected by keyword overlap with *prompt*, then
        formatted as a concise text block suitable for injection into the
        system or user prompt.

        Args:
            prompt:      The current prompt to find relevant lessons for.
            agent_id:    If provided, only lessons for this agent are
                         considered (plus any shared lessons).
            max_lessons: Maximum number of lessons to include.

        Returns:
            A formatted string ready for prompt injection, or an empty string
            if no relevant lessons exist.
        """
        # Collect candidates
        candidates: List[Dict[str, Any]] = []
        if agent_id:
            candidates.extend(self.query(agent_id=agent_id, limit=100))
        candidates.extend(self.query(limit=100))

        # Deduplicate by lesson_text
        seen: set = set()
        unique: List[Dict[str, Any]] = []
        for c in candidates:
            key = c["lesson_text"][:200]
            if key not in seen:
                seen.add(key)
                unique.append(c)

        # Score by keyword overlap with prompt
        prompt_words = set(prompt.lower().split())
        scored: List[Tuple[float, Dict[str, Any]]] = []
        for lesson in unique:
            text_words = set(lesson["lesson_text"].lower().split())
            prompt_words_in_lesson = set(lesson["prompt"].lower().split())
            overlap = len(prompt_words & prompt_words_in_lesson) + 0.5 * len(
                prompt_words & text_words
            )
            if overlap > 0:
                scored.append((overlap, lesson))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max_lessons]

        if not top:
            return ""

        lines = [
            "--- Past Lessons (auto-injected) ---",
        ]
        for i, (_, lesson) in enumerate(top, 1):
            dim = lesson.get("dimension") or "general"
            lines.append(
                f"  {i}. [{dim}] {lesson['lesson_text'][:500]}"
            )
        lines.append("--- End Lessons ---")
        return "\n".join(lines)

    def reflect(
        self,
        agent_id: Optional[str] = None,
        group_by: str = "dimension",
        min_occurrences: int = 2,
    ) -> Dict[str, Any]:
        """Analyse patterns across all stored lessons to identify systemic issues.

        This is the meta-cognitive 'reflect' method that examines the
        collection of lessons as a whole and returns a structured analysis
        including:

          - Most common weakness dimensions.
          - Frequent keywords / topics in low-scoring outputs.
          - Improvement trends over time.
          - Cross-agent lesson overlap.

        Args:
            agent_id:        If set, restrict analysis to lessons from this agent.
            group_by:        Group results by ``"dimension"`` or ``"tag"``.
            min_occurrences: Minimum occurrences for a pattern to be reported.

        Returns:
            A dict with reflection results.
        """
        lessons = self.query(
            agent_id=agent_id,
            limit=10_000,
            order_by="created_at ASC",
        )

        if not lessons:
            return {
                "total_lessons": 0,
                "message": "No lessons stored yet. Run more cycles to gather data.",
            }

        result: Dict[str, Any] = {
            "total_lessons": len(lessons),
            "total_agents": len(set(l["agent_id"] for l in lessons if l["agent_id"])),
            "time_span_days": self._compute_time_span_days(lessons),
        }

        # --- Dimension breakdown ---
        dim_counter: Counter = Counter()
        for l in lessons:
            dim = l.get("dimension") or "unknown"
            dim_counter[dim] += 1
        result["dimension_breakdown"] = dict(
            dim_counter.most_common()
        )

        # --- Most common weakness dimensions (low-score clusters) ---
        low_score_lessons = [l for l in lessons if (l.get("score_composite") or 10) <= 5]
        low_dim_counter: Counter = Counter()
        for l in low_score_lessons:
            dim = l.get("dimension") or "unknown"
            low_dim_counter[dim] += 1
        result["weakness_clusters"] = dict(
            low_dim_counter.most_common()
        )

        # --- Keyword frequency in lesson texts ---
        word_counter: Counter = Counter()
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "above",
            "below", "between", "out", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where",
            "why", "how", "all", "each", "every", "both", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only",
            "own", "same", "so", "than", "too", "very", "just", "because",
            "and", "but", "or", "if", "while", "that", "this", "it", "its",
            "i", "me", "my", "we", "our", "you", "your", "he", "she", "they",
            "them", "their", "what", "which", "who", "whom",
        }
        for l in lessons:
            words = l["lesson_text"].lower().split()
            for w in words:
                w_clean = w.strip(".,!?;:'\"()[]{}")
                if w_clean and w_clean not in stop_words and len(w_clean) > 2:
                    word_counter[w_clean] += 1
        result["frequent_topics"] = dict(
            word_counter.most_common(20)
        )

        # --- Improvement trend (score over time) ---
        scored_lessons = [
            l for l in lessons
            if l.get("score_composite") is not None
        ]
        if len(scored_lessons) >= min_occurrences:
            mid = len(scored_lessons) // 2
            first_half = [l["score_composite"] for l in scored_lessons[:mid]]
            second_half = [l["score_composite"] for l in scored_lessons[mid:]]
            result["improvement_trend"] = {
                "first_half_avg": round(sum(first_half) / len(first_half), 2),
                "second_half_avg": round(sum(second_half) / len(second_half), 2),
                "trend": (
                    "improving"
                    if sum(second_half) / len(second_half) > sum(first_half) / len(first_half)
                    else "declining" if sum(second_half) / len(second_half) < sum(first_half) / len(first_half)
                    else "stable"
                ),
            }

        # --- Cross-agent overlap ---
        if not agent_id:
            agent_ids = list(set(l["agent_id"] for l in lessons if l["agent_id"]))
            if len(agent_ids) > 1:
                # Determine shared lesson texts
                agent_lessons: Dict[str, set] = defaultdict(set)
                for l in lessons:
                    if l["agent_id"]:
                        agent_lessons[l["agent_id"]].add(l["lesson_text"][:300])
                shared_across = set.intersection(*agent_lessons.values()) if agent_lessons else set()
                result["cross_agent_overlap"] = {
                    "agents": agent_ids,
                    "shared_lesson_count": len(shared_across),
                }

        return result

    def delete_lesson(self, lesson_id: str) -> bool:
        """Delete a lesson by ID.

        Returns:
            ``True`` if a row was deleted, ``False`` otherwise.
        """
        with self._lock:
            cursor = self._conn.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
            self._conn.commit()
        return cursor.rowcount > 0

    def count(self, agent_id: Optional[str] = None) -> int:
        """Return the total number of stored lessons, optionally filtered."""
        if agent_id:
            with self._lock:
                row = self._conn.execute(
                    "SELECT COUNT(*) FROM lessons WHERE agent_id = ?", (agent_id,)
                ).fetchone()
            return row[0] if row else 0
        with self._lock:
            row = self._conn.execute("SELECT COUNT(*) FROM lessons").fetchone()
        return row[0] if row else 0

    def close(self) -> None:
        """Close the database connection."""
        if hasattr(self, "_conn") and self._conn:
            self._conn.close()
            logger.info("LessonStore connection closed.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_path(path_str: str) -> str:
        """Expand ``~`` to the user's home directory and return an absolute path."""
        return str(Path(path_str).expanduser().resolve())

    def _create_connection(self) -> sqlite3.Connection:
        """Create a SQLite connection with WAL mode for concurrency."""
        conn = sqlite3.connect(self._db_path, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        return conn

    def _create_schema(self) -> None:
        """Create the lessons table and indexes if they don't exist."""
        with self._lock:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS lessons (
                    id              TEXT PRIMARY KEY,
                    agent_id        TEXT NOT NULL,
                    prompt          TEXT NOT NULL,
                    output          TEXT,
                    lesson_text     TEXT NOT NULL,
                    analysis        TEXT,
                    dimension       TEXT,
                    score_composite REAL,
                    tags            TEXT DEFAULT '[]',
                    created_at      REAL NOT NULL,
                    updated_at      REAL NOT NULL,
                    shared_count    INTEGER DEFAULT 0,
                    metadata        TEXT DEFAULT '{}'
                );

                CREATE INDEX IF NOT EXISTS idx_lessons_agent
                    ON lessons(agent_id);
                CREATE INDEX IF NOT EXISTS idx_lessons_dimension
                    ON lessons(dimension);
                CREATE INDEX IF NOT EXISTS idx_lessons_created
                    ON lessons(created_at);
                CREATE INDEX IF NOT EXISTS idx_lessons_score
                    ON lessons(score_composite);
                CREATE INDEX IF NOT EXISTS idx_lessons_tags
                    ON lessons(tags);
                """
            )
            self._conn.commit()

    @staticmethod
    def _infer_dimension(experience: Experience) -> str:
        """Heuristically infer the primary weakness dimension from a score."""
        if experience.score is None:
            return "general"
        dims = DEFAULT_DIMENSIONS
        lowest_dim = min(dims, key=lambda d: getattr(experience.score, d))  # type: ignore[arg-type]
        return lowest_dim

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a SQLite row to a plain dictionary with JSON deserialisation."""
        d = dict(row)
        # Deserialise JSON fields
        for json_field in ("tags", "metadata"):
            if isinstance(d.get(json_field), str):
                try:
                    d[json_field] = json.loads(d[json_field])
                except (json.JSONDecodeError, TypeError):
                    d[json_field] = [] if json_field == "tags" else {}
        return d

    @staticmethod
    def _compute_time_span_days(lessons: List[Dict[str, Any]]) -> float:
        """Compute the time span covered by a list of lessons in days."""
        timestamps = [
            l["created_at"] for l in lessons if l.get("created_at")
        ]
        if len(timestamps) < 2:
            return 0.0
        return round((max(timestamps) - min(timestamps)) / 86400, 2)

    def __enter__(self) -> "LessonStore":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# LearningLoop
# ---------------------------------------------------------------------------


class LearningLoop:
    """Orchestrator for the full agent self-improvement cycle.

    The LearningLoop ties together the :class:`QualityScorer`,
    :class:`ExperienceReplay`, and :class:`LessonStore` into a cohesive
    pipeline that an agent can use to continuously improve.

    Typical usage::

        loop = LearningLoop(agent_id="my-agent")
        score = loop.evaluate(prompt="...", output="...")
        loop.record(prompt="...", output="...", score=score)
        prompt_with_lessons = loop.augment_prompt(prompt="...")
        insights = loop.reflect()
    """

    def __init__(
        self,
        agent_id: str = "default_agent",
        db_path: Optional[str] = None,
        scorer: Optional[QualityScorer] = None,
        replay_capacity: int = 10_000,
        auto_reflect_interval: int = 100,
    ) -> None:
        """Initialise the learning loop.

        Args:
            agent_id:              Unique identifier for this agent.
            db_path:               Path to the SQLite database (passed to
                                   :class:`LessonStore`).
            scorer:                A :class:`QualityScorer` instance (or a
                                   callable duck-typed equivalent).  Creates a
                                   default one if ``None``.
            replay_capacity:       Capacity of the experience replay buffer.
            auto_reflect_interval: Automatically run :meth:`reflect` every
                                   N records (set to 0 to disable).
        """
        self.agent_id = agent_id
        self.scorer = scorer or QualityScorer()
        self.replay = ExperienceReplay(capacity=replay_capacity)
        self.lesson_store = LessonStore(db_path=db_path)

        self._auto_reflect_interval = auto_reflect_interval
        self._run_count: int = 0
        self._last_reflection: Optional[Dict[str, Any]] = None
        self._session_start: float = time.time()

    # ------------------------------------------------------------------
    # Core loop methods
    # ------------------------------------------------------------------

    def evaluate(
        self,
        prompt: str,
        output: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> QualityScore:
        """Score an agent's output (step 2 of the learning loop).

        Args:
            prompt:   The original prompt.
            output:   The agent's generated output.
            metadata: Optional metadata (e.g. ``{"model": "gpt-4", "temperature": 0.7}``).

        Returns:
            A :class:`QualityScore` instance.
        """
        return self.scorer.score(prompt, output, metadata=metadata)

    def record(
        self,
        prompt: str,
        output: str,
        score: Optional[QualityScore] = None,
        analysis: str = "",
        lesson: str = "",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record an agent run and (if low-scoring) derive + store a lesson.

        This implements steps 3-4 of the learning loop: analyse low-scoring
        outputs, derive a lesson, and persist it.

        Args:
            prompt:   The original prompt.
            output:   The agent's output.
            score:    A pre-computed quality score.  If ``None``, the internal
                      scorer will evaluate the output automatically.
            analysis: Human or LLM-generated analysis of shortcomings.  If
                      empty and the score is low, a heuristic analysis will
                      be generated.
            lesson:   The corrective lesson text.  If empty and the score is
                      low, a heuristic lesson will be derived.
            tags:     Optional tags for categorisation.
            metadata: Optional extra structured data.

        Returns:
            The lesson ID if a lesson was saved, or an empty string.
        """
        # Auto-score if not provided
        if score is None:
            score = self.evaluate(prompt, output, metadata=metadata)

        # Build experience
        exp = Experience(
            agent_id=self.agent_id,
            prompt=prompt,
            output=output,
            score=score,
            analysis=analysis,
            lesson=lesson,
            tags=tags or [],
            metadata=metadata or {},
        )

        # Add to replay buffer
        self.replay.add(exp)

        # If low-scoring, auto-analyse and store lesson
        lesson_id = ""
        if score.is_low():
            if not analysis:
                exp.analysis = self._auto_analyse(score, prompt, output)
            if not lesson:
                exp.lesson = self._auto_derive_lesson(exp.analysis, score)
            lesson_id = self.lesson_store.save(exp)

        self._run_count += 1

        # Auto-reflect if interval reached
        if self._auto_reflect_interval > 0 and self._run_count % self._auto_reflect_interval == 0:
            self._last_reflection = self.reflect()

        return lesson_id

    def record_batch(
        self,
        experiences: Sequence[Tuple[str, str, Optional[QualityScore]]],
    ) -> List[str]:
        """Record multiple runs in batch.

        Args:
            experiences: Sequence of ``(prompt, output, score)`` tuples.

        Returns:
            List of lesson IDs (empty strings where no lesson was saved).
        """
        return [
            self.record(prompt=prompt, output=output, score=score)
            for prompt, output, score in experiences
        ]

    def augment_prompt(
        self,
        prompt: str,
        include_replay: bool = True,
        max_replay_examples: int = 3,
    ) -> str:
        """Augment *prompt* with relevant lessons and replay experiences.

        This is the prompt injection mechanism (part of the learning loop):
        relevant past lessons are formatted and prepended to the prompt so
        the agent can adjust its future behaviour.

        Args:
            prompt:              The original prompt to augment.
            include_replay:      Whether to also include relevant replay
                                 experiences.
            max_replay_examples: Maximum number of replay examples to include.

        Returns:
            The augmented prompt string (original prompt unchanged if no
            relevant lessons exist).
        """
        # 1. Lessons from the store
        lessons_text = self.lesson_store.format_for_prompt(
            prompt=prompt,
            agent_id=self.agent_id,
        )

        # 2. Relevant replay experiences
        replay_text = ""
        if include_replay:
            relevant = self.replay.sample_for_prompt(
                prompt=prompt,
                batch_size=max_replay_examples,
            )
            if relevant:
                lines = ["--- Related Past Experiences ---"]
                for i, exp in enumerate(relevant, 1):
                    score_str = str(exp.score) if exp.score else "unscored"
                    lines.append(
                        f"  {i}. [Score: {score_str}] {exp.output[:200]}"
                    )
                lines.append("--- End Experiences ---")
                replay_text = "\n".join(lines)

        # Combine
        parts = [lessons_text, replay_text]
        context = "\n\n".join(p for p in parts if p)

        if not context:
            return prompt

        return f"{context}\n\n--- Current Task ---\n{prompt}"

    def reflect(
        self,
        agent_id: Optional[str] = None,
        group_by: str = "dimension",
    ) -> Dict[str, Any]:
        """Analyse patterns across all stored lessons.

        Delegates to :meth:`LessonStore.reflect`.  Results are cached in
        ``self._last_reflection`` for access via :attr:`last_reflection`.

        Args:
            agent_id: If set, restrict to lessons from this agent.  Defaults
                      to ``self.agent_id``.
            group_by: Group results by ``"dimension"`` or ``"tag"``.

        Returns:
            A structured dict with reflection analysis (see
            :meth:`LessonStore.reflect` for details).
        """
        agent = agent_id or self.agent_id
        self._last_reflection = self.lesson_store.reflect(
            agent_id=agent,
            group_by=group_by,
        )
        return self._last_reflection

    def share_lesson(self, lesson_id: str, target_agent_id: str) -> bool:
        """Share a lesson with another agent.

        Delegates to :meth:`LessonStore.share_lesson`.
        """
        return self.lesson_store.share_lesson(lesson_id, target_agent_id)

    def share_with_siblings(self, lesson_id: str, sibling_ids: Sequence[str]) -> Dict[str, bool]:
        """Share a lesson with multiple sibling agents at once.

        Args:
            lesson_id:    The lesson to share.
            sibling_ids:  Collection of agent IDs to share with.

        Returns:
            Dict mapping agent_id -> success boolean.
        """
        return {
            sid: self.share_lesson(lesson_id, sid) for sid in sibling_ids
        }

    # ------------------------------------------------------------------
    # Status & introspection
    # ------------------------------------------------------------------

    @property
    def run_count(self) -> int:
        """Total number of agent runs recorded in this session."""
        return self._run_count

    @property
    def session_duration(self) -> float:
        """Seconds elapsed since this LearningLoop was created."""
        return time.time() - self._session_start

    @property
    def last_reflection(self) -> Optional[Dict[str, Any]]:
        """Result of the most recent :meth:`reflect` call."""
        return self._last_reflection

    def summary(self) -> Dict[str, Any]:
        """Produce a comprehensive status summary of the learning loop.

        Includes run count, replay stats, lesson count, and last reflection
        (if available).
        """
        replay_stats = self.replay.stats()
        lesson_count = self.lesson_store.count(agent_id=self.agent_id)
        total_lessons = self.lesson_store.count()

        return {
            "agent_id": self.agent_id,
            "run_count": self._run_count,
            "session_duration_seconds": round(self.session_duration, 2),
            "replay_buffer": replay_stats,
            "lessons_own": lesson_count,
            "lessons_total": total_lessons,
            "last_reflection": self._last_reflection,
            "scorer_calls": self.scorer.call_count,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _auto_analyse(
        score: QualityScore,
        prompt: str,
        output: str,
    ) -> str:
        """Generate a heuristic analysis for a low-scoring output.

        Identifies which dimensions scored lowest and provides a brief
        textual analysis.

        In production, this should be replaced by an LLM call.
        """
        dims = sorted(DEFAULT_DIMENSIONS, key=lambda d: getattr(score, d))
        lowest = dims[:3]
        parts = [
            f"Low-scoring dimensions (in order): {', '.join(lowest)}.",
            f"Composite score: {score.composite():.1f}/10.",
        ]
        for d in lowest:
            val = getattr(score, d)
            if d == "relevance" and val < 5:
                parts.append(
                    f"  - Relevance ({val:.1f}): Output may not directly address the prompt. "
                    "Consider restating the key request and verifying alignment."
                )
            elif d == "accuracy" and val < 5:
                parts.append(
                    f"  - Accuracy ({val:.1f}): Potential factual or logical errors detected. "
                    "Verify claims against reliable sources."
                )
            elif d == "completeness" and val < 5:
                parts.append(
                    f"  - Completeness ({val:.1f}): Output appears to be partial. "
                    "Check that all sub-requests are addressed."
                )
            elif d == "actionability" and val < 5:
                parts.append(
                    f"  - Actionability ({val:.1f}): Output lacks concrete, executable steps. "
                    "Provide code, commands, or numbered instructions."
                )
            elif d == "methodology" and val < 5:
                parts.append(
                    f"  - Methodology ({val:.1f}): Reasoning or structure could be improved. "
                    "Use clear sections, logical flow, or explicit step-by-step reasoning."
                )
        return " ".join(parts)

    @staticmethod
    def _auto_derive_lesson(analysis: str, score: QualityScore) -> str:
        """Derive a corrective lesson from an analysis text.

        In production, this should be replaced by an LLM summarisation step.
        """
        dims = sorted(DEFAULT_DIMENSIONS, key=lambda d: getattr(score, d))
        weakest = dims[0]
        return (
            f"IMPROVE {weakest.upper()}: When responding, pay special attention to "
            f"improving the '{weakest}' dimension. Review the analysis: {analysis[:300]}"
        )

    def close(self) -> None:
        """Close the lesson store database connection."""
        self.lesson_store.close()

    def __enter__(self) -> "LearningLoop":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Demo / self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile

    logging.basicConfig(level=logging.INFO)

    # Use a temporary database for the demo
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name

    print("=" * 60)
    print("Learning Loop Self-Test")
    print("=" * 60)

    # 1. Create the loop
    loop = LearningLoop(agent_id="demo-agent", db_path=db_path)

    # 2. Evaluate a good output
    score_good = loop.evaluate(
        prompt="Write a Python function to reverse a string.",
        output="""
Here's a Python function that reverses a string:

```python
def reverse_string(s: str) -> str:
    return s[::-1]
```

This uses Python's slice syntax with a step of -1 to reverse the string.
""",
    )
    print(f"\nGood output scored: {score_good}")

    # 3. Evaluate a poor output
    score_poor = loop.evaluate(
        prompt="Explain the difference between lists and tuples in Python.",
        output="Lists and tuples are both collections. They are different.",
    )
    print(f"Poor output scored: {score_poor}")

    # 4. Record the poor output (auto-generates lesson)
    lesson_id = loop.record(
        prompt="Explain the difference between lists and tuples in Python.",
        output="Lists and tuples are both collections. They are different.",
        score=score_poor,
        tags=["python", "data-structures"],
    )
    print(f"\nRecorded lesson ID: {lesson_id}")

    if lesson_id:
        # 5. Retrieve the lesson
        lesson = loop.lesson_store.get_lesson(lesson_id)
        if lesson:
            print(f"Lesson text: {lesson['lesson_text'][:100]}...")

    # 6. Record a few more runs to populate the buffer
    for i in range(5):
        loop.record(
            prompt=f"Sample prompt {i}",
            output=f"Sample output {i} with some content for testing purposes.",
            tags=["test"],
        )

    # 7. Augment a prompt with past lessons
    augmented = loop.augment_prompt("Explain Python decorators.")
    print(f"\nAugmented prompt length: {len(augmented)} chars")
    if augmented:
        print(f"Augmented prompt preview:\n{augmented[:500]}")

    # 8. Run reflection
    reflection = loop.reflect()
    print(f"\nReflection results:")
    for key, value in reflection.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")

    # 9. Summary
    summary = loop.summary()
    print(f"\nLoop Summary:")
    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")

    # 10. Cross-agent sharing demo
    lesson_id2 = loop.record(
        prompt="Write a SQL query to join two tables.",
        output="""
SELECT * FROM table1, table2;
""",
        tags=["sql"],
    )
    if lesson_id2:
        success = loop.share_lesson(lesson_id2, "another-agent")
        print(f"\nCross-agent sharing: {'succeeded' if success else 'failed'}")

    # Cleanup
    loop.close()
    os.unlink(db_path)

    print("\n" + "=" * 60)
    print("Self-test complete.")
    print("=" * 60)
