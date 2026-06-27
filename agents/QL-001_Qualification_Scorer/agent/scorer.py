"""QL-001 BANT/MEDDPICC Scorer — scores deals against qualification frameworks.

Uses LLM (Complex Reasoning tier) for evidence-based scoring with
rule-based fallback when LLM is unavailable.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_span_id

from .models import (
    QualificationDimension, Confidence,
    DimensionScore, BANTScore, MEDDPICCScore,
    L1Score, L2Score, L3Score, CustomerInputGating, QualificationResult,
)


class QualificationScorer(RevenueAgent):
    """Scores every opportunity against BANT and MEDDPICC frameworks."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="ql-001-v1",
            agent_version="0.1.0",
            llm_tier="complex",
            nats_servers=nats_servers,
        )
        self._env = "dev"

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.qualifying.scoring.request")
        await self.subscribe(f"revenue.{self._env}.deal.*.created")
        print(f"[QL-001] Listening for qualification requests on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"

        if event_type in ("DealCreated", "DealScoringRequested"):
            result = await self.score_deal(deal_id, envelope.data.get("transcript_text", ""),
                                           envelope.data.get("email_threads", []))
            await self._publish_result(result, deal_id)

    async def score_deal(self, deal_id: str, transcript: str = "",
                         email_threads: list[str] | None = None) -> QualificationResult:
        print(f"[QL-001] Scoring deal {deal_id}...")

        llm_result = self.llm.complete(
            system_prompt=self._scoring_system_prompt(),
            user_prompt=self._scoring_user_prompt(deal_id, transcript, email_threads or []),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                result = self._parse_llm_result(parsed, deal_id)
                print(f"[QL-001] LLM scoring: BANT={result.bant.composite:.2f} "
                      f"MEDDPICC={result.meddpicc.composite:.2f} DQI={result.deal_quality_index:.2f}")
                return result

        return self._rule_based_scoring(deal_id, transcript)

    async def _publish_result(self, result: QualificationResult, deal_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.qualifying.scored",
            "DealScored",
            {
                "deal_id": deal_id,
                "bant_score": result.bant.composite if result.bant else None,
                "meddpicc_score": result.meddpicc.composite if result.meddpicc else None,
                "deal_quality_index": result.deal_quality_index,
                "disqualify": result.disqualify,
                "disqualify_reason": result.disqualify_reason,
                "gaps": result.gaps,
                "next_questions": result.next_questions,
            },
            deal_id=deal_id,
        )
        if result.meddpicc:
            await self.publish(
                f"revenue.{self._env}.deal.{deal_id}.qualifying.meddpicc",
                "DealMEDDPICCScored",
                {
                    "deal_id": deal_id,
                    "dimensions": {
                        d.value: getattr(result.meddpicc, d.value, DimensionScore(d, 0.0, Confidence.UNKNOWN)).score
                        for d in [
                            QualificationDimension.METRICS, QualificationDimension.ECONOMIC_BUYER,
                            QualificationDimension.DECISION_CRITERIA, QualificationDimension.PROCESS,
                            QualificationDimension.IMPLICIT_PAIN, QualificationDimension.CHAMPION,
                            QualificationDimension.COMPETITION,
                        ]
                    },
                    "composite": result.meddpicc.composite,
                },
                deal_id=deal_id,
            )

        if result.disqualify:
            await self.publish(
                f"revenue.{self._env}.deal.{deal_id}.qualifying.disqualified",
                "DealDisqualified",
                {"deal_id": deal_id, "reason": result.disqualify_reason},
                deal_id=deal_id,
            )

    #  LLM prompts

    def _scoring_system_prompt(self) -> str:
        return """You are a senior sales qualification analyst. Score every deal against
BANT (Budget, Authority, Need, Timeline), MEDDPICC (Metrics, Economic Buyer,
Decision Criteria, Process, Implicit Pain, Champion, Competition),
AND Skip Miller's L1-L2-L3 framework with Paul Butterfield's Customer Input Gating.

=== BANT + MEDDPICC (standard scoring) ===
For each dimension, provide:
- score: 0.0 to 1.0
- confidence: confirmed, high, medium, low, unknown
- evidence: specific quotes or data points supporting the score
- gaps: information still missing

=== L1-L2-L3 (Skip Miller) — Three-level qualification ===

L1: Problem Qualification (threshold: 60/120)
  - pain_clarity: 0.0-1.0 — Have they clearly stated the problem?
  - impact: 0.0-1.0 — How significant is the impact on their business?
  - urgency_trend: 0.0-1.0 — Is the pain getting worse?
  Composite = (pain_clarity × 20) + (impact × 20) + (urgency_trend × 20)

L2: Solution Qualification (threshold: 100/210)
  - fit_clarity: 0.0-1.0 — Have they defined what a solution looks like?
  - authority_access: 0.0-1.0 — Can we reach the economic buyer?
  - evaluation_readiness: 0.0-1.0 — Are they actively evaluating options?
  Composite = (fit_clarity × 30) + (authority_access × 30) + (evaluation_readiness × 40)

L3: Buying Qualification (threshold: 200/400)
  - budget: 0.0-1.0 — Is there a funded budget?
  - timeline: 0.0-1.0 — Is there a defined buying timeline?
  - decision_process: 0.0-1.0 — Do we understand the decision process?
  - cost_of_inaction: 0.0-1.0 — Have they quantified what delay costs?
  Composite = (budget × 50) + (timeline × 50) + (decision_process × 50) + (cost_of_inaction × 50)

=== Customer Input Gating (Paul Butterfield) ===
Before trusting any score, verify input quality:
  - problem_in_own_words: Has the prospect described the problem in THEIR words (not parroting us)?
  - participatory_discovery: Has the prospect actively participated in discovery (not just received info)?
  - questions_asked: Has the prospect asked questions about our solution (not just answered ours)?
  - time_invested: Has the prospect invested time in evaluation (meetings, demos, trials)?

If input_gating gates are closed, scores may be artificially inflated.
Each closed gate reduces effective score by 25%.

=== Value = Progress (Andy Paul) ===
Qualification isn't about fit — it's about velocity of progress toward the desired outcome.
Consider: How quickly can we move them from current state to desired state?

Output JSON only:
{
  "bant": { "budget": {...}, "authority": {...}, "need": {...}, "timeline": {...} },
  "meddpicc": { "metrics": {...}, "economic_buyer": {...}, "decision_criteria": {...},
                "process": {...}, "implicit_pain": {...}, "champion": {...}, "competition": {...} },
  "miller_l1": { "pain_clarity": 0.5, "impact": 0.6, "urgency_trend": 0.3, "evidence": [...], "gaps": [...] },
  "miller_l2": { "fit_clarity": 0.4, "authority_access": 0.7, "evaluation_readiness": 0.5, "evidence": [...], "gaps": [...] },
  "miller_l3": { "budget": 0.8, "timeline": 0.6, "decision_process": 0.5, "cost_of_inaction": 0.3, "evidence": [...], "gaps": [...] },
  "input_gating": { "problem_in_own_words": true, "participatory_discovery": false, "questions_asked": true, "time_invested": false },
  "deal_quality_index": 0.0-1.0,
  "disqualify": false,
  "disqualify_reason": "",
  "gaps": ["..."],
  "next_questions": ["..."]
}"""

    def _scoring_user_prompt(self, deal_id: str, transcript: str, emails: list[str]) -> str:
        return f"""Deal ID: {deal_id}
Transcript: {transcript[:2000] if transcript else "Not available"}
Email Threads: {len(emails)} threads available

Score this deal against BANT, MEDDPICC, Skip Miller L1-L2-L3, and Paul Butterfield Input Gating.

L1 thresholds: >= 60 = problem exists
L2 thresholds: >= 100 = solution fit confirmed
L3 thresholds: >= 200 = buying-ready

If insufficient evidence, tag as low confidence. Verify Input Gating before trusting scores."""

    #  Parsing

    def _parse_llm_result(self, data: dict, deal_id: str) -> QualificationResult:
        bant_raw = data.get("bant", {})
        med_raw = data.get("meddpicc", {})
        l1_raw = data.get("miller_l1", {})
        l2_raw = data.get("miller_l2", {})
        l3_raw = data.get("miller_l3", {})
        ig_raw = data.get("input_gating", {})

        bant = BANTScore(
            budget=self._parse_dim(bant_raw.get("budget", {}), QualificationDimension.BUDGET),
            authority=self._parse_dim(bant_raw.get("authority", {}), QualificationDimension.AUTHORITY),
            need=self._parse_dim(bant_raw.get("need", {}), QualificationDimension.NEED),
            timeline=self._parse_dim(bant_raw.get("timeline", {}), QualificationDimension.TIMELINE),
        )
        bant.compute()

        med = MEDDPICCScore(
            metrics=self._parse_dim(med_raw.get("metrics", {}), QualificationDimension.METRICS),
            economic_buyer=self._parse_dim(med_raw.get("economic_buyer", {}), QualificationDimension.ECONOMIC_BUYER),
            decision_criteria=self._parse_dim(med_raw.get("decision_criteria", {}), QualificationDimension.DECISION_CRITERIA),
            process=self._parse_dim(med_raw.get("process", {}), QualificationDimension.PROCESS),
            implicit_pain=self._parse_dim(med_raw.get("implicit_pain", {}), QualificationDimension.IMPLICIT_PAIN),
            champion=self._parse_dim(med_raw.get("champion", {}), QualificationDimension.CHAMPION),
            competition=self._parse_dim(med_raw.get("competition", {}), QualificationDimension.COMPETITION),
        )
        med.compute()

        l1 = L1Score(
            pain_clarity=float(l1_raw.get("pain_clarity", 0.0)),
            impact=float(l1_raw.get("impact", 0.0)),
            urgency_trend=float(l1_raw.get("urgency_trend", 0.0)),
            evidence=l1_raw.get("evidence", []),
            gaps=l1_raw.get("gaps", []),
        )
        l1.compute()

        l2 = L2Score(
            fit_clarity=float(l2_raw.get("fit_clarity", 0.0)),
            authority_access=float(l2_raw.get("authority_access", 0.0)),
            evaluation_readiness=float(l2_raw.get("evaluation_readiness", 0.0)),
            evidence=l2_raw.get("evidence", []),
            gaps=l2_raw.get("gaps", []),
        )
        l2.compute()

        l3 = L3Score(
            budget=float(l3_raw.get("budget", 0.0)),
            timeline=float(l3_raw.get("timeline", 0.0)),
            decision_process=float(l3_raw.get("decision_process", 0.0)),
            cost_of_inaction=float(l3_raw.get("cost_of_inaction", 0.0)),
            evidence=l3_raw.get("evidence", []),
            gaps=l3_raw.get("gaps", []),
        )
        l3.compute()

        input_gating = CustomerInputGating(
            problem_in_own_words=ig_raw.get("problem_in_own_words", False),
            participatory_discovery=ig_raw.get("participatory_discovery", False),
            questions_asked=ig_raw.get("questions_asked", False),
            time_invested=ig_raw.get("time_invested", False),
        )

        dqi = data.get("deal_quality_index", (bant.composite + med.composite) / 2)
        penalty = input_gating.penalty
        adjusted_dqi = dqi * (1.0 - penalty)

        return QualificationResult(
            deal_id=deal_id,
            bant=bant,
            meddpicc=med,
            miller_l1=l1,
            miller_l2=l2,
            miller_l3=l3,
            input_gating=input_gating,
            deal_quality_index=adjusted_dqi,
            disqualify=data.get("disqualify", False),
            disqualify_reason=data.get("disqualify_reason", ""),
            disqualify_confidence=Confidence.MEDIUM,
            gaps=data.get("gaps", []),
            next_questions=data.get("next_questions", []),
            scored_at=datetime.now(timezone.utc).isoformat(),
        )

    def _parse_dim(self, raw: dict, dim: QualificationDimension) -> DimensionScore:
        return DimensionScore(
            dimension=dim,
            score=min(1.0, max(0.0, float(raw.get("score", 0.5)))),
            confidence=Confidence(raw.get("confidence", "unknown")),
            evidence=raw.get("evidence", []),
            gaps=raw.get("gaps", []),
        )

    def _rule_based_scoring(self, deal_id: str, transcript: str) -> QualificationResult:
        """Fallback when LLM unavailable — simple keyword-based scoring."""
        text = transcript.lower()

        def kw_score(positive: list[str], negative: list[str]) -> tuple[float, list[str], list[str]]:
            hits = [k for k in positive if k in text]
            misses = [k for k in negative if k in text]
            score = len(hits) / (len(positive) or 1)
            return score, hits, misses

        budget_val, budget_ev, budget_gaps = kw_score(
            ["budget", "spend", "cost", "price", "investment", "pricing"],
            ["no budget", "expensive", "too much"])

        return QualificationResult(
            deal_id=deal_id,
            bant=BANTScore(
                budget=DimensionScore(QualificationDimension.BUDGET, budget_val, Confidence.LOW, budget_ev, budget_gaps),
                authority=DimensionScore(QualificationDimension.AUTHORITY, 0.3, Confidence.LOW, [], ["No authority signals"]),
                need=DimensionScore(QualificationDimension.NEED, 0.5, Confidence.LOW, [], ["Need not clear"]),
                timeline=DimensionScore(QualificationDimension.TIMELINE, 0.3, Confidence.LOW, [], ["No timeline"]),
            ),
            deal_quality_index=0.3,
            gaps=["Insufficient evidence for accurate scoring"],
            next_questions=["What is your budget range?", "Who is the economic buyer?", "What is your evaluation timeline?"],
            scored_at=datetime.now(timezone.utc).isoformat(),
        )
