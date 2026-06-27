"""RCC-001 Revenue Orchestrator — main agent loop.

Routes incoming revenue events to the correct workflow DAG,
dispatches agents, monitors execution, and handles failures.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    WorkflowDAG, WorkflowStatus, AgentStatus, AgentHealth,
    WORKFLOW_DAGS, GateReason, PSYCH_STAGES,
)
from .dag_engine import DAGEngine
from .state import ExecutionState


class RevenueOrchestrator(RevenueAgent):
    """Central nervous system — routes events to correct agent chains."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="rcc-001-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self.state = ExecutionState()
        self.dag_engine = DAGEngine(self, self.state)
        self.env = "dev"

    #  Lifecycle hooks

    async def on_start(self):
        # Subscribe to all deal lifecycle events
        for subject_suffix in [
            "revenue.{env}.deal.*.created",
            "revenue.{env}.deal.*.meeting_scheduled.completed",
            "revenue.{env}.deal.*.contract_sent.delivered",
            "revenue.{env}.deal.*.closed_won.achieved",
            "revenue.{env}.deal.*.closed_lost.recorded",
            "revenue.{env}.deal.*.*.entered",
            "revenue.{env}.agent.*.heartbeat",
            "revenue.{env}.agent.*.failure",
            "revenue.{env}.human.approval.*",
        ]:
            subject = subject_suffix.replace("{env}", self.env)
            await self.subscribe(subject)

        print(f"[RCC-001] Subscribed to deal events on revenue.{self.env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"

        self.state.update_agent_health(
            envelope.source_agent,
            AgentStatus.HEALTHY if event_type == "AgentHeartbeat" else AgentStatus.UNKNOWN,
        )

        dag = self._resolve_dag(event_type)
        if not dag:
            return

        print(f"[RCC-001] Event: {event_type} (deal={deal_id}) -> DAG: {dag.dag_id}")
        execution = await self.dag_engine.execute(dag, deal_id, self.env)

        if execution.status == WorkflowStatus.FAILED:
            print(f"[RCC-001] Chain {execution.chain_id} FAILED: {execution.error}")
        elif execution.status == WorkflowStatus.COMPLETED:
            print(f"[RCC-001] Chain {execution.chain_id} completed in "
                  f"{(execution.completed_at - execution.started_at).total_seconds():.1f}s")

    async def tick(self):
        """Periodic health check — log state summary."""
        summary = self.state.get_summary()
        agents_healthy = sum(1 for a in summary["agents"].values() if a["status"] == "healthy")
        circuits_open = sum(1 for a in summary["agents"].values() if a["circuit_open"])
        print(f"[RCC-001:STATUS] chains_active={summary['active_chains']} "
              f"agents_healthy={agents_healthy}/{len(summary['agents'])} "
              f"circuits_open={circuits_open}")
        for aid, info in summary["agents"].items():
            if info["circuit_open"]:
                print(f"  [CIRCUIT OPEN] {aid}")
                await self.publish(
                    f"revenue.{self.env}.system.circuit_breaker.{aid}",
                    "CircuitBreakerTripped",
                    {"agent_id": aid, "auto_tune": True},
                )

    _PSYCH_STAGE_MAPPING = {
        "DealCreated": "awareness",
        "PipelineSnapshotted": "awareness",
        "MeetingCompleted": "consideration",
        "IntentStackActive": "intent",
        "QualificationScored": "evaluation",
        "ContractSent": "decision",
        "DealClosedLost": "loss",
        "DealHealthUpdated": "monitoring",
        "NegotiationProfileReady": "decision",
        "WinLossAnalysisComplete": "loss",
    }

    def _resolve_dag(self, event_type: str) -> WorkflowDAG | None:
        mapping = {
            "DealCreated": "new_lead",
            "MeetingCompleted": "meeting_completed",
            "ContractSent": "contract_sent",
            "DealClosedLost": "closed_lost",
            "PipelineSnapshotted": "new_lead",
            "OutreachPriorityQueue": "new_lead",
            "DealHealthUpdated": "meeting_completed",
            "NegotiationProfileReady": "contract_sent",
            "WinLossAnalysisComplete": "closed_lost",
        }
        dag_id = mapping.get(event_type)
        if dag_id:
            psych_stage = self._PSYCH_STAGE_MAPPING.get(event_type)
            if psych_stage:
                stage_info = PSYCH_STAGES.get(psych_stage, {})
                print(f"[RCC-001] Psych stage: buyer in '{stage_info.get('label', psych_stage)}' "
                      f"phase — needs: {stage_info.get('needs', 'information')}")
            return WORKFLOW_DAGS.get(dag_id)
        return None
