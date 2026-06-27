# Phase 14: Sprint Breakdown & Implementation Roadmap

**Created:** 2026-06-06
**Purpose:** Phased implementation plan — sprint-by-sprint tasks, dependencies, team requirements, milestones, and risk mitigation.

---

## 0. ROADMAP PHILOSOPHY

| Principle | Application |
|-----------|-------------|
| **Functional product first** | Sprint 1-2 ships a working CRM, not infrastructure |
| **Dogfood from day 1** | Team uses the CRM to build the CRM (track bugs, features, releases) |
| **Vertical modules are extensions, not rewrites** | ITC and SaaS modules bolt onto the core without modifying it |
| **AI comes after data** | You need populated data before AI can be useful |
| **Test everything** | Unit tests mandatory. E2E tests for critical paths. |

---

## 1. TEAM STRUCTURE

### Core Team (Sprint 1-4)
| Role | Count | Skills |
|------|:-----:|--------|
| Go Backend Engineer | 2 | Go, PostgreSQL, REST, GraphQL |
| Frontend Engineer | 2 | Next.js, TypeScript, React, Tailwind |
| Full-Stack Engineer | 1 | Go + React |
| DevOps Engineer | 1 | Docker, Kubernetes, CI/CD, Terraform |
| QA Engineer | 1 | Playwright, API testing, E2E |
| Product Manager | 1 | CRM domain expertise |
| UI/UX Designer | 1 (50%) | SaaS product design |

### Extended Team (Sprint 5+)
| Role | Count | When |
|------|:-----:|:----:|
| Second Frontend Engineer | +1 | Sprint 5 |
| Data Engineer | 1 | Sprint 4 (DW) |
| Security Engineer | 1 (50%) | Sprint 1 (ongoing) |
| AI Engineer | 1 | Sprint 4 |
| Technical Writer | 1 | Sprint 3 (API docs) |

---

## 2. SPRINT 1: FOUNDATION (Weeks 1-2)

**Theme:** Auth, User Management, Core Data Types — the absolute minimum to have a working system.

### Tasks
```
Backend:
[1.1] Project scaffold: Go project structure, Docker Compose for Postgres/Redis
[1.2] Database schema: migrations + seed for User, Tenant, Role, Team
[1.3] Auth system: register, login, JWT, MFA, password reset
[1.4] RBAC middleware: permission check on every route
[1.5] User CRUD API: create, read, update, deactivate
[1.6] Role CRUD API: create, read, update (with permission set)
[1.7] Audit log: automatic field-level change tracking

Frontend:
[1.8] Login page, password reset flow
[1.9] User management UI (admin: list, create, edit, deactivate)
[1.10] Navigation shell: sidebar, top bar, user menu
[1.11] Role management UI (basic)

DevOps:
[1.12] CI/CD pipeline (GitHub Actions: build, test, lint)
[1.13] Docker images for all services
[1.14] Staging environment in Docker Compose

QA:
[1.15] Auth integration tests (login, logout, MFA, password reset)
[1.16] RBAC unit tests
```

**Dependencies:** None — this is the foundation.
**Risk:** Auth is critical. If auth breaks, nothing works. Invest in backup auth flow.
**Milestone:** ✅ Admin can log in, create users, assign roles.

---

## 3. SPRINT 2: CORE CRM (Weeks 3-5)

**Theme:** Contacts, Organizations, Deals, Pipeline — the data that makes a CRM a CRM.

### Tasks
```
Backend:
[2.1] Contact CRUD API (with dedup on email)
[2.2] Organization CRUD API (with hierarchy)
[2.3] Deal CRUD API (with pipeline, stages, probability)
[2.4] Pipeline CRUD API (multi-pipeline support)
[2.5] Lead CRUD API (with conversion to Contact + Org + Deal)
[2.6] Activity CRUD API (polymorphic: calls, emails, meetings, tasks, notes)
[2.7] Global search API (basic: SQL full-text search)
[2.8] Import/Export API: CSV import with mapping + validation
[2.9] Soft-delete for all entities + restore
[2.10] Dynamic Object Builder backend: create custom entities + fields

Frontend:
[2.11] Contact list + detail pages (with activity timeline)
[2.12] Organization list + detail pages (with hierarchy tree)
[2.13] Deal list + detail pages (with tabs: summary, activity, contacts)
[2.14] Pipeline kanban board (drag-and-drop stage move)
[2.15] Lead management UI (list, kanban, convert)
[2.16] Activity logging UI (1-click call log, email log, task creation)
[2.17] Global search bar (Cmd+K)
[2.18] Import wizard UI (upload → map → preview → execute)
[2.19] Home dashboard with widgets (pipeline summary, tasks, activity feed)
[2.20] Dynamic Object Builder UI (entity creation wizard)

QA:
[2.21] E2E tests: create contact, create deal, move stage, log activity
[2.22] Import test: 10k records, validate mapping
```

**Dependencies:** Sprint 1 (auth, RBAC, user management).
**Risk:** Data model changes will happen. Account for migration rollback plan.
**Milestone:** ✅ Core CRM functional. Users can manage contacts, deals, pipeline.

---

## 4. SPRINT 3: SALES OPERATIONS (Weeks 6-8)

**Theme:** Email, calendar, sequences, workflows, approval engine.

### Tasks
```
Backend:
[3.1] Email integration (Gmail/O365 via OAuth: send, sync, tracking)
[3.2] Calendar integration (Google/Outlook: sync, create from CRM)
[3.3] Email template engine (merge fields, categories)
[3.4] Sequence engine (step builder, enrollment, auto-advance)
[3.5] Sequence analytics (open rate, reply rate, click rate)
[3.6] Workflow engine: trigger → condition → action (create, update, email, webhook)
[3.7] Approval engine: multi-step, parallel, escalation, delegation
[3.8] Document template engine (proposal/quote/SOW generation)
[3.9] Webhook engine: outbound event delivery + retry
[3.10] Forecasting engine: commit/best case/pipeline + AI bias correction (basic)
[3.11] Territory CRUD + assignment API
[3.12] Quota API (per rep, per period)

Frontend:
[3.13] Email sidebar (inbox from CRM, send, track opens)
[3.14] Calendar widget (today's meetings, create from CRM)
[3.15] Sequence builder (drag-drop steps, templates)
[3.16] Workflow rule builder (visual condition → action tree)
[3.17] Approval process UI (create + approve/reject in-app)
[3.18] Quote builder (select products → generate PDF)
[3.19] Webhook configuration UI
[3.20] Forecast UI (rep view, manager rollup, commit vs actual)
[3.21] Sandbox management UI

QA:
[3.22] Email sync test: 10k emails, verify tracking
[3.23] Workflow test: trigger → action, time-based, error handling
```

**Dependencies:** Sprint 2 (core entities).
**Risk:** Email integration complexity (OAuth flows, rate limiting, IMAP vs Graph API).
**Milestone:** ✅ Sales operations functional. Emails, sequences, workflows, forecasting.

---

## 5. SPRINT 4: AI & ANALYTICS (Weeks 9-11)

**Theme:** AI assistant, insights engine, report builder, dashboards.

### Tasks
```
Backend:
[4.1] MCP server implementation (all CRM tools exposed)
[4.2] AI chat API (NL→query, NL→action with permission check)
[4.3] AI insight engine (deal risk, pipeline health, stale detection)
[4.4] Report builder API (tabular, summary, chart, filter, group, metrics)
[4.5] Dashboard builder API (widget layout, multiple reports)
[4.6] ClickHouse setup + CDC pipeline (Postgres → Redpanda → ClickHouse)
[4.7] MV denormalized views for analytics
[4.8] Data export (CSV, Excel, PDF, scheduled delivery)
[4.9] Model provider configuration (Ollama, OpenAI, Anthropic)

Frontend:
[4.10] AI chat sidebar (ask questions, get answers, execute actions)
[4.11] AI insight cards on dashboard and deal pages
[4.12] Report builder (drag-drop fields, live preview)
[4.13] Dashboard builder (add/remove widgets, resize, save)
[4.14] Chart library (bar, line, pie, funnel, area, pivot table)
[4.15] Scheduled report UI
[4.16] AI configuration UI (model selection, permissions)

QA:
[4.17] AI query accuracy test: 100 natural language queries
[4.18] Report performance test: 1M records, sub-5s response
```

**Dependencies:** Sprint 2 (data) + Sprint 3 (workflows).
**Risk:** AI quality depends on data quality. If data is sparse, AI is useless.
**Milestone:** ✅ AI assistant working. Reports and dashboards functional.

---

## 6. SPRINT 5: VERTICAL EXTENSIONS (Weeks 12-14)

**Theme:** IT Consulting module and SaaS extension built on Dynamic Object Builder.

### Tasks
```
IT Consulting Vertical:
[5.1] Engagement entity + CRUD
[5.2] SOW entity + template + generation + approval
[5.3] Resource entity + skill tagging + rate card
[5.4] Resource allocation UI (drag-drop, conflict detection)
[5.5] Time entry system (weekly grid, timer, approval)
[5.6] Expense tracking (receipt upload, approval)
[5.7] Change order workflow
[5.8] Engagement P&L dashboard
[5.9] Jira integration (project sync, time tracking)

SaaS Vertical:
[5.10] Subscription entity + CRUD + lifecycle tracking
[5.11] MRR/ARR dashboard (breakdown, cohort, waterfall)
[5.12] Invoice management + Stripe sync
[5.13] Health score engine (configurable weights + calculation)
[5.14] Dunning process (failed payment recovery)
[5.15] Renewal management UI

QA:
[5.16] Time entry approval E2E
[5.17] MRR calculation accuracy: verify against Stripe data
```

**Dependencies:** Sprint 2 (core entities) + Dynamic Object Builder.
**Risk:** Vertical features may need core changes. Keep them as dynamic entities.
**Milestone:** ✅ Two verticals functional with core workflows.

---

## 7. SPRINT 6-10: ADVANCED (Weeks 15-30)

### Sprint 6: Marketing Hub (Weeks 15-17)
- Campaign management, form builder, landing pages, email marketing
- Lead scoring (advanced ML), attribution (multi-touch)
- AI CRM Administrator (autonomous agent for data cleanup)

### Sprint 7: Customer Success + Support (Weeks 18-21)
- Ticket management, SLA engine, knowledge base, omni-channel inbox
- CSAT surveys, macros, customer portal (basic)

### Sprint 8: Performance & Scale (Weeks 22-24)
- Performance optimization: query optimization, indexing, caching
- Load testing: 10k concurrent users, 10M records
- CDN setup, edge caching, database read replicas
- Monitoring: Prometheus + Grafana dashboards

### Sprint 9: Advanced Features (Weeks 25-27)
- Partner/reseller management, portal, commission
- Advanced CPQ, contract management
- Conversation intelligence (call recording, AI analysis)
- Customer portal (full)

### Sprint 10: Enterprise & Compliance (Weeks 28-30)
- SAML/SSO for all major providers
- SOC 2 documentation + controls implementation
- Advanced encryption key management
- Multi-region deployment support
- White-labeling / branding options

---

## 8. MILESTONE MAP

```
Sprint 1 (W2)     Sprint 2 (W5)    Sprint 3 (W8)     Sprint 4 (W11)     Sprint 5 (W14)
─────────────     ─────────────    ─────────────     ──────────────     ──────────────
Auth, Users       Core CRM         Sales Ops          AI + Reports       Verticals
Tenant Setup      Contacts         Email Integr       MCP Server         IT Consulting
RBAC              Orgs             Calendar           AI Chat            SaaS Extension
Audit             Deals            Workflows          Report Builder     Engagements
Login/Register    Pipeline         Approvals          Dashboard Builder  Subscriptions
User Mgmt         Leads            Sequences          AI Insights        Time Tracking
Navigation        Activity Log     Forecasting        ClickHouse DW      MRR Dashboard
                  Import/Export    Webhooks            P&L Dashboard      Health Score
                  Search           Sandbox             Stripe Sync
                  Dynamic Objects                      Jira Integration

    │                  │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼                  ▼
 MVP Alpha         MVP Beta         MVP Release        Analytics Release    Vertical Release
 (internal demo)   (friend test)    (early adopters)   (all users)          (beta)
```

---

## 9. ESTIMATED EFFORT

| Sprint | Duration | Team | Story Points | Key Deliverable |
|:------:|:--------:|:----:|:------------:|-----------------|
| 1 | 2 weeks | 5 eng | 150 | Auth + User Mgmt |
| 2 | 3 weeks | 5 eng | 220 | Core CRM |
| 3 | 3 weeks | 5 eng | 200 | Sales Operations |
| 4 | 3 weeks | 6 eng | 200 | AI + Analytics |
| 5 | 3 weeks | 6 eng | 180 | Verticals |
| 6 | 3 weeks | 6 eng | 160 | Marketing Hub |
| 7 | 4 weeks | 6 eng | 200 | CS + Support |
| 8 | 3 weeks | 5 eng | 120 | Performance |
| 9 | 3 weeks | 6 eng | 160 | Advanced Features |
| 10 | 3 weeks | 5 eng | 140 | Enterprise |

**Total: 30 weeks (~7.5 months) to MVP Release with core CRM + one vertical.**

---

## 10. GO/NO-GO GATES

| Gate | Criteria | Who Decides |
|:----:|----------|:-----------:|
| G1 | Auth works, users can be created, RBAC enforced | PM + Lead Eng |
| G2 | Contacts, Deals, Pipeline working with import. 10 test users active for 1 week. | PM + QA |
| G3 | Email sync working. Workflows executing. Forecasting matches manual calc. | PM + Sales Advisors |
| G4 | AI assistant answers 80% of queries correctly. Reports load in <5s for 100k records. | PM + Eng Lead |
| G5 | Two verticals demonstrated with real data. Partners can test. | CEO + PM |
| G6 | Marketing Hub reached. Paying customers onboarded. | CEO |

---

*Phase 14 complete. Sprint breakdown covers 10 sprints over 30 weeks with team structure, dependencies, milestones, and go/no-go gates. Next: Phase 15 — Data Migration & Onboarding Strategy.*
