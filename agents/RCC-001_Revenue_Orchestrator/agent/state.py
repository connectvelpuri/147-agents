"""Execution state tracking for RCC-001 — active chains, agent health, human gates."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from .models import WorkflowExecution, AgentHealth, AgentStatus


class ExecutionState:
    """In-memory state for active workflow executions.

    In production, backed by NATS KV store for crash recovery.
    """

    def __init__(self):
        self._active_chains: dict[str, WorkflowExecution] = {}
        self._agent_health: dict[str, AgentHealth] = {}
        self._chain_history: list[WorkflowExecution] = []

    def add_chain(self, execution: WorkflowExecution):
        self._active_chains[execution.chain_id] = execution

    def get_chain(self, chain_id: str) -> WorkflowExecution | None:
        return self._active_chains.get(chain_id)

    def complete_chain(self, chain_id: str):
        ex = self._active_chains.pop(chain_id, None)
        if ex:
            self._chain_history.append(ex)

    def update_agent_health(self, agent_id: str, status: AgentStatus, processed: int = 0, failed: int = 0):
        h = self._agent_health.get(agent_id)
        if not h:
            h = AgentHealth(agent_id=agent_id, status=status)
            self._agent_health[agent_id] = h
        h.status = status
        h.last_heartbeat_at = datetime.now(timezone.utc)
        h.processed_total = processed
        h.failed_total = failed
        if status == AgentStatus.FAILED:
            h.failure_streak += 1
        else:
            h.failure_streak = max(0, h.failure_streak - 1)
        h.circuit_open = h.failure_streak >= 5

    def get_active_chains(self) -> list[WorkflowExecution]:
        return list(self._active_chains.values())

    def get_summary(self) -> dict:
        return {
            "active_chains": len(self._active_chains),
            "chain_history": len(self._chain_history),
            "agents": {
                aid: {"status": h.status.value, "circuit_open": h.circuit_open}
                for aid, h in self._agent_health.items()
            },
        }
