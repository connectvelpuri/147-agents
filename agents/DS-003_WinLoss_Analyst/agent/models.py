"""Data models for DS-003 Win/Loss Analyst — Clozd/Gong methodology."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class LossReason(Enum):
    PRICE = "price"
    PRODUCT = "product"
    RELATIONSHIP = "relationship"
    PROCESS = "process"
    NO_DECISION = "no_decision"
    COMPETITOR = "competitor"
    TIMING = "timing"
    VENDOR_RISK = "vendor_risk"
    INTERNAL_POLITICS = "internal_politics"
    OTHER = "other"


class WinReason(Enum):
    PRODUCT_FIT = "product_fit"
    RELATIONSHIP = "relationship"
    PRICE_VALUE = "price_value"
    TIMING = "timing"
    EXISTING_VENDOR = "existing_vendor"
    EXECUTIVE_PULL = "executive_pull"
    CHAMPION = "champion"
    OTHER = "other"


class PatternType(Enum):
    REPEATING_OBJECTION = "repeating_objection"
    STALLED_STAGE = "stalled_stage"
    MISSING_STAKEHOLDER = "missing_stakeholder"
    PRICE_SENSITIVITY = "price_sensitivity"
    COMPETITIVE_WEAKNESS = "competitive_weakness"
    PROCESS_FLAW = "process_flaw"
    TIMING_PATTERN = "timing_pattern"


@dataclass
class LossReasonDetail:
    primary: LossReason
    contributing: list[LossReason] = field(default_factory=list)
    description: str = ""
    evidence: str = ""
    preventability: float = 0.0


@dataclass
class WinLossRecord:
    deal_id: str
    outcome: str
    value: float = 0.0
    sales_cycle_days: int = 0
    loss_details: Optional[LossReasonDetail] = None
    win_reason: Optional[WinReason] = None
    stages_passed: list[str] = field(default_factory=list)
    stakeholder_count: int = 0
    competitive_process: bool = False
    created_at: str = ""


@dataclass
class PatternAnalysis:
    pattern_type: PatternType
    description: str
    frequency: int
    avg_impact: float
    recommendation: str = ""
    sample_deals: list[str] = field(default_factory=list)


@dataclass
class WinLossAnalysisResult:
    deal_id: str
    record: WinLossRecord
    patterns: list[PatternAnalysis] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    data_completeness: float = 0.0
    analyzed_at: str = ""


LOSS_TAXONOMY: dict[LossReason, str] = {
    LossReason.PRICE: "Price or value perception — buyer felt cost exceeded value or budget constrained",
    LossReason.PRODUCT: "Product fit — missing features, integration issues, or capability gaps",
    LossReason.RELATIONSHIP: "Relationship failure — no champion, poor rapport, or trust deficit",
    LossReason.PROCESS: "Sales process breakdown — late engagement, poor discovery, or misqualified",
    LossReason.NO_DECISION: "No decision made — evaluation paralysis, status quo maintained, or stalled",
    LossReason.COMPETITOR: "Lost to competitor — specific competitive loss with identified rival",
    LossReason.TIMING: "Timing mismatch — budget cycle, initiative deprioritized, or bad timing",
    LossReason.VENDOR_RISK: "Vendor risk concerns — security, compliance, financial viability",
    LossReason.INTERNAL_POLITICS: "Internal politics — stakeholder conflict, reorg, or priority shift",
    LossReason.OTHER: "Other — uncategorized or unique reason",
}

WIN_TAXONOMY: dict[WinReason, str] = {
    WinReason.PRODUCT_FIT: "Superior product fit — solution best addressed their needs",
    WinReason.RELATIONSHIP: "Strong relationship — champion-driven, trusted advisor dynamic",
    WinReason.PRICE_VALUE: "Best price-value ratio — perceived value exceeded cost",
    WinReason.TIMING: "Right timing — aligned with buyer's initiative cycle",
    WinReason.EXISTING_VENDOR: "Existing vendor — expansion or renewal from existing relationship",
    WinReason.EXECUTIVE_PULL: "Executive pull — C-level sponsorship drove decision",
    WinReason.CHAMPION: "Internal champion — stakeholder actively sold on our behalf",
    WinReason.OTHER: "Other — uncategorized win reason",
}
