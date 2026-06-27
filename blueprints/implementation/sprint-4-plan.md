# Sprint 4: "Launch, Integrate & Intelligent" — Comprehensive Plan

**Date:** 2026-06-06
**Methodology:** Big 4 (McKinsey MECE + hypothesis-driven) × Pre-mortem × Anti-Bloat
**Scope:** Email Integration (A) + AI & Analytics (B) + Market Launch (C) + Gaps from Research
**Duration:** 3 weeks (target: 18 working days)

---

## 0. EXECUTIVE SUMMARY

This sprint combines three workstreams into one integrated plan. The market research (Reddit r/CRM, r/sales, r/selfhosted, r/opensource; Twenty CRM GitHub issues; G2/Capterra reviews; Product Hunt trends; analyst landscape) reveals a **unified strategic opportunity**:

> **No open-source CRM combines: (1) modern UX, (2) native email+sequences, (3) AI co-pilot, (4) transparent pricing, and (5) excellent self-hosting — in one product.**

Sprint 4 aims to close this gap by shipping the pillars that convert an MVP into a *launch-ready product*.

### Key Research Insights Driving This Plan

| Source | Finding | Sprint 4 Action |
|--------|---------|-----------------|
| r/CRM, r/sales | "Salesforce/HubSpot costs explode; SuiteCRM is a maintenance nightmare" | Position as low-cost, self-hostable alternative |
| r/selfhosted | "Open source CRM UX is terrible; Twenty is closest but missing email & mobile" | Invest in UX polish + email integration |
| Twenty GitHub (top issue #8811) | "Mass email campaigns needed" | Email sequences (Option A) |
| Twenty GitHub (#8034) | "Custom objects/models needed" | Already have custom fields; document extensibility path |
| G2 reviews (cross-CRM) | "Price bait-and-switch is the #1 complaint" | Publish transparent pricing (Option C) |
| Product Hunt 2025-26 | "AI-first CRMs winning; AI co-pilot inside records, not sidebar" | Build AI chat inside records (Option B) |
| Analyst landscape | "CRM → system of intelligence; privacy-first AI is tailwind for self-hosted" | Local LLM support (Option B) |
| r/sales, r/CRM | "Mobile app unusable in field" | Charter mobile PWA plan (not in sprint, but documented) |

### The Three Workstreams (MECE — Mutually Exclusive, Collectively Exhaustive)

| Workstream | Theme | Options Covered | Risk Level | 
|-----------|-------|----------------|:----------:|
| **W1: Launch Foundation** | Make it deployable, discoverable, and publishable | C (Validate + Launch) + what we missed | MEDIUM |
| **W2: Email & SSO** | Table-stakes CRM features that unlock enterprise conversations | A (Email + SSO) | HIGH |
| **W3: AI Co-pilot** | The differentiator — intelligence inside the CRM | B (AI & Analytics) | VERY HIGH |

---

## 1. WHAT WE'VE MISSED (Gap Analysis)

### From Portfolio Review (Sprint 3)

| Gap | Urgency | How Sprint 4 Addresses It |
|-----|:-------:|--------------------------|
| Zero live demo/deployment | CRITICAL | W1: Deploy demo.sovereigncrm.com |
| No pricing page | CRITICAL | W1: Publish pricing on public page |
| No community infrastructure | CRITICAL | W1: GitHub Discussions + Discord + CLA + CONTRIBUTING.md |
| No migration tooling | HIGH | W2: Salesforce/HubSpot CSV import wizard |
| No mobile app | HIGH | Documented as PWA charter; mobile-first responsive polish |
| No SSO/SAML | HIGH | W2: Google OAuth + SAML |
| No email integration | CRITICAL | W2: IMAP/Graph API email sync |
| No AI capabilities | HIGH | W3: AI co-pilot + insight engine |
| No performance baseline | MEDIUM | W1: k6 benchmark documented |
| No testing beyond unit | HIGH | W1: Integration + E2E test foundation |

### From Market Research (New Gaps Uncovered)

| Gap | Source | Severity | How Sprint 4 Addresses It |
|-----|--------|:--------:|--------------------------|
| Email sequences/cadences missing | Twenty GitHub #8811, r/selfhosted | HIGH | W2: Basic email sequences |
| No visual pipeline builder | r/CRM (180 upvotes) | MEDIUM | W2: Enhance existing Kanban with drag-drop |
| No flexible report/dashboard builder | Twenty GitHub #7451, r/sales | HIGH | W3: Report builder API + UI |
| No mobile app for field sales | r/sales, r/CRM, G2 reviews | HIGH | Documented; add responsive improvements |
| Data export limited/painful | G2 HubSpot reviews | MEDIUM | W2: Clean CSV/Excel export |
| AI data entry assistance | r/sales rising post | HIGH | W3: AI "summarize & create" from email |
| Customer success features missing | G2/Gartner gap analysis | MEDIUM | Deferred to Sprint 5 |
| Self-hosting is too complex | Twenty GitHub reviews, r/selfhosted | CRITICAL | W1: `docker compose up` one-liner |
| Migration fear is #1 switching blocker | r/sales, r/HubSpot | HIGH | W2: Migration import wizard |
| Flat/predictable pricing desired | r/selfhosted, G2 reviews | MEDIUM | W1: Publish $0/$29/$custom tiers |

---

## 2. WORKSTREAM 1: LAUNCH FOUNDATION (Option C + Gaps)

**Goal:** Make Sovereign CRM real — deployable, discoverable, and ready for public feedback.

### Tasks

#### 1.1 Live Demo Deployment (P0)
- `docker-compose.yml` one-liner for production deployment (Postgres + API + Web)
- Auto-seed with sample data: 50 contacts, 20 leads, 10 deals, 7 pipeline stages
- SSL + auto-cert via Caddy/Traefik
- Deploy to demo.sovereigncrm.com (DigitalOcean/VPS, $10-20/mo)

#### 1.2 Community Infrastructure (P0)
- GitHub Discussions enabled with categories: Feature Requests, Q&A, Show & Tell
- Discord server with channels: #general, #development, #support, #announcements, #self-hosting
- CONTRIBUTING.md — clear PR workflow, code style, commit conventions
- CODE_OF_CONDUCT.md — standard Contributor Covenant
- CLA — Apache-style Contributor License Agreement (first PR protection)
- ISSUE_TEMPLATE.md — bug report + feature request templates
- Good-first-issue labels on 10+ issues

#### 1.3 Pricing Page (P0)
- Public at /pricing: "Self-Hosted: $0" / "Cloud: $29/seat/mo" / "Enterprise: Custom"
- Feature comparison table
- FAQ: What's included, migration help, support SLAs

#### 1.4 Performance Baseline (P1)
- pgbench for database performance (10K, 50K, 100K records)
- k6 load test for API endpoints (GET /api/contacts, POST /api/leads, search)
- Document breaking points and optimization recommendations
- Target: <200ms p95 for list endpoints, <500ms for search, <2s for import

#### 1.5 Dogfooding (P1)
- Use Sovereign CRM to track Sprint 4 tasks
- Create sample records: bugs found, features built, daily notes
- Validate that the product can manage its own development

#### 1.6 Launch Assets (P1)
- 5-slide pitch deck (problem, solution, differentiator, pricing, team)
- Product Hunt listing (screenshots, tagline, first comment)
- Hacker News Show HN post draft
- r/selfhosted, r/opensource, r/CRM launch posts
- Demo video (<2 min walkthrough)

#### 1.7 Self-Hosting Polish (P2)
- `docker compose up` works in <30 seconds
- Documentation: minimum system requirements, backup/restore, upgrade path
- Health check endpoint (`GET /api/health`)
- First-run setup wizard improvement

---

## 3. WORKSTREAM 2: EMAIL & SSO (Option A + Core Gaps)

**Goal:** Table-stakes CRM features that unlock enterprise conversations.

### Tasks

#### 2.1 Email Integration (Backend) — P0

**2.1.1 IMAP Sync Engine**
- Connect to Gmail/Outlook via IMAP + OAuth2
- Sync emails to database (from, to, cc, bcc, subject, body, attachments, timestamps)
- Link emails to contacts by matching sender/recipient
- Periodic sync (5-min intervals) with last-sync timestamp
- Rate limiting: Gmail (2500/day/user), Outlook (10000/day)

**2.1.2 Graph API / Gmail API**
- Fallback to REST API when IMAP is unavailable
- Push notifications via webhooks (Gmail Pub/Sub, Outlook notifications)
- Real-time email sync (<30 second delay)

**2.1.3 Send Email API**
- Outbound email via SMTP (OAuth2 or app password)
- Email template engine (merge fields: {{contact.name}}, {{deal.name}})
- Track opens via 1x1 pixel, clicks via URL rewrite
- Store sent emails in timeline

**2.1.4 Email Sequences (Basic)**
- Multi-step email sequence builder
- Step types: send email, wait (X days), condition (opened/clicked/replied)
- Enroll contacts in sequences
- Sequence analytics: open rate, reply rate, click rate
- **Note:** This is a differentiated feature from Twenty and EspoCRM (both missing)

#### 2.2 SSO & Authentication (P0)

**2.2.1 Google OAuth**
- "Sign in with Google" button on login page
- Auto-provision tenant for Gmail domain matches
- Token refresh for email API

**2.2.2 SAML/SSO (Enterprise)**
- SAML 2.0 SP-initiated flow
- Support: Okta, Azure AD, Google Workspace, OneLogin
- IdP metadata upload via admin UI
- Just-in-time provisioning (auto-create user on first SSO login)
- **This unlocks the enterprise segment**

#### 2.3 Migration Import Wizard (P1)

**2.3.1 Salesforce CSV Import**
- Standard Salesforce object export → mapping UI → import
- Object mapping: Contact, Account, Lead, Opportunity, Task
- 100k record test

**2.3.2 HubSpot Import**
- HubSpot contacts/deals/companies export → mapping
- Handle HubSpot's custom property structure

**2.3.3 Generic CSV/Excel Import (Improve Existing)**
- Schema detection (auto-map column names to fields)
- Error report with line-level failures
- Duplicate detection (by email)

#### 2.4 Export (P1)
- Full data export: Contacts, Organizations, Deals, Leads → CSV/Excel
- Include related timeline/activities
- Scheduled exports (daily/weekly via cron)

#### 2.5 Calendar Integration (P2)
- Google Calendar read-only: show events on contact/deal timeline
- Outlook Calendar read-only

---

## 4. WORKSTREAM 3: AI CO-PILOT (Option B + Differentiator)

**Goal:** Make Sovereign CRM intelligent — the differentiator that no open-source CRM has.

### Tasks

#### 3.1 MCP Server — Model Context Protocol (P0)
- Expose CRM tools via MCP protocol
- Tools: search_contacts, get_deal, create_lead, update_contact, list_pipelines, run_report
- Authentication: pass through JWT from parent request
- Auto-discovery for MCP-compatible clients (Claude Desktop, Cursor, custom agents)
- **This is the foundation for all AI features**

#### 3.2 AI Chat API (P0)

**3.2.1 Natural Language → Query**
- "Show me all deals over $50k that are stuck in negotiation"
- "Who hasn't been contacted in the last 30 days?"
- Translate NL to SQL/API calls using LLM
- Permission-checked: only query records user has access to

**3.2.2 Natural Language → Action**
- "Create a new lead for Acme Corp, Tom is the contact"
- "Move the BigCo deal to won and close it"
- Execute actions with confirmation step

**3.2.3 Multi-Provider Support**
- Ollama (local, default)
- OpenAI
- Anthropic
- User-configurable: provider, model, endpoint, API key

#### 3.3 AI Insight Engine (P1)

**3.3.1 Deal Risk Detection**
- Stale deals (no activity in X days)
- Stuck stages (deal hasn't moved in >2x expected duration)
- Amount drop (deal amount decreased)
- Competitor detected (new lead/contact from known competitor domain)

**3.3.2 Pipeline Health**
- Bottleneck stages (high concentration of deals)
- Velocity analysis (avg days per stage)
- Conversion rates (stage-to-stage, stage-to-won)

**3.3.3 AI Assistant Cards**
- Insight cards on dashboard: "3 deals at risk this week"
- Deal page sidebar: "Next best action: send proposal to Tom"
- Contact page: "Last contacted 14 days ago — due for follow-up"

#### 3.4 Report Builder (P1)

**3.4.1 Report API**
- Tabular, summary (pivot), chart (bar/line/pie/funnel)
- Filters: date range, user, stage, source, any custom field
- Grouping: by owner, stage, source, month, quarter
- Metrics: count, sum, avg, min, max, conversion rate

**3.4.2 Dashboard Builder (Basic)**
- Widget layout (grid-based)
- Widget types: chart, metric card, recent activity, pipeline summary
- Save/Load dashboards per user
- Multiple dashboard tabs

#### 3.5 AI Data Enrichment (P2)
- Auto-enrich contacts from email domain (company name, industry, size)
- Suggest tags/categories based on email content
- Detect email sentiment (positive/negative/neutral) on replies

---

## 5. WHAT WE'RE NOT DOING (Anti-Bloat Guard)

These were explicitly identified during research but excluded from Sprint 4 scope:

| Deferred Feature | Rationale | Future Sprint |
|-----------------|-----------|:-------------:|
| Native mobile app | Needs dedicated engineering; PWA + responsive first | Sprint 5 |
| Customer Success module (health score, NPS, playbooks) | Requires CS domain expertise; no existing need validated | Sprint 6 |
| Vertical modules (IT Consulting, SaaS) | Premature without market validation of core | Sprint 5+ |
| Document template engine | Low vote from research; nice-to-have | Sprint 6 |
| Workflow engine (if-this-then-that) | Complex; better to ship and iterate based on actual usage | Sprint 6 |
| Conversation intelligence (call recording) | Requires SIP/telephony integration | Sprint 7 |
| CRDT sync (local-first) | Aspirational vision, not yet validated as needed | Sprint 8+ |
| Multi-region deployment | Not needed until first enterprise customer ships | Post-MVP |

---

## 6. RISK ASSESSMENT (Pre-mortem)

| Risk | Likelihood | Impact | Severity | Mitigation |
|------|:----------:|:------:|:--------:|-----------|
| Email OAuth complexity sinks timeline | HIGH | HIGH | CRITICAL | Start IMAP/SMTP first (3 days), then add Graph API |
| AI co-pilot quality is poor without data | MEDIUM | HIGH | HIGH | Ship insight engine first (rule-based), then add LLM layer |
| Demo deployment gets no traffic | HIGH | HIGH | HIGH | Cross-post to 4+ communities on day 1; $50 in ads if needed |
| Pipeline stages migration conflicts with existing data | MEDIUM | HIGH | HIGH | Run migration on fresh DB; document rollback path |
| SAML vendor compatibility issues | MEDIUM | MEDIUM | MEDIUM | Test against Okta free tier first; one provider at a time |
| Community infra doesn't get engagement | HIGH | MEDIUM | MEDIUM | Good-first-issue labels + dedicated onboarding channels |
| Docker compose doesn't work on Windows | MEDIUM | HIGH | HIGH | Test on Windows Docker Desktop + WSL2 before launch |
| Report builder scope creeps into BI tool | MEDIUM | LOW | LOW | Set strict scope: no pivot tables, calculated fields, or scheduled reports |

---

## 7. WEEK-BY-WEEK BREAKDOWN

### Week 1 (Days 1-6): Foundation + Infrastructure

| Day | W1: Launch | W2: Email & SSO | W3: AI & Analytics |
|:---:|-----------|-----------------|--------------------|
| 1 | `docker-compose.yml` + deploy demo | — | — |
| 2 | GitHub Discussions + Discord + CLA | IMAP sync engine start | — |
| 3 | Pricing page + CONTRIBUTING.md | IMAP sync engine finish | MCP server skeleton |
| 4 | Performance baseline (pgbench + k6) | OAuth2 flow (Google) | MCP tools registration |
| 5 | Dogfood: Sprint 4 tracking inside CRM | SAML SP-initiated flow start | AI Chat API — NL→Query |
| 6 | Launch assets draft (PH, HN, Reddit posts) | IMAP→contact linking | AI Chat API — NL→Action |

### Week 2 (Days 7-12): Core Features

| Day | W1: Launch | W2: Email & SSO | W3: AI & Analytics |
|:---:|-----------|-----------------|--------------------|
| 7 | Self-hosting docs + first-run polish | Send email API | Ollama integration |
| 8 | Issue templates + good-first-issues | Email template engine | Deal risk detection |
| 9 | Demo video <2 min | Email sequences (basic) | Pipeline health engine |
| 10 | Product Hunt + HN listing prep | Migration import wizard (SF) | Insight cards UI |
| 11 | r/selfhosted + r/opensource launch post | Migration import wizard (HubSpot) | Report builder API |
| 12 | Monitor + triage first user feedback | Calendar sync (read-only) | Dashboard builder API |

### Week 3 (Days 13-18): Polish + Ship

| Day | W1: Launch | W2: Email & SSO | W3: AI & Analytics |
|:---:|-----------|-----------------|--------------------|
| 13 | Fix top 3 UX issues from feedback | SMS/Push export | Report builder UI (list) |
| 14 | Performance fixes from baseline | Data export (CSV, Excel) | Dashboard builder UI |
| 15 | Second demo deployment (EU region) | Email open tracking + analytics | AI enrichment (domain→company) |
| 16 | Update pricing based on feedback | Email sequence analytics | Integration tests |
| 17 | Blog post: "Building an open-source CRM in 2026" | SSO integration test suite | Performance test: 1M record reports |
| 18 | Sprint review + retrospective + Sprint 5 planning | Ship email sidebar in UI | Ship AI co-pilot in sidebar |

---

## 8. ACCEPTANCE CRITERIA

### Hard Gates (Required for Sprint 4 Completion)

| # | Criterion | Workstream | How to Verify |
|:-:|-----------|:----------:|-------------|
| 1 | `docker compose up` deploys full stack in <30 seconds | W1 | Run on fresh VPS; time from command to login |
| 2 | demo.sovereigncrm.com is live and functional | W1 | Visit URL; create contact, lead, deal |
| 3 | Pricing page published at /pricing | W1 | Public URL with 3 tiers + FAQ |
| 4 | GitHub Discussions + Discord live with 10+ posts | W1 | Visit each platform |
| 5 | CLA + CONTRIBUTING.md + CODE_OF_CONDUCT.md in repo | W1 | Files exist in root of repo |
| 6 | Performance baseline documented: <200ms p95 list, <500ms search | W1 | k6 report published |
| 7 | Email sync working: Gmail IMAP + OUTLOOK IMAP | W2 | Sync 50 emails; verify linked to contacts |
| 8 | Send email from CRM via SMTP | W2 | Send test; verify received in Gmail/Outlook |
| 9 | Google OAuth login works | W2 | "Sign in with Google" → creates user → logs in |
| 10 | SAML login works with Okta | W2 | SP-initiated SSO → Okta → redirect to CRM |
| 11 | CSV import handles 10k records with error report | W2 | Import 10k contacts; verify error report + dedup |
| 12 | MCP server responds to search_contacts + get_deal | W3 | MCP client connects; tools respond correctly |
| 13 | AI Chat answers "Show me deals over $50k stuck in negotiation" | W3 | Query returns correct results |
| 14 | Deal risk detection flags stale deals (>30d no activity) | W3 | Insert old deal; verify insight card appears |
| 15 | Report builder returns tabular report for contacts by owner | W3 | POST to /api/reports with filter; verifiable output |
| 16 | Dashboard builder creates 2-widget layout | W3 | Create dashboard; add pipeline + activity widgets |
| 17 | At least 1 non-developer signs up for demo and uses it | W1 | Google Analytics or manual check |
| 18 | Sprint 4 tracked inside Sovereign CRM (dogfood proof) | W1 | Export Sprint 4 task list from CRM |

### Soft Gates (Desired but Not Blocking)

| # | Criterion | Workstream |
|:-:|-----------|:----------:|
| 1 | 5+ GitHub stars on repo | W1 |
| 2 | 3+ Discord members | W1 |
| 3 | 1+ feature request from external user | W1 |
| 4 | Email sequence works end-to-end (enroll → send → track) | W2 |
| 5 | AI Chat correctly handles 10 NL queries in a row | W3 |

---

## 9. DEPENDENCIES

| Task | Depends On | Blocking |
|------|-----------|:--------:|
| Demo deployment (W1.1) | Docker compose, SSL cert, VPS | W1.4, W1.5, W1.7 |
| Email sync (W2.1) | OAuth2 flow, IMAP library | W2.3 (migration with email) |
| Email sequences (W2.1.4) | Email sync + send + template | — |
| SAML SSO (W2.2.2) | Auth middleware improvements | W2.2.1 (Google OAuth) |
| Migration import (W2.3) | Existing import/export code | W2.3.1 (SF), W2.3.2 (HubSpot) |
| MCP server (W3.1) | Go MCP library | W3.2, W3.3 |
| AI Chat (W3.2) | MCP server, LLM provider config | W3.4 |
| Report builder (W3.4) | Existing contact/lead/deal APIs | W3.5 |
| Dashboard builder (W3.5) | Report builder API | — |
| AI enrichment (W3.5) | Domain parsing, email analysis | — |

---

## 10. EFFORT ESTIMATE

| Workstream | Backend (days) | Frontend (days) | Total (days) |
|-----------|:--------------:|:---------------:|:------------:|
| W1: Launch Foundation | 3 | 4 | 7 |
| W2: Email & SSO | 12 | 6 | 18 |
| W3: AI & Analytics | 10 | 5 | 15 |
| **Total** | **25** | **15** | **40** |

**Note:** As a solo developer, this is ~3-4 weeks of effort. The sprint plan above is aspirational for a single developer. **Recommended: prioritize W1 completely, then W2 (Email + SSO) as the primary feature work, and deliver W3 (AI) at the "basic but functional" level.** If anything must be cut, reduce W3 to MCP server + basic insight engine only, defer the report/dashboard builder to Sprint 5.

---

## 11. CONSTITUTION CHECK

| Question | Answer |
|----------|--------|
| **What problem does this solve?** | CRM users are trapped between expensive cloud CRMs (SF/HubSpot) and painful open-source ones (SuiteCRM). Sovereign provides modern UX + email + AI at a fraction of the cost. |
| **Why is this different from existing solutions?** | No open-source CRM combines email+sequences + SSO + AI co-pilot + transparent pricing + excellent self-hosting. This sprint closes the gap. |
| **What is the simplest version?** | Email sync + Google OAuth + basic AI chat. Everything else is layered on proven foundations. |
| **How do we measure success?** | 18 acceptance criteria above. Key metric: 1+ non-developer using the demo. |
| **What is the maintenance cost?** | Email sync requires OAuth token refresh, IMAP connection management. AI requires LLM provider API keys. Estimated $20-50/mo infra for demo. |
| **What would make this fail?** | Email OAuth complexity, AI quality with sparse data, or zero community engagement. Pre-mortem controls in place. |

---

## 12. APPROVAL & EXECUTION

**Sprint 4 Go / No-Go Gates:**
1. ✅ Research complete and synthesized into this plan
2. ❐ User approves this Sprint 4 plan
3. ❐ Pre-mortem reviewed and mitigations accepted
4. ❐ Anti-bloat guard reviewed (what's NOT in scope)
5. ❐ All three workstreams resourced (solo dev = staged delivery)

**Once approved, execution follows:**
1. Create blueprint markdown in vault/blueprints/sprint-4/
2. Create GitHub issues for each task
3. Daily progress tracking in Sovereign CRM (dogfood)
4. EOD updates: what shipped, what blocked, what changed
5. Mid-sprint checkpoint (Day 9): review scope, cut if needed
6. End-of-sprint: demo + review + Sprint 5 planning

---
*Sprint 4 plan produced using: Market research (Reddit, GitHub, G2, PH, Gartner/Forrester) + Portfolio Review (Sprint 3) + Sprint Breakdown (Phase 14) + Big 4 methodology*
