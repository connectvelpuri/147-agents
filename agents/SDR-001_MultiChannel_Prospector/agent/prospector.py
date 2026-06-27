"""SDR-001 Multi-Channel Prospector — discovers, enriches, and prioritizes prospects.

Runs on a 6-hour tick to scan intent and firmographic sources for
ICP-matching accounts and contacts.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_span_id, new_event_id

from .models import (
    ICPDefinition, ICPCriterion, ICPDimension,
    Prospect, AccountProspect, PriorityQueue, FitLevel, TableAssignment,
    SourceScanResult, EnrichmentSource,
)


class MultiChannelProspector(RevenueAgent):
    """Continuously discovers ICP-matching prospects from external sources."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="sdr-001-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._icp = self._default_icp()
        self._discovered_accounts: dict[str, AccountProspect] = {}
        self._env = "dev"

    @property
    def tick_interval_seconds(self) -> float:
        return 360.0  # 6 min in dev (6 hours in prod)

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.system.pipeline.snapshot.triggered")
        await self.subscribe(f"revenue.{self._env}.agent.rcc-001-v1.config.updated")
        print(f"[SDR-001] Watching for prospecting triggers on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        if envelope.event_type == "PipelineSnapshotted":
            await self._run_discovery_cycle()

    async def tick(self):
        await self._run_discovery_cycle()

    async def _run_discovery_cycle(self):
        print(f"[SDR-001] Discovery cycle starting...")
        all_prospects: list[Prospect] = []

        for source in EnrichmentSource:
            result = await self._scan_source(source)
            if result.accounts_discovered or result.prospects_discovered:
                print(f"  Source {source.value}: {result.accounts_discovered} accounts, "
                      f"{result.prospects_discovered} prospects ({result.duration_seconds:.1f}s)")

        for aid, account in self._discovered_accounts.items():
            account.icp_score = self._icp.score({
                d.value: account.prospects[0].enrichment.get(d.value, 0) if account.prospects else 0
                for d in ICPDimension
            })
            if account.icp_score >= self._icp.min_fit_score:
                for prospect in account.prospects:
                    prospect.fit_score = account.icp_score
                    prospect.fit_level = self._level_from_score(account.icp_score)
                    prospect.table = self._assign_table(prospect)
                    all_prospects.append(prospect)

        # Reverse Funnel Math: calculate prospect requirements from revenue target
        funnel_breakdown = self._reverse_funnel_math(
            pipeline_target=5_000_000,  # $5M quarterly pipeline target
            avg_deal_size=100_000,
            meeting_to_qualified=0.4,
            contact_to_meeting=0.15,
            outreach_to_contact=0.25,
        )

        all_prospects.sort(key=lambda p: p.fit_score, reverse=True)
        adult_table = [p for p in all_prospects if p.table == TableAssignment.ADULT_TABLE]
        kid_table = [p for p in all_prospects if p.table == TableAssignment.KID_TABLE]
        queue = PriorityQueue(
            items=(adult_table + kid_table)[:50],
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

        await self.publish(
            f"revenue.{self._env}.prospecting.priority_queue",
            "OutreachPriorityQueue",
            {
                "queue_type": "outreach",
                "prospect_count": len(queue.items),
                "adult_table_count": sum(1 for p in queue.items if p.table == TableAssignment.ADULT_TABLE),
                "kid_table_count": sum(1 for p in queue.items if p.table == TableAssignment.KID_TABLE),
                "reverse_funnel": funnel_breakdown,
                "top_prospects": [
                    {"prospect_id": p.prospect_id, "name": p.name, "company": p.company,
                     "title": p.title, "fit_score": p.fit_score, "fit_level": p.fit_level.value,
                     "table": p.table.value}
                    for p in queue.items[:10]
                ],
            },
        )
        print(f"[SDR-001] Discovery cycle complete: {len(all_prospects)} prospects, "
              f"top score: {all_prospects[0].fit_score:.2f}" if all_prospects else
              f"[SDR-001] Discovery cycle complete: 0 prospects")

    async def _scan_source(self, source: EnrichmentSource) -> SourceScanResult:
        result = SourceScanResult(source=source)
        if source == EnrichmentSource.CRUNCHBASE:
            accounts = [
                {"name": "Acme Corp", "domain": "acme.com", "industry": "tech",
                 "revenue": 50000000, "employees": 200, "funding": "series-b"},
                {"name": "Globex Inc", "domain": "globex.io", "industry": "fintech",
                 "revenue": 100000000, "employees": 500, "funding": "series-c"},
                {"name": "Initech", "domain": "initech.com", "industry": "enterprise-saas",
                 "revenue": 75000000, "employees": 350, "funding": "series-a"},
            ]
            for acc in accounts:
                aid = acc["name"].lower().replace(" ", "_")
                if aid not in self._discovered_accounts:
                    self._discovered_accounts[aid] = AccountProspect(
                        account_id=aid, account_name=acc["name"], domain=acc["domain"])
                self._discovered_accounts[aid].prospects.append(Prospect(
                    prospect_id=f"p_{aid}_ceo",
                    name=f"CEO of {acc['name']}",
                    title="CEO",
                    company=acc["name"],
                    enrichment={
                        ICPDimension.INDUSTRY.value: acc["industry"],
                        ICPDimension.REVENUE.value: acc["revenue"],
                        ICPDimension.EMPLOYEE_COUNT.value: acc["employees"],
                        ICPDimension.FUNDING.value: acc["funding"],
                    },
                    discovered_at=datetime.now(timezone.utc).isoformat(),
                ))
                result.accounts_discovered += 1
                result.prospects_discovered += 1
        return result

    def _default_icp(self) -> ICPDefinition:
        return ICPDefinition(
            name="Enterprise SaaS ICP",
            criteria=[
                ICPCriterion(dimension=ICPDimension.INDUSTRY, allowed_values=["tech", "fintech", "enterprise-saas", "healthtech"]),
                ICPCriterion(dimension=ICPDimension.REVENUE, min_value=10_000_000, max_value=1_000_000_000),
                ICPCriterion(dimension=ICPDimension.EMPLOYEE_COUNT, min_value=50, max_value=10000),
            ],
            min_fit_score=0.7,
        )

    # === Kid/Adult Table (Tony Hughes) ===
    # Adult Table: decision-maker titles with high fit → full outreach sequence
    # Kid Table: low fit or non-DM titles → automated/nurture sequence

    _ADULT_TABLE_TITLES = {
        "ceo", "chief", "vp", "vice president", "president", "founder",
        "cfo", "cto", "cio", "coo", "cmo", "head of", "director of",
        "svp", "evp", "senior vice president", "executive vice president",
    }

    def _assign_table(self, prospect: Prospect) -> TableAssignment:
        title_lower = prospect.title.lower()
        is_mature_fit = prospect.fit_score >= 0.7
        is_decision_maker = any(t in title_lower for t in self._ADULT_TABLE_TITLES)
        if is_mature_fit and is_decision_maker:
            return TableAssignment.ADULT_TABLE
        return TableAssignment.KID_TABLE

    # === Reverse Funnel Math (Trish Bertuzzi) ===
    # Works backwards from pipeline target: how many outreaches are needed?

    @staticmethod
    def _reverse_funnel_math(
        pipeline_target: float = 5_000_000,
        avg_deal_size: float = 100_000,
        meeting_to_qualified: float = 0.4,
        contact_to_meeting: float = 0.15,
        outreach_to_contact: float = 0.25,
    ) -> dict:
        deals_needed = max(1, pipeline_target / avg_deal_size)
        meetings_needed = max(1, round(deals_needed / meeting_to_qualified))
        contacts_needed = max(1, round(meetings_needed / contact_to_meeting))
        outreaches_needed = max(1, round(contacts_needed / outreach_to_contact))
        return {
            "pipeline_target": pipeline_target,
            "avg_deal_size": avg_deal_size,
            "deals_needed": deals_needed,
            "meetings_needed": meetings_needed,
            "contacts_needed": contacts_needed,
            "outreaches_needed": outreaches_needed,
        }

    def _level_from_score(self, score: float) -> FitLevel:
        if score >= 0.9:
            return FitLevel.PERFECT
        elif score >= 0.7:
            return FitLevel.GOOD
        elif score >= 0.4:
            return FitLevel.MARGINAL
        return FitLevel.POOR
