"""MO-003 Objection Detector and Classifier — identifies, classifies, and timestamps objections.

Uses Moderate LLM tier for contextual objection classification with
keyword-based fallback when LLM unavailable.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_event_id

from .models import (
    ObjectionCategory, ObjectionSeverity,
    ObjectionEvent, RecommendedResponse, ObjectionLog,
    UnaddressedObjectionAlert, ObjectionPattern, ObjectionAnalysisResult,
)


# Keyword maps for rule-based fallback detection
_OBJECTION_KEYWORDS: dict[ObjectionCategory, list[str]] = {
    ObjectionCategory.PRICE: [
        "too expensive", "too much", "overpriced", "cost", "pricing",
        "budget", "afford", "expensive", "price", "costly",
        "not in budget", "no budget", "can't afford", "spend",
    ],
    ObjectionCategory.TIMING: [
        "not right now", "too soon", "not yet", "later", "timing",
        "this quarter", "next quarter", "next year", "too busy",
        "not a priority right now", "bad time", "not the right time",
    ],
    ObjectionCategory.AUTHORITY: [
        "need to check", "need approval", "talk to my manager",
        "involve legal", "need to discuss", "not my decision",
        "need buy-in", "need to run this by", "i'll need",
    ],
    ObjectionCategory.NEED: [
        "don't need", "not a problem", "not needed", "not necessary",
        "don't have that issue", "working fine", "not a priority",
        "not important", "satisfied with current", "happy with",
    ],
    ObjectionCategory.COMPETING_PRIORITY: [
        "other priorities", "competing", "multiple initiatives",
        "too many projects", "not the only thing", "other things",
        "bandwidth", "capacity", "already working on",
    ],
    ObjectionCategory.COMPETITOR: [
        "using another", "already use", "evaluating others",
        "comparing", "competitor", "salesforce", "hubspot",
        "other vendor", "another solution", "currently using",
    ],
    ObjectionCategory.SECURITY: [
        "security", "compliance", "data privacy", "gdrp",
        "security review", "vulnerability", "data residency",
        "audit", "security team", "infosec", "certification",
        "soc2", "hipaa", "encryption",
    ],
    ObjectionCategory.FIT: [
        "not a fit", "doesn't fit", "not suitable", "wrong fit",
        "not aligned", "not for us", "different needs",
        "misalignment", "doesn't match",
    ],
}


class ObjectionDetector(RevenueAgent):
    """Detects, classifies, and timestamps objections during meetings."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="mo-003-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._sessions: dict[str, ObjectionAnalysisResult] = {}
        self._account_patterns: dict[str, list[ObjectionPattern]] = {}

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.meeting.transcript_chunk")
        await self.subscribe(f"revenue.{self._env}.deal.*.meeting.transcript")
        print(f"[MO-003] Listening for transcripts on revenue.{self._env}.deal.*.meeting.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}
        meeting_id = data.get("meeting_id", "unknown")
        session_key = f"{deal_id}:{meeting_id}"

        if event_type == "FullTranscript":
            result = await self._analyze(session_key, deal_id, meeting_id, data)
            if result:
                await self._publish_result(result, deal_id, meeting_id)

    async def _analyze(self, session_key: str, deal_id: str, meeting_id: str,
                       data: dict) -> Optional[ObjectionAnalysisResult]:
        transcript_text = data.get("text", "") or data.get("full_text", "")
        print(f"[MO-003] Analyzing transcript for {deal_id}/{meeting_id} ({len(transcript_text)} chars)...")

        llm_result = self.llm.complete(
            system_prompt=self._objection_system_prompt(),
            user_prompt=self._objection_user_prompt(deal_id, meeting_id, transcript_text),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                result = self._parse_llm_result(parsed, deal_id, meeting_id)
                self._sessions[session_key] = result
                # Update account patterns
                await self._update_patterns(deal_id, result)
                print(f"[MO-003] LLM analysis: {result.objection_count} objections "
                      f"({result.blocking_count} blocking), {len(result.alerts)} unaddressed")
                return result

        fallback = self._rule_analysis(deal_id, meeting_id, transcript_text)
        self._sessions[session_key] = fallback
        return fallback

    async def _update_patterns(self, account_id: str, result: ObjectionAnalysisResult):
        if account_id not in self._account_patterns:
            self._account_patterns[account_id] = []
        existing = {p.category.value: p for p in self._account_patterns[account_id]}

        now = datetime.now(timezone.utc).isoformat()
        for obj in result.log.objections:
            cat_val = obj.category.value
            if cat_val in existing:
                p = existing[cat_val]
                p.frequency += 1
                p.last_seen = now
                if obj.utterance not in p.sample_utterances:
                    p.sample_utterances.append(obj.utterance)
            else:
                p = ObjectionPattern(
                    category=obj.category, account_id=account_id,
                    first_seen=now, last_seen=now,
                    sample_utterances=[obj.utterance],
                )
                existing[cat_val] = p
        self._account_patterns[account_id] = list(existing.values())

    async def _publish_result(self, result: ObjectionAnalysisResult, deal_id: str, meeting_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.meeting.objection_log",
            "MeetingObjectionLog",
            {
                "deal_id": deal_id,
                "meeting_id": meeting_id,
                "objection_count": result.objection_count,
                "blocking_count": result.blocking_count,
                "addressed_count": result.addressed_count,
                "objections": [
                    {
                        "objection_id": o.objection_id,
                        "participant_id": o.participant_id,
                        "category": o.category.value,
                        "severity": o.severity.value,
                        "utterance": o.utterance,
                        "addressed": o.addressed,
                    }
                    for o in result.log.objections
                ],
            },
            deal_id=deal_id,
        )
        for alert in result.alerts:
            await self.publish(
                f"revenue.{self._env}.deal.{deal_id}.meeting.objection_alert",
                "UnaddressedObjectionAlert",
                {
                    "deal_id": deal_id,
                    "meeting_id": meeting_id,
                    "objection_id": alert.objection_id,
                    "participant_id": alert.participant_id,
                    "category": alert.category.value,
                    "severity": alert.severity.value,
                    "context": alert.context,
                },
                deal_id=deal_id,
            )

    #  LLM Prompts

    def _objection_system_prompt(self) -> str:
        return """You are an objection detection specialist using Gal Borenstein's Three-Bucket framework,
Jeff Shore's CBT method, and Andy Paul's 5 Fears model.

Analyze the transcript and identify every objection raised by the buyer.

=== CATEGORIZATION ===
Categories: price, timing, authority, need, competing_priority, competitor, security, fit
Severity: blocking (deal-killer), significant (major concern), minor (small doubt)

=== PSYCHOLOGICAL BUCKET (Gal Borenstein) ===
Map each objection to the buyer's unspoken fear:

SAFE bucket: "Will this get me fired / cause problems?"
  - price → "I'll be blamed for overspending"
  - security → "I'll be blamed for a breach"
  - authority → "I need permission to avoid blame"

BEST bucket: "Is this the right choice among options?"
  - need → "Do we actually need this?"
  - competitor → "Is this better than others?"
  - fit → "Does this actually work for us?"

INNOVATIVE bucket: "Is the timing right?"
  - timing → "Am I too early/late?"
  - competing_priority → "Is this more important than everything else?"

=== 5 FEARS (Andy Paul) ===
Identify which fear is driving the objection:
  1. FEAR OF MISTAKE: "I don't want to make the wrong choice"
  2. FEAR OF CHANGE: "The current system works well enough"
  3. FEAR OF LOSING CREDIBILITY: "What if this makes me look bad?"
  4. FEAR OF COMMITMENT: "What if something better comes along?"
  5. FEAR OF THE UNKNOWN: "I don't have enough information"

=== CBT RESPONSE (Jeff Shore) ===
For EACH objection, suggest which CBT step applies:
  Step 1 — VALIDATE: "That makes sense given what you know"
  Step 2 — REFRAME: "What if the risk is actually staying put?"
  Step 3 — REPLACE: "Here's what other leaders in your position found"

Output JSON only:
{
  "objections": [
    {
      "participant_id": "speaker",
      "timestamp_sec": 0,
      "category": "price",
      "severity": "significant",
      "utterance": "This seems expensive for what we need",
      "context": "Responding to pricing discussion",
      "addressed": false,
      "response_utterance": "",
      "psychological_bucket": "safe",
      "underlying_fear": "fear_of_mistake",
      "cbt_step": 1
    }
  ],
  "unaddressed_alerts": [
    {
      "objection_id": "...",
      "participant_id": "speaker",
      "category": "price",
      "severity": "significant",
      "context": "No response from seller"
    }
  ],
  "response_map": {
    "price": {
      "strategy": "Value justify / ROI breakdown",
      "suggested_rebuttal": "Share ROIs from similar customers",
      "psychological_bucket": "safe",
      "underlying_fear": "fear_of_mistake"
    }
  }
}"""

    def _objection_user_prompt(self, deal_id: str, meeting_id: str, transcript: str) -> str:
        bucket_guide = (
            "Bucket response strategies:\n"
            "  SAFE bucket: Validate concern, offer risk reversal, "
            "reframe 'what if the risk is staying put?'\n"
            "  BEST bucket: Acknowledge comparison, ask evaluation criteria, "
            "provide comparative evidence\n"
            "  INNOVATIVE bucket: Validate timing, share peer adoption, "
            "reframe cost of inaction\n\n"
            "Fear response strategies:\n"
            "  FEAR OF MISTAKE: Risk reversal + limited commitment framing\n"
            "  FEAR OF CHANGE: Loss aversion + Discovery Gap\n"
            "  FEAR OF LOSING CREDIBILITY: Validate + peer proof from similar roles\n"
            "  FEAR OF COMMITMENT: Micro-commitments + no long-term contract framing\n"
            "  FEAR OF THE UNKNOWN: Transparency + concrete examples\n"
        )
        return f"""Deal: {deal_id}
Meeting: {meeting_id}

{bucket_guide}

Transcript:
{transcript[:3000]}

Identify all objections. Classify each by bucket (safe/best/innovative)
and underlying fear (fear_of_mistake / fear_of_change / fear_of_losing_credibility /
fear_of_commitment / fear_of_the_unknown).
Return JSON only."""

    #  Parsing

    def _parse_llm_result(self, data: dict, deal_id: str, meeting_id: str) -> ObjectionAnalysisResult:
        objections_raw = data.get("objections", [])
        responses_raw = data.get("response_map", {})

        response_map = {}
        for cat, resp in responses_raw.items():
            try:
                c = ObjectionCategory(cat)
                bucket_raw = resp.get("psychological_bucket", "")
                fear_raw = resp.get("underlying_fear", "")
                bucket = None
                if bucket_raw:
                    try:
                        bucket = PsychologicalBucket(bucket_raw)
                    except ValueError:
                        pass
                fear = None
                if fear_raw:
                    try:
                        fear = BuyerFear(fear_raw)
                    except ValueError:
                        pass
                response_map[cat] = RecommendedResponse(
                    category=c,
                    strategy=resp.get("strategy", ""),
                    suggested_rebuttal=resp.get("suggested_rebuttal", ""),
                    psychological_bucket=bucket or BUCKET_MAP.get(c),
                    underlying_fear=fear or FEAR_MAP.get(c),
                )
            except ValueError:
                pass

        objection_events = []
        unaddressed = []
        for o in objections_raw:
            try:
                cat = ObjectionCategory(o.get("category", "price"))
            except ValueError:
                cat = ObjectionCategory.PRICE
            try:
                sev = ObjectionSeverity(o.get("severity", "minor"))
            except ValueError:
                sev = ObjectionSeverity.MINOR

            bucket = None
            bucket_raw = o.get("psychological_bucket", "")
            if bucket_raw:
                try:
                    bucket = PsychologicalBucket(bucket_raw)
                except ValueError:
                    bucket = BUCKET_MAP.get(cat)

            fear = None
            fear_raw = o.get("underlying_fear", "")
            if fear_raw:
                try:
                    fear = BuyerFear(fear_raw)
                except ValueError:
                    fear = FEAR_MAP.get(cat)

            event = ObjectionEvent(
                objection_id=o.get("objection_id", new_event_id()),
                participant_id=o.get("participant_id", "unknown"),
                timestamp_sec=float(o.get("timestamp_sec", 0)),
                category=cat,
                severity=sev,
                utterance=o.get("utterance", ""),
                context=o.get("context", ""),
                addressed=o.get("addressed", False),
                response_utterance=o.get("response_utterance", ""),
                psychological_bucket=bucket or BUCKET_MAP.get(cat),
                underlying_fear=fear or FEAR_MAP.get(cat),
            )
            objection_events.append(event)

        for a in data.get("unaddressed_alerts", []):
            unaddressed.append(UnaddressedObjectionAlert(
                objection_id=a.get("objection_id", new_event_id()),
                participant_id=a.get("participant_id", "unknown"),
                category=ObjectionCategory(a.get("category", "price")),
                severity=ObjectionSeverity(a.get("severity", "minor")),
                context=a.get("context", ""),
                timestamp_sec=float(a.get("timestamp_sec", 0)),
            ))

        blocking = sum(1 for o in objection_events if o.severity == ObjectionSeverity.BLOCKING)
        addressed = sum(1 for o in objection_events if o.addressed)

        return ObjectionAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            log=ObjectionLog(meeting_id=meeting_id, objections=objection_events, response_map=response_map),
            alerts=unaddressed,
            objection_count=len(objection_events),
            blocking_count=blocking,
            addressed_count=addressed,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    #  Rule-based fallback

    def _rule_analysis(self, deal_id: str, meeting_id: str,
                       transcript: str) -> ObjectionAnalysisResult:
        text_lower = transcript.lower()
        objections = []
        unaddressed = []

        for category, keywords in _OBJECTION_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    idx = text_lower.find(kw)
                    start = max(0, idx - 20)
                    end = min(len(transcript), idx + len(kw) + 40)
                    context = transcript[start:end].strip()

                    # simple severity heuristic
                    sev = (
                        ObjectionSeverity.BLOCKING
                        if category in (ObjectionCategory.PRICE, ObjectionCategory.SECURITY)
                        and any(w in kw for w in ["expensive", "security", "budget"])
                        else ObjectionSeverity.MINOR
                    )
                    event = ObjectionEvent(
                        objection_id=new_event_id(),
                        participant_id="unknown",
                        timestamp_sec=0.0,
                        category=category,
                        severity=sev,
                        utterance=kw,
                        context=context,
                        psychological_bucket=BUCKET_MAP.get(category),
                        underlying_fear=FEAR_MAP.get(category),
                    )
                    objections.append(event)
                    unaddressed.append(UnaddressedObjectionAlert(
                        objection_id=event.objection_id,
                        participant_id="unknown",
                        category=category,
                        severity=sev,
                        context=context,
                        timestamp_sec=0.0,
                    ))

        # Deduplicate by removing duplicate-category objections
        seen_categories = set()
        unique_objections = []
        for o in objections:
            if o.category not in seen_categories:
                seen_categories.add(o.category)
                unique_objections.append(o)

        blocking = sum(1 for o in unique_objections if o.severity == ObjectionSeverity.BLOCKING)

        return ObjectionAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            log=ObjectionLog(meeting_id=meeting_id, objections=unique_objections),
            alerts=unaddressed[:len(unique_objections)],
            objection_count=len(unique_objections),
            blocking_count=blocking,
            addressed_count=0,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )
