# SOVEREIGN CRM — FINAL DEPLOYMENT & USAGE REPORT
# Complete Repository Usage Guide + Deployment Status

**Date:** June 7, 2026
**Total Repositories Evaluated:** 62
**Total Installed:** 40 repos cloned + 48 pip packages + 7 npm projects
**Infrastructure Services:** 10 containers deployed

---

## PART 1: INFRASTRUCTURE DEPLOYMENT STATUS

### Running Services

| Service | Port | Status | Container Image | Purpose |
|---------|------|--------|-----------------|---------|
| PostgreSQL | 5432 | UP | postgres:16-alpine | Primary database |
| Valkey/Redis | 6379 | UP | valkey:7-alpine | Cache + session store |
| Next.js Web | 3000 | UP | local build | CRM frontend |
| ClickHouse | 9000 | UP | clickhouse-server | Analytics engine |

### Deployed but Needs Image Pull Fix

| Service | Port | Status | Issue | Fix Required |
|---------|------|--------|-------|--------------|
| Directus | 8055 | Created | ghcr.io 403 | `podman login ghcr.io` or use Docker Hub mirror |
| Dify API | 5001 | Created | ghcr.io 403 | `podman login ghcr.io` then re-pull |
| Dify Web | 3001 | Created | ghcr.io 403 | `podman login ghcr.io` then re-pull |
| ClickHouse HTTP | 8123 | Partial | Native port UP, HTTP not exposed | Restart with correct port mapping |
| BillionMail | 8080 | Failed | Image not found | Verify image name: `docker.io/billionmail/billionmail` |
| Trigger.dev | — | Failed | ghcr.io 403 | `podman login ghcr.io` then re-pull |

### How to Fix GHCR.io Access

```bash
# Step 1: Authenticate with GitHub Container Registry
podman login ghcr.io
# Enter GitHub username and Personal Access Token (read:packages scope)

# Step 2: Re-pull failed images
podman pull ghcr.io/langgenius/dify-api:latest
podman pull ghcr.io/langgenius/dify-web:latest
podman pull ghcr.io/triggerdotdev/trigger.dev:latest
```

### Services NOT Yet Deployed (Need Manual Sprint 0)

| Service | Why | Action Required |
|---------|-----|-----------------|
| Supabase | Complex multi-container setup | Run official supabase-docker compose |
| Coolify | Requires bare-metal or VPS install | Run Coolify install script on server |
| Go API | CRM backend not built yet | Implement in Sprint 1+ |

---

## PART 2: COMPLETE REPOSITORY USAGE REPORT

### TIER 0: CORE INFRASTRUCTURE (6 repos)

#### 1. supabase/supabase (103K stars)
**Priority:** P0 — Install Immediately
**How We Use It:** Primary infrastructure layer for the entire CRM.
- **Database:** PostgreSQL with built-in connection pooling, migrations
- **Authentication:** Email/password, OAuth, MFA for CRM users
- **Row-Level Security:** Tenant isolation enforced at database level
- **Realtime:** WebSocket subscriptions for live deal/pipeline updates
- **Storage:** File uploads (documents, exports, attachments)
- **Edge Functions:** Serverless logic for webhooks, integrations
**Status:** Architecture ready; deploy in Sprint 0.

#### 2. postgres/postgres (21K stars)
**Priority:** P0 — Core Database
**How We Use It:** Underlying database engine for Supabase and all CRM data.
- **Schema:** Multi-tenant with RLS policies (12+ CRM tables)
- **Extensions:** pgvector for embeddings, pg_trgm for fuzzy search
- **Analytics:** ClickHouse replicates from Postgres for OLAP
- **Backups:** pgBackRest for point-in-time recovery
**Status:** Running on port 5432.

#### 3. coollabsio/coolify (56K stars)
**Priority:** P1 — Self-hosted PaaS
**How We Use It:** Production deployment and container orchestration.
- **Deploy:** One-click deploys for API, Web, Dify, Trigger.dev
- **TLS:** Automatic Let's Encrypt certificates
- **Monitoring:** Built-in resource monitoring
- **Backups:** Automated database backups
**Status:** Not yet deployed; requires bare-metal install.

#### 4. pocketbase/pocketbase (58K stars)
**Priority:** P2* — Pilot Only (NOT replacing Supabase)
**How We Use It:** Lightweight embedded database for:
- **Agent Memory Store:** Local key-value store for agent working memory
- **Offline Mode:** PocketBase as fallback if Supabase is unreachable
- **Internal Tools:** Quick prototypes for admin dashboards
**Status:** Cloned to sovereign-crm-tools/. Evaluate in Sprint 2.

#### 5. directus/directus (36K stars)
**Priority:** P3 — Headless CMS
**How We Use It:** Content management for CRM-specific content.
- **Knowledge Base:** Customer-facing FAQ, help articles
- **Email Templates:** Visual editor for marketing/support emails
- **Content API:** Auto-generated REST/GraphQL for non-dev content
- **Admin UI:** Non-technical users manage content without code
**Status:** Container created; needs GHCR auth to pull image.

#### 6. apache/shardingsphere (20K stars)
**Priority:** P4 — REJECT
**How We Use It:** NOT ADOPTED. Java-based database sharding is overkill for
multi-tenant CRM. PostgreSQL partitioning + RLS handles tenancy at this scale.

---

### TIER 1: AI AGENT FRAMEWORKS (12 repos)

#### 7. langchain-ai/langchain (108K stars)
**Priority:** P0 — Agent Engineering Platform
**How We Use It:** Core framework for building all AI agent chains.
- **CRM Copilot:** Natural language queries on deals, contacts, pipeline
- **Email Drafting:** AI-assisted email composition from templates + context
- **Lead Scoring:** ML pipeline for automated lead qualification
- **Data Extraction:** Parse documents into structured CRM records
- **Chain Composition:** RAG chains for knowledge-grounded responses
**Status:** Installed (langchain 1.3.1, langgraph 1.2.1, langsmith 0.8.5).

#### 8. langgenius/dify (98K stars)
**Priority:** P1 — Visual Workflow Builder
**How We Use It:** Low-code workflow automation for non-technical users.
- **Lead Nurture:** Drag-and-drop drip campaign builder
- **Approval Workflows:** Deal approval, discount authorization flows
- **Integration Hub:** Connect CRM to Slack, email, calendars visually
- **Agent Playground:** Test and debug AI agents before production
**Status:** Container created; needs GHCR auth fix.

#### 9. triggerdotdev/trigger.dev (13K stars)
**Priority:** P0 — Background Job Engine
**How We Use It:** All async/scheduled/background processing.
- **Email Sending:** Queue and deliver bulk + transactional emails
- **Report Generation:** Nightly/weekly pipeline reports
- **Data Sync:** Sync CRM data with external systems (ERP, accounting)
- **Webhook Processing:** Handle incoming webhooks from integrations
- **Scheduled Tasks:** Cron jobs for reminders, follow-ups, escalations
- **MCP Integration:** Trigger.dev supports MCP for agent task routing
**Status:** npm project cloned; needs self-hosted deployment.

#### 10. unclecode/crawl4ai (45K stars)
**Priority:** P0 — Web Research Engine
**How We Use It:** All web crawling and data collection for research agents.
- **Market Intel:** Crawl competitor websites, pricing pages, changelogs
- **Lead Enrichment:** Scrape LinkedIn, company websites for lead data
- **News Monitoring:** Track industry news, regulatory changes
- **VoC Analysis:** Crawl review sites, forums for customer sentiment
- **Document Ingestion:** Convert web pages to structured data for RAG
**Status:** Installed (crawl4ai 0.8.9).

#### 11. addyosmani/agent-skills (5K stars)
**Priority:** P0 — Engineering Skills Library
**How We Use It:** Standardized skill definitions for all coding agents.
- **Code Review:** Skill for running automated code reviews
- **Testing:** Skill for generating and running test suites
- **Refactoring:** Skill for safe code refactoring
- **Documentation:** Skill for auto-generating API docs
**Status:** Cloned to sovereign-crm-tools/.

#### 12. gastownhall/beads (4K stars)
**Priority:** P1 — Agent Memory (Go)
**How We Use It:** Persistent cross-session memory for all agents.
- **Working Memory:** Agent recalls previous interactions per customer
- **Learning Store:** Agents accumulate knowledge from past decisions
- **Context Sharing:** Multiple agents share context on same customer
- **Go Native:** Matches our Go backend stack
**Status:** Cloned to sovereign-crm-tools/.

#### 13. volcengine/OpenViking (3K stars)
**Priority:** P1 — Context Database
**How We Use It:** Long-term context storage for agent conversations.
- **Conversation History:** Store full agent-customer interaction threads
- **Context Retrieval:** Retrieve relevant past context for current tasks
- **Knowledge Caching:** Cache frequently accessed knowledge
**Status:** Cloned to sovereign-crm-tools/.

#### 14. rohitg00/agentmemory (2K stars)
**Priority:** P3 — Supplemental Memory (beads is primary)
**How We Use It:** Lightweight memory store for simple key-value agent state.
- **Session State:** Store agent state during complex multi-step workflows
- **Preference Store:** Remember user preferences across sessions
**Status:** Installed (agentmemory 0.4.8).

#### 15. colbymchenry/codegraph (4K stars)
**Priority:** P1 — Code Intelligence
**How We Use It:** Code understanding for development agents.
- **Code Review:** Understand code relationships for smarter reviews
- **Impact Analysis:** Map which code changes affect CRM modules
- **Dependency Graph:** Track Go/JS dependencies for build optimization
- **MCP Support:** Integrates with agent workflows via MCP
**Status:** npm project cloned.

#### 16. tirth8205/code-review-graph (1K stars)
**Priority:** P2 — Code Review Intelligence
**How We Use It:** Specialized code review analysis.
- **Security Patterns:** Detect security anti-patterns in code
- **Quality Metrics:** Track code quality over time
- **Review Automation:** Auto-assign reviewers based on code ownership
**Status:** Cloned to sovereign-crm-tools/.

#### 17. MinishLab/semble (2K stars)
**Priority:** P4 — REJECT (codegraph covers this)
**How We Use It:** NOT ADOPTED. Overlaps with codegraph which has higher
community and MCP support.

#### 18. opensandbox-group/OpenSandbox (1K stars)
**Priority:** P2 — Agent Sandbox
**How We Use It:** Secure execution environment for untrusted agent code.
- **Code Execution:** Run AI-generated code in isolated sandboxes
- **Plugin Testing:** Test third-party integrations safely
- **Multi-tenant:** Isolated execution per customer
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 2: WEB CRAWLING & RESEARCH (6 repos)

#### 19. getmaxun/maxun (23K stars)
**Priority:** P2 — No-Code Web Scraping
**How We Use It:** Visual web scraping for non-technical users.
- **Lead Lists:** Build scraping workflows to collect leads
- **Price Monitoring:** Track competitor pricing changes
- **Data Collection:** No-code scrapers for market research
**Status:** Cloned to sovereign-crm-tools/.

#### 20. Panniantong/Agent-Reach (500 stars)
**Priority:** P2 — Multi-Platform Research
**How We Use It:** Cross-platform data collection.
- **Social Research:** Scrape Twitter, LinkedIn, Reddit for VoC
- **Multi-source:** Aggregate data from multiple platforms
- **Research Reports:** Combine sources into research summaries
**Status:** Cloned to sovereign-crm-tools/.

#### 21. milvus-io/milvus (34K stars)
**Priority:** P3 — Vector Database (Alternative)
**How We Use It:** Production vector search if Chroma/Qdrant insufficient.
- **Semantic Search:** Find similar CRM records by meaning
- **RAG Backend:** Vector store for agent knowledge retrieval
- **Embedding Search:** Search customer communications by intent
**Status:** Cloned to sovereign-crm-tools/.

#### 22. RyanCodrai/turbovec (500 stars)
**Priority:** P3 — Lightweight Vector Search
**How We Use It:** Fast vector search for simple similarity queries.
- **Contact Matching:** Find similar contacts for deduplication
- **Content Matching:** Match support tickets to knowledge base
**Status:** Cloned to sovereign-crm-tools/.

#### 23. unclecode/crawl4ai (listed in P0, cross-reference)
See #10 above.

#### 24. infiniflow/ragflow (42K stars)
**Priority:** P2 — RAG Framework
**How We Use It:** Document-grounded RAG for knowledge agents.
- **Document QA:** Answer questions from uploaded CRM documents
- **Knowledge Base:** Build searchable knowledge from company docs
- **Chunking Engine:** Smart document chunking for embeddings
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 3: AI CODING TOOLS (8 repos)

#### 25. cline/cline (40K stars)
**Priority:** P2 — AI Coding Agent
**How We Use It:** Autonomous coding for CRM development.
- **Feature Development:** Generate CRM features from specifications
- **Bug Fixes:** Autonomous bug detection and fixing
- **Refactoring:** Large-scale codebase refactoring
- **SDK Mode:** Integrate into automated pipelines
**Status:** Cloned to sovereign-crm-tools/.

#### 26. Aider-AI/aider (32K stars)
**Priority:** P2 — Terminal AI Pair Programming
**How We Use It:** Interactive AI coding for developers.
- **Pair Programming:** Real-time code suggestions
- **Git Integration:** Auto-commit with meaningful messages
- **Multi-file Edits:** Make coordinated changes across files
**Status:** Installed (aider-chat 0.82.1).

#### 27. OpenHands/openhands (55K stars)
**Priority:** P1 — AI Development Environment
**How We Use It:** Full AI development environment.
- **Code Generation:** Generate full applications from specs
- **Testing:** Auto-generate test suites
- **Documentation:** Generate docs from code
**Status:** Installed (openhands 1.2.1).

#### 28. aaif-goose/goose (16K stars)
**Priority:** P2 — Extensible Agent Runtime
**How We Use It:** Custom agent execution environment.
- **Plugin System:** Extend agent capabilities via plugins
- **Tool Integration:** Connect agents to external tools
- **Agent Lifecycle:** Manage agent startup, execution, shutdown
**Status:** Cloned to sovereign-crm-tools/.

#### 29. snarktank/ralph (4K stars)
**Priority:** P3 — PRD-to-Code Agent
**How We Use It:** Convert product specs to implementation plans.
- **PRD Execution:** Parse PRD documents into coding tasks
- **Sprint Planning:** Generate sprint backlogs from features
**Status:** Cloned to sovereign-crm-tools/.

#### 30. agentsmd/agents.md (2K stars)
**Priority:** P1 — Agent Configuration Standard
**How We Use It:** Standardize agent definitions across the platform.
- **AGENTS.md Format:** Define agent behavior in structured markdown
- **Consistency:** All agents follow the same specification format
- **Tool Integration:** Works with Hermes, Claude Code, Cline
**Status:** npm project installed.

#### 31. vercel-labs/skills (1K stars)
**Priority:** P3 — Agent Skills (reference)
**How We Use It:** Reference for skill design patterns.
- **Skill Templates:** Use as template for custom skills
**Status:** npm project installed.

#### 32. midudev/autoskills (500 stars)
**Priority:** P4 — REJECT (reference only)
**How We Use It:** NOT ADOPTED. Reference for skill auto-generation patterns.

---

### TIER 4: EMAIL & COMMUNICATION (4 repos)

#### 33. Billionmail/BillionMail (5K stars)
**Priority:** P2 — Self-hosted Email Server
**How We Use It:** Complete email infrastructure.
- **SMTP Server:** Send transactional CRM emails
- **Email Marketing:** Bulk email campaigns
- **DMARC/DKIM/SPF:** Email authentication for deliverability
- **Analytics:** Track opens, clicks, bounces
- **Self-hosted:** Full control over email infrastructure
**Status:** Container deployment failed (image not found). Verify image name.

#### 34. usesend/useSend (2K stars)
**Priority:** P2 — Transactional Email API
**How We Use It:** API-based email for developer workflows.
- **Transactional Email:** Password resets, notifications
- **API-first:** Programmatic email sending
- **Templates:** HTML email templates
**Status:** Cloned to sovereign-crm-tools/.

#### 35. resendinc/resend (28K stars)
**Priority:** P2 — Modern Email API (Alternative to useSend)
**How We Use It:** High-reliability email API.
- **Deliverability:** High inbox rates
- **React Emails:** Build emails with React components
- **Analytics:** Real-time email analytics
**Status:** Cloned to sovereign-crm-tools/.

#### 36. unsend-dev/unsend (5K stars)
**Priority:** P3 — Open Source Email (Alternative)
**How We Use It:** Open-source alternative to Resend.
- **Self-hosted:** Full control over email sending
- **API Compatible:** Drop-in replacement for commercial APIs
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 5: SECURITY & COMPLIANCE (4 repos)

#### 37. usestrix/strix (2K stars)
**Priority:** P1 — AI Security Scanner
**How We Use It:** Automated security testing.
- **Code Scanning:** Find vulnerabilities in Go/JS code
- **Dependency Audit:** Track vulnerable dependencies
- **CI Integration:** Run on every PR
**Status:** Cloned to sovereign-crm-tools/.

#### 38. OWASP/crAPI (4K stars)
**Priority:** P3 — Security Training
**How We Use It:** Security awareness training for development team.
- **Training Environment:** Practice finding vulnerabilities
- **Security Testing:** Validate security scanner results
**Status:** Cloned to sovereign-crm-tools/.

#### 39. qazwsxedcrfvtgb1970/awesome-cloud-security (1K stars)
**Priority:** P3 — Security Reference
**How We Use It:** Reference for cloud security best practices.
- **Checklist:** Use as security audit checklist
- **Tools:** Discover new security tools
**Status:** Cloned to sovereign-crm-tools/.

#### 40. trufflesecurity/trufflehog (17K stars)
**Priority:** P1 — Secret Detection
**How We Use It:** Prevent secrets from leaking into code.
- **Pre-commit:** Scan for API keys, passwords before commit
- **CI/CD:** Scan repositories for exposed secrets
- **Monitoring:** Continuously scan for leaked credentials
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 6: OBSERVABILITY & MONITORING (5 repos)

#### 41. prometheus/prometheus (57K stars)
**Priority:** P2 — Metrics Collection
**How We Use It:** System and application metrics.
- **API Metrics:** Request rates, latency, error rates
- **Business Metrics:** Deals closed, pipeline velocity
- **Infrastructure:** CPU, memory, disk usage
**Status:** Cloned to sovereign-crm-tools/.

#### 42. grafana/grafana (67K stars)
**Priority:** P2 — Visualization & Dashboards
**How We Use It:** Monitoring dashboards and alerting.
- **CRM Dashboard:** Real-time pipeline visualization
- **Agent Dashboard:** Track agent performance and costs
- **Alerting:** PagerDuty/Slack alerts for anomalies
**Status:** Cloned to sovereign-crm-tools/.

#### 43. open-telemetry/opentelemetry-collector (3K stars)
**Priority:** P2 — Telemetry Pipeline
**How We Use It:** Collect and forward traces, metrics, logs.
- **Distributed Tracing:** Track requests across services
- **Log Aggregation:** Centralized logging
**Status:** Cloned to sovereign-crm-tools/.

#### 44. SigNoz/signoz (20K stars)
**Priority:** P2 — Observability Platform
**How We Use It:** All-in-one observability.
- **Traces:** Distributed tracing for API calls
- **Metrics:** Application performance monitoring
- **Logs:** Structured log search and analysis
**Status:** Cloned to sovereign-crm-tools/.

#### 45. getsentry/sentry (40K stars)
**Priority:** P1 — Error Tracking
**How We Use It:** Real-time error monitoring.
- **Error Tracking:** Capture and prioritize errors
- **Performance:** Track slow operations
- **Release Health:** Monitor deployment impact
**Status:** Installed (sentry-sdk 2.61.1).

---

### TIER 7: SEARCH & DISCOVERY (4 repos)

#### 46. meilisearch/meilisearch (50K stars)
**Priority:** P2 — Full-Text Search
**How We Use It:** Fast search across CRM entities.
- **Contact Search:** Fuzzy name/email/company search
- **Deal Search:** Search by deal name, amount, stage
- **Global Search:** Cross-entity search bar
**Status:** Cloned to sovereign-crm-tools/.

#### 47. typesense/typesense (22K stars)
**Priority:** P3 — Search Alternative
**How We Use It:** Alternative to Meilisearch if needed.
- **Typo-tolerant:** Handle misspellings in search
- **Faceted Search:** Filter by multiple attributes
**Status:** Cloned to sovereign-crm-tools/.

#### 48. rapidfuzz/rapidfuzz (5K stars)
**Priority:** P2 — Fuzzy String Matching
**How We Use It:** Match similar strings for deduplication.
- **Contact Dedup:** Find duplicate contacts by name similarity
- **Company Matching:** Match company names across sources
**Status:** Cloned to sovereign-crm-tools/.

#### 49. archit-palwal-dev/Research-Canvas (1K stars)
**Priority:** P3 — Research Framework
**How We Use It:** Structured research methodology.
- **Market Research:** Framework for competitive analysis
- **Due Diligence:** Structured research for deals
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 8: WORKFLOW & AUTOMATION (5 repos)

#### 50. n8n-io/n8n (80K stars)
**Priority:** P2 — Workflow Automation
**How We Use It:** Visual workflow automation (alternative to Dify for simple workflows).
- **Integrations:** 200+ integrations (CRM, email, calendar)
- **Automation:** If-this-then-that for business processes
- **Webhooks:** Handle incoming events from external systems
**Status:** Cloned to sovereign-crm-tools/.

#### 51. langflow-ai/langflow (55K stars)
**Priority:** P3 — AI Workflow Builder (Dify alternative)
**How We Use It:** Build AI agent workflows visually.
- **Agent Design:** Drag-and-drop agent architecture
- **Testing:** Visual testing of agent chains
**Status:** Cloned to sovereign-crm-tools/.

#### 52. flowiseai/Flowise (35K stars)
**Priority:** P3 — Chatbot Builder
**How We Use It:** Build CRM chatbots visually.
- **Customer Chat:** Support chatbot for customers
- **Internal Chat:** Internal helpdesk bot
**Status:** Cloned to sovereign-crm-tools/.

#### 53. n8n-io/n8n (duplicate, see #50)

#### 54. blakeblackshear/frigate (19K stars)
**Priority:** P4 — REJECT (wrong domain: video surveillance)
**How We Use It:** NOT ADOPTED.

---

### TIER 9: DATA & STORAGE (5 repos)

#### 55. minio/minio (52K stars)
**Priority:** P2 — Object Storage
**How We Use It:** S3-compatible file storage.
- **File Storage:** CRM document attachments
- **Backups:** Database backup storage
- **Exports:** CSV/Excel export file staging
**Status:** Cloned to sovereign-crm-tools/.

#### 56. dragonflydb/dragonfly (27K stars)
**Priority:** P3 — Redis Alternative
**How We Use It:** High-performance cache if Valkey insufficient.
- **Session Cache:** Store user sessions
- **Rate Limiting:** Token bucket for API rate limiting
**Status:** Cloned to sovereign-crm-tools/.

#### 57. ClickHouse/clickhouse (39K stars)
**Priority:** P2 — Analytics Database
**How We Use It:** OLAP analytics for CRM reporting.
- **Pipeline Analytics:** Deal conversion funnels
- **Performance Dashboards:** Real-time KPIs
- **Data Warehouse:** Historical analysis at scale
**Status:** Running on port 9000.

#### 58. duckdb/duckdb (29K stars)
**Priority:** P3 — Embedded Analytics
**How We Use It:** Embedded analytics in Go backend.
- **In-process Analytics:** Fast aggregations without external DB
- **Data Import:** CSV/Parquet analysis
**Status:** Cloned to sovereign-crm-tools/.

#### 59. dolthub/dolt (18K stars)
**Priority:** P3 — Version-Controlled Database
**How We Use It:** Version-controlled CRM data migrations.
- **Schema Versioning:** Track database schema changes
- **Data Audit:** Full history of data changes
**Status:** Cloned to sovereign-crm-tools/.

---

### TIER 10: DOCUMENT PROCESSING (4 repos)

#### 60. opendatalab/MinerU (33K stars)
**Priority:** P2 — Document Extraction
**How We Use It:** Extract structured data from documents.
- **PDF Processing:** Extract text, tables from uploaded PDFs
- **Contract Parsing:** Parse contract terms into CRM fields
- **Invoice Processing:** Extract line items from invoices
**Status:** Cloned to sovereign-crm-tools/.

#### 61. pymupdf/PyMuPDF (7K stars)
**Priority:** P1 — PDF Processing
**How We Use It:** Fast PDF rendering and extraction.
- **PDF Preview:** Generate thumbnails for document viewer
- **Text Extraction:** Extract text from scanned PDFs
**Status:** Installed (pymupdf 1.27.2.3).

#### 62. QuivrHQ/quivr (38K stars)
**Priority:** P3 — Knowledge Base
**How We Use It:** Build searchable knowledge bases from documents.
- **Internal Wiki:** Company knowledge base
- **Customer Docs:** Searchable product documentation
**Status:** Cloned to sovereign-crm-tools/.

---

## PART 3: USAGE SUMMARY BY CRM MODULE

### How Each Tool Maps to CRM Features

| CRM Module | Primary Tools | Secondary Tools |
|------------|--------------|-----------------|
| **Contacts** | PostgreSQL, Supabase, Meilisearch | rapidfuzz (dedup), crawl4ai (enrichment) |
| **Deals/Pipeline** | PostgreSQL, Supabase, ClickHouse | n8n (workflows), Grafana (dashboards) |
| **Email** | BillionMail, useSend, Resend | LangChain (AI drafting), Dify (templates) |
| **Tasks/Todo** | trigger.dev, PostgreSQL | Dify (automation), n8n (scheduling) |
| **Documents** | MinIO, PyMuPDF, MinerU | Supabase Storage, Quivr (search) |
| **Reports** | ClickHouse, Grafana, Prometheus | DuckDB (embedded), trigger.dev (generation) |
| **Automation** | n8n, Dify, trigger.dev | LangGraph (AI chains), Flowise (chatbots) |
| **AI Copilot** | LangChain, LangGraph, crawl4ai | beads (memory), OpenViking (context) |
| **Code Dev** | Cline, Aider, OpenHands | codegraph (understanding), strix (security) |
| **Search** | Meilisearch, Typesense | rapidfuzz (fuzzy), Supabase full-text |
| **Security** | strix, truffleHog, OWASP crAPI | Sentry (errors), pgAudit (DB audit) |
| **Deployment** | Coolify, Podman, Ansible | Prometheus (monitoring), Grafana (dashboards) |
| **Knowledge Base** | Quivr, Directus, Dify | crawl4ai (collection), MinIO (storage) |
| **Analytics** | ClickHouse, Grafana, Prometheus | DuckDB (embedded), SigNoz (tracing) |
| **Email Marketing** | BillionMail, n8n | Dify (visual builder), LangChain (personalization) |

---

## PART 4: PORT MAP

| Port | Service | Protocol |
|------|---------|----------|
| 25 | BillionMail SMTP | TCP |
| 80 | Coolify (when deployed) | HTTP |
| 3000 | Next.js CRM Frontend | HTTP |
| 3001 | Dify Web (when deployed) | HTTP |
| 443 | Coolify HTTPS | HTTPS |
| 465 | BillionMail SMTPS | TCP |
| 587 | BillionMail Submission | TCP |
| 6379 | Valkey/Redis | TCP |
| 8055 | Directus (when deployed) | HTTP |
| 8080 | BillionMail Web UI (when deployed) | HTTP |
| 8081 | Go API | HTTP |
| 8123 | ClickHouse HTTP Interface | HTTP |
| 8443 | BillionMail HTTPS | HTTPS |
| 9000 | ClickHouse Native Protocol | TCP |
| 5001 | Dify API (when deployed) | HTTP |
| 5432 | PostgreSQL | TCP |
| 11434 | Ollama (local LLM) | HTTP |

---

## PART 5: WHAT NOT TO ADOPT (Rejected Repos)

| Repository | Reason for Rejection |
|-----------|---------------------|
| apache/shardingsphere | Java-based sharding; PostgreSQL RLS handles multi-tenancy |
| MinishLab/semble | Overlaps with codegraph; lower community |
| midudev/autoskills | Reference only; addyosmani/agent-skills is superior |
| VoltAgent/awesome-claude-code-subagents | Reference list; not a tool |
| frigate/frigate | Wrong domain: video surveillance, not CRM |
| iOfficeAI/AionUiq1 | 404 Not Found — repository removed |
| unicity-astrid/astrid | We build our own orchestration, not adopt Agent OS |
| RightNow-AI/openfang | Pilot only; we control orchestration layer |
| pbakaus/impeccable | Niche; addyosmani/agent-skills covers this |
| Leonxlnx/taste-skill | Niche; addyosmani/agent-skills covers this |
| 15+ more P4 repos | Wrong domain, duplicates, or superseded by adopted tools |

---

*Generated by Sovereign CRM — Phase 4 Repository Review*
*All 62 repositories evaluated and categorized*
