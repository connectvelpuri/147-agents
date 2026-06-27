from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class PersonalizationLayer(str, Enum):
    SEGMENT = "segment"    # industry, role, company size
    ACCOUNT = "account"    # company initiatives, news, funding
    INDIVIDUAL = "individual"  # recent post, blog, activity


class Channel(str, Enum):
    EMAIL = "email"
    LINKEDIN = "linkedin"
    CALL = "call"


class OutreachStage(str, Enum):
    INITIAL = "initial"
    FOLLOW_UP_1 = "follow_up_1"
    FOLLOW_UP_2 = "follow_up_2"
    FOLLOW_UP_3 = "follow_up_3"
    BREAK_UP = "break_up"


@dataclass
class Prospect:
    contact_id: str
    name: str
    title: str
    company: str
    industry: str
    company_size: str  # 1-10, 11-50, 51-200, 201-1000, 1000+
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    recent_activity: list[str] = field(default_factory=list)
    company_news: list[str] = field(default_factory=list)
    intent_signals: list[str] = field(default_factory=list)
    personal_notes: list[str] = field(default_factory=list)
    custom_fields: dict = field(default_factory=dict)


@dataclass
class EmailDraft:
    subject: str
    body: str
    preview_text: str
    cta: str
    personalization_depth: PersonalizationLayer
    template_id: str
    variant: str = "A"
    tone: str = "professional"
    character_count: int = 0
    estimated_open_rate: float = 0.0
    estimated_reply_rate: float = 0.0


@dataclass
class LinkedInMessage:
    subject: Optional[str]
    body: str
    message_type: str  # connection_request, inmail, follow_up
    character_count: int = 0
    personalization_depth: PersonalizationLayer = PersonalizationLayer.SEGMENT
    estimated_response_rate: float = 0.0


@dataclass
class CallScript:
    opening: str
    value_proposition: str
    discovery_questions: list[str]
    objection_handlers: list[tuple[str, str]]
    closing: str
    estimated_duration_seconds: int = 300
    personalization_depth: PersonalizationLayer = PersonalizationLayer.ACCOUNT


@dataclass
class SequenceStep:
    day: int
    channel: Channel
    content: EmailDraft | LinkedInMessage | CallScript
    stage: OutreachStage
    condition: Optional[str] = None  # e.g. "if no reply"


@dataclass
class MultiChannelSequence:
    sequence_id: str
    prospect_id: str
    steps: list[SequenceStep]
    total_touches: int
    duration_days: int
    channels_used: list[Channel]
    personalization_depth: PersonalizationLayer
    created_at: datetime
    metadata: dict = field(default_factory=dict)


@dataclass
class FollowUpVariant:
    variant_id: str
    base_sequence_id: str
    variant_label: str  # A, B, C
    changes: list[str]
    expected_lift: float  # expected improvement vs baseline
    created_at: datetime


@dataclass
class Template:
    template_id: str
    channel: Channel
    name: str
    subject_template: Optional[str]
    body_template: str
    personalization_hints: list[str]
    target_layer: PersonalizationLayer
    industry: Optional[str] = None
    role: Optional[str] = None
    aida_stage: str = "attention"  # attention, interest, desire, action
    success_rate: float = 0.0
    use_count: int = 0


OUTREACH_TEMPLATES: dict[Channel, list[Template]] = {
    Channel.EMAIL: [
        Template(
            "email_trigger_1", Channel.EMAIL, "Trigger-based intro",
            "Quick question about {company}'s {topic}",
            "Hi {name},\n\n"
            "Noticed {trigger}. "
            "We help {industry} companies like you achieve {value_prop}.\n\n"
            "Worth 10 minutes this week?\n\n{signature}",
            ["{trigger}", "{topic}", "{value_prop}"],
            PersonalizationLayer.ACCOUNT, aida_stage="attention",
        ),
        Template(
            "email_value_1", Channel.EMAIL, "Value prop follow-up",
            "Idea for {company}",
            "Hi {name},\n\n"
            "Following up on my last note. "
            "Here's how {similar_company} achieved {result} using our approach.\n\n"
            "{social_proof}\n\n"
            "Open to a quick call?\n\n{signature}",
            ["{similar_company}", "{result}", "{social_proof}"],
            PersonalizationLayer.SEGMENT, aida_stage="interest",
        ),
        Template(
            "email_social_1", Channel.EMAIL, "Social proof",
            "What {similar_company} did — and why it matters for {company}",
            "Hi {name},\n\n"
            "{social_proof_intro}\n\n"
            "Thought you might find this relevant given {context}.\n\n"
            "Happy to share more specifics.\n\n{signature}",
            ["{similar_company}", "{social_proof_intro}", "{context}"],
            PersonalizationLayer.ACCOUNT, aida_stage="desire",
        ),
        Template(
            "email_breakup_1", Channel.EMAIL, "Break-up / final",
            "Closing the loop",
            "Hi {name},\n\n"
            "I know you're busy. I'll stop reaching out for now.\n\n"
            "If {topic} becomes a priority down the line, "
            "feel free to ping me.\n\n"
            "Best,\n{signature}",
            ["{topic}"],
            PersonalizationLayer.SEGMENT, aida_stage="action",
        ),
    ],
    Channel.LINKEDIN: [
        Template(
            "li_connect_1", Channel.LINKEDIN, "Connection request",
            None,
            "Hi {name}, I came across your work at {company} "
            "and was impressed by {personal_note}. "
            "Would love to connect.",
            ["{personal_note}", "{company}"],
            PersonalizationLayer.INDIVIDUAL,
        ),
        Template(
            "li_inmail_1", Channel.LINKEDIN, "InMail follow-up",
            "Quick thought on {topic}",
            "Hi {name},\n\n"
            "Saw that {trigger}. "
            "Many {industry} leaders are approaching this by {insight}.\n\n"
            "Would you be open to a brief chat?\n\n"
            "Best,\n{name_sender}",
            ["{trigger}", "{insight}", "{industry}"],
            PersonalizationLayer.ACCOUNT,
        ),
        Template(
            "li_content_1", Channel.LINKEDIN, "Content share",
            None,
            "Hi {name}, thought you might find this relevant given "
            "your focus on {topic}. Shared this with a few "
            "{industry} leaders recently.",
            ["{topic}", "{industry}"],
            PersonalizationLayer.SEGMENT,
        ),
    ],
    Channel.CALL: [
        Template(
            "call_trigger_1", Channel.CALL, "Trigger-based opening",
            None,
            "Hi {name}, this is {sender} from {company_sender}. "
            "I saw that {trigger} and wanted to reach out. "
            "We've been helping {industry} companies with {value_prop}. "
            "Got 30 seconds?",
            ["{trigger}", "{value_prop}"],
            PersonalizationLayer.ACCOUNT,
        ),
        Template(
            "call_follow_1", Channel.CALL, "Follow-up call",
            None,
            "Hi {name}, {sender} again. I sent over an email about "
            "{topic} last week. Curious if you had a chance to review. "
            "Happy to answer any questions.",
            ["{topic}"],
            PersonalizationLayer.SEGMENT,
        ),
    ],
}


CHANNEL_CONSTRAINTS = {
    Channel.EMAIL: {
        "subject_max": 60,
        "body_max": 250,
        "max_links": 2,
        "tone": "professional",
    },
    Channel.LINKEDIN: {
        "connection_request_max": 300,
        "inmail_max": 2000,
        "tone": "conversational",
    },
    Channel.CALL: {
        "opening_max_seconds": 15,
        "max_objections": 3,
        "tone": "conversational",
    },
}


TONES_BY_CHANNEL = {
    Channel.EMAIL: ["professional", "casual", "direct", "consultative"],
    Channel.LINKEDIN: ["conversational", "professional", "friendly"],
    Channel.CALL: ["conversational", "direct", "consultative"],
}


SEQUENCE_DESIGNS = {
    "standard_14day": [
        (1, Channel.EMAIL, OutreachStage.INITIAL),
        (3, Channel.LINKEDIN, OutreachStage.FOLLOW_UP_1),
        (5, Channel.CALL, OutreachStage.FOLLOW_UP_1),
        (7, Channel.EMAIL, OutreachStage.FOLLOW_UP_2),
        (10, Channel.LINKEDIN, OutreachStage.FOLLOW_UP_2),
        (14, Channel.EMAIL, OutreachStage.BREAK_UP),
    ],
    "intensive_7day": [
        (1, Channel.EMAIL, OutreachStage.INITIAL),
        (2, Channel.LINKEDIN, OutreachStage.FOLLOW_UP_1),
        (3, Channel.CALL, OutreachStage.FOLLOW_UP_1),
        (4, Channel.EMAIL, OutreachStage.FOLLOW_UP_2),
        (5, Channel.LINKEDIN, OutreachStage.FOLLOW_UP_2),
        (7, Channel.EMAIL, OutreachStage.BREAK_UP),
    ],
    "li_first_10day": [
        (1, Channel.LINKEDIN, OutreachStage.INITIAL),
        (3, Channel.EMAIL, OutreachStage.FOLLOW_UP_1),
        (5, Channel.LINKEDIN, OutreachStage.FOLLOW_UP_2),
        (7, Channel.CALL, OutreachStage.FOLLOW_UP_2),
        (10, Channel.EMAIL, OutreachStage.BREAK_UP),
    ],
}


def estimate_personalization_depth(
    prospect: Prospect,
) -> PersonalizationLayer:
    if prospect.recent_activity or prospect.personal_notes:
        return PersonalizationLayer.INDIVIDUAL
    if prospect.intent_signals or prospect.company_news:
        return PersonalizationLayer.ACCOUNT
    return PersonalizationLayer.SEGMENT
