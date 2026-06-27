"""Abstract base class for all RevenueOS agents.

Every agent extends this class which provides:
- NATS connectivity (pub/sub/KV)
- LLM inference client (tier-managed)
- Health check and heartbeat
- Event-driven main loop
- Configuration loading
- Graceful degradation
"""

from __future__ import annotations

import asyncio
import json
import os
import signal
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from .event_envelope import EventEnvelope, new_span_id
from .nats_client import NatsClient
from .llm_client import LLMClient


class RevenueAgent(ABC):
    """Base class that all 108 RevenueOS agents extend."""

    def __init__(
        self,
        agent_id: str,
        agent_version: str = "0.1.0",
        llm_tier: str = "moderate",
        nats_servers: list[str] | None = None,
    ):
        self.agent_id = agent_id
        self.agent_version = agent_version
        self.nats = NatsClient(servers=nats_servers, agent_id=agent_id)
        self.llm = LLMClient(tier=llm_tier)
        self._running = False
        self._health_status = "starting"
        self._processed_count = 0
        self._failed_count = 0
        self._last_failure_at: str | None = None
        self._subscriptions: list[str] = []
        self._kv_buckets: set[str] = set()

    #  Lifecycle

    async def run(self):
        """Start the agent — connect, register, subscribe, then run loop."""
        self._running = True
        self._health_status = "starting"
        print(f"[{self.agent_id}] Starting v{self.agent_version}...")

        await self.nats.connect()
        await self.on_start()
        await self._register()
        await self._subscribe_to_lifecycle()
        await self._publish_heartbeat()

        self._health_status = "healthy"
        print(f"[{self.agent_id}] Running — listening for events")

        while self._running:
            try:
                await self.tick()
                await asyncio.sleep(self.tick_interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._failed_count += 1
                self._last_failure_at = datetime.now(timezone.utc).isoformat()
                print(f"[{self.agent_id}] Tick error: {e}")
                await self._publish_failure(str(e))

        await self.on_shutdown()
        await self.nats.close()
        print(f"[{self.agent_id}] Stopped")

    async def stop(self):
        self._running = False

    @property
    def tick_interval_seconds(self) -> float:
        return 60.0

    #  Subclass hooks

    @abstractmethod
    async def on_start(self):
        """Called once after NATS connects — set up subscriptions, load state."""

    async def on_shutdown(self):
        """Called before shutdown."""

    async def tick(self):
        """Called every tick_interval_seconds while running."""

    async def handle_event(self, envelope: EventEnvelope):
        """Default event handler — logs and counts."""

    #  Subscription helpers

    async def subscribe(self, subject: str, handler: Callable | None = None):
        await self.nats.subscribe(subject, handler or self.handle_event)
        self._subscriptions.append(subject)

    async def publish(self, subject: str, event_type: str, data: dict[str, Any], deal_id: str | None = None):
        envelope = EventEnvelope(
            event_type=event_type,
            source_agent=self.agent_id,
            deal_id=deal_id,
            span_id=new_span_id(),
            data=data,
        )
        await self.nats.publish(subject, envelope)
        self._processed_count += 1
        return envelope

    async def kv_put(self, bucket: str, key: str, value: dict[str, Any]):
        self._kv_buckets.add(bucket)
        await self.nats.kv_put(bucket, key, value)

    async def kv_get(self, bucket: str, key: str) -> dict[str, Any] | None:
        return await self.nats.kv_get(bucket, key)

    #  Lifecycle events

    async def _register(self):
        await self.publish(
            f"revenue.dev.agent.{self.agent_id}.started",
            "AgentStarted",
            {"version": self.agent_version, "llm_tier": self.llm.tier},
        )

    async def _subscribe_to_lifecycle(self):
        await self.nats.subscribe(
            f"revenue.dev.agent.{self.agent_id}.health.check",
            self._handle_health_check,
        )
        await self.nats.subscribe(
            f"revenue.dev.agent.{self.agent_id}.config.updated",
            self._handle_config_update,
        )
        await self.nats.subscribe(
            f"revenue.dev.agent.{self.agent_id}.shutdown",
            self._handle_shutdown,
        )

    async def _publish_heartbeat(self):
        envelope = EventEnvelope(
            event_type="AgentHeartbeat",
            source_agent=self.agent_id,
            data={
                "agent_id": self.agent_id,
                "version": self.agent_version,
                "status": self._health_status,
                "processed_total": self._processed_count,
                "failed_total": self._failed_count,
                "last_failure_at": self._last_failure_at,
            },
        )
        await self.nats.publish(f"revenue.dev.agent.{self.agent_id}.heartbeat", envelope)

    async def _publish_failure(self, error: str):
        envelope = EventEnvelope(
            event_type="AgentFailure",
            source_agent=self.agent_id,
            data={"error": error, "failed_total": self._failed_count},
        )
        await self.nats.publish(f"revenue.dev.agent.{self.agent_id}.failure", envelope)

    async def _handle_health_check(self, envelope: EventEnvelope):
        await self._publish_heartbeat()

    async def _handle_config_update(self, envelope: EventEnvelope):
        print(f"[{self.agent_id}] Config update received")

    async def _handle_shutdown(self, envelope: EventEnvelope):
        print(f"[{self.agent_id}] Shutdown requested")
        await self.stop()
