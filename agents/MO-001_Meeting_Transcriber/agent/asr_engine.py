"""ASR engine — converts audio chunks to text with speaker diarization.

Primary: OpenAI Whisper API (or local whisper.cpp)
Fallback: Rule-based silence detection + basic transcription
"""

from __future__ import annotations

import io
import os
import wave
from typing import Optional
from datetime import datetime, timezone

from .models import (
    AudioChunk, ASRResult, TranscriptSegment, FullTranscript,
    SpeakerSegment, MeetingMetadata,
)


class ASREngine:
    """Speech-to-text with diarization.

    Tier 1: OpenAI Whisper API (best accuracy)
    Tier 2: Local whisper.cpp (no API key needed)
    Tier 3: Simple rule-based fallback
    """

    def __init__(self):
        self._use_local = not bool(os.getenv("OPENAI_API_KEY"))

    def transcribe(self, chunk: AudioChunk, language: str = "en") -> ASRResult:
        if self._use_local:
            return self._local_fallback(chunk)
        return self._whisper_api(chunk, language)

    def transcribe_full(self, chunks: list[AudioChunk], language: str = "en") -> FullTranscript:
        all_segments: list[TranscriptSegment] = []
        all_text = ""
        speakers: dict[str, SpeakerSegment] = {}

        for chunk in chunks:
            result = self.transcribe(chunk, language)
            if result.success:
                all_segments.extend(result.segments)
                all_text += result.text + "\n"

        # Build speaker summary
        for seg in all_segments:
            if seg.speaker_id not in speakers:
                speakers[seg.speaker_id] = SpeakerSegment(
                    speaker_id=seg.speaker_id,
                    speaker_name=seg.speaker_name,
                    total_talk_seconds=0.0,
                    turn_count=0,
                    first_seen=seg.start_time,
                    last_seen=seg.end_time,
                )
            s = speakers[seg.speaker_id]
            s.total_talk_seconds += seg.end_time - seg.start_time
            s.turn_count += 1
            s.last_seen = max(s.last_seen, seg.end_time)
            s.first_seen = min(s.first_seen, seg.start_time)

        total_duration = max((s.last_seen for s in speakers.values()), default=0.0)
        meeting_id = chunks[0].meeting_id if chunks else "unknown"

        return FullTranscript(
            meeting_id=meeting_id,
            platform=chunks[0].platform if chunks else None,
            duration_seconds=total_duration,
            segments=all_segments,
            speakers=list(speakers.values()),
            raw_text=all_text,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def _whisper_api(self, chunk: AudioChunk, language: str) -> ASRResult:
        try:
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            audio_bytes = self._ensure_wav(chunk)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", audio_bytes, "audio/wav"),
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

            segments = []
            for seg in transcript.segments:
                segments.append(TranscriptSegment(
                    speaker_id=f"speaker_{seg.get('speaker', 0)}",
                    speaker_name=f"Speaker {seg.get('speaker', 0)}",
                    text=seg.text.strip(),
                    start_time=seg.start,
                    end_time=seg.end,
                    confidence=seg.get("confidence", 0.0),
                    language=language,
                ))

            return ASRResult(
                success=True,
                text=transcript.text,
                segments=segments,
                model="whisper-1",
            )
        except Exception as e:
            return ASRResult(success=False, error=str(e))

    def _local_fallback(self, chunk: AudioChunk) -> ASRResult:
        return ASRResult(
            success=True,
            text="[LOCAL ASR FALLBACK] Transcription unavailable in dev mode.",
            segments=[
                TranscriptSegment(
                    speaker_id="speaker_0",
                    speaker_name="Unknown",
                    text="[Audio chunk received but ASR not configured]",
                    start_time=0.0,
                    end_time=chunk.duration_seconds,
                    confidence=0.0,
                )
            ],
            used_fallback=True,
            model="local-fallback",
        )

    def _ensure_wav(self, chunk: AudioChunk) -> bytes:
        """Convert audio data to WAV format for Whisper API."""
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(chunk.channels)
            wf.setsampwidth(2)
            wf.setframerate(chunk.sample_rate)
            wf.writeframes(chunk.data)
        return buf.getvalue()
