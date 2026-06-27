"""Data models for MO-002 Sentiment and Emotion Analyst."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class NeurosciencePrinciple(Enum):
    COGNITIVE_DISSONANCE = "cognitive_dissonance"
    LOSS_AVERSION = "loss_aversion"
    SOCIAL_PROOF_SEEKING = "social_proof_seeking"
    ANCHORING = "anchoring"
    STATUS_QUO_BIAS = "status_quo_bias"
    REACTANCE = "reactance"
    EMOTIONAL_CONTAGION = "emotional_contagion"
    PROSPECT_THEORY = "prospect_theory"
    ZEIGARNIK_EFFECT = "zeigarnik_effect"
    PEAK_END_RULE = "peak_end_rule"


class SentimentLabel(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class EmotionType(Enum):
    EXCITEMENT = "excitement"
    FRUSTRATION = "frustration"
    CONFUSION = "confusion"
    SKEPTICISM = "skepticism"
    SATISFACTION = "satisfaction"
    DISAPPOINTMENT = "disappointment"
    URGENCY = "urgency"
    INTEREST = "interest"
    BOREDOM = "boredom"
    TRUST = "trust"
    SURPRISE = "surprise"
    AGREEMENT = "agreement"


class SentimentTrend(Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class SentimentPoint:
    participant_id: str
    timestamp_sec: float
    sentiment: SentimentLabel
    emotions: list[EmotionType] = field(default_factory=list)
    intensity: float = 0.5
    confidence: float = 0.7
    utterance_snippet: str = ""


@dataclass
class ParticipantSentimentTimeline:
    participant_id: str
    points: list[SentimentPoint] = field(default_factory=list)
    overall_sentiment: SentimentLabel = SentimentLabel.NEUTRAL
    trend: SentimentTrend = SentimentTrend.STABLE
    volatility: float = 0.0
    dominant_emotions: list[EmotionType] = field(default_factory=list)
    neuroscience_signals: list[str] = field(default_factory=list)


@dataclass
class EmotionHighlight:
    participant_id: str
    timestamp_sec: float
    emotion: EmotionType
    intensity: float
    context: str
    utterance: str = ""
    neuroscience_principle: str = ""


@dataclass
class EngagementScore:
    participant_id: str
    score: float
    trend: SentimentTrend
    speaking_percentage: float = 0.0
    signal_quality: str = ""


@dataclass
class FrustrationAlert:
    participant_id: str
    intensity: float
    context: str
    timestamp_sec: float
    utterance: str = ""


@dataclass
class ConfusionMarker:
    participant_id: str
    timestamp_sec: float
    context: str
    trigger_phrase: str = ""
    resolved_later: bool = False


@dataclass
class SentimentAnalysisResult:
    deal_id: str
    meeting_id: str
    timelines: list[ParticipantSentimentTimeline] = field(default_factory=list)
    highlights: list[EmotionHighlight] = field(default_factory=list)
    engagement_scores: list[EngagementScore] = field(default_factory=list)
    frustration_alerts: list[FrustrationAlert] = field(default_factory=list)
    confusion_markers: list[ConfusionMarker] = field(default_factory=list)
    overall_meeting_sentiment: SentimentLabel = SentimentLabel.NEUTRAL
    analyzed_at: str = ""
