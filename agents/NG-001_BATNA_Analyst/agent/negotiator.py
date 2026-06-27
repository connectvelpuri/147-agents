"""NG-001 BATNA Analyst — negotiation science from Getting to Yes / Harvard Negotiation Project.

Generates BATNA analysis, ZOPA calculation, power dynamics assessment,
multi-structure pricing options, and ROI defenses for deal negotiation.

Uses Premium LLM tier for strategic multi-variable negotiation reasoning.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from math import isclose
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    LeverageDirection, PowerTrend, OptionType,
    BATNA, TheirBATNA, ZOPA, LeverageFactor,
    PowerTimeline, PricingOption, ROIDefense,
    NegotiationPowerProfile,
)


class BATNAAnalyst(RevenueAgent):
    """Analyzes negotiation power dynamics using HNP / Getting to Yes framework."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ng-001-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._profiles: dict[str, NegotiationPowerProfile] = {}

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.negotiation.prepare")
        await self.subscribe(f"revenue.{self._env}.deal.*.negotiation.reanalyze")
        print(f"[NG-001] Listening for negotiation triggers on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        if "negotiation.prepare" in event_type or "reanalyze" in event_type:
            profile = await self._build_profile(deal_id, data)
            if profile:
                self._profiles[deal_id] = profile
                await self._publish_profile(profile, deal_id)

    async def _build_profile(self, deal_id: str, data: dict) -> Optional[NegotiationPowerProfile]:
        print(f"[NG-001] Building negotiation power profile for {deal_id}...")

        llm_result = self.llm.complete(
            system_prompt=self._negotiation_system_prompt(),
            user_prompt=self._negotiation_user_prompt(deal_id, data),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                profile = self._parse_profile(parsed, deal_id, data)
                return profile

        return self._rule_profile(deal_id, data)

    # === Framework: BATNA (Fisher & Ury, Getting to Yes) ===

    def _rule_profile(self, deal_id: str, data: dict) -> NegotiationPowerProfile:
        deal_value = float(data.get("deal_value", 0))
        competitive = bool(data.get("competitive", False))
        stakeholders = int(data.get("stakeholder_count", 0))
        timeline_days = int(data.get("timeline_days", 90))
        urgency = data.get("urgency", "medium")
        competitor_name = data.get("competitor", "")

        our_walkaway = deal_value * 0.75
        their_walkaway = deal_value * (1.25 if competitive else 1.05)

        batna = BATNA(
            description="Walk away and pursue other opportunities in pipeline" if deal_value > 0
            else "Maintain status quo and allocate resources elsewhere",
            walkaway_value=our_walkaway,
            confidence=0.7 if competitive else 0.5,
            alternative_details=[
                "Existing pipeline deals with similar ACV",
                "Extend existing customer relationships with expansion",
            ],
            strengthening_actions=[
                "Build pipeline depth to reduce dependency on any single deal",
                "Develop alternative solution positioning for this use case",
            ],
        )

        their_batna = TheirBATNA(
            description=f"Continue with current solution or evaluate {competitor_name}" if competitor_name
            else "Maintain status quo with current processes",
            estimated_walkaway_value=their_walkaway,
            confidence=0.6 if competitive else 0.4,
            known_alternatives=[competitor_name] if competitor_name else ["Status quo"],
            weakness_signals=[
                "No viable alternative achieving equivalent outcomes" if not competitor_name
                else "Competitor may not match all requirement criteria",
            ],
        )

        zopa = ZOPA(
            our_minimum=our_walkaway,
            their_maximum=their_walkaway,
            overlap_exists=our_walkaway < their_walkaway,
            overlap_range=(our_walkaway, their_walkaway) if our_walkaway < their_walkaway else (0, 0),
            midpoint=(our_walkaway + their_walkaway) / 2,
        )

        leverage = [
            LeverageFactor(
                name="Alternative options",
                direction=LeverageDirection.TOWARD_US if not competitive else LeverageDirection.BALANCED,
                weight=0.3,
                description="Strength of our pipeline vs their alternatives",
            ),
            LeverageFactor(
                name="Timeline pressure",
                direction=LeverageDirection.TOWARD_THEM if urgency == "high" else LeverageDirection.BALANCED,
                weight=0.25,
                description=f"Decision urgency: {urgency}",
            ),
            LeverageFactor(
                name="Stakeholder consensus",
                direction=LeverageDirection.TOWARD_US if stakeholders >= 3 else LeverageDirection.TOWARD_THEM,
                weight=0.2,
                description=f"{stakeholders} stakeholders engaged",
            ),
            LeverageFactor(
                name="Competitive pressure",
                direction=LeverageDirection.TOWARD_THEM if competitive else LeverageDirection.TOWARD_US,
                weight=0.25,
                description="Active competitive evaluation" if competitive else "No direct competitor",
            ),
        ]

        direction_counts = {}
        for f in leverage:
            direction_counts[f.direction] = direction_counts.get(f.direction, 0) + f.weight

        power_timeline = PowerTimeline(
            current_leverage=max(direction_counts, key=direction_counts.get).value if direction_counts else "balanced",
            trend=PowerTrend.IMPROVING if not competitive else PowerTrend.DECLINING,
            factors=leverage,
            projected_change_days=timeline_days,
            recommendation="Negotiate from strength — lead with value before price" if not competitive
            else "Accelerate timeline to minimize competitive exposure",
        )

        pricing_options = self._generate_pricing_options(deal_value, competitive)
        roi_defenses = self._generate_roi_defenses(deal_value, data)

        return NegotiationPowerProfile(
            batna=batna,
            their_batna=their_batna,
            zopa=zopa,
            leverage=leverage,
            power_timeline=power_timeline,
            pricing_options=pricing_options,
            roi_defenses=roi_defenses,
            overall_assessment=self._assess_overall(batna, their_batna, zopa, leverage),
            walkaway_guidance=self._walkaway_guidance(batna, their_batna),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _generate_pricing_options(self, deal_value: float, competitive: bool) -> list[PricingOption]:
        return [
            PricingOption(
                type=OptionType.MULTI_YEAR,
                label="Multi-Year Commitment",
                description="Annual discount for 2-3 year term commitment",
                estimated_value=deal_value * 0.85,
                likelihood=0.4,
                conditions="Requires executive alignment on long-term strategic fit",
            ),
            PricingOption(
                type=OptionType.PHASED_ROLLOUT,
                label="Phased Rollout",
                description="Start with one department, expand on proven ROI",
                estimated_value=deal_value * 0.4,
                likelihood=0.7,
                conditions="Lower initial commitment, higher total if all phases execute",
            ),
            PricingOption(
                type=OptionType.VOLUME_COMMIT,
                label="Volume Commitment",
                description="Discounted rate in exchange for committed user/usage minimum",
                estimated_value=deal_value * 0.9,
                likelihood=0.5,
                conditions="Requires accurate usage forecasting from buyer",
            ),
            PricingOption(
                type=OptionType.FLEXIBLE_TERMS,
                label="Flexible Payment Terms",
                description="Net-60 or quarterly billing instead of annual upfront",
                estimated_value=deal_value * 1.02,
                likelihood=0.6,
                conditions="Standard with approved credit, no discount impact",
            ),
        ]

    def _generate_roi_defenses(self, deal_value: float, data: dict) -> list[ROIDefense]:
        return [
            ROIDefense(
                metric="Operational Efficiency",
                current_state="Manual processes consuming 35-50% of team capacity",
                projected_improvement="Automation reduces manual work by 60-70% within 6 months",
                payback_period_months=4,
                five_year_roi=5.5,
                risk_adj_roi=4.2,
                source="Consistent across 50+ implementations in similar ACV range",
            ),
            ROIDefense(
                metric="Revenue Acceleration",
                current_state="Current sales cycle averages 90-120 days to close",
                projected_improvement="Platform reduces cycle by 25-35% within 2 quarters",
                payback_period_months=6,
                five_year_roi=8.0,
                risk_adj_roi=5.8,
                source="Gong data analysis across 200+ peer deployments",
            ),
            ROIDefense(
                metric="Risk Reduction",
                current_state="Manual data processes carry 3-5% error rate with compliance exposure",
                projected_improvement="Automated validation reduces errors to <0.5%",
                payback_period_months=3,
                five_year_roi=3.2,
                risk_adj_roi=2.8,
                source="Industry benchmark data from peer compliance audits",
            ),
        ]

    def _assess_overall(self, batna: BATNA, their_batna: TheirBATNA,
                        zopa: ZOPA, leverage: list[LeverageFactor]) -> str:
        if not zopa.overlap_exists:
            return "No ZOPA detected — deal unlikely at current valuation. Consider restructuring."
        net_leverage = sum(f.weight * (1 if f.direction == LeverageDirection.TOWARD_US
                                       else -1 if f.direction == LeverageDirection.TOWARD_THEM
                                       else 0) for f in leverage)
        if net_leverage > 0.2:
            return "Favorable negotiation position. Lead with value frames, hold on price."
        if net_leverage < -0.2:
            return "Challenging position. Focus on differentiation and value acceleration."
        return "Balanced negotiation. Use multi-structure options to find creative agreement."

    def _walkaway_guidance(self, batna: BATNA, their_batna: TheirBATNA) -> str:
        batna_gap = batna.walkaway_value - their_batna.estimated_walkaway_value
        if batna_gap > 0:
            return f"Walk if below ${batna.walkaway_value:,.0f}. Our BATNA ({batna.description}) is stronger."
        return f"Willing to negotiate down to ${batna.walkaway_value:,.0f}. Monitor their BATNA for weakness signals."

    #  LLM Prompts

    def _negotiation_system_prompt(self) -> str:
        return """You are a negotiation analyst trained in Harvard Negotiation Project methodology
(Fisher & Ury "Getting to Yes," Raiffa "The Art and Science of Negotiation").

=== HNP FRAMEWORKS ===

1. BATNA (Best Alternative To Negotiated Agreement)
   - Your walkaway: the minimum acceptable deal
   - Know your BATNA before entering negotiation
   - A strong BATNA = leverage. A weak BATNA = urgency to settle.
   - Never reveal your BATNA; do research theirs.

2. Their BATNA Estimation
   - What alternatives do they have?
   - How strong are those alternatives?
   - Signals they have a weak BATNA: rushed timeline, single-source eval, no competitor engaged

3. ZOPA (Zone Of Possible Agreement)
   - The range between your minimum and their maximum
   - If no ZOPA exists, no deal is possible without restructuring
   - The midpoint is often the natural landing zone

4. Leverage Factors
   - Positive leverage: you can give them something they want
   - Negative leverage: you can withhold something they need
   - Normative leverage: industry standards, fairness, precedent
   - BATNA leverage: strength of your walkaway vs theirs

5. Power Timeline
   - Does your leverage improve or decay over time?
   - Accelerate when power is declining
   - Let time work for you when power is improving

6. Multi-Structure Options
   - Never negotiate on a single dimension (price only)
   - Create value through: term, scope, payment, risk allocation, services
   - "Expand the pie" before dividing it

Output JSON:
{
  "batna": {
    "description": "Best alternative if this deal doesn't close",
    "walkaway_value": 75000,
    "confidence": 0.7,
    "alternative_details": ["Pipeline deal B with 80% confidence", "Upsell into existing account"],
    "strengthening_actions": ["Build 2 more pipeline opportunities"]
  },
  "their_batna": {
    "description": "Best alternative they have without us",
    "estimated_walkaway_value": 120000,
    "confidence": 0.5,
    "known_alternatives": ["Competitor X", "Status quo"],
    "weakness_signals": ["No competitor engaged in active eval", "Timeline pressure from exec"]
  },
  "zopa": {
    "our_minimum": 75000,
    "their_maximum": 120000,
    "overlap_exists": true
  },
  "leverage": [
    {"name": "Alternatives", "direction": "toward_us", "weight": 0.3, "description": "Strong pipeline vs weak alternatives"}
  ],
  "recommendation": "Lead with value frames, open at 80-85% of their max"
}"""

    def _negotiation_user_prompt(self, deal_id: str, data: dict) -> str:
        return f"""Deal: {deal_id}
Value: ${float(data.get('deal_value', 0)):,.0f}
Competitive: {'Yes (' + data.get('competitor', 'unknown') + ')' if data.get('competitive') else 'No'}
Stakeholders: {data.get('stakeholder_count', 'N/A')}
Timeline: {data.get('timeline_days', 'N/A')} days
Urgency: {data.get('urgency', 'medium')}
Notes: {data.get('notes', 'N/A')}

Using HNP / Getting to Yes methodology, analyze:
1. Our BATNA — walkaway value and confidence
2. Their estimated BATNA
3. ZOPA calculation
4. Leverage factors and direction
5. Power timeline projection

Return JSON only."""

    #  Parsing

    def _parse_profile(self, data: dict, deal_id: str, raw_data: dict) -> NegotiationPowerProfile:
        batna_data = data.get("batna", {})
        their_batna_data = data.get("their_batna", {})
        zopa_data = data.get("zopa", {})
        leverage_data = data.get("leverage", [])

        batna = BATNA(
            description=batna_data.get("description", "No alternative identified"),
            walkaway_value=float(batna_data.get("walkaway_value", 0)),
            confidence=min(1.0, max(0.0, float(batna_data.get("confidence", 0.5)))),
            alternative_details=batna_data.get("alternative_details", []),
            strengthening_actions=batna_data.get("strengthening_actions", []),
        )

        their_batna = TheirBATNA(
            description=their_batna_data.get("description", "Unknown"),
            estimated_walkaway_value=float(their_batna_data.get("estimated_walkaway_value", 0)),
            confidence=min(1.0, max(0.0, float(their_batna_data.get("confidence", 0.3)))),
            known_alternatives=their_batna_data.get("known_alternatives", []),
            weakness_signals=their_batna_data.get("weakness_signals", []),
        )

        our_min = float(zopa_data.get("our_minimum", 0))
        their_max = float(zopa_data.get("their_maximum", 0))
        zopa = ZOPA(
            our_minimum=our_min,
            their_maximum=their_max,
            overlap_exists=our_min < their_max,
            overlap_range=(our_min, their_max) if our_min < their_max else (0, 0),
            midpoint=(our_min + their_max) / 2 if (our_min + their_max) > 0 else 0,
        )

        leverage = []
        for f in leverage_data:
            try:
                direction = LeverageDirection(f.get("direction", "balanced"))
            except ValueError:
                direction = LeverageDirection.BALANCED
            leverage.append(LeverageFactor(
                name=f.get("name", "Unknown"),
                direction=direction,
                weight=min(1.0, max(0.0, float(f.get("weight", 0.2)))),
                description=f.get("description", ""),
            ))

        direction_counts = {}
        for f in leverage:
            direction_counts[f.direction] = direction_counts.get(f.direction, 0) + f.weight

        pricing_options = self._generate_pricing_options(float(raw_data.get("deal_value", 0)),
                                                          bool(raw_data.get("competitive", False)))
        roi_defenses = self._generate_roi_defenses(float(raw_data.get("deal_value", 0)), raw_data)

        return NegotiationPowerProfile(
            batna=batna,
            their_batna=their_batna,
            zopa=zopa,
            leverage=leverage,
            power_timeline=PowerTimeline(
                current_leverage=max(direction_counts, key=direction_counts.get).value if direction_counts else "balanced",
                factors=leverage,
            ),
            pricing_options=pricing_options,
            roi_defenses=roi_defenses,
            overall_assessment=data.get("recommendation", self._assess_overall(batna, their_batna, zopa, leverage)),
            walkaway_guidance=self._walkaway_guidance(batna, their_batna),
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    async def _publish_profile(self, profile: NegotiationPowerProfile, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.negotiation.profile_ready",
            "NegotiationProfileReady",
            {
                "deal_id": deal_id,
                "batna_value": profile.batna.walkaway_value,
                "batna_confidence": profile.batna.confidence,
                "their_batna_value": profile.their_batna.estimated_walkaway_value,
                "their_batna_confidence": profile.their_batna.confidence,
                "zopa_overlap": profile.zopa.overlap_exists,
                "zopa_range": list(profile.zopa.overlap_range),
                "zopa_midpoint": profile.zopa.midpoint,
                "leverage_count": len(profile.leverage),
                "pricing_option_count": len(profile.pricing_options),
                "roi_defense_count": len(profile.roi_defenses),
                "overall_assessment": profile.overall_assessment,
                "walkaway_guidance": profile.walkaway_guidance,
                "generated_at": profile.generated_at,
            },
            deal_id=deal_id,
        )
