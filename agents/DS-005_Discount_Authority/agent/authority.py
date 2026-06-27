from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    ApprovalDecision, ApprovalLevel,
    DiscountRequest, DiscountDecision,
)


DISCOUNT_AUTHORITY_MATRIX = {
    "sdr": {"max_pct": 5, "approval_level": ApprovalLevel.REP_LEVEL},
    "bdr": {"max_pct": 5, "approval_level": ApprovalLevel.REP_LEVEL},
    "ae": {"max_pct": 10, "approval_level": ApprovalLevel.MANAGER},
    "senior_ae": {"max_pct": 15, "approval_level": ApprovalLevel.VP},
    "manager": {"max_pct": 20, "approval_level": ApprovalLevel.C_LEVEL},
    "director": {"max_pct": 25, "approval_level": ApprovalLevel.CEO},
}

HIGH_VALUE_THRESHOLD = 50000


class DiscountAuthority(RevenueAgent):
    """DS-005 Discount Authority — policy enforcement with structured concession paths."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-005-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.discount.rep_requested")
        await self.subscribe(f"revenue.{self._env}.quarter_end.approaching")
        print(f"[DS-005] Listening on revenue.{self._env}.deal.*.discount.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        request = DiscountRequest(
            deal_id=deal_id,
            rep_name=data.get("rep_name", "Unknown"),
            rep_role=data.get("rep_role", "ae").lower(),
            deal_value=float(data.get("deal_value", 0)),
            requested_discount_pct=float(data.get("discount_pct", 0)),
            current_margin_pct=float(data.get("margin_pct", 70)),
            competitive_pressure=data.get("competitive_pressure", "none"),
            buyer_relationship=data.get("buyer_relationship", "new"),
            reason=data.get("reason", ""),
        )

        decision = await self.evaluate_discount(request)
        await self._publish_decision(deal_id, decision)

    async def evaluate_discount(self, request: DiscountRequest) -> DiscountDecision:
        role_key = request.rep_role.replace(" ", "_")
        authority = DISCOUNT_AUTHORITY_MATRIX.get(role_key, {"max_pct": 0, "approval_level": ApprovalLevel.CEO})

        within_authority = request.requested_discount_pct <= authority["max_pct"]
        high_value = request.deal_value > HIGH_VALUE_THRESHOLD

        if within_authority and not high_value:
            return DiscountDecision(
                deal_id=request.deal_id,
                decision=ApprovalDecision.APPROVED,
                approval_level=authority["approval_level"],
                approved_discount_pct=request.requested_discount_pct,
                rationale=f"Within {request.rep_role} authority ({authority['max_pct']}%)",
                conditions=[],
                alternative_concessions=self._suggest_concessions(request),
            )

        if high_value:
            return DiscountDecision(
                deal_id=request.deal_id,
                decision=ApprovalDecision.ESCALATED,
                approval_level=ApprovalLevel.C_LEVEL,
                approved_discount_pct=authority["max_pct"],
                rationale=f"Deal value ${request.deal_value:,.0f} exceeds high-value threshold. Requires C-level approval.",
                conditions=["C-level review required", "Competitive analysis required"],
                alternative_concessions=self._suggest_concessions(request),
            )

        decision = await self._llm_evaluate(request, authority)
        return decision

    async def _llm_evaluate(self, request: DiscountRequest, authority: dict) -> DiscountDecision:
        prompt = f"""Evaluate this discount request:

Deal: {request.deal_id}
Rep: {request.rep_name} ({request.rep_role})
Deal Value: ${request.deal_value:,.0f}
Requested Discount: {request.requested_discount_pct}%
Current Margin: {request.current_margin_pct}%
Competitive Pressure: {request.competitive_pressure}
Buyer Relationship: {request.buyer_relationship}
Reason: {request.reason}
Max Authority for Role: {authority['max_pct']}%

Return JSON with:
- decision: "approved" | "denied" | "modified"
- approved_discount_pct (float, actual approved amount)
- rationale (string)
- conditions (array of strings)
- alternative_concessions (array of strings)"""
        llm_result = self.llm.complete(system_prompt="You are DS-005, discount authority evaluator.", user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return DiscountDecision(
            deal_id=request.deal_id,
            decision=ApprovalDecision(result.get("decision", "denied")),
            approval_level=ApprovalLevel.C_LEVEL if request.deal_value > HIGH_VALUE_THRESHOLD else authority["approval_level"],
            approved_discount_pct=float(result.get("approved_discount_pct", request.requested_discount_pct)),
            rationale=result.get("rationale", ""),
            conditions=result.get("conditions", []),
            alternative_concessions=result.get("alternative_concessions", self._suggest_concessions(request)),
        )

    def _suggest_concessions(self, request: DiscountRequest) -> list[str]:
        suggestions = []
        if request.deal_value > 10000:
            suggestions.append("Offer phased payment terms instead of discount")
        suggestions.append("Bundle professional services at reduced rate")
        suggestions.append("Extend contract term for volume pricing")
        suggestions.append("Offer implementation support instead of price reduction")
        return suggestions

    async def _publish_decision(self, deal_id: str, decision: DiscountDecision):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.discount.decision_made",
            "DiscountDecisionMade",
            {
                "deal_id": deal_id,
                "decision": decision.decision.value,
                "approved_discount_pct": decision.approved_discount_pct,
                "rationale": decision.rationale,
                "conditions": decision.conditions,
                "alternatives": decision.alternative_concessions,
            },
            deal_id=deal_id,
        )
