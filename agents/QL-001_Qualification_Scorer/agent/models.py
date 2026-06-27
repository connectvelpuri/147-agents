"""Data models for QL-001 BANT/MEDDPICC Scorer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class QualificationDimension(Enum):
    # BANT
    BUDGET = "budget"
    AUTHORITY = "authority"
    NEED = "need"
    TIMELINE = "timeline"
    # MEDDPICC extras
    METRICS = "metrics"
    ECONOMIC_BUYER = "economic_buyer"
    DECISION_CRITERIA = "decision_criteria"
    PROCESS = "process"
    IMPLICIT_PAIN = "implicit_pain"
    CHAMPION = "champion"
    COMPETITION = "competition"


class Confidence(Enum):
    CONFIRMED = "confirmed"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class DisqualificationUrgency(Enum):
    IMMEDIATE = "immediate"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class DimensionScore:
    dimension: QualificationDimension
    score: float  # 0.0 to 1.0
    confidence: Confidence
    evidence: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


@dataclass
class BANTScore:
    budget: DimensionScore
    authority: DimensionScore
    need: DimensionScore
    timeline: DimensionScore
    composite: float = 0.0

    def compute(self):
        self.composite = (
            self.budget.score * 0.25
            + self.authority.score * 0.25
            + self.need.score * 0.30
            + self.timeline.score * 0.20
        )


@dataclass
class MEDDPICCScore:
    metrics: DimensionScore
    economic_buyer: DimensionScore
    decision_criteria: DimensionScore
    process: DimensionScore
    implicit_pain: DimensionScore
    champion: DimensionScore
    competition: DimensionScore
    composite: float = 0.0

    def compute(self):
        self.composite = (
            self.metrics.score * 0.15
            + self.economic_buyer.score * 0.15
            + self.decision_criteria.score * 0.10
            + self.process.score * 0.10
            + self.implicit_pain.score * 0.20
            + self.champion.score * 0.20
            + self.competition.score * 0.10
        )


@dataclass
class L1Score:
    """Skip Miller L1: Problem Qualification."""
    pain_clarity: float = 0.0
    impact: float = 0.0
    urgency_trend: float = 0.0
    composite: float = 0.0
    qualified: bool = False
    evidence: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)

    def compute(self) -> float:
        self.composite = self.pain_clarity * 20 + self.impact * 20 + self.urgency_trend * 20
        self.qualified = self.composite >= 60
        return self.composite


@dataclass
class L2Score:
    """Skip Miller L2: Solution Qualification."""
    fit_clarity: float = 0.0
    authority_access: float = 0.0
    evaluation_readiness: float = 0.0
    composite: float = 0.0
    qualified: bool = False
    evidence: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)

    def compute(self) -> float:
        self.composite = self.fit_clarity * 30 + self.authority_access * 30 + self.evaluation_readiness * 40
        self.qualified = self.composite >= 100
        return self.composite


@dataclass
class L3Score:
    """Skip Miller L3: Buying Qualification."""
    budget: float = 0.0
    timeline: float = 0.0
    decision_process: float = 0.0
    cost_of_inaction: float = 0.0
    composite: float = 0.0
    qualified: bool = False
    evidence: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)

    def compute(self) -> float:
        self.composite = self.budget * 50 + self.timeline * 50 + self.decision_process * 50 + self.cost_of_inaction * 50
        self.qualified = self.composite >= 200
        return self.composite


@dataclass
class CustomerInputGating:
    """Paul Butterfield: Input Gating — checks if qualification is valid."""
    problem_in_own_words: bool = False
    participatory_discovery: bool = False
    questions_asked: bool = False
    time_invested: bool = False

    @property
    def gates_open(self) -> int:
        return sum([self.problem_in_own_words, self.participatory_discovery, self.questions_asked, self.time_invested])

    @property
    def all_gates_open(self) -> bool:
        return self.gates_open == 4

    @property
    def penalty(self) -> float:
        closed = 4 - self.gates_open
        return closed * 0.25


@dataclass
class QualificationResult:
    deal_id: str
    bant: BANTScore | None = None
    meddpicc: MEDDPICCScore | None = None
    miller_l1: L1Score | None = None
    miller_l2: L2Score | None = None
    miller_l3: L3Score | None = None
    input_gating: CustomerInputGating | None = None
    deal_quality_index: float = 0.0
    gaps: list[str] = field(default_factory=list)
    next_questions: list[str] = field(default_factory=list)
    disqualify: bool = False
    disqualify_reason: str = ""
    disqualify_confidence: Confidence = Confidence.UNKNOWN
    scored_at: str = ""
