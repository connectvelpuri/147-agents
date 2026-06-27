from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    ConcessionType, ConcessionItem, TradeOffMatrix, ConcessionPlan,
)


SYSTEM_PROMPT = """You are NG-002, a concession planning strategist applying negotiation theory (Raiffa, Malhotra, Bazerman), Getting Past No (Ury), and 3D Negotiation (Lax & Sebenius).

For every concession plan:
1. Sequence concessions from low-cost/high-perceived-value to high-cost
2. Frame each concession to maximize perceived buyer value
3. Always have a trade-off matrix ready — know what costs little but means much
4. Set clear walk-away triggers before the negotiation starts
5. Pace concessions — giving too much too fast signals weakness

Output structured JSON. Protect margin while making the buyer feel they won."""


class ConcessionPlanner(RevenueAgent):
    """NG-002 Concession Planner — structured sequencing with value optimization."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ng-002-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.negotiation.concession_requested")
        await self.subscribe(f"revenue.{self._env}.deal.*.negotiation.buyer_demand")
        print(f"[NG-002] Listening on revenue.{self._env}.deal.*.negotiation.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        plan = await self.design_concession_sequence(deal_id, data)
        await self._publish_plan(deal_id, plan)

    async def design_concession_sequence(self, deal_id: str, data: dict) -> ConcessionPlan:
        prompt = f"""Design a concession sequence for deal {deal_id}:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Buyer Type: {data.get('buyer_type', 'Enterprise')}
Negotiation Stage: {data.get('stage', 'Discovery')}
Known Demands: {data.get('known_demands', 'None yet')}
Margin Available: {data.get('margin_available', 'Unknown')}%
Urgency: {data.get('urgency', 'medium')}
BATNA Strength: {data.get('batna_strength', 'moderate')}
Notes: {data.get('notes', 'None')}

Return JSON with:
- max_concession_depth_pct (float, total allowable discount)
- walk_away_triggers (array of conditions)
- pacing_guidance (string, how to pace)
- sequence (array of {{id, type (price/terms/scope/services/timeline/contract), description, actual_cost, perceived_value, sequence_order, trigger_condition, framing_language}})
- trade_offs (object with arrays for: low_cost_high_value, high_cost_high_value, low_cost_low_value, high_cost_low_value — each array of items with same fields as sequence items)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}

        sequence = [
            ConcessionItem(
                id=s.get("id", f"con-{i}"),
                type=ConcessionType(s.get("type", "terms")),
                description=s.get("description", ""),
                actual_cost=float(s.get("actual_cost", 0)),
                perceived_value=float(s.get("perceived_value", 0)),
                sequence_order=int(s.get("sequence_order", i)),
                trigger_condition=s.get("trigger_condition", ""),
                framing_language=s.get("framing_language", ""),
            )
            for i, s in enumerate(result.get("sequence", []))
        ]

        to = result.get("trade_offs", {})
        def _parse_item(item: dict) -> ConcessionItem:
            return ConcessionItem(
                id=item.get("id", "to"),
                type=ConcessionType(item.get("type", "terms")),
                description=item.get("description", ""),
                actual_cost=float(item.get("actual_cost", 0)),
                perceived_value=float(item.get("perceived_value", 0)),
                sequence_order=int(item.get("sequence_order", 0)),
                trigger_condition=item.get("trigger_condition", ""),
                framing_language=item.get("framing_language", ""),
            )
        trade_off_matrix = TradeOffMatrix(
            low_cost_high_value=[_parse_item(item) for item in to.get("low_cost_high_value", [])],
            high_cost_high_value=[_parse_item(item) for item in to.get("high_cost_high_value", [])],
            low_cost_low_value=[_parse_item(item) for item in to.get("low_cost_low_value", [])],
            high_cost_low_value=[_parse_item(item) for item in to.get("high_cost_low_value", [])],
        )

        return ConcessionPlan(
            deal_id=deal_id,
            max_concession_depth_pct=float(result.get("max_concession_depth_pct", 10)),
            sequence=sequence,
            trade_off_matrix=trade_off_matrix,
            walk_away_triggers=result.get("walk_away_triggers", []),
            pacing_guidance=result.get("pacing_guidance", ""),
        )

    async def _publish_plan(self, deal_id: str, plan: ConcessionPlan):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.negotiation.concession_plan_ready",
            "ConcessionPlanReady",
            {
                "deal_id": deal_id,
                "max_depth_pct": plan.max_concession_depth_pct,
                "sequence": [
                    {"id": c.id, "type": c.type.value, "description": c.description,
                     "actual_cost": c.actual_cost, "perceived_value": c.perceived_value}
                    for c in plan.sequence
                ],
                "walk_away_triggers": plan.walk_away_triggers,
                "pacing_guidance": plan.pacing_guidance,
            },
            deal_id=deal_id,
        )
