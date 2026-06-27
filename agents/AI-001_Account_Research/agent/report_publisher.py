"""Report publisher — packages intelligence and publishes to NATS JetStream."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from .models import (
    AccountIntelligenceReport, ResearchCycleReport, Confidence,
)


class ReportPublisher:
    def __init__(self, nats_servers: list[str] | None = None):
        self._nats_servers = nats_servers or ["nats://localhost:4222"]
        self._nc = None

    def _ensure_connected(self):
        if self._nc is None:
            try:
                import nats
                self._nc = nats.connect(servers=self._nats_servers)
            except ImportError:
                print("[!] NATS not available — publishing to log only")
            except Exception as e:
                print(f"[!] NATS connection failed: {e}")

    def publish_intelligence_profile(self, report: AccountIntelligenceReport):
        subject = f"ai.account.intelligence.profile.{report.account_id}"
        payload = report.to_dict()
        self._publish(subject, payload)
        print(f"[PUBLISH] {subject} — {report.account_name} ({report.research_depth.value})")

    def publish_org_chart(self, report: AccountIntelligenceReport):
        subject = f"ai.account.org_chart.{report.account_id}"
        org = report.organizational_chart
        payload = {
            "account_id": report.account_id,
            "c_suite_count": len(org.c_suite),
            "decision_makers_count": len(org.decision_makers),
            "data_quality": org.data_quality.value,
        }
        self._publish(subject, payload)

    def publish_signal(self, report: AccountIntelligenceReport, signal: dict):
        subject = f"ai.account.signal.{report.account_id}"
        self._publish(subject, signal)

    def publish_financial(self, report: AccountIntelligenceReport):
        subject = f"ai.account.financial.{report.account_id}"
        fin = report.financial_health
        payload = {
            "account_id": report.account_id,
            "trend": fin.revenue_growth_trend.value,
            "profitability": fin.profitability_status,
            "risk_flags": fin.risk_flags,
            "confidence": fin.confidence.value,
        }
        self._publish(subject, payload)

    def publish_techstack(self, report: AccountIntelligenceReport):
        subject = f"ai.account.techstack.{report.account_id}"
        tech = report.technology_stack
        payload = {
            "account_id": report.account_id,
            "detection_method": tech.detection_method,
            "confidence": tech.detection_confidence.value,
        }
        self._publish(subject, payload)

    def publish_competitive(self, report: AccountIntelligenceReport):
        subject = f"ai.account.competitive.{report.account_id}"
        payload = {
            "account_id": report.account_id,
            "competitors": [
                {
                    "name": c.competitor_name,
                    "relationship": c.relationship_type,
                    "confidence": c.confidence.value,
                }
                for c in report.competitors_present
            ],
        }
        self._publish(subject, payload)

    def publish_cycle_complete(self, cycle: ResearchCycleReport):
        subject = f"ai.account.research.completed"
        payload = {
            "account_id": cycle.account_id,
            "depth": cycle.depth.value,
            "duration_seconds": cycle.total_duration_seconds,
            "jobs_completed": sum(1 for j in cycle.jobs if j.status == "completed"),
            "jobs_failed": sum(1 for j in cycle.jobs if j.status == "failed"),
            "reports_published": cycle.reports_published,
            "errors": cycle.errors[:5],
        }
        self._publish(subject, payload)

    def _publish(self, subject: str, payload: dict):
        data = json.dumps(payload, default=str).encode()
        if self._nc:
            try:
                self._nc.publish(subject, data)
            except Exception as e:
                print(f"[!] NATS publish failed for {subject}: {e}")
        else:
            print(f"[LOG] Would publish to {subject}: {len(data)} bytes")

    def close(self):
        if self._nc:
            self._nc.close()
