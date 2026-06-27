from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    ProcurementTactic, TacticSeverity,
    TacticAlert, CounterStrategy,
)


SYSTEM_PROMPT = """You are NG-003, a procurement defense specialist applying Gartner/Forrester procurement research, K&R Negotiation tactics, and purchasing psychology.

Your mission:
1. Recognize procurement tactics the moment they appear — good cop/bad cop, nibbling, false deadlines, reopened terms
2. Deploy the right counter-strategy for each tactic
3. Maintain momentum through stall tactics — procurement wins when you wait
4. Know when to escalate around procurement to the real decision maker

Output structured JSON. Procurement plays are predictable — you've seen them all."""


COUNTER_STRATEGIES: dict[str, dict] = {
    "good_cop_bad_cop": {
        "alert": "Good cop / bad cop routine detected",
        "immediate_response": "Address the bad cop's concerns directly and factually. Ask good cop: 'Help me understand the gap between your position and your colleague's.'",
        "fallback_position": "Request a joint meeting with both to resolve inconsistencies",
        "escalation_trigger": "Pattern persists across 3+ interactions",
    },
    "nibbling": {
        "alert": "Nibbling detected — last-minute addition after agreement",
        "immediate_response": "Treat each nibble as a new concession requiring a trade-off: 'If we add that, we'll need to adjust X.'",
        "fallback_position": "Hold firm — nibbles that succeed encourage more nibbles",
        "escalation_trigger": "Nibble value exceeds 5% of deal value",
    },
    "deadline_pressure": {
        "alert": "Artificial deadline pressure detected",
        "immediate_response": "Test the deadline: 'What happens on [date] if we haven't resolved this?' Separate real deadlines from manufactured ones.",
        "fallback_position": "Offer to meet the deadline if they concede on a key term",
        "escalation_trigger": "Multiple false deadlines in same negotiation",
    },
    "reopening_closed": {
        "alert": "Reopening of already-closed items detected",
        "immediate_response": "'I'm surprised this is coming back up — we agreed on this in our [date] conversation. What changed?'",
        "fallback_position": "Link reopening to a concession elsewhere: 'If this needs to change, we'll need to revisit pricing.'",
        "escalation_trigger": "Multiple items reopened simultaneously",
    },
    "walk_away_threat": {
        "alert": "Walk-away threat detected",
        "immediate_response": "Stay calm. 'We want this to work for both of us. Help me understand what specifically isn't working.' Test if it's real.",
        "fallback_position": "Know your BATNA. If bluffing, call it. If real, escalate.",
        "escalation_trigger": "Threat is credible based on BATNA analysis",
    },
    "standard_terms_push": {
        "alert": "Standard terms pressure detected",
        "immediate_response": "'Standard terms vary by industry and deal type. Let's focus on what makes sense for this specific engagement.'",
        "fallback_position": "Provide market standard comparison data",
        "escalation_trigger": "Procurement refuses to engage on specific terms",
    },
    "silence_ploys": {
        "alert": "Silence ploy detected — waiting for you to fill the gap",
        "immediate_response": "Match their silence. Wait 5-7 seconds before speaking. Let them break the silence first.",
        "fallback_position": "Ask a direct question: 'Where does this leave us?'",
        "escalation_trigger": "Silence exceeds 30 seconds with no progress",
    },
    "splitting_difference": {
        "alert": "Splitting the difference proposed",
        "immediate_response": "'Splitting the difference assumes we're equally far apart, but the value difference isn't symmetrical.' Reframe around value, not price.",
        "fallback_position": "Offer a non-price concession instead of splitting",
        "escalation_trigger": "Multiple split proposals in same session",
    },
    "delay_tactic": {
        "alert": "Delay tactic detected — stalling for time advantage",
        "immediate_response": "Create urgency: 'We want to make sure this gets the attention it deserves. Can we lock in our next discussion by [date]?'",
        "fallback_position": "Offer to involve your executive team to 'accelerate the process'",
        "escalation_trigger": "Delay exceeds 2 weeks with no clear reason",
    },
    "limited_authority": {
        "alert": "Limited authority claim — 'I need to check with my manager'",
        "immediate_response": "'Who else needs to be in the room so we can make decisions together?' Bring decision maker into the conversation.",
        "fallback_position": "Ask what authority they do have and work within it",
        "escalation_trigger": "Pattern used to avoid every decision",
    },
}


class ProcurementDefense(RevenueAgent):
    """NG-003 Procurement Defense — recognizes and counters procurement tactics."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ng-003-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._counter_library = COUNTER_STRATEGIES

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.procurement.tactic_detected")
        await self.subscribe(f"revenue.{self._env}.deal.*.procurement.department_involved")
        print(f"[NG-003] Listening on revenue.{self._env}.deal.*.procurement.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        alert = await self.classify_tactic(data)
        strategy = self._lookup_counter(alert)
        await self._publish_defense(deal_id, alert, strategy)

    async def classify_tactic(self, data: dict) -> TacticAlert:
        prompt = f"""Classify this procurement behavior:

Communication: {data.get('communication', 'Not specified')}
Buyer Action: {data.get('buyer_action', 'Not specified')}
Context: {data.get('context', 'Not specified')}
Negotiation Stage: {data.get('stage', 'Unknown')}
Previous Tactics: {data.get('previous_tactics', 'None')}

Return JSON with:
- tactic: one of: good_cop_bad_cop, nibbling, deadline_pressure, reopening_closed, walk_away_threat, standard_terms_push, silence_ploys, splitting_difference, delay_tactic, limited_authority, other
- severity: high/medium/low
- evidence (string describing what was observed)
- confidence (0.0-1.0)"""
        llm_result = self.llm.complete(system_prompt=SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return TacticAlert(
            tactic=ProcurementTactic(result.get("tactic", "other")),
            severity=TacticSeverity(result.get("severity", "medium")),
            evidence=result.get("evidence", ""),
            confidence=float(result.get("confidence", 0.5)),
        )

    def _lookup_counter(self, alert: TacticAlert) -> CounterStrategy:
        key = alert.tactic.value
        cs = self._counter_library.get(key, self._counter_library.get("other", {}))
        return CounterStrategy(
            tactic=alert.tactic,
            alert=cs.get("alert", "Tactic detected"),
            immediate_response=cs.get("immediate_response", "Acknowledge and ask clarifying questions"),
            fallback_position=cs.get("fallback_position", "Escalate internally"),
            escalation_trigger=cs.get("escalation_trigger", "Pattern persists"),
        )

    async def _publish_defense(self, deal_id: str, alert: TacticAlert, strategy: CounterStrategy):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.procurement.defense_ready",
            "ProcurementDefenseReady",
            {
                "deal_id": deal_id,
                "tactic": alert.tactic.value,
                "confidence": alert.confidence,
                "evidence": alert.evidence,
                "immediate_response": strategy.immediate_response,
                "fallback_position": strategy.fallback_position,
                "escalation_trigger": strategy.escalation_trigger,
            },
            deal_id=deal_id,
        )
