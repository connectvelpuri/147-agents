"""Data models for SDR-001 Multi-Channel Prospector."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class ICPDimension(Enum):
    COMPANY_SIZE = "company_size"
    INDUSTRY = "industry"
    REVENUE = "revenue"
    TECHNOLOGY = "technology"
    FUNDING = "funding"
    LOCATION = "location"
    EMPLOYEE_COUNT = "employee_count"
    GROWTH_RATE = "growth_rate"


class EnrichmentSource(Enum):
    ZOOMINFO = "zoominfo"
    LINKEDIN = "linkedin"
    APOLLO = "apollo"
    CLEARBIT = "clearbit"
    CRUNCHBASE = "crunchbase"
    BUILTWITH = "builtwith"


class FitLevel(Enum):
    PERFECT = "perfect"
    GOOD = "good"
    MARGINAL = "marginal"
    POOR = "poor"
    UNKNOWN = "unknown"


class TableAssignment(Enum):
    ADULT_TABLE = "adult_table"
    KID_TABLE = "kid_table"


@dataclass
class ICPCriterion:
    dimension: ICPDimension
    min_value: float | None = None
    max_value: float | None = None
    allowed_values: list[str] | None = None
    weight: float = 1.0


@dataclass
class ICPDefinition:
    name: str
    criteria: list[ICPCriterion] = field(default_factory=list)
    min_fit_score: float = 0.7

    def score(self, profile: dict) -> float:
        total_weight = 0.0
        weighted_score = 0.0
        for c in self.criteria:
            val = profile.get(c.dimension.value)
            if val is None:
                continue
            score = 0.0
            if c.allowed_values:
                score = 1.0 if str(val) in c.allowed_values else 0.0
            elif c.min_value is not None and c.max_value is not None:
                try:
                    v = float(val)
                    if c.min_value <= v <= c.max_value:
                        score = 1.0
                    else:
                        score = max(0.0, 1.0 - abs(v - c.min_value) / max(c.max_value - c.min_value, 1))
                except (ValueError, TypeError):
                    score = 0.0
            total_weight += c.weight
            weighted_score += score * c.weight
        return weighted_score / total_weight if total_weight > 0 else 0.0


@dataclass
class Prospect:
    prospect_id: str
    name: str
    title: str
    company: str
    email: str | None = None
    linkedin_url: str | None = None
    fit_score: float = 0.0
    fit_level: FitLevel = FitLevel.UNKNOWN
    enrichment: dict[str, Any] = field(default_factory=dict)
    discovered_at: str = ""
    table: TableAssignment = TableAssignment.KID_TABLE


@dataclass
class AccountProspect:
    account_id: str
    account_name: str
    domain: str
    prospects: list[Prospect] = field(default_factory=list)
    icp_score: float = 0.0
    intent_signals: list[str] = field(default_factory=list)


@dataclass
class PriorityQueue:
    items: list[Prospect] = field(default_factory=list)
    queue_type: str = "outreach"
    generated_at: str = ""


@dataclass
class SourceScanResult:
    source: EnrichmentSource
    accounts_discovered: int = 0
    prospects_discovered: int = 0
    errors: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0
