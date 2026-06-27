from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProcurementTactic(Enum):
    GOOD_COP_BAD_COP = "good_cop_bad_cop"
    NIBBLING = "nibbling"
    DEADLINE_PRESSURE = "deadline_pressure"
    REOPENING_CLOSED = "reopening_closed"
    WALK_AWAY_THREAT = "walk_away_threat"
    STANDARD_TERMS_PUSH = "standard_terms_push"
    SILENCE_PLOYS = "silence_ploys"
    SPLITTING_DIFFERENCE = "splitting_difference"
    DELAY_TACTIC = "delay_tactic"
    LIMITED_AUTHORITY = "limited_authority"
    OTHER = "other"


class TacticSeverity(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TacticAlert:
    tactic: ProcurementTactic
    severity: TacticSeverity
    evidence: str
    confidence: float


@dataclass
class CounterStrategy:
    tactic: ProcurementTactic
    alert: str
    immediate_response: str
    fallback_position: str
    escalation_trigger: str
