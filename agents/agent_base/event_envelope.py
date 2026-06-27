"""Standard event envelope for all inter-agent communication.

Every message on the NATS bus uses this schema.
See REVENUE_OS_ORCHESTRATION.md §2 for full specification.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any


def new_event_id() -> str:
    return f"evt_{uuid.uuid4().hex[:12]}"


def new_trace_id() -> str:
    return f"tr_{uuid.uuid4().hex[:16]}"


def new_span_id() -> str:
    return f"sp_{uuid.uuid4().hex[:8]}"


class EventEnvelope:
    """Standard NATS message envelope for all agent communication."""

    def __init__(
        self,
        event_type: str,
        source_agent: str,
        event_id: str | None = None,
        deal_id: str | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
        data: dict[str, Any] | None = None,
    ):
        self.spec_version = "2.0"
        self.event_id = event_id or new_event_id()
        self.event_type = event_type
        self.source_agent = source_agent
        self.trace_id = trace_id or new_trace_id()
        self.span_id = span_id or new_span_id()
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.deal_id = deal_id
        self.correlation_id = correlation_id
        self.causation_id = causation_id
        self.data = data or {}

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "spec_version": self.spec_version,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source_agent": self.source_agent,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "timestamp": self.timestamp,
            "data": self.data,
        }
        if self.deal_id:
            d["deal_id"] = self.deal_id
        if self.correlation_id:
            d["correlation_id"] = self.correlation_id
        if self.causation_id:
            d["causation_id"] = self.causation_id
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @staticmethod
    def from_json(raw: str) -> EventEnvelope:
        d = json.loads(raw)
        return EventEnvelope(
            event_type=d["event_type"],
            source_agent=d["source_agent"],
            event_id=d.get("event_id"),
            deal_id=d.get("deal_id"),
            correlation_id=d.get("correlation_id"),
            causation_id=d.get("causation_id"),
            trace_id=d.get("trace_id"),
            span_id=d.get("span_id"),
            data=d.get("data", {}),
        )

    #  NATS header helpers

    @property
    def nats_headers(self) -> dict[str, str]:
        return {
            "Nats-Msg-Id": self.event_id,
            "X-Event-Type": self.event_type,
            "X-Source-Agent": self.source_agent,
            "Traceparent": self.trace_id,
        }
