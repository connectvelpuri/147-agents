import json
import hashlib
import uuid
import re
from datetime import datetime, timedelta
from typing import Optional

from agent_base.agent_base import RevenueAgent
from agent_base.event_envelope import EventEnvelope
from .models import (
    IntentSignal, SignalType, SignalSource, SignalStrength, BuyingReadiness,
    OutreachTrigger, SignalAggregation, IntentTrend,
    ATL_BTL, IntentLevel,
    ATL_SIGNAL_TYPES, BTL_SIGNAL_TYPES, INTENT_STACK_THRESHOLDS,
    SIGNAL_WEIGHTS, SIGNAL_CONFIDENCE_BY_SOURCE, classify_strength,
)


SIGNAL_KEYWORDS = {
    SignalType.JOB_CHANGE: [
        "joined", "hired", "promoted", "appointed", "named", "new role",
        "new position", "left", "departed", "resigned", "onboarding",
    ],
    SignalType.FUNDING: [
        "raised", "series", "funding", "investment", "acquired", "acquisition",
        "IPO", "went public", "valuation", "seed round", "venture",
    ],
    SignalType.TECHNOLOGY: [
        "migrated to", "implemented", "deployed", "adopted", "switched to",
        "integrated", "upgraded to", "standardized on", "new tech stack",
    ],
    SignalType.COMPETITOR: [
        "evaluating", "comparing", "considering", "reviewing alternatives",
        "proof of concept", "POC", "trial with", "rfi", "rfp",
        "request for proposal",
    ],
    SignalType.PUBLISHING: [
        "case study", "whitepaper", "research report", "benchmark",
        "industry analysis", "report", "webinar", "ebook",
    ],
    SignalType.EVENT: [
        "conference", "summit", "expo", "trade show", "attend",
        "sponsor", "exhibit",
    ],
    SignalType.CONTENT: [
        "pricing page", "demo request", "free trial", "started trial",
        "product tour", "documentation", "api docs", "pricing",
    ],
}

SIGNAL_TOPICS = {
    "crm": ["crm", "salesforce", "hubspot", "sales pipeline", "lead management"],
    "analytics": ["analytics", "data warehouse", "bi tool", "dashboard", "reporting"],
    "security": ["security", "compliance", "vulnerability", "cybersecurity", "encryption"],
    "infrastructure": ["cloud", "kubernetes", "aws", "azure", "gcp", "devops"],
    "hr": ["hiring", "recruiting", "hr tech", "workforce", "payroll"],
    "finance": ["erp", "accounting", "finance", "budgeting", "forecasting"],
    "support": ["helpdesk", "customer support", "ticketing", "support"],
    "marketing": ["marketing automation", "email marketing", "abm", "lead gen"],
    "ai": ["ai", "machine learning", "llm", "artificial intelligence", "generative"],
}


INTENT_SOURCE_FEEDS = {
    SignalSource.CRUNCHBASE: [
        "https://feeds.feedburner.com/crunchbase",
        "https://news.crunchbase.com/feed/",
    ],
    SignalSource.NEWS: [
        "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB",
        "https://feeds.bloomberg.com/markets/news.rss",
    ],
    SignalSource.RSS: [
        "https://www.g2.com/blog/feed",
        "https://blog.hubspot.com/sales/rss.xml",
    ],
}


class IntentMonitor(RevenueAgent):
    def __init__(self, agent_id: str = "sdr-002-v1", env: str = "dev"):
        super().__init__(agent_id=agent_id)
        self.signal_history: dict[str, list[IntentSignal]] = {}
        self.scan_cooldown: dict[str, datetime] = {}
        self.min_scan_interval = timedelta(hours=6)
        self._env = env

    async def on_start(self):
        pass

    def _get_llm_client(self, tier: str = "moderate"):
        from agent_base.llm_client import LLMClient
        return LLMClient(tier=tier)

    # --- public API ---

    def scan_all_sources(
        self,
        deal_id: str,
        account: Optional[dict] = None,
        now: Optional[datetime] = None,
    ) -> BuyingReadiness:
        if now is None:
            now = datetime.now()

        if account is None:
            account = {"name": f"Account-{deal_id}", "domain": f"{deal_id}.com"}

        signals = []

        rule_signals = self._rule_based_scan(deal_id, account, now)
        signals.extend(rule_signals)

        history = self.signal_history.get(deal_id, [])
        active = [s for s in history if s.age_days(now) <= 90]
        active.extend(signals)
        self._deduplicate(active)

        deduped = self._deduplicate(active)
        self.signal_history[deal_id] = deduped

        readiness = BuyingReadiness.from_signals(deal_id, deduped, now)
        return readiness

    def scan_single_source(
        self,
        deal_id: str,
        source: SignalSource,
        account: dict,
        now: Optional[datetime] = None,
    ) -> list[IntentSignal]:
        if now is None:
            now = datetime.now()
        return self._scan_source(deal_id, account, source, now)

    def detect_trend(
        self,
        topic: str,
        days_back: int = 30,
        now: Optional[datetime] = None,
    ) -> IntentTrend:
        if now is None:
            now = datetime.now()

        cutoff = now - timedelta(days=days_back)
        prior_cutoff = cutoff - timedelta(days=days_back)

        current = []
        prior = []
        for sig_list in self.signal_history.values():
            for s in sig_list:
                if s.topic and topic.lower() in s.topic.lower():
                    if s.timestamp >= cutoff:
                        current.append(s)
                    elif s.timestamp >= prior_cutoff:
                        prior.append(s)

        rate = len(current) / max(len(prior), 1)
        growth = ((rate - 1) * 100) if len(prior) > 0 else (100 if current else 0)
        growth = round(growth, 1)

        accounts = list(set(s.account_id or "unknown" for s in current))

        if growth >= 100:
            sev = "critical"
            rec = f"Sudden spike in intent signals around '{topic}'. Investigate immediately."
        elif growth >= 30:
            sev = "elevated"
            rec = f"Increased intent signals around '{topic}'. Monitor closely for acceleration."
        else:
            sev = "normal"
            rec = f"Normal intent signal level for '{topic}'. No action needed."

        return IntentTrend(
            trend_id=f"trend_{uuid.uuid4().hex[:12]}",
            topic=topic,
            signal_count=len(current),
            period_days=days_back,
            growth_rate=growth,
            accounts_affected=accounts,
            severity=sev,
            recommendation=rec,
            detected_at=now,
        )

    def aggregate(
        self,
        period: str = "weekly",
        now: Optional[datetime] = None,
        min_score: float = 0.0,
    ) -> SignalAggregation:
        if now is None:
            now = datetime.now()

        if period == "daily":
            cutoff = now - timedelta(days=1)
        else:
            cutoff = now - timedelta(days=7)

        all_signals = []
        for sig_list in self.signal_history.values():
            for s in sig_list:
                if s.timestamp >= cutoff and s.effective_weight >= min_score:
                    all_signals.append(s)

        by_type: dict[str, int] = {}
        by_source: dict[str, int] = {}
        topics: dict[str, int] = {}
        accounts: dict[str, int] = {}

        for s in all_signals:
            by_type[s.signal_type.value] = by_type.get(s.signal_type.value, 0) + 1
            by_source[s.source.value] = by_source.get(s.source.value, 0) + 1
            if s.topic:
                topics[s.topic] = topics.get(s.topic, 0) + 1
            acct = s.account_id or "unknown"
            accounts[acct] = accounts.get(acct, 0) + 1

        sorted_topics = sorted(topics.items(), key=lambda x: -x[1])[:5]
        sorted_accounts = sorted(accounts.items(), key=lambda x: -x[1])[:5]

        top_accounts_data = [
            {"id": a, "signal_count": c} for a, c in sorted_accounts
        ]

        summary_parts = []
        if by_type:
            dominant = max(by_type, key=by_type.get)
            summary_parts.append(
                f"Dominant signal type: {dominant} ({by_type[dominant]} signals)"
            )
        if sorted_topics:
            summary_parts.append(
                f"Top topic: {sorted_topics[0][0]} ({sorted_topics[0][1]} signals)"
            )
        if len(all_signals) >= 0:
            summary_parts.append(f"Total: {len(all_signals)} signals in {period} period")

        return SignalAggregation(
            period=period,
            start_date=cutoff,
            end_date=now,
            total_signals=len(all_signals),
            by_type=by_type,
            by_source=by_source,
            top_accounts=top_accounts_data,
            top_topics=sorted_topics,
            summary=" | ".join(summary_parts),
        )

    def score_readiness(
        self, deal_id: str, now: Optional[datetime] = None
    ) -> Optional[BuyingReadiness]:
        if deal_id not in self.signal_history:
            return None
        return BuyingReadiness.from_signals(deal_id, self.signal_history[deal_id], now)

    def evaluate_triggers(
        self,
        readiness: BuyingReadiness,
        now: Optional[datetime] = None,
    ) -> list[OutreachTrigger]:
        if now is None:
            now = datetime.now()

        triggers = []
        for sig in readiness.active_signals:
            if sig.effective_weight < 2.0:
                continue

            action, channel, msg = self._classify_outreach_action(sig, readiness)
            priority = self._compute_priority(sig, readiness)

            triggers.append(OutreachTrigger(
                trigger_id=f"trg_{uuid.uuid4().hex[:12]}",
                deal_id=readiness.deal_id,
                contact_id=sig.metadata.get("contact_id"),
                signal_type=sig.signal_type,
                source=sig.source,
                strength=classify_strength(sig.effective_weight),
                readiness_score=readiness.total_score,
                recommended_action=action,
                recommended_channel=channel,
                priority=priority,
                message_suggestion=msg,
                triggered_at=now,
                raw_signal=sig,
            ))

        triggers.sort(key=lambda t: t.priority)
        return triggers

    def enrich_with_llm(
        self,
        readiness: BuyingReadiness,
        deal_context: Optional[str] = None,
    ) -> dict:
        try:
            sig_summary = []
            for s in readiness.active_signals[:10]:
                sig_summary.append(
                    f"  - {s.signal_type.value} from {s.source.value} "
                    f"(weight: {s.effective_weight:.1f}, topic: {s.topic}): {s.raw_text[:100]}"
                )

            prompt = (
                "You are a senior SDR analyst evaluating buyer intent signals.\n"
                f"Deal: {readiness.deal_id}\n"
                f"Readiness Level: {readiness.readiness_level} (score: {readiness.total_score}/100)\n"
                f"Trend: {readiness.trend_direction}\n"
                f"Signal Count: {readiness.signal_count}\n"
                f"Top Signals:\n" + "\n".join(sig_summary) + "\n"
            )
            if deal_context:
                prompt += f"\nDeal Context:\n{deal_context}\n"

            prompt += (
                "\nProvide:\n"
                "1. Brief intent assessment (2-3 sentences)\n"
                "2. Recommended next action\n"
                "3. Optimal outreach channel\n"
                "4. Key talking points (2-3 bullets)\n"
                "5. Risk factors to watch\n"
                "Format as a concise JSON object with keys: assessment, next_action, "
                "channel, talking_points (list), risk_factors (list)."
            )

            resp = self.llm.generate(prompt, max_tokens=600)
            enriched = self._parse_json_response(resp)
            return enriched or {
                "assessment": f"Buying readiness at {readiness.readiness_level} level",
                "next_action": readiness.recommendation,
                "channel": "email",
                "talking_points": [],
                "risk_factors": ["No LLM enrichment available"],
            }
        except Exception:
            return {
                "assessment": f"Buying readiness at {readiness.readiness_level} level "
                             f"(score: {readiness.total_score})",
                "next_action": readiness.recommendation,
                "channel": "email",
                "talking_points": [],
                "risk_factors": ["LLM enrichment unavailable"],
            }

    # --- core scanning ---

    def _rule_based_scan(
        self,
        deal_id: str,
        account: dict,
        now: datetime,
    ) -> list[IntentSignal]:
        sources = list(SignalSource)
        signals = []

        for source in sources:
            result = self._scan_source(deal_id, account, source, now)
            signals.extend(result)

        return signals

    def _scan_source(
        self,
        deal_id: str,
        account: dict,
        source: SignalSource,
        now: datetime,
    ) -> list[IntentSignal]:
        cooldown_key = f"{deal_id}:{source.value}"
        last = self.scan_cooldown.get(cooldown_key)
        if last and (now - last) < self.min_scan_interval:
            return []

        self.scan_cooldown[cooldown_key] = now

        account_name = account.get("name", "Unknown")
        domain = account.get("domain", "unknown.com")
        industry = account.get("industry", "")

        signals = []

        if source == SignalSource.LINKEDIN:
            signals = self._simulate_linkedin(deal_id, account_name, domain, industry, now)
        elif source == SignalSource.CRUNCHBASE:
            signals = self._simulate_crunchbase(deal_id, account_name, domain, now)
        elif source == SignalSource.BUILTWITH:
            signals = self._simulate_builtwith(deal_id, account_name, domain, now)
        elif source == SignalSource.G2:
            signals = self._simulate_g2(deal_id, account_name, domain, now)
        elif source == SignalSource.RSS:
            signals = self._simulate_rss(deal_id, account_name, domain, now)
        elif source == SignalSource.COMPANY_BLOG:
            signals = self._simulate_blog(deal_id, account_name, domain, now)
        elif source == SignalSource.NEWS:
            signals = self._simulate_news(deal_id, account_name, domain, industry, now)
        elif source == SignalSource.TWITTER:
            signals = self._simulate_twitter(deal_id, account_name, domain, now)
        elif source == SignalSource.WEBSITE:
            signals = self._simulate_website(deal_id, account_name, domain, now)
        elif source == SignalSource.REDDIT:
            signals = self._simulate_reddit(deal_id, account_name, domain, now)

        return signals

    def _make_signal(
        self,
        deal_id: str,
        signal_type: SignalType,
        source: SignalSource,
        raw_text: str,
        timestamp: datetime,
        account_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        topic: Optional[str] = None,
        url: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> IntentSignal:
        base_weight = SIGNAL_WEIGHTS.get(signal_type, 2.0)
        base_confidence = SIGNAL_CONFIDENCE_BY_SOURCE.get(source, 0.5)

        hash_input = f"{deal_id}|{signal_type.value}|{source.value}|{raw_text[:80]}|{timestamp.isoformat()}"
        sig_id = f"sig_{hashlib.sha256(hash_input.encode()).hexdigest()[:16]}"

        sig = IntentSignal(
            signal_id=sig_id,
            deal_id=deal_id,
            contact_id=contact_id,
            account_id=account_id or deal_id,
            signal_type=signal_type,
            source=source,
            strength=SignalStrength.LOW,
            confidence=base_confidence,
            base_weight=base_weight,
            effective_weight=base_weight,
            raw_text=raw_text,
            url=url,
            timestamp=timestamp,
            topic=topic,
            metadata=metadata or {},
        )
        sig.recalculate_weight(timestamp)
        sig.strength = classify_strength(sig.effective_weight)
        return sig

    # --- simulated sources ---

    def _simulate_linkedin(
        self, deal_id: str, account: str, domain: str, industry: str, now: datetime
    ) -> list[IntentSignal]:
        signals = []
        job_titles = [
            "VP of Sales", "Head of Engineering", "CFO", "Chief Revenue Officer",
            "Director of IT", "Head of Product", "Chief Data Officer",
        ]
        for i in range(2):
            title = self._rng.choice(job_titles)
            person = f"person_{i + 1}"
            event = self._rng.choice(["joined", "promoted to", "left"])
            signals.append(self._make_signal(
                deal_id, SignalType.JOB_CHANGE, SignalSource.LINKEDIN,
                f"{person} {event} {title} at {account}",
                now - timedelta(days=self._rng.randint(1, 30)),
                contact_id=person,
                topic=title,
            ))
        return signals

    def _simulate_crunchbase(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        fund_events = [
            f"raised $50M Series C",
            f"acquired by a strategic buyer",
            f"completed $30M Series B funding round",
        ]
        event = self._rng.choice(fund_events)
        return [self._make_signal(
            deal_id, SignalType.FUNDING, SignalSource.CRUNCHBASE,
            f"{account} {event}",
            now - timedelta(days=self._rng.randint(5, 45)),
            topic=self._rng.choice(["infrastructure", "analytics", "ai"]),
        )]

    def _simulate_builtwith(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        changes = [
            "deployed Salesforce CRM",
            "implemented HubSpot",
            "migrated to Snowflake",
            "adopted Datadog for monitoring",
            "standardized on AWS",
        ]
        change = self._rng.choice(changes)
        return [self._make_signal(
            deal_id, SignalType.TECHNOLOGY, SignalSource.BUILTWITH,
            f"{account} {change}",
            now - timedelta(days=self._rng.randint(2, 20)),
            topic=self._rng.choice(["crm", "infrastructure", "analytics"]),
        )]

    def _simulate_g2(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        activities = [
            "reviewing CRM solutions on G2",
            "compared competitor pricing page",
            "requested a demo from vendor",
            "reading case studies on category page",
        ]
        activity = self._rng.choice(activities)
        return [self._make_signal(
            deal_id, SignalType.COMPETITOR, SignalSource.G2,
            f"{account} {activity}",
            now - timedelta(days=self._rng.randint(1, 14)),
            topic="crm",
        )]

    def _simulate_rss(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        signals = []
        feeds = INTENT_SOURCE_FEEDS.get(SignalSource.RSS, [])
        for feed in feeds[:2]:
            signals.append(self._make_signal(
                deal_id, SignalType.PUBLISHING, SignalSource.RSS,
                f"New industry content from G2/blog related to {account}",
                now - timedelta(days=self._rng.randint(1, 7)),
                topic=self._rng.choice(["crm", "sales", "analytics"]),
                url=feed,
            ))
        return signals

    def _simulate_blog(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        topics = [
            "why we chose Snowflake over Redshift",
            "how we scaled our engineering team",
            "our journey to SOC 2 compliance",
            "building a data-driven sales culture",
            "migrating to microservices",
        ]
        topic = self._rng.choice(topics)
        return [self._make_signal(
            deal_id, SignalType.PUBLISHING, SignalSource.COMPANY_BLOG,
            f"{account} published: {topic}",
            now - timedelta(days=self._rng.randint(3, 14)),
            topic=self._rng.choice(["infrastructure", "security", "analytics"]),
            url=f"https://{domain}/blog",
        )]

    def _simulate_news(
        self, deal_id: str, account: str, domain: str, industry: str, now: datetime
    ) -> list[IntentSignal]:
        articles = [
            f"announced major restructuring",
            f"opening new HQ in Austin",
            f"laid off 5% of workforce",
            f"named new CEO",
            f"expanding into European market",
        ]
        article = self._rng.choice(articles)
        return [self._make_signal(
            deal_id, SignalType.PUBLISHING, SignalSource.NEWS,
            f"{account} {article}",
            now - timedelta(days=self._rng.randint(1, 10)),
            topic="news",
        )]

    def _simulate_twitter(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        posts = [
            "looking for CRM recommendations",
            "anyone using vendor X? thoughts?",
            "just deployed new sales tool",
            "comparing tool A vs tool B",
        ]
        post = self._rng.choice(posts)
        return [self._make_signal(
            deal_id, SignalType.SOCIAL, SignalSource.TWITTER,
            f"Post: {post}",
            now - timedelta(days=self._rng.randint(1, 7)),
            topic="crm" if "crm" in post or "tool" in post else None,
        )]

    def _simulate_reddit(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        posts = [
            "r/sales: Best CRM for enterprise in 2026?",
            "r/sales: Anyone used vendor X for outbound?",
            "r/sales: Moving from legacy CRM to modern platform - advice?",
            "r/sales: Evaluating sales engagement platforms",
        ]
        post = self._rng.choice(posts)
        return [self._make_signal(
            deal_id, SignalType.CONTENT, SignalSource.REDDIT,
            post,
            now - timedelta(days=self._rng.randint(1, 14)),
            topic="crm" if "crm" in post or "sales" in post else None,
        )]

    def _simulate_website(
        self, deal_id: str, account: str, domain: str, now: datetime
    ) -> list[IntentSignal]:
        pages = [
            "visited /pricing page",
            "visited /case-studies",
            "visited /product page",
            "visited /demo-request",
            "started free trial",
        ]
        page = self._rng.choice(pages)
        return [self._make_signal(
            deal_id, SignalType.CONTENT, SignalSource.WEBSITE,
            f"{account} contact {page}",
            now - timedelta(days=self._rng.randint(0, 5)),
            topic="product",
        )]

    # --- analysis ---

    def _classify_atl_btl(self, signal: IntentSignal) -> ATL_BTL:
        if signal.signal_type in ATL_SIGNAL_TYPES:
            return ATL_BTL.ATL
        if signal.signal_type in BTL_SIGNAL_TYPES:
            return ATL_BTL.BTL
        return ATL_BTL.BTL

    def _classify_intent_level(self, readiness: BuyingReadiness) -> IntentLevel:
        score = readiness.total_score
        level = IntentLevel.COLD
        for threshold, lvl, _ in reversed(INTENT_STACK_THRESHOLDS):
            if score >= threshold:
                level = lvl
                break
        return level

    def _classify_outreach_action(
        self, signal: IntentSignal, readiness: BuyingReadiness
    ) -> tuple[str, str, str]:
        atl_btl = self._classify_atl_btl(signal)
        intent_level = self._classify_intent_level(readiness)
        is_atl = atl_btl == ATL_BTL.ATL
        is_active = intent_level in (IntentLevel.ACTIVE, IntentLevel.CONSIDERING)

        if signal.signal_type == SignalType.JOB_CHANGE:
            return (
                "BTL: Send personalized congratulations + value prop (indirect)",
                "linkedin",
                f"Congrats on the new role at {signal.deal_id}! "
                f"Curious how you're approaching [topic] in the new role.",
            )
        if signal.signal_type == SignalType.FUNDING:
            return (
                "ATL: Growth-oriented outreach with intent context",
                "email",
                f"Congrats on the recent funding! We help growth-stage "
                f"companies scale [capability]. Would 15 min be useful?",
            )
        if signal.signal_type == SignalType.COMPETITOR:
            return (
                "ATL: Immediate competitive differentiation — they're in evaluation mode",
                "email" if is_active else "linkedin",
                f"Noticed you're evaluating solutions. We've helped [similar_company] "
                f"achieve [result] — happy to share how we compare on the criteria "
                f"that matter most to you.",
            )
        if signal.signal_type == SignalType.CONTENT:
            return (
                "ATL: Direct outreach with content-aware value prop",
                "email",
                f"Saw you were looking at [topic]. Here's a case study of "
                f"how [customer] achieved [result] — relevant to what you're exploring?",
            )
        if atl_btl == ATL_BTL.BTL:
            return (
                "BTL: Indirect nurture, build awareness before direct ask",
                "linkedin",
                f"Noticed [company]'s recent [signal_type] activity. "
                f"Thought you might find this relevant — [value observation].",
            )
        return (
            "ATL: Direct outreach with signal-aware context",
            "email",
            f"Noticed recent [signal_type] activity at your company. "
            f"Relevant in the context of [topic]?",
        )

    def _compute_priority(self, signal: IntentSignal, readiness: BuyingReadiness) -> int:
        score = readiness.total_score
        weight = signal.effective_weight
        intent_level = self._classify_intent_level(readiness)

        if intent_level == IntentLevel.ACTIVE and weight >= 4.0:
            return 1
        if intent_level in (IntentLevel.ACTIVE, IntentLevel.CONSIDERING) and weight >= 3.0:
            return 2
        if intent_level == IntentLevel.INTERESTED and weight >= 2.0:
            return 3
        if intent_level == IntentLevel.AWARE:
            return 4
        return 5

    def _deduplicate(self, signals: list[IntentSignal]) -> list[IntentSignal]:
        seen: set[str] = set()
        unique = []
        for s in signals:
            key = f"{s.deal_id}|{s.signal_type.value}|{s.raw_text[:100]}"
            if key not in seen:
                seen.add(key)
                unique.append(s)
        return unique

    def _parse_json_response(self, text: str) -> Optional[dict]:
        try:
            match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except (json.JSONDecodeError, AttributeError):
            return None

    @property
    def _rng(self):
        import random
        return random.Random(42)
