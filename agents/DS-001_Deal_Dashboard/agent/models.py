"""Data models for DS-001 Deal Dashboard — VMF health scoring & MEDDIC metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class VMFRating(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


class ForecastCategory(Enum):
    COMMITTED = "committed"
    BEST_CASE = "best_case"
    PIPELINE = "pipeline"
    UPSIDE = "upside"
    OMITTED = "omitted"


class StakeholderAlignment(Enum):
    ALIGNED = "aligned"
    NEUTRAL = "neutral"
    BLOCKING = "blocking"
    UNENGAGED = "unengaged"


@dataclass
class VMFDimension:
    name: str
    rating: VMFRating
    score: float
    evidence: str
    updated_at: str = ""


@dataclass
class MEDDICMetrics:
    metrics_identified: int = 0
    economic_buyer_engaged: bool = False
    decision_criteria_clear: bool = False
    decision_process_mapped: bool = False
    identified_pain_confirmed: bool = False
    champion_confirmed: bool = False


@dataclass
class Stakeholder:
    name: str
    title: str
    sentiment: str = "neutral"
    alignment: StakeholderAlignment = StakeholderAlignment.NEUTRAL
    influence_level: float = 0.5
    last_interaction: str = ""


@dataclass
class DealHealthCard:
    deal_id: str
    overall_score: float
    dimensions: list[VMFDimension] = field(default_factory=list)
    meddic: MEDDICMetrics = field(default_factory=MEDDICMetrics)
    stakeholders: list[Stakeholder] = field(default_factory=list)
    forecast_category: ForecastCategory = ForecastCategory.PIPELINE
    risk_factors: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    generated_at: str = ""


DEAL_HEALTH_WEIGHTS: dict[str, float] = {
    "economic_buyer": 0.15,
    "negative_consequences": 0.15,
    "pbo_clarity": 0.15,
    "required_capabilities": 0.10,
    "decision_process": 0.10,
    "stakeholder_consensus": 0.15,
    "timeline_urgency": 0.10,
    "competitive_position": 0.10,
}

DIMENSION_DEFINITIONS: list[dict[str, Any]] = [
    {
        "id": "economic_buyer",
        "label": "Economic Buyer Identified & Engaged",
        "description": "Person with budget authority is known and actively engaged in the process",
        "green_if": "EB named, met 2+ times, actively discussing budget/timeline",
        "yellow_if": "EB identified but not directly engaged or only 1 meeting",
        "red_if": "EB unknown or no direct contact",
    },
    {
        "id": "negative_consequences",
        "label": "Negative Consequences of Status Quo Articulated",
        "description": "Buyer can articulate specific, personal negative consequences of not changing",
        "green_if": "Buyer personally describes pain, cost of inaction, missed opportunities",
        "yellow_if": "Generic need acknowledged but no personal cost articulated",
        "red_if": "No urgency or dissatisfaction with current state expressed",
    },
    {
        "id": "pbo_clarity",
        "label": "PBO Clarity — Preferred Business Outcome",
        "description": "Buyer has defined what success looks like in measurable terms",
        "green_if": "Clear, measurable success criteria documented with buyer agreement",
        "yellow_if": "Vague outcome stated but not yet quantified or agreed",
        "red_if": "No defined outcomes; discussion still feature-level",
    },
    {
        "id": "required_capabilities",
        "label": "Required Capabilities Validated",
        "description": "Solution capabilities mapped to buyer's stated requirements and validated",
        "green_if": "All key requirements mapped to solution, gaps acknowledged and addressed",
        "yellow_if": "Partial mapping with unresolved gaps",
        "red_if": "Requirements unclear or significant capability gaps unaddressed",
    },
    {
        "id": "decision_process",
        "label": "Decision Process Mapped",
        "description": "Buyer's internal decision-making process, timeline, and stakeholders are known",
        "green_if": "Full process mapped: stages, stakeholders, timeline, decision criteria",
        "yellow_if": "Partial map: some stakeholders or timeline gaps",
        "red_if": "No decision process visibility",
    },
    {
        "id": "stakeholder_consensus",
        "label": "Stakeholder Consensus Building",
        "description": "All key stakeholders are identified and moving toward consensus",
        "green_if": "3+ stakeholders engaged, champion active, no blockers identified",
        "yellow_if": "Key stakeholders identified but not all engaged or neutral sentiment",
        "red_if": "Single-threaded deal or known blocker with no mitigation plan",
    },
    {
        "id": "timeline_urgency",
        "label": "Timeline-Driven Urgency",
        "description": "Buyer has a stated timeline and urgency to make a decision",
        "green_if": "Clear decision timeline within 90 days tied to business event",
        "yellow_if": "General timeframe but no triggering event or >90 day horizon",
        "red_if": "No timeline or 'sometime this year' vagueness",
    },
    {
        "id": "competitive_position",
        "label": "Competitive Position Strength",
        "description": "Deal is competitive or sole-source with clear differentiation validated",
        "green_if": "Clear differentiation confirmed; buyer sees us as best option",
        "yellow_if": "Competitive evaluation underway; differentiation not fully validated",
        "red_if": "Incumbent entrenched or leading competitor identified without counter",
    },
]
