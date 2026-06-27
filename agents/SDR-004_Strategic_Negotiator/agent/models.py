"""Data models for SDR-004 Strategic Negotiator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class NegotiationPhase(Enum):
    OPENING = "opening"
    DISCOVERY = "discovery"
    VALUE_BUILDING = "value_building"
    OBJECTION_HANDLING = "objection_handling"
    CLOSING = "closing"
    POST_DEAL = "post_deal"


class NegotiationMove(Enum):
    GIVE_GET = "give_get"
    VALUE_PROGRESS = "value_progress"
    MIRROR_ATTACK = "mirror_attack"
    CALIBRATED_ABSENCE = "calibrated_absence"
    FRAME_CONTROL = "frame_control"
    CONCESSION = "concession"
    COMMITMENT = "commitment"


@dataclass
class GiveGetPair:
    give: str
    get: str
    rationale: str = ""


@dataclass
class ValueProgressFrame:
    metric: str
    current_state: str
    desired_state: str
    progress_gap: str
    value_proposition: str = ""


@dataclass
class MirrorAttack:
    their_frame: str
    mirrored_response: str
    reframe: str
    evidence: str = ""


@dataclass
class CalibratedAbsence:
    trigger: str
    silence_duration_seconds: int = 5
    expected_effect: str = ""
    fallback: str = ""


@dataclass
class DealContext:
    deal_id: str
    prospect_name: str
    prospect_title: str
    company: str
    deal_value: float = 0.0
    current_stage: str = "discovery"
    objections: list[str] = field(default_factory=list)
    stakeholders: list[str] = field(default_factory=list)
    timeline: str = ""
    competitor: str = ""
    notes: str = ""


@dataclass
class NegotiationPlan:
    deal_id: str
    context: DealContext
    phase: NegotiationPhase = NegotiationPhase.OPENING
    moves: list[NegotiationMove] = field(default_factory=list)
    give_gets: list[GiveGetPair] = field(default_factory=list)
    value_frames: list[ValueProgressFrame] = field(default_factory=list)
    mirror_attacks: list[MirrorAttack] = field(default_factory=list)
    calibrated_absences: list[CalibratedAbsence] = field(default_factory=list)
    recommended_approach: str = ""
    script: str = ""
    generated_at: str = ""


@dataclass
class NegotiationOutcome:
    plan_id: str
    moves_executed: list[NegotiationMove] = field(default_factory=list)
    accepted_gives: list[str] = field(default_factory=list)
    rejected_moves: list[str] = field(default_factory=list)
    commitment_made: bool = False
    next_steps: list[str] = field(default_factory=list)
    notes: str = ""
