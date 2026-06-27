from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConcessionType(Enum):
    PRICE = "price"
    TERMS = "terms"
    SCOPE = "scope"
    SERVICES = "services"
    TIMELINE = "timeline"
    CONTRACT = "contract"


@dataclass
class ConcessionItem:
    id: str
    type: ConcessionType
    description: str
    actual_cost: float
    perceived_value: float
    sequence_order: int
    trigger_condition: str
    framing_language: str


@dataclass
class TradeOffMatrix:
    low_cost_high_value: list[ConcessionItem]
    high_cost_high_value: list[ConcessionItem]
    low_cost_low_value: list[ConcessionItem]
    high_cost_low_value: list[ConcessionItem]


@dataclass
class ConcessionPlan:
    deal_id: str
    max_concession_depth_pct: float
    sequence: list[ConcessionItem]
    trade_off_matrix: TradeOffMatrix
    walk_away_triggers: list[str]
    pacing_guidance: str
