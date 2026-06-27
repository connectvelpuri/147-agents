"""SDR-004 Strategic Negotiator — Give-Get, Value=Progress, Mirror Attack, Calibrated Absence.

Implements four advanced negotiation frameworks:
1. Give-Get (Bob Burg): Every ask must be preceded by a give
2. Value=Progress (Jeff Shore): Value = measurable progress toward a goal
3. Mirror Attack (Oren Klaff): Match their frame, then reframe
4. Calibrated Absence (Stuart Diamond): Strategic silence as leverage
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    NegotiationPhase, NegotiationMove, DealContext,
    GiveGetPair, ValueProgressFrame, MirrorAttack,
    CalibratedAbsence, NegotiationPlan, NegotiationOutcome,
)


class StrategicNegotiator(RevenueAgent):
    """Agent SDR-004: applies 4 advanced negotiation frameworks to close deals."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="sdr-004-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.negotiation.plan.requested")
        await self.subscribe(f"revenue.{self._env}.deal.*.objection.detected")
        print(f"[SDR-004] Listening for negotiation triggers on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        if "negotiation.plan.requested" in event_type:
            plan = await self._build_plan(deal_id, data)
            await self._publish_plan(plan, deal_id)
        elif "objection.detected" in event_type:
            move = await self._respond_to_objection(deal_id, data)
            await self._publish_move(move, deal_id)

    async def _build_plan(self, deal_id: str, data: dict) -> NegotiationPlan:
        ctx = DealContext(
            deal_id=deal_id,
            prospect_name=data.get("prospect_name", ""),
            prospect_title=data.get("prospect_title", ""),
            company=data.get("company", ""),
            deal_value=float(data.get("deal_value", 0)),
            current_stage=data.get("stage", "discovery"),
            objections=data.get("objections", []),
            stakeholders=data.get("stakeholders", []),
            timeline=data.get("timeline", ""),
            competitor=data.get("competitor", ""),
            notes=data.get("notes", ""),
        )

        give_gets = self._generate_give_gets(ctx)
        value_frames = self._generate_value_frames(ctx)
        mirror_attacks = self._generate_mirror_attacks(ctx)
        absences = self._generate_calibrated_absences(ctx)
        script = self._build_script(ctx, give_gets, value_frames, mirror_attacks, absences)
        moves = [NegotiationMove.GIVE_GET, NegotiationMove.VALUE_PROGRESS,
                 NegotiationMove.MIRROR_ATTACK, NegotiationMove.CALIBRATED_ABSENCE]

        return NegotiationPlan(
            deal_id=deal_id,
            context=ctx,
            phase=NegotiationPhase(self._map_stage_to_phase(ctx.current_stage)),
            moves=moves,
            give_gets=give_gets,
            value_frames=value_frames,
            mirror_attacks=mirror_attacks,
            calibrated_absences=absences,
            recommended_approach=self._recommend_approach(ctx),
            script=script,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    # === Framework: Give-Get (Bob Burg) ===

    def _generate_give_gets(self, ctx: DealContext) -> list[GiveGetPair]:
        pairs = []
        if ctx.deal_value > 0:
            pairs.append(GiveGetPair(
                give="Complimentary onboarding consultation to map your team's workflow",
                get="Dedicated champion to provide feedback during implementation",
                rationale="Pre-committed collaboration reduces churn risk",
            ))
        if ctx.stakeholders:
            pairs.append(GiveGetPair(
                give="Custom ROI model tailored to each stakeholder's KPIs",
                get="Joint meeting with all decision-makers on the same call",
                rationale="Multi-threaded engagement accelerates consensus",
            ))
        if ctx.timeline:
            pairs.append(GiveGetPair(
                give="Expedited security review and compliance documentation",
                get="Commitment to evaluation timeline before quarter-end",
                rationale="Timeline certainty reduces pipeline forecast variance",
            ))
        return pairs

    # === Framework: Value=Progress (Jeff Shore) ===

    def _generate_value_frames(self, ctx: DealContext) -> list[ValueProgressFrame]:
        frames = [
            ValueProgressFrame(
                metric="Revenue efficiency",
                current_state="Manual processes consuming 40% of team capacity",
                desired_state="Automated workflows freeing 60% of capacity for revenue-generating activity",
                progress_gap="20% automation gap",
                value_proposition="Our platform turns that 20% gap into $X new pipeline monthly",
            ),
            ValueProgressFrame(
                metric="Time-to-value",
                current_state="Current solution requires 6+ months to show ROI",
                desired_state="Value realization within 30 days",
                progress_gap="5-month acceleration opportunity",
                value_proposition="We compress the path from investment to measurable return",
            ),
        ]
        if ctx.competitor:
            frames.append(ValueProgressFrame(
                metric="Competitive advantage",
                current_state="Current vendor delivers 60% of desired outcomes",
                desired_state="Full outcome coverage with integrated platform",
                progress_gap="40% capability gap vs available alternatives",
                value_proposition=f"Unlike {ctx.competitor}, our solution covers the full workflow",
            ))
        return frames

    # === Framework: Mirror Attack (Oren Klaff) ===

    def _generate_mirror_attacks(self, ctx: DealContext) -> list[MirrorAttack]:
        attacks = []
        if ctx.objections:
            for obj in ctx.objections[:2]:
                attacks.append(MirrorAttack(
                    their_frame=obj,
                    mirrored_response=f"I understand your concern about {obj.lower()} — that's exactly the right thing to be thinking about.",
                    reframe=f"Let me show you how other {ctx.company}-sized companies used this exact situation to gain an advantage.",
                    evidence=f"3 of 5 recent clients in similar industries raised this same point before adopting.",
                ))
        attacks.append(MirrorAttack(
            their_frame="We need to think about this more",
            mirrored_response="You're right — this is a big decision and deserves proper consideration.",
            reframe="At the same time, every week of delay costs your team roughly 10-15% in missed pipeline. Let me show you the math.",
            evidence="Our data across 200+ implementations shows decision speed correlates 0.7 with ultimate deal satisfaction.",
        ))
        return attacks

    # === Framework: Calibrated Absence (Stuart Diamond) ===

    def _generate_calibrated_absences(self, ctx: DealContext) -> list[CalibratedAbsence]:
        return [
            CalibratedAbsence(
                trigger="After asking for commitment: 'Can we move forward with this?'",
                silence_duration_seconds=5,
                expected_effect="Prospect fills the silence with their own reasoning, often revealing true objections or giving themselves reasons to buy",
                fallback="If they deflect, pivot to Value=Progress frame",
            ),
            CalibratedAbsence(
                trigger="After they say 'It's too expensive'",
                silence_duration_seconds=4,
                expected_effect="They either justify the statement (revealing budget constraints) or self-correct and qualify it",
                fallback="Mirror Attack: 'I hear you — let's look at what not doing this costs'",
            ),
            CalibratedAbsence(
                trigger="After presenting a Give-Get pair",
                silence_duration_seconds=3,
                expected_effect="They mentally weigh the exchange and often add more value to their side of the trade",
                fallback="Return to Value=Progress frame to reinforce the gap",
            ),
        ]

    # === Script Builder ===

    def _build_script(self, ctx: DealContext, give_gets: list[GiveGetPair],
                      value_frames: list[ValueProgressFrame],
                      mirror_attacks: list[MirrorAttack],
                      absences: list[CalibratedAbsence]) -> str:
        lines = []
        lines.append(f"--- NEGOTIATION SCRIPT: {ctx.prospect_name} ({ctx.company}) ---")
        lines.append(f"Stage: {ctx.current_stage} | Value: ${ctx.deal_value:,.0f}")
        lines.append("")

        lines.append("PHASE 1: OPENING (Anchor with Value=Progress)")
        if value_frames:
            vf = value_frames[0]
            lines.append(f"  'I know {ctx.prospect_name}, your team is focused on {vf.metric}. "
                        f"Right now you're at [{vf.current_state}] and you need to get to "
                        f"[{vf.desired_state}]. The gap is {vf.progress_gap}.'")
        lines.append("")

        lines.append("PHASE 2: BUILD (Give-Get pairs)")
        for gg in give_gets:
            lines.append(f"  GIVE: {gg.give}")
            lines.append(f"  GET:  {gg.get}")
            lines.append(f"  WHY:  {gg.rationale}")
            lines.append("")

        lines.append("PHASE 3: HANDLE (Mirror Attacks)")
        for ma in mirror_attacks:
            lines.append(f"  THEM: {ma.their_frame}")
            lines.append(f"  YOU:  {ma.mirrored_response}")
            lines.append(f"  THEN: {ma.reframe}")
            lines.append("")

        lines.append("PHASE 4: CLOSE (Calibrated Absence + Commitment)")
        for ca in absences:
            lines.append(f"  TRIGGER: {ca.trigger}")
            lines.append(f"  SILENCE: {ca.silence_duration_seconds}s")
            lines.append(f"  EXPECT:  {ca.expected_effect}")
            lines.append(f"  FALLBACK: {ca.fallback}")
            lines.append("")

        return "\n".join(lines)

    def _recommend_approach(self, ctx: DealContext) -> str:
        if ctx.objections:
            return "Lead with Mirror Attack to disarm objections, then build Value=Progress frames"
        if ctx.competitor:
            return "Open with Value=Progress comparing against competitor, close with Give-Get"
        return "Lead with Value=Progress, insert Give-Get pairs, handle any resistance with Mirror Attack"

    def _map_stage_to_phase(self, stage: str) -> str:
        mapping = {
            "discovery": "discovery",
            "demo": "value_building",
            "evaluation": "value_building",
            "negotiation": "closing",
            "closed_won": "post_deal",
            "closed_lost": "post_deal",
        }
        return mapping.get(stage, "opening")

    async def _respond_to_objection(self, deal_id: str, data: dict) -> dict:
        objection = data.get("objection", "")
        prospect = data.get("prospect_name", "Prospect")
        ctx = DealContext(deal_id=deal_id, prospect_name=prospect,
                          prospect_title=data.get("prospect_title", ""),
                          company=data.get("company", ""),
                          objections=[objection])

        mirror = MirrorAttack(
            their_frame=objection,
            mirrored_response=f"I understand why {prospect} would raise that — it's a valid concern.",
            reframe=f"Let's look at this from the other side. What does {ctx.company} risk by not addressing this?",
            evidence="",
        )
        value = ValueProgressFrame(
            metric="Decision confidence",
            current_state=f"Uncertainty around '{objection}'",
            desired_state="Clarity and confidence to move forward",
            progress_gap="One conversation's worth of information",
        )

        return {
            "deal_id": deal_id,
            "objection": objection,
            "mirror_attack": {
                "mirrored_response": mirror.mirrored_response,
                "reframe": mirror.reframe,
            },
            "value_frame": {
                "metric": value.metric,
                "gap": value.progress_gap,
            },
        }

    async def _publish_plan(self, plan: NegotiationPlan, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.negotiation.plan.ready",
            "NegotiationPlanReady",
            {
                "deal_id": deal_id,
                "phase": plan.phase.value,
                "prospect": plan.context.prospect_name,
                "company": plan.context.company,
                "recommended_approach": plan.recommended_approach,
                "give_get_count": len(plan.give_gets),
                "value_frame_count": len(plan.value_frames),
                "mirror_attack_count": len(plan.mirror_attacks),
                "calibrated_absence_count": len(plan.calibrated_absences),
                "script": plan.script,
            },
            deal_id=deal_id,
        )

    async def _publish_move(self, move: dict, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.negotiation.move",
            "NegotiationMoveReady",
            move,
            deal_id=deal_id,
        )
