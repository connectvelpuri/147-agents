from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ApprovalDecision(Enum):
    APPROVED = "approved"
    DENIED = "denied"
    MODIFIED = "modified"
    ESCALATED = "escalated"


class ApprovalLevel(Enum):
    REP_LEVEL = "rep_level"
    MANAGER = "manager"
    VP = "vp"
    C_LEVEL = "c_level"
    CEO = "ceo"


@dataclass
class DiscountRequest:
    deal_id: str
    rep_name: str
    rep_role: str
    deal_value: float
    requested_discount_pct: float
    current_margin_pct: float
    competitive_pressure: str
    buyer_relationship: str
    reason: str


@dataclass
class DiscountDecision:
    deal_id: str
    decision: ApprovalDecision
    approval_level: ApprovalLevel
    approved_discount_pct: float
    rationale: str
    conditions: list[str]
    alternative_concessions: list[str]
