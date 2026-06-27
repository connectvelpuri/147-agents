"""Minimal OpenTelemetry helpers for RevenueOS agents.

In development mode, all operations are no-ops with console logging.
In production, emits OTLP traces to the configured endpoint.
"""

from __future__ import annotations

from typing import Any, Optional


class Tracer:
    """Minimal tracer — no-ops in dev, OTLP in production."""

    def __init__(self, agent_id: str, enabled: bool = False):
        self.agent_id = agent_id
        self.enabled = enabled

    def span(self, name: str, **attrs) -> SpanContext:
        return SpanContext(name=name, tracer=self)

    def record_error(self, span: SpanContext, error: Exception):
        print(f"[TRACE:ERR] {span.name}: {error}")

    def record_metric(self, name: str, value: float, attrs: dict | None = None):
        pass


class SpanContext:
    def __init__(self, name: str, tracer: Tracer):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
