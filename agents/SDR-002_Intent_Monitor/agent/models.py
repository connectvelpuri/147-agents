from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class SignalType(str, Enum):
    JOB_CHANGE = "job_change"
    FUNDING = "funding"
    TECHNOLOGY = "technology"
    CONTENT = "content"
    COMPETITOR = "competitor"
    PUBLISHING = "publishing"
    EVENT = "event"
    SOCIAL = "social"


class SignalSource(str, Enum):
    LINKEDIN = "linkedin"
    CRUNCHBASE = "crunchbase"
    BUILTWITH = "builtwith"
    G2 = "g2"
    RSS = "rss"
    COMPANY_BLOG = "company_blog"
    NEWS = "news"
    TWITTER = "twitter"
    WEBSITE = "website"
    REDDIT = "reddit"
    INTERNAL = "internal"


class SignalStrength(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ATL_BTL(str, Enum):
    ATL = "atl"
    BTL = "btl"


class IntentLevel(str, Enum):
    COLD = "cold"
    AWARE = "aware"
    INTERESTED = "interested"
    CONSIDERING = "considering"
    ACTIVE = "active"


# Map which signal types are ATL (conscious/rational) vs BTL (subconscious/emotional)
ATL_SIGNAL_TYPES: set[SignalType] = {
    SignalType.CONTENT,       # pricing page, demo request, trial
    SignalType.COMPETITOR,    # RFP, vendor evaluation, comparison
}

BTL_SIGNAL_TYPES: set[SignalType] = {
    SignalType.JOB_CHANGE,
    SignalType.FUNDING,
    SignalType.TECHNOLOGY,
    SignalType.PUBLISHING,
    SignalType.EVENT,
    SignalType.SOCIAL,
}

INTENT_STACK_THRESHOLDS: list[tuple[float, IntentLevel, str]] = [
    (0, IntentLevel.COLD, "No significant signals detected. Nurture or skip."),
    (20, IntentLevel.AWARE, "1-2 BTL signals. Gentle awareness building."),
    (40, IntentLevel.INTERESTED, "BTL signals or first ATL. Start sequence, BTL→ATL transition."),
    (60, IntentLevel.CONSIDERING, "ATL signal or 3+ BTL signals. Warm outreach, reference trigger."),
    (80, IntentLevel.ACTIVE, "Direct inquiry or demo request. Immediate outreach, direct ATL."),
]


@dataclass
class IntentSignal:
    signal_id: str
    deal_id: str
    contact_id: Optional[str]
    account_id: Optional[str]
    signal_type: SignalType
    source: SignalSource
    strength: SignalStrength
    confidence: float  # 0.0 - 1.0
    base_weight: float  # raw weight before decay
    effective_weight: float  # weight after time decay
    raw_text: str
    url: Optional[str]
    timestamp: datetime
    decay_factor: float = 0.85  # exponential decay per day
    topic: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def age_days(self, now: Optional[datetime] = None) -> float:
        if now is None:
            now = datetime.now()
        return max(0.0, (now - self.timestamp).total_seconds() / 86400.0)

    def recalculate_weight(self, now: Optional[datetime] = None) -> float:
        days = self.age_days(now)
        self.effective_weight = self.base_weight * (self.decay_factor ** days)
        return self.effective_weight


SIGNAL_WEIGHTS = {
    SignalType.JOB_CHANGE: 5.0,
    SignalType.FUNDING: 5.0,
    SignalType.TECHNOLOGY: 3.0,
    SignalType.CONTENT: 2.5,
    SignalType.COMPETITOR: 4.0,
    SignalType.PUBLISHING: 4.0,
    SignalType.EVENT: 2.0,
    SignalType.SOCIAL: 1.5,
}

SIGNAL_CONFIDENCE_BY_SOURCE = {
    SignalSource.LINKEDIN: 0.85,
    SignalSource.CRUNCHBASE: 0.90,
    SignalSource.BUILTWITH: 0.80,
    SignalSource.G2: 0.75,
    SignalSource.RSS: 0.65,
    SignalSource.COMPANY_BLOG: 0.70,
    SignalSource.NEWS: 0.60,
    SignalSource.TWITTER: 0.55,
    SignalSource.WEBSITE: 0.70,
    SignalSource.REDDIT: 0.50,
    SignalSource.INTERNAL: 0.95,
}

STRENGTH_BY_WEIGHT = [
    (0.0, SignalStrength.LOW),
    (2.0, SignalStrength.MEDIUM),
    (4.0, SignalStrength.HIGH),
    (7.0, SignalStrength.CRITICAL),
]


def classify_strength(effective_weight: float) -> SignalStrength:
    threshold, label = STRENGTH_BY_WEIGHT[0]
    for t, l in STRENGTH_BY_WEIGHT:
        if effective_weight >= t:
            threshold, label = t, l
    return label


@dataclass
class BuyingReadiness:
    deal_id: str
    account_id: Optional[str]
    total_score: float  # 0-100 composite
    signal_count: int
    active_signals: list[IntentSignal]
    top_signals: list[IntentSignal]
    readiness_level: str  # cold / exploring / engaged / buying
    confidence: float  # 0.0 - 1.0
    recommendation: str
    calculated_at: datetime
    trend_direction: str  # rising / stable / declining

    @staticmethod
    def from_signals(
        deal_id: str,
        signals: list[IntentSignal],
        now: Optional[datetime] = None,
    ) -> "BuyingReadiness":
        if now is None:
            now = datetime.now()

        for s in signals:
            s.recalculate_weight(now)

        total_raw = sum(s.base_weight for s in signals)
        total_effective = sum(s.effective_weight for s in signals)
        confidences = [s.confidence for s in signals]
        avg_confidence = sum(confidences) / max(len(confidences), 1)

        max_possible = 40.0
        score = min(100.0, (total_effective / max_possible) * 100.0)

        if score >= 65:
            level = "buying"
        elif score >= 40:
            level = "engaged"
        elif score >= 15:
            level = "exploring"
        else:
            level = "cold"

        sorted_signals = sorted(
            signals, key=lambda s: s.effective_weight, reverse=True
        )
        top = sorted_signals[:3]

        recent = [s for s in signals if s.age_days(now) <= 14]
        older = [s for s in signals if 14 < s.age_days(now) <= 45]
        rising = len(recent) >= len(older) and len(recent) > 0
        declining = not rising and len(older) > len(recent) * 2
        trend = "rising" if rising else ("declining" if declining else "stable")

        rec = _generate_recommendation(level, top, total_raw)

        return BuyingReadiness(
            deal_id=deal_id,
            account_id=signals[0].account_id if signals else None,
            total_score=round(score, 2),
            signal_count=len(signals),
            active_signals=signals,
            top_signals=top,
            readiness_level=level,
            confidence=round(avg_confidence, 2),
            recommendation=rec,
            calculated_at=now,
            trend_direction=trend,
        )


def _generate_recommendation(
    level: str, top: list[IntentSignal], total_raw: float
) -> str:
    has_atl = any(s.signal_type in ATL_SIGNAL_TYPES for s in top)
    has_btl = any(s.signal_type in BTL_SIGNAL_TYPES for s in top)
    style = "ATL (direct)" if has_atl else ("BTL (indirect)" if has_btl else "mixed")

    if level == "buying":
        return (
            f"Intent Stack: ACTIVE ({style}). Contact immediately. "
            "Multiple strong intent signals detected. Route to SDR-001 for immediate "
            "direct outreach referencing specific signals. "
            "Target decision-maker with value prop aligned to observed needs."
        )
    if level == "engaged":
        trigger_types = [s.signal_type.value for s in top[:2]]
        return (
            f"Intent Stack: CONSIDERING ({style}). Engage with targeted content. "
            f"Lead signals cluster around {', '.join(trigger_types)}. "
            f"Route to SDR-003 with ATL messaging. "
            f"Send relevant case studies, schedule educational touchpoint."
        )
    if level == "exploring":
        return (
            f"Intent Stack: INTERESTED ({style}). Monitor and nurture. "
            "Early intent signals detected. "
            "Route to SDR-003 with BTL→ATL sequencing. "
            "Watch for signal acceleration before direct outreach."
        )
    return (
        f"Intent Stack: COLD. "
        "No significant intent signals detected. Maintain general awareness, "
        "revisit account research. Consider adding to broader ABM campaign."
    )


@dataclass
class OutreachTrigger:
    trigger_id: str
    deal_id: str
    contact_id: Optional[str]
    signal_type: SignalType
    source: SignalSource
    strength: SignalStrength
    readiness_score: float
    recommended_action: str
    recommended_channel: str
    priority: int  # 1-5 (1 = immediate)
    message_suggestion: str
    triggered_at: datetime
    raw_signal: IntentSignal


@dataclass
class SignalAggregation:
    period: str  # daily, weekly
    start_date: datetime
    end_date: datetime
    total_signals: int
    by_type: dict[str, int]
    by_source: dict[str, int]
    top_accounts: list[dict]
    top_topics: list[tuple[str, int]]
    summary: str


@dataclass
class IntentTrend:
    trend_id: str
    topic: str
    signal_count: int
    period_days: int
    growth_rate: float  # % change vs prior period
    accounts_affected: list[str]
    severity: str  # normal / elevated / critical
    recommendation: str
    detected_at: datetime
