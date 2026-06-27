"""Data models for MO-003 Objection Detector and Classifier."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ObjectionCategory(Enum):
    PRICE = "price"
    TIMING = "timing"
    AUTHORITY = "authority"
    NEED = "need"
    COMPETING_PRIORITY = "competing_priority"
    COMPETITOR = "competitor"
    SECURITY = "security"
    FIT = "fit"


class ObjectionSeverity(Enum):
    BLOCKING = "blocking"
    SIGNIFICANT = "significant"
    MINOR = "minor"


class PsychologicalBucket(Enum):
    SAFE = "safe"
    BEST = "best"
    INNOVATIVE = "innovative"


class BuyerFear(Enum):
    FEAR_OF_MISTAKE = "fear_of_mistake"
    FEAR_OF_CHANGE = "fear_of_change"
    FEAR_OF_LOSING_CREDIBILITY = "fear_of_losing_credibility"
    FEAR_OF_COMMITMENT = "fear_of_commitment"
    FEAR_OF_THE_UNKNOWN = "fear_of_the_unknown"


BUCKET_MAP: dict[ObjectionCategory, PsychologicalBucket] = {
    ObjectionCategory.PRICE: PsychologicalBucket.SAFE,
    ObjectionCategory.SECURITY: PsychologicalBucket.SAFE,
    ObjectionCategory.AUTHORITY: PsychologicalBucket.SAFE,
    ObjectionCategory.NEED: PsychologicalBucket.BEST,
    ObjectionCategory.COMPETITOR: PsychologicalBucket.BEST,
    ObjectionCategory.FIT: PsychologicalBucket.BEST,
    ObjectionCategory.TIMING: PsychologicalBucket.INNOVATIVE,
    ObjectionCategory.COMPETING_PRIORITY: PsychologicalBucket.INNOVATIVE,
}

FEAR_MAP: dict[ObjectionCategory, BuyerFear] = {
    ObjectionCategory.PRICE: BuyerFear.FEAR_OF_MISTAKE,
    ObjectionCategory.SECURITY: BuyerFear.FEAR_OF_LOSING_CREDIBILITY,
    ObjectionCategory.AUTHORITY: BuyerFear.FEAR_OF_COMMITMENT,
    ObjectionCategory.NEED: BuyerFear.FEAR_OF_CHANGE,
    ObjectionCategory.COMPETITOR: BuyerFear.FEAR_OF_MISTAKE,
    ObjectionCategory.FIT: BuyerFear.FEAR_OF_THE_UNKNOWN,
    ObjectionCategory.TIMING: BuyerFear.FEAR_OF_COMMITMENT,
    ObjectionCategory.COMPETING_PRIORITY: BuyerFear.FEAR_OF_CHANGE,
}

BUCKET_RESPONSE_STRATEGIES: dict[PsychologicalBucket, str] = {
    PsychologicalBucket.SAFE: (
        "Validate the concern. Offer risk reversal evidence (case studies, guarantees). "
        "Reframe: 'What if the risk is staying put?' Use social proof from similar companies. "
        "Jeff Shore CBT Step 1: 'That makes sense given what you know.'"
    ),
    PsychologicalBucket.BEST: (
        "Acknowledge the comparison need. Ask: 'What criteria matter most to you?' "
        "Provide comparative evidence. Avoid badmouthing competitors. "
        "Anchoring: Frame the comparison criteria before they do."
    ),
    PsychologicalBucket.INNOVATIVE: (
        "Validate the timing concern. Share peer adoption proof. "
        "Reframe cost of inaction: 'What does waiting cost?' "
        "Use Andy Paul Value=Progress: 'How much progress could you make in 30 days?'"
    ),
}

FEAR_RESPONSE_STRATEGIES: dict[BuyerFear, str] = {
    BuyerFear.FEAR_OF_MISTAKE: (
        "Risk reversal: 'What's the worst case? A 15-minute call.' "
        "Social proof: 'Companies like yours chose this.' "
        "Limited commitment framing."
    ),
    BuyerFear.FEAR_OF_CHANGE: (
        "Loss aversion: 'What if the status quo is the real risk?' "
        "Paint the gap (Butterfield Discovery Gap) between current and possible. "
        "Show that the effort-to-impact ratio favors change."
    ),
    BuyerFear.FEAR_OF_LOSING_CREDIBILITY: (
        "Validate: 'Your team trusts you to find the best path.' "
        "Peer proof from similar roles. "
        "Frame as career-building: 'Finding a better path builds credibility.'"
    ),
    BuyerFear.FEAR_OF_COMMITMENT: (
        "Micro-commitments: 'Let's define what investigation looks like.' "
        "No long-term contract framing. "
        "Clear timeline with off-ramp: 'If it doesn't work, what's the exit?'"
    ),
    BuyerFear.FEAR_OF_THE_UNKNOWN: (
        "Transparency: 'What questions do you need answered?' "
        "Over-communicate process, timeline, expectations. "
        "Provide concrete examples, not abstract promises."
    ),
}


@dataclass
class ObjectionEvent:
    objection_id: str
    participant_id: str
    timestamp_sec: float
    category: ObjectionCategory
    severity: ObjectionSeverity
    utterance: str
    context: str = ""
    addressed: bool = False
    response_utterance: str = ""
    psychological_bucket: Optional[PsychologicalBucket] = None
    underlying_fear: Optional[BuyerFear] = None


@dataclass
class RecommendedResponse:
    category: ObjectionCategory
    strategy: str
    suggested_rebuttal: str
    source: str = ""
    psychological_bucket: Optional[PsychologicalBucket] = None
    underlying_fear: Optional[BuyerFear] = None


@dataclass
class ObjectionLog:
    meeting_id: str
    objections: list[ObjectionEvent] = field(default_factory=list)
    response_map: dict[str, RecommendedResponse] = field(default_factory=dict)


@dataclass
class UnaddressedObjectionAlert:
    objection_id: str
    participant_id: str
    category: ObjectionCategory
    severity: ObjectionSeverity
    context: str
    timestamp_sec: float


@dataclass
class ObjectionPattern:
    category: ObjectionCategory
    account_id: str
    frequency: int = 1
    first_seen: str = ""
    last_seen: str = ""
    sample_utterances: list[str] = field(default_factory=list)


@dataclass
class ObjectionAnalysisResult:
    deal_id: str
    meeting_id: str
    log: ObjectionLog
    alerts: list[UnaddressedObjectionAlert] = field(default_factory=list)
    patterns: list[ObjectionPattern] = field(default_factory=list)
    objection_count: int = 0
    blocking_count: int = 0
    addressed_count: int = 0
    analyzed_at: str = ""
