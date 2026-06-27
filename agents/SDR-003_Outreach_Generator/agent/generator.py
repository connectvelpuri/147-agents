import json
import re
import uuid
from datetime import datetime, timedelta
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope

from .models import (
    Prospect, PersonalizationLayer, Channel, OutreachStage,
    EmailDraft, LinkedInMessage, CallScript, SequenceStep,
    MultiChannelSequence, FollowUpVariant, Template,
    OUTREACH_TEMPLATES, CHANNEL_CONSTRAINTS, SEQUENCE_DESIGNS,
    TONES_BY_CHANNEL, estimate_personalization_depth,
)


AIDA_GUIDE = (
    "AIDA copywriting framework:\n"
    "  ATTENTION: Hook with a specific trigger, signal, or relevant pain point. "
    "Be specific, not generic. You have 6 seconds to earn this — make it count.\n"
    "  INTEREST: Build relevance with social proof, case studies, or data. "
    "Show understanding of their context. Use the Dual WIIFM: "
    "organizational value + personal value for the reader.\n"
    "  DESIRE: Paint a vision of the outcome. Frame the value in their terms. "
    "Use 'imagine if' or 'what if' framing. Leverage loss aversion: "
    "'what do you lose by waiting?' vs 'what do you gain?'\n"
    "  ACTION: Clear, low-friction next step. One CTA only. "
    "Make it easy to say yes. Remember: EASY = RIGHT (Jeff Shore). "
    "Every friction point reduces response probability by ~15%."
)

SKIP_MILLER_ATL_BTL = (
    "ATL (Above the Line) vs BTL (Below the Line) communication:\n"
    "  ATL = conscious, rational, direct. Use when prospect has explicit intent signals.\n"
    "  BTL = subconscious, emotional, indirect. Use when prospect is cold/unaware.\n"
    "  For cold outreach, lead BTL (story, question, observation) before going ATL.\n"
    "  Hot leads can handle ATL directly (problem → solution → CTA).\n"
    "  Match the communication style to the prospect's buying readiness."
)

GIVE_GET_HOMEWORK = (
    "Give-Get Framework: Every interaction must pass this test.\n"
    "  GIVE: What value am I bringing? (insight, data, perspective, case study)\n"
    "  GET: What am I walking away with? (reply, meeting, referral, commitment)\n"
    "  If you can't articulate both, the email isn't ready.\n"
    "  Rule: Give MORE than you Get — especially in the first 2 touches."
)

MOVIE_TRAILER = (
    "The Movie Trailer (Dale Merrill): Don't tell the whole story.\n"
    "  1. HOOK (30 words): The problem they feel but haven't named.\n"
    "  2. STAKES (30 words): The cost of NOT solving this.\n"
    "  3. TEASE (30 words): A glimpse of what's possible (not the full solution).\n"
    "  4. CTA (15 words): 'Want to see the full movie?' — not 'buy the ticket'.\n"
    "  Goal: Curiosity gap that demands closure (Zeigarnik Effect)."
)

ANTI_PITCH = (
    "Anti-Pitch Structure (Ashley Welch):\n"
    "  1. 'I have an observation about [their specific situation]'\n"
    "  2. 'Would you be open to 90 seconds on how we've helped similar companies?'\n"
    "  3. After permission: Brief relevant case study (one paragraph max)\n"
    "  4. 'Does that resonate with what you're seeing?'\n"
    "  Key: Ask permission before pitching. This triggers reciprocity + liking."
)

SIX_SIXTY_RULE = (
    "6/60 Rule: You have 6 seconds to earn attention, 60 seconds to earn time.\n"
    "  First 6 seconds (subject line/opener):\n"
    "    - Must be specific to THEM, not generic\n"
    "    - Creates a curiosity gap ('the one thing stopping X...')\n"
    "    - Looks like an internal email, not marketing\n"
    "  Next 60 seconds (body):\n"
    "    - State THEIR problem in THEIR words\n"
    "    - Imply the solution, don't explain it fully\n"
    "    - End with a question that requires a real answer\n"
    "  If you haven't earned attention by the first sentence, you've lost."
)

DUAL_WIIFM = (
    "Dual WIIFM (Andy Paul): Every email needs TWO value propositions.\n"
    "  1. Organizational WIIFM: What the company gains (revenue, efficiency, growth)\n"
    "  2. Personal WIIFM: What the INDIVIDUAL gains (promotion, recognition, less stress)\n"
    "  This is the single most underused B2B sales technique.\n"
    "  Most cold emails only address #1. The ones that work also address #2."
)

PSYCHOLOGICAL_BUCKETS = (
    "Gal Borenstein's Psychological Objection Buckets (pre-emptive):\n"
    "  SAFE: 'Will this get me fired?' → Mitigate with risk reversal, guarantees, case studies\n"
    "  BEST: 'Is this the right choice?' → Mitigate with comparative evidence, clear criteria\n"
    "  INNOVATIVE: 'Am I too early?' → Mitigate with peer adoption proof, market timing\n"
    "  For cold outreach, address the SAFE bucket pre-emptively in every email.\n"
    "  The unspoken question is always: 'What's the risk of engaging with you?'"
)

VALUE_EQUATION = (
    "Value = Progress (Andy Paul): Buyers don't buy products, they buy progress.\n"
    "  Every interaction must answer: 'How does this move me forward?'\n"
    "  Quantify the cost of inaction: 'Every month you delay costs $X'\n"
    "  The real competitor is always inertia/status quo, not another vendor.\n"
    "  Reference: Paul Butterfield's Discovery Gap — help them see the gap.\n"
    "  between current state and desired future state."
)

PERSUASION_PRINCIPLES = (
    "Use these persuasion principles naturally (never mechanically):\n"
    "  RECIPROCITY: Give value before asking for anything\n"
    "  SCARCITY: Limited availability creates desire\n"
    "  SOCIAL PROOF: 'Similar companies achieve X with this approach'\n"
    "  COMMITMENT: Start with a micro-commitment (reply → call → meeting)\n"
    "  LIKING: Mirror their language, show genuine understanding\n"
    "  LOSS AVERSION: 'What do you lose by waiting?' is 2x more powerful than 'What do you gain?'\n"
    "  CURIOSITY GAP: Tease the answer, don't give it (Zeigarnik Effect)\n"
    "  PEAK-END RULE: Make the strongest point early, close strong\n"
    "  ANCHORING: Frame the comparison before they do\n"
    "  PARADOX OF CHOICE: Never give more than 2-3 options"
)

SOCIAL_PROOF_MUTUAL = (
    "Social Proof on LinkedIn: Use these naturally.\n"
    "  - Mutual connection: 'We're both connected to X — they mentioned your work on Y'\n"
    "  - Their content: 'Your post on Z resonated — you made an interesting point about...'\n"
    "  - Shared context: Alumni, past company, same conferences\n"
    "  - Industry proof: 'I've been working with teams in [industry] on [problem]'\n"
    "  Never: 'I see you're connected to X' without a genuine reason why it matters."
)


CHANNEL_TONE_GUIDES = {
    Channel.EMAIL: (
        "Professional, peer-to-peer tone. Never vendor-to-prospect.\n"
        "Subject line under 60 chars — looks like internal email, not marketing.\n"
        "Body under 250 words. One link max.\n"
        "Personalize with specific company/role signals.\n"
        "Never start with 'I hope this email finds you well' — it signals template.\n"
        "Lead with THEIR world, not yours. First sentence is about them.\n"
        "Write like you're emailing a smart colleague at another company.\n"
        "Every sentence must either: create curiosity, establish relevance, "
        "build credibility, or drive to action. No filler.\n"
        "Dual WIIFM: organizational value + personal value for the reader.\n"
        "The personal WIIFM is what gets replies.\n"
        "Safe Choice pre-emption: address 'will this get me fired?' risk.\n"
        "Hard Truth: The buyer doesn't care about you. They care about their problem."
    ),
    Channel.LINKEDIN: (
        "Conversational, peer-to-peer tone.\n"
        "Connection requests: under 300 chars, end with a genuine reason to connect.\n"
        "InMails: under 2000 chars, more casual than email.\n"
        "Reference specific content or activity — shows you did the work.\n"
        "No hard sell on LinkedIn — build relationship first.\n"
        "Liking principle: find genuine common ground (alma mater, mutual connection, shared interest).\n"
        "Social Proof: mention mutual connections or their content you found valuable.\n"
        "Reciprocity: engage with their content before asking for their time.\n"
        "The goal is conversation, not conversion. First touch = 300 chars max."
    ),
    Channel.CALL: (
        "Conversational and confident.\n"
        "Opening must grab attention in under 15 seconds.\n"
        "State who you are, why you're calling (trigger-based), and ask a question.\n"
        "6/60 Rule: first 6 seconds must earn permission to continue.\n"
        "Anti-Pitch: 'I have an observation — would you be open to 90 seconds?'\n"
        "Prepare 2-3 discovery questions and 3 objection handlers.\n"
        "Movie Trailer: hook, stakes, tease, CTA — never the full story.\n"
        "End with a clear next step or meeting request.\n"
        "After delivering value, use Calibrated Absence: let silence create tension.\n"
        "The person who speaks first after a value moment loses negotiation power.\n"
        "Mirror their language patterns to build rapport (Mirror Neurons)."
    ),
}


PROSPECT_PERSONAS = {
    "ceo": {
        "priorities": ["revenue growth", "market share", "team scaling", "competitive advantage"],
        "tone": "strategic, concise",
        "length_preference": "short",
    },
    "vp_sales": {
        "priorities": ["quota attainment", "pipeline velocity", "rep productivity", "forecast accuracy"],
        "tone": "results-driven, peer-to-peer",
        "length_preference": "medium",
    },
    "director_marketing": {
        "priorities": ["lead quality", "campaign ROI", "attribution", "pipeline contribution"],
        "tone": "data-driven, collaborative",
        "length_preference": "medium",
    },
    "head_engineering": {
        "priorities": ["engineering velocity", "tech debt", "team growth", "product quality"],
        "tone": "direct, technical",
        "length_preference": "short",
    },
    "cfo": {
        "priorities": ["cost efficiency", "ROI", "forecast accuracy", "risk management"],
        "tone": "financial, risk-aware",
        "length_preference": "short",
    },
    "default": {
        "priorities": ["efficiency", "growth", "competitive edge", "team productivity"],
        "tone": "professional",
        "length_preference": "medium",
    },
}


class OutreachGenerator(RevenueAgent):
    def __init__(self, agent_id: str = "sdr-003-v1"):
        super().__init__(agent_id=agent_id)
        self._template_usage: dict[str, int] = {}
        self._sequences: dict[str, MultiChannelSequence] = {}
        self._variants: dict[str, list[FollowUpVariant]] = {}

    async def on_start(self):
        pass

    # --- public API ---

    def generate_email(
        self,
        prospect: Prospect,
        template_id: Optional[str] = None,
        stage: OutreachStage = OutreachStage.INITIAL,
        variant: str = "A",
        force_llm: bool = False,
    ) -> EmailDraft:
        templates = OUTREACH_TEMPLATES.get(Channel.EMAIL, [])
        if template_id:
            template = next((t for t in templates if t.template_id == template_id), templates[0])
        else:
            idx = min(len(templates) - 1, ["initial", "follow_up_1", "follow_up_2", "follow_up_3", "break_up"].index(stage.value) if stage.value in ["initial", "follow_up_1", "follow_up_2", "follow_up_3", "break_up"] else 0)
            template = templates[min(idx, len(templates) - 1)]

        depth = estimate_personalization_depth(prospect)

        if force_llm:
            return self._llm_generate_email(prospect, template, stage, depth, variant)

        return self._rule_generate_email(prospect, template, stage, depth, variant)

    def generate_linkedin_message(
        self,
        prospect: Prospect,
        message_type: str = "connection_request",
        template_id: Optional[str] = None,
        force_llm: bool = False,
    ) -> LinkedInMessage:
        templates = OUTREACH_TEMPLATES.get(Channel.LINKEDIN, [])
        if template_id:
            template = next((t for t in templates if t.template_id == template_id), templates[0])
        else:
            template = templates[0]

        depth = estimate_personalization_depth(prospect)

        if force_llm:
            return self._llm_generate_linkedin(prospect, template, message_type, depth)

        return self._rule_generate_linkedin(prospect, template, message_type, depth)

    def generate_call_script(
        self,
        prospect: Prospect,
        template_id: Optional[str] = None,
        force_llm: bool = False,
    ) -> CallScript:
        call_templates = OUTREACH_TEMPLATES.get(Channel.CALL, [])
        if template_id:
            template = next((t for t in call_templates if t.template_id == template_id), call_templates[0])
        else:
            template = call_templates[0]

        depth = estimate_personalization_depth(prospect)

        if force_llm:
            return self._llm_generate_call(prospect, template, depth)

        return self._rule_generate_call(prospect, template, depth)

    def design_sequence(
        self,
        prospect: Prospect,
        design_name: str = "standard_14day",
    ) -> MultiChannelSequence:
        design = SEQUENCE_DESIGNS.get(design_name, SEQUENCE_DESIGNS["standard_14day"])
        depth = estimate_personalization_depth(prospect)
        steps: list[SequenceStep] = []
        channels_used: set[Channel] = set()

        for day, channel, stage in design:
            channels_used.add(channel)
            if channel == Channel.EMAIL:
                content = self.generate_email(prospect, stage=stage)
            elif channel == Channel.LINKEDIN:
                content = self.generate_linkedin_message(prospect)
            elif channel == Channel.CALL:
                content = self.generate_call_script(prospect)
            else:
                continue

            condition = None
            if stage in (OutreachStage.FOLLOW_UP_1, OutreachStage.FOLLOW_UP_2, OutreachStage.FOLLOW_UP_3):
                condition = "if no reply"
            elif stage == OutreachStage.BREAK_UP:
                condition = "if no response after all prior touches"

            steps.append(SequenceStep(
                day=day,
                channel=channel,
                content=content,
                stage=stage,
                condition=condition,
            ))

        seq_id = f"seq_{uuid.uuid4().hex[:12]}"
        sequence = MultiChannelSequence(
            sequence_id=seq_id,
            prospect_id=prospect.contact_id,
            steps=steps,
            total_touches=len(steps),
            duration_days=design[-1][0],
            channels_used=list(channels_used),
            personalization_depth=depth,
            created_at=datetime.now(),
        )
        self._sequences[seq_id] = sequence
        return sequence

    def create_variant(
        self,
        base_sequence: MultiChannelSequence,
        variant_label: str = "B",
        changes: Optional[list[str]] = None,
    ) -> FollowUpVariant:
        if changes is None:
            changes = ["alternative subject line", "different CTA placement", "shortened body"]

        var_id = f"var_{uuid.uuid4().hex[:12]}"
        variant = FollowUpVariant(
            variant_id=var_id,
            base_sequence_id=base_sequence.sequence_id,
            variant_label=variant_label,
            changes=changes,
            expected_lift=0.10,
            created_at=datetime.now(),
        )

        if base_sequence.sequence_id not in self._variants:
            self._variants[base_sequence.sequence_id] = []
        self._variants[base_sequence.sequence_id].append(variant)
        return variant

    def enrich_with_llm(
        self,
        prospect: Prospect,
        message_type: str = "initial_outreach",
        context: Optional[str] = None,
    ) -> dict:
        try:
            persona = self._match_persona(prospect.title)
            depth = estimate_personalization_depth(prospect)

            prompt = (
                "You are a senior SDR crafting personalized B2B sales outreach.\n\n"
                f"Prospect: {prospect.name}, {prospect.title} at {prospect.company}\n"
                f"Industry: {prospect.industry} | Size: {prospect.company_size}\n"
                f"Personalization Depth: {depth.value}\n"
                f"Message Type: {message_type}\n"
                f"Persona: {persona['tone']}\n"
            )
            if prospect.recent_activity:
                prompt += f"Recent Activity: {'; '.join(prospect.recent_activity)}\n"
            if prospect.company_news:
                prompt += f"Company News: {'; '.join(prospect.company_news)}\n"
            if prospect.intent_signals:
                prompt += f"Intent Signals: {'; '.join(prospect.intent_signals)}\n"
            if context:
                prompt += f"\nAdditional Context:\n{context}\n"

            prompt += (
                f"\n=== COPYWRITING FRAMEWORKS ===\n"
                f"{AIDA_GUIDE}\n\n"
                f"{SKIP_MILLER_ATL_BTL}\n\n"
                f"{GIVE_GET_HOMEWORK}\n\n"
                f"{MOVIE_TRAILER}\n\n"
                f"{ANTI_PITCH}\n\n"
                f"{SIX_SIXTY_RULE}\n\n"
                f"{DUAL_WIIFM}\n\n"
                f"{PSYCHOLOGICAL_BUCKETS}\n\n"
                f"{VALUE_EQUATION}\n\n"
                f"{PERSUASION_PRINCIPLES}\n\n"
                f"Generate a {message_type} message for this prospect. "
                "Return JSON with keys: subject_line, body, cta, personalization_notes, "
                "channel_recommendation.\n"
                "Rules: Professional tone. No cliches. Specific > generic. "
                "One CTA only.\n"
                "Check every sentence: Does this serve the prospect or our ego?"
            )

            resp = self.llm.generate(prompt, max_tokens=800)
            result = self._parse_json(resp)
            if result:
                return result
            return self._fallback_enrichment(prospect, message_type)
        except Exception:
            return self._fallback_enrichment(prospect, message_type)

    def track_template_result(self, template_id: str, success: bool):
        key = f"{template_id}:{'won' if success else 'lost'}"
        self._template_usage[key] = self._template_usage.get(key, 0) + 1
        self._template_usage[template_id] = self._template_usage.get(template_id, 0) + 1

    def get_template_stats(self) -> dict:
        stats = {}
        for tid in set(k.split(":")[0] for k in self._template_usage):
            total = self._template_usage.get(tid, 0)
            won = self._template_usage.get(f"{tid}:won", 0)
            if total > 0:
                stats[tid] = {
                    "uses": total,
                    "successes": won,
                    "success_rate": round(won / total, 2),
                }
            else:
                stats[tid] = {"uses": 0, "successes": 0, "success_rate": 0.0}
        return stats

    # --- rule-based generation ---

    def _rule_generate_email(
        self,
        prospect: Prospect,
        template: Template,
        stage: OutreachStage,
        depth: PersonalizationLayer,
        variant: str,
    ) -> EmailDraft:
        subs = self._build_substitutions(prospect, depth)

        subject = template.subject_template or ""
        for k, v in subs.items():
            subject = subject.replace("{" + k + "}", v)

        body = template.body_template
        for k, v in subs.items():
            body = body.replace("{" + k + "}", v)

        body = body.replace("{signature}", self._signature())
        body = body.replace("{name_sender}", "Alex")
        body = body.replace("{company_sender}", "Revenue OS")

        cta = self._extract_cta(body)
        preview = body[:120].replace("\n", " ").strip()

        reply_rate_est = 0.08
        if depth == PersonalizationLayer.INDIVIDUAL:
            reply_rate_est = 0.15
        elif depth == PersonalizationLayer.ACCOUNT:
            reply_rate_est = 0.10

        return EmailDraft(
            subject=subject,
            body=body,
            preview_text=preview,
            cta=cta,
            personalization_depth=depth,
            template_id=template.template_id,
            variant=variant,
            character_count=len(body),
            estimated_open_rate=0.25,
            estimated_reply_rate=reply_rate_est,
        )

    def _rule_generate_linkedin(
        self,
        prospect: Prospect,
        template: Template,
        message_type: str,
        depth: PersonalizationLayer,
    ) -> LinkedInMessage:
        subs = self._build_substitutions(prospect, depth)

        body = template.body_template
        for k, v in subs.items():
            body = body.replace("{" + k + "}", v)

        if prospect.linkedin_url and "{personal_note}" in body and prospect.personal_notes:
            body = body.replace("{personal_note}", prospect.personal_notes[0])
        else:
            body = body.replace("{personal_note}", f"your work in {prospect.industry}")

        body = body.replace("{name_sender}", "Alex")
        body = body.replace("{company_sender}", "Revenue OS")

        resp_rate = 0.10 if depth == PersonalizationLayer.INDIVIDUAL else 0.05

        return LinkedInMessage(
            subject=template.subject_template,
            body=body,
            message_type=message_type,
            character_count=len(body),
            personalization_depth=depth,
            estimated_response_rate=resp_rate,
        )

    def _rule_generate_call(
        self,
        prospect: Prospect,
        template: Template,
        depth: PersonalizationLayer,
    ) -> CallScript:
        subs = self._build_substitutions(prospect, depth)
        opening = template.body_template
        for k, v in subs.items():
            opening = opening.replace("{" + k + "}", v)
        opening = opening.replace("{sender}", "Alex")
        opening = opening.replace("{company_sender}", "Revenue OS")

        persona = self._match_persona(prospect.title)
        top_p = persona["priorities"][:2]

        questions = [
            f"How are you currently approaching {top_p[0]}?",
            f"What's the biggest challenge with {top_p[1]} right now?",
            f"Have you looked at any solutions for this in the past year?",
        ]

        handlers = [
            ("We're happy with our current solution",
             "That's great to hear. What metrics are you tracking to measure its impact?"),
            ("Not interested right now",
             "I understand. What would make this a better time to revisit?"),
            ("Send me some information",
             "Happy to. What specific area would be most relevant for your team?"),
        ]

        estimated_dur = 180 if depth == PersonalizationLayer.SEGMENT else 300

        return CallScript(
            opening=opening,
            value_proposition=f"Helping {prospect.industry} companies improve {top_p[0]}",
            discovery_questions=questions,
            objection_handlers=handlers,
            closing="Let's set up 15 minutes next week. What works better — Tuesday or Thursday?",
            estimated_duration_seconds=estimated_dur,
            personalization_depth=depth,
        )

    # --- LLM generation (with fallback) ---

    def _llm_generate_email(
        self,
        prospect: Prospect,
        template: Template,
        stage: OutreachStage,
        depth: PersonalizationLayer,
        variant: str,
    ) -> EmailDraft:
        try:
            persona = self._match_persona(prospect.title)
            tone_guide = CHANNEL_TONE_GUIDES.get(Channel.EMAIL, "")
            aida_guide = AIDA_GUIDE

            prompt = (
                f"Generate a personalized B2B sales email.\n\n"
                f"TEMPLATE: {template.name} ({template.template_id})\n"
                f"STAGE: {stage.value}\n"
                f"VARIANT: {variant}\n\n"
                f"PROSPECT: {prospect.name}, {prospect.title} at {prospect.company}\n"
                f"INDUSTRY: {prospect.industry}\n"
                f"ROLE PRIORITIES: {', '.join(persona['priorities'])}\n"
                f"TONE: {persona['tone']}\n"
                f"PERSONALIZATION DEPTH: {depth.value}\n"
            )
            if prospect.recent_activity:
                prompt += f"RECENT ACTIVITY: {'; '.join(prospect.recent_activity)}\n"
            if prospect.intent_signals:
                prompt += f"INTENT SIGNALS: {'; '.join(prospect.intent_signals)}\n"
            if prospect.company_news:
                prompt += f"COMPANY NEWS: {'; '.join(prospect.company_news)}\n"
            if prospect.personal_notes:
                prompt += f"PERSONAL NOTES: {'; '.join(prospect.personal_notes)}\n"

            prompt += (
                f"\n=== COPYWRITING FRAMEWORKS ===\n"
                f"{aida_guide}\n\n"
                f"{GIVE_GET_HOMEWORK}\n\n"
                f"{MOVIE_TRAILER}\n\n"
                f"{ANTI_PITCH}\n\n"
                f"{SIX_SIXTY_RULE}\n\n"
                f"{DUAL_WIIFM}\n\n"
                f"{PSYCHOLOGICAL_BUCKETS}\n\n"
                f"{VALUE_EQUATION}\n\n"
                f"{PERSUASION_PRINCIPLES}\n\n"
                f"=== CHANNEL TONE ===\n"
                f"{tone_guide}\n\n"
                "Return JSON with keys: subject, body, preview_text, cta.\n"
                "Rules: No cliches. Specific > generic. One CTA. "
                "Subject under 60 chars. Body under 250 words.\n"
                "BRUTAL TRUTH: Most cold emails get ignored because they're about the sender, "
                "not the receiver. Check every sentence: does this serve the prospect or our ego? "
                "The buyer doesn't care about you. They care about their problem."
            )

            resp = self.llm.generate(prompt, max_tokens=600)
            parsed = self._parse_json(resp)
            if parsed and "subject" in parsed:
                return EmailDraft(
                    subject=parsed["subject"][:60],
                    body=parsed.get("body", ""),
                    preview_text=parsed.get("preview_text", "")[:150],
                    cta=parsed.get("cta", ""),
                    personalization_depth=depth,
                    template_id=template.template_id,
                    variant=variant,
                    character_count=len(parsed.get("body", "")),
                    estimated_open_rate=0.30,
                    estimated_reply_rate=0.12,
                )
        except Exception:
            pass

        return self._rule_generate_email(prospect, template, stage, depth, variant)

    def _llm_generate_linkedin(
        self,
        prospect: Prospect,
        template: Template,
        message_type: str,
        depth: PersonalizationLayer,
    ) -> LinkedInMessage:
        try:
            tone_guide = CHANNEL_TONE_GUIDES.get(Channel.LINKEDIN, "")
            prompt = (
                f"Generate a LinkedIn {message_type} message.\n\n"
                f"PROSPECT: {prospect.name}, {prospect.title} at {prospect.company}\n"
                f"INDUSTRY: {prospect.industry}\n"
            )
            if prospect.recent_activity:
                prompt += f"RECENT ACTIVITY: {'; '.join(prospect.recent_activity)}\n"
            if prospect.personal_notes:
                prompt += f"PERSONAL NOTES: {'; '.join(prospect.personal_notes)}\n"

            prompt += (
                f"\n=== FRAMEWORKS ===\n"
                f"{SKIP_MILLER_ATL_BTL}\n\n"
                f"On LinkedIn, you're always BTL (below the line). "
                f"Emotional, indirect, relationship-first.\n\n"
                f"{GIVE_GET_HOMEWORK}\n\n"
                f"For connection requests, use the MOVIE TRAILER:\n"
                f"  HOOK: What caught your eye about them\n"
                f"  STAKES: Why they should care (briefly)\n"
                f"  TEASE: What's possible\n"
                f"  CTA: Accept the invite — that's it\n\n"
                f"{SOCIAL_PROOF_MUTUAL}:\n"
                f"  - Mention mutual connections\n"
                f"  - Reference their content\n"
                f"  - Show you did the homework\n\n"
                f"=== CHANNEL TONE ===\n"
                f"{tone_guide}\n\n"
                "Return JSON with keys: subject (or null), body, message_type.\n"
                "Connection request under 300 chars. InMail under 2000. "
                "No hard sell. First touch = conversation, not conversion."
            )

            resp = self.llm.generate(prompt, max_tokens=500)
            parsed = self._parse_json(resp)
            if parsed and "body" in parsed:
                return LinkedInMessage(
                    subject=parsed.get("subject"),
                    body=parsed["body"],
                    message_type=message_type,
                    character_count=len(parsed["body"]),
                    personalization_depth=depth,
                    estimated_response_rate=0.12,
                )
        except Exception:
            pass

        return self._rule_generate_linkedin(prospect, template, message_type, depth)

    def _llm_generate_call(
        self,
        prospect: Prospect,
        template: Template,
        depth: PersonalizationLayer,
    ) -> CallScript:
        try:
            persona = self._match_persona(prospect.title)
            tone_guide = CHANNEL_TONE_GUIDES.get(Channel.CALL, "")
            prompt = (
                f"Generate a call script for B2B outbound.\n\n"
                f"PROSPECT: {prospect.name}, {prospect.title} at {prospect.company}\n"
                f"INDUSTRY: {prospect.industry}\n"
                f"PRIORITIES: {', '.join(persona['priorities'])}\n"
            )
            if prospect.intent_signals:
                prompt += f"TRIGGER: {'; '.join(prospect.intent_signals)}\n"

            prompt += (
                f"\n=== FRAMEWORKS ===\n"
                f"{ANTI_PITCH}\n\n"
                f"{MOVIE_TRAILER}\n\n"
                f"{VALUE_EQUATION}\n\n"
                f"{PSYCHOLOGICAL_BUCKETS}\n\n"
                f"Objection handling: Map each objection to Gal Borenstein's buckets:\n"
                f"  - SAFE objection: 'I'm happy with current solution' → Use risk reversal, "
                f"'What would be the cost of finding out you're missing something?'\n"
                f"  - BEST objection: 'Send me info' → 'I'd rather show you in 5 min — "
                f"what specifically matters most?'\n"
                f"  - INNOVATIVE objection: 'Too early' → Peer adoption proof, market timing\n\n"
                f"Jeff Shore CBT (Cognitive Behavioral Technique) for objections:\n"
                f"  1. Validate the feeling: 'That makes sense given what you know'\n"
                f"  2. Reframe the narrative: 'What if the risk is actually staying put?'\n"
                f"  3. Replace: 'Here's what other leaders in your position found'\n\n"
                f"5 Fears (Andy Paul) that block buyer action:\n"
                f"  1. FEAR OF MISTAKE: 'I don't want to make the wrong choice'\n"
                f"  2. FEAR OF CHANGE: 'The current system works (well enough)'\n"
                f"  3. FEAR OF LOSING CREDIBILITY: 'What if this makes me look bad?'\n"
                f"  4. FEAR OF COMMITMENT: 'What if something better comes along?'\n"
                f"  5. FEAR OF THE UNKNOWN: 'I don't have enough information'\n"
                f"  Address the relevant fear BEFORE they voice it.\n\n"
                f"=== CHANNEL TONE ===\n"
                f"{tone_guide}\n\n"
                "Return JSON with keys: opening, value_proposition, "
                "discovery_questions (list), objection_handlers (list of [objection, response]), "
                "closing.\n"
                "Opening under 15 seconds. Max 3 questions."
            )

            resp = self.llm.generate(prompt, max_tokens=600)
            parsed = self._parse_json(resp)
            if parsed and "opening" in parsed:
                handlers = [
                    (h[0], h[1]) if isinstance(h, list) else ("", "")
                    for h in parsed.get("objection_handlers", [["", ""]])
                ]
                return CallScript(
                    opening=parsed["opening"],
                    value_proposition=parsed.get("value_proposition", ""),
                    discovery_questions=parsed.get("discovery_questions", []),
                    objection_handlers=handlers[:3],
                    closing=parsed.get("closing", ""),
                    personalization_depth=depth,
                )
        except Exception:
            pass

        return self._rule_generate_call(prospect, template, depth)

    # --- helpers ---

    def _build_substitutions(
        self, prospect: Prospect, depth: PersonalizationLayer
    ) -> dict[str, str]:
        subs = {
            "name": prospect.name,
            "title": prospect.title,
            "company": prospect.company,
            "industry": prospect.industry,
            "company_size": prospect.company_size,
        }

        if prospect.company_news and depth in (PersonalizationLayer.ACCOUNT, PersonalizationLayer.INDIVIDUAL):
            subs["trigger"] = prospect.company_news[0][:80]
        elif prospect.intent_signals:
            subs["trigger"] = prospect.intent_signals[0][:80]
        else:
            subs["trigger"] = f"your growth in {prospect.industry}"

        if prospect.industry.lower() in ("saas", "technology", "software"):
            subs["topic"] = "revenue growth"
            subs["value_prop"] = "increase pipeline velocity by 40%"
            subs["result"] = "40% pipeline growth in 90 days"
            subs["similar_company"] = "a Series B SaaS company"
            subs["social_proof"] = "They went from $2M to $3.5M pipeline in one quarter"
            subs["social_proof_intro"] = "A company similar to yours recently achieved 40% pipeline growth"
        elif prospect.industry.lower() in ("healthcare", "medical", "pharma"):
            subs["topic"] = "patient acquisition"
            subs["value_prop"] = "accelerate patient referrals by 30%"
            subs["result"] = "30% referral growth in 60 days"
            subs["similar_company"] = "a mid-market healthcare provider"
            subs["social_proof"] = "They added 150+ new patients in the first month"
            subs["social_proof_intro"] = "A healthcare provider recently grew referrals 30%"
        elif prospect.industry.lower() in ("finance", "banking", "fintech"):
            subs["topic"] = "deal flow"
            subs["value_prop"] = "increase qualified lead volume by 35%"
            subs["result"] = "35% pipeline increase in one quarter"
            subs["similar_company"] = "a fintech company your size"
            subs["social_proof"] = "They closed 12 new enterprise accounts last quarter"
            subs["social_proof_intro"] = "A fintech company your size recently scaled pipeline 35%"
        else:
            subs["topic"] = "growth"
            subs["value_prop"] = "accelerate revenue"
            subs["result"] = "measurable pipeline growth"
            subs["similar_company"] = "a company in your space"
            subs["social_proof"] = "Achieved 2x pipeline in the first quarter"
            subs["social_proof_intro"] = f"A {prospect.industry} company recently achieved strong results"

        subs["context"] = f"your focus on {subs['topic']}"

        if prospect.recent_activity and depth == PersonalizationLayer.INDIVIDUAL:
            subs["insight"] = f"based on your recent work on {prospect.recent_activity[0][:60]}"
        else:
            subs["insight"] = f"a more strategic approach to {subs['topic']}"

        return subs

    def _match_persona(self, title: str) -> dict:
        title_lower = title.lower()
        if any(t in title_lower for t in ("ceo", "chief", "founder", "owner")):
            return PROSPECT_PERSONAS["ceo"]
        if any(t in title_lower for t in ("vp of sales", "vp sales", "head of sales", "sales director", "cro")):
            return PROSPECT_PERSONAS["vp_sales"]
        if any(t in title_lower for t in ("marketing", "demand gen", "growth")):
            return PROSPECT_PERSONAS["director_marketing"]
        if any(t in title_lower for t in ("engineer", "cto", "vp engineering", "head of engineering", "tech lead")):
            return PROSPECT_PERSONAS["head_engineering"]
        if any(t in title_lower for t in ("cfo", "finance", "controller")):
            return PROSPECT_PERSONAS["cfo"]
        return PROSPECT_PERSONAS["default"]

    def _extract_cta(self, body: str) -> str:
        lines = body.strip().split("\n")
        for line in reversed(lines):
            clean = line.strip().lower()
            if any(w in clean for w in ("call", "chat", "meeting", "talk", "discuss", "hop on", "15 minutes", "30 min")):
                return line.strip()[:80]
        return "Open to a quick chat?"

    def _signature(self) -> str:
        return "Best,\nAlex\nRevenue OS"

    def _parse_json(self, text: str) -> Optional[dict]:
        try:
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except (json.JSONDecodeError, AttributeError):
            return None

    def _fallback_enrichment(self, prospect: Prospect, message_type: str) -> dict:
        persona = self._match_persona(prospect.title)
        return {
            "subject_line": f"Quick thought on {prospect.company}'s growth",
            "body": f"Hi {prospect.name}, noticed your work at {prospect.company}. "
                    f"Would love to connect.",
            "cta": "Open to a 15-minute chat?",
            "personalization_notes": f"Suggest {persona['tone']} tone targeting "
                                    f"{persona['priorities'][0]}",
            "channel_recommendation": "email",
        }
