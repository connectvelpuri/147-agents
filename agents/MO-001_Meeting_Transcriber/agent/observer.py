"""MO-001 Meeting Observer — main agent loop.

Listens for meeting audio chunks, transcribes in real time,
publishes transcript chunks, and finalizes the full transcript
when the meeting ends.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope, new_span_id

from .models import (
    AudioChunk, MeetingPlatform, AudioFormat,
    TranscriptChunk, TranscriptSegment, FullTranscript, MeetingMetadata,
)
from .asr_engine import ASREngine


class MeetingObserver(RevenueAgent):
    """Real-time meeting transcription and speaker diarization."""

    def __init__(self, nats_servers: list[str] | None = None):
        super().__init__(
            agent_id="mo-001-v1",
            agent_version="0.1.0",
            llm_tier="simple",
            nats_servers=nats_servers,
        )
        self.asr = ASREngine()
        self._active_meetings: dict[str, list[AudioChunk]] = {}
        self._env = "dev"

    @property
    def tick_interval_seconds(self) -> float:
        return 30.0

    async def on_start(self):
        subjects = [
            f"revenue.{self._env}.meeting.*.audio.chunk",
            f"revenue.{self._env}.meeting.*.started",
            f"revenue.{self._env}.meeting.*.ended",
        ]
        for sub in subjects:
            await self.subscribe(sub)
        print(f"[MO-001] Watching for meeting events on revenue.{self._env}.meeting.*")

    async def handle_event(self, envelope: EventEnvelope):
        event_type = envelope.event_type
        data = envelope.data

        if event_type == "MeetingStarted" or event_type == "meeting.started":
            meeting_id = data.get("meeting_id") or envelope.deal_id or "unknown"
            self._active_meetings[meeting_id] = []
            print(f"[MO-001] Meeting started: {meeting_id} "
                  f"(platform={data.get('platform', 'unknown')})")

        elif event_type == "MeetingAudioChunk" or event_type == "meeting.audio.chunk":
            meeting_id = data.get("meeting_id") or envelope.deal_id or "unknown"
            if meeting_id not in self._active_meetings:
                print(f"[MO-001] WARN: chunk for unknown meeting {meeting_id}")
                return
            chunk = self._parse_chunk(meeting_id, data)
            self._active_meetings[meeting_id].append(chunk)

            result = self.asr.transcribe(chunk)
            if result.success and result.segments:
                transcript_chunk = TranscriptChunk(
                    meeting_id=meeting_id,
                    chunk_index=chunk.chunk_index,
                    segments=result.segments,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                )
                await self.publish(
                    f"revenue.{self._env}.meeting.{meeting_id}.transcript.chunk.{chunk.chunk_index}",
                    "TranscriptChunk",
                    {
                        "meeting_id": meeting_id,
                        "chunk_index": chunk.chunk_index,
                        "segments_count": len(result.segments),
                        "segments": [
                            {"speaker": s.speaker_name, "text": s.text,
                             "start": s.start_time, "end": s.end_time, "confidence": s.confidence}
                            for s in result.segments
                        ],
                    },
                    deal_id=meeting_id,
                )

        elif event_type == "MeetingEnded" or event_type == "meeting.ended":
            meeting_id = data.get("meeting_id") or envelope.deal_id or "unknown"
            chunks = self._active_meetings.pop(meeting_id, [])
            if not chunks:
                print(f"[MO-001] WARN: no chunks for ended meeting {meeting_id}")
                return

            print(f"[MO-001] Finalizing transcript for {meeting_id} ({len(chunks)} chunks)...")
            full = self.asr.transcribe_full(chunks)
            await self._publish_full_transcript(full, meeting_id)
            await self._publish_summary(full, meeting_id)

    async def tick(self):
        active = len(self._active_meetings)
        if active:
            print(f"[MO-001:STATUS] Active meetings: {active}")

    async def _publish_full_transcript(self, transcript: FullTranscript, meeting_id: str):
        await self.publish(
            f"revenue.{self._env}.meeting.{meeting_id}.transcript.full",
            "FullTranscript",
            {
                "meeting_id": meeting_id,
                "duration_seconds": transcript.duration_seconds,
                "segments_count": len(transcript.segments),
                "speakers": [
                    {"id": s.speaker_id, "name": s.speaker_name,
                     "talk_seconds": s.total_talk_seconds, "turns": s.turn_count}
                    for s in transcript.speakers
                ],
                "word_error_rate": transcript.word_error_rate,
                "diarization_accuracy": transcript.diarization_accuracy,
            },
            deal_id=meeting_id,
        )

    async def _publish_summary(self, transcript: FullTranscript, meeting_id: str):
        await self.publish(
            f"revenue.{self._env}.meeting.{meeting_id}.transcript.summary",
            "TranscriptSummary",
            {
                "meeting_id": meeting_id,
                "duration_seconds": transcript.duration_seconds,
                "speaker_count": len(transcript.speakers),
                "top_speaker": max(transcript.speakers, key=lambda s: s.total_talk_seconds).speaker_name if transcript.speakers else "",
                "total_words": len(transcript.raw_text.split()),
            },
            deal_id=meeting_id,
        )

    def _parse_chunk(self, meeting_id: str, data: dict) -> AudioChunk:
        return AudioChunk(
            meeting_id=meeting_id,
            chunk_index=data.get("chunk_index", 0),
            platform=MeetingPlatform(data.get("platform", "generic")),
            format=AudioFormat(data.get("format", "pcm16")),
            data=b"",
            sample_rate=data.get("sample_rate", 16000),
            channels=data.get("channels", 1),
            duration_seconds=data.get("duration_seconds", 0.0),
        )
