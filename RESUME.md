# Sovereign CRM — Resume State

**Last Session:** 2026-06-06  |  **Status:** Sprint 1 Complete, Sprint 2 In Progress
**Stack:** Go + Next.js + Postgres  |  **License:** AGPL v3
**Repo:** github.com/sovereign-crm/sovereign  |  **Vault:** (private, no git)
**Governing Doc:** CONSTITUTION.md (v1.0, ratified)

---

## Project Phase Phase 5: Implementation

### Completed Work
| Sprint | Status | Deliverables |
|--------|:------:|--------------|
| Sprint 1 | DONE | Project scaffold, auth (JWT login/register/refresh), RBAC middleware, User CRUD API, Role CRUD + permissions API, audit logging, Docker Compose, CI/CD, login UI, dashboard shell, admin users UI, admin roles UI, Makefile, seed data (5 system roles + admin user), CONTRIBUTING.md, issue/PR templates, Code of Conduct, auth unit tests, RBAC unit tests |
| Sprint 2 | DONE | Contacts + Orgs CRUD (Go + Next.js UI), activity timeline (generic entity pattern), contact dedup (SHA256 + merge endpoint), PostgreSQL full-text search, auth JWT + RBAC unit tests |
| Sprint 2.5 | DONE | Methodology Fix Sprint: OCM framework, CSV import/export, migration playbook, business case calculator, discovery sprint template, IT Consulting industry profile, telemetry spec, hypercare runbook, compliance matrix, adoption dashboard spec |

### Active Work (Sprint 2)
- Contacts + Organizations CRUD (Go API + Next.js UI)
- Activity timeline per contact
- Field-level permission enforcement
- CSV import/export for contacts
- Contact deduplication foundation
- Search (ILIKE + PostgreSQL full-text)
- Backfill Sprint 1 tests

### Next After Sprint 2
- Sprint 3: Lead Management + Pipeline
- Sprint 4: Sync Engine (CRDT)
- Sprint 5: Mobile (React Native)

---

## Architecture Snapshot

```
sovereign/                  # Git repo (source code only)
├── api/                    # Go API server
│   ├── cmd/server/         # Entry point (chi router, graceful shutdown)
│   ├── internal/
│   │   ├── auth/           # JWT, login/register/refresh handlers
│   │   ├── middleware/     # Auth, RBAC, CORS, logging
│   │   ├── handlers/       # User, Role, Contact, Organization, Activity, Import/Export
│   │   ├── models/         # All domain types
│   │   └── database/       # Postgres pool + migrations (001_init, 002_seed_admin)
│   └── pkg/response/       # Standardized JSON responses
├── web/                    # Next.js 14 App Router
│   ├── app/                # login/, dashboard/, contacts/, organizations/, admin/users/, admin/roles/
│   ├── components/         # layout/sidebar, auth-provider
│   └── lib/                # API client (axios with token refresh)
├── docker-compose.yml      # postgres:16 + redis:7 + api + web
├── Makefile                # dev, test, lint, build, reset
├── CONTRIBUTING.md         # Open source contribution guide
├── CODE_OF_CONDUCT.md
├── .github/                # CI pipeline, issue/PR templates
└── README.md
```

## Key Decisions Made
1. License: AGPL v3 with commercial exception
2. Repo: github.com/sovereign-crm/sovereign
3. Monetization: 100% open core (no license key checks). Managed cloud = separate deployment. Marketplace in Month 6+.
4. Stack: Go + Next.js + Postgres (confirmed)
5. Governance: BDFL + Core Maintainers
6. Admin seed: admin@sovereign.local / admin1234 (dev only, warning in README)

## Standing Committees (Established)
| Committee | Charter Location | Chair | Next Meeting |
|-----------|-----------------|-------|:------------:|
| Community & Ecosystem | committees/community-charter.md | TBD | Week 1 of Sprint 2 |
| Mobile & Field Sales OS | committees/mobile-charter.md | TBD | Week 1 |
| Developer Platform | committees/dev-platform-charter.md | TBD | Week 1 |
| SRE & Operations | committees/sre-charter.md | TBD | Week 2 |
| Testing & Trust Arch | committees/testing-charter.md | TBD | Week 2 |

## Vault Documents Created/Updated This Session
| Document | Action | Notes |
|----------|:------:|-------|
| CONSTITUTION.md | CREATED | 18.3K, master governing document |
| committees/community-charter.md | CREATED | 4.0K, community flywheel + governance |
| committees/mobile-charter.md | CREATED | 5.0K, Field Sales OS spec |
| committees/dev-platform-charter.md | CREATED | 4.4K, DX + plugin system |
| committees/sre-charter.md | CREATED | 5.8K, SRE + operations |
| committees/testing-charter.md | CREATED | 6.4K, testing trust architecture |
| blueprints/index/blueprint-index.md | UPDATED | Added Constitution + Committees + Sprint 1 |
| RESUME.md | UPDATED | This document |

## Known Gaps / Technical Debt
1. MFA flow: framework exists (mfa_enabled field, mfa_secret) but no actual TOTP setup/verify endpoints
2. Password reset: not implemented (Postgres migration has no reset_tokens table yet)
3. Tests: Sprint 1 has zero tests (planned backfill in Sprint 2)
4. Staging Compose: Docker Compose is dev-only. Need a prod-like docker-compose.prod.yml
5. RBAC field-level enforcement: schema stores field_permissions but API doesn't enforce field-level visibility yet
6. Redis session store: Redis is connected but session blacklisting not implemented


### Sprint 2.5: Methodology Fix Sprint ✅ COMPLETE
- GAP 1 (OCM): Community Charter updated with OCM framework — training profiles, adoption metrics, onboarding flows, champion program
- GAP 2 (Migration): CSV Import/Export endpoint (Go API), Migration Playbook (discovery→validation→rollback)
- GAP 3 (Business Case): Business case calculator with TCO/ROI comparison vs Salesforce/HubSpot/Zoho, Discovery Sprint template (Week 0)
- GAP 4 (Industry Configs): IT Consulting industry profile — custom fields (skills, rates, certifications), engagement/placement objects, pipeline stages, workflows, dashboards, integrations
- GAP 5 (Post-Deploy): Telemetry spec (anonymous, opt-in), Hypercare runbook (5-day war room), Adoption dashboard spec, Compliance matrix (GDPR/SOC2/HIPAA)
- Fix: Contact model search_vector (company→department column)

### Customer Pre-Mortem Fixes (Sprint 2.5b) ✅ COMPLETE
- P0: Custom Fields system — migration (JSONB + field definitions table), Go API (CRUD), Next.js admin UI
- P0: Global Search — unified API across contacts + organizations (tsvector), React search component
- P1: Webhooks — event subscription management, HMAC-signed dispatch, delivery logging, admin UI
- Customer Pre-Mortem document published (98 customer questions across 6 personas, ranked by severity)
- Public ROADMAP.md published in repo
- CHANGELOG.md published in repo
- SYSTEM_REQUIREMENTS.md published in repo
- Sidebar updated with Custom Fields + Webhooks navigation
- Dashboard layout updated with Global Search bar
## Sprint 3 — Lead Management + Pipeline (Complete)

**Dates:** 2026-06-06
**Theme:** Core sales capability — the engine that drives every CRM

### Delivered

| Area | Deliverable | Files |
|------|-------------|-------|
| **Migration** | leads, pipeline_stages, deals tables | `api/internal/database/migrations/005_leads_pipeline.sql` |
| **Lead Engine** | CRUD + scoring engine + search + assignment + conversion-to-contact | `api/internal/handlers/leads.go` |
| **Pipeline** | Stage CRUD + reorder + probabilities | `api/internal/handlers/pipeline_stages.go` |
| **Deal Engine** | CRUD + stage transitions + won/lost tracking + forecast API | `api/internal/handlers/deals.go` |
| **Field Permissions** | Field-level RBAC middleware per entity/role | `api/internal/auth/field_permissions.go` |
| **Lead UI** | List (filters, score/status/source badges) + Create + Detail (with activity timeline + conversion) | `web/app/leads/*` |
| **Pipeline UI** | Kanban board (drag-to-move, forecast bar, stage form) | `web/app/pipeline/page.tsx` |
| **Deal UI** | List + Detail (stage transitions, weighted value, lost reasons) | `web/app/deals/*` |
| **Dashboard** | Pipeline health widget (forecast bar, stage distribution, leads by status) | `web/app/dashboard/page.tsx` |
| **Setup Wizard** | 5-step first-run onboarding (org, team, import) | `web/app/setup/page.tsx` |
| **Sidebar** | Sales section (Leads, Pipeline, Deals) + Admin links (Custom Fields, Webhooks) | `web/components/layout/sidebar.tsx` |

### Model

**Leads:** id, name(s), email, phone, title, company, source (8 types), source_detail (UTM/partner), status (new→contacted→qualified→proposal→negotiation→won/lost/archived), score (0-100), score_detail (JSONB breakdown), assigned_to, last_contacted_at, dedup, tsvector

**Pipeline Stages:** id, name, probability (0-100), sort_order, color, category (active/won/lost), tenant-scoped

**Deals:** id, name, lead_id FK, contact_id FK, org_id FK, pipeline_stage_id FK, amount, currency, probability, expected_close_date, assigned_to, lost_reason, won_at, dedup, tsvector

### Intelligence Applied

- **Scoring:** 7-factor rule engine (email domain, title keywords, source, company size, engagement signals, completeness, recency), configurable weights, stored score_detail JSONB for transparency
- **Forecast:** Weighted pipeline = sum(amount × probability/100) per stage, grouped stage distribution for visual forecast bar
- **Stage transitions:** Validation (can't skip stages), lost reason capture, won_at timestamp on move to won
- **Conversion:** Lead→Contact+Deal atomically, archives original lead, creates audit trail
- **Field-level RBAC:** sales_rep reads/writes subset, sales_manager full access, read_only view-only
- **Kanban UX:** Native HTML5 drag-and-drop, forecast bar at top, stage-level deal counts/probabilities

### Architecture

```
api/
  internal/
    handlers/
      leads.go           — CRUD + scoring + search + assign + convert
      pipeline_stages.go  — CRUD + reorder + probabilities
      deals.go           — CRUD + move_stage + forecast + won/lost
    auth/
      field_permissions.go — role-field matrix, middleware, response filtering
    database/
      migrations/
        005_leads_pipeline.sql
web/
  app/
    leads/              — list + create + detail
    pipeline/           — Kanban board
    deals/              — list + detail
    setup/              — first-run wizard
