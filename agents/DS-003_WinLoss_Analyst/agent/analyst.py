"""DS-003 Win/Loss Analyst — Clozd/Gong root cause analysis from deal outcomes.

Analyzes closed-lost and closed-won deals using structured loss taxonomy,
pattern detection, data completeness scoring, and actionable recommendations.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_event_id

from .models import (
    LossReason, WinReason, PatternType,
    LossReasonDetail, WinLossRecord, PatternAnalysis,
    WinLossAnalysisResult, LOSS_TAXONOMY, WIN_TAXONOMY,
)


class WinLossAnalyst(RevenueAgent):
    """Analyzes closed deals for root cause and pattern detection."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ds-003-v1",
            agent_version="0.2.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._results: dict[str, WinLossAnalysisResult] = {}
        self._deal_history: list[WinLossRecord] = []

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.closed_lost.recorded")
        await self.subscribe(f"revenue.{self._env}.deal.*.closed_won.achieved")
        await self.subscribe(f"revenue.{self._env}.deal.*.winloss.analyze.requested")
        print(f"[DS-003] Listening for deal outcomes on revenue.{self._env}.deal.*.closed_*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        if "closed_lost" in event_type:
            result = await self._analyze_loss(deal_id, data)
            if result:
                self._deal_history.append(result.record)
                await self._publish_result(result, deal_id)
        elif "closed_won" in event_type:
            result = await self._analyze_win(deal_id, data)
            if result:
                self._deal_history.append(result.record)
                await self._publish_result(result, deal_id)
        elif "winloss.analyze" in event_type:
            result = await self._cross_deal_analysis(deal_id, data)
            if result:
                await self._publish_result(result, deal_id)

    async def _analyze_loss(self, deal_id: str, data: dict) -> Optional[WinLossAnalysisResult]:
        print(f"[DS-003] Analyzing closed-lost deal {deal_id}...")
        llm_result = self.llm.complete(
            system_prompt=self._winloss_system_prompt(),
            user_prompt=self._loss_user_prompt(deal_id, data),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                result = self._parse_result(parsed, deal_id, "closed_lost")
                self._results[deal_id] = result
                return result

        fallback = self._rule_loss_analysis(deal_id, data)
        self._results[deal_id] = fallback
        return fallback

    async def _analyze_win(self, deal_id: str, data: dict) -> Optional[WinLossAnalysisResult]:
        print(f"[DS-003] Analyzing closed-won deal {deal_id}...")
        record = WinLossRecord(
            deal_id=deal_id,
            outcome="won",
            value=float(data.get("deal_value", 0)),
            sales_cycle_days=int(data.get("sales_cycle_days", 0)),
            stages_passed=data.get("stages_passed", []),
            stakeholder_count=int(data.get("stakeholder_count", 0)),
            competitive_process=bool(data.get("competitive", False)),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        try:
            wr = WinReason(data.get("win_reason", "other"))
        except ValueError:
            wr = WinReason.OTHER

        return WinLossAnalysisResult(
            deal_id=deal_id,
            record=record,
            recommendations=self._generate_win_recs(data, wr),
            data_completeness=self._data_completeness(data),
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    async def _cross_deal_analysis(self, deal_id: str, data: dict) -> WinLossAnalysisResult:
        print(f"[DS-003] Cross-deal pattern analysis for {deal_id}...")
        history = list(self._deal_history)
        if not history:
            return WinLossAnalysisResult(
                deal_id=deal_id,
                record=WinLossRecord(deal_id=deal_id, outcome="unknown"),
                recommendations=["Insufficient deal history for pattern analysis"],
                analyzed_at=datetime.now(timezone.utc).isoformat(),
            )

        patterns = self._detect_patterns(history)
        recs = [p.recommendation for p in patterns if p.recommendation]

        return WinLossAnalysisResult(
            deal_id=deal_id,
            record=WinLossRecord(deal_id=deal_id, outcome="cross_deal"),
            patterns=patterns,
            recommendations=recs,
            data_completeness=1.0,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    #  Pattern Detection

    def _detect_patterns(self, history: list[WinLossRecord]) -> list[PatternAnalysis]:
        patterns = []

        loss_records = [r for r in history if r.outcome == "closed_lost" and r.loss_details]

        if loss_records:
            # Price sensitivity pattern
            price_losses = [r for r in loss_records if r.loss_details.primary == LossReason.PRICE]
            if len(price_losses) >= 2:
                patterns.append(PatternAnalysis(
                    pattern_type=PatternType.PRICE_SENSITIVITY,
                    description=f"Price is the primary loss reason in {len(price_losses)}/{len(loss_records)} lost deals",
                    frequency=len(price_losses),
                    avg_impact=sum(r.value for r in price_losses) / len(price_losses),
                    recommendation="Review pricing strategy: consider value-based packaging or tiered pricing",
                    sample_deals=[r.deal_id for r in price_losses[:3]],
                ))

            # Process flaw pattern
            process_losses = [r for r in loss_records if r.loss_details.primary == LossReason.PROCESS]
            if len(process_losses) >= 2:
                patterns.append(PatternAnalysis(
                    pattern_type=PatternType.PROCESS_FLAW,
                    description=f"Sales process breakdown in {len(process_losses)} deals",
                    frequency=len(process_losses),
                    avg_impact=sum(r.value for r in process_losses) / len(process_losses),
                    recommendation="Review discovery qualification rigor; consider additional training",
                    sample_deals=[r.deal_id for r in process_losses[:3]],
                ))

            # Stalled stage pattern
            stalled = [r for r in loss_records if "stalled" in r.loss_details.evidence.lower()]
            if len(stalled) >= 2:
                patterns.append(PatternAnalysis(
                    pattern_type=PatternType.STALLED_STAGE,
                    description=f"{len(stalled)} deals stalled in later stages",
                    frequency=len(stalled),
                    avg_impact=sum(r.value for r in stalled) / len(stalled),
                    recommendation="Review late-stage engagement playbook: add executive sponsors earlier",
                    sample_deals=[r.deal_id for r in stalled[:3]],
                ))

        return patterns

    def _generate_win_recs(self, data: dict, win_reason: WinReason) -> list[str]:
        base = ["Document win story for competitive reference"]
        if win_reason == WinReason.EXECUTIVE_PULL:
            base.append("Maintain executive relationship for future deal sponsorship")
        if win_reason == WinReason.CHAMPION:
            base.append("Nurture champion relationship for referrals and case study")
        if win_reason == WinReason.PRICE_VALUE:
            base.append("Capture value justification narrative for similar deals")
        return base

    def _data_completeness(self, data: dict) -> float:
        fields = ["deal_value", "sales_cycle_days", "stages_passed",
                   "stakeholder_count", "win_reason"]
        filled = sum(1 for f in fields if data.get(f))
        return filled / len(fields)

    #  LLM Prompts

    def _winloss_system_prompt(self) -> str:
        return """You are a win/loss analysis specialist trained in Clozd methodology.

Analyze closed-lost deals to determine root cause using structured taxonomy.

=== LOSS REASONS ===
- price: Cost exceeded value perception or budget constraints
- product: Missing features, integration issues, capability gaps
- relationship: No champion, poor rapport, trust deficit
- process: Sales process breakdown, poor discovery, misqualification
- no_decision: Evaluation paralysis, status quo maintained, stalled
- competitor: Specific competitive loss with identified rival
- timing: Budget cycle, deprioritized, bad timing
- vendor_risk: Security, compliance, financial viability concerns
- internal_politics: Stakeholder conflict, reorg, priority shift
- other: Unique or uncategorized reason

=== PREVENTABILITY SCORE ===
Score 0.0-1.0 how preventable this loss was:
- 0.0: Unavoidable (company bankruptcy, reorg, product doesn't exist)
- 0.5: Partially preventable (different approach could have helped)
- 1.0: Fully preventable (process failure, relationship neglect)

=== CLOZD PRINCIPLES ===
1. The buyer's perception IS reality — analyze from their frame
2. Loss reasons are rarely singular — look for contributing factors
3. "No decision" is often a decision for the status quo
4. Price objection usually masks value perception failure

Output JSON:
{
  "loss_analysis": {
    "primary_reason": "price",
    "contributing_reasons": ["product", "timing"],
    "description": "Buyer felt pricing was above market despite product fit",
    "evidence": "Competitive eval showed lower-priced alternative meeting core needs",
    "preventability": 0.6
  },
  "recommendations": [
    "Develop competitive battle card for price objections",
    "Consider tiered pricing for SMB segment"
  ]
}"""

    def _loss_user_prompt(self, deal_id: str, data: dict) -> str:
        return f"""Deal: {deal_id}
Value: ${data.get('deal_value', 0):,.0f}
Cycle Days: {data.get('sales_cycle_days', 'N/A')}
Stakeholders: {data.get('stakeholder_count', 'N/A')}
Stages Passed: {data.get('stages_passed', [])}
Competitive: {'Yes' if data.get('competitive') else 'No'}
Notes: {data.get('notes', 'N/A')}

Analyze this closed-lost deal using Clozd methodology.
Determine primary loss reason, contributing factors, and preventability.
Return JSON only."""

    #  Parsing

    def _parse_result(self, data: dict, deal_id: str, outcome: str) -> WinLossAnalysisResult:
        analysis = data.get("loss_analysis", {})
        try:
            primary = LossReason(analysis.get("primary_reason", "other"))
        except ValueError:
            primary = LossReason.OTHER

        contributing = []
        for r in analysis.get("contributing_reasons", []):
            try:
                contributing.append(LossReason(r))
            except ValueError:
                pass

        detail = LossReasonDetail(
            primary=primary,
            contributing=contributing,
            description=analysis.get("description", ""),
            evidence=analysis.get("evidence", ""),
            preventability=min(1.0, max(0.0, float(analysis.get("preventability", 0.5)))),
        )

        record = WinLossRecord(
            deal_id=deal_id,
            outcome=outcome,
            value=float(data.get("deal_value", 0)),
            sales_cycle_days=int(data.get("sales_cycle_days", 0)),
            loss_details=detail,
            stages_passed=data.get("stages_passed", []),
            stakeholder_count=int(data.get("stakeholder_count", 0)),
            competitive_process=bool(data.get("competitive", False)),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        patterns = self._detect_patterns(self._deal_history + [record])

        return WinLossAnalysisResult(
            deal_id=deal_id,
            record=record,
            patterns=patterns,
            recommendations=analysis.get("recommendations", []),
            data_completeness=self._data_completeness(data),
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    def _rule_loss_analysis(self, deal_id: str, data: dict) -> WinLossAnalysisResult:
        notes = (data.get("notes", "") or "").lower()
        text = notes + " " + str(data.get("stages_passed", []))

        if any(w in text for w in ["price", "expensive", "budget", "cost"]):
            primary = LossReason.PRICE
        elif any(w in text for w in ["competitor", "competition", "rival", "other vendor"]):
            primary = LossReason.COMPETITOR
        elif any(w in text for w in ["feature", "missing", "capability", "integration"]):
            primary = LossReason.PRODUCT
        elif any(w in text for w in ["timing", "too early", "too late", "not now"]):
            primary = LossReason.TIMING
        elif any(w in text for w in ["no decision", "stalled", "went dark", "no response"]):
            primary = LossReason.NO_DECISION
        elif any(w in text for w in ["relationship", "champion", "access"]):
            primary = LossReason.RELATIONSHIP
        else:
            primary = LossReason.OTHER

        recs_map = {
            LossReason.PRICE: "Develop ROI calculator and value-based pricing narrative",
            LossReason.PRODUCT: "Review product roadmap alignment with buyer requirements",
            LossReason.COMPETITOR: "Create competitive battle cards and differentiation playbook",
            LossReason.RELATIONSHIP: "Implement stakeholder mapping and champion development plan",
            LossReason.PROCESS: "Review qualification criteria and discovery process",
            LossReason.NO_DECISION: "Create urgency framework with cost-of-inaction calculator",
            LossReason.TIMING: "Build trigger-event monitoring for re-engagement timing",
            LossReason.VENDOR_RISK: "Prepare security/compliance package for early deal stages",
            LossReason.INTERNAL_POLITICS: "Map stakeholder influence and develop multi-thread strategy",
            LossReason.OTHER: "Conduct win/loss interview with buyer for deeper insight",
        }

        detail = LossReasonDetail(
            primary=primary,
            description=f"Rule-based classification: {LOSS_TAXONOMY.get(primary, primary.value)}",
            evidence=f"Keywords found in deal notes: '{text[:100]}'",
            preventability=0.5,
        )

        record = WinLossRecord(
            deal_id=deal_id,
            outcome="closed_lost",
            value=float(data.get("deal_value", 0)),
            sales_cycle_days=int(data.get("sales_cycle_days", 0)),
            loss_details=detail,
            stages_passed=data.get("stages_passed", []),
            stakeholder_count=int(data.get("stakeholder_count", 0)),
            competitive_process=bool(data.get("competitive", False)),
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        patterns = self._detect_patterns(self._deal_history + [record])

        return WinLossAnalysisResult(
            deal_id=deal_id,
            record=record,
            patterns=patterns,
            recommendations=[recs_map.get(primary, "Conduct win/loss interview")],
            data_completeness=self._data_completeness(data),
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    async def _publish_result(self, result: WinLossAnalysisResult, deal_id: str):
        record = result.record
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.winloss.analyzed",
            "WinLossAnalysisComplete",
            {
                "deal_id": deal_id,
                "outcome": record.outcome,
                "primary_reason": record.loss_details.primary.value if record.loss_details else "",
                "preventability": record.loss_details.preventability if record.loss_details else 0.0,
                "recommendations": result.recommendations,
                "pattern_count": len(result.patterns),
                "data_completeness": result.data_completeness,
                "analyzed_at": result.analyzed_at,
            },
            deal_id=deal_id,
        )

    async def get_aggregate_stats(self) -> dict[str, Any]:
        losses = [r for r in self._deal_history if r.outcome == "closed_lost"]
        wins = [r for r in self._deal_history if r.outcome == "won"]

        reason_dist = {}
        for r in losses:
            if r.loss_details:
                key = r.loss_details.primary.value
                reason_dist[key] = reason_dist.get(key, 0) + 1

        return {
            "total_analyzed": len(self._deal_history),
            "total_losses": len(losses),
            "total_wins": len(wins),
            "win_rate": len(wins) / len(self._deal_history) * 100 if self._deal_history else 0,
            "loss_reason_distribution": reason_dist,
            "avg_preventability": (
                sum(r.loss_details.preventability for r in losses if r.loss_details) / len(losses)
                if losses else 0
            ),
        }
