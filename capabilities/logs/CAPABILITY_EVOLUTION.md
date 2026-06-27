# Capability Evolution Log


## 2026-06-18 - Capability Upgrade Scan (Week 3)

### Discoveries:

#### 1. Local-First Sync Engines
- **Zero 1.0** (rocicorp/mono, ★3,287) - Production-ready since June 8. Supabase schema change hook confirmed. No new challengers. Zero remains the recommended primary sync layer.
- **TanStack DB** (★3,792, v1.0.40) - Steady releases. Tauri SQLite persistence v0.2.0. Incremental adoption path alongside Zero.

#### 2. Go-Based Backend Architectures for CRMs
- **Wuphf (nex-crm/wuphf, ★1,190, YC S26)** - Go multi-agent AI office. Terminal-native, AI employees collaborate with shared knowledge graph. Supports Codex, Claude Code, local LLMs. Validates Go + AI-native paradigm.
- **Bonds (naiba/bonds, ★73)** - Go + React rewrite of Monica CRM (24k★). Single binary + SQLite, CardDAV/CalDAV sync. HN Show HN. Validates Go CRM backend at personal CRM scale.
- **crmkit (★26, v0.6.0)** - AI-first CRM for ChatGPT/Claude. Directly validates Sovereign CRM thesis.

#### 3. Local LLM Orchestration via MCP and Ollama
- **MCP 2026 Roadmap published** - Streamable HTTP, OAuth 2.1, remote servers, enterprise auth, audit trails, working groups. MCP maturing from dev tool to enterprise connectivity layer.
- **Microsoft Dynamics 365 MCP at Build** - Enterprise CRM validation.
- **Twenty CRM ★50,376** (+4k in 72h). v2.14.0 (Jun 15). MCP-native, Apps framework (v2.0), AI chat, AI agents. Shipping daily.
- **Relaticle v3.3.8** (★1,360) - 30 MCP tools, daily releases, schema discovery.
- **Build remote MCP server** with Streamable HTTP + OAuth 2.1 from day one.

#### 4. Next.js 16 Performance Patterns
- **Next.js 16.2** current. Turbopack default, PPR via Cache Components default.
- **PPR + Suspense + TanStack Virtual + Zero IndexedDB** - addresses slow dashboard complaint.
- Top template: next-shadcn-dashboard-starter (★6,577).

### Reddit CRM Complaints (Jan-Jun 2026)

Sources: 950+ reviews (r/sales, r/CRM, r/CRMSoftware, r/SaaS, r/gohighlevel).

Fresh threads: "In 2026, what makes a CRM useful?" (adoption > features), "CRM for people who hate CRMs" (validates thesis), "Manual data entry in 2026 is wrong" (AI enrichment expected), "Lead follow-up still broken."

| Rank | Complaint | Micro-Feature |
|:----:|-----------|--------------|
| 1 | Manual data entry | AI enrichment |
| 2 | Bloat | Minimal UX, 1-click pipeline |
| 3 | Slow dashboards | Zero + PPR = instant UI |
| 4 | No offline | Zero sync layer |
| 5 | Lead routing broken | AI lead routing |
| 6 | AI bolted-on (rising) | AI-first architecture |

### Competitive Matrix

| Feature | Twenty CRM | Relaticle | Salesforce | Wuphf | Sovereign CRM |
|---------|:---------:|:---------:|:----------:|:----:|:-------------:|
| Stars | ★50,376 | ★1,360 | N/A | ★1,190 | - |
| Stack | TS/Nest.js | Laravel/PHP | Apex | Go | Go + Next.js 16 |
| Local-first | No | No | No | No | Yes (Zero) |
| MCP | Native | 30 tools | Agentforce | N/A | Planned |
| Offline | No | No | No | No | Yes |
| Go backend | No | No | No | Yes | Yes |
| Release | Daily | Daily | Quarterly | Multi/day | TBD |

### Competitive Window: 6-9 Months

Risks: Twenty (★50k, daily) could add offline. MCP is table stakes. Wuphf (YC S26) validates Go+AI. crmkit validates thesis.

Unique triad: (1) Offline-first Zero, (2) Go business CRM backend, (3) MCP roadmap-compliant.

### Recommendations
1. MCP server Weeks 1-4 (Streamable HTTP, OAuth 2.1, 40+ tools, schema discovery)
2. Zero sync Weeks 1-8 (ZQL: Contact, Deal, Account, Activity)
3. Go modular monolith Weeks 1-12 (Gin, PostgreSQL, Redis, event-driven routing)
4. Next.js 16 PPR dashboard (CDN shell, Suspense streaming, TanStack Virtual)
5. AI-first agents as first-class citizens, not AI wrapper

---

## 2026-06-15 - Capability Upgrade Scan (Week 2)

### Discoveries:

#### 1. Local-First Sync Engines (CRDTs)
- **Zero 1.0 by Rocicorp** (github.com/rocicorp/mono) — ★3.3k, 9,700+ commits. **Released June 8, 2026**, the first stable version after 2 years of development. Schema change hooks for Supabase, relational queries via ZQL, instant UI against IndexedDB with Postgres as source of truth. Linear is mid-migration from Replicache to Zero. Critical: Zero replaces the old KV-based Replicache model with first-class ORM-style queries (), making complex CRM domains natural to express.
- **Yjs** (github.com/yjs/yjs) — The most mature CRDT library. Production-ready with huge community. Powers tldraw, Excalidraw, TipTap. Key self-hosted server option: **Y-Sweet** (github.com/jamsocket/y-sweet) — open-source Yjs sync and persistence server backed by S3-compatible storage, like Figma's architecture.
- **ElectricSQL** (electric-sql.com) — Pivoted to server-authority + shape-based subscription model. Uses PGlite (WASM Postgres) as local client DB with Postgres logical replication. Strengths: leaves existing Postgres backend untouched, works with existing ORMs. Weakness: no direct client writes (no optimistic updates without layering TanStack Query).
- **TanStack DB 0.6** (tanstack.com/db/latest) — March 2026: added SQLite-backed persistence, offline support, hierarchical includes. Reactive client-first store with live queries and optimistic mutations. Safest early-2026 pick for incremental adoption.
- **OT vs CRDT consensus (2026)**: Use CRDTs for offline-first, P2P, or distributed apps. Use OT for always-online centralized coordination. For a CRM with offline capabilities, CRDTs (Yjs) are the clear choice.
- Source: Youngju.dev "Real-time Collaboration Engines & Sync 2026 Deep Dive" (May 2026) — comprehensive survey of Liveblocks, PartyKit, Yjs, Automerge, ElectricSQL, Replicache, Zero, Convex, Triplit, Jazz.tools, Loro.

#### 2. High-Performance Go-Based Backend Architectures for CRMs
- **GopherCRM** (github.com/florinel-chis/GopherCRM) — Go backend + React TypeScript frontend. Lead management, customer tracking, support tickets, real-time analytics. Built with Gin framework, PostgreSQL, Redis for queues. Clean modular monolith structure with cmd/internal separation. Recently generated significant interest (built with Claude Code).
- **CRM-system-go-microservices** (github.com/Rahugg/CRM-system-go-microservices) — Go microservices CRM using Gin, Kafka for event-driven architecture, PostgreSQL, in-memory caching. Shows Go + event-driven pattern for CRM workloads.
- **Modular Monolith resurgence**: 2026 trend favors modular monolith over full microservices for most CRM deployments — simplicity of monolith with enforced module boundaries. Go's package system makes this natural.
- **Event-Driven Architecture in Go**: Packt published "Event-Driven Architecture in Golang" (2026). Go's goroutines and channels provide natural primitives for event-driven CRM backends handling lead scoring, pipeline transitions, and notification workflows.
- **Sovereign CRM differentiation**: No existing Go-based CRM has reached the scale of Twenty (TypeScript/Nest.js, 46k★) — Go backend would be a genuine differentiator for performance-critical paths.

#### 3. Local LLM Orchestration via MCP and Ollama
- **Model Context Protocol (MCP) has become the de facto standard** for AI agent integration as of 2026. In 18 months since open-sourcing, it's now the standard for connecting LLMs to tools and data.
- **Relaticle** (github.com/Relaticle/relaticle) — ★1.3k. **Revelation**: A self-hosted open-source CRM with a **production-grade MCP server exposing 30 tools** for full CRM operations. Built with Laravel 12, Filament 5, PHP 8.4. 22 custom field types, REST API with full CRUD, schema discovery for AI agents, 5-layer authorization with team-scoped data. **This demonstrates the MCP-native CRM pattern that Sovereign CRM should target.**
- **Twenty CRM v2.13.0** (github.com/twentyhq/twenty) — ★46k, actively shipping (release 6 hours ago). Native MCP server support with AI/MCP tool schemas (including MORPH_RELATION join columns). The leading open-source Salesforce alternative now has first-class MCP/AI integration.
- **Ollama MCP ecosystem**: ollama-mcp-bridge, MCPHost, Open WebUI all support local LLM ↔ MCP connection. Multiple guides published April-May 2026 for running Ollama + MCP with Qwen3.5, Gemma 4, Llama 4.
- **Agent-Native CRM Architecture (2026)**: Three-layer pattern — (1) Unified Data Backbone with vector search, (2) Schema-Aware Context Injection (not just field-level APIs but full object model awareness), (3) Trust and Governance Wrapper (PII masking, RBAC, prompt injection defense). Salesforce's Agentforce crossed $540M ARR proving market demand.

#### 4. Next.js 14/15 Performance Patterns for Data-Heavy Dashboards
- **Next.js 16 is current** (released Oct 2025), with Next.js 16.2 latest (March 2026). Turbopack default, Cache Components as the new PPR path.
- **Partial Prerendering (PPR) is stable** in Next.js 15 and production-ready in Next.js 16. Mental model: treat page as a static shell with explicitly labelled dynamic holes. Perfect for CRM dashboards where nav/sidebar is static but data panels stream in.
- **PPR key pattern for Sovereign CRM**: Static shell (navigation, layout, UI chrome) pre-rendered to CDN. Dynamic data panels (deals table, activity feed, analytics charts) stream via nested Suspense boundaries. Results in instant navigation with fresh data.
- **SitePoint RSC Streaming Guide (Feb 2026)**: Building a streaming dashboard with Next.js 15's PPR, nested Suspense, and Edge Runtime. Data-heavy dashboards benefit from streaming skeleton states then filling content as data arrives.
- **Next.js 16 Performance Cheat Sheet (May 2026)**: Turbopack default reduces dev iteration, Cache Components simplify data caching,  directive for granular cache control.
- **Key optimization for data-heavy dashboards**: Server Components for initial data fetch, client components only for interactive elements, streaming via Suspense for slow queries, PPR for hybrid static/dynamic pages, virtualized lists (TanStack Virtual) for long CRM tables.
- **Comparison context**: Twenty CRM uses Nest.js backend + React frontend (not Next.js). Sovereign CRM using Next.js 15/16 could achieve better dashboard performance through PPR and Server Components.

### Reddit CRM Complaints Analysis (r/sales, r/CRM, r/CRMSoftware)
Sources analyzed: "What CRM you use and what are your biggest hitches" (r/sales), "What's missing in your CRM?" (r/CRM), "CRM wishlist" (r/sales), "What is expected in a modern CRM from 2026" (r/CRM), "SMB owners: biggest pain point with CRM" (r/CRM), "What's the must-have CRM feature" (r/CRM), "Which CRM are you using in 2026" (r/CRMSoftware), GummySearch aggregated analysis of 893 Reddit reviews.

**Top Recurring Complaints:**
1. **"Too much manual data entry"** — the #1 complaint across threads. Salesforce reps spend only 29% of time selling; CRM data entry is the single largest non-selling work category.
2. **"Bloated with features we don't need"** — Microsoft Dynamics, Salesforce, and HubSpot all criticized for trying to be everything to everyone, creating overwhelming interfaces.
3. **"Slow performance"** — Legacy CRMs (especially self-hosted PHP solutions) suffer from page load latency, especially on dashboard views with large datasets.
4. **"No real offline capability"** — Sales reps in the field lose connectivity and can't access or update CRM data. "Subways, airplanes, mountain valleys" are dead zones.
5. **"Hard to customize without expensive consultants"** — Salesforce customization requires admin certifications; even open-source PHP CRMs require deep PHP knowledge.
6. **"AI features feel bolted on, not native"** — Users complain AI features in legacy CRMs are glorified copilots that draft emails but can't execute autonomously.
7. **"Poor mobile experience"** — Mobile apps are afterthoughts, missing core functionality available on desktop.
8. **"Integrations are brittle"** — Zapier/Make connectors break, custom API integrations require constant maintenance.

**Micro-Features That Could Be Competitive Advantages:**
- **AI-assisted data enrichment** — Auto-populate contact fields from email signatures, LinkedIn, public sources. Reddit users consistently mention this as a "would pay for" feature.
- **Offline-first with seamless sync** — Work entirely offline, sync when connected. Nobody expects to lose data when the WiFi drops.
- **Activity timeline view** — Chronological view of every interaction (email, call, meeting, note) automatically assembled. Users love HubSpot's timeline but hate the cost.
- **Built-in communication logging** — Native email sync, call recording, SMS logging without third-party integrations.
- **One-click pipeline updates** — Reduce deal stage updates from 5 clicks to 1. Speed matters in daily workflows.
- **AI-powered lead qualification** — Auto-score leads based on engagement signals, not just manual field entry.
- **Deal risk detection** — Surface deals at risk of stalling (old pipeline stage, no recent activity, competitor mentions) proactively.
- **Native document generation** — Generate proposals, quotes, contracts from CRM data without switching to Office/Google Docs.
- **Customer health scoring** — Combine support ticket severity, email responsiveness, payment history into a single health score.
- **Visual pipeline with drag-and-drop** — Users consistently praise Pipedrive's visual pipeline but wish it had more backend power.

### Recommended Architectural Changes for Sovereign CRM

1. **Adopt Zero sync engine for local-first architecture**
   - Zero 1.0 (just released) is stable and production-ready. Postgres as source of truth, IndexedDB client, instant UI, automatic background sync.
   - Enables offline-first capability (solves #4 complaint: "no real offline capability").
   - Relational query model fits CRM data naturally (contacts → deals → activities → notes).
   - Linear's successful migration from Replicache to Zero validates the approach for CRM-like workloads.

2. **Build MCP-native CRM capabilities (the Relaticle pattern)**
   - Expose a production-grade MCP server with 30+ CRM operation tools (contacts CRUD, deal management, activity logging, search, analytics).
   - Schema discovery endpoints so AI agents understand the full CRM object model.
   - Connect local Ollama models via MCP for AI-powered features: auto-enrichment, lead scoring, deal risk detection, task generation.
   - This positions Sovereign CRM as "agent-native" — the architectural direction Salesforce, HubSpot, and Pipedrive are all racing toward.

3. **Implement the Three-Layer Agent-Native Architecture**
   - Layer 1: Unified Data Backbone — harmonize contacts, deals, activities, emails, calendar events in a single queryable layer with vector embeddings for semantic search.
   - Layer 2: Schema-Aware Context Injection — agents get full object model context, not just field-level API access.
   - Layer 3: Trust & Governance Wrapper — PII masking, RBAC, prompt injection defense at the MCP server level.

4. **Use Next.js 16 with PPR for the dashboard**
   - Static shell (navigation, layout) pre-rendered to CDN.
   - Dynamic panels (deals table, analytics, activity feed) streamed via Suspense + PPR.
   - Server Components for initial data fetch, client components only for interactivity.
   - TanStack Virtual for virtualized CRM tables handling 10,000+ rows.
   - This provides the "instant UI" feel that differentiates from slow legacy CRMs.

5. **Adopt Go modular monolith for the backend**
   - Go's goroutines and channels for event-driven lead routing, pipeline transitions, notification processing.
   - Modular monolith (not full microservices) for deployment simplicity with enforced module boundaries.
   - PostgreSQL as primary database with Redis for queues and caching.
   - The absence of a major Go-based CRM is a genuine market gap — GopherCRM proves the concept.

6. **Prioritize the top-3 micro-features from Reddit analysis**
   - AI-assisted data enrichment (auto-populate from public sources)
   - Offline-first with seamless Zero sync
   - Activity timeline with auto-logged communications

---

## 2026-06-07 - Capability Upgrade Scan (Week 1)

### Discoveries:
*(Previous week's findings — see reference: capability-upgrade-scan/references/sovereign_crm_scan_2026-06-07.md)*

---


## 2026-06-19 — Capability Upgrade Scan (Week 2, Day +1)

### Key Change Since Yesterday

- **Twenty CRM hit 50,560★** (+184 since June 18, +~4,500 since June 7). Still at v2.14.0 (June 15) — no v2.15 yet.
- **Relaticle v3.3.8** (June 16) — 1,364★ (+4 since yesterday).
- **Wuphf v0.228.1** (June 18) — shipping multiple daily releases. 1,191★.
- **crmkit v0.6.0** (June 18) — 26★. Stable since last scan.
- **Zero (rocicorp/mono)**: 3,287★. InfoQ article confirming Zero 1.0 stability.
- **TanStack DB**: 3,792★. v0.6 stable.
- **Ollama v0.30.8** (June 12) — latest version with expanded GGUF HW support.

### Discoveries:

#### 1. Local-First Sync Engines
- **Zero 1.0 confirmed stable** — InfoQ feature article published. Schema change hooks, relational ZQL queries, instant UI from IndexedDB. Linear mid-migration from Replicache validates CRM-like workload fit.
- **CRDTs mature category** — Yjs powers tldraw/Excalidraw/TipTap. Automerge 2.0 production-ready (JS + Rust).
- **TanStack DB 0.6** — SQLite persistence, offline, hierarchical includes. Safest incremental adoption path.
- **ElectricSQL** — Server-authority + shape subscriptions. No direct client writes limitation.

#### 2. Go-Based Backend Architectures for CRMs
- **Wuphf (★1,191, YC S26)** — Go multi-agent AI office. Validates Go + AI-native paradigm.
- **crmkit (★26, Go, MIT)** — AI-first CRM for ChatGPT/Claude. Headless API. Agent-first CRM thesis in Go.
- **Bonds (★73, Go)** — Monica CRM rewrite in Go + React. Single binary + SQLite. Show HN.
- **Modular Monolith renaissance** — CNCF Q1 2026: 42% of orgs consolidating microservices. Go package system natural fit.
- **Market gap**: No Go business CRM has mainstream adoption.

#### 3. Local LLM Orchestration via MCP and Ollama — BREAKING: MCP Specification Release Candidate
- **MCP 2026-07-28 Release Candidate published** (major revision since launch):
  - **Stateless protocol** — Server retains no client state. Scales on ordinary HTTP infrastructure.
  - **MCP Apps extension** — Servers ship interactive HTML in sandboxed iframes.
  - **Tasks graduated** — Long-running, cancellable, resumable work.
  - **Full JSON Schema 2020-12** for tool definitions.
  - **OAuth 2.1 + OpenID Connect** for enterprise authorization.
  - **Formal deprecation policy**. Final spec due July 28, 2026.
- **Ollama MCP bridge maturing**: ollama-mcp-bridge, MCPHost. PulseMCP: 16,810+ servers.
- **Ollama v0.30.8**. Best local CRM models: Qwen 3.6 27B (77.2% SWE-bench), Llama 4 Scout (10M ctx), MiniMax M3.
- **Relaticle MCP** (v3.3.8) with 30 tools remains reference pattern for MCP-native CRM.

#### 4. Next.js 16 Performance Patterns
- **Next.js 16 PPR production stable** — Mastercard Dynamic Yield confirmed use.
- **PPR for CRM**: Static shell (nav/layout) to CDN, data panels via Suspense streaming.
- **Top template**: next-shadcn-dashboard-starter (★6,577). TanStack Virtual v8 for 10k+ rows.
- **Key optimization**: Server Components + Zero IndexedDB for instant local reads.

### Reddit CRM Complaints Analysis
(r/CRM, r/sales, r/CRMSoftware, r/salestechniques, r/Solopreneur, r/AI_Agents — 950+ reviews)

**New threads**: Manual data entry viral thread, Sales frustrations, Sales process manual parts, Best CRM small biz 2026, Which CRM 2026 (AI primary filter), AI agents by use case.

**Top 10 Complaints**: 1) Manual data entry/post-meeting cleanup (29% rep time), 2) Bloated features, 3) Slow performance, 4) No offline, 5) AI bolted on, 6) AI hype misses boring work, 7) Clean data prerequisite, 8) Lead scoring manual, 9) Post-meeting cleanup silent time sink, 10) Brittle integrations.

**New Micro-Features**: Auto-post-meeting cleanup AI agent, Voice-driven CRM updates, Proactive deal health monitoring, Auto-lead enrichment, One-click pipeline updates.

### Competitive Positioning
| Feature | Twenty CRM | Relaticle | Salesforce | HubSpot | Wuphf | Sovereign CRM |
|---------|:---------:|:---------:|:----------:|:-------:|:----:|:-------------:|
| Stars | ★50,560 | ★1,364 | N/A | N/A | ★1,191 | — |
| Stack | TS/Nest.js | Laravel/PHP | Apex | Java/Node | Go | Go+Next.js16 |
| Local-first | No | No | No | No | No | **Yes (Zero)** |
| MCP | Native | 30 tools | Agentforce | GA | N/A | **Planned** |
| Offline | No | No | No | No | No | **Yes** |
| Self-hosted | Yes | Yes | No | No | Yes | **Yes** |
| Go backend | No | No | No | No | Yes | **Yes** |
| Schema discovery | No | **Yes** | No | No | No | **Planned** |
| MCP spec 2026-07-28 | ? | ? | ? | ? | N/A | **Target** |
| Latest release | v2.14.0 | v3.3.8 | Summer 26 | Jun 5 | v0.228.1 | — |

### Competitive Window: 6-9 months (unchanged)
- Twenty at 50k could add offline. Extensibility SDK widening moat.
- **MCP 2026-07-28 spec creates urgency** — build to stateless spec by July 28.
- Relaticle's 30 MCP tools is the bar to clear (target 40+).
- Wuphf (YC S26) validates Go + AI-native paradigm.
- Modular monolith trend favors Go architecture.

### Recommended Architectural Changes for Sovereign CRM
1. **MCP server is THE priority — ship before July 28, 2026**: Build to stateless spec (Streamable HTTP, OAuth 2.1, JSON Schema 2020-12). Target 40+ tools. Schema discovery for AI agents. Trust & Governance Wrapper (PII masking, RBAC, prompt injection). MCP Apps support. Ollama bridge for on-premise AI.
2. **Adopt Zero sync engine**: Zero 1.0 stable/production-ready. Postgres + IndexedDB = instant UI + offline. ZQL queries map naturally to CRM domain model. Linear migration validates approach.
3. **Go modular monolith backend**: Gin, PostgreSQL, Redis. Event-driven architecture for lead routing, pipeline transitions. Single binary deployment.
4. **Next.js 16 PPR dashboard**: Static shell to CDN, data panels via Suspense streaming. TanStack Virtual for 10k+ rows. Zero IndexedDB for instant reads.
5. **Build post-meeting cleanup AI agent first**: Addresses #1 micro-feature. Voice-driven CRM updates. Auto-extract action items, update stages, create tasks. Serve via MCP Tools.
6. **Ship top micro-features**: AI data enrichment, offline-first with Zero, activity timeline, one-click pipeline updates.

---
