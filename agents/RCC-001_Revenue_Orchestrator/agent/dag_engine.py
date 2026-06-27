"""DAG execution engine — resolves dependencies and dispatches agents in order."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_event_id, new_span_id

from .models import (
    WorkflowDAG, WorkflowExecution, WorkflowStatus, DAGStep, AgentHealth, AgentStatus, GateReason,
)
from .state import ExecutionState


class DAGEngine:
    """Executes workflow DAGs with dependency resolution, timeouts, and fallback."""

    def __init__(self, agent: RevenueAgent, state: ExecutionState):
        self.agent = agent
        self.state = state

    async def execute(self, dag: WorkflowDAG, deal_id: str, env: str = "dev") -> WorkflowExecution:
        chain_id = f"ch_{new_event_id()[4:]}"
        execution = WorkflowExecution(chain_id=chain_id, dag_id=dag.dag_id, deal_id=deal_id, status=WorkflowStatus.PENDING, started_at=datetime.now(timezone.utc))

        await self._publish_chain_started(execution, dag, env)
        execution.status = WorkflowStatus.RUNNING

        try:
            completed = set()
            for step in dag.steps:
                if step.agent_id in dag.human_gate_at:
                    execution.status = WorkflowStatus.GATED
                    execution.human_gates.append(GateReason.RISK_THRESHOLD)
                    await self._request_human_gate(execution, step, env)
                    await self._wait_for_gate(chain_id, step, execution)
                    execution.status = WorkflowStatus.RUNNING

                deps = [d for d in step.depends_on if d not in completed]
                if deps:
                    continue

                success = await self._dispatch_step(step, deal_id, env)
                if success:
                    completed.add(step.agent_id)
                    execution.steps_completed.append(step.agent_id)
                else:
                    execution.steps_failed.append(step.agent_id)
                    if step.fallback_agent:
                        fallback_step = DAGStep(agent_id=step.fallback_agent, subject=step.subject)
                        await self._dispatch_step(fallback_step, deal_id, env)
                        completed.add(step.fallback_agent)
                        execution.steps_completed.append(step.fallback_agent)
                    else:
                        raise RuntimeError(f"Step {step.agent_id} failed with no fallback")

            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now(timezone.utc)

        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now(timezone.utc)

        await self._publish_chain_result(execution, env)
        return execution

    async def _dispatch_step(self, step: DAGStep, deal_id: str, env: str) -> bool:
        subject = step.subject.replace("{env}", env).replace("{deal_id}", deal_id)
        try:
            self.agent._processed_count += 1
            envelope = EventEnvelope(
                event_type="AgentTaskDispatched",
                source_agent=self.agent.agent_id,
                deal_id=deal_id,
                span_id=new_span_id(),
                data={"dag_step_agent": step.agent_id, "timeout_seconds": step.timeout_seconds},
            )
            await asyncio.wait_for(
                self.agent.nats.publish(subject, envelope),
                timeout=step.timeout_seconds,
            )
            return True
        except asyncio.TimeoutError:
            print(f"[DAG:TIMEOUT] {step.agent_id} — exceeded {step.timeout_seconds}s")
            return False
        except Exception as e:
            print(f"[DAG:FAIL] {step.agent_id} — {e}")
            return False

    async def _request_human_gate(self, execution: WorkflowExecution, step: DAGStep, env: str):
        subject = f"revenue.{env}.human.approval.{execution.deal_id}"
        envelope = EventEnvelope(
            event_type="HumanGateRequired",
            source_agent=self.agent.agent_id,
            deal_id=execution.deal_id,
            span_id=new_span_id(),
            data={
                "chain_id": execution.chain_id,
                "dag_id": execution.dag_id,
                "step": step.agent_id,
            },
        )
        await self.agent.nats.publish(subject, envelope)

    async def _wait_for_gate(self, chain_id: str, step: DAGStep, execution: WorkflowExecution):
        """For dev mode — automatically approve after a short delay."""
        await asyncio.sleep(1)

    async def _publish_chain_started(self, execution: WorkflowExecution, dag: WorkflowDAG, env: str):
        subject = f"revenue.{env}.system.chain.{execution.chain_id}.started"
        envelope = EventEnvelope(
            event_type="AgentChainStarted",
            source_agent=self.agent.agent_id,
            deal_id=execution.deal_id,
            span_id=new_span_id(),
            data={
                "chain_id": execution.chain_id,
                "deal_id": execution.deal_id,
                "dag_id": dag.dag_id,
                "steps": [s.agent_id for s in dag.steps],
            },
        )
        await self.agent.nats.publish(subject, envelope)

    async def _publish_chain_result(self, execution: WorkflowExecution, env: str):
        status = "completed" if execution.status == WorkflowStatus.COMPLETED else "failed"
        subject = f"revenue.{env}.system.chain.{execution.chain_id}.{status}"
        envelope = EventEnvelope(
            event_type="AgentChainCompleted" if execution.status == WorkflowStatus.COMPLETED else "AgentChainFailed",
            source_agent=self.agent.agent_id,
            deal_id=execution.deal_id,
            span_id=new_span_id(),
            data={
                "chain_id": execution.chain_id,
                "deal_id": execution.deal_id,
                "duration_seconds": ((datetime.now(timezone.utc) - execution.started_at).total_seconds()),
                "steps_completed": execution.steps_completed,
                "steps_failed": execution.steps_failed,
                "error": execution.error,
                "status": execution.status.value,
            },
        )
        await self.agent.nats.publish(subject, envelope)
