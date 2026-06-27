from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    TermCategory, ImpactLevel,
    TermAnalysis, PaymentTermsOptimization,
    LiabilityExposure, TermsOptimizationReport,
)


SYSTEM_PROMPT = """You are NG-004, a commercial terms specialist applying IACCM standards, ASC 606 revenue recognition, and market standard contract analysis.

For every terms review:
1. Analyze each term for business impact — not just legal risk
2. Compare against market standards — know what's normal vs aggressive
3. Optimize payment terms for cash flow while maintaining competitiveness
4. Flag liability exposures and recommend specific mitigation
5. Prioritize actions by business impact

Output structured JSON. Terms are where margin goes to die — protect it."""


class TermsOptimizer(RevenueAgent):
    """NG-004 Terms Optimizer — analyzes and optimizes contract terms for business impact."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ng-004-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.contract.draft_received")
        await self.subscribe(f"revenue.{self._env}.deal.*.contract.legal_review_completed")
        print(f"[NG-004] Listening on revenue.{self._env}.deal.*.contract.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        report = await self.analyze_terms(deal_id, data)
        await self._publish_report(deal_id, report)

    async def analyze_terms(self, deal_id: str, data: dict) -> TermsOptimizationReport:
        prompt = f"""Analyze contract terms for deal {deal_id}:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Contract Type: {data.get('contract_type', 'SaaS')}
Key Terms: {data.get('key_terms', 'Not provided')}
Buyer Proposed Changes: {data.get('buyer_changes', 'None')}
Payment Structure: {data.get('payment_structure', 'Annual upfront')}
Industry: {data.get('industry', 'Technology')}
Legal Review Notes: {data.get('legal_notes', 'None')}

Return JSON with:
- analyses (array of {{clause, category (payment/liability/sla/renewal/ip/termination/data/compliance), impact (high/medium/low), risk, recommendation, market_standard}})
- payment_optimization (object with: current_terms, recommended_terms, cash_flow_impact (float), rationale) or null
- liability_exposures (array of {{clause, exposure, severity (high/medium/low), mitigation}})
- priority_actions (array of strings)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}

        valid_categories = {e.value for e in TermCategory}
        valid_impacts = {e.value for e in ImpactLevel}

        analyses = []
        for i, a in enumerate(result.get("analyses", [])):
            cat = a.get("category", "payment")
            imp = a.get("impact", "medium")
            analyses.append(TermAnalysis(
                clause=a.get("clause", f"Clause {i}"),
                category=TermCategory(cat) if cat in valid_categories else TermCategory.PAYMENT,
                impact=ImpactLevel(imp) if imp in valid_impacts else ImpactLevel.MEDIUM,
                risk=a.get("risk", ""),
                recommendation=a.get("recommendation", ""),
                market_standard=a.get("market_standard", ""),
            ))

        po_data = result.get("payment_optimization")
        payment_opt = PaymentTermsOptimization(
            current_terms=po_data.get("current_terms", ""),
            recommended_terms=po_data.get("recommended_terms", ""),
            cash_flow_impact=float(po_data.get("cash_flow_impact", 0)),
            rationale=po_data.get("rationale", ""),
        ) if po_data else None

        liabilities = []
        for l in result.get("liability_exposures", []):
            sv = l.get("severity", "medium")
            liabilities.append(LiabilityExposure(
                clause=l.get("clause", ""),
                exposure=l.get("exposure", ""),
                severity=ImpactLevel(sv) if sv in valid_impacts else ImpactLevel.MEDIUM,
                mitigation=l.get("mitigation", ""),
            ))

        return TermsOptimizationReport(
            deal_id=deal_id,
            analyses=analyses,
            payment_optimization=payment_opt,
            liability_exposures=liabilities,
            priority_actions=result.get("priority_actions", []),
        )

    async def _publish_report(self, deal_id: str, report: TermsOptimizationReport):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.contract.terms_optimized",
            "TermsOptimizationReady",
            {
                "deal_id": deal_id,
                "clauses_analyzed": len(report.analyses),
                "liability_exposures": [
                    {"clause": l.clause, "severity": l.severity.value, "exposure": l.exposure}
                    for l in report.liability_exposures
                ],
                "priority_actions": report.priority_actions,
            },
            deal_id=deal_id,
        )
