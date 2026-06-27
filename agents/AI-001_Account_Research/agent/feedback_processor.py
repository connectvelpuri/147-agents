"""Feedback processor — handles human corrections, updates source scoring, triggers retraining."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .models import CorrectionEvent
from .source_registry import SourceRegistry


FEEDBACK_THRESHOLD_P1 = 0.15
FEEDBACK_THRESHOLD_IMMEDIATE = 0.20
CORRECTION_LOG_PATH = Path("data/corrections.jsonl")


class FeedbackProcessor:
    def __init__(self, source_registry: SourceRegistry):
        self.sources = source_registry
        self._corrections: list[CorrectionEvent] = []
        self._load()

    def _load(self):
        if CORRECTION_LOG_PATH.exists():
            for line in CORRECTION_LOG_PATH.read_text().strip().split("\n"):
                if line:
                    data = json.loads(line)
                    self._corrections.append(CorrectionEvent(**data))

    def _save(self, event: CorrectionEvent):
        CORRECTION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CORRECTION_LOG_PATH, "a") as f:
            f.write(json.dumps(event.__dict__, default=str) + "\n")

    def process_correction(self, event: CorrectionEvent) -> dict:
        self._corrections.append(event)
        self._save(event)

        domain_corrections = [
            c for c in self._corrections
            if c.domain == event.domain
        ]
        total_corrections = len(self._corrections)

        domain_rate = len([c for c in domain_corrections if c.domain == event.domain]) / max(len(domain_corrections), 1)
        overall_rate = total_corrections / max(len(self._corrections), 1)

        result = {
            "correction_logged": True,
            "domain_correction_rate": domain_rate,
            "overall_correction_rate": overall_rate,
            "actions": [],
        }

        if domain_rate >= FEEDBACK_THRESHOLD_IMMEDIATE:
            result["actions"].append(f"ESCALATE: {event.domain} correction rate {domain_rate:.0%} exceeds P0 threshold — trigger AIG-002 immediate optimization")
        elif domain_rate >= FEEDBACK_THRESHOLD_P1:
            result["actions"].append(f"FLAG: {event.domain} correction rate {domain_rate:.0%} exceeds P1 threshold — queue for KL-005 weekly retrain")
            result["actions"].append("PUBLISH: ai.account.research.prompt_drift event")

        if overall_rate >= FEEDBACK_THRESHOLD_IMMEDIATE:
            result["actions"].append("ESCALATE: Overall correction rate exceeds 20% — immediate AIG-002 escalation")

        return result

    def get_correction_rate_by_domain(self) -> dict[str, float]:
        by_domain: dict[str, list] = {}
        for c in self._corrections:
            by_domain.setdefault(c.domain, []).append(c)
        return {
            domain: len(corrections) / max(len(self._corrections), 1)
            for domain, corrections in by_domain.items()
        }

    def get_weekly_correction_trend(self) -> list[dict]:
        trend = []
        now = datetime.now()
        for i in range(4):
            week_start = now - timedelta(days=7 * i + 7)
            week_end = now - timedelta(days=7 * i)
            week_corrections = [
                c for c in self._corrections
                if week_start <= c.corrected_at < week_end
            ]
            trend.append({
                "week": f"Week {i+1}",
                "corrections": len(week_corrections),
                "domains": list(set(c.domain for c in week_corrections)),
            })
        return trend

    def should_trigger_retrain(self) -> bool:
        if not self._corrections:
            return False
        recent = [
            c for c in self._corrections
            if c.corrected_at > datetime.now() - timedelta(days=7)
        ]
        if not recent:
            return False
        rate = len(recent) / max(len(self._corrections), 1)
        return rate >= FEEDBACK_THRESHOLD_P1
