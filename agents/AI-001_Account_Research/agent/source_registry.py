"""Source registry — manages source configurations, API keys, and reliability scoring."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import SourceRecord


class SourceRegistry:
    def __init__(self, db_path: str | Path | None = None):
        self._db_path = Path(db_path) if db_path else Path("data/source_registry.json")
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._sources: dict[str, SourceRecord] = {}
        self._load()

    def _load(self):
        if self._db_path.exists():
            data = json.loads(self._db_path.read_text())
            for s in data:
                record = SourceRecord(**s)
                self._sources[record.source_id] = record

    def _save(self):
        data = [s.__dict__ for s in self._sources.values()]
        self._db_path.write_text(json.dumps(data, indent=2, default=str))

    def register(self, source_id: str, name: str, source_type: str) -> SourceRecord:
        record = SourceRecord(source_id=source_id, name=name, type=source_type)
        self._sources[source_id] = record
        self._save()
        return record

    def get(self, source_id: str) -> SourceRecord | None:
        return self._sources.get(source_id)

    def log_claim(self, source_id: str):
        if source_id in self._sources:
            self._sources[source_id].total_claims += 1
            self._save()

    def log_correction(self, source_id: str):
        if source_id in self._sources:
            self._sources[source_id].corrections += 1
            if self._sources[source_id].is_deprecated:
                self._sources[source_id].enabled = False
            self._save()

    def log_error(self, source_id: str, error: str):
        if source_id in self._sources:
            self._sources[source_id].last_error = error
            self._save()

    def get_reliable_sources(self, min_score: float = 0.7) -> list[SourceRecord]:
        return [
            s for s in self._sources.values()
            if s.enabled and s.reliability_score >= min_score
        ]

    def get_deprecated_sources(self) -> list[SourceRecord]:
        return [s for s in self._sources.values() if s.is_deprecated]

    def configure_default_sources(self):
        defaults = {
            "crunchbase": {"name": "CrunchBase API", "type": "api"},
            "sec_edgar": {"name": "SEC EDGAR", "type": "api"},
            "builtwith": {"name": "BuiltWith", "type": "api"},
            "wappalyzer": {"name": "Wappalyzer", "type": "api"},
            "linkedin_salesnav": {"name": "LinkedIn Sales Navigator", "type": "api"},
            "zoominfo": {"name": "ZoomInfo", "type": "api"},
            "newsapi": {"name": "NewsAPI", "type": "api"},
            "google_news": {"name": "Google News", "type": "rss"},
            "glassdoor": {"name": "Glassdoor", "type": "api"},
            "g2": {"name": "G2", "type": "api"},
            "agent_reach_web": {"name": "Agent-Reach Web", "type": "skill"},
            "agent_reach_linkedin": {"name": "Agent-Reach LinkedIn", "type": "skill"},
            "agent_reach_twitter": {"name": "Agent-Reach Twitter", "type": "skill"},
            "agent_reach_reddit": {"name": "Agent-Reach Reddit", "type": "skill"},
            "last30days": {"name": "last30days", "type": "skill"},
            "company_website": {"name": "Company Website", "type": "web"},
            "annual_report": {"name": "Annual Report", "type": "document"},
            "sec_8k": {"name": "SEC 8-K Filing", "type": "filing"},
            "sec_10k": {"name": "SEC 10-K Filing", "type": "filing"},
            "careers_page": {"name": "Company Careers Page", "type": "web"},
            "indeed": {"name": "Indeed", "type": "web"},
            "crunchbase_news": {"name": "CrunchBase News", "type": "rss"},
            "pitchbook": {"name": "PitchBook", "type": "api"},
        }
        for sid, info in defaults.items():
            if sid not in self._sources:
                self.register(sid, info["name"], info["type"])
