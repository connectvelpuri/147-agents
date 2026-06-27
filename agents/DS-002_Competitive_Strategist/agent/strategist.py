from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    StrategicDirection, CompetitorStrength,
    CompetitorProfile, LandscapeAssessment, PositioningStrategy,
)


SYSTEM_PROMPT = """You are DS-002, a competitive positioning strategist applying Michael Porter (Five Forces), Blue Ocean Strategy (Kim & Mauborgne), and Trout & Ries positioning.

For every analysis:
1. Map the competitive landscape objectively — know every player's position
2. Choose differentiate/neutralize/cede per competitor
3. Exploit strengths ruthlessly, mitigate weaknesses systematically
4. Frame the landscape favorably — buyer should see us as the obvious choice

Output structured JSON. Be specific and honest — bad intelligence loses deals."""


class CompetitiveStrategist(RevenueAgent):
    """DS-002 Competitive Positioning Strategist — Porter/Blue Ocean positioning."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-002-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.competitive.intel_updated")
        await self.subscribe(f"revenue.{self._env}.deal.*.competitor.identified")
        print(f"[DS-002] Listening on revenue.{self._env}.deal.*.competitive.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        assessment = await self.analyze_competitive_landscape(deal_id, data)
        strategy = await self.develop_positioning_strategy(assessment, data)
        await self._publish_strategy(deal_id, strategy)

    async def analyze_competitive_landscape(self, deal_id: str, data: dict) -> LandscapeAssessment:
        prompt = f"""Analyze the competitive landscape for deal {deal_id}:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Buyer: {data.get('buyer_name', 'Unknown')}
Industry: {data.get('industry', 'Unknown')}
Competitors: {data.get('competitors', 'Not specified')}
Our Strengths: {data.get('our_strengths', 'Not specified')}
Buyer Priorities: {data.get('buyer_priorities', 'Not specified')}
Notes: {data.get('notes', 'None')}

Return JSON with:
- competitors (array of {{name, strength (strong/moderate/weak), differentiators, vulnerabilities, typical_positioning, win_rate_against_us}})
- our_advantages (array)
- our_vulnerabilities (array)
- buyer_priorities (array)
- summary (string)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return LandscapeAssessment(
            competitors=[
                CompetitorProfile(
                    name=c.get("name", f"Competitor {i}"),
                    strength=CompetitorStrength(c.get("strength", "moderate")),
                    differentiators=c.get("differentiators", []),
                    vulnerabilities=c.get("vulnerabilities", []),
                    typical_positioning=c.get("typical_positioning", ""),
                    win_rate_against_us=float(c.get("win_rate_against_us", 0)) if isinstance(c.get("win_rate_against_us"), (int, float)) else 0.5,
                )
                for i, c in enumerate(result.get("competitors", []))
            ],
            our_advantages=result.get("our_advantages", []),
            our_vulnerabilities=result.get("our_vulnerabilities", []),
            buyer_priorities=result.get("buyer_priorities", []),
            summary=result.get("summary", ""),
        )

    async def develop_positioning_strategy(self, assessment: LandscapeAssessment, data: dict) -> PositioningStrategy:
        competitors_json = json.dumps([
            {"name": c.name, "strength": c.strength.value, "differentiators": c.differentiators}
            for c in assessment.competitors
        ])
        prompt = f"""Develop a competitive positioning strategy:

Our Advantages: {', '.join(assessment.our_advantages)}
Our Vulnerabilities: {', '.join(assessment.our_vulnerabilities)}
Buyer Priorities: {', '.join(assessment.buyer_priorities)}
Competitors: {competitors_json}

Return JSON with:
- direction: "differentiate" | "neutralize" | "cede"
- primary_narrative (how to frame the landscape)
- strength_exploitation (array of actions)
- weakness_mitigation (array of actions)
- key_messages (array of positioning statements)
- risk_points (array of risks)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return PositioningStrategy(
            direction=StrategicDirection(result.get("direction", "differentiate")),
            primary_narrative=result.get("primary_narrative", ""),
            strength_exploitation=result.get("strength_exploitation", []),
            weakness_mitigation=result.get("weakness_mitigation", []),
            key_messages=result.get("key_messages", []),
            risk_points=result.get("risk_points", []),
        )

    async def _publish_strategy(self, deal_id: str, strategy: PositioningStrategy):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.competitive.positioning_ready",
            "CompetitivePositioningReady",
            {
                "deal_id": deal_id,
                "direction": strategy.direction.value,
                "narrative": strategy.primary_narrative,
                "key_messages": strategy.key_messages,
                "strength_exploitation": strategy.strength_exploitation,
                "weakness_mitigation": strategy.weakness_mitigation,
                "risk_points": strategy.risk_points,
            },
            deal_id=deal_id,
        )
