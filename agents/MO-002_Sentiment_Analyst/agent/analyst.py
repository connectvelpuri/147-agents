"""MO-002 Sentiment and Emotion Analyst — tracks emotional trajectory of meeting participants.

Uses Moderate LLM tier for contextual sentiment analysis with
rule-based keyword fallback when LLM unavailable.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    SentimentLabel, EmotionType, SentimentTrend, NeurosciencePrinciple,
    SentimentPoint, ParticipantSentimentTimeline, EmotionHighlight,
    EngagementScore, FrustrationAlert, ConfusionMarker, SentimentAnalysisResult,
)


# Positive / negative / confusion keyword lists for rule-based fallback
_POSITIVE_WORDS = {
    "great", "excellent", "perfect", "love", "amazing", "fantastic",
    "awesome", "brilliant", "wonderful", "terrific", "outstanding",
    "impressed", "impressive", "delighted", "happy", "pleased",
    "excited", "exciting", "fantastic", "superb", "thrilled",
    "perfect", "ideal", "solves", "solution", "valuable", "value",
    "confident", "helpful", "thanks", "thank", "appreciate",
    "absolutely", "agree", "agreed", "makes sense", "exactly",
}
_NEGATIVE_WORDS = {
    "bad", "terrible", "horrible", "awful", "hate", "dislike",
    "disappointed", "disappointing", "frustrating", "frustrated",
    "annoying", "annoyed", "waste", "useless", "pointless",
    "expensive", "too much", "too expensive", "overpriced",
    "slow", "broken", "doesn't work", "not working", "problem",
    "issue", "concern", "worried", "worry", "difficult", "hard",
    "complicated", "confusing", "unclear", "not sure", "not good",
    "unfortunately", "sorry but", "unfortunately", "no thanks",
}
_CONFUSION_WORDS = {
    "confused", "confusing", "unclear", "not sure", "what do you mean",
    "can you explain", "i don't follow", "i don't understand",
    "not following", "lost me", "too complex", "complex",
    "complicated", "need more detail", "clarify", "clarification",
}


class SentimentAnalyst(RevenueAgent):
    """Tracks emotional trajectory of meeting participants in real time."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="mo-002-v1",
            agent_version="0.1.0",
            llm_tier="moderate",
            nats_servers=nats_servers,
        )
        self._env = "dev"
        self._sessions: dict[str, SentimentAnalysisResult] = {}

    async def on_start(self):
        await self.subscribe(f"revenue.{self._env}.deal.*.meeting.transcript_chunk")
        await self.subscribe(f"revenue.{self._env}.deal.*.meeting.transcript")
        print(f"[MO-002] Listening for transcript chunks / full transcripts on revenue.{self._env}.deal.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        deal_id = envelope.deal_id or "unknown"
        data = envelope.data or {}

        meeting_id = data.get("meeting_id", "unknown")
        session_key = f"{deal_id}:{meeting_id}"

        if event_type == "TranscriptChunk":
            await self._handle_chunk(session_key, deal_id, meeting_id, data)
        elif event_type == "FullTranscript":
            result = await self._handle_full(session_key, deal_id, meeting_id, data)
            if result:
                await self._publish_result(result, deal_id, meeting_id)

    async def _handle_chunk(self, session_key: str, deal_id: str, meeting_id: str, data: dict):
        chunk_text = data.get("text", "")
        speaker = data.get("speaker", "unknown")
        timestamp = float(data.get("timestamp_sec", 0))

        if session_key not in self._sessions:
            self._sessions[session_key] = SentimentAnalysisResult(
                deal_id=deal_id, meeting_id=meeting_id,
                analyzed_at=datetime.now(timezone.utc).isoformat(),
            )

        sp = self._rule_sentiment_point(speaker, timestamp, chunk_text)
        self._sessions[session_key].timelines.append(
            ParticipantSentimentTimeline(participant_id=speaker, points=[sp])
        )

    async def _handle_full(self, session_key: str, deal_id: str, meeting_id: str,
                           data: dict) -> Optional[SentimentAnalysisResult]:
        transcript_text = data.get("text", "") or data.get("full_text", "")
        speakers = data.get("speakers", [])

        print(f"[MO-002] Analyzing full transcript for {deal_id}/{meeting_id} ({len(transcript_text)} chars)...")

        llm_result = self.llm.complete(
            system_prompt=self._sentiment_system_prompt(),
            user_prompt=self._sentiment_user_prompt(deal_id, meeting_id, transcript_text, speakers),
        )

        if llm_result.success:
            parsed = self.llm.format_json(llm_result.text)
            if parsed:
                result = self._parse_llm_result(parsed, deal_id, meeting_id)
                print(f"[MO-002] LLM analysis: sentiment={result.overall_meeting_sentiment.value}, "
                      f"highlights={len(result.highlights)}, alerts={len(result.frustration_alerts)}")
                self._sessions[session_key] = result
                return result

        fallback = self._rule_full_analysis(deal_id, meeting_id, transcript_text, speakers)
        self._sessions[session_key] = fallback
        return fallback

    async def _publish_result(self, result: SentimentAnalysisResult, deal_id: str, meeting_id: str):
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.meeting.sentiment_timeline",
            "MeetingSentimentTimeline",
            {
                "deal_id": deal_id,
                "meeting_id": meeting_id,
                "overall_sentiment": result.overall_meeting_sentiment.value,
                "participant_count": len(result.timelines),
                "timelines": [
                    {
                        "participant_id": t.participant_id,
                        "overall_sentiment": t.overall_sentiment.value,
                        "trend": t.trend.value,
                        "dominant_emotions": [e.value for e in t.dominant_emotions],
                    }
                    for t in result.timelines
                ],
            },
            deal_id=deal_id,
        )
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.meeting.emotion_highlights",
            "MeetingEmotionHighlights",
            {
                "deal_id": deal_id,
                "meeting_id": meeting_id,
                "highlights": [
                    {"participant_id": h.participant_id, "emotion": h.emotion.value,
                     "intensity": h.intensity, "context": h.context}
                    for h in result.highlights
                ],
            },
            deal_id=deal_id,
        )
        await self.publish(
            f"revenue.{self._env}.deal.{deal_id}.meeting.engagement_score",
            "MeetingEngagementScore",
            {
                "deal_id": deal_id,
                "meeting_id": meeting_id,
                "engagement_scores": [
                    {"participant_id": e.participant_id, "score": e.score, "trend": e.trend.value}
                    for e in result.engagement_scores
                ],
            },
            deal_id=deal_id,
        )
        if result.frustration_alerts:
            for fa in result.frustration_alerts:
                await self.publish(
                    f"revenue.{self._env}.deal.{deal_id}.meeting.frustration_alert",
                    "FrustrationAlert",
                    {
                        "deal_id": deal_id, "meeting_id": meeting_id,
                        "participant_id": fa.participant_id, "intensity": fa.intensity,
                        "context": fa.context, "timestamp_sec": fa.timestamp_sec,
                    },
                    deal_id=deal_id,
                )

    #  LLM Prompts

    def _sentiment_system_prompt(self) -> str:
        return """You are a sentiment and emotion analyst for sales meetings, trained in
10 neuroscience principles of emotional intelligence.

Analyze meeting transcripts and extract emotional signals per participant.

For each participant, identify:
1. Overall sentiment trajectory (positive, negative, neutral, mixed)
2. Specific emotional moments (excitement, frustration, confusion, skepticism, etc.)
3. Engagement level (0.0-1.0)
4. Frustration alerts (threshold >0.6 intensity)
5. Confusion markers (moments buyer appears confused)

=== 10 Neuroscience Principles for Emotion Detection ===

1. COGNITIVE DISSONANCE: Contradictory statements, backtracking, hedging.
   Signal: Anxiety, discomfort — the mind trying to reconcile inconsistency.
   Action: Probe to resolve, realign expectations.

2. LOSS AVERSION DOMINANCE: Focus on what they'll lose vs what they'll gain.
   Signal: Cautious/defensive language ("concerned", "worried", "risk").
   Action: Reframe as "what do you lose by waiting?"

3. SOCIAL PROOF SEEKING: "Who else is using this?" "What do others think?"
   Signal: Curious but uncertain — needs safety in numbers.
   Action: Cite peer evidence to validate.

4. ANCHORING EFFECT: Fixation on first piece of info (price, timeline, feature).
   Signal: Negotiating / cautious posture around a specific reference point.
   Action: Work from their frame, reset only if necessary.

5. STATUS QUO BIAS: "We've always done it this way."
   Signal: Resistance to change, inertia.
   Action: Don't push — create productive discomfort about current state.

6. REACTANCE: "Don't tell me what I need."
   Signal: Defensive, pushback against perceived pressure.
   Action: Give autonomy, back off, let them feel in control.

7. EMOTIONAL CONTAGION: Their tone mirrors yours.
   Signal: If they're flat, they may be reflecting your energy.
   Action: Lead with tone — enthusiasm begets enthusiasm.

8. PROSPECT THEORY (Risk Asymmetry): Risk-avoidant in gains, risk-seeking in losses.
   Signal: "I'm worried" = gain territory (risk averse). "I'm losing" = loss territory (risk seeking).
   Action: Frame situations as loss territory to drive action.

9. ZEIGARNIK EFFECT (Open Loops): Incomplete thoughts, hanging questions.
   Signal: They'll return to close unfinished mental loops.
   Action: Leave strategic questions unanswered to maintain engagement.

10. PEAK-END RULE: They remember the emotional peak and the ending.
    Signal: Overall impression is shaped by the most intense moment + the final moment.
    Action: Ensure the conversation ends on a high note.

Output JSON only:
{
  "participants": [
    {
      "participant_id": "speaker_a",
      "overall_sentiment": "positive",
      "trend": "improving",
      "dominant_emotions": ["excitement", "interest"],
      "engagement_score": 0.85,
      "neuroscience_signals": ["cognitive_dissonance", "emotional_contagion"]
    }
  ],
  "highlights": [
    {"participant_id": "speaker_a", "timestamp_sec": 1245, "emotion": "excitement",
     "intensity": 0.9, "context": "Excited about integration capabilities",
     "utterance": "This would be huge for our team",
     "neuroscience_principle": "social_proof_seeking"}
  ],
  "frustration_alerts": [],
  "confusion_markers": [],
  "overall_meeting_sentiment": "positive"
}"""

    def _sentiment_user_prompt(self, deal_id: str, meeting_id: str,
                                transcript: str, speakers: list) -> str:
        speaker_list = ", ".join(speakers) if speakers else "unknown"
        neuro_guide = (
            "Neuroscience mapping guide:\n"
            "  - cognitive_dissonance: hedging, contradiction, anxiety\n"
            "  - loss_aversion: focus on what they'll lose, caution\n"
            "  - social_proof_seeking: asking about peers, need validation\n"
            "  - anchoring: fixated on first number/reference point\n"
            "  - status_quo_bias: resistance, 'we've always done it this way'\n"
            "  - reactance: defensive pushback to perceived pressure\n"
            "  - emotional_contagion: mirroring your energy (or lack of)\n"
            "  - prospect_theory: risk-avoidant vs risk-seeking language\n"
            "  - zeigarnik_effect: open loops, hanging questions\n"
            "  - peak_end_rule: intense moments + final moments shape memory\n"
        )
        return f"""Deal: {deal_id}
Meeting: {meeting_id}
Participants: {speaker_list}

{neuro_guide}

Transcript:
{transcript[:3000]}

Analyze the emotional trajectory of each participant. Map emotions to neuroscience principles where applicable."""

    #  Parsing

    def _parse_llm_result(self, data: dict, deal_id: str, meeting_id: str) -> SentimentAnalysisResult:
        participants_raw = data.get("participants", [])

        timelines = []
        engagement_scores = []
        for p in participants_raw:
            pid = p.get("participant_id", "unknown")
            emotions = [EmotionType(e) for e in p.get("dominant_emotions", [])
                        if e in EmotionType._value2member_map_]
            neuro = [s for s in p.get("neuroscience_signals", [])
                     if s in NeurosciencePrinciple._value2member_map_]
            timelines.append(ParticipantSentimentTimeline(
                participant_id=pid,
                overall_sentiment=self._parse_sentiment(p.get("overall_sentiment", "neutral")),
                trend=self._parse_trend(p.get("trend", "stable")),
                dominant_emotions=emotions,
                neuroscience_signals=neuro,
            ))
            engagement_scores.append(EngagementScore(
                participant_id=pid,
                score=min(1.0, max(0.0, float(p.get("engagement_score", 0.5)))),
                trend=self._parse_trend(p.get("trend", "stable")),
            ))

        return SentimentAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            timelines=timelines,
            highlights=[EmotionHighlight(
                participant_id=h.get("participant_id", ""),
                timestamp_sec=float(h.get("timestamp_sec", 0)),
                emotion=EmotionType(h.get("emotion", "interest")),
                intensity=float(h.get("intensity", 0.5)),
                context=h.get("context", ""),
                utterance=h.get("utterance", ""),
                neuroscience_principle=h.get("neuroscience_principle", ""),
            ) for h in data.get("highlights", []) if h.get("emotion") in EmotionType._value2member_map_],
            engagement_scores=engagement_scores,
            frustration_alerts=[FrustrationAlert(
                participant_id=f.get("participant_id", ""),
                intensity=float(f.get("intensity", 0)),
                context=f.get("context", ""),
                timestamp_sec=float(f.get("timestamp_sec", 0)),
                utterance=f.get("utterance", ""),
            ) for f in data.get("frustration_alerts", [])],
            confusion_markers=[ConfusionMarker(
                participant_id=c.get("participant_id", ""),
                timestamp_sec=float(c.get("timestamp_sec", 0)),
                context=c.get("context", ""),
                trigger_phrase=c.get("trigger_phrase", ""),
            ) for c in data.get("confusion_markers", [])],
            overall_meeting_sentiment=self._parse_sentiment(
                data.get("overall_meeting_sentiment", "neutral")),
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    def _parse_sentiment(self, val: str) -> SentimentLabel:
        try:
            return SentimentLabel(val.lower())
        except ValueError:
            return SentimentLabel.NEUTRAL

    def _parse_trend(self, val: str) -> SentimentTrend:
        try:
            return SentimentTrend(val.lower())
        except ValueError:
            return SentimentTrend.STABLE

    #  Rule-based fallback

    def _rule_sentiment_point(self, speaker: str, timestamp: float, text: str) -> SentimentPoint:
        words = set(text.lower().split())
        pos_hits = len(words & _POSITIVE_WORDS)
        neg_hits = len(words & _NEGATIVE_WORDS)
        conf_hits = len(words & _CONFUSION_WORDS)

        if pos_hits > neg_hits and pos_hits > conf_hits:
            sentiment = SentimentLabel.POSITIVE
            intensity = min(1.0, pos_hits * 0.15)
        elif neg_hits > pos_hits:
            sentiment = SentimentLabel.NEGATIVE
            intensity = min(1.0, neg_hits * 0.15)
        elif conf_hits > 0:
            sentiment = SentimentLabel.NEUTRAL
            intensity = min(1.0, conf_hits * 0.15)
        else:
            sentiment = SentimentLabel.NEUTRAL
            intensity = 0.2

        emotions = []
        if pos_hits > 1:
            emotions.append(EmotionType.INTEREST)
        if neg_hits > 1:
            emotions.append(EmotionType.SKEPTICISM)
        if conf_hits > 0:
            emotions.append(EmotionType.CONFUSION)

        return SentimentPoint(
            participant_id=speaker,
            timestamp_sec=timestamp,
            sentiment=sentiment,
            emotions=emotions,
            intensity=intensity,
            confidence=0.5,
            utterance_snippet=text[:100],
        )

    def _rule_full_analysis(self, deal_id: str, meeting_id: str,
                            transcript: str, speakers: list[str]) -> SentimentAnalysisResult:
        lines = transcript.split("\n")
        results: dict[str, ParticipantSentimentTimeline] = {}
        highlights: list[EmotionHighlight] = []
        alerts: list[FrustrationAlert] = []
        markers: list[ConfusionMarker] = []

        for line in lines[:200]:
            parts = line.split(":", 1)
            if len(parts) < 2:
                continue
            speaker = parts[0].strip()
            text = parts[1].strip()
            if not speaker:
                continue
            words = set(text.lower().split())
            pos_hits = len(words & _POSITIVE_WORDS)
            neg_hits = len(words & _NEGATIVE_WORDS)
            conf_hits = len(words & _CONFUSION_WORDS)

            if speaker not in results:
                results[speaker] = ParticipantSentimentTimeline(participant_id=speaker)

            if pos_hits > neg_hits and pos_hits > 0:
                results[speaker].points.append(
                    SentimentPoint(speaker, 0, SentimentLabel.POSITIVE, [EmotionType.INTEREST],
                                   min(1.0, pos_hits * 0.2), 0.5, text[:100])
                )
            if neg_hits > 0 and neg_hits >= pos_hits:
                results[speaker].points.append(
                    SentimentPoint(speaker, 0, SentimentLabel.NEGATIVE, [EmotionType.SKEPTICISM],
                                   min(1.0, neg_hits * 0.2), 0.5, text[:100])
                )
                if neg_hits >= 3 and not any(fa.context == text[:50] for fa in alerts):
                    alerts.append(FrustrationAlert(speaker, min(1.0, neg_hits * 0.25),
                                                   text[:100], 0, text[:100]))
            if conf_hits > 0:
                results[speaker].points.append(
                    SentimentPoint(speaker, 0, SentimentLabel.NEUTRAL, [EmotionType.CONFUSION],
                                   min(1.0, conf_hits * 0.2), 0.5, text[:100])
                )
                markers.append(ConfusionMarker(speaker, 0, text[:100], text[:50]))

        for pid, tl in results.items():
            total = len(tl.points)
            if total == 0:
                continue
            pos_count = sum(1 for p in tl.points if p.sentiment == SentimentLabel.POSITIVE)
            neg_count = sum(1 for p in tl.points if p.sentiment == SentimentLabel.NEGATIVE)
            ratio = pos_count / (neg_count + 1)
            tl.overall_sentiment = SentimentLabel.POSITIVE if ratio > 2 else SentimentLabel.NEGATIVE if neg_count > pos_count else SentimentLabel.NEUTRAL
            tl.trend = SentimentTrend.IMPROVING if ratio > 1.5 else SentimentTrend.DECLINING if ratio < 0.5 else SentimentTrend.STABLE
            if pos_count > 0:
                tl.dominant_emotions.append(EmotionType.INTEREST)
            if neg_count > 0:
                tl.dominant_emotions.append(EmotionType.SKEPTICISM)

            # Also add engagement for each speaker
            engagement_score = pos_count / max(total, 1) * 0.7 + 0.3
            tl.dominant_emotions = list(set(tl.dominant_emotions))

        engagement_scores = [
            EngagementScore(pid, len(tl.points) / 50 if tl.points else 0.0,
                            tl.trend, 0.0, "")
            for pid, tl in results.items()
        ]

        # Collapse per-participant timelines: collect all points for same speaker
        collapsed: dict[str, ParticipantSentimentTimeline] = {}
        for pid, tl in results.items():
            if pid not in collapsed:
                collapsed[pid] = ParticipantSentimentTimeline(
                    participant_id=pid,
                    overall_sentiment=tl.overall_sentiment,
                    trend=tl.trend,
                    dominant_emotions=tl.dominant_emotions,
                )

        return SentimentAnalysisResult(
            deal_id=deal_id,
            meeting_id=meeting_id,
            timelines=list(collapsed.values()),
            highlights=highlights,
            engagement_scores=engagement_scores,
            frustration_alerts=alerts,
            confusion_markers=markers,
            overall_meeting_sentiment=(
                SentimentLabel.POSITIVE
                if sum(1 for e in engagement_scores if e.score > 0.5) > len(engagement_scores) / 2
                else SentimentLabel.NEGATIVE
                if any(a.intensity > 0.7 for a in alerts)
                else SentimentLabel.NEUTRAL
            ),
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )
