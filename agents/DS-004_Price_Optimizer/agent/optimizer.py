from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    PriceSensitivity, PriceSensitivityProfile,
    PriceRecommendation, DiscountImpactAnalysis,
)


SYSTEM_PROMPT = """You are DS-004, a price optimization strategist applying value-based pricing (Donovan, Hinterhuber), pricing strategy (Tom Nagle), and Van Westendorp price sensitivity measurement.

For every pricing recommendation:
1. Assess the buyer's price sensitivity — segment, willingness-to-pay, reference price
2. Recommend an optimal price balancing win probability and margin
3. Quantify discount impact before accepting any reduction
4. Always justify price with value delivered, not cost

Output structured JSON. Protect margin while maximizing win rate."""


class PriceOptimizer(RevenueAgent):
    """DS-004 Price Optimizer — value-based pricing with win-rate optimization."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-004-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.pricing.requested")
        await self.subscribe(f"revenue.{self._env}.deal.*.discount.requested")
        print(f"[DS-004] Listening on revenue.{self._env}.deal.*.pricing.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}
        event_type = envelope.event_type

        if "pricing.requested" in event_type:
            profile = await self.analyze_price_sensitivity(deal_id, data)
            recommendation = await self.recommend_optimal_price(profile, data)
            await self._publish_price(deal_id, recommendation)
        elif "discount.requested" in event_type:
            impact = await self.calculate_discount_impact(data)
            await self._publish_discount_impact(deal_id, impact)

    async def analyze_price_sensitivity(self, deal_id: str, data: dict) -> PriceSensitivityProfile:
        prompt = f"""Analyze price sensitivity for deal {deal_id}:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Buyer Segment: {data.get('segment', 'Enterprise')}
Industry: {data.get('industry', 'Unknown')}
Competitive Context: {data.get('competitive_context', 'Unknown')}
Buyer Budget: {data.get('buyer_budget', 'Unknown')}
Historical Win Rate at Price: {data.get('historical_win_rate', 'Unknown')}
Notes: {data.get('notes', 'None')}

Return JSON with:
- segment (string)
- sensitivity (high/moderate/low)
- willingness_to_pay (float)
- discount_elasticity (0.0-1.0)
- reference_price (float)
- key_factors (array of strings)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return PriceSensitivityProfile(
            segment=data.get("segment", "Enterprise"),
            sensitivity=PriceSensitivity(result.get("sensitivity", "moderate")),
            willingness_to_pay=float(result.get("willingness_to_pay", 0)),
            discount_elasticity=float(result.get("discount_elasticity", 0.5)),
            reference_price=float(result.get("reference_price", 0)),
            key_factors=result.get("key_factors", []),
        )

    async def recommend_optimal_price(self, profile: PriceSensitivityProfile, data: dict) -> PriceRecommendation:
        prompt = f"""Recommend an optimal price:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Sensitivity: {profile.sensitivity.value}
Willingness to Pay: ${profile.willingness_to_pay:,.0f}
Discount Elasticity: {profile.discount_elasticity:.1f}
Reference Price: ${profile.reference_price:,.0f}
Key Factors: {', '.join(profile.key_factors)}
Competitive Pressure: {data.get('competitive_pressure', 'unknown')}

Return JSON with:
- recommended_price (float)
- rationale (string)
- expected_win_rate (0.0-1.0)
- margin_impact (0.0-1.0, as fraction of target margin)
- floor_price (float, minimum acceptable)
- ceiling_price (float, maximum justifiable)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return PriceRecommendation(
            recommended_price=float(result.get("recommended_price", 0)),
            rationale=result.get("rationale", ""),
            expected_win_rate=float(result.get("expected_win_rate", 0.5)),
            margin_impact=float(result.get("margin_impact", 0)),
            floor_price=float(result.get("floor_price", 0)),
            ceiling_price=float(result.get("ceiling_price", 0)),
        )

    async def calculate_discount_impact(self, data: dict) -> DiscountImpactAnalysis:
        prompt = f"""Analyze discount impact:

Deal Value: ${float(data.get('deal_value', 0)):,.0f}
Requested Discount: {data.get('discount_pct', 0)}%
Current Margin: {data.get('margin_pct', 70)}%
Competitive Pressure: {data.get('competitive_pressure', 'none')}

Return JSON with:
- requested_discount_pct (float)
- revenue_impact (float, $ amount lost)
- margin_impact_pct (float, margin compression)
- break_even_units (int, additional units needed)
- alternative_suggestions (array of strings)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return DiscountImpactAnalysis(
            requested_discount_pct=float(result.get("requested_discount_pct", 0)),
            revenue_impact=float(result.get("revenue_impact", 0)),
            margin_impact_pct=float(result.get("margin_impact_pct", 0)),
            break_even_units=int(result.get("break_even_units", 0)),
            alternative_suggestions=result.get("alternative_suggestions", []),
        )

    async def _publish_price(self, deal_id: str, rec: PriceRecommendation):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.pricing.optimized",
            "PriceOptimizationReady",
            {
                "deal_id": deal_id,
                "recommended_price": rec.recommended_price,
                "expected_win_rate": rec.expected_win_rate,
                "margin_impact": rec.margin_impact,
                "floor_price": rec.floor_price,
                "ceiling_price": rec.ceiling_price,
                "rationale": rec.rationale,
            },
            deal_id=deal_id,
        )

    async def _publish_discount_impact(self, deal_id: str, impact: DiscountImpactAnalysis):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.pricing.discount_analyzed",
            "DiscountImpactAnalyzed",
            {
                "deal_id": deal_id,
                "requested_discount_pct": impact.requested_discount_pct,
                "revenue_impact": impact.revenue_impact,
                "margin_impact_pct": impact.margin_impact_pct,
                "break_even_units": impact.break_even_units,
                "alternatives": impact.alternative_suggestions,
            },
            deal_id=deal_id,
        )
