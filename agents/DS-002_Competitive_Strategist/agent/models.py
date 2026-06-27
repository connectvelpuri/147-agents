from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StrategicDirection(Enum):
    DIFFERENTIATE = "differentiate"
    NEUTRALIZE = "neutralize"
    CEDE = "cede"


class CompetitorStrength(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


@dataclass
class CompetitorProfile:
    name: str
    strength: CompetitorStrength
    differentiators: list[str]
    vulnerabilities: list[str]
    typical_positioning: str
    win_rate_against_us: float = 0.0


@dataclass
class LandscapeAssessment:
    competitors: list[CompetitorProfile]
    our_advantages: list[str]
    our_vulnerabilities: list[str]
    buyer_priorities: list[str]
    summary: str


@dataclass
class PositioningStrategy:
    direction: StrategicDirection
    primary_narrative: str
    strength_exploitation: list[str]
    weakness_mitigation: list[str]
    key_messages: list[str]
    risk_points: list[str]
