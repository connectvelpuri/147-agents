# Customer Pre-Mortem — Will Sovereign CRM Succeed or Fail?

**Date:** 2026-06-06
**Methodology:** Based on real customer objections to open-source CRMs (SuiteCRM, EspoCRM, Twenty, Monica, Corteza, SugarCE) gathered from Reddit, HN, G2, TrustRadius, and community forums.

---

## Executive Summary

**If Sovereign CRM fails, it will be for ONE of these reasons:**
1. No custom fields (CRM is unusable without this)
2. Email integration broken or missing
3. Reporting too basic for management decisions
4. UI/UX not polished enough for sales team adoption
5. Deployment complexity scares away self-hosters

**If Sovereign CRM succeeds, it will be because:**
- Go binary = trivially deployable (single `./server` or Docker)
- AGPL v3 = genuinely open, no bait-and-switch
- Local-first/CRDT = competitive moat no other CRM has
- Local AI (Ollama) = differentiated feature Big 4 can't match
- IT Consulting focus = solves a real vertical need

---

## Section 1: Every Customer Question You'll Face (Organized by Persona)

### CTO / VP Engineering (Technical Decision Maker)

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| Can I add custom fields without touching code? | **No** — only static schema | 🔴 CRITICAL | **THIS SPRINT** |
| Is there a REST API? | ✅ Yes — chi router, JSON | 🟢 Fine | — |
| Is there an API client (Go/TS/Python)? | **No** — raw curl only | 🟡 Docs needed | Sprint 4 |
| How do I integrate with our existing stack? | **Webhooks not built** — no event system | 🔴 HIGH | **THIS SPRINT** |
| Does it support SSO/SAML/OIDC? | **No** — email+password only | 🟡 Plan exists | Sprint 4 |
| How do I set up a staging env? | ✅ Docker Compose override | 🟢 Fine | — |
| Can I deploy on Kubernetes? | **No Helm chart** — Docker Compose only | 🟡 Docs needed | Sprint 4 |
| What's the performance at 10K users? | **Not benchmarked** | 🟡 Plan exists | Sprint 5 |
| How is tenant isolation enforced? | ✅ Row-level + schema patterns | 🟢 Fine | — |
| Is there rate limiting? | ✅ Middleware exists | 🟢 Fine | — |
| Can I write custom business logic? | **Not without forking** | 🟡 Plugin system planned | Sprint 6 |
| How do I search across all data? | **Per-entity only** — no global search | 🟡 Quick win | **THIS SPRINT** |

### VP Sales / Sales Ops (Business Decision Maker)

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| Can I create custom reports? | **Not built** — only dashboard widgets | 🔴 HIGH | Sprint 3 |
| Can I build custom dashboards? | **No** — fixed admin dashboard | 🟡 Plan exists | Sprint 3 |
| Can I see pipeline forecasts? | **Not built** — pipeline API exists, no forecast | 🟡 Plan exists | Sprint 3 |
| Does it integrate with our email? (Gmail/Outlook) | **No** — email tracking not built | 🔴 HIGH | Sprint 4 |
| Can I import data from Salesforce/HubSpot? | ✅ CSV import exists, migration playbook | 🟢 Fine | — |
| Can I export my data? | ✅ Full CSV export | 🟢 Fine | — |
| Is there a mobile app? | **No** — mobile charter exists, no code | 🟡 Plan exists | Sprint 6 |
| Can I use it offline? | **No** — CRDT planned, not built | 🟡 Plan exists | Sprint 6 |
| Can I set up email sequences? | **No** — not planned | 🟢 Not a P0 | Sprint 7 |
| Does it track email opens/clicks? | **No** | 🟢 Not a P0 | Sprint 7 |
| Is there a Chrome extension? | **No** | 🟢 Not a P0 | Sprint 8 |

### CISO / Legal / Compliance (Gatekeeper)

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| Is data encrypted at rest? | **PostgreSQL TDE — depends on hosting** | 🟡 Docs needed | Sprint 4 |
| Is data encrypted in transit? | ✅ TLS via reverse proxy | 🟢 Fine | — |
| What compliance certifications? | **None — but compliance matrix exists** | 🟡 Roadmap | Sprint 8 |
| Do you have SOC 2? | **No** | 🟡 Plan exists | Sprint 8 |
| Can I set data retention policies? | **No — no purge/retention logic** | 🟡 Plan exists | Sprint 5 |
| What happens if the project dies? | **AGPL v3 — code is yours forever** | 🟢 Strong | — |
| Data Processing Agreement (DPA)? | **Not drafted** | 🟡 Sprint 8 | Sprint 8 |
| Can I audit who did what? | ✅ Full audit log | 🟢 Fine | — |
| Where is data physically stored? | **Your infrastructure — your choice** | 🟢 Strong | — |

### DevOps / IT Admin (Implementer)

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| How do I back up the database? | **Documented in migration playbook** | 🟢 Fine | — |
| What are system requirements? | **Not documented** | 🟡 Quick win | **THIS SPRINT** |
| How do I enable logging? | ✅ Structured logging via chi | 🟢 Fine | — |
| Can I use external PostgreSQL? | ✅ ENV variable | 🟢 Fine | — |
| Is there a health check endpoint? | ✅ Docker health check | 🟢 Fine | — |
| Can I deploy on Raspberry Pi? | **Go binary — yes, but not documented** | 🟡 Doc update | Sprint 4 |
| Is there a Helm chart? | **No** | 🟡 Plan exists | Sprint 4 |
| Can I monitor with Prometheus? | **Not instrumented** | 🟡 Plan exists | Sprint 5 |

### End User / Sales Rep (Daily User)

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| Is the UI fast? | ✅ Go + Next.js SSR | 🟢 Fine | — |
| Can I search everything from one box? | **Per-entity search only** | 🟡 Quick win | **THIS SPRINT** |
| Can I filter and save views? | **Not built** | 🟡 Plan exists | Sprint 4 |
| Can I log calls and meetings? | **Activity timeline built — UI not linked yet** | 🟡 Partial | Sprint 3 |
| Is there keyboard navigation? | **No** | 🟢 Nice-to-have | Sprint 5 |
| Can I work offline? | **No** | 🟡 Plan exists | Sprint 6 |

### Open Source Community Evaluator

| Question | Current Answer | Gap? | Fix Sprint |
|----------|---------------|:----:|:----------:|
| What's the license? | ✅ AGPL v3 + commercial exception | 🟢 Fine | — |
| How active is development? | ✅ Active sprint cadence | 🟢 Fine | — |
| How do I contribute? | ✅ CONTRIBUTING.md exists | 🟢 Fine | — |
| Is there a public roadmap? | **Not published** — vault is private | 🟡 Quick win | **THIS SPRINT** |
| Can I extend it with plugins? | **Charter exists — nothing built** | 🟡 Plan exists | Sprint 6 |
| How do I get help? | **No community channels yet** | 🟡 Plan exists | Sprint 3 |
| Is there a changelog? | **No — SESSION_LOG is internal** | 🟡 Quick win | **THIS SPRINT** |

---

## Section 2: Competitive Vulnerabilities

These are attacks competitors (Salesforce, HubSpot, Twenty) would make in a bake-off:

### "You're open source — what happens to my data when the project dies?"
**Our answer:** AGPL v3. The code is yours forever. You have a working fork. Additionally, we're structured as a public benefit entity with a foundation backstop.

**Risk:** Medium — real concern, but our license mitigates it better than most.

### "Your UI is built by engineers, not designers."
**Our answer:** Fair. We're investing in UX — guided by the Product Constitution's "Design is not decoration" principle. We're building for power users who value speed over eye candy, but we know we need to improve.

**Risk:** HIGH — this is why Twenty is winning adoption despite being alpha-quality. Sales teams are UI-sensitive.

### "You don't have reports. How do I sell this to my CEO?"
**Our answer:** We have the data model and API. Reports are coming in Sprint 3. We're building Metabase integration for power users and native report builder for lightweight needs.

**Risk:** HIGH — #1 request across ALL open source CRM feedback.

### "You don't have email integration. How do I log my communications?"
**Our answer:** BCC-to-CRM (Sprint 4) + IMAP sync (Sprint 5). We chose to build the data foundation before integrations.

**Risk:** HIGH — this is the #2 blocker for CRM adoption.

### "I can't add custom fields? Then it's useless for my business."
**Our answer:** Building it RIGHT NOW. See below.

**Risk:** CRITICAL — if someone evaluates today and asks this, they walk. Period.

---

## Section 3: What We MUST Build Right Now (Before Sprint 3)

### P0: Custom Fields System — **Building now**

Without custom fields, a CRM is unusable for any real business. Period. Every Salesforce, HubSpot, Zoho, and SuiteCRM user expects this. This is the #1 blocker.

**What needs to exist:**
- JSONB `custom_fields` column on contacts, organizations
- `custom_field_definitions` table with type validation
- API to CRUD field definitions and values
- Admin UI to manage fields
- Contact/Org UI to show/edit custom fields

### P1: Global Search — **Building now**

Every CRM has a universal search bar. We have per-entity search only. This is a quick win using existing tsvector columns.

### P1: Webhook System — **Building now**

For any integration story to work, we need webhooks. Without them, every integration is a custom code path.

### P2: API Documentation (OpenAPI/Swagger) — **Documenting now**

Every CTO asks "is there an API?" We need a swagger.json that auto-discovers all endpoints.

### P2: Public Roadmap + Changelog — **Quick wins**

We have the data (vault docs). Just need to publish a markdown roadmap and changelog in the repo.

---

## Section 4: Decision Record — What NOT to Build Yet

| Feature | Why Not Now | Sprint |
|---------|-------------|:------:|
| SSO/SAML | Critical for enterprise but most early adopters are small teams | Sprint 4 |
| Mobile app | Mobile charter exists; field sales use case | Sprint 6 |
| Email integration (IMAP) | High value but complex; needs webhook foundation first | Sprint 4-5 |
| Reporting | P0 for Sprint 3 — need pipeline data first | Sprint 3 |
| Plugin system | Needs stable API surface first | Sprint 6 |
| Helm chart | Need K8s testing infra first | Sprint 4 |
| Prometheus metrics | Nice but not a blocker | Sprint 5 |
