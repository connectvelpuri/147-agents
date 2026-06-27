"""NATS JetStream client wrapper for RevenueOS agents.

Provides publish, subscribe, KV, and ObjectStore with
graceful degradation when NATS is unavailable.
"""

from __future__ import annotations

import json
import asyncio
from typing import Any, Callable, Optional
from datetime import timedelta

from .event_envelope import EventEnvelope


class NatsClient:
    """NATS client with graceful degradation.

    In dev/testing mode (nats_servers empty or None), all operations
    are no-ops with local logging. This lets agents run without a NATS cluster.
    """

    def __init__(self, servers: list[str] | None = None, agent_id: str = "unknown"):
        self.servers = servers or []
        self.agent_id = agent_id
        self._nc = None
        self._js = None
        self._connected = False
        self._handlers: dict[str, list[Callable]] = {}
        self._dev_mode = len(self.servers) == 0

    async def connect(self):
        if self._dev_mode:
            print(f"[NATS] Dev mode — no connection (agent={self.agent_id})")
            self._connected = True
            return
        try:
            import nats
            self._nc = await nats.connect(
                servers=self.servers,
                name=self.agent_id,
                ping_interval=20,
                max_outstanding_pings=5,
            )
            self._js = self._nc.jetstream()
            self._connected = True
            print(f"[NATS] Connected to {self.servers} (agent={self.agent_id})")
        except Exception as e:
            print(f"[NATS] Connection failed — falling back to dev mode: {e}")
            self._dev_mode = True
            self._connected = True

    async def publish(self, subject: str, envelope: EventEnvelope):
        if self._dev_mode:
            print(f"[NATS:PUB] {subject} | {envelope.event_type} | {json.dumps(envelope.data, default=str)[:200]}")
            return
        if not self._connected:
            return
        try:
            await self._nc.publish(
                subject,
                envelope.to_json().encode(),
                headers=envelope.nats_headers,
            )
        except Exception as e:
            print(f"[NATS:PUB:ERR] {subject}: {e}")

    async def subscribe(self, subject: str, handler: Callable, queue: str | None = None):
        self._handlers.setdefault(subject, []).append(handler)
        if self._dev_mode:
            return
        if not self._connected:
            return
        try:
            qgroup = queue or self.agent_id
            await self._nc.subscribe(
                subject,
                queue=qgroup,
                cb=self._make_callback(handler),
            )
        except Exception as e:
            print(f"[NATS:SUB:ERR] {subject}: {e}")

    def _make_callback(self, handler: Callable):
        async def _cb(msg):
            try:
                envelope = EventEnvelope.from_json(msg.data.decode())
                await handler(envelope)
            except Exception as e:
                print(f"[NATS:CB:ERR] {msg.subject}: {e}")
        return _cb

    async def kv_put(self, bucket: str, key: str, value: dict[str, Any]):
        if self._dev_mode:
            print(f"[NATS:KV] {bucket}/{key} = {json.dumps(value, default=str)[:200]}")
            return
        if not self._connected or not self._js:
            return
        try:
            kv = await self._js.create_key_value(bucket=bucket)
            await kv.put(key, json.dumps(value, default=str).encode())
        except Exception as e:
            print(f"[NATS:KV:ERR] {bucket}/{key}: {e}")

    async def kv_get(self, bucket: str, key: str) -> dict[str, Any] | None:
        if self._dev_mode:
            return None
        if not self._connected or not self._js:
            return None
        try:
            kv = await self._js.create_key_value(bucket=bucket)
            entry = await kv.get(key)
            return json.loads(entry.value.decode()) if entry else None
        except Exception:
            return None

    async def close(self):
        if self._nc:
            await self._nc.drain()
