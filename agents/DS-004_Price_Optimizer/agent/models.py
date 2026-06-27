from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PriceSensitivity(Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


@dataclass
class PriceSensitivityProfile:
    segment: str
    sensitivity: PriceSensitivity
    willingness_to_pay: float
    discount_elasticity: float
    reference_price: float
    key_factors: list[str]


@dataclass
class PriceRecommendation:
    recommended_price: float
    rationale: str
    expected_win_rate: float
    margin_impact: float
    floor_price: float
    ceiling_price: float


@dataclass
class DiscountImpactAnalysis:
    requested_discount_pct: float
    revenue_impact: float
    margin_impact_pct: float
    break_even_units: int
    alternative_suggestions: list[str]
