# 🏗️ Revenue OS — Open Source Tool Catalog

> **Purpose:** Definitive shopping list of open-source building blocks for an AI-Powered Revenue Operating System with 80–120 agents.
> **Decision framework:** For each tool, we answer: *Use as-is? Minor adapt? Major rework? Inspiration only?*
> **Status:** Live catalog — update as tools evolve.

---

## 1. Installation Priority Matrix

| Tool | Category | Priority | Effort (hrs) | Replaces | Decision |
|------|----------|----------|-------------|----------|----------|
| Twenty CRM | CRM | **Critical** | 8–16 | Salesforce, HubSpot | Self-host, use REST API |
| CrewAI | Agent orchestration | INSPIRATION ONLY — NOT in critical path | 4–8 | n8n (partial), Zapier | Reference for agent design patterns only — do not integrate. NATS event mesh replaces CrewAI orchestration. |
| Qdrant | Vector store | **Critical** | 2–4 | Pinecone | Self-host, attach to agents |
| call.md | Call intelligence | **Critical** | 4–8 | Gong, Chorus | Self-host, webhook pipeline |
| Supabase | Backend / Auth | **Critical** | 4–8 | Firebase, Auth0 | Self-host, auth + storage |
| OpenTelemetry | Observability | **Critical** | 4–8 | Datadog, New Relic | Self-host collector |
| Prometheus + Grafana | Monitoring | **Critical** | 4–8 | Datadog | Wire to OTel |
| Whisper (faster-whisper) | Transcription | **High** | 2–4 | Deepgram | Self-host, GPU optional |
| LangGraph | Agent orchestration | **High** | 8–16 | — | Complex multi-step flows |
| NATS JetStream | Message bus | **High** | 4–8 | RabbitMQ, Kafka | Agent intercom |
| Resend | Email | **High** | 2 | SendGrid, Mailgun | Transactional + campaigns |
| QStash | Queue / HTTP | **High** | 2 | AWS SQS | Agent task queue |
| dbt | Data transform | **High** | 4–8 | — | CRM analytics layer |
| Metabase | BI / Dashboards | **High** | 2–4 | Tableau, Looker | Embedded analytics |
| PostHog | Product analytics | **High** | 4 | Mixpanel, Amplitude | Self-host or cloud |
| Unstructured.io | Document parsing | **High** | 2–4 | — | Ingest sales docs, PDFs |
| Neo4j | Knowledge graph | **High** | 8–16 | — | Entity resolution, CRM graph |
| docling | PDF extraction | **Medium** | 2 | — | Contract parsing |
| Vaultwarden | Secrets | **Medium** | 2 | 1Password, Vault | Agent credential store |
| EspoCRM | CRM (alt) | **Medium** | 4 | — | Lightweight Twenty backup |
| PocketBase | Backend (light) | **Medium** | 2 | Supabase (lite) | Microservices |
| Trivy | Security scan | **Medium** | 2 | Snyk | CI/CD pipeline |
| SuiteCRM | CRM (legacy) | **Medium** | 8 | SalesForce classic | Migration target |
| Loki | Log aggregation | **Medium** | 2 | Splunk | OTel logs |
| Jaeger / Tempo | Distributed tracing | **Medium** | 4 | DataDog APM | Agent call tracing |
| theHarvester | OSINT | **Medium** | 1 | — | Prospect enrichment |
| Chroma | Vector store (light) | **Low** | 1 | — | Dev/experimental |
| Hunter.io API | Email discovery | **Low** | 1 | — | Prospect find |
| Twilio API | SMS / Voice | **Low** | 2 | — | Outreach channel |
| WhatsApp Business API | Messaging | **Low** | 4 | — | Outreach channel |
| Bright Data API | Data collection | **Low** | 2 | — | Web scraping infra |
| Firecrawl | Web scraping | **Low** | 2 | — | Prospect site crawl |
| OpenSCAP | Compliance | **Low** | 4 | — | SOC2 prep |
| Vanta API | Compliance (read) | **Low** | 2 | — | Evidence collection |

*Note on CrewAI: NATS event mesh replaces CrewAI orchestration. CrewAI's sequential/hierarchical crew model conflicts with the event-driven architecture. Reference for agent design patterns only — do not integrate.*

---

## 2. Orchestration & Agent Frameworks (Install Now)

### 2.1 CrewAI
- **URL:** https://github.com/joaomdmoura/crewai
- **Stars:** ~25k+ ⭐
- **What it does:** Multi-agent orchestration with role-based agents, sequential/hierarchical task execution, and built-in tooling.
- **Revenue OS mapping:** Agent Orchestrator — primary agent runner for SDR, AE, CS agent teams.
- **Integration effort:** Use as-is
- **Tech stack:** Python, LangChain integration
- **Notes:**
  - Define agents as `SalesDevAgent`, `LeadQualifier`, `MeetingScheduler` with specific roles/goals.
  - Use `@tool` decorator to expose CRM actions (Twenty API, email, calendar).
  - Process: `Process.hierarchical` for complex workflows (manager agent coordinates sub-agents).
  - Tip: Set `memory=True` and attach Qdrant for cross-session context.
  - Crews should be max 4–5 agents per crew for reliability; use NATS to bridge crews.

### 2.2 LangGraph
- **URL:** https://github.com/langchain-ai/langgraph
- **Stars:** ~10k+ ⭐
- **What it does:** Framework for building stateful, multi-actor agent applications with graph-based workflows, cycles, and human-in-the-loop.
- **Revenue OS mapping:** Agent Orchestrator — complex multi-step sales workflows (negotiation, contract review).
- **Integration effort:** Minor adapt
- **Tech stack:** Python, LangChain, Pydantic
- **Notes:**
  - Use for branching workflows: qualify → nurture → propose → close.
  - `StateGraph` with `add_conditional_edges` for routing leads based on score/tier.
  - Human-in-the-loop via `interrupt_before` for manager approvals.
   - Combine with CrewAI[^1]: CrewAI for sub-crews, LangGraph for top-level workflow DAG.

### 2.3 AutoGen (Microsoft)
- **URL:** https://github.com/microsoft/autogen
- **Stars:** ~30k+ ⭐
- **What it does:** Multi-agent conversation framework with code execution sandboxing, group chats, and extensible agent types.
- **Revenue OS mapping:** Agent Orchestrator (alt) — code-writing agents, async research.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, .NET, Docker
- **Notes:**
  - `GroupChat` with `RoundRobinManager` for debate between SDR/AE/RevOps agents.
  - Code execution agents can generate and run SQL against Metabase or dbt.
  - Use `AssistantAgent` for tool-calling, `UserProxyAgent` for human handoff.

### 2.4 Mastra
- **URL:** https://github.com/mastra-ai/mastra
- **Stars:** ~6k+ ⭐
- **What it does:** TypeScript-native agent framework with workflows, RAG, memory, and eval system.
- **Revenue OS mapping:** Agent Orchestrator (Node.js agents).
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, Node.js, React (for playground)
- **Notes:**
  - Use when agents need to be deeply embedded in a Node.js/Next.js stack.
  - Built-in RAG with PGVector support.
  - `Step`-based workflows for deterministic sales sequences.
  - Good for frontend-facing agents (chat widgets, embedded assistants).

### 2.5 MCP Server Patterns
- **URL:** https://github.com/modelcontextprotocol/servers
- **Stars:** ~5k+ ⭐
- **What it does:** Model Context Protocol — standardized way for agents to discover and call tools/resources, with reference server implementations.
- **Revenue OS mapping:** All agents — agent-to-tool communication layer.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, Python, JSON-RPC
- **Notes:**
  - Every Revenue OS tool should expose an MCP server for agent consumption.
  - Use SD (Service Discovery) via NATS for MCP server registry.
  - Pattern: each domain (CRM_Read, CRM_Write, Email, Calendar) = one MCP server.
  - `tools/list`, `tools/call` are the two critical endpoints.
  - Auth: API key header (agents pass their JWT in `Authorization`).

### 2.6 NATS JetStream
- **URL:** https://github.com/nats-io/nats-server
- **Stars:** ~16k+ ⭐
- **What it does:** High-performance messaging system with persistent streams, exactly-once delivery, and key-value store.
- **Revenue OS mapping:** Agent intercom bus — async agent-to-agent messaging.
- **Integration effort:** Minor adapt
- **Tech stack:** Go, NATS protocol
- **Notes:**
  - Use `JetStream` for durable agent message queues.
  - Stream subjects per agent type: `agent.sdr.outbound`, `agent.ae.proposal`.
  - KV store for shared agent state (lead ownership, lock management).
  - Object store for file transfer (contracts, recordings) between agents.

---

## 3. Meeting & Conversation Intelligence (Install Now)

### 3.1 call.md
- **URL:** https://github.com/synaptiai/call.md
- **Stars:** ~2k+ ⭐
- **What it does:** Open-source meeting intelligence platform — records, transcribes, summarizes Zoom/Meet/Teams calls.
- **Revenue OS mapping:** Conversation Intelligence Agent — processes all sales calls.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, React, Whisper
- **Notes:**
  - Self-host with Docker Compose.
  - Webhook on call-end → triggers analysis agent (score sentiment, extract objections, log to CRM).
  - Integrates with Google Calendar + Zoom native.
  - Provides speaker diarization, topic extraction, action items.
  - Webhook payload includes: transcript, summary, action items, sentiment per segment.

### 3.2 faster-whisper (Replicate / local)
- **URL:** https://github.com/SYSTRAN/faster-whisper
- **Stars:** ~12k+ ⭐
- **What it does:** CTranslate2-based reimplementation of OpenAI Whisper for 4x faster transcription with lower memory.
- **Revenue OS mapping:** Conversation Intelligence Agent — transcription engine.
- **Integration effort:** Use as-is
- **Tech stack:** Python, CTranslate2, ONNX
- **Notes:**
  - Large-v3 model fits in 4GB VRAM.
  - Batch processing for call recordings.
  - Use `vad_filter=True` to strip silence from sales calls.
  - Output → NLP pipeline for objection detection, competitor mentions, next-step extraction.

### 3.3 Vexa
- **URL:** https://github.com/yazdipour/vexa
- **Stars:** ~500+ ⭐
- **What it does:** AI meeting assistant that joins calls, records, transcribes, and provides real-time suggestions.
- **Revenue OS mapping:** Conversation Intelligence Agent — real-time assistant.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, WebRTC, Whisper
- **Notes:**
  - Can join as a bot participant.
  - Real-time suggestions generated via LLM during the call.
  - Useful for live coaching agent — detect when rep is being talked over or missing objections.

### 3.4 Meetily
- **URL:** https://github.com/yourkin/meetily
- **Stars:** ~1k+ ⭐
- **What it does:** Open-source meeting transcription and note-taking for Google Meet with speaker labels.
- **Revenue OS mapping:** Conversation Intelligence Agent — Google Meet focused.
- **Integration effort:** Minor adapt (Chrome extension)
- **Tech stack:** JavaScript, Chrome Extension, Whisper
- **Notes:**
  - Chrome extension — lightweight, runs in-browser.
  - Captures live captions from Google Meet.
  - Sends transcript to webhook → Revenue OS pipeline.
  - Lower quality than call.md but zero infra.

### 3.5 Memoir
- **URL:** https://github.com/synaptiai/memoir
- **Stars:** ~800+ ⭐
- **What it does:** AI-powered meeting notes with automatic action item extraction and CRM sync.
- **Revenue OS mapping:** Conversation Intelligence Agent — post-call CRM update.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, React, PostgreSQL
- **Notes:**
  - Extracts action items as structured JSON.
  - Maps to CRM fields (Next Step, Owner, Due Date).
  - Auto-creates tasks in linked CRM.

### 3.6 Gong Data Integration Patterns
- **GitHub:** N/A (SaaS, API-based)
- **What it does:** Enterprise conversation intelligence platform — tracking calls, emails, and meetings with AI analytics.
- **Revenue OS mapping:** Conversation Intelligence — enterprise data source.
- **Integration effort:** Minor adapt (API consumption)
- **Tech stack:** REST API, Webhook
- **Notes:**
  - Revenue agents consume Gong API: /v2/calls, /v2/emails, /v2/scorecards.
  - Gong exposes scored call data (talk ratio, sentiment, competitive mentions).
  - Agent pattern: Poll Gong API daily, sync scored calls → CRM enrichment pipeline.
  - Webhook: `call.completed` → trigger analysis agent.
  - Gong data blends with call.md transcript for dual-source validation.

---

## 4. CRM & Data Platforms (Install Now)

### 4.1 Twenty CRM
- **URL:** https://github.com/twentyhq/twenty
- **Stars:** ~25k+ ⭐
- **What it does:** Modern open-source CRM with GraphQL API, workflows, and a HubSpot-like interface.
- **Revenue OS mapping:** **Core CRM** — primary record system for contacts, accounts, opportunities, activities.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, React, GraphQL, PostgreSQL
- **Notes:**
  - Self-host via Docker Compose (1 server, 1 worker, 1 db).
  - GraphQL API is agent-native — agents query/mutate with structured queries.
  - Custom objects: create custom objects for lead scores, deal stages, enrichment logs.
  - Webhooks: `record.created`, `record.updated` → trigger agent pipelines.
  - REST fallback available at /rest/* for simpler agents.
  - Rate limit: 100 req/min per API key (configurable).
  - Fields that agents populate: `pointOfContact`, `dealStage`, `nextActionDate`, `enrichmentScore`.
  - Recommended: 1 API key per agent type with scoped permissions.

### 4.2 EspoCRM
- **URL:** https://github.com/espocrm/espocrm
- **Stars:** ~2k+ ⭐
- **What it does:** Lightweight, extensible CRM with entity manager, workflows, and formula-based automation.
- **Revenue OS mapping:** CRM (secondary/backup) — lower complexity deployments.
- **Integration effort:** Use as-is
- **Tech stack:** PHP, MySQL/PostgreSQL, JavaScript
- **Notes:**
  - Entity Manager allows creating custom entities without code.
  - REST API: `GET /api/v1/Contact`, `POST /api/v1/Opportunity`.
  - Formula engine for conditional field updates.
  - Less agent-friendly than Twenty (no GraphQL) but simpler data model.

### 4.3 SuiteCRM
- **URL:** https://github.com/salesagility/SuiteCRM
- **Stars:** ~5k+ ⭐
- **What it does:** Enterprise-grade open-source CRM (SugarCRM fork) with full sales, marketing, service modules.
- **Revenue OS mapping:** CRM (enterprise migration target).
- **Integration effort:** Major rework
- **Tech stack:** PHP, MySQL, JavaScript
- **Notes:**
  - REST v8 API available in latest versions.
  - Heavy codebase — agent interaction is fragile without middleware.
  - Better as a data migration source → Twenty.
  - If already on SuiteCRM, build an API proxy layer to clean up responses for agent consumption.

### 4.4 PocketBase
- **URL:** https://github.com/pocketbase/pocketbase
- **Stars:** ~42k+ ⭐
- **What it does:** Single-binary backend with embedded SQLite, REST API, real-time subscriptions, and auth.
- **Revenue OS mapping:** Microservices backend — agent state, config, session store.
- **Integration effort:** Use as-is
- **Tech stack:** Go, SQLite
- **Notes:**
  - Single binary, zero deps — deploy as agent-sidecar.
  - Real-time subscriptions via SSE — agents listen for data changes.
  - Built-in file storage for call recordings, contract uploads.
  - Auth: OAuth2, email/password, JWT — agent tokens.
  - Not a CRM replacement (SQLite limitations) but excellent for per-agent state.

### 4.5 Supabase
- **URL:** https://github.com/supabase/supabase
- **Stars:** ~75k+ ⭐
- **What it does:** Open-source Firebase alternative with PostgreSQL, auth, real-time, storage, and Edge Functions.
- **Revenue OS mapping:** Backend platform — auth, storage, real-time sync, vector store (pgvector).
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, Go, PostgreSQL
- **Notes:**
  - Self-host with `supabase start` (Docker).
  - Auth: JWT tokens per agent, Row Level Security (RLS) per agent type.
  - `pgvector` extension for embedding storage (agent memory).
  - Realtime: Broadcast via PostgreSQL replication → WebSocket agents.
  - Edge Functions: deploy agent HTTP handlers without servers.
  - Storage: call recordings, documents, email attachments.
  - Master database for all Revenue OS records.

---

## 5. SDR & Prospecting (Install Now)

### 5.1 OpenSales
- **URL:** https://github.com/opensales/opensales
- **Stars:** ~500+ ⭐
- **What it does:** Open-source sales engagement platform — sequences, email tracking, task management.
- **Revenue OS mapping:** SDR Agent — outbound cadence execution.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, React, PostgreSQL
- **Notes:**
  - Manage sequences (steps with delay, conditions, branching).
  - Email tracking (opens, clicks).
  - API-first: `POST /sequences/{id}/enroll` to enroll leads.
  - Agent creates sequences dynamically based on lead segment.

### 5.2 B2B SDR Agent Template
- **URL:** https://github.com/crewAIInc/crewAI-examples (SDR example)
- **Stars:** N/A (part of CrewAI[^1] examples)
- **What it does:** Reference implementation of a multi-agent SDR team using CrewAI[^1] — lead research, outreach, qualification.
- **Revenue OS mapping:** SDR Agent — reference architecture.
- **Integration effort:** Use as-is
- **Tech stack:** Python, CrewAI[^1]
- **Notes:**
  - Roles: Lead Researcher, Outreach Specialist, Qualifier.
  - Tools: SERP search, LinkedIn scraping, email sender.
  - Extend with Twenty CRM read/write tools.

### 5.3 theHarvester
- **URL:** https://github.com/laramies/theHarvester
- **Stars:** ~12k+ ⭐
- **What it does:** OSINT tool for email, subdomain, and employee discovery from public sources (search engines, PGP, LinkedIn).
- **Revenue OS mapping:** Prospect Enrichment Agent — lead discovery.
- **Integration effort:** Use as-is (CLI wrapper)
- **Tech stack:** Python
- **Notes:**
  - `theHarvester -d company.com -b linkedin` → employee list.
  - `-b google,pgp,bing` for broader discovery.
  - Wrap as API: `POST /enrich` returns found emails → CRM upsert.
  - Rate limit per source, add delays between queries.

### 5.4 Bright Data (API integration)
- **URL:** https://brightdata.com
- **Stars:** N/A (commercial, API-based)
- **What it does:** Proxy network + scraping APIs for structured data extraction at scale.
- **Revenue OS mapping:** Prospect Enrichment Agent — data collection proxy layer.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, Proxy
- **Notes:**
  - Use `Web Unlocker` to bypass LinkedIn/company site blocks.
  - `Dataset API` for pre-built datasets (company info, employee data).
  - Agent pattern: Bright Data fetch → LLM extract → CRM enrich.

### 5.5 Hunter.io (API integration)
- **URL:** https://hunter.io
- **Stars:** N/A (commercial API)
- **What it does:** Email pattern discovery and verification API — find and validate professional emails.
- **Revenue OS mapping:** Prospect Enrichment Agent — email finding.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API
- **Notes:**
  - `GET /email-finder` → find email for specific first/last/domain.
  - `GET /email-verifier` → verify deliverability.
  - Agent workflow: theHarvester → Hunter verify → CRM create.
  - Rate limit free tier: 25 req/month. Paid: 500+/month.

### 5.6 Clay (API integration / alternative)
- **URL:** https://clay.com
- **Stars:** N/A (commercial)
- **What it does:** Waterfall enrichment platform — cascades through 50+ data sources to build complete prospect profiles.
- **Revenue OS mapping:** Prospect Enrichment Agent — multi-source merge.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, GraphQL
- **Notes:**
  - Agent calls Clay API with partial contact data → returns enriched profile.
  - Waterfall merges from Crunchbase, Apollo, LinkedIn, etc.
  - Use Clay as the "enrichment orchestrator" — feed partial data, get clean records.
  - Alternative to building custom enrichment waterfall.

### 5.7 Apollo.io (API integration)
- **URL:** https://apollo.io
- **Stars:** N/A (commercial API)
- **What it does:** B2B contact and company database with intent signals and engagement data.
- **Revenue OS mapping:** Prospect Sourcing Agent — database queries.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API
- **Notes:**
  - `POST /v1/contacts/search` → query by title, company size, industry.
  - `POST /v1/people/bulk_match` → enrich existing contact list.
  - Agent pattern: query intent API for "actively buying" signals.

---

## 6. Knowledge & Memory (Install Now)

### RAG Scope Definition (Qdrant/pgvector)

RAG is used exclusively for these three purposes:

1. **Knowledge Retrieval** — playbooks, case studies, competitive intel, pricing guidelines
   - Indexed by: deal attributes (industry, deal size, product line, competitor)
   - Retrieved by: Deal Strategy, Negotiation, Content agents

2. **Training Material Retrieval** — methodology frameworks (MEDDPICC, SPIN, Challenger, etc.)
   - Indexed by: agent role + query type
   - Retrieved by: agents during cold start and uncertain scenarios

3. **Historical Deal Patterns** — anonymized win/loss data for pattern matching
   - Indexed by: segment + deal attributes
   - Retrieved by: Deal Strategy, Qualification for similar-deal lookup

**NOT used for:**
- Real-time conversation context → use NATS KV
- CRM data queries → direct API calls
- Agent-to-agent communication → NATS events
- Real-time transcript processing → streaming buffer (not RAG)

### 6.1 Qdrant
- **URL:** https://github.com/qdrant/qdrant
- **Stars:** ~22k+ ⭐
- **What it does:** Vector similarity search engine with filtering, payload storage, and horizontal scaling.
- **Revenue OS mapping:** Agent Memory Store — all agent embeddings (contacts, emails, calls, docs).
- **Integration effort:** Use as-is
- **Tech stack:** Rust, gRPC, REST
- **Notes:**
  - `docker run -p 6333:6333 qdrant/qdrant`.
  - Collections per domain: `contact_embeddings`, `email_embeddings`, `call_transcripts`.
  - `payload` stores metadata filters (deal stage, date range, territory).
  - Agent query: `search similar deals to X` with payload filter `stage = "closed_won"`.
  - Quantization for memory efficiency on large collections.

### 6.2 pgvector
- **URL:** https://github.com/pgvector/pgvector
- **Stars:** ~13k+ ⭐
- **What it does:** PostgreSQL extension for vector similarity search — no separate database needed.
- **Revenue OS mapping:** Agent Memory Store — Supabase-native embeddings.
- **Integration effort:** Use as-is
- **Tech stack:** PostgreSQL extension (C)
- **Notes:**
  - `CREATE EXTENSION vector;` in Supabase.
  - `CREATE TABLE embeddings (id bigserial, embedding vector(1536), metadata jsonb);`
  - `ORDER BY embedding <=> $1 LIMIT 10` for similarity.
  - Simpler than Qdrant if already on Supabase; Qdrant is faster at scale.

### 6.3 Chroma
- **URL:** https://github.com/chroma-core/chroma
- **Stars:** ~16k+ ⭐
- **What it does:** Lightweight, embedded vector database for prototyping and small-scale RAG.
- **Revenue OS mapping:** Agent Memory Store (dev/experimental).
- **Integration effort:** Use as-is
- **Tech stack:** Python, TypeScript, ClickHouse
- **Notes:**
  - `pip install chromadb` — runs in-process.
  - Good for local agent memory during development.
  - Not production-grade for 50+ agent concurrent access.
  - Transition to Qdrant at scale.

### 6.4 Neo4j
- **URL:** https://github.com/neo4j/neo4j
- **Stars:** ~13k+ ⭐
- **What it does:** Native graph database with Cypher query language, ACID transactions, and graph analytics.
- **Revenue OS mapping:** Entity Resolution Graph — people, companies, relationships, deal hierarchy.
- **Integration effort:** Major rework
- **Tech stack:** Java, Cypher, Bolt protocol
- **Notes:**
  - Model: `(Person)-[:WORKS_AT]->(Company)`, `(Company)-[:IN_INDUSTRY]->(Sector)`.
  - Agent query: `MATCH (p:Person)-[:WORKS_AT]->(c:Company) WHERE c.employees > 500 RETURN p`.
  - Use APOC library for advanced graph algorithms (PageRank for influence scoring).
  - Cypher is agent-friendly as a tool (tool: `graph_query`, argument: Cypher).
  - Sync from Twenty CRM via change-data-capture webhooks.
  - NOT a CRM replacement — CRM in Twenty, relationship graph in Neo4j.

### 6.5 Memory MCP
- **URL:** https://github.com/modelcontextprotocol/servers (memory server)
- **Stars:** ~5k+ ⭐ (MCP servers repo)
- **What it does:** MCP server providing persistent memory (facts, entities, relations) for AI agents using a knowledge graph.
- **Revenue OS mapping:** Agent Memory — cross-session fact recall.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, JSON-RPC, graph
- **Notes:**
  - Agents read/write facts: `entity: "Acme Corp", fact: "uses Salesforce", confidence: 0.9`.
  - Start with `npx @modelcontextprotocol/server-memory`.
   - Attach to every agent in CrewAI[^1] / LangGraph via `mcp_servers` config.
  - Short-term memory lives here; long-term in Qdrant/Neo4j.

### 6.6 knowledge-ops
- **URL:** GitHub ops/knowledge management (ECC skill)
- **Stars:** N/A (skill)
- **What it does:** Knowledge base management pipeline — ingest, sync, deduplicate, search across local files, vector stores, and Git repos.
- **Revenue OS mapping:** Agent Knowledge Pipeline — automated ingestion.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, MCP, vector store
- **Notes:**
  - Automated sync: CRM notes → embeddings → searchable.
  - Deduplication before vector insert.

---

## 7. Research & Intelligence (Install Now)

### 7.1 Agent-Reach
- **URL:** GitHub agent skill (see AGENTS.md)
- **Stars:** N/A (skill)
- **What it does:** Multi-platform search across 17 channels (web, YouTube, GitHub, Reddit, LinkedIn, Twitter/X, Bilibili, RSS, podcasts).
- **Revenue OS mapping:** Research Agent — account/prospect intelligence.
- **Integration effort:** Use as-is
- **Tech stack:** Python, CLI, MCP
- **Notes:**
  - Agent queries: "find recent news about {company}" → web + RSS + news.
  - "find decision makers at {company}" → LinkedIn + GitHub.
  - Channel config via SKILL.md routing table.

### 7.2 last30days
- **URL:** GitHub agent skill
- **Stars:** N/A (skill)
- **What it does:** Cross-platform trend/engagement research (Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub).
- **Revenue OS mapping:** Research Agent — competitive intel, market sensing.
- **Integration effort:** Use as-is
- **Tech stack:** Python, CLI
- **Notes:**
  - `/last30days "competitor X"` → posts, sentiment, vote counts.
  - Agent enriches prospect profiles with public sentiment data.
  - Feed to LLM for competitive positioning analysis.

### 7.3 social-fusion
- **URL:** GitHub agent skill
- **Stars:** N/A (skill)
- **What it does:** Unified LinkedIn/Reddit/Instagram query with dual-source LinkedIn fusion.
- **Revenue OS mapping:** Research Agent — social intelligence.
- **Integration effort:** Use as-is
- **Tech stack:** Python, PRAW, Instaloader, linkedin-api
- **Notes:**
  - Agent asks: "find all LinkedIn posts by {prospect} last 90 days".
  - Fusion compares linkedin-api vs linkedin-mcp-server results.
  - Social proof for outreach personalization.

### 7.4 Firecrawl
- **URL:** https://github.com/nickbaumann98/firecrawl
- **Stars:** ~15k+ ⭐
- **What it does:** Web scraping API that converts websites to clean markdown or structured data — handles JS rendering, anti-bot.
- **Revenue OS mapping:** Prospect Site Agent — company website intelligence.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, Puppeteer, REST API
- **Notes:**
  - `POST /scrape` → returns markdown of prospect website.
  - Agent uses to extract: tech stack, pricing page, team page.
  - `POST /crawl` → deep crawl (pricing, blog, about, careers).
  - Use as enrichment trigger when lead enters "researching" stage.

### 7.5 crawl4ai
- **URL:** https://github.com/unclecode/crawl4ai
- **Stars:** ~25k+ ⭐
- **What it does:** Open-source LLM-friendly web crawler with async batch crawling, extraction strategies, and LLM integration.
- **Revenue OS mapping:** Prospect Site Agent — batch competitor/prospect crawling.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, aiohttp, BeautifulSoup
- **Notes:**
  - `async_crawl_many(urls, strategy="llm")` — extract structured data.
  - Strategies: CSS selector, LLM extraction, cosine relevance.
  - Agent uses for competitive intelligence: crawl top 10 competitor pricing pages.
  - Cheaper than Firecrawl for high-volume (self-host).

### 7.6 theHarvester
*(See Section 5.3 — also relevant for research)*

---

## 8. Document & Content (Install Now)

### 8.1 Nutrient Document Processing (DWS API)
- **URL:** https://www.nutrient.io
- **Stars:** N/A (commercial API, open-source SDK components)
- **What it does:** Full document processing pipeline — convert, OCR, extract, redact, sign, fill for PDFs, DOCX, XLSX, PPTX.
- **Revenue OS mapping:** Contract Intelligence Agent — process inbound/outbound documents.
- **Integration effort:** Minor adapt
- **Tech stack:** REST API, various SDKs
- **Notes:**
  - Agent workflow: inbound PDF contract → OCR → extract terms → validate → CRM update.
  - Detect: renewal date, pricing changes, liability caps, auto-renewal clauses.
  - Template fill for outbound proposals.

### 8.2 Unstructured.io
- **URL:** https://github.com/Unstructured-IO/unstructured
- **Stars:** ~9k+ ⭐
- **What it does:** Pre-processing library for unstructured documents (PDF, HTML, Word, email) — chunk, classify, extract.
- **Revenue OS mapping:** Document Ingestion Agent — chunk + embed pipeline.
- **Integration effort:** Use as-is
- **Tech stack:** Python
- **Notes:**
  - `partition_pdf()` → list of elements (Title, NarrativeText, Table, etc.).
  - `chunk_by_title()` for RAG-ready chunks.
  - `POST /general/v0/general` → returns structured elements.
  - Agent pipeline: Unstructured → embed (OpenAI/Cohere) → Qdrant.

### 8.3 docling
- **URL:** https://github.com/DS4SD/docling
- **Stars:** ~15k+ ⭐
- **What it does:** Document understanding and conversion — PDF, DOCX, PPTX → Markdown, JSON, structured representations with layout preservation.
- **Revenue OS mapping:** Document Extraction Agent — contract terms, financial data.
- **Integration effort:** Use as-is
- **Tech stack:** Python, PyTorch
- **Notes:**
  - IBM-developed, excellent table extraction from PDFs.
  - Understands complex layouts (multi-column, headers/footers).
  - Output: JSON with `pages[].tables[]` and `pages[].text`.
  - Agent uses: extract pricing tables from competitor brochures.

### 8.4 marker
- **URL:** https://github.com/VikParuchuri/marker
- **Stars:** ~18k+ ⭐
- **What it does:** PDF to markdown conversion with high accuracy — handles tables, equations, headers.
- **Revenue OS mapping:** Document Extraction Agent — contract to markdown pipeline.
- **Integration effort:** Use as-is
- **Tech stack:** Python, PyTorch, Surya
- **Notes:**
  - `marker_single(pdf_file, output_dir)` → markdown output.
  - Higher accuracy than PyMuPDF for complex PDFs.
  - GPU recommended but CPU works (slower).

---

## 9. Monitoring & Observability (Install Now)

### 9.1 OpenTelemetry Collector
- **URL:** https://github.com/open-telemetry/opentelemetry-collector
- **Stars:** ~4k+ ⭐
- **What it does:** Vendor-agnostic telemetry collection — traces, metrics, logs from agents and infrastructure.
- **Revenue OS mapping:** Observability Layer — all agent telemetry.
- **Integration effort:** Minor adapt
- **Tech stack:** Go, OTLP protocol
- **Notes:**
  - Every agent emits OTLP: traces (agent call chain), metrics (tasks/sec, latency), logs.
  - Deploy OTel Collector as sidecar per agent pod.
  - Export to Prometheus (metrics), Tempo (traces), Loki (logs).
  - Configure batch processor to reduce egress costs.

### 9.2 Prometheus
- **URL:** https://github.com/prometheus/prometheus
- **Stars:** ~57k+ ⭐
- **What it does:** Metrics collection and alerting with a dimensional data model and PromQL query language.
- **Revenue OS mapping:** Metrics Layer — agent performance, CRM throughput.
- **Integration effort:** Use as-is
- **Tech stack:** Go, TSDB
- **Notes:**
  - Scrape metrics from: agent RPS, queue depth, CRM API latency, enrichment success rate.
  - Record rules for SLA metrics (e.g., `sdr_outbound_rate`, `lead_to_meeting_time`).
  - Alert rules for anomalies (zero enrichment for 1h, CRM API 5xx spike).

### 9.3 Grafana
- **URL:** https://github.com/grafana/grafana
- **Stars:** ~66k+ ⭐
- **What it does:** Observability dashboard platform — metrics, logs, traces, alerts in unified panels.
- **Revenue OS mapping:** Observability Dashboards — agent health, pipeline metrics.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, Go
- **Notes:**
  - Dashboards: Agent Fleet Health, Pipeline Throughput, CRM Sync Lag, Enrichment Quality.
  - Alerting: via Slack webhook to #ops-revenue-os channel.
  - Annotations for agent deployments.

### 9.4 Jaeger
- **URL:** https://github.com/jaegertracing/jaeger
- **Stars:** ~21k+ ⭐
- **What it does:** Distributed tracing system — monitor and troubleshoot agent call chains.
- **Revenue OS mapping:** Tracing Layer — agent call chain visualization.
- **Integration effort:** Minor adapt
- **Tech stack:** Go, Cassandra/Elasticsearch/Badger
- **Notes:**
  - Each agent function is a span. Full trace: `LeadEnrich → VerifyEnail → CRMUpdate → SDRNotify`.
  - Identify bottlenecks: which agent step is slowest?
  - Bloom filter for head-based sampling (sample 1 in 10 traces at high volume).

### 9.5 Grafana Tempo
- **URL:** https://github.com/grafana/tempo
- **Stars:** ~4k+ ⭐
- **What it does:** Scalable distributed tracing backend — S3-compatible storage, cheap, works with OTel.
- **Revenue OS mapping:** Tracing Layer — cheaper alternative to Jaeger at scale.
- **Integration effort:** Minor adapt
- **Tech stack:** Go, S3/GCS
- **Notes:**
  - Object storage for traces → much cheaper than Jaeger's Cassandra.
  - Use when running 500k+ traces/day.

### 9.6 Grafana Loki
- **URL:** https://github.com/grafana/loki
- **Stars:** ~24k+ ⭐
- **What it does:** Log aggregation system — cheap, scalable, indexes metadata not content.
- **Revenue OS mapping:** Logging Layer — all agent logs.
- **Integration effort:** Use as-is
- **Tech stack:** Go, S3/GCS
- **Notes:**
  - Agent logs shipped via OTel → Promtail → Loki.
  - LogQL for querying: `{agent="sdr-1"} |= "error"`.
  - Retention: 30d hot storage, 1y cold.

---

## 10. Security & Compliance (Install Now)

### 10.1 Vaultwarden
- **URL:** https://github.com/dani-garcia/vaultwarden
- **Stars:** ~40k+ ⭐
- **What it does:** Lightweight Bitwarden-compatible server — password and secrets management.
- **Revenue OS mapping:** Secrets Vault — agent API keys, CRM credentials, email passwords.
- **Integration effort:** Use as-is
- **Tech stack:** Rust, Rocket, SQLite/MySQL/PostgreSQL
- **Notes:**
  - Docker deploy, 30MB image.
  - Bitwarden clients (CLI, browser) connect to it.
  - Agent pattern: `bw get password CRM_API_KEY` at startup.
  - Organization collections per agent type (SDR_API_KEYS, AE_API_KEYS).

### 10.2 Trivy
- **URL:** https://github.com/aquasecurity/trivy
- **Stars:** ~24k+ ⭐
- **What it does:** Comprehensive security scanner — containers, filesystems, Git repos, SBOM.
- **Revenue OS mapping:** CI/CD Security Gate — agent image scanning.
- **Integration effort:** Use as-is
- **Tech stack:** Go
- **Notes:**
  - `trivy image my-agent:latest` → scan for CVEs before deployment.
  - `trivy repo https://github.com/...` → scan agent dependencies.
  - Integrate into GitHub Actions as pre-deploy gate.

### 10.3 OpenSCAP
- **URL:** https://github.com/OpenSCAP/openscap
- **Stars:** ~1.5k+ ⭐
- **What it does:** Security compliance framework — SCAP content, vulnerability scanning, hardening guides.
- **Revenue OS mapping:** Compliance Agent — SOC2, ISO 27001 evidence collection.
- **Integration effort:** Major rework
- **Tech stack:** C, Python, XCCDF
- **Notes:**
  - Use `oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis` for CIS benchmarks.
  - Agent wraps to produce compliance evidence reports.
  - Heavy tool — only run on schedule, not per-agent.

### 10.4 Vanta API (integration)
- **URL:** https://vanta.com
- **Stars:** N/A (commercial)
- **What it does:** Automated SOC 2 / ISO 27001 compliance evidence collection (SaaS).
- **Revenue OS mapping:** Compliance Agent — evidence API.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, GraphQL
- **Notes:**
  - Automate test evidence upload via API.
  - Agent runs compliance tests → pushes results to Vanta.
  - Evidence categories: access control, encryption, backup, monitoring.

### 10.5 SecurityScorecard API (integration)
- **URL:** https://securityscorecard.com
- **Stars:** N/A (commercial)
- **What it does:** Security ratings and third-party risk monitoring (SaaS).
- **Revenue OS mapping:** Risk Assessment Agent — vendor/prospect security scoring.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API
- **Notes:**
  - Agent queries prospect security rating as qualification step.
  - "Reject lead if security rating < B" rule.

---

## 11. Communication & Notifications

### 11.1 SendGrid (API integration)
- **URL:** https://sendgrid.com (Twilio SendGrid)
- **Stars:** N/A (commercial API)
- **What it does:** Email delivery service — transactional, marketing, with templates and analytics.
- **Revenue OS mapping:** Email Agent — outbound/inbound email pipeline.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, SMTP
- **Notes:**
  - Agent sends via `POST /v3/mail/send` with template ID.
  - Inbound Parse webhook for reply handling.
  - Track: opens, clicks, bounces, spam reports.
  - Agent reads inbound → classifies (meeting request, question, unsubscribe) → routes.

### 11.2 Resend
- **URL:** https://github.com/resend/resend-node
- **Stars:** ~7k+ ⭐
- **What it does:** Modern email API for developers — high deliverability, React email templates, webhooks.
- **Revenue OS mapping:** Email Agent — transactional email.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, REST API
- **Notes:**
  - Simpler API than SendGrid.
  - `react-email` for building email templates in React.
  - Webhooks: `email.delivered`, `email.bounced`, `email.complained`.
  - Cheaper than SendGrid at volume.

### 11.3 Twilio (API integration)
- **URL:** https://twilio.com
- **Stars:** N/A (commercial API)
- **What it does:** Cloud communications platform — SMS, voice, WhatsApp, email, verify.
- **Revenue OS mapping:** Multi-Channel Communication Agent — SMS, voice outreach.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, TwiML
- **Notes:**
  - `POST /2010-04-01/Accounts/{sid}/Messages.json` for SMS.
  - Twilio Studio for visual IVR/call flows.
  - Agent-initiated calls via Twilio + TTS.
  - Verify API for lead contact verification.

### 11.4 Slack API (integration)
- **URL:** https://api.slack.com
- **Stars:** N/A (commercial)
- **What it does:** Team messaging platform with granular API — events, webhooks, bots, workflows.
- **Revenue OS mapping:** Notification Agent — internal alerts, handoffs, approvals.
- **Integration effort:** Minor adapt (API)
- **Tech stack:** REST API, WebSocket (RTM), Events API
- **Notes:**
  - Agent posts to Slack channels: `#sdr-wins`, `#ae-handoffs`, `#approval-requests`.
  - `chat.postMessage` with blocks for rich formatting.
  - Interactive buttons for approval workflows.
  - Events API: listen for mentions, channel messages.

### 11.5 WhatsApp Business API (integration)
- **URL:** https://developers.facebook.com/docs/whatsapp
- **Stars:** N/A (commercial)
- **What it does:** Official WhatsApp Business API — messaging, templates, interactive messages.
- **Revenue OS mapping:** Multi-Channel Communication Agent — WhatsApp outreach.
- **Integration effort:** Major rework
- **Tech stack:** REST API, GraphQL (Meta)
- **Notes:**
  - Business verification required (can take weeks).
  - Template messages for proactive outreach (24h+ window).
  - Session messages for active conversations (24h window).
  - Meta's GraphQL API — only send message templates initially.

### 11.6 QStash
- **URL:** https://github.com/upstash/qstash
- **Stars:** ~1k+ ⭐
- **What it does:** HTTP-based message queue and scheduler — durable, exactly-once delivery, rate limiting.
- **Revenue OS mapping:** Agent Task Queue — agent-to-agent job dispatch.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, REST API
- **Notes:**
  - `POST /v1/publish/{url}` with body → delivers to URL with retry.
  - Schedule: `POST /v1/schedule` for recurring agent runs.
  - Rate limiting per API key.
  - Useful for: "enrich this lead in 2 hours", "daily SDR task at 8 AM".

---

## 12. Analytics & Forecasting

### 12.1 Metabase
- **URL:** https://github.com/metabase/metabase
- **Stars:** ~40k+ ⭐
- **What it does:** Business intelligence platform — SQL queries, dashboards, embedded analytics, without engineering dependencies.
- **Revenue OS mapping:** Analytics Agent — revenue dashboards, pipeline reporting.
- **Integration effort:** Use as-is
- **Tech stack:** Java, Clojure, React
- **Notes:**
  - Connect to Supabase/PostgreSQL (Revenue OS OLTP).
  - X-ray feature auto-discovers relevant charts.
  - Embed dashboards in internal Revenue OS admin UI.
  - Alerting: "pipeline value dropped > 20% week-over-week".
  - Agent queries Metabase API for report generation.

### 12.2 Apache Superset
- **URL:** https://github.com/apache/superset
- **Stars:** ~64k+ ⭐
- **What it does:** Enterprise-level BI platform — rich visualizations, SQL Lab, dashboard composition, RBAC.
- **Revenue OS mapping:** Analytics Agent — advanced revenue analytics (vs Metabase for simpler needs).
- **Integration effort:** Major rework
- **Tech stack:** Python, React, SQLAlchemy
- **Notes:**
  - More powerful than Metabase but heavier to deploy.
  - SQL Lab for ad-hoc agent queries.
  - Virtual datasets for pre-joined CRM + email + call data.
  - Use if Metabase hits SQL complexity limits.

### 12.3 dbt (data build tool)
- **URL:** https://github.com/dbt-labs/dbt-core
- **Stars:** ~10k+ ⭐
- **What it does:** Data transformation framework — SQL-based ELT, testing, documentation, lineage.
- **Revenue OS mapping:** Analytics Pipeline — transform CRM + ops data into revenue models.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, SQL (Snowflake, Postgres, BigQuery, DuckDB)
- **Notes:**
  - Models:
    - `stg_crm_opportunities.sql` (clean and type)
    - `fct_pipeline_by_stage.sql` (aggregate)
    - `rpt_forecast.sql` (ML forecast input)
  - Tests: `not_null`, `unique`, `accepted_values` on critical fields.
  - Documentation: auto-generated lineage DAG for Revenue OS data flow.
  - Use DuckDB adapter for local dev, Postgres for prod.

### 12.4 PostHog
- **URL:** https://github.com/PostHog/posthog
- **Stars:** ~23k+ ⭐
- **What it does:** Product analytics platform — events, feature flags, session replay, funnel analysis.
- **Revenue OS mapping:** Product/Usage Analytics — track agent adoption, user behavior.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, TypeScript, ClickHouse, Kafka
- **Notes:**
  - Self-host on Docker.
  - Track agent actions as PostHog events: `agent_enrichment_completed`, `email_opened`.
  - Funnels: "Lead Created → Contacted → Meeting Booked → Deal Won".
  - Feature flags: roll out new agent behaviors gradually.
  - Session recording on user-facing Revenue OS UI.

---

## 13. Additional Tools (Not Yet Installed — Future Consideration)

### 13.1 n8n
- **URL:** https://github.com/n8n-io/n8n
- **Stars:** ~50k+ ⭐
- **What it does:** Fair-code workflow automation with 400+ integrations, visual builder, and code nodes.
- **Revenue OS mapping:** Workflow Orchestrator (fallback) — human-friendly workflow builder.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, Node.js, Vue.js
- **Notes:**
  - Use for manual workflow creation by RevOps team.
  - Agents can trigger n8n webhooks for human-in-the-loop steps.
  - NOT a replacement for agent orchestration — complementary.

### 13.2 Dify
- **URL:** https://github.com/langgenius/dify
- **Stars:** ~55k+ ⭐
- **What it does:** LLM application platform with visual workflow builder, RAG pipeline, agent mode, model management.
- **Revenue OS mapping:** Agent Builder (visual) — non-technical team members build simple agents.
- **Integration effort:** Minor adapt
- **Tech stack:** Python, TypeScript, PostgreSQL, Redis
- **Notes:**
  - Visual prompt engineering and RAG.
   - Agents built here are simpler than CrewAI[^1]/LangGraph.
  - Good for: "lead scoring agent" defined by RevOps manager.

### 13.3 Plane
- **URL:** https://github.com/makeplane/plane
- **Stars:** ~32k+ ⭐
- **What it does:** Open-source project management (Jira/Linear alternative) with issue tracking, cycles, modules.
- **Revenue OS mapping:** Project Management — track Revenue OS build sprints.
- **Integration effort:** Use as-is
- **Tech stack:** TypeScript, React, PostgreSQL
- **Notes:**
  - Track agent development tasks.
  - API for agents to create/update issues.

### 13.4 Documenso
- **URL:** https://github.com/documenso/documenso
- **Stars:** ~8k+ ⭐
- **What it does:** Open-source DocuSign alternative — e-signatures, document templates, API-first.
- **Revenue OS mapping:** Contract Agent — send, sign, manage contracts automatically.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, React, PostgreSQL
- **Notes:**
  - Self-host signing workflows.
  - API: create signing link, webhook on signed.
  - Template merge for proposal → contract conversion.

### 13.5 Cal.com
- **URL:** https://github.com/calcom/cal.com
- **Stars:** ~33k+ ⭐
- **What it does:** Open-source scheduling platform (Calendly alternative) with API, workflows, and routing forms.
- **Revenue OS mapping:** Scheduling Agent — automated meeting booking.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, React, Prisma, PostgreSQL
- **Notes:**
  - Agent books meetings via API: `POST /bookings`.
  - Routing forms for lead qualification → right AE.
  - Webhook `booking.created` → agent prepares briefing.

### 13.6 Huly
- **URL:** https://github.com/hcengineering/huly-platform
- **Stars:** ~18k+ ⭐
- **What it does:** All-in-one project management platform (Linear/Jira/Notion alternative) with docs, chat, HR.
- **Revenue OS mapping:** Project Management — alternative to Plane, broader scope.
- **Integration effort:** Major rework
- **Tech stack:** TypeScript, Svelte, MongoDB
- **Notes:**
  - Includes CRM-adjacent features (contacts, companies).
  - May conflict with Twenty; use for ops, not sales.

### 13.7 Formbricks
- **URL:** https://github.com/formbricks/formbricks
- **Stars:** ~7k+ ⭐
- **What it does:** Open-source survey and feedback platform — in-app surveys, link surveys, email surveys.
- **Revenue OS mapping:** Voice of Customer Agent — NPS, CSAT, lead qualification forms.
- **Integration effort:** Minor adapt
- **Tech stack:** TypeScript, React, PostgreSQL
- **Notes:**
  - Embed in outreach emails.
  - Agent triggers NPS survey after deal closed.

---

## 14. Integration Patterns & Architecture Notes

### 14.1 Core Data Flow
```
Prospect Sources (Agent-Reach, theHarvester, Hunter, Apollo, Bright Data)
    │
    ▼
Enrichment Layer (Clay, Firecrawl, crawl4ai, LLM extraction)
    │
    ▼
CRM (Twenty Core / Supabase / Neo4j graph)
    │
    ▼
Engagement Layer (OpenSales sequences, Email via Resend, SMS via Twilio)
    │
    ▼
Conversation Intelligence (call.md, Whisper, Memoir)
    │
    ▼
Analytics Layer (dbt → Metabase / Superset, PostHog)
    │
    ▼
Observability (OTel → Prometheus + Tempo + Loki → Grafana)
```

### 14.2 Agent Communication Patterns

| Pattern | Tool | Use Case |
|---------|------|----------|
| Direct HTTP | QStash | Scheduled task dispatch |
| Message Queue | NATS JetStream | Async agent-to-agent handoff |
| Pub/Sub | NATS JetStream | Event broadcast (new lead, deal won) |
| Webhook | Twenty → Agent | Record change trigger |
| Shared Vector Store | Qdrant | Cross-agent context retrieval |
| Shared Graph | Neo4j | Entity relationship resolution |
| MCP | All | Agent-to-tool standardized calls |

### 14.3 Auth Flow
```
Agent → JWT (Supabase Auth / Vaultwarden-managed)
    → Passes in Authorization header
    → Each service validates via JWKS or shared secret
    → RLS filters data per agent role (SDR vs AE vs Admin)
```

### 14.4 Deployment Model
```
Docker Swarm or Nomad (lighter than K8s for 80-120 agents)
    │
    ├── Agent pods (CrewAI[^1], LangGraph, custom Python/TS)
    ├── Data layer (PostgreSQL, Qdrant, Neo4j, Redis)
    ├── Queue (NATS, QStash)
    ├── Observability (OTel Collector, Prometheus, Grafana, Loki, Tempo)
    └── User-facing UI (Twenty, Metabase, custom dashboard)
```

### 14.5 Cost Baseline (monthly self-host)

| Resource | Cost | Notes |
|----------|------|-------|
| LLM API (GPT-4 / Claude) | ~$2,000–5,000 | 80-120 agents, ~100 calls/day each |
| VPS / Cloud VMs | ~$300–800 | 4-8 nodes |
| Object Storage (S3) | ~$100 | Recordings, documents |
| Vector DB (Qdrant) | ~$50 | 4GB RAM node |
| Enrichment APIs | ~$500–2,000 | Hunter, BrightData, Clay |
| Email (Resend) | ~$100 | 50k emails/mo |
| **Total** | **~$3,000–8,000/mo** | vs $50k+ for equivalent SaaS |

---

## 15. Tool Comparison: Build vs Buy Decision Matrix

| Need | Build | Open Source | Buy (SaaS) | Decision |
|------|-------|-------------|------------|----------|
| CRM | — | Twenty | Salesforce ($150/seat) | **Twenty** — native API |
| Agent orchestration | CrewAI[^1] | — | — | **CrewAI[^1]** — fast to deploy |
| Vector search | — | Qdrant | Pinecone ($0.01/hr) | **Qdrant** — cheaper at scale |
| Call intelligence | — | call.md | Gong ($10k/yr) | **call.md** — 90% of Gong value |
| Email sending | — | — | Resend ($20/mo) | **Resend** — reliability matters |
| BI dashboards | — | Metabase | Tableau ($75/seat) | **Metabase** — good enough |
| Compliance | — | OpenSCAP | Vanta ($5k/yr) | **Both** — Vanta for evidence, OpenSCAP for depth |
| Knowledge graph | — | Neo4j | — | **Neo4j** — unique capability |
| Data collection | — | Agent-Reach | — | **Agent-Reach** — already built |
| Enrichment waterfall | — | — | Clay ($100/mo) | **Clay** — best-in-class, cheap |

---

## Appendix: Quick Install Commands

### Docker Compose Bootstrap
```yaml
# docker-compose.yml for Revenue OS Core
version: '3.8'
services:
  # Data
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: revenue_os
      POSTGRES_PASSWORD: ${DB_PASSWORD}
  qdrant:
    image: qdrant/qdrant
    ports: ["6333:6333"]
  nats:
    image: nats:latest
    command: ["-js"]
    ports: ["4222:4222"]

  # Agent orchestration[^1]
  crew-ai:
    build: ./agents
    environment:
      NATS_URL: nats://nats:4222
      QDRANT_URL: http://qdrant:6333
      DB_URL: postgresql://postgres:${DB_PASSWORD}@postgres/revenue_os

  # Monitoring
  otel-collector:
    image: otel/opentelemetry-collector:latest
    volumes: ["./otel-config.yaml:/etc/otel/config.yaml"]
  prometheus:
    image: prom/prometheus
  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
```

### Quick Deploy Checklist
- [ ] Twenty CRM: `docker compose -f twenty-compose.yml up -d`
- [ ] Supabase: `npx supabase start`
- [ ] Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`
- [ ] NATS: `docker run -d -p 4222:4222 nats -js`
- [ ] call.md: `docker compose -f callmd-compose.yml up -d`
- [ ] Metabase: `docker run -d -p 3000:3000 metabase/metabase`
- [ ] PostHog: `docker compose -f posthog-compose.yml up -d`
- [ ] OTel + Prometheus + Grafana: `docker compose -f observability.yml up -d`
- [ ] Resend: configure domain + API key (no self-host)
- [ ] Vaultwarden: `docker run -d -p 8080:80 vaultwarden/server`

---

[^1]: **NOT used in Revenue OS.** NATS JetStream replaces all CrewAI orchestration. CrewAI's sequential/hierarchical crew model conflicts with the event-driven architecture. Keep for reference/design patterns only.

> **Last updated:** 2026-06-24
> **Maintainer:** Revenue OS Engineering Team
> **Next review:** When a tool in this catalog releases a major version or a superior alternative emerges.
>
> *This catalog is a living document. Every tool listed has been evaluated against real sales agent workflows. Prioritize installation by the Priority column — Critical first, then High, then Medium/Low as capacity allows.*
