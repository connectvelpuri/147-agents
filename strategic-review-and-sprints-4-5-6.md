# Strategic Review & Sprints 4-5-6 Plan

**Date:** 2026-06-06
**Methodology:** Big 4 strategy audit × Multi-persona × Pre-mortem × Zero-to-One
**Architecture:** Hybrid Supabase + Go API + Next.js + Podman + Ollama
**Stack:** Supabase (PostgreSQL + Auth) | Go (Business Logic API) | Next.js (UI) | Podman (Containers) | GitHub (Repo + CI) | Ollama (AI)

---

## PART I: STRATEGIC REVIEW OF SPRINTS 1-3

### What Was Built

| Sprint | Deliverables | Status |
|--------|-------------|--------|
| **Sprint 1** | Auth (JWT, register, login), Users CRUD, Roles CRUD, RBAC middleware, Audit logging, Tenant setup, Navigation shell, Login page, User management UI, Role management UI | Code exists, Go API doesn't compile |
| **Sprint 2** | Contacts CRUD, Organizations CRUD, Deals CRUD, Pipeline CRUD, Leads CRUD, Activities CRUD, Global search (tsvector), CSV Import/Export, Dynamic custom fields, Contact/Org detail pages, Pipeline Kanban, Lead management UI, Activity logging UI, Global search bar, Import wizard | Code exists, partial |
| **Sprint 3** | Custom fields & webhooks, Leads pipeline & deals, Forecasting engine, Kanban board, Setup wizard, Lead scoring (7-factor) | Code exists, tables created |

### Architectural Alignment Review

#### Current Architecture:

```
Browser → Next.js (port 3000) → Go API (port 8080) → PostgreSQL (5432)
                                                      ↕
                                                  Redis (6379) [unused]
```

#### Target Architecture (Post-Sprint 6):

```
Browser → Next.js → Supabase Auth (JWT) → Go API (business logic) → Supabase Postgres
                  ↘ Supabase Client (realtime, storage) ↗
                                             ↕
                                       Ollama (local LLM)
                                             ↕
                                  Email (SMTP/Gmail API)
```

### Critical Gaps in Sprints 1-3

| Gap | Impact | Requires |
|-----|--------|----------|
| **No git repository initialized** | Cannot deploy, cannot CI/CD, cannot accept contributions | `git init`, `.gitignore`, GitHub remote |
| **Go API doesn't compile** | Cannot build docker image, cannot deploy demo | Fix 12+ compilation errors |
| **No Dockerfiles for API or web** | Cannot containerize, cannot use Podman | Dockerfiles for both services |
| **No environment configuration** | API and frontend can't connect; no Supabase config | `.env` files, Supabase project setup |
| **Auth is custom Go JWT** | Duplicates Supabase Auth; need to migrate to Supabase Auth | Auth migration strategy |
| **Redis dependency but not used** | Unnecessary complexity; should remove or configure | Either integrate or remove |
| **No seed data for demo** | Manual data exists but not reproducible | Reliable seed script |
| **No monitoring/healthcheck** | Cannot detect email sync failures, DB issues | Health endpoints + Sentry |
| **No backup/restore** | Data loss risk for demo users | pg_dump script + docs |
| **Code quality issues** | 21 files, many with compilation errors | Full code audit + fix |
| **Frontend has no API client configured** | Can't connect to backend | .env.local with API URL |

### Decisions That Need Reversal

| Original Decision | New Direction | Rationale |
|-------------------|---------------|-----------|
| Go API handles auth (JWT, register, login) | Supabase Auth handles auth | Supabase provides Google OAuth, magic link, SSO out of box; saves weeks of work; enterprise-ready auth |
| Custom RBAC in Go middleware | Supabase RLS + Go layer | Supabase Row Level Security provides per-row permissions; Go API can add business-level RBAC on top |
| Redis required | Remove Redis dependency | Not used; adds complexity for demo; can add later when caching/queues are needed |
| docker-compose.yml | podman-compose.yml | User has Podman; Docker Compose syntax is compatible |

### Sprint 1-3 Retrospective Learnings

**What Went Well:**
- Data model is solid — 19 tables with proper migrations, enums, indexing, tsvector search
- Feature scope was ambitious but achieved — 3 sprints delivered a credible CRM backend
- Vault documentation is comprehensive — 52 documents show strategic thinking
- Custom fields via JSONB is a good architecture decision — extensible without schema changes

**What Could Have Been Better:**
- Should have initialized git and pushed to GitHub after Sprint 1
- Should have set up CI/CD after Sprint 1 — would have caught compilation errors immediately
- Should have written Dockerfiles during Sprint 1 deployment phase
- Should have aligned on auth strategy (custom vs Supabase) before building
- Should have validated the API compiles after each sprint — the current compilation failure means regressions went unnoticed

---

## PART II: TARGET ARCHITECTURE (Sprint 4-6)

### Technology Decisions

| Component | Choice | Why |
|-----------|--------|-----|
| **Database** | Supabase PostgreSQL (local or cloud) | Managed Postgres, built-in auth, RLS, realtime, storage; can run locally via `supabase start` |
| **Authentication** | Supabase Auth | Google OAuth, magic link, SAML/SSO (enterprise); replaces custom JWT code; free tier generous |
| **API (business logic)** | Go (existing) | Existing codebase; Go is fast, maintainable; handles complex operations Supabase can't (email sync, AI orchestration, report aggregation) |
| **Frontend** | Next.js (existing) | Existing codebase; integrates with Supabase JS SDK for auth + realtime |
| **Containers** | Podman (rootless) | User preference; Docker-compatible CLI; podman-compose for orchestration |
| **AI** | Ollama (local) + configurable provider | Open source; runs locally; can add OpenAI/Anthropic as configurable backends |
| **Email** | SMTP (generic) + Gmail API | SMTP for outbound; Gmail API/IMAP for sync |
| **Git** | GitHub | Community infra, CI/CD via GitHub Actions, issue tracking |
| **CI/CD** | GitHub Actions | Free for public repos; auto-build, test, deploy |

### Architecture Diagram

```
┌──────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Next.js     │────→│    Go API (chi)       │────→│  Supabase       │
│   (Frontend)  │     │    (Business Logic)   │     │  PostgreSQL     │
│               │     │                        │     │                 │
│  Supabase SDK │────→│  • Deals/Pipeline      │     │  • Data storage │
│  (auth client)│     │  • Email Sync          │     │  • Auth (users) │
└──────┬───────┘     │  • AI Orchestration    │     │  • RLS policies │
       │             │  • Reports/Dashboards  │     └────────┬────────┘
       │             │  • Import/Export        │              │
       ▼             └──────────┬──────────────┘              │
┌──────────────┐               │                              │
│  Supabase    │               ▼                              │
│  Auth (UI)   │     ┌──────────────────┐                     │
│  Login/SSO   │     │  Ollama (local)   │                    │
└──────────────┘     │  (or OpenAI/etc)  │                    │
                     └──────────────────┘                     │
                                                              │
┌──────────────┐                                              │
│  Gmail IMAP/ │──────────────────────────────────────────────┘
│  SMTP        │
└──────────────┘
```

### Migration Plan: Custom Auth → Supabase Auth

| Step | What | Effort |
|------|------|--------|
| 1 | Create Supabase project (local or cloud) | 30 min |
| 2 | Link Supabase auth to existing users table | 2 hrs |
| 3 | Remove Go JWT generation/verification code | 4 hrs |
| 4 | Add Supabase JS SDK to frontend | 2 hrs |
| 5 | Update Go API to validate Supabase JWT | 3 hrs |
| 6 | Add Google OAuth provider in Supabase dashboard | 15 min |
| 7 | Test full auth flow (register, login, OAuth) | 2 hrs |

---

## PART III: SPRINT 4 DETAILED PLAN

### Theme: "Launch + Email + Auth Migration"

**Duration:** 3 weeks
**Supabase integration:** YES (auth + database)
**Podman deployment:** YES
**Git/GitHub setup:** YES

### Week 1: Foundation & Git Setup

| Day | Task | Details | Dependencies |
|:---:|------|---------|:------------:|
| 1 | **Git init + GitHub remote** | `git init`, create `.gitignore`, `git add`, `git commit`, push to GitHub | None |
| 2 | **Fix Go API compilation** | Fix all ~12 compilation errors (missing functions, broken struct tags, import issues) | Git repo |
| 3 | **Dockerfiles** | Write Dockerfile for Go API (multi-stage build, ~20MB binary) + Dockerfile for Next.js | Go API compiles |
| 4 | **Supabase project setup** | Create Supabase project (local: `supabase init`, or cloud: supabase.com dashboard) | Git repo |
| 5 | **Auth migration** | Link Supabase Auth to existing users table; remove Go JWT code; add Supabase SDK to frontend | Supabase project |
| 6 | **Podman compose** | Write podman-compose.yml (API + web + Supabase services); test full stack starts | Dockerfiles, Supabase |

### Week 2: Email Sync & Demo Deployment

| Day | Task | Details | Dependencies |
|:---:|------|---------|:------------:|
| 7 | **SMTP email send** | Go API: send email via SMTP (Gmail app password); template engine with merge fields | Go API compiles |
| 8 | **IMAP email receive** | Go API: sync inbox; link to contacts by email match; store in database | SMTP working |
| 9 | **Email sidebar in frontend** | UI: inbox view, send email, thread view; link to contact timeline | IMAP working |
| 10 | **Demo deployment** | Deploy to VPS via Podman; demo.sovereigncrm.com live; seed with 50 contacts, 20 leads, 10 deals | Full stack working |
| 11 | **Pricing page** | /pricing page: $0 self-hosted / $29 cloud / Custom enterprise; feature table; FAQ | Demo live |
| 12 | **Community infra** | GitHub Discussions + Discord + CONTRIBUTING.md + CLA + CODE_OF_CONDUCT.md + issue templates | GitHub repo |

### Week 3: SSO + Polish + Launch

| Day | Task | Details | Dependencies |
|:---:|------|---------|:------------:|
| 13 | **Google OAuth via Supabase** | Supabase Auth: enable Google provider; test sign-in flow | Supabase project |
| 14 | **SAML SSO (Okta)** | Supabase Auth SAML; SP-initiated flow; metadata upload UI | Google OAuth working |
| 15 | **Performance baseline** | k6 load test (list, search, create); pgbench; document breaking points | Demo live |
| 16 | **Migration import (Salesforce)** | CSV import wizard: map standard SF objects → Sovereign entities; 10k record test | Import/export code exists |
| 17 | **Healthcheck + monitoring** | `GET /api/health` endpoint; Sentry error tracking; pg_stat_statements | API compiles |
| 18 | **Product Hunt + HN + Reddit launch** | PH listing, Show HN post, r/selfhosted + r/opensource posts; track feedback | Everything above |

### Sprint 4 Acceptance Criteria

- [ ] GitHub repo initialized and pushed
- [ ] Go API compiles and runs
- [ ] Dockerfiles for API and web build successfully
- [ ] Supabase project created, auth working (email + Google OAuth)
- [ ] Old Go JWT auth code removed, Supabase auth integrated
- [ ] Podman compose starts full stack in <30 seconds
- [ ] SMTP email sending works (test: send from CRM, receive in Gmail)
- [ ] IMAP email sync works (test: sync 50 emails, verify linked to contacts)
- [ ] Email sidebar shows inbox, allows send
- [ ] demo.sovereigncrm.com is live and functional
- [ ] Pricing page published
- [ ] GitHub Discussions + Discord live
- [ ] Google OAuth login works
- [ ] SAML login works (Okta)
- [ ] Performance baseline documented
- [ ] CSV import handles 10k records
- [ ] Healthcheck + Sentry configured
- [ ] Product Hunt / HN / Reddit posts published

---

## PART IV: SPRINT 5 PLAN

### Theme: "AI Co-pilot + Email Sequences + Reports"

**Duration:** 3 weeks
**Prerequisites:** Sprint 4 complete (email working, demo live, auth on Supabase)

### The "Why Now"

- Sprint 4 gives us users (demo signups) and email (data gravity)
- Sprint 5 adds AI (differentiator) and sequences (retention)
- By Sprint 5, we'll have enough user feedback to prioritize which AI features matter most
- Report builder is demanded by market (Twenty GitHub #7451, r/sales)

### Week 1: AI Foundation

| Day | Task | Details |
|:---:|------|---------|
| 1 | **Ollama integration** | Go API: connect to Ollama API; configurable model, endpoint, provider (Ollama default, OpenAI/Anthropic optional) |
| 2 | **MCP server** | Expose CRM tools via MCP protocol: search_contacts, get_deal, create_lead, update_contact, list_pipelines |
| 3 | **AI Chat (NL→Query)** | Go API: natural language to SQL/API calls; permission-checked; return results as formatted response |
| 4 | **AI Chat UI** | Chat sidebar in frontend; message history; clear results display; "ask a question" input |
| 5 | **AI Chat (NL→Action)** | Go API: "Create a lead for Acme Corp" → validate → execute; confirmation step for destructive actions |
| 6 | **Multi-provider config UI** | Settings page: provider selection (Ollama/OpenAI/Anthropic), model, endpoint, API key |

### Week 2: Email Sequences & Insights

| Day | Task | Details |
|:---:|------|---------|
| 7 | **Email sequence engine** | Multi-step: send email, wait (X days), condition (opened/clicked/replied) |
| 8 | **Sequence builder UI** | Drag-and-drop step editor; template selection; enrollment UI |
| 9 | **Open/click tracking** | 1x1 pixel for opens; URL rewrite for clicks; analytics per step |
| 10 | **Deal risk detection** | Stale deals (>14d no activity), stuck stages (>2x expected), amount drops |
| 11 | **Pipeline health engine** | Bottleneck stages, velocity analysis, stage conversion rates |
| 12 | **Insight cards UI** | Dashboard: at-risk deals, stale leads, next-best-action suggestions |

### Week 3: Reports & Launch Polish

| Day | Task | Details |
|:---:|------|---------|
| 13 | **Report builder API** | Tabular, summary (pivot), chart (bar/line/pie/funnel); filters, grouping, metrics |
| 14 | **Report builder UI** | Drag-drop field selector; live preview; save/share reports |
| 15 | **Dashboard builder API** | Grid-based widget layout; widget types: chart, metric card, recent activity, pipeline summary |
| 16 | **Dashboard builder UI** | Add/remove widgets; resize; save multiple dashboards; per-user |
| 17 | **AI enrichment (basic)** | Auto-enrich from email domain: company name, industry, size estimate |
| 18 | **Sprint review + user feedback triage** | Review first 30 days of feedback; adjust Sprint 6 plan |

### Sprint 5 Acceptance Criteria

- [ ] Ollama connection working (local LLM answers questions)
- [ ] MCP server responds to all CRM tools
- [ ] AI Chat answers 10/10 test queries correctly
- [ ] AI Chat creates a lead via NL→Action (with confirmation)
- [ ] Provider config UI allows switching between Ollama/OpenAI/Anthropic
- [ ] Email sequence sends 3-step sequence and tracks opens/clicks
- [ ] Deal risk detection flags a stale deal correctly
- [ ] Pipeline health shows bottleneck stages and velocity
- [ ] Insight cards appear on dashboard
- [ ] Report builder creates tabular + chart reports
- [ ] Dashboard builder creates 2+ widget layouts
- [ ] AI enrichment fills company/industry from email domain

---

## PART V: SPRINT 6 PLAN

### Theme: "Mobile + Customer Success + Polish"

**Duration:** 3 weeks
**Prerequisites:** Sprint 5 complete (AI working, sequences shipping, reports live)

### The "Why Now"

- By Sprint 6, we'll have ~3 months of user feedback from the demo
- Mobile is the #1 complaint in CRM reviews (r/sales, r/CRM, G2)
- Customer Success module is a gap NO open-source CRM fills
- Polish and stability will determine whether early users stay or churn

### Week 1: Mobile PWA

| Day | Task | Details |
|:---:|------|---------|
| 1 | **PWA shell** | Service worker, manifest.json, offline fallback page, app install prompt |
| 2 | **Mobile-responsive contacts** | Mobile-optimized contact list with swipe actions; quick-add FAB |
| 3 | **Mobile-responsive deals** | Pipeline view for mobile; deal card with key fields; drag-to-move simplified |
| 4 | **Mobile-responsive email** | Inbox for mobile; quick reply; swipe to archive |
| 5 | **Push notifications** | Web push API; notify on new email, deal stage change, task due |
| 6 | **Mobile testing** | Test on iOS Safari, Android Chrome, responsive breakpoints |

### Week 2: Customer Success Module

| Day | Task | Details |
|:---:|------|---------|
| 7 | **Health score engine** | Configurable metrics: login frequency, email engagement, deal velocity, support tickets; weighted calculation |
| 8 | **Health score UI** | Customer list with health indicator (red/yellow/green); drill-down to factors |
| 9 | **NPS survey** | Send NPS survey via email; collect responses; dashboard with score trend |
| 10 | **Success playbooks** | Trigger-based: "If health drops to yellow, create task: call customer" |
| 11 | **Playbook builder UI** | Visual condition→action tree; enroll customers in playbooks |
| 12 | **Customer timeline** | Unified view: emails, calls, deals, support tickets, NPS responses, health changes |

### Week 3: Platform & Polish

| Day | Task | Details |
|:---:|------|---------|
| 13 | **OpenAPI spec** | Document all Go API endpoints in OpenAPI 3.0; serve from /api/docs |
| 14 | **Plugin SDK (foundation)** | Define plugin interface (webhooks + custom routes + custom UI panels); documentation |
| 15 | **Performance optimization** | Query optimization (EXPLAIN ANALYZE on all slow queries); connection pooling tuning; CDN for static assets |
| 16 | **Backup/restore automation** | pg_dump script; restore procedure documentation; test on demo instance |
| 17 | **User onboarding v2** | Guided first-run: import contacts → create pipeline → add team members → send first email |
| 18 | **Sprint review + community roadmap** | Publish public roadmap; prioritize top 10 feature requests from community |

### Sprint 6 Acceptance Criteria

- [ ] PWA installs on iOS and Android home screen
- [ ] Mobile contact list + deal pipeline work offline (cached data)
- [ ] Push notifications arrive on new email and deal updates
- [ ] Health score engine calculates score from configurable metrics
- [ ] Health dashboard shows customer list with color indicators
- [ ] NPS survey sends, collects, and displays results
- [ ] Success playbooks trigger on health score changes
- [ ] Customer timeline shows unified activity feed
- [ ] OpenAPI spec published at /api/docs
- [ ] Plugin SDK documented with example plugin
- [ ] All slow queries optimized (sub-100ms p95)
- [ ] Backup/restore tested with demo database
- [ ] Onboarding completion rate >50% (up from current)
- [ ] Public roadmap published with top 10 community requests

---

## PART VI: CROSS-SPRINT DEPENDENCIES

### Migration Path: Custom Auth → Supabase Auth

The auth migration spans Sprint 4 but has implications for Sprints 5-6:

```
Sprint 4                  Sprint 5              Sprint 6
─────────                ─────────             ─────────
Create Supabase project   ──────────→           ──────────→
Migrate users to SB Auth  
Remove Go JWT code        
Add Supabase SDK to FE    
                         Use SB Auth for AI     Use SB Auth for mobile
                         Use SB RLS for perms   Use SB Storage for files
```

### Email Architecture Evolution

```
Sprint 4                  Sprint 5              Sprint 6
─────────                ─────────             ─────────
SMTP outbound             ──────────→           ──────────→
IMAP sync (basic)         Sequence engine       Email templates marketplace
Email sidebar             Open/click tracking   Email analytics dashboard
                         AI compose draft       Auto-reply suggestions
```

### AI Architecture Evolution

```
Sprint 4                  Sprint 5              Sprint 6
─────────                ─────────             ─────────
(Sprint 5 starts)         Ollama integration    AI enrichment v2
                         MCP server            AI suggestions in all forms
                         NL→Query/Action       AI agent: autonomous actions
                         Deal risk detection   Predictive forecasting
                         Pipeline health       Anomaly detection
```

### Database Schema Evolution

```
Sprint 4 (Supabase)       Sprint 5              Sprint 6
───────────────────       ─────────             ─────────
Add email tables:         Add sequence tables:  Add health_score tables:
- email_messages          - email_sequences     - customer_health
- email_sync_status       - sequence_steps      - health_metrics
- email_attachments       - sequence_enrollments - nps_responses
- oauth_tokens            - sequence_analytics  - playbooks
Add SSO table:            Add AI tables:        Add plugin tables:
- sso_providers           - ai_conversations    - plugins
                          - insight_cards       - plugin_settings
                          - reports             Add onboarding tables:
                          - dashboards          - onboarding_progress
                          - dashboard_widgets   - onboarding_steps
```

---

## PART VII: TECH DEBT & ARCHITECTURAL RISKS

### Known Tech Debt (Must Fix)

| Item | Sprint | Effort | Priority |
|------|:------:|:------:|:--------:|
| Go API doesn't compile | 4 | 1 day | CRITICAL |
| No .git / GitHub repo | 4 | 1 hr | CRITICAL |
| No Dockerfiles | 4 | 3 hrs | CRITICAL |
| No .env configs | 4 | 1 hr | CRITICAL |
| Frontend can't connect to API | 4 | 2 hrs | CRITICAL |
| Redis dependency (unused) | 4 | 1 hr | HIGH |
| Custom auth duplicates Supabase | 4 | 2 days | HIGH |
| Broken struct tags in Go files | 4 | 2 hrs | HIGH |
| Missing Init()/Migrate() functions in db.go | 4 Already added | - | DONE |
| No monitoring/healthcheck | 4 | 1 day | HIGH |
| No seed data script (reliable) | 4 | 2 hrs | MEDIUM |

### Architectural Risks

| Risk | Sprint | Severity | Mitigation |
|------|:------:|:--------:|-----------|
| Supabase local dev requires Docker; user has Podman | 4 | MEDIUM | Supabase CLI supports Podman via `SUPABASE_DOCKER=podman` env var; or use Supabase Cloud for demo |
| Gmail SMTP requires "less secure app" or app password | 4 | LOW | Use Gmail App Password (2FA required); document setup |
| Go API auth migration to Supabase JWT may have subtle bugs | 4 | HIGH | Write integration tests for all auth flows; test edge cases |
| Ollama requires GPU or sufficient RAM for local LLMs | 5 | MEDIUM | Default to small model (phi4, llama3.2); document hardware requirements |
| Email sync may hit Gmail rate limits on demo | 5 | MEDIUM | Implement backoff + queue; stay within 2500/day/user |
| Mobile PWA push notifications unreliable on iOS | 6 | MEDIUM | iOS requires app service worker for push; test thoroughly |
| Multi-provider AI config may leak API keys | 5 | HIGH | Encrypt API keys at rest; never expose in frontend responses |

---

## PART VIII: SUPABASE INTEGRATION DETAILS

### Supabase Features Used Per Sprint

| Sprint | Supabase Feature | Purpose |
|:------:|-----------------|---------|
| 4 | Auth (email + Google OAuth + SAML) | Replace custom JWT auth; enterprise SSO |
| 4 | PostgreSQL (managed) | Database as service; backup included |
| 4 | Realtime (optional) | Future: live pipeline updates, collaboration |
| 5 | Storage (optional) | Email attachments, avatar uploads |
| 5 | PostgreSQL | Same DB; AI features read/write via Go API |
| 6 | PostgreSQL | Customer health data, NPS responses |
| 6 | Storage | Plugin assets, onboarding media |

### Supabase + Go API Integration

```
                 ┌─────────────────────────────┐
                 │        Supabase Cloud        │
                 │  ┌───────────────────────┐   │
                 │  │  Auth (GoTrue)         │   │
                 │  │  • Users & sessions    │   │
                 │  │  • OAuth (Google, etc) │   │
                 │  │  • SAML/SSO            │   │
                 │  └──────────┬────────────┘   │
                 │  ┌──────────▼────────────┐   │
                 │  │  PostgreSQL            │   │
                 │  │  • sovereign_db        │   │
                 │  │  • RLS policies        │   │
                 │  │  • pgcrypto            │   │
                 │  └───────────────────────┘   │
                 └─────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Go API  │ │ Next.js  │ │  psql    │
        │ (port    │ │ (port    │ │ (direct) │
        │  8080)   │ │  3000)   │ │          │
        │          │ │          │ │          │
        │ Business │ │ Supabase │ │ Admin    │
        │ Logic    │ │ SDK      │ │ queries  │
        │          │ │ (auth)   │ │          │
        └──────────┘ └──────────┘ └──────────┘
```

### Supabase Local Development vs Cloud

| Aspect | Local (supabase start) | Cloud (supabase.com) |
|--------|----------------------|---------------------|
| Setup time | 5 min (Docker pull) | 2 min (create project) |
| Data persistence | Volumes (reset on stop) | Persistent |
| Auth providers | All supported | All supported |
| Backup | Manual pg_dump | Automatic |
| Cost | Free (uses local resources) | Free tier (500MB DB, 50K users) |
| Public URL | localhost:54321 | project-ref.supabase.co |
| Best for | Development, testing | Demo, production |

**Recommendation:** Use Supabase Cloud for the demo deployment (demo.sovereigncrm.com), use Supabase Local for development.

---

## PART IX: NODE.JS & WSL2 SETUP

Since Node.js is already installed on Windows but not in WSL2 PATH:

```bash
# Option 1: Add Windows Node.js to WSL2 PATH (recommended for simplicity)
export PATH="/mnt/c/Program Files/nodejs:$PATH"
echo 'export PATH="/mnt/c/Program Files/nodejs:$PATH"' >> ~/.bashrc

# Option 2: Install nvm in WSL2 (better for version management)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install 20
nvm use 20
```

**Recommendation:** Option 1 for immediate use (no re-install needed), Option 2 for long-term development.

---

## PART X: EXECUTION PLAN

### Immediate Prerequisites (Before Sprint 4 Start)

| # | Task | Who | Time |
|:-:|------|:---:|:----:|
| 1 | Fix Node.js PATH in WSL2 | You/Agent | 2 min |
| 2 | Create Supabase project (cloud.supabase.com) | You | 5 min |
| 3 | Enable Gmail App Password (Google Account → Security) | You | 5 min |
| 4 | Create GitHub repo (sovereign-crm/sovereign) | You | 2 min |
| 5 | Install Ollama (ollama.com) if not done | You | 5 min |
| 6 | Pull Ollama model (phi4 or llama3.2) | You | 5-10 min |

### Sprint 4 Kickoff (Day 1)

```bash
# Fix Node.js PATH
echo 'export PATH="/mnt/c/Program Files/nodejs:$PATH"' >> ~/.bashrc
source ~/.bashrc
node --version  # Should show v20.x or v22.x

# Initialize Git
cd /mnt/c/Users/Lenovo/sovereign
git init
git add .
git commit -m "Sprint 1-3: Core CRM foundation"
git remote add origin https://github.com/sovereign-crm/sovereign.git
git push -u origin main

# Verify Supabase CLI works
supabase --version

# Fix Go API compilation (agent will handle this)
cd api && go build ./cmd/server/
```

---

## PART XI: RISK REGISTER

| # | Risk | Sprint | Likelihood | Impact | Mitigation |
|:-:|------|:------:|:----------:|:------:|-----------|
| 1 | Supabase local dev incompatible with Podman | 4 | MEDIUM | Use Supabase Cloud for demo; test local later |
| 2 | Go API auth migration breaks existing users | 4 | MEDIUM | Migrate during low-usage window; test rollback |
| 3 | Gmail SMTP blocks demo emails | 4 | MEDIUM | Use SendGrid/Mailgun as fallback (free tier) |
| 4 | GitHub Actions minutes exhausted | 4-6 | LOW | Public repo = free minutes; use self-hosted runner if needed |
| 5 | Ollama crashes on small VPS | 5 | HIGH | Default to smaller model; allow configurable host |
| 6 | AI Chat hallucinates deal data | 5 | HIGH | Always include "AI may be incorrect" disclaimer; confirmation for actions |
| 7 | Mobile PWA doesn't work on iOS | 6 | MEDIUM | Test on real iOS device; have responsive web fallback |
| 8 | Community infra generates zero engagement | 4-6 | HIGH | Have backup plan: direct outreach to 10 potential users |
| 9 | Supabase free tier limits exceeded (50K users, 500MB DB) | 5-6 | LOW | Upgrade to Pro tier ($25/mo) when needed |
| 10 | Email sync privacy concerns (storing emails) | 4 | MEDIUM | Document data handling; offer opt-out; encrypt at rest |

---

## PART XII: SUCCESS METRICS

### Sprint 4

| Metric | Target | Measurement |
|--------|:------:|-------------|
| GitHub stars | 5+ | GitHub API |
| Discord members | 10+ | Discord widget |
| Demo signups | 10+ | Database count |
| Docker pulls (sovereign-image) | 20+ | DockerHub/GHCR stats |
| GitHub issues created by community | 3+ | GitHub API |
| API uptime | 99.5%+ | Uptime Kuma / healthcheck |
| Email sync success rate | 95%+ | Sync job logs |

### Sprint 5

| Metric | Target | Measurement |
|--------|:------:|-------------|
| AI Chat queries (unique users) | 20+ | Database logs |
| AI Chat accuracy (user-rated) | 80%+ | Thumbs up/down per query |
| Email sequences created | 10+ | Database count |
| Insight cards clicked | 30+ | Click tracking |
| Reports created | 15+ | Database count |
| Active users (7-day) | 10+ | Auth logs |

### Sprint 6

| Metric | Target | Measurement |
|--------|:------:|-------------|
| PWA installs | 20+ | Service worker events |
| Mobile sessions | 50+ | Analytics |
| Health scores calculated | 50+ | Database count |
| NPS responses collected | 10+ | Database count |
| OpenAPI spec requests | 100+ | API access logs |
| Plugin SDK downloads | 5+ | npm/pip downloads |

---

*End of strategic review and Sprints 4-5-6 plan.*
