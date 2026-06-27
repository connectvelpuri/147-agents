"""Data models for RCC-001 Revenue Orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    GATED = "awaiting_human"
    DEGRADED = "degraded"


class AgentStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


class GateReason(Enum):
    RISK_THRESHOLD = "risk_threshold"
    PRICE_EXCEPTION = "price_exception"
    EXECUTIVE_OUTREACH = "executive_outreach"
    CONTRACT_TERM = "contract_term"
    SECURITY_EXCEPTION = "security_exception"
    FIRST_OUTREACH = "first_outreach"


@dataclass
class DAGStep:
    agent_id: str
    subject: str
    depends_on: list[str] = field(default_factory=list)
    timeout_seconds: int = 60
    fallback_agent: str | None = None


@dataclass
class WorkflowDAG:
    dag_id: str
    trigger_event_type: str
    steps: list[DAGStep]
    fallback_steps: list[DAGStep] = field(default_factory=list)
    human_gate_at: list[str] = field(default_factory=list)
    timeout_seconds: int = 300


@dataclass
class WorkflowExecution:
    chain_id: str
    dag_id: str
    deal_id: str
    status: WorkflowStatus
    steps_completed: list[str] = field(default_factory=list)
    steps_failed: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    human_gates: list[GateReason] = field(default_factory=list)
    error: str | None = None


@dataclass
class AgentHealth:
    agent_id: str
    status: AgentStatus
    last_heartbeat_at: datetime | None = None
    processed_total: int = 0
    failed_total: int = 0
    failure_streak: int = 0
    circuit_open: bool = False


PSYCH_STAGES: dict[str, dict] = {
    "awareness": {
        "label": "Awareness & Discovery",
        "needs": "Education, social proof, ICP fit confirmation",
        "action": "Route to SDR-001 + AI-001 for research + SDR-003 for outreach",
    },
    "interest": {
        "label": "Interest & Curiosity",
        "needs": "Personalized content, value framing, peer evidence",
        "action": "Route to SDR-003 with BTL→ATL sequencing + SDR-004 for engagement",
    },
    "consideration": {
        "label": "Consideration & Evaluation",
        "needs": "Meeting recaps, objection handling, qualification scoring",
        "action": "Route to MO-002/003/004 + QL-001 + DS-001 for full meeting analysis + deal health dashboard",
    },
    "intent": {
        "label": "Intent & Buying Signals",
        "needs": "Intent confirmation, urgency creation, stakeholder alignment",
        "action": "Route to SDR-002 for intent stack + DS-001 timeline urgency update + SDR-004 for closing prep",
    },
    "evaluation": {
        "label": "Evaluation & Decision",
        "needs": "ROI validation, risk mitigation, competitive comparison",
        "action": "Route to QL-001 rescore + DS-001 health recalculation + SDR-004 with Mirror Attacks",
    },
    "decision": {
        "label": "Decision & Negotiation",
        "needs": "Contract review, BATNA analysis, pricing options, terms alignment",
        "action": "Route to PL-001 + NG-001 (BATNA/ZOPA/power profile) + SDR-004 Give-Get pairs",
    },
    "loss": {
        "label": "Closed Lost — Analysis",
        "needs": "Win/loss root cause, pattern detection, competitive intel capture",
        "action": "Route to DS-003 (Clozd analysis) + KL-001 for learning capture",
    },
    "monitoring": {
        "label": "Active Deal Monitoring",
        "needs": "Continuous health score tracking, risk factor escalation, forecast category updates",
        "action": "DS-001 aggregates all MO, QL, SDR signals into real-time VMF dashboard",
    },
}


WORKFLOW_DAGS: dict[str, WorkflowDAG] = {
    "new_lead": WorkflowDAG(
        dag_id="new_lead",
        trigger_event_type="DealCreated",
        steps=[
            DAGStep(agent_id="sdr-001-v1", subject="revenue.{env}.deal.{deal_id}.prospecting.discover"),
            DAGStep(agent_id="ai-001-v1", subject="revenue.{env}.deal.{deal_id}.intelligence.research"),
            DAGStep(agent_id="sdr-003-v1", subject="revenue.{env}.deal.{deal_id}.outreach.generate", depends_on=["sdr-001-v1", "ai-001-v1"]),
            DAGStep(agent_id="sdr-004-v1", subject="revenue.{env}.deal.{deal_id}.sequence.execute", depends_on=["sdr-003-v1"]),
        ],
        human_gate_at=["sdr-003-v1"],
    ),
    "meeting_completed": WorkflowDAG(
        dag_id="meeting_completed",
        trigger_event_type="MeetingCompleted",
        steps=[
            DAGStep(agent_id="mo-001-v1", subject="revenue.{env}.deal.{deal_id}.meeting.transcribe"),
            DAGStep(agent_id="mo-002-v1", subject="revenue.{env}.deal.{deal_id}.meeting.sentiment", depends_on=["mo-001-v1"]),
            DAGStep(agent_id="mo-003-v1", subject="revenue.{env}.deal.{deal_id}.meeting.objections", depends_on=["mo-001-v1"]),
            DAGStep(agent_id="mo-004-v1", subject="revenue.{env}.deal.{deal_id}.meeting.commitments", depends_on=["mo-001-v1"]),
            DAGStep(agent_id="ql-001-v1", subject="revenue.{env}.deal.{deal_id}.qualifying.rescore", depends_on=["mo-002-v1", "mo-003-v1"]),
            DAGStep(agent_id="ds-001-v1", subject="revenue.{env}.deal.{deal_id}.dashboard.refresh", depends_on=["ql-001-v1"]),
        ],
    ),
    "contract_sent": WorkflowDAG(
        dag_id="contract_sent",
        trigger_event_type="ContractSent",
        steps=[
            DAGStep(agent_id="pl-001-v1", subject="revenue.{env}.deal.{deal_id}.contract.review"),
            DAGStep(agent_id="ng-001-v1", subject="revenue.{env}.deal.{deal_id}.negotiation.prepare"),
            DAGStep(agent_id="cs-001-v1", subject="revenue.{env}.deal.{deal_id}.onboarding.prepare", depends_on=["pl-001-v1"]),
        ],
        human_gate_at=["pl-001-v1"],
    ),
    "closed_lost": WorkflowDAG(
        dag_id="closed_lost",
        trigger_event_type="DealClosedLost",
        steps=[
            DAGStep(agent_id="ds-003-v1", subject="revenue.{env}.deal.{deal_id}.winloss.analyze"),
            DAGStep(agent_id="kl-001-v1", subject="revenue.{env}.deal.{deal_id}.knowledge.capture"),
        ],
    ),
}
