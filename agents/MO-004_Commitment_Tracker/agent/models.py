"""Data models for MO-004 Commitment Tracker."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class CommitmentParty(Enum):
    BUYER = "buyer"
    SELLER = "seller"
    JOINT = "joint"


class CommitmentStatus(Enum):
    PENDING = "pending"
    FULFILLED = "fulfilled"
    MISSED = "missed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class CommitmentType(Enum):
    SEND_DOCUMENT = "send_document"
    SCHEDULE_MEETING = "schedule_meeting"
    PROVIDE_INFORMATION = "provide_information"
    INTERNAL_DISCUSSION = "internal_discussion"
    DECISION = "decision"
    INTRODUCE_STAKEHOLDER = "introduce_stakeholder"
    REVIEW_PROPOSAL = "review_proposal"
    TRIAL_EVALUATION = "trial_evaluation"
    REFERENCE_CALL = "reference_call"
    OTHER = "other"


@dataclass
class Commitment:
    commitment_id: str
    party: CommitmentParty
    description: str
    type: CommitmentType
    status: CommitmentStatus = CommitmentStatus.PENDING
    deadline: str = ""
    participant_id: str = ""
    meeting_id: str = ""
    deal_id: str = ""
    created_at: str = ""
    fulfilled_at: str = ""
    notes: str = ""
    buyer_wiifm: str = ""
    seller_wiifm: str = ""
    commitment_risk: str = "medium"


@dataclass
class CommitmentReminder:
    commitment: Commitment
    days_overdue: int = 0
    suggested_action: str = ""


@dataclass
class MissedCommitmentAlert:
    commitment: Commitment
    impact: str = ""
    suggested_recovery: str = ""


@dataclass
class CommitmentLog:
    meeting_id: str
    commitments: list[Commitment] = field(default_factory=list)
    buyer_count: int = 0
    seller_count: int = 0


@dataclass
class CommitmentAnalysisResult:
    deal_id: str
    meeting_id: str
    log: CommitmentLog
    reminders: list[CommitmentReminder] = field(default_factory=list)
    missed_alerts: list[MissedCommitmentAlert] = field(default_factory=list)
    no_commitments: bool = False
    analyzed_at: str = ""
