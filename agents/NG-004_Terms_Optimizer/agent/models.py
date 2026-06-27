from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TermCategory(Enum):
    PAYMENT = "payment"
    LIABILITY = "liability"
    SLA = "sla"
    RENEWAL = "renewal"
    IP = "ip"
    TERMINATION = "termination"
    DATA = "data"
    COMPLIANCE = "compliance"


class ImpactLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TermAnalysis:
    clause: str
    category: TermCategory
    impact: ImpactLevel
    risk: str
    recommendation: str
    market_standard: str


@dataclass
class PaymentTermsOptimization:
    current_terms: str
    recommended_terms: str
    cash_flow_impact: float
    rationale: str


@dataclass
class LiabilityExposure:
    clause: str
    exposure: str
    severity: ImpactLevel
    mitigation: str


@dataclass
class TermsOptimizationReport:
    deal_id: str
    analyses: list[TermAnalysis]
    payment_optimization: PaymentTermsOptimization | None
    liability_exposures: list[LiabilityExposure]
    priority_actions: list[str]
