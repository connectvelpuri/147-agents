"""Intelligence engine — LLM-powered analysis brain.

Transforms collected data into strategic intelligence through
three analytical layers: Descriptive → Diagnostic → Predictive.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Optional

from .models import (
    AccountRequest, AccountIntelligenceReport, ResearchDepth,
    FirmographicData, FinancialData, TechnologyStack,
    OrganizationalChart, OrganizationalNode, StrategicInitiative,
    BuyingSignal, TriggerEvent, CompetitorPresence, RiskFactor,
    EngagementRecommendation, ConsumerSection, DataGap,
    Confidence, FinancialTrend, SignalType, TriggerType, RiskType,
    VerifiedClaim,
)


class IntelligenceEngine:
    def __init__(self):
        self._client = None
        self._init_client()

    def _init_client(self):
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        provider = os.getenv("LLM_PROVIDER", "openrouter")

        if provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
            import anthropic
            self._client = anthropic.Anthropic(api_key=api_key)
            self._provider = "anthropic"
            self._model = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-20250514")
        else:
            import openai
            self._client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            self._provider = "openrouter"
            self._model = os.getenv("OPENROUTER_MODEL", "openrouter/auto")

    def analyze(self, request: AccountRequest, claims: list[VerifiedClaim]) -> AccountIntelligenceReport:
        report = AccountIntelligenceReport(
            account_id=request.account_id,
            account_name=request.account_name,
            research_depth=request.depth,
        )

        report.firmographic = self._analyze_firmographic(claims)
        report.financial_health = self._analyze_financial(claims)
        report.technology_stack = self._analyze_technographic(claims)
        report = self._llm_analysis_pass(report, request)

        return report

    def _analyze_firmographic(self, claims: list[VerifiedClaim]) -> FirmographicData:
        data = FirmographicData()
        for claim in claims:
            if claim.domain == "firmographic":
                if claim.key == "revenue":
                    data.revenue = claim
                elif claim.key == "employees":
                    data.employees = claim
                elif claim.key == "industry":
                    data.industry.append(claim)
        return data

    def _analyze_financial(self, claims: list[VerifiedClaim]) -> FinancialData:
        data = FinancialData()
        for claim in claims:
            if claim.domain == "financial":
                if claim.key == "sec_data_available":
                    data.confidence = Confidence.HIGH if claim.value else Confidence.LOW
        return data

    def _analyze_technographic(self, claims: list[VerifiedClaim]) -> TechnologyStack:
        stack = TechnologyStack()
        for claim in claims:
            if claim.domain == "technographic" and claim.key == "technologies":
                stack.detection_confidence = claim.confidence
                stack.detection_method = "builtwith"
        return stack

    def _llm_analysis_pass(self, report: AccountIntelligenceReport, request: AccountRequest) -> AccountIntelligenceReport:
        prompt = f"""You are the intelligence analysis engine for RevenueOS Account Research Agent AI-001.

Target Account: {report.account_name}
Research Depth: {request.depth.value}

Collected Intelligence:
{firmographic_section(report)}
{financial_section(report)}
{technographic_section(report)}

Perform three analysis layers:

1. DESCRIPTIVE: Summarize the account's current state — who they are, what they do, their market position.

2. DIAGNOSTIC: Identify strategic initiatives, pain points, buying signals, and organizational dynamics.
   - What problems are their job postings trying to solve?
   - What do their recent news/events suggest about priorities?
   - What keeps their executives up at night based on available data?

3. PREDICTIVE: Forecast likely next moves, risks, and engagement recommendations.
   - What is their likely next strategic initiative?
   - What risk factors should we be aware of?
   - Which persona should we approach first and why?
   - What value proposition would resonate?
   - Estimated win probability and deal size range.

Respond as JSON:
{{
  "account_summary": "...",
  "strategic_initiatives": [
    {{"initiative": "...", "evidence": ["..."], "confidence": "high|medium|low", "implication_for_us": "..."}}
  ],
  "pain_points_inferred": ["...", "..."],
  "buying_signals": [
    {{"signal_type": "role_change|funding|tech_evaluation|...", "confidence": "high|medium|low", "description": "...", "recommended_action": "..."}}
  ],
  "key_personas": [
    {{"name": "...", "title": "...", "role_in_decision": "decision_maker|influencer|champion|gatekeeper", "recommended_approach": "..."}}
  ],
  "risk_factors": [
    {{"risk_type": "regulatory|financial|culture_fit|competition|timing", "severity": 1-10, "description": "...", "mitigation": "..."}}
  ],
  "engagement_recommendation": {{
    "recommended_persona": "...",
    "recommended_value_proposition": "...",
    "recommended_approach": "relationship_built|value_proof|executive|land_and_expand",
    "optimal_timing": "immediate|this_quarter|next_quarter|monitor",
    "win_probability": 0.0-1.0,
    "estimated_deal_size_range": {{"min": 0, "max": 0, "currency": "USD"}}
  }},
  "competitors_present": [
    {{"competitor_name": "...", "relationship_type": "existing_vendor|evaluating|past_vendor", "confidence": "high|medium|low"}}
  ]
}}
"""

        try:
            response = self._call_llm(prompt)
            analysis = json.loads(response)

            report.strategic_initiatives = [
                StrategicInitiative(**s) for s in analysis.get("strategic_initiatives", [])
            ]
            report.buying_signals = [
                BuyingSignal(**s) for s in analysis.get("buying_signals", [])
            ]
            report.risk_factors = [
                RiskFactor(**r) for r in analysis.get("risk_factors", [])
            ]
            rec = analysis.get("engagement_recommendation", {})
            if rec:
                report.engagement_recommendation = EngagementRecommendation(**rec)
            report.competitors_present = [
                CompetitorPresence(**c) for c in analysis.get("competitors_present", [])
            ]

        except (json.JSONDecodeError, Exception) as e:
            report.data_gaps.append(DataGap(
                domain="analysis",
                gaps=[f"LLM analysis failed: {e}"],
                impact="Using rule-based fallback analysis",
            ))

        return report

    def _call_llm(self, prompt: str) -> str:
        if self._client is None:
            return self._fallback_analysis(prompt)

        try:
            if self._provider == "anthropic":
                msg = self._client.messages.create(
                    model=self._model,
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}],
                )
                return msg.content[0].text
            else:
                response = self._client.chat.completions.create(
                    model=self._model,
                    max_tokens=4000,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.choices[0].message.content or "{}"
        except Exception as e:
            print(f"[!] LLM call failed: {e}")
            return self._fallback_analysis(prompt)

    def _fallback_analysis(self, prompt: str) -> str:
        return json.dumps({
            "account_summary": "Rule-based analysis — no LLM available",
            "strategic_initiatives": [],
            "pain_points_inferred": [],
            "buying_signals": [],
            "key_personas": [],
            "risk_factors": [],
            "engagement_recommendation": {
                "optimal_timing": "monitor", "win_probability": 0.0,
            },
            "competitors_present": [],
        })


def firmographic_section(report: AccountIntelligenceReport) -> str:
    f = report.firmographic
    parts = ["### Firmographic"]
    if f.revenue:
        parts.append(f"Revenue: {f.revenue.value} (confidence: {f.revenue.confidence.value})")
    if f.employees:
        parts.append(f"Employees: {f.employees.value} (confidence: {f.employees.confidence.value})")
    return "\n".join(parts)


def financial_section(report: AccountIntelligenceReport) -> str:
    f = report.financial_health
    parts = ["### Financial"]
    parts.append(f"Confidence: {f.confidence.value}")
    if f.risk_flags:
        parts.append(f"Risk flags: {', '.join(f.risk_flags)}")
    return "\n".join(parts)


def technographic_section(report: AccountIntelligenceReport) -> str:
    t = report.technology_stack
    parts = ["### Technographic"]
    parts.append(f"Detection: {t.detection_method} (confidence: {t.detection_confidence.value})")
    return "\n".join(parts)
