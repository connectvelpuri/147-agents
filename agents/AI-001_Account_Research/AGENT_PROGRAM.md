# AI-001: Account Research Agent — Agent Program

> **Agent ID:** AI-001  
> **Division:** Account Intelligence (Division 23)  
> **LLM Tier:** Complex Reasoning (Opus-class)  
> **Criticality:** P1  
> **NATS Stream:** `ai.account.research`  
> **Version:** 1.0.0 | **Status:** Program Design

---

## 1. Role Summary

AI-001 is the RevenueOS intelligence foundation. Before any SDR reaches out, before any qualification score is calculated, before any meeting observer analyzes a call — AI-001 has already profiled the account, its people, its tech stack, its financial health, its strategic initiatives, and its trigger events.

**One-line purpose:** Transform fragmented public data into decision-grade strategic intelligence that every downstream agent consumes.

**Why this agent exists as dedicated:** Account intelligence is the most data-intensive, source-diverse task in the RevenueOS. It requires synthesizing across 12+ data domains (financial, technographic, organizational, social, news, regulatory, jobs, competitive, partner, cultural, intent, historical). No single domain agent can hold this breadth. Every other account-facing agent depends on AI-001's output to do their job.

---

## 2. Core Methodology — OSINT-DRIVEN ACCOUNT INTELLIGENCE (ODAI)

This is a custom methodology purpose-built for RevenueOS. It adapts the OSINT intelligence cycle to B2B sales research, layering in sales-specific frameworks where applicable.

### The ODAI Intelligence Cycle (6 phases)

```
PHASE 1 ──► PHASE 2 ──► PHASE 3 ──► PHASE 4 ──► PHASE 5 ──► PHASE 6
DIRECTION    COLLECTION   VERIFICATION  ANALYSIS    PRODUCTION   FEEDBACK
```

#### Phase 1: Direction & Scoping
Before collecting anything, AI-001 defines:
- **ICP context:** What kind of account is this? (Strategic, Mid-market, SMB expansion)
- **Research depth required:** Quick profile (<5 min), Standard profile (15 min), Deep dive (60+ min)
- **Priority intelligence gaps:** What does the SDR/team already know vs what's blind?
- **Trigger relevance:** Is this account responding to a specific event (funding, exec change, product launch, competitor loss)?
- **Downstream consumer needs:** What does each consuming agent need? (SDR needs talking points, Qual needs budget signal, Meeting Obs needs org context)

**Input:** `account_research_requested` event from RCC-001 (Revenue Orchestrator) or `new_lead_created` event  
**Outputs:** Research plan with scope, depth, priority intelligence targets, and consumer-specific requirements

#### Phase 2: Multi-Source Collection (12 Domains)
AI-001 collects data across 12 intelligence domains, each with specific tools and sources:

| # | Domain | Primary Tools | Key Data Points | Priority |
|---|--------|--------------|----------------|----------|
| 1 | **Firmographic** | CrunchBase API, company website, annual reports | Revenue, employee count, HQ, founded, industry, ownership | 1-Highest |
| 2 | **Financial** | SEC EDGAR, PitchBook, annual/quarterly filings, news | Revenue growth, funding rounds, valuation, profitability, debt structure | 1 |
| 3 | **Technographic** | BuiltWith, Wappalyzer, StackShare, LinkedIn skills | ERP, CRM, WMS, TMS, analytics stack, cloud providers, integration tech | 1 |
| 4 | **Organizational** | LinkedIn Sales Navigator, company website, Zoominfo | Org chart, decision-maker hierarchy, tenure, reporting lines, C-suite | 1 |
| 5 | **News & Events** | agent-reach (RSS/NewsAPI/Google News), last30days, SEC filings | Press releases, earnings calls, product launches, partnerships, M&A | 2 |
| 6 | **Social Intelligence** | agent-reach (LinkedIn/Twitter/Reddit), last30days (X/TikTok/HN) | Executive posts, employee sentiment, company culture signals, brand perception | 2 |
| 7 | **Job Posting Intelligence** | LinkedIn jobs, company careers page, Indeed, Glassdoor | New roles (signal of investment), role types (tech hires = digital transformation), departures | 2 |
| 8 | **Competitive** | CrunchBase, agent-reach web search, G2, Gartner | Who else sells to them, competitor wins/losses, competitive landscape | 2 |
| 9 | **Regulatory & Legal** | SEC filings, USPTO database, FTC, GDPR register, PACER | Pending lawsuits, patent filings, regulatory risks, compliance obligations | 3 |
| 10 | **Cultural & Organizational** | Glassdoor, Indeed reviews, LinkedIn employee posts, news | Culture signals, leadership style, DEI focus, talent retention, management churn | 3 |
| 11 | **Partner & Ecosystem** | LinkedIn, CrunchBase, news | System integrators, technology partners, channel partners, alliance history | 3 |
| 12 | **Intent** | G2 buyer intent, company career page growth, job posting velocity, news frequency | Buying signals, technology evaluation cycles, expansion indicators | 1 |

**Key tools invoked per domain:**
- `agent-reach` — 17 platforms: web pages, YouTube, GitHub, Bilibili, V2EX, Reddit, RSS, LinkedIn, Twitter, etc.
- `last30days` — 8 platforms: Reddit, X/Twitter, YouTube transcripts, Hacker News, Polymarket, GitHub, TikTok, Instagram
- BuiltWith/Wappalyzer — direct API calls for technographic detection
- CrunchBase API — firmographic and funding data
- SEC EDGAR API — financial filings for public companies
- LinkedIn Sales Navigator (via MCP) — org chart and decision-maker hierarchy
- Google News / NewsAPI — real-time news monitoring
- RSS feeds per account — press releases, blog posts, investor relations

#### Phase 3: Cross-Source Verification
Every data point is verified against at least two independent sources before inclusion:

- **Financial data:** SEC filing + CrunchBase + news article = trusted. If only one source, mark as "unverified" in the report with a confidence score.
- **Org chart:** LinkedIn + Zoominfo/CrunchBase + company website = trusted. LinkedIn alone produces "unverified org node" markers.
- **Tech stack:** BuiltWith + Wappalyzer + LinkedIn job postings (tech roles) = trusted. Single-tool detection is a "suspected" tag.
- **News:** agent-reach from 2+ distinct sources (e.g., Google News + RSS + social media cross-post). Single-source = "rumor/unconfirmed".

**Confidence tagging:** Every intelligence item is tagged with `{source_count: N, confidence: low|medium|high, last_verified: ISO8601}`. The consuming agent can choose to trust or disregard based on its own risk tolerance.

#### Phase 4: Multi-Layer Analysis
Raw collected data is synthesized through three analytical passes:

**Layer 1: Descriptive** — What is the account?
- Company overview, financial position, org structure, tech landscape
- Direct output to AI-002 (Relationship Mapper) for warm path analysis
- Direct output to SDR-001 (SDR Team) for first outreach talking points

**Layer 2: Diagnostic** — Why does the account behave this way?
- Strategic initiatives analysis (what problems are they actively trying to solve?)
- Pain point inference (what keeps their execs up at night based on job postings, news, investor calls?)
- Buying window signals (has a contract expiration, new C-suite, funding event, or competitor loss created an opening?)
- Culture fit assessment (do they buy from companies like ours? relationship-driven or RFP-driven?)

**Layer 3: Predictive** — What will happen next?
- Likely next strategic move (expansion, acquisition, cost-cutting, digital transformation?)
- Risk factors (regulatory threat, market headwinds, talent attrition, competitive pressure)
- Engagement recommendation (which persona to approach first? what value prop resonates? what timing?)
- Win probability estimate based on fit score + intent signals + relationship mapping

#### Phase 5: Production & Publication
The intelligence is packaged into domain-specific reports, each targeting a specific downstream consumer:

| Report Type | Consumer Agent(s) | Format | Trigger |
|-------------|-------------------|--------|---------|
| **Account Intelligence Profile** | SDR-001, SDR-002, QL-001, QL-002 | Structured JSON + natural language summary | Account entered target list |
| **Org Chart & Relationship Map** | AI-002, SDR-001 | Graph structure (nodes + edges + weighting) | Intelligence profile complete |
| **Buying Signal Alert** | SDR-001, RCC-003 | Event with signal type, confidence, relevant persona | High-confidence intent signal detected |
| **Trigger Event Briefing** | MO-001, SDR-001, QL-001 | Natural language + structured event data | Exec change, funding, M&A, product launch |
| **Competitive Intel Flash** | VE-001, NG-001, DS-001 | Structured + natural language | Competitor identified at account |
| **Financial Health Report** | DSV-001, VE-001 | Structured metrics + trend analysis | Quarterly/annual reporting cycle |
| **Tech Stack Blueprint** | VE-001, DLC-001 | System diagram JSON + integration points | Technographic collection complete |

**Publication mechanism:** All reports published to specific NATS JetStream subjects:
- `ai.account.intelligence.profile.{account_id}`
- `ai.account.org_chart.{account_id}`
- `ai.account.signal.{account_id}`
- `ai.account.trigger.{account_id}`
- `ai.account.competitive.{account_id}`
- `ai.account.financial.{account_id}`
- `ai.account.techstack.{account_id}`

#### Phase 6: Feedback & Accuracy Scoring
Every claim published by AI-001 that gets corrected by a human is logged and analyzed:

- **Accuracy tracking:** Each intelligence item has a unique ID. If the SDR, AE, or customer team corrects it, the correction is logged back to AI-001's feedback stream (`ai.account.research.feedback`).
- **Source reliability scoring:** Per source, track what percentage of its data points get corrected. Low-reliability sources get deprioritized.
- **Timeliness scoring:** Was the intelligence produced before or after the SDR needed it? Track lag time.
- **Confidence calibration:** Are high-confidence items actually accurate? Are low-confidence items less wrong than tagged? Adjust confidence heuristics.
- **Coverage gaps:** What domains consistently lack data? Flag for source pipeline improvements.

---

## 3. Skills & Tools

### Skills (opencode skills loaded on activation)

| Skill | Purpose | When Used |
|-------|---------|-----------|
| **agent-reach** | 17-platform data collection (web, social, video, RSS, dev platforms) | Phase 2 — every collection cycle |
| **last30days** | Multi-platform sentiment and trend detection (Reddit, X, YouTube, TikTok, HN, GitHub, Polymarket) | Phase 2 — sentiment analysis, trigger detection |
| **deep-research** | Comprehensive multi-source research with cited reports | Phase 2 — deep dive accounts |
| **exa-search** | Neural search for company intel, people lookup, competitive intel | Phase 2 — when specific data points are missing |
| **market-research** | Market sizing, competitive analysis, industry intelligence | Phase 2 — competitive/landscape layer |
| **benchmark** | Performance baselines for comparing against industry benchmarks | Phase 4 — predictive analysis |
| **production-audit** | Production readiness checks | Pre-deployment validation |

### External Tools & APIs

| Tool/API | Purpose | Phase |
|----------|---------|-------|
| BuiltWith API | Technographic detection (ERP, CRM, analytics, cloud) | Phase 2 |
| Wappalyzer | Real-time tech stack identification from website | Phase 2 |
| CrunchBase API | Firmographic + funding + acquisition data | Phase 2 |
| SEC EDGAR API | Financial filings (10-K, 10-Q, 8-K) | Phase 2 |
| LinkedIn Sales Navigator | Org chart, decision-maker hierarchy, job changes | Phase 2 |
| Google News / NewsAPI | Real-time news monitoring per account | Phase 2 |
| RSS feeds (per account) | Press releases, investor relations, blog monitoring | Phase 2 |
| Glassdoor API | Employee reviews, culture signals | Phase 2 |
| G2 API | Technology reviews, buyer intent | Phase 2 |
| USPTO API | Patent filings (technology direction signals) | Phase 2 |
| NATS JetStream | All inter-agent communication | Phase 5 |

### Reference Sources (Domain Expertise)

The agent's Training Corpus draws from:

**OSINT & Research Methodology:**
- Bellingcat OSINT methodology (digital investigation techniques)
- The OSINT Handbook (systematic intelligence collection)
- SANS SEC487: Open-Source Intelligence course material
- IntelTechniques OSINT framework (Michael Bazzell)
- Project Sherlock (social media cross-referencing)

**Sales-Specific Research:**
- Gong Labs Research Library (https://www.gong.io/research-library/) — conversation intelligence-backed research methodology
- Lavina Gandhi (LinkedIn Sales Navigator thought leader) — social selling intelligence techniques
- Josh Braun (SDR research methodology) — trigger-based selling, signal detection
- Morgan J Ingram (SDR execution and research) — persona profiling methodology
- Outreach / SalesLoaf research methodology (account-based intelligence)
- ZoomInfo Blog — account intelligence data quality patterns
- CrunchBase Blog — firmographic data sources and analysis
- LinkedIn Sales Navigator Blog — social selling intelligence

**Technographic Analysis:**
- BuiltWith Blog — technology detection methodology
- Wappalyzer detection patterns
- StackShare community intelligence

---

## 4. Inter-Agent Communication Architecture

AI-001 is a **data producer** for many agents and a **data consumer** of a few. Here is the full communication graph:

### Data Consumed FROM (inputs)

| Source Agent | Data | NATS Subject | Cadence |
|-------------|------|-------------|---------|
| RCC-001 (Revenue Orchestrator) | Account research request, ICP criteria, priority settings | `rcc.workflow.account_request` | Event-driven |
| RCC-003 (Revenue Analyzer) | Account performance tier, revenue signals | `rcc.analytics.account_tier` | On tier change |
| DSV-001 (Data Ingestion Engine) | Enriched CRM data, normalized account records | `dsv.crm.account_enriched` | On CRM update |
| DSV-003 (Data Quality Monitor) | Data quality flags, missing field alerts | `dsv.quality.account_flag` | On quality issue |
| CV-001 (Customer Voice Monitor) | Customer sentiment signals, public mentions | `cv.social.account_mention` | On mention detected |
| KL-005 (Weekly Retrain) | Updated prompt weights, classification patterns | `kl.retrain.research_patterns` | Weekly |
| Human-in-the-loop (corrections) | Research accuracy corrections | `ai.account.research.feedback` | On human correction |

### Data Published TO (outputs)

| Consumer Agent | Data | NATS Subject | Cadence |
|---------------|------|-------------|---------|
| AI-002 (Relationship Mapper) | Org chart, decision-maker hierarchy, relationship candidates | `ai.account.org_chart.{id}` | On account research complete |
| SDR-001 (SDR Inbound/Outbound) | Account profile, talking points, trigger events, recommended personas | `ai.account.intelligence.profile.{id}` | On account entered target list |
| SDR-002 (SDR Meeting Booker) | Buying signals, optimal timing, persona availability | `ai.account.signal.{id}` | On signal detected |
| QL-001 (MEDDPICC Scorer) | Financial health, tech stack, funding events, growth signals | `ai.account.financial.{id}` | On financial data update |
| QL-002 (Budget Validator) | Revenue range, funding details, spending authority, procurement history | `ai.account.financial.{id}` | On financial data update |
| MO-001 (Meeting Observer) | Org context, persona role/responsibilities, strategic initiatives | `ai.account.intelligence.profile.{id}` | On meeting scheduled |
| VE-001 (Value Engineer) | Tech stack, integration points, current vendor landscape | `ai.account.techstack.{id}` | On deal advanced to stage 2+ |
| DS-001 (Deal Strategist) | Competitive landscape, partner ecosystem, regulatory risks | `ai.account.competitive.{id}` | On deal entered strategy review |
| NG-001 (Negotiator) | Financial health, purchasing history, approval hierarchy | `ai.account.financial.{id}` | On deal entered negotiation |
| RFP-001 (RFP Manager) | Regulatory filings, compliance posture, security certifications | `ai.account.regulatory.{id}` | On RFP initiated |
| BP-001 (Buyer Persona) | Organisational psychographics, decision-maker personality profiles | `ai.account.org_chart.{id}` | On org chart complete |
| ABM-001 (ABM Campaign Design) | Technology stack, partner ecosystem, cultural signals for campaign targeting | `ai.account.techstack.{id}` | On account selected for ABM |
| RCC-004 (Pipeline Forecaster) | Account fit score, win probability, risk factors | `ai.account.intelligence.profile.{id}` | On research complete |

### How AI-001 Handles Missing Data

When AI-001 needs additional data that it cannot collect itself:

1. Publishes `ai.account.data_gap` event specifying: `{account_id, missing_domain, suggested_source_agent, urgency}`
2. The target agent receives the request and either fulfills it or returns `data_unavailable`
3. AI-001 proceeds with available data, marking the gap in its confidence scoring
4. If 3+ consecutive requests to the same agent return `data_unavailable`, AI-001 logs a gap pattern to KL-005 for retrain

---

## 5. Workflow & Daily Operation

### Account Research Request Flow

```
1. RCC-001 publishes `rcc.workflow.account_request` with account_name + depth
       │
2. AI-001 receives event, Phase 1 (Direction): creates research plan
       │
3. AI-001 requests Phase 2 collection across 12 domains (parallel where possible)
       ├── Firmographic (CrunchBase + website + annual report)
       ├── Financial (SEC EDGAR + CrunchBase + news) [if public]
       ├── Technographic (BuiltWith + Wappalyzer + LinkedIn job posts)
       ├── Organizational (LinkedIn Sales Navigator + company site + Zoominfo)
       ├── News (agent-reach RSS + NewsAPI + last30days)
       ├── Social (agent-reach LinkedIn/Twitter + last30days)
       ├── Jobs (LinkedIn jobs + careers page + Indeed)
       ├── Competitive (CrunchBase + agent-reach web + G2)
       ├── Regulatory (SEC + USPTO if applicable)
       ├── Cultural (Glassdoor + LinkedIn posts)
       ├── Partner (LinkedIn + CrunchBase + news)
       └── Intent (G2 + job velocity + news frequency)
       │
4. Phase 3 (Verification): cross-source verify each claim, assign confidence
       │
5. Phase 4 (Analysis): Descriptive → Diagnostic → Predictive passes
       │
6. Phase 5 (Production): Package into domain-specific reports, publish to NATS
       │
7. Phase 6 (Feedback loop): Await corrections, log accuracy, update source scores
```

### Autonomous Cadence (Ongoing Monitoring)

Beyond one-shot research requests, AI-001 operates a monitoring loop for active accounts:

| Frequency | Action |
|-----------|--------|
| **Every 24h** | Check configured news sources for active accounts; publish signal updates if trigger events detected |
| **Every 7 days** | Full intelligence refresh for active pursuit accounts (stage 2+ in pipeline) |
| **Every 30 days** | Full intelligence refresh for all target list accounts |
| **Event-driven** | Immediate collection on: executive change, funding announcement, acquisition news, competitor win/loss, RFP issuance |

### Quality Gates (Pre-Publication)

Every report passes through these gates before publication:

1. **Completeness gate:** All 12 domains checked. Missing domains flagged with confidence penalty.
2. **Verification gate:** Every claim has at least 2 sources OR is tagged as "unverified" with reasoning.
3. **Contradiction gate:** If two sources disagree, both are presented with source confidence weights. Do NOT silently pick one.
4. **Timeliness gate:** Data older than the configured refresh cadence is marked with a "stale" warning and deprioritized.
5. **Consumer relevance gate:** Each report section is tagged with the consuming agent ID. Irrelevant data is included but demoted to "appendix" status.

---

## 6. Output Specifications

### Account Intelligence Profile (JSON Schema)

```json
{
  "account_id": "string",
  "account_name": "string",
  "research_depth": "quick|standard|deep",
  "report_version": "string",
  "generated_at": "ISO8601",
  "research_plan": {
    "domains_collected": ["domain1", "..."],
    "domains_missing": ["domain2", "..."],
    "overall_confidence": 0.0-1.0
  },
  "firmographic": {
    "revenue": {"value": "string", "source_count": 2, "confidence": "high"},
    "employees": {"value": 10000, "confidence": "high"},
    "headquarters": {"city": "...", "country": "..."},
    "industry": ["industry1", "industry2"],
    "ownership": "public|private|pe_backed|subsidiary",
    "founded": 1995,
    "stock_ticker": "string (if public)"
  },
  "financial_health": {
    "revenue_growth_trend": "declining|stable|growing",
    "funding_rounds": [...],
    "profitability_status": "profitable|breakeven|unprofitable",
    "debt_structure_summary": "string",
    "last_filing_date": "ISO8601",
    "risk_flags": ["flag1", "..."]
  },
  "technology_stack": {
    "erp": [...],
    "crm": [...],
    "wms_tms": [...],
    "analytics": [...],
    "cloud_providers": [...],
    "integration_tech": [...],
    "security_compliance": [...],
    "detection_method": "builtwith|wappalyzer|linkedin_jobs",
    "detection_confidence": "high|medium|low"
  },
  "organizational_chart": {
    "c_suite": [
      {"name": "...", "title": "...", "tenure_years": 5,
       "linkedin_url": "...", "reporting_to": "...",
       "confidence": "high"}
    ],
    "decision_makers": [...],
    "influencers": [...],
    "buying_committee_candidates": [...]
  },
  "strategic_initiatives": [
    {
      "initiative": "ERP modernization",
      "evidence": ["job postings for SAP S/4HANA", "news article", "Q3 earnings call transcript"],
      "confidence": "high",
      "relevant_vendors": ["SAP", "Accenture"],
      "implication_for_us": "Opportunity for integration services"
    }
  ],
  "buying_signals": [
    {
      "signal_type": "role_change|funding|contract_expiry|tech_evaluation|competitor_loss",
      "confidence": "high|medium|low",
      "description": "...",
      "detected_at": "ISO8601",
      "recommended_action": "..."
    }
  ],
  "trigger_events": [
    {
      "event_type": "exec_change|acquisition|funding|restructuring|product_launch",
      "title": "...",
      "url": "...",
      "summary": "...",
      "severity": 1-10,
      "detected_at": "ISO8601",
      "relevant_personas": ["persona_key1", "..."]
    }
  ],
  "competitors_present": [
    {
      "competitor_name": "...",
      "relationship_type": "existing_vendor|evaluating|past_vendor",
      "contract_value_estimated": "string or null",
      "contract_expiration": "ISO8601 or null",
      "confidence": "medium"
    }
  ],
  "risk_factors": [
    {
      "risk_type": "regulatory|financial|culture_fit|competition|timing",
      "severity": 1-10,
      "description": "...",
      "mitigation": "..."
    }
  ],
  "engagement_recommendation": {
    "recommended_persona": "...",
    "recommended_value_proposition": "...",
    "recommended_approach": "relationship_built|value_proof|executive|land_and_expand",
    "optimal_timing": "immediate|this_quarter|next_quarter|monitor",
    "win_probability": 0.0-1.0,
    "estimated_deal_size_range": {"min": 0, "max": 0, "currency": "USD"}
  },
  "consumer_specific_sections": {
    "SDR-001": {
      "key_talking_points": ["...", "..."],
      "icebreakers": ["...", "..."],
      "trigger_based_openers": ["...", "..."]
    },
    "QL-001": {
      "budget_signals": ["...", "..."],
      "authority_structure": "...",
      "timeline_indicators": ["...", "..."]
    },
    "MO-001": {
      "persona_context": {"role": "...", "current_initiatives": "..."},
      "likely_challenges": ["...", "..."]
    }
  },
  "data_gaps": [
    {
      "domain": "financial",
      "gaps": ["Private company - no SEC filings available"],
      "impact": "Reduced financial confidence score"
    }
  ]
}
```

---

## 7. Performance Score & Quality Evaluation

### Scoring Rubric (Composite Score 0-100)

| Dimension | Weight | Measurement | Target |
|-----------|--------|-------------|--------|
| **Accuracy** | 30% | Human correction rate per intelligence item | <10% correction rate |
| **Completeness** | 20% | % of 12 domains with high-confidence data | >80% domains covered |
| **Timeliness** | 15% | New account research completion time | <15 min standard, <5 min quick |
| **Freshness** | 15% | Age of data in profile | <7 days for active pursuit |
| **Signal Detection** | 10% | Trigger events detected before human finds them | >60% detected first |
| **Consumer Satisfaction** | 10% | Feedback score from consuming agents (SDR, MO, QL, etc.) | >4.0/5.0 |

### Score Thresholds

| Score | Rating | Status |
|-------|--------|--------|
| **90-100** | Green | Fully autonomous — no human review needed for standard research |
| **70-89** | Amber | Human spot-check required for financial and org chart sections |
| **<70** | Red | Full human review required; AIG-002 prompt optimization triggered |

---

## 8. Feedback & Learning Loop

### Correction Flow
```
Human (SDR/AE) corrects intelligence item
        │
        ▼
Correction logged to `ai.account.research.feedback` NATS subject
        │
        ├──► AI-001 updates source reliability score for the originating source
        │
        ├──► AI-001 adjusts confidence calibration if pattern detected
        │
        ├──► If >15% correction rate in any domain → publish `ai.account.research.prompt_drift` 
        │   → KL-005 includes in next weekly retrain → AIG-002 prompt optimization
        │
        └──► If >20% correction rate overall → immediate AIG-002 escalation
```

### Self-Learning Mechanisms

1. **Source reliability scoring:** Every source tracked with `{total_claims, corrections, reliability_score}`. Scores updated on each correction. Low-reliability sources (<60%) demoted or flagged.

2. **Confidence calibration:** AI-001 periodically reviews its own confidence assignments vs actual accuracy. If high-confidence items have >10% error rate, confidence thresholds are tightened.

3. **Coverage gap learning:** If the same domain (e.g., technographic) consistently lacks data for a type of account (e.g., SMBs), AI-001 learns to note this as an expected gap rather than flagging it as research failure.

4. **Consumer preference learning:** If SDR-001 consistently ignores certain report sections, AI-001 reduces emphasis there. If QL-001 always expands the financial section, AI-001 prioritizes financial depth.

5. **Pattern extraction:** Monthly audit by AIG-001 identifies patterns in correction data — e.g., "tech stack detection is frequently wrong for manufacturing accounts using OT systems" → triggers source pipeline change.

---

## 9. Deviations & Improvements Over ceva_agent

| Dimension | ceva_agent | AI-001 (RevenueOS) |
|-----------|-----------|-------------------|
| **Scope** | Single-company outreach (CEVA Logistics) | Multi-account intelligence across entire target list |
| **Signal Sources** | 2 (RSS + NewsAPI) | 12 domains across 30+ sources via agent-reach + last30days + dedicated APIs |
| **LinkedIn Monitoring** | Placeholder / TODO (no implementation) | Full implementation via LinkedIn Sales Navigator MCP + agent-reach |
| **Output** | Single-channel message for one persona | Structured multi-report intelligence consumed by 15+ downstream agents |
| **Inter-Agent Awareness** | None (standalone agent) | Full event-mesh communication with 15+ consumers and 5+ producers |
| **Verification** | None (data used as-is) | 3-phase verification (every claim from 2+ sources) |
| **Confidence Scoring** | None | Per-item confidence tagging with calibration tracking |
| **Feedback Loop** | None (no learning from outcomes) | Full feedback pipeline: human correction → source scoring → prompt optimization |
| **Research Depth** | Just enough to write a personalized email | 3-layer analysis (Descriptive → Diagnostic → Predictive) |
| **Source Reliability** | None tracked | Per-source reliability scoring with automatic demotion |
| **Output Format** | Natural language email body | Structured JSON schema consumed programmatically by agents |
| **Quality Gates** | Sinek/Hormozi framework validation (message quality only) | Completeness + Verification + Contradiction + Timeliness + Consumer Relevance |
| **Fallback** | Rule-based regex extraction | Multi-model LLM fallback chain → rule-based → graceful degradation with gap reporting |

---

## 10. Implementation Roadmap

### Phase A (Current — MVP)
- Python agent with orchestrator loop (cf. ceva_agent pattern)
- Phase 2 collection from 6 priority domains (Firmographic, Financial, Technographic, Organizational, News, Jobs)
- Phase 3 verification (basic cross-source check)
- Phase 4 analysis (Descriptive only)
- Phase 5 publication (2 report types: Profile + Signal)
- NATS JetStream integration for publish/subscribe
- SQLite state persistence

### Phase B (Next)
- All 12 domains collection
- Phase 3 verification (full 2+ source requirement)
- Phase 4 analysis (Diagnostic + Predictive)
- All 7 report types
- LinkedIn Sales Navigator full integration
- Agent-reach + last30days full integration

### Phase C (Future)
- Source reliability scoring and automatic demotion
- Confidence calibration
- Consumer preference learning
- Monthly accuracy drift audit
- Full feedback loop pipeline

---

## 11. Key Files

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main agent loop — runs research cycles, connects all components |
| `intelligence_engine.py` | LLM-powered analysis brain (Phase 1, 4) |
| `collection_engine.py` | Multi-source data collection coordinator (Phase 2) |
| `verification_engine.py` | Cross-source verification (Phase 3) |
| `report_publisher.py` | Packages and publishes to NATS (Phase 5) |
| `feedback_processor.py` | Processes human corrections, updates scoring (Phase 6) |
| `source_registry.py` | Manages source configurations, API keys, reliability scores |
| `config.yaml` | Account definitions, ICP criteria, source configurations |
| `models.py` | All data models and JSON schemas |
| `database.py` | State persistence |
| `docs/research_methodology.md` | Full ODAI methodology reference |
| `docs/ceva_comparison.md` | Detailed comparison to ceva_agent benchmark |
