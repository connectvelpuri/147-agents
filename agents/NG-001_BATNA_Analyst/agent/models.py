"""Data models for NG-001 BATNA Analyst — Getting to Yes negotiation science."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class LeverageDirection(Enum):
    TOWARD_US = "toward_us"
    TOWARD_THEM = "toward_them"
    BALANCED = "balanced"
    UNCLEAR = "unclear"


class PowerTrend(Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"
    UNCERTAIN = "uncertain"


class OptionType(Enum):
    MULTI_YEAR = "multi_year"
    VOLUME_COMMIT = "volume_commit"
    PHASED_ROLLOUT = "phased_rollout"
    PILOT = "pilot"
    FLEXIBLE_TERMS = "flexible_terms"
    VALUE_ADD = "value_add"
    BUNDLED = "bundled"
    PER_USER = "per_user"


@dataclass
class BATNA:
    """Our best alternative to negotiated agreement (Fisher & Ury)."""
    description: str
    walkaway_value: float
    confidence: float
    alternative_details: list[str] = field(default_factory=list)
    strengthening_actions: list[str] = field(default_factory=list)


@dataclass
class TheirBATNA:
    """Their best alternative — estimated from market intelligence."""
    description: str
    estimated_walkaway_value: float
    confidence: float
    known_alternatives: list[str] = field(default_factory=list)
    weakness_signals: list[str] = field(default_factory=list)


@dataclass
class ZOPA:
    """Zone of Possible Agreement (Raiffa)."""
    our_minimum: float
    their_maximum: float
    overlap_exists: bool = False
    overlap_range: tuple[float, float] = (0.0, 0.0)
    midpoint: float = 0.0


@dataclass
class LeverageFactor:
    name: str
    direction: LeverageDirection
    weight: float
    description: str = ""


@dataclass
class PowerTimeline:
    current_leverage: str = "balanced"
    trend: PowerTrend = PowerTrend.STABLE
    factors: list[LeverageFactor] = field(default_factory=list)
    projected_change_days: int = 90
    recommendation: str = ""


@dataclass
class PricingOption:
    type: OptionType
    label: str
    description: str
    estimated_value: float
    likelihood: float
    conditions: str = ""


@dataclass
class ROIDefense:
    metric: str
    current_state: str
    projected_improvement: str
    payback_period_months: int
    five_year_roi: float
    risk_adj_roi: float
    source: str = ""


@dataclass
class NegotiationPowerProfile:
    batna: BATNA
    their_batna: TheirBATNA
    zopa: ZOPA
    leverage: list[LeverageFactor] = field(default_factory=list)
    power_timeline: Optional[PowerTimeline] = None
    pricing_options: list[PricingOption] = field(default_factory=list)
    roi_defenses: list[ROIDefense] = field(default_factory=list)
    overall_assessment: str = ""
    walkaway_guidance: str = ""
    generated_at: str = ""
