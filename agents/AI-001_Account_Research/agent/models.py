"""Data models for Account Research Agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional


class ResearchDepth(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNVERIFIED = "unverified"


class OwnershipType(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    PE_BACKED = "pe_backed"
    SUBSIDIARY = "subsidiary"
    NONPROFIT = "nonprofit"
    GOVERNMENT = "government"


class FinancialTrend(str, Enum):
    GROWING = "growing"
    STABLE = "stable"
    DECLINING = "declining"
    UNKNOWN = "unknown"


class SignalType(str, Enum):
    ROLE_CHANGE = "role_change"
    FUNDING = "funding"
    CONTRACT_EXPIRY = "contract_expiry"
    TECH_EVALUATION = "tech_evaluation"
    COMPETITOR_LOSS = "competitor_loss"
    REGULATORY_CHANGE = "regulatory_change"
    MANDATE_CHANGE = "mandate_change"
    PARTNER_SHIFT = "partner_shift"


class TriggerType(str, Enum):
    EXEC_CHANGE = "exec_change"
    ACQUISITION = "acquisition"
    FUNDING = "funding"
    RESTRUCTURING = "restructuring"
    PRODUCT_LAUNCH = "product_launch"
    EARNINGS = "earnings"
    LAYOFF = "layoff"
    PARTNERSHIP = "partnership"
    LEGAL = "legal"
    EXPANSION = "expansion"


class RiskType(str, Enum):
    REGULATORY = "regulatory"
    FINANCIAL = "financial"
    CULTURE_FIT = "culture_fit"
    COMPETITION = "competition"
    TIMING = "timing"
    TECHNICAL = "technical"
    RELATIONSHIP = "relationship"


class ResearchDomain(str, Enum):
    FIRMOGRAPHIC = "firmographic"
    FINANCIAL = "financial"
    TECHNOGRAPHIC = "technographic"
    ORGANIZATIONAL = "organizational"
    NEWS = "news"
    SOCIAL = "social"
    JOBS = "jobs"
    COMPETITIVE = "competitive"
    REGULATORY = "regulatory"
    CULTURAL = "cultural"
    PARTNER = "partner"
    INTENT = "intent"


@dataclass
class VerifiedClaim:
    domain: str
    key: str
    value: any
    sources: list[str]
    source_count: int
    confidence: Confidence
    last_verified: datetime | None = None
    correction_history: list[dict] = field(default_factory=list)


@dataclass
class SourceRecord:
    source_id: str
    name: str
    type: str
    total_claims: int = 0
    corrections: int = 0
    last_error: str | None = None
    enabled: bool = True

    @property
    def reliability_score(self) -> float:
        if self.total_claims == 0:
            return 0.5
        return max(0.0, 1.0 - (self.corrections / self.total_claims))

    @property
    def is_deprecated(self) -> bool:
        return self.reliability_score < 0.6


@dataclass
class ResearchPlan:
    account_name: str
    account_id: str
    depth: ResearchDepth
    domains_to_collect: list[ResearchDomain]
    priority_targets: list[str]
    consumer_requirements: dict[str, list[str]]
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None


@dataclass
class AccountRequest:
    account_name: str
    account_id: str
    depth: ResearchDepth = ResearchDepth.STANDARD
    requestor: str = ""
    context: dict[str, any] = field(default_factory=dict)


@dataclass
class FirmographicData:
    revenue: VerifiedClaim | None = None
    employees: VerifiedClaim | None = None
    headquarters: VerifiedClaim | None = None
    industry: list[VerifiedClaim] = field(default_factory=list)
    ownership: VerifiedClaim | None = None
    founded: VerifiedClaim | None = None
    stock_ticker: VerifiedClaim | None = None
    description: VerifiedClaim | None = None
    website: VerifiedClaim | None = None


@dataclass
class FinancialData:
    revenue_growth_trend: FinancialTrend = FinancialTrend.UNKNOWN
    funding_rounds: list[dict] = field(default_factory=list)
    profitability_status: str = "unknown"
    debt_summary: str = ""
    last_filing_date: date | None = None
    risk_flags: list[str] = field(default_factory=list)
    confidence: Confidence = Confidence.LOW


@dataclass
class TechnologyStack:
    erp: list[str] = field(default_factory=list)
    crm: list[str] = field(default_factory=list)
    wms_tms: list[str] = field(default_factory=list)
    analytics: list[str] = field(default_factory=list)
    cloud_providers: list[str] = field(default_factory=list)
    integration_tech: list[str] = field(default_factory=list)
    security_compliance: list[str] = field(default_factory=list)
    detection_method: str = ""
    detection_confidence: Confidence = Confidence.LOW
    raw_findings: list[VerifiedClaim] = field(default_factory=list)


@dataclass
class OrganizationalNode:
    name: str
    title: str
    department: str = ""
    tenure_years: float = 0.0
    linkedin_url: str = ""
    reporting_to: str = ""
    confidence: Confidence = Confidence.LOW
    email: str = ""
    phone: str = ""
    previous_roles: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)


@dataclass
class OrganizationalChart:
    c_suite: list[OrganizationalNode] = field(default_factory=list)
    decision_makers: list[OrganizationalNode] = field(default_factory=list)
    influencers: list[OrganizationalNode] = field(default_factory=list)
    buying_committee_candidates: list[OrganizationalNode] = field(default_factory=list)
    data_quality: Confidence = Confidence.LOW


@dataclass
class StrategicInitiative:
    initiative: str
    evidence: list[str] = field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    relevant_vendors: list[str] = field(default_factory=list)
    implication_for_us: str = ""


@dataclass
class BuyingSignal:
    signal_type: SignalType
    confidence: Confidence
    description: str = ""
    detected_at: datetime = field(default_factory=datetime.now)
    recommended_action: str = ""


@dataclass
class TriggerEvent:
    event_type: TriggerType
    title: str
    url: str = ""
    summary: str = ""
    severity: int = 5
    detected_at: datetime = field(default_factory=datetime.now)
    relevant_personas: list[str] = field(default_factory=list)
    acted_on: bool = False


@dataclass
class CompetitorPresence:
    competitor_name: str
    relationship_type: str = ""
    contract_value_estimated: str = ""
    contract_expiration: date | None = None
    confidence: Confidence = Confidence.LOW


@dataclass
class RiskFactor:
    risk_type: RiskType
    severity: int = 5
    description: str = ""
    mitigation: str = ""


@dataclass
class EngagementRecommendation:
    recommended_persona: str = ""
    recommended_value_proposition: str = ""
    recommended_approach: str = ""
    optimal_timing: str = "monitor"
    win_probability: float = 0.0
    estimated_deal_size_range: dict = field(default_factory=lambda: {"min": 0, "max": 0, "currency": "USD"})


@dataclass
class DataGap:
    domain: str
    gaps: list[str] = field(default_factory=list)
    impact: str = ""


@dataclass
class ConsumerSection:
    agent_id: str
    content: dict[str, any] = field(default_factory=dict)


@dataclass
class AccountIntelligenceReport:
    account_id: str
    account_name: str
    research_depth: ResearchDepth
    report_version: str = "1.0.0"
    generated_at: datetime = field(default_factory=datetime.now)
    research_plan: dict = field(default_factory=dict)
    firmographic: FirmographicData = field(default_factory=FirmographicData)
    financial_health: FinancialData = field(default_factory=FinancialData)
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    organizational_chart: OrganizationalChart = field(default_factory=OrganizationalChart)
    strategic_initiatives: list[StrategicInitiative] = field(default_factory=list)
    buying_signals: list[BuyingSignal] = field(default_factory=list)
    trigger_events: list[TriggerEvent] = field(default_factory=list)
    competitors_present: list[CompetitorPresence] = field(default_factory=list)
    risk_factors: list[RiskFactor] = field(default_factory=list)
    engagement_recommendation: EngagementRecommendation = field(default_factory=EngagementRecommendation)
    consumer_sections: list[ConsumerSection] = field(default_factory=list)
    data_gaps: list[DataGap] = field(default_factory=list)
    overall_confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "account_name": self.account_name,
            "research_depth": self.research_depth.value,
            "report_version": self.report_version,
            "generated_at": self.generated_at.isoformat(),
            "consumer_agents": [s.agent_id for s in self.consumer_sections],
            "overall_confidence": self.overall_confidence,
        }


@dataclass
class CollectionJob:
    domain: ResearchDomain
    account_name: str
    sources: list[str] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    results: list[VerifiedClaim] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    status: str = "pending"

    @property
    def duration_seconds(self) -> float:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0


@dataclass
class ResearchCycleReport:
    account_id: str
    depth: ResearchDepth
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    jobs: list[CollectionJob] = field(default_factory=list)
    verification_errors: int = 0
    reports_published: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def total_duration_seconds(self) -> float:
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0


@dataclass
class CorrectionEvent:
    intelligence_item_id: str
    account_id: str
    domain: str
    original_value: any
    corrected_value: any
    corrected_by: str
    corrected_at: datetime = field(default_factory=datetime.now)
    reason: str = ""
