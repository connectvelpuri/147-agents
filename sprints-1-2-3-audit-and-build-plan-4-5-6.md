# Sprints 1-3 Audit + Sprints 4-5-6 Build Plan

**Date:** 2026-06-06
**Author:** Hermes Agent (Big 4 Methodology Review)
**Status:** AWAITING USER APPROVAL BEFORE EXECUTION

---

## PART 1: SPRINTS 1-3 AUDIT — What Was Actually Delivered?

### 1.1 Sprint Structure Confusion

The sprint-breakdown.md defines Sprints 1-3 as **BUILD sprints** (8 weeks each):
- Sprint 1: Foundation (Auth, Users, Roles)
- Sprint 2: Core CRM (Contacts, Orgs, Deals, Pipeline)
- Sprint 3: Sales Operations (Email, Calendar, Sequences, Workflows)

But the portfolio-review-sprint-3.md treats them as **PLANNING sprints** and says:
> "The initiative has achieved exceptional sprint velocity and technical execution across Sprints 1-3."

**Reality:** Sprints 1-3 produced BOTH planning documents AND code, but with significant gaps in each.

---

### 1.2 Planning Deliverables Audit (Vault Documents)

| Document | Size | Status | Quality |
|----------|------|--------|---------|
| CONSTITUTION.md | 18KB | Complete | Excellent — anti-bloat framework, standing committees |
| PROJECT_BRIEF.md | 6KB | Complete | Good — full blueprint |
| blueprints/first-principles-analysis.md | 20KB | Complete | Excellent — 600+ dimensions |
| blueprints/architecture/ (7 files) | 120KB | Complete | Strong — AI, API, security, info architecture |
| blueprints/data-model/complete-data-model.md | 50KB | Complete | Strong — full schema |
| blueprints/personas/17-user-personas.md | 25KB | Complete | Speculative — 17 personas, 0 validated |
| blueprints/processes/ (2 files) | 60KB | Complete | Theoretical — 52 processes, 0 tested |
| blueprints/implementation/sprint-breakdown.md | 13KB | Complete | Misaligned — plans 8-week sprints, actual was faster |
| blueprints/implementation/sprint-4-plan.md | 23KB | Complete | Over-scoped — includes AI, analytics, email, SSO |
| committees/ (5 charters) | 28KB | Complete | Over-engineered — 5 committees, 1 person |
| research/competitors/ (5 files) | 30KB | Complete | Good — Salesforce, HubSpot, Zoho, LeadSquared |
| research/market_trends/ | 9KB | Complete | Narrow — only IT consulting + SaaS |
| methodology-gap-analysis.md | 11KB | Complete | Valuable — 8 gaps vs Big 4 standards |
| portfolio-review-sprint-3.md | 21KB | Complete | Critical — identifies existential risks |
| customer-pre-mortem.md | 10KB | Complete | Speculative — 98 questions, 0 answered |
| sales-kit/ (6 files) | 20KB | Complete | premature — demo scripts for undeployed product |
| strategic-review-and-sprints-4-5-6.md | 32KB | Complete | Over-scoped — combines too many concerns |

**Planning Assessment:** 53 documents, 600KB+ of strategy. The depth is impressive but there's a fundamental problem: **most of it is speculative.** Personas aren't validated. Processes aren't tested. Competitive analysis is desk research, not customer feedback.

---

### 1.3 Code Deliverables Audit

#### API (Go) — 21 files, 17MB binary

| Component | Files | Lines | Status | Notes |
|-----------|:-----:|:-----:|:------:|-------|
| Auth (JWT, register, login) | 3 | 350 | FUNCTIONAL | Missing MFA, password reset |
| RBAC middleware | 1 | 150 | FUNCTIONAL | Permission check works |
| User CRUD | 1 | 240 | FUNCTIONAL | Full CRUD |
| Role CRUD | 1 | 193 | PARTIAL | Update/Delete are stubs |
| Contact CRUD | 1 | 353 | FUNCTIONAL | Dedup via hash |
| Organization CRUD | 1 | 213 | FUNCTIONAL | Full CRUD |
| Lead CRUD + scoring | 1 | 622 | FUNCTIONAL | 7-factor scoring |
| Deal CRUD + pipeline | 1 | 685 | FUNCTIONAL | Stage movement, forecast |
| Activity CRUD | 1 | 105 | PARTIAL | Basic implementation |
| Custom Fields | 1 | 144 | FUNCTIONAL | JSONB, 9 types |
| Webhooks | 1 | 195 | FUNCTIONAL | 8 event types |
| Global Search | 1 | 98 | STUB | Basic tsvector |
| Import/Export | 1 | 227 | STUB | Placeholder code |
| Database migrations | 6 | 120KB | FUNCTIONAL | 19 tables, seed data |
| **TOTAL** | **21** | **~3,500** | | |

#### Frontend (Next.js) — 22 pages, 3 components

| Page | Lines | Status | Notes |
|------|:-----:|:------:|-------|
| Dashboard | 156 | FUNCTIONAL | API-connected |
| Contacts (list/new/detail) | 482 | FUNCTIONAL | 3 pages |
| Organizations (list/new) | 180 | PARTIAL | New page is UI-only |
| Deals (list/detail) | 199 | FUNCTIONAL | 2 pages |
| Leads (list/new/detail) | 269 | FUNCTIONAL | 3 pages |
| Pipeline (kanban) | 132 | FUNCTIONAL | Drag-drop |
| Login | 115 | UI-ONLY | No API integration |
| Setup | 171 | FUNCTIONAL | Onboarding wizard |
| Pricing | 110 | UI-ONLY | Static page |
| Admin (users/roles/custom-fields/webhooks) | 623 | MIXED | Some functional, some UI-only |
| **TOTAL** | **~2,800** | | |

#### Tests — 2 files, 6KB

| Test | Status | Notes |
|------|--------|-------|
| auth_test.go | SCAFFOLD | Basic structure |
| rbac_test.go | SCAFFOLD | Basic structure |
| E2E tests | NONE | |
| Integration tests | NONE | |
| Performance tests | NONE | |

**Code Assessment:** Sprint 1 (Auth/Users) is ~85% complete. Sprint 2 (Core CRM) is ~75% complete. Sprint 3 (Sales Operations) is ~10% complete — only the leads/deals/pipeline overlap with Sprint 2 exists. **No email, no calendar, no sequences, no workflows.**

---

### 1.4 Gap Matrix: Planned vs Delivered

| Sprint | Planned | Delivered | Gap |
|--------|---------|-----------|-----|
| **Sprint 1** | Auth, RBAC, Users, Roles, CI/CD, Docker, Tests | Auth, RBAC, Users, Roles, CI/CD, Docker | Missing: MFA, password reset, integration tests, staging env |
| **Sprint 2** | Contacts, Orgs, Deals, Pipeline, Leads, Activities, Search, Import/Export, Dynamic Objects | Contacts, Orgs, Deals, Pipeline, Leads, Activities, Search (basic), Import/Export (stub) | Missing: Dynamic Objects, soft-delete, E2E tests |
| **Sprint 3** | Email, Calendar, Templates, Sequences, Workflows, Approvals, Forecasting, Territories, Quotas | Leads/Deals/Pipeline (from Sprint 2 overlap) | Missing: EVERYTHING — email, calendar, templates, sequences, workflows, approvals, forecasting, territories, quotas |

---

### 1.5 Critical Findings

1. **Sprint 3 was never built.** The codebase has leads/deals/pipeline from Sprint 2, but zero Sprint 3 features (email, calendar, sequences, workflows).

2. **The portfolio review is accurate.** The product is a credible MVP for Sprints 1-2, but Sprint 3 (Sales Operations) is completely missing.

3. **The sprint-4-plan.md is over-scoped.** It bundles email, SSO, AI, analytics, and launch into one sprint — that's 3-4 sprints worth of work.

4. **No market validation.** 53 vault documents, 0 customer interviews, 0 beta users, 0 external feedback.

5. **The code compiles and the API runs** — but there's no guarantee the frontend connects properly, and there are no tests.

---

## PART 2: WHAT SHOULD SPRINTS 4-6 ACTUALLY BE?

### 2.1 Portfolio Review Recommendations (Prioritized)

The portfolio-review-sprint-3.md is clear:

> **Sprint 4:** "Validate + Launch" (2 weeks)
> - Deploy live demo
> - Run 10 customer discovery calls
> - Publish pricing page
> - Create community infrastructure

> **Sprint 5:** "Email + SSO + Migration"
> - Migration wizard (Salesforce/HubSpot CSV)
> - SSO/SAML
> - Email integration (IMAP/SMTP)
> - Product Hunt + HN launch

> **Sprint 6+:** "Mobile + AI + Extensions"
> - Mobile PWA with offline
> - Plugin/extension SDK
> - AI assistant

### 2.2 The Gap: Sprint 3 Was Never Built

The portfolio review assumes Sprint 3 features exist. They don't. We have two options:

**Option A: Build Sprint 3 features first, then validate**
- Pros: More complete product for demos
- Cons: More time without user feedback, risk of building wrong things

**Option B: Validate first, then build Sprint 3 features based on feedback**
- Pros: User feedback shapes what we build
- Cons: Demo is less impressive without email/calendar

**Recommendation: Option B.** The portfolio review is right — validation before features. A working CRM with contacts, deals, pipeline, and kanban is enough for a demo. Email and sequences are nice-to-have for the first conversation, not must-have.

---

## PART 3: SPRINTS 4-6 BUILD PLAN (CONCRETE)

### Sprint 4: "Deploy + Validate" (2 weeks)

**Goal:** Get the product in front of real users. Learn what they actually want.

#### Week 1: Deploy + Community (Days 1-5)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 1 | Fix frontend build + env config | `npm run build` succeeds | Zero build errors |
| 1 | Fix API-to-frontend connection | Frontend loads, shows data | Login works, dashboard shows contacts |
| 1 | Deploy demo via Docker | `podman-compose up` on a VPS | Public URL accessible |
| 2 | Seed realistic demo data | 50 contacts, 20 leads, 10 deals, 7 pipeline stages | Data looks like a real CRM |
| 2 | Create GitHub repo + push | sovereign-crm/sovereign on GitHub | Code is public, README works |
| 2 | Enable GitHub Discussions | Community tab active | Someone can post a question |
| 3 | Discord server setup | sovereign-crm Discord | Invite link works |
| 3 | Pricing page (real) | $0/5 users, $29/seat, enterprise | Page loads, tiers clear |
| 4 | Product Hunt draft | Listing ready to submit | Screenshot, tagline, description |
| 4 | Hacker News "Show HN" draft | Post ready to submit | Title, description, link |
| 5 | Demo script (5 min) | Written walkthrough | Shows key features |
| 5 | First tweet/thread | Announce open-source launch | Draft ready |

#### Week 2: Customer Discovery (Days 6-10)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 6-8 | 5 customer discovery calls | Recorded notes + insights | Learn: current CRM, pain points, willingness to pay |
| 6-8 | Reddit posts (r/selfhosted, r/CRM, r/SaaS) | 3 posts | Get feedback on product |
| 9-10 | Analyze all feedback | Findings document | Top 5 insights, roadmap impact |
| 10 | Sprint 4 retro | What we learned | Update roadmap based on feedback |

**Exit Criteria (Sprint 4):**
- [ ] Demo deployed at public URL
- [ ] GitHub repo live with 5+ stars
- [ ] Discord active with 3+ members
- [ ] 5 customer discovery calls completed
- [ ] Pricing page published
- [ ] Top 5 user insights documented

---

### Sprint 5: "Email + SSO + Core Gaps" (3 weeks)

**Goal:** Build the features users told us they need in Sprint 4.

#### Week 1: Email Integration (Days 1-5)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 1 | IMAP sync backend | Go handler for Gmail IMAP | Can read emails |
| 2 | SMTP send backend | Go handler for Gmail SMTP | Can send emails |
| 3 | Email-to-contact linking | Auto-link emails to contacts | Email appears on contact timeline |
| 4 | Email tracking (opens, clicks) | Pixel tracking + redirect links | Track open/click rates |
| 5 | Email template engine | Merge fields, categories | Create and send templated emails |

#### Week 2: SSO + Auth Gaps (Days 6-10)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 6 | Google OAuth | Login with Google | Works end-to-end |
| 7 | SAML/SSO | Enterprise SSO login | Works with test IdP |
| 8 | MFA (TOTP) | Two-factor authentication | Works with Google Authenticator |
| 9 | Password reset | Email-based reset flow | Works end-to-end |
| 10 | Auth hardening | Rate limiting, lockout, audit | Security review passed |

#### Week 3: Migration + Polish (Days 11-15)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 11 | CSV import (improved) | Field mapping, validation | Import 10k records |
| 12 | Salesforce CSV import | Map SF fields to Sovereign | Import SF export |
| 13 | HubSpot CSV import | Map HS fields to Sovereign | Import HS export |
| 14 | Data export (CSV, Excel) | Full export with filters | Export works |
| 15 | Sprint 5 retro + PH launch | Product Hunt submission | Live on PH |

**Exit Criteria (Sprint 5):**
- [ ] Email sync works (IMAP + SMTP)
- [ ] Google OAuth works
- [ ] SAML/SSO works
- [ ] MFA works
- [ ] Password reset works
- [ ] CSV import from Salesforce/HubSpot works
- [ ] Product Hunt launched
- [ ] 50+ GitHub stars

---

### Sprint 6: "Mobile + Workflows + Intelligence" (3 weeks)

**Goal:** Mobile access, automation, and basic AI — the features that make it a real CRM.

#### Week 1: Mobile PWA (Days 1-5)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 1 | PWA manifest + service worker | Installable on mobile | "Add to Home Screen" works |
| 2 | Responsive pipeline kanban | Touch-friendly drag-drop | Works on iPhone/Android |
| 3 | Responsive contacts/deals | Mobile-optimized list + detail | Readable on 375px screen |
| 4 | Offline support (basic) | Cache key pages | Works without WiFi |
| 5 | Push notifications | Web push for new leads/deals | Notification appears |

#### Week 2: Workflows + Sequences (Days 6-10)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 6 | Workflow engine backend | Trigger → Condition → Action | Create a rule |
| 7 | Workflow builder UI | Visual rule builder | Create rule without code |
| 8 | Email sequences backend | Step builder, enrollment, auto-advance | Enroll contact in sequence |
| 9 | Sequence analytics | Open rate, reply rate, click rate | View sequence performance |
| 10 | Sequence builder UI | Drag-drop steps | Create sequence without code |

#### Week 3: AI Foundation (Days 11-15)

| Day | Task | Deliverable | Acceptance Criteria |
|:---:|------|-------------|-------------------|
| 11 | Ollama integration | Connect to local Ollama | Query works |
| 12 | NL→SQL query | Ask questions, get data | "How many deals this month?" answered |
| 13 | Deal risk detection | AI flags at-risk deals | Risk score appears on deal page |
| 14 | Pipeline health insights | AI summarizes pipeline state | Insight card on dashboard |
| 15 | Sprint 6 retro + metrics | What worked, what didn't | Update roadmap |

**Exit Criteria (Sprint 6):**
- [ ] PWA installable on mobile
- [ ] Pipeline works on mobile
- [ ] Workflows create and execute
- [ ] Email sequences send and track
- [ ] Ollama integration works
- [ ] NL→SQL queries return correct answers
- [ ] Deal risk detection works
- [ ] 100+ GitHub stars

---

## PART 4: WHAT I GOT WRONG (AND WHAT I'LL FIX)

### What I Did Wrong

1. **Jumped into Sprint 4 execution** without auditing Sprints 1-3 deliverables
2. **Ignored the portfolio review's recommendation** to pivot Sprint 4 to "Validate + Launch"
3. **Created an over-scoped sprint-4-plan.md** that bundled 3-4 sprints into one
4. **Started fixing code** (compilation errors, Dockerfiles) before understanding the full picture
5. **Didn't ask for your approval** on the build plan before executing

### What I'll Do Differently

1. **Every sprint starts with a plan document** — you approve before I write code
2. **Every sprint ends with a retro** — what worked, what didn't, what to change
3. **No feature work without user validation** — Sprint 4 is about learning, not building
4. **Keep the vault clean** — one plan per sprint, no duplication
5. **Show, don't tell** — working demo > impressive documents

---

## PART 5: YOUR DECISION NEEDED

### Option A: Follow Portfolio Review (Recommended)
Sprint 4 = Deploy + Validate (2 weeks). No new features. Get users, learn what they want.

### Option B: Build Sprint 3 First
Sprint 4 = Build missing Sprint 3 features (email, calendar, sequences). Then validate in Sprint 5.

### Option C: Hybrid
Sprint 4 = Deploy demo + quick email integration (3 days) + validate (7 days).

---

**Awaiting your decision before proceeding with any execution.**
