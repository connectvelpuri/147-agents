# Competitive Analysis: Twenty CRM

**Phase 1 — Competitive Research | Created:** 2026-06-09
**Focus:** Open-Source CRM Competitor Analysis
**Target:** Sovereign CRM Product Blueprint

---

## 1. COMPANY OVERVIEW

| Attribute | Detail |
|-----------|--------|
| Founded | 2021 |
| Parent | Twenty SAS (Private) |
| Funding | ~$5M Seed (Y Combinator, others) |
| Primary Customers | SMB to Mid-Market, Developer-first |
| Pricing Model | AGPL (self-hosted) + Cloud (freemium per-user/month) |
| Deployment | Self-hosted (Docker, AGPL) + Managed Cloud (paid) |
| GitHub Stars | 22,000+ (one of the fastest-growing OSS projects) |
| Target Verticals | General SMB, SaaS, Developer-led adoption |

## 2. TECHNICAL ARCHITECTURE

| Layer | Technology |
|-------|-----------|
| Backend | NestJS (Node.js/TypeScript) |
| Frontend | React (TypeScript) with Apollo Client |
| API | GraphQL (primary) + REST endpoints |
| Database | PostgreSQL (main), Redis (caching) |
| Real-Time Sync | Yjs CRDT (Conflict-free Replicated Data Types) |
| Search | PostgreSQL full-text search |
| File Storage | Local filesystem or S3-compatible |
| Auth | Google, Magic Link, Email/Password |
| Deployment | Docker compose, Docker Swarm, manual |
| License | AGPL v3 (self-hosted), proprietary (cloud) |

## 3. CORE MODULES

**Standard CRM Objects:**
- People (contacts), Companies (accounts), Opportunities (deals)
- Custom objects (experimental)
- Custom fields (rich types: text, number, boolean, select, relation)

**Current Features:**
- Pipeline/Board view (Kanban-style)
- Table view (spreadsheet-style)
- Timeline/Activity feed
- Notes and rich text
- Email integration (IMAP/SMTP)
- Calendar sync (Google Calendar)
- Search (cross-object)
- File attachments
- Tasks and reminders
- API (GraphQL)
- Webhooks

**Missing / Early Stage:**
- No email sequences
- No calling/VoIP
- No marketing automation
- No service/support ticketing
- No CPQ or quoting
- No forecasting
- No workflow automation
- No reporting/dashboards (basic only)
- No mobile app (web-only responsive)
- No templates
- No roles/permissions beyond basic
- No multi-currency
- No sandboxes

## 4. STRENGTHS (Top 12)

1. **Modern tech stack** — NestJS, GraphQL, React, TypeScript throughout. Clean architecture
2. **Open source (AGPL)** — full code available, self-hostable, auditable
3. **Fast-growing community** — 22K+ GitHub stars, 1K+ contributors, active Discord
4. **CRDT-based sync** — Yjs enables real-time collaboration and conflict-free editing
5. **Beautiful UI** — modern, minimal, comparable to Linear/Notion in design quality
6. **GraphQL API** — flexible, typed, efficient data fetching
7. **Active development** — weekly releases, aggressive feature shipping
8. **Flat data model** — simple, approachable. Less overwhelming than Salesforce
9. **Copy-paste from Notion** — UX patterns borrowed from modern tools
10. **Self-hostable** — simple Docker setup, AGPL guarantees freedom
11. **Developer-friendly** — full TypeScript, clean codebase, easy to extend
12. **Positioned as "open-source HubSpot alternative"** — clear narrative

## 5. WEAKNESSES — OUR OPPORTUNITIES (Top 15)

1. **Extremely early stage** — missing 80% of features compared to mature CRMs
2. **No enterprise features** — no RBAC, no audit logs, no sandboxes, no security controls
3. **No mobile app** — web-only. Cannot be used for field sales
4. **No marketing automation** — no email campaigns, forms, landing pages, lead scoring
5. **No service/support** — no ticketing, knowledge base, SLA management
6. **No calling or telephony** — no VoIP integration, no call logging
7. **No workflow engine** — no visual automation builder, no approval chains
8. **No advanced reporting** — no dashboards, no custom reports, no BI
9. **Basic permission model** — no profiles, permission sets, field-level security
10. **AGPL license may deter enterprise** — copyleft AGPL is restrictive for commercial use
11. **No offline mode** — CRDT exists but no real offline-first architecture yet
12. **Small company** — ~10 employees, limited support capacity
13. **Performance at scale** — hasn't been tested beyond SMB data volumes
14. **No vertical specialization** — generic SMB CRM, no IT/Consulting/SaaS features
15. **Cloud pricing unclear** — pricing page is vague, no public enterprise tiers

## 6. SCORECARD (1-10)

| Category | Score | Notes |
|----------|-------|-------|
| Lead Management | 2 | Basic contact capture only. No lead scoring, routing, or forms |
| Contact Management | 4 | Good for simple contact mgmt. No dedup, enrichment, or hierarchies |
| Account Management | 3 | Companies object is basic, no org hierarchy |
| Deal Management | 3 | Basic pipeline, no forecasting, no product catalog |
| Automation | 1 | No workflow or automation engine |
| Reporting | 2 | Activity log only. No dashboards or custom reports |
| Customization | 5 | Custom objects early stage. Custom fields good. No page layouts |
| Administration | 2 | Basic permissions. No sandboxes, no metadata management |
| AI | 0 | No AI features whatsoever |
| Integrations | 3 | GraphQL API + webhooks, but no marketplace |
| Ease of Use | 8 | Excellent UI. Minimal learning curve |
| Scalability | 2 | Untested at enterprise scale |
| Pricing | 7 | Free AGPL self-host. Cloud pricing competitive |
| Customer Support | 2 | Community-only. Small team |
| Mobile | 0 | No mobile app |

**Overall: 3.0/10** — Promising foundation with excellent architecture and design. Missing virtually all features required for mid-market and enterprise. Strongest OSS competitor on trajectory, but 2-3 years behind sovereign CRM vision.

## 7. COMPETITIVE ANALYSIS: TWENTY VS SOVEREIGN

| Dimension | Twenty | Sovereign CRM |
|-----------|--------|---------------|
| License | AGPL (copyleft) | AGPL (by choice) |
| Self-Host | Yes (Docker) | Yes (Docker + single-tenant) |
| Backend | NestJS/Node.js | Go + gRPC |
| Frontend | React/TypeScript | React/TypeScript |
| API | GraphQL + REST | GraphQL + REST + gRPC |
| Database | PostgreSQL | PostgreSQL + TimescaleDB |
| Sync | Yjs CRDT | CRDT + Native Offline |
| Offline | No | Full CRDT offline-first |
| Mobile | None | Native mobile (CRDT sync) |
| AI | None | BYO-LLM MCP-native |
| Workflows | None | Visual workflow builder |
| Marketing | None | Email, forms, landing pages, scoring |
| Service | None | Ticketing, KB, SLA, portals |
| Enterprise | None | RBAC, sandboxes, audit, SSO |
| Reporting | Basic | Full BI with custom dashboards |
| Vertical | None | IT Consulting + SaaS templates |

## 8. OUR STRATEGIC RESPONSE

**Twenty is our most relevant OSS competitor.** They have community momentum and modern architecture. But they are 2-3 years behind our planned feature depth. Key differentiators:

1. **Go backend (vs Node.js)** — better performance, lower TCO at scale
2. **Full offline-first** — Twenty has CRDT in-browser but no true offline
3. **Mobile from day one** — Twenty has no mobile strategy
4. **AI-native architecture** — Twenty has no AI story
5. **Enterprise depth** — Twenty is SMB-only for foreseeable future
6. **Vertical specialization** — IT Consulting + SaaS out of the box

We should monitor Twenty's development velocity closely. If they accelerate enterprise features, they could become a threat. Currently, they validate the open-core CRM market we are targeting.

---

*Sources: twenty.com GitHub repository, twenty.com website, Discord community, Hacker News discussions, GitHub issues, product walkthrough.*
