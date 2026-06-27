"""DS-001 Deal Dashboard — real-time VMF health scoring from event streams.

Aggregates sentiment, objection, commitment, qualification, and intent
event streams into a single deal health card with 8 VMF dimensions
rated Green/Yellow/Red and a weighted overall score (0-100).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    VMFRating, ForecastCategory, StakeholderAlignment,
    VMFDimension, MEDDICMetrics, Stakeholder,
    DealHealthCard, DEAL_HEALTH_WEIGHTS, DIMENSION_DEFINITIONS,
)


class DealDashboard(RevenueAgent):
    """Aggregates deal signals into real-time health dashboard."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-001-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._deal_cards: dict[str, DealHealthCard] = {}

    async def on_start(self):
        subscriptions = [
            f"revenue.{self._env}.deal.*.meeting.sentiment_timeline",
            f"revenue.{self._env}.deal.*.meeting.emotion_highlights",
            f"revenue.{self._env}.deal.*.meeting.engagement_score",
            f"revenue.{self._env}.deal.*.meeting.objection_log",
            f"revenue.{self._env}.deal.*.meeting.commitment_log",
            f"revenue.{self._env}.deal.*.qualifying.scored",
            f"revenue.{self._env}.deal.*.intent.updated",
        ]
        for sub in subscriptions:
            await self.subscribe(sub)
        keys = ", ".join(s.rsplit(".", 1)[0] for s in subscriptions)
        print(f"[DS-001] Listening on {keys}.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        event_type = envelope.event_type
        data = envelope.data or {}

        if deal_id not in self._deal_cards:
            self._deal_cards[deal_id] = DealHealthCard(
                deal_id=deal_id, overall_score=50.0,
            )

        card = self._deal_cards[deal_id]

        if "sentiment_timeline" in event_type:
            self._apply_sentiment(card, data)
        elif "objection_log" in event_type:
            self._apply_objections(card, data)
        elif "commitment_log" in event_type:
            self._apply_commitments(card, data)
        elif "qualifying.scored" in event_type:
            self._apply_qualification(card, data)
        elif "intent.updated" in event_type:
            self._apply_intent(card, data)

        self._recalculate(card)
        await self._publish_card(card, deal_id)

    #  Signal processors

    def _apply_sentiment(self, card: DealHealthCard, data: dict):
        overall = data.get("overall_sentiment", "neutral")
        for t in data.get("timelines", []):
            pid = t.get("participant_id", "unknown")
            existing = next((s for s in card.stakeholders if s.name == pid), None)
            if not existing:
                card.stakeholders.append(Stakeholder(name=pid, title=""))
            else:
                existing.sentiment = overall
                if overall == "positive":
                    existing.alignment = StakeholderAlignment.ALIGNED
                elif overall == "negative":
                    existing.alignment = StakeholderAlignment.BLOCKING

    def _apply_objections(self, card: DealHealthCard, data: dict):
        blocking = data.get("blocking_count", 0)
        total = data.get("objection_count", 0)
        addressed = data.get("addressed_count", 0)
        if blocking > 0:
            factor = f"{blocking} blocking objection(s) unaddressed"
            if factor not in card.risk_factors:
                card.risk_factors.append(factor)
        if addressed < total:
            card.risk_factors.append(f"{total - addressed} objection(s) not addressed")

    def _apply_commitments(self, card: DealHealthCard, data: dict):
        buyer_c = data.get("buyer_commitments", 0)
        seller_c = data.get("seller_commitments", 0)
        no_commit = data.get("no_commitments", False)
        if no_commit:
            card.risk_factors.append("No commitments made in last meeting — deal may be stalling")
        if buyer_c > 0 and "Buyer commitments increasing" not in str(card.recommendations):
            card.recommendations.append("Buyer commitments increasing — maintain momentum")

    def _apply_qualification(self, card: DealHealthCard, data: dict):
        score = data.get("score", 0)
        gates_passed = data.get("gates_passed", 0)
        total_gates = data.get("total_gates", 1)
        if gates_passed < total_gates:
            card.risk_factors.append(f"Qualification gate incomplete ({gates_passed}/{total_gates})")

    def _apply_intent(self, card: DealHealthCard, data: dict):
        readiness = data.get("readiness_level", "cold")
        if readiness in ("active", "considering"):
            for dim in card.dimensions:
                if dim.name == "timeline_urgency" and dim.rating != VMFRating.GREEN:
                    dim.rating = VMFRating.GREEN
                    dim.score = 1.0
                    dim.evidence = "Buyer intent signals indicate active consideration"

    #  VMF recalculation

    def _recalculate(self, card: DealHealthCard):
        dims = self._score_dimensions(card)
        weighted = sum(
            d.score * DEAL_HEALTH_WEIGHTS.get(d.name, 0.125)
            for d in dims
        )
        card.dimensions = dims
        card.overall_score = round(weighted * 100.0, 1)
        card.meddic = self._score_meddic(card)
        card.forecast_category = self._forecast_category(card)
        card.recommendations = self._generate_recommendations(card)
        card.generated_at = datetime.now(timezone.utc).isoformat()

    def _score_dimensions(self, card: DealHealthCard) -> list[VMFDimension]:
        now = datetime.now(timezone.utc).isoformat()
        dims = []

        stakeholder_count = len(card.stakeholders)
        has_negative_sentiment = any(
            s.alignment == StakeholderAlignment.BLOCKING for s in card.stakeholders
        )
        positive_stakeholders = sum(
            1 for s in card.stakeholders if s.alignment == StakeholderAlignment.ALIGNED
        )
        has_commitments = not any(
            "No commitments" in r for r in card.risk_factors
        )
        has_blocking_objections = any(
            "blocking objection" in r for r in card.risk_factors
        )
        has_timeline_risk = any("timeline" in r.lower() for r in card.risk_factors)
        has_gate_risk = any("gate" in r.lower() for r in card.risk_factors)

        def _rate(
            green_if: bool,
            yellow_if: bool,
            green_evidence: str,
            yellow_evidence: str,
            red_evidence: str,
        ) -> tuple[VMFRating, float, str]:
            if green_if:
                return VMFRating.GREEN, 1.0, green_evidence
            if yellow_if:
                return VMFRating.YELLOW, 0.5, yellow_evidence
            return VMFRating.RED, 0.0, red_evidence

        # 1. Economic Buyer
        eb_rating, eb_score, eb_ev = _rate(
            green_if=stakeholder_count >= 2 and any(s.title for s in card.stakeholders),
            yellow_if=stakeholder_count >= 1,
            green_evidence="Multiple titled stakeholders engaged",
            yellow_evidence="Stakeholder identified but title/authority unclear",
            red_evidence="No economic buyer identified",
        )
        dims.append(VMFDimension("economic_buyer", eb_rating, eb_score, eb_ev, now))

        # 2. Negative Consequences
        nc_rating, nc_score, nc_ev = _rate(
            green_if=has_negative_sentiment or has_timeline_risk,
            yellow_if=has_commitments,
            green_evidence="Negative sentiment or timeline risk indicates awareness of consequences",
            yellow_evidence="Commitments being made suggest engagement with change need",
            red_evidence="No evidence of dissatisfaction with status quo",
        )
        dims.append(VMFDimension("negative_consequences", nc_rating, nc_score, nc_ev, now))

        # 3. PBO Clarity
        pbo_rating, pbo_score, pbo_ev = _rate(
            green_if=stakeholder_count >= 2 and positive_stakeholders >= 1,
            yellow_if=stakeholder_count >= 1,
            green_evidence="Multiple stakeholders engaged with positive sentiment — outcomes being defined",
            yellow_evidence="Deal has engagement but PBO not yet confirmed",
            red_evidence="No stakeholder engagement to assess PBO clarity",
        )
        dims.append(VMFDimension("pbo_clarity", pbo_rating, pbo_score, pbo_ev, now))

        # 4. Required Capabilities
        rc_rating, rc_score, rc_ev = _rate(
            green_if=has_commitments and not has_blocking_objections,
            yellow_if=has_commitments,
            green_evidence="Commitments flowing and no blocking objections — capabilities validated",
            yellow_evidence="Commitments exist but capabilities may not be fully validated",
            red_evidence="No commitments or validated requirements",
        )
        dims.append(VMFDimension("required_capabilities", rc_rating, rc_score, rc_ev, now))

        # 5. Decision Process
        dp_rating, dp_score, dp_ev = _rate(
            green_if=stakeholder_count >= 3 and positive_stakeholders >= 2,
            yellow_if=stakeholder_count >= 2,
            green_evidence="Multiple stakeholders with positive alignment — process visibility",
            yellow_evidence="Some stakeholders known but process not fully mapped",
            red_evidence="Decision process opaque — single-threaded",
        )
        dims.append(VMFDimension("decision_process", dp_rating, dp_score, dp_ev, now))

        # 6. Stakeholder Consensus
        sc_rating, sc_score, sc_ev = _rate(
            green_if=positive_stakeholders >= 2 and not has_negative_sentiment,
            yellow_if=positive_stakeholders >= 1 or stakeholder_count >= 2,
            green_evidence="Strong positive alignment across multiple stakeholders",
            yellow_evidence="Some positive engagement but not universal",
            red_evidence="Single stakeholder or negative sentiment detected",
        )
        dims.append(VMFDimension("stakeholder_consensus", sc_rating, sc_score, sc_ev, now))

        # 7. Timeline Urgency
        tu_rating, tu_score, tu_ev = _rate(
            green_if=has_timeline_risk or not has_gate_risk,
            yellow_if=has_commitments,
            green_evidence="Timeline awareness present or qualification complete",
            yellow_evidence="Commitments suggest forward motion but no explicit timeline",
            red_evidence="No timeline or urgency indicators",
        )
        dims.append(VMFDimension("timeline_urgency", tu_rating, tu_score, tu_ev, now))

        # 8. Competitive Position
        cp_rating, cp_score, cp_ev = _rate(
            green_if=positive_stakeholders > stakeholder_count / 2 and not has_blocking_objections,
            yellow_if=positive_stakeholders >= 1,
            green_evidence="Strong positive sentiment across majority of stakeholders",
            yellow_evidence="Some positive signal but competitive position unclear",
            red_evidence="No positive signals — competitive vulnerability",
        )
        dims.append(VMFDimension("competitive_position", cp_rating, cp_score, cp_ev, now))

        return dims

    def _score_meddic(self, card: DealHealthCard) -> MEDDICMetrics:
        stakeholder_names = [s.name for s in card.stakeholders if s.name]
        titled = sum(1 for s in card.stakeholders if s.title)
        return MEDDICMetrics(
            metrics_identified=titled,
            economic_buyer_engaged=any(
                "economic" in d.evidence.lower() and d.rating == VMFRating.GREEN
                for d in card.dimensions
            ),
            decision_criteria_clear=any(
                d.name == "pbo_clarity" and d.rating == VMFRating.GREEN
                for d in card.dimensions
            ),
            decision_process_mapped=any(
                d.name == "decision_process" and d.rating in (VMFRating.GREEN, VMFRating.YELLOW)
                for d in card.dimensions
            ),
            identified_pain_confirmed=any(
                d.name == "negative_consequences" and d.rating == VMFRating.GREEN
                for d in card.dimensions
            ),
            champion_confirmed=any(
                s.alignment == StakeholderAlignment.ALIGNED
                for s in card.stakeholders
            ),
        )

    def _forecast_category(self, card: DealHealthCard) -> ForecastCategory:
        score = card.overall_score
        if score >= 80:
            return ForecastCategory.COMMITTED
        if score >= 65:
            return ForecastCategory.BEST_CASE
        if score >= 40:
            return ForecastCategory.PIPELINE
        return ForecastCategory.UPSIDE

    def _generate_recommendations(self, card: DealHealthCard) -> list[str]:
        recs = []
        for dim in card.dimensions:
            if dim.rating == VMFRating.RED:
                recs.append(f"URGENT: {DIMENSION_DEFINITIONS_LOOKUP.get(dim.name, {}).get('label', dim.name)} — {dim.evidence}")
        for dim in card.dimensions:
            if dim.rating == VMFRating.YELLOW:
                recs.append(f"IMPROVE: {DIMENSION_DEFINITIONS_LOOKUP.get(dim.name, {}).get('label', dim.name)} — {dim.evidence}")
        if not card.meddic.economic_buyer_engaged:
            recs.append("URGENT: Identify and engage economic buyer")
        if not card.meddic.champion_confirmed:
            recs.append("IMPROVE: Develop internal champion")
        return recs

    #  Publishing

    async def _publish_card(self, card: DealHealthCard, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.dashboard.health_updated",
            "DealHealthUpdated",
            {
                "deal_id": deal_id,
                "overall_score": card.overall_score,
                "forecast_category": card.forecast_category.value,
                "dimensions": [
                    {"name": d.name, "rating": d.rating.value, "score": d.score, "evidence": d.evidence}
                    for d in card.dimensions
                ],
                "stakeholders": [
                    {"name": s.name, "title": s.title, "sentiment": s.sentiment,
                     "alignment": s.alignment.value, "influence": s.influence_level}
                    for s in card.stakeholders
                ],
                "meddic": {
                    "economic_buyer_engaged": card.meddic.economic_buyer_engaged,
                    "decision_criteria_clear": card.meddic.decision_criteria_clear,
                    "decision_process_mapped": card.meddic.decision_process_mapped,
                    "champion_confirmed": card.meddic.champion_confirmed,
                },
                "risk_factors": card.risk_factors,
                "recommendations": card.recommendations,
                "generated_at": card.generated_at,
            },
            deal_id=deal_id,
        )


DIMENSION_DEFINITIONS_LOOKUP: dict[str, dict] = {
    d["id"]: d for d in DIMENSION_DEFINITIONS
}
