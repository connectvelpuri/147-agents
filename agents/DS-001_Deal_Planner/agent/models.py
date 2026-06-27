from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class RiskSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MilestoneStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class StakeholderInfluence(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CompetitivePosition(Enum):
    STRONG_LEADER = "strong_leader"
    CONTENDING = "contending"
    VULNERABLE = "vulnerable"
    UNKNOWN = "unknown"


@dataclass
class Milestone:
    id: str
    title: str
    description: str
    due_date: str
    status: MilestoneStatus = MilestoneStatus.PENDING
    owner: str = ""
    dependencies: list[str] = field(default_factory=list)
    completion_criteria: str = ""


@dataclass
class RiskRegisterItem:
    id: str
    risk: str
    severity: RiskSeverity
    probability: float
    impact: str
    mitigation: str
    owner: str = ""


@dataclass
class StakeholderEngagementAction:
    stakeholder_name: str
    title: str
    influence: StakeholderInfluence
    current_sentiment: str
    engagement_goal: str
    message_focus: str
    proposed_action: str
    cadence: str
    notes: str = ""


@dataclass
class DealSituation:
    deal_id: str
    deal_value: float
    buyer_need: str
    stakeholders: list[dict[str, Any]]
    competitive_landscape: str
    timeline_context: str
    blockers: list[str]
    summary: str


@dataclass
class DealPlan:
    deal_id: str
    version: str
    situation: DealSituation
    milestones: list[Milestone]
    stakeholder_plan: list[StakeholderEngagementAction]
    risk_register: list[RiskRegisterItem]
    competitive_positioning: str
    critical_path: list[str]
    recommendations: list[str]
    created_at: str
    generated_by: str = "ds-001-v1"
