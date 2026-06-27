"""Data models for MO-001 Meeting Observer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class MeetingPlatform(Enum):
    ZOOM = "zoom"
    GOOGLE_MEET = "google_meet"
    TEAMS = "teams"
    WEBEX = "webex"
    GENERIC = "generic"


class AudioFormat(Enum):
    PCM16 = "pcm16"
    OPUS = "opus"
    AAC = "aac"
    MP4 = "mp4"
    WEBM = "webm"


@dataclass
class AudioChunk:
    meeting_id: str
    chunk_index: int
    platform: MeetingPlatform
    format: AudioFormat
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    duration_seconds: float = 0.0
    received_at: str = ""


@dataclass
class TranscriptSegment:
    speaker_id: str
    speaker_name: str
    text: str
    start_time: float
    end_time: float
    confidence: float = 0.0
    language: str = "en"


@dataclass
class TranscriptChunk:
    meeting_id: str
    chunk_index: int
    segments: list[TranscriptSegment]
    timestamp: str = ""


@dataclass
class SpeakerSegment:
    speaker_id: str
    speaker_name: str
    total_talk_seconds: float
    turn_count: int
    first_seen: float
    last_seen: float


@dataclass
class FullTranscript:
    meeting_id: str
    platform: MeetingPlatform
    duration_seconds: float
    segments: list[TranscriptSegment]
    speakers: list[SpeakerSegment]
    word_error_rate: float = 0.0
    diarization_accuracy: float = 0.0
    created_at: str = ""
    raw_text: str = ""


@dataclass
class MeetingMetadata:
    meeting_id: str
    platform: MeetingPlatform
    duration_seconds: float
    participant_count: int
    participants: list[str]
    started_at: str
    ended_at: str
    title: str = ""


@dataclass
class ASRResult:
    success: bool
    text: str = ""
    segments: list[TranscriptSegment] = field(default_factory=list)
    error: str = ""
    used_fallback: bool = False
    model: str = "whisper-1"
