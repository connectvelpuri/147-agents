"""MO-004 Commitment Tracker — extracts, categorizes, and tracks meeting commitments.

Uses Moderate LLM tier for contextual commitment extraction with
keyword-based fallback when LLM unavailable.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_event_id

from .models import (
    CommitmentParty, CommitmentStatus, CommitmentType,
    Commitment, CommitmentReminder, MissedCommitmentAlert,
    CommitmentLog, CommitmentAnalysisResult,
)


# Commitment-triggering phrases for rule-based fallback
_BUYER_COMMIT_TRIGGERS = [
    "i'll send", "i'll share", "i'll check", "i'll look", "i'll get back",
    "i'll discuss", "i'll talk to", "i'll review", "i'll think about",
    "i'll let you know", "i'll follow up", "i'll introduce",
    "let me check", "let me look", "let me discuss", "let me review",
    "i will send", "i will share", "i will check",
    "i can send", "i can share", "i can introduce",
    "we'll review", "we'll discuss", "we'll look",
    "send me", "share with me", "email me",
]
_SELLER_COMMIT_TRIGGERS = [
    "i'll send you", "i'll share the", "i'll follow up", "i'll get you",
    "i'll put together", "i'll create", "i'll set up", "i'll schedule",
    "i'll send over", "i'll draft", "i'll prepare",
    "i will send you", "i will share the",
    "let me send", "let me share", "let me set up",
    "we'll send", "we'll share", "we'll set up",
]


class CommitmentTracker(RevenueAgent):
    """Extracts, categorizes, and tracks commitments from meetings."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="mo-004-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._sessions: dict[str, CommitmentAnalysisResult] = {}

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.meeting.transcript")
        print(f"[MO-004] Listening for transcripts on revenue.{self._env}.deal.*.meeting.transcript")

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
                       data: dict) -> Optional[CommitmentAnalysisResult]:
        transcript_text = data.get("text", "") or data.get("full_text", "")
        print(f"[MO-004] Extracting commitments from {deal_id}/{meeting_id} ({len(transcript_text)} chars)...")

        llm_result = self.llm.complete(
            system_prompt=self._commitment_system_prompt(),
            user_prompt=self._commitment_user_prompt(deal_id, meeting_id, transcript_text),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                result = self._parse_llm_result(parsed, deal_id, meeting_id)
                self._sessions[session_key] = result
                print(f"[MO-004] LLM extraction: {result.log.buyer_count} buyer, "
                      f"{result.log.seller_count} seller commitments"
                      f"{' (NO COMMITMENTS)' if result.no_commitments else ''}")
                return result

        fallback = self._rule_analysis(deal_id, meeting_id, transcript_text)
        self._sessions[session_key] = fallback
        return fallback

    async def _publish_result(self, result: CommitmentAnalysisResult, deal_id: str, meeting_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.meeting.commitment_log",
            "MeetingCommitmentLog",
            {
                "deal_id": deal_id,
                "meeting_id": meeting_id,
                "buyer_commitments": result.log.buyer_count,
                "seller_commitments": result.log.seller_count,
                "no_commitments": result.no_commitments,
                "commitments": [
                    {
                        "commitment_id": c.commitment_id,
                        "party": c.party.value,
                        "type": c.type.value,
                        "description": c.description,
                        "status": c.status.value,
                        "participant_id": c.participant_id,
                        "buyer_wiifm": c.buyer_wiifm,
                        "seller_wiifm": c.seller_wiifm,
                        "commitment_risk": c.commitment_risk,
                    }
                    for c in result.log.commitments
                ],
            },
            deal_id=deal_id,
        )
        for reminder in result.reminders:
            await self.publish(
                f"revenue.{self._env}.deal.{deal_id}.meeting.commitment_reminder",
                "CommitmentReminder",
                {
                    "deal_id": deal_id,
                    "commitment_id": reminder.commitment.commitment_id,
                    "description": reminder.commitment.description,
                    "days_overdue": reminder.days_overdue,
                    "suggested_action": reminder.suggested_action,
                },
                deal_id=deal_id,
            )
        for alert in result.missed_alerts:
            await self.publish(
                f"revenue.{self._env}.deal.{deal_id}.meeting.commitment_missed",
                "CommitmentMissed",
                {
                    "deal_id": deal_id,
                    "commitment_id": alert.commitment.commitment_id,
                    "description": alert.commitment.description,
                    "impact": alert.impact,
                    "suggested_recovery": alert.suggested_recovery,
                },
                deal_id=deal_id,
            )

    #  LLM Prompts

    def _commitment_system_prompt(self) -> str:
        return """You are a commitment tracking specialist for sales meetings.
Extract every commitment made during the meeting using the Dual WIIFM framework.

=== Dual WIIFM (Jeff Shore / Bob Burg) ===
Every commitment has TWO "What's In It For Me" sides:
1. Buyer's WIIFM: Why does the buyer benefit from fulfilling this commitment?
   - "Reviewing our proposal helps them compare options confidently"
   - "Introducing their CFO gets them budget clarity"
2. Seller's WIIFM: Why does the seller benefit?
   - "Getting the introduction means we can multi-thread the deal"
   - "Scheduling the demo moves us closer to close"

When both WIIFMs are articulated, commitment likelihood is ~3x higher.
When the buyer's WIIFM is unclear, the commitment is high-risk.

A commitment is anything someone agrees to do after the meeting.

Categories:
- buyer commitments: buyer agrees to send info, review materials, discuss internally, introduce stakeholders
- seller commitments: seller agrees to send documents, schedule demos, prepare proposals

For each commitment, identify:
- party: buyer, seller, or joint
- type: send_document, schedule_meeting, provide_information, internal_discussion, decision, introduce_stakeholder, review_proposal, trial_evaluation, reference_call, other
- description: what exactly was committed
- deadline: if one was stated
- participant_id: who made the commitment
- buyer_wiifm: why this commitment matters to the buyer
- seller_wiifm: why this commitment matters to the seller
- commitment_risk: low, medium, or high (based on clarity of both WIIFMs)

If no commitments were found, set no_commitments: true.

Output JSON only:
{
  "commitments": [
    {
      "party": "buyer",
      "type": "internal_discussion",
      "description": "Will discuss pricing internally with the CFO",
      "deadline": "this Friday",
      "participant_id": "Bob",
      "buyer_wiifm": "Gets budget clarity for decision-making",
      "seller_wiifm": "Moves deal to next stage with financial stakeholder buy-in",
      "commitment_risk": "medium"
    }
  ],
  "no_commitments": false
}"""

    def _commitment_user_prompt(self, deal_id: str, meeting_id: str, transcript: str) -> str:
        return f"""Deal: {deal_id}
Meeting: {meeting_id}

Transcript:
{transcript[:3000]}

Extract all commitments using Dual WIIFM. For each commitment, state the buyer's WIIFM and seller's WIIFM, and assess commitment risk (low/medium/high based on how clear both WIIFMs are). Return JSON only."""

    #  Parsing

    def _parse_llm_result(self, data: dict, deal_id: str, meeting_id: str) -> CommitmentAnalysisResult:
        commitments_raw = data.get("commitments", [])
        no_commit = data.get("no_commitments", False)

        commitments = []
        for c in commitments_raw:
            try:
                party = CommitmentParty(c.get("party", "joint"))
            except ValueError:
                party = CommitmentParty.JOINT
            try:
                ctype = CommitmentType(c.get("type", "other"))
            except ValueError:
                ctype = CommitmentType.OTHER

            commitments.append(Commitment(
                commitment_id=c.get("commitment_id", new_event_id()),
                party=party,
                description=c.get("description", ""),
                type=ctype,
                deadline=c.get("deadline", ""),
                participant_id=c.get("participant_id", ""),
                meeting_id=meeting_id,
                deal_id=deal_id,
                created_at=datetime.now(timezone.utc).isoformat(),
                buyer_wiifm=c.get("buyer_wiifm", ""),
                seller_wiifm=c.get("seller_wiifm", ""),
                commitment_risk=c.get("commitment_risk", "medium"),
            ))

        buyer_c = sum(1 for c in commitments if c.party == CommitmentParty.BUYER)
        seller_c = sum(1 for c in commitments if c.party == CommitmentParty.SELLER)
        joint_c = sum(1 for c in commitments if c.party == CommitmentParty.JOINT)

        return CommitmentAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            log=CommitmentLog(
                meeting_id=meeting_id,
                commitments=commitments,
                buyer_count=buyer_c,
                seller_count=seller_c + joint_c,
            ),
            no_commitments=no_commit and len(commitments) == 0,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    #  Rule-based fallback

    def _rule_analysis(self, deal_id: str, meeting_id: str,
                       transcript: str) -> CommitmentAnalysisResult:
        text_lower = transcript.lower()
        commitments = []
        lines = transcript.split("\n")

        for line in lines:
            line_lower = line.lower()

            # Check buyer commitments
            for trigger in _BUYER_COMMIT_TRIGGERS:
                if trigger in line_lower:
                    party = CommitmentParty.BUYER
                    ctype = CommitmentType.OTHER
                    if any(w in trigger for w in ["send", "share", "email"]):
                        ctype = CommitmentType.SEND_DOCUMENT
                    elif any(w in trigger for w in ["check", "look", "discuss", "talk", "think"]):
                        ctype = CommitmentType.INTERNAL_DISCUSSION
                    elif any(w in trigger for w in ["review"]):
                        ctype = CommitmentType.REVIEW_PROPOSAL
                    elif any(w in trigger for w in ["introduce"]):
                        ctype = CommitmentType.INTRODUCE_STAKEHOLDER

                    speaker = line.split(":")[0].strip() if ":" in line else "unknown"
                    commitments.append(Commitment(
                        commitment_id=new_event_id(),
                        party=party,
                        description=line.strip()[:200],
                        type=ctype,
                        participant_id=speaker,
                        meeting_id=meeting_id,
                        deal_id=deal_id,
                        created_at=datetime.now(timezone.utc).isoformat(),
                    ))
                    break

            # Check seller commitments
            for trigger in _SELLER_COMMIT_TRIGGERS:
                if trigger in line_lower:
                    party = CommitmentParty.SELLER
                    ctype = CommitmentType.OTHER
                    if any(w in trigger for w in ["send", "send you", "send over"]):
                        ctype = CommitmentType.SEND_DOCUMENT
                    elif any(w in trigger for w in ["schedule", "set up"]):
                        ctype = CommitmentType.SCHEDULE_MEETING
                    elif any(w in trigger for w in ["draft", "prepare", "create", "put together"]):
                        ctype = CommitmentType.SEND_DOCUMENT

                    speaker = line.split(":")[0].strip() if ":" in line else "unknown"
                    commitments.append(Commitment(
                        commitment_id=new_event_id(),
                        party=party,
                        description=line.strip()[:200],
                        type=ctype,
                        participant_id=speaker,
                        meeting_id=meeting_id,
                        deal_id=deal_id,
                        created_at=datetime.now(timezone.utc).isoformat(),
                    ))
                    break

        buyer_count = sum(1 for c in commitments if c.party == CommitmentParty.BUYER)
        seller_count = sum(1 for c in commitments if c.party == CommitmentParty.SELLER)

        return CommitmentAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            log=CommitmentLog(
                meeting_id=meeting_id,
                commitments=commitments,
                buyer_count=buyer_count,
                seller_count=seller_count,
            ),
            no_commitments=len(commitments) == 0,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )
