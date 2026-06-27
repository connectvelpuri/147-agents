from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    RiskSeverity, MilestoneStatus, StakeholderInfluence,
    Milestone, RiskRegisterItem, StakeholderEngagementAction,
    DealSituation, DealPlan,
)


DEAL_PLAN_SYSTEM_PROMPT = """You are DS-001, a senior deal strategist applying Miller Heiman Strategic Selling, MEDDIC, and military strategy (Sun Tzu, von Clausewitz) to create comprehensive deal plans.

For every deal plan you produce:
1. Assess the situation objectively — identify the real stakeholders, their influence, and their hidden agenda
2. Design milestone-driven execution — specific dates, owners, and completion criteria for each step
3. Build stakeholder engagement strategy — who needs what message, at what cadence, through which channel
4. Identify risks before they become blockers — rank by severity with concrete mitigation
5. Define competitive positioning — exploit strengths, neutralize weaknesses, frame landscape favorably

Output structured JSON only. Be specific and actionable — generic plans lose deals."""


class DealPlanner(RevenueAgent):
    """DS-001 Deal Planner — strategic deal planning using Miller Heiman, MEDDIC, Sun Tzu."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-001-v1",
            agent_version="0.2.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._deal_plans: dict[str, DealPlan] = {}

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.plan.requested")
        await self.subscribe(f"revenue.{self._env}.deal.*.stalled")
        await self.subscribe(f"revenue.{self._env}.deal.*.stakeholder.new")
        print(f"[DS-001] Deal Planner listening on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}
        event_type = envelope.event_type

        if "plan.requested" in event_type:
            plan = await self.create_comprehensive_deal_plan(deal_id, data)
            await self._publish_plan(plan, deal_id)
        elif "stalled" in event_type:
            recovery = await self._build_stall_recovery(deal_id, data)
            await self._publish_stall_recovery(deal_id, recovery)
        elif "stakeholder.new" in event_type:
            existing = self._deal_plans.get(deal_id)
            if existing:
                updated = await self._update_with_stakeholder(existing, data)
                await self._publish_plan(updated, deal_id)

    async def assess_deal_situation(self, data: dict) -> DealSituation:
        prompt = f"""Assess this deal situation:

Deal ID: {data.get('deal_id', 'unknown')}
Value: ${data.get('deal_value', 0):,.0f}
Buyer: {data.get('buyer_name', 'Unknown')}
Industry: {data.get('industry', 'Unknown')}
Stage: {data.get('current_stage', 'Discovery')}
Stakeholders: {json.dumps(data.get('stakeholders', []))}
Competitive: {data.get('competitive_landscape', 'Unknown')}
Timeline: {data.get('timeline', 'No timeline provided')}
Key Notes: {data.get('notes', 'None')}

Return JSON with:
- summary (2-3 sentence deal overview)
- buyer_need (what the buyer needs to achieve)
- blockers (array of known blockers)
- competitive_landscape (assessment)
- timeline_context (urgency and timeline)
- stakeholder_count (int)
- stakeholder_engagement_quality (low/medium/high)"""
        llm_result = self.llm.complete(system_prompt=DEAL_PLAN_SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return DealSituation(
            deal_id=data.get("deal_id", "unknown"),
            deal_value=float(data.get("deal_value", 0)),
            buyer_need=result.get("buyer_need", "Unknown"),
            stakeholders=data.get("stakeholders", []),
            competitive_landscape=result.get("competitive_landscape", "Unknown"),
            timeline_context=result.get("timeline_context", "Unknown"),
            blockers=result.get("blockers", []),
            summary=result.get("summary", "No assessment available"),
        )

    async def _build_milestones(self, situation: DealSituation, data: dict) -> list[Milestone]:
        prompt = f"""Design a milestone-driven deal plan for:

Deal: {situation.deal_id}
Value: ${situation.deal_value:,.0f}
Situation: {situation.summary}
Buyer Need: {situation.buyer_need}
Blockers: {', '.join(situation.blockers)}
Timeline: {situation.timeline_context}

Return JSON with milestones array (each: id, title, description, due_date, completion_criteria).
Create 4-6 specific, dated milestones covering: stakeholder engagement, capability validation, competitive positioning, negotiation prep, close."""
        llm_result = self.llm.complete(system_prompt=DEAL_PLAN_SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return [
            Milestone(
                id=m.get("id", f"ms-{i}"),
                title=m.get("title", f"Milestone {i+1}"),
                description=m.get("description", ""),
                due_date=m.get("due_date", "TBD"),
                completion_criteria=m.get("completion_criteria", ""),
            )
            for i, m in enumerate(result.get("milestones", []))
        ]

    async def _build_stakeholder_plan(self, situation: DealSituation) -> list[StakeholderEngagementAction]:
        prompt = f"""Build a stakeholder engagement plan for:

Deal: {situation.deal_id}
Summary: {situation.summary}
Blockers: {', '.join(situation.blockers)}

Return JSON with actions array (each: stakeholder_name, title, influence (high/medium/low), current_sentiment, engagement_goal, message_focus, proposed_action, cadence, notes)."""
        llm_result = self.llm.complete(system_prompt=DEAL_PLAN_SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return [
            StakeholderEngagementAction(
                stakeholder_name=a.get("stakeholder_name", f"Stakeholder {i+1}"),
                title=a.get("title", ""),
                influence=StakeholderInfluence(a.get("influence", "medium")),
                current_sentiment=a.get("current_sentiment", "neutral"),
                engagement_goal=a.get("engagement_goal", ""),
                message_focus=a.get("message_focus", ""),
                proposed_action=a.get("proposed_action", ""),
                cadence=a.get("cadence", "weekly"),
                notes=a.get("notes", ""),
            )
            for i, a in enumerate(result.get("actions", []))
        ]

    async def _identify_risks(self, situation: DealSituation) -> list[RiskRegisterItem]:
        prompt = f"""Identify risks for this deal:

Deal: {situation.deal_id}
Value: ${situation.deal_value:,.0f}
Summary: {situation.summary}
Blockers: {', '.join(situation.blockers)}
Timeline: {situation.timeline_context}

Return JSON with risks array (each: id, risk, severity (critical/high/medium/low), probability (0.0-1.0), impact, mitigation, owner)."""
        llm_result = self.llm.complete(system_prompt=DEAL_PLAN_SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return [
            RiskRegisterItem(
                id=r.get("id", f"risk-{i}"),
                risk=r.get("risk", f"Risk {i+1}"),
                severity=RiskSeverity(r.get("severity", "medium")),
                probability=float(r.get("probability", 0.5)),
                impact=r.get("impact", ""),
                mitigation=r.get("mitigation", ""),
                owner=r.get("owner", ""),
            )
            for i, r in enumerate(result.get("risks", []))
        ]

    async def create_comprehensive_deal_plan(self, deal_id: str, data: dict) -> DealPlan:
        data["deal_id"] = deal_id
        situation = await self.assess_deal_situation(data)
        milestones, stakeholder_plan, risks = await self._build_parallel(situation, data)
        competitive = await self._assess_competitive(situation, data)
        critical_path = self._derive_critical_path(milestones)
        recs = await self._generate_recommendations(situation, risks, competitive)
        plan = DealPlan(
            deal_id=deal_id,
            version="1.0",
            situation=situation,
            milestones=milestones,
            stakeholder_plan=stakeholder_plan,
            risk_register=risks,
            competitive_positioning=competitive,
            critical_path=critical_path,
            recommendations=recs,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._deal_plans[deal_id] = plan
        return plan

    async def _build_parallel(self, situation: DealSituation, data: dict) -> tuple:
        import asyncio
        ms = self._build_milestones(situation, data)
        sp = self._build_stakeholder_plan(situation)
        ri = self._identify_risks(situation)
        results = await asyncio.gather(ms, sp, ri)
        return results[0], results[1], results[2]

    async def _assess_competitive(self, situation: DealSituation, data: dict) -> str:
        prompt = f"""Assess competitive positioning for:

Deal: {situation.deal_id}
Summary: {situation.summary}
Competitive Landscape: {situation.competitive_landscape}

Return JSON with positioning: assessment of our competitive position, key differentiators, vulnerabilities, and recommended framing strategy (single paragraph)."""
        llm_result = self.llm.complete(system_prompt=DEAL_PLAN_SYSTEM_PROMPT, user_prompt=prompt)
        result = self.llm.format_json(llm_result.text) or {}
        return result.get("positioning", "No competitive assessment available.")

    async def _generate_recommendations(self, situation: DealSituation, risks: list[RiskRegisterItem], competitive: str) -> list[str]:
        recs = []
        for r in risks:
            if r.severity in (RiskSeverity.CRITICAL, RiskSeverity.HIGH):
                recs.append(f"ADDRESS: {r.risk} — {r.mitigation}")
        if situation.blockers:
            recs.append(f"RESOLVE BLOCKERS: {', '.join(situation.blockers[:3])}")
        return recs

    def _derive_critical_path(self, milestones: list[Milestone]) -> list[str]:
        sorted_ms = sorted(milestones, key=lambda m: m.due_date)
        return [m.id for m in sorted_ms[:3]]

    async def _build_stall_recovery(self, deal_id: str, data: dict) -> DealPlan:
        data["deal_id"] = deal_id
        data["deal_value"] = data.get("deal_value", 0)
        plan = await self.create_comprehensive_deal_plan(deal_id, data)
        plan.recommendations.insert(0, f"STALL RECOVERY: Deal stalled at {data.get('stall_stage', 'unknown')}. Accelerating stakeholder engagement and timeline.")
        return plan

    async def _update_with_stakeholder(self, existing: DealPlan, data: dict) -> DealPlan:
        new_stakeholder = StakeholderEngagementAction(
            stakeholder_name=data.get("name", "New Stakeholder"),
            title=data.get("title", ""),
            influence=StakeholderInfluence(data.get("influence", "medium")),
            current_sentiment=data.get("sentiment", "neutral"),
            engagement_goal="Build rapport and understand priorities",
            message_focus="Value proposition aligned to role",
            proposed_action=f"Schedule introductory meeting with {data.get('name', 'new stakeholder')}",
            cadence="weekly",
        )
        existing.stakeholder_plan.append(new_stakeholder)
        existing.version = f"{float(existing.version) + 0.1:.1f}"
        return existing

    async def _publish_plan(self, plan: DealPlan, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.plan.created",
            "DealPlanCreated",
            {
                "deal_id": plan.deal_id,
                "version": plan.version,
                "situation_summary": plan.situation.summary,
                "milestones": [
                    {"id": m.id, "title": m.title, "due_date": m.due_date, "criteria": m.completion_criteria}
                    for m in plan.milestones
                ],
                "stakeholder_count": len(plan.stakeholder_plan),
                "risk_count": len(plan.risk_register),
                "critical_path": plan.critical_path,
                "recommendations": plan.recommendations,
                "generated_at": plan.created_at,
            },
            deal_id=deal_id,
        )

    async def _publish_stall_recovery(self, deal_id: str, plan: DealPlan):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.plan.stall_recovery",
            "DealStallRecoveryPlan",
            {"deal_id": deal_id, "version": plan.version, "recommendations": plan.recommendations},
            deal_id=deal_id,
        )
