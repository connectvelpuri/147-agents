# REPOSITORY INTAKE & ADOPTION REVIEW
# Sovereign CRM — Complete Repository Evaluation

**Date:** June 7, 2026
**Evaluated Repositories:** 62 (1 removed: iOfficeAI/AionUiq1 = 404 Not Found)
**Architecture Reference:** Phase 3 Agentic SDLC Operating Model + Phase 4 Runtime Specifications
**CRM Stack:** Go/chi + Next.js + Supabase/PostgreSQL + Redis

---

## EXECUTIVE SUMMARY

62 repositories evaluated against the Sovereign CRM program architecture.
Each scored on 9 criteria (Architecture Fit, Security, Maintainability,
Community Strength, Documentation Quality, CRM Relevance, Agentic SDLC
Relevance, Scalability, Production Readiness) at 0-10 scale.

**Key Findings:**
- 5 P0 (Install Immediately): supabase, crawl4ai, langchain, trigger.dev, addyosmani/agent-skills
- 8 P1 (Strong Candidate): coolify, dify, pocketbase, openhands, codegraph, beads, openviking, agentmemory
- 12 P2 (Pilot First): BillionMail, useSend, turbovec, agent-reach, openfang, ralph, etc.
- 15 P3 (Nice to Have): whisper, kronos, appflowy, etc.
- 22 P4 (Reject): Direct duplicates, wrong domain, or superseded tools

---

## 1. REPOSITORY EVALUATION TABLE

### Scoring Criteria
- **AF** = Architecture Fit (0-10): How well it fits Go/Next.js/Supabase stack
- **SE** = Security (0-10): Security posture, vulnerability management
- **MA** = Maintainability (0-10): Code quality, release cadence, bus factor
- **CO** = Community (0-10): Stars, contributors, adoption velocity
- **DO** = Documentation (0-10): README, API docs, examples
- **CR** = CRM Relevance (0-10): Direct CRM module/workflow value
- **AS** = Agentic SDLC Relevance (0-10): Agent workflow/orchestration value
- **SC** = Scalability (0-10): Horizontal/vertical scaling potential
- **PR** = Production Readiness (0-10): Battle-tested, stable APIs
- **TOTAL** = Weighted sum (max 90)

### Tier 0: Core Infrastructure (Database, Auth, Deployment)

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 1 | supabase/supabase | 103,749 | TypeScript | 10 | 9 | 9 | 10 | 9 | 10 | 7 | 9 | 9 | **82** | **P0** |
| 2 | postgres/postgres | 21,101 | C | 10 | 9 | 10 | 10 | 9 | 10 | 2 | 10 | 10 | **80** | **P0** |
| 3 | coollabsio/coolify | 56,600 | PHP | 8 | 8 | 8 | 9 | 8 | 6 | 3 | 8 | 8 | **66** | **P1** |
| 4 | pocketbase/pocketbase | 58,939 | Go | 9 | 7 | 8 | 9 | 8 | 7 | 3 | 7 | 8 | **66** | P2* |
| 5 | directus/directus | 36,019 | TypeScript | 6 | 7 | 8 | 9 | 9 | 7 | 2 | 7 | 8 | **63** | P3 |
| 6 | apache/shardingsphere | 20,730 | Java | 5 | 8 | 8 | 7 | 6 | 4 | 1 | 9 | 7 | **55** | P4 |

*Note: PocketBase is a strong project but overlaps significantly with Supabase.
It is a lightweight alternative evaluated as P2 (pilot) for potential use in
lightweight agent memory storage or internal tooling, NOT as a replacement for
Supabase in the main CRM stack.*

### Tier 1: AI Agent Frameworks & Orchestration

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 7 | langchain-ai/langchain | 138,717 | Python | 7 | 7 | 7 | 10 | 8 | 6 | 10 | 8 | 8 | **71** | **P0** |
| 8 | langgenius/dify | 144,244 | TypeScript | 7 | 7 | 8 | 10 | 8 | 5 | 10 | 8 | 8 | **71** | **P1** |
| 9 | triggerdotdev/trigger.dev | 15,243 | TypeScript | 8 | 8 | 8 | 8 | 7 | 6 | 9 | 8 | 7 | **69** | **P0** |
| 10 | OpenHands/openhands | 76,091 | Python | 6 | 6 | 7 | 9 | 7 | 4 | 9 | 7 | 7 | **62** | **P1** |
| 11 | aaif-goose/goose | 47,161 | Rust | 6 | 7 | 7 | 9 | 6 | 4 | 9 | 8 | 6 | **62** | P2 |
| 12 | RightNow-AI/openfang | 17,752 | Rust | 6 | 7 | 7 | 8 | 5 | 4 | 9 | 8 | 5 | **59** | P2 |
| 13 | snarktank/ralph | 19,995 | TypeScript | 7 | 6 | 7 | 8 | 6 | 5 | 9 | 6 | 6 | **60** | P2 |
| 14 | affaan-m/ECC | 209,492 | JavaScript | 7 | 6 | 7 | 10 | 7 | 4 | 9 | 5 | 7 | **62** | P2 |
| 15 | SuperClaude-Org/SuperClaude_Framework | 23,203 | Python | 6 | 5 | 6 | 8 | 7 | 3 | 8 | 5 | 5 | **53** | P3 |
| 16 | phodal/routa | 1,663 | TypeScript | 7 | 6 | 6 | 5 | 5 | 5 | 9 | 7 | 4 | **54** | P3 |
| 17 | unicity-astrid/astrid | 7,933 | Rust | 5 | 6 | 6 | 7 | 4 | 3 | 8 | 7 | 5 | **51** | P3 |
| 18 | opensquilla/opensquilla | 3,432 | Python | 6 | 5 | 6 | 5 | 4 | 3 | 8 | 6 | 4 | **47** | P4 |

### Tier 2: Agent Memory & Context Management

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 19 | gastownhall/beads | 24,391 | Go | 9 | 7 | 7 | 8 | 6 | 6 | 9 | 7 | 6 | **65** | **P1** |
| 20 | volcengine/OpenViking | 25,254 | Python | 7 | 7 | 7 | 8 | 6 | 6 | 9 | 8 | 6 | **64** | **P1** |
| 21 | rohitg00/agentmemory | 21,660 | TypeScript | 8 | 6 | 7 | 8 | 6 | 6 | 9 | 7 | 6 | **63** | **P1** |
| 22 | colbymchenry/codegraph | 43,467 | TypeScript | 8 | 7 | 7 | 9 | 7 | 5 | 9 | 7 | 7 | **66** | **P1** |
| 23 | tirth8205/code-review-graph | 18,164 | Python | 7 | 7 | 7 | 8 | 6 | 5 | 9 | 7 | 6 | **62** | P2 |
| 24 | MinishLab/semble | 4,902 | Python | 7 | 6 | 7 | 6 | 6 | 4 | 8 | 6 | 5 | **55** | P3 |

### Tier 3: Web Crawling & Data Extraction

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 25 | unclecode/crawl4ai | 67,977 | Python | 8 | 7 | 8 | 9 | 8 | 7 | 8 | 7 | 8 | **70** | **P0** |
| 26 | getmaxun/maxun | 15,783 | TypeScript | 7 | 7 | 7 | 8 | 7 | 6 | 6 | 7 | 7 | **62** | P2 |
| 27 | Panniantong/Agent-Reach | 22,914 | Python | 7 | 6 | 7 | 8 | 6 | 5 | 8 | 6 | 6 | **59** | P2 |
| 28 | opendataloader-project/opendataloader-pdf | 24,013 | Java | 5 | 7 | 7 | 8 | 7 | 5 | 4 | 7 | 7 | **57** | P3 |
| 29 | alibaba/page-agent | 18,337 | TypeScript | 6 | 6 | 7 | 8 | 5 | 4 | 7 | 7 | 6 | **56** | P3 |
| 30 | firecrawl/open-lovable | 26,703 | TypeScript | 4 | 5 | 6 | 8 | 6 | 2 | 5 | 5 | 5 | **46** | P4 |

### Tier 4: Email & Communication

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 31 | Billionmail/BillionMail | 15,077 | Go | 7 | 7 | 7 | 8 | 6 | 8 | 3 | 7 | 7 | **60** | P2 |
| 32 | usesend/useSend | 4,328 | TypeScript | 7 | 7 | 7 | 6 | 6 | 8 | 3 | 7 | 6 | **57** | P2 |
| 33 | openai/whisper | 102,008 | Python | 3 | 8 | 9 | 10 | 8 | 3 | 4 | 8 | 9 | **62** | P3 |

### Tier 5: Security & Testing

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 34 | usestrix/strix | 25,860 | Python | 7 | 9 | 7 | 8 | 6 | 5 | 7 | 7 | 7 | **63** | P2 |
| 35 | aliasrobotics/cai | 8,895 | Python | 5 | 9 | 7 | 7 | 5 | 4 | 6 | 6 | 6 | **55** | P3 |
| 36 | mickamy/sql-tap | 1,510 | Go | 8 | 6 | 7 | 5 | 5 | 4 | 3 | 5 | 5 | **48** | P3 |

### Tier 6: Agent Skills & Development Tools

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 37 | addyosmani/agent-skills | 48,842 | Shell | 8 | 6 | 8 | 9 | 8 | 5 | 10 | 5 | 8 | **67** | **P0** |
| 38 | vercel-labs/skills | 21,572 | TypeScript | 7 | 6 | 7 | 8 | 6 | 4 | 9 | 6 | 6 | **59** | P2 |
| 39 | agentsmd/agents.md | 22,034 | TypeScript | 8 | 6 | 7 | 8 | 7 | 5 | 9 | 5 | 7 | **62** | P2 |
| 40 | VoltAgent/awesome-claude-code-subagents | 21,314 | Shell | 6 | 5 | 6 | 8 | 7 | 4 | 9 | 4 | 6 | **55** | P3 |
| 41 | midudev/autoskills | 5,901 | Ruby | 5 | 5 | 6 | 7 | 6 | 3 | 8 | 4 | 5 | **49** | P3 |
| 42 | darkrishabh/agent-skills-eval | 568 | TypeScript | 6 | 5 | 6 | 4 | 5 | 3 | 8 | 5 | 4 | **46** | P4 |
| 43 | Leonxlnx/taste-skill | 35,786 | Shell | 5 | 4 | 6 | 8 | 6 | 3 | 7 | 3 | 5 | **47** | P3 |
| 44 | pbakaus/impeccable | 35,315 | JavaScript | 5 | 4 | 6 | 8 | 6 | 3 | 7 | 4 | 5 | **48** | P3 |

### Tier 7: Vector Search & Databases

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 45 | milvus-io/milvus | 44,663 | Go | 7 | 8 | 8 | 9 | 7 | 6 | 7 | 9 | 8 | **69** | P2* |
| 46 | RyanCodrai/turbovec | 6,240 | Python/Rust | 6 | 6 | 6 | 6 | 5 | 4 | 6 | 7 | 5 | **51** | P3 |
| 47 | ClickHouse/ClickHouse | 47,861 | C++ | 5 | 8 | 9 | 9 | 7 | 4 | 3 | 10 | 9 | **64** | P3 |

*Milvus evaluated P2 (pilot) — Supabase pgvector may suffice for initial vector needs. Milvus becomes relevant at scale >10M embeddings.*

### Tier 8: No-Code/Low-Code & Productivity

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 48 | AppFlowy-IO/AppFlowy | 71,998 | Dart | 3 | 7 | 7 | 9 | 7 | 5 | 2 | 7 | 7 | **54** | P3 |
| 49 | BloopAI/vibe-kanban | 26,831 | Rust | 6 | 5 | 7 | 8 | 5 | 4 | 8 | 5 | 5 | **53** | P3 |

### Tier 9: AI Engineering Education & Templates

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 50 | Shubhamsaboo/awesome-llm-apps | 113,625 | Python | 4 | 5 | 6 | 10 | 8 | 3 | 6 | 3 | 4 | **49** | P3 |
| 51 | rohitg00/ai-engineering-from-scratch | 29,646 | Python | 3 | 5 | 6 | 8 | 7 | 2 | 5 | 3 | 4 | **43** | P4 |
| 52 | datawhalechina/easy-vibe | 16,456 | JavaScript | 3 | 4 | 5 | 7 | 6 | 2 | 4 | 3 | 3 | **37** | P4 |
| 53 | danielmiessler/Personal_AI_Infrastructure | 15,159 | TypeScript | 5 | 6 | 7 | 8 | 6 | 3 | 7 | 4 | 5 | **51** | P3 |
| 54 | KhazP/vibe-coding-prompt-template | 2,461 | — | 5 | 4 | 5 | 5 | 6 | 3 | 7 | 3 | 3 | **41** | P4 |

### Tier 10: Specialized / Domain-Specific

| # | Repository | Stars | Language | AF | SE | MA | CO | DO | CR | AS | SC | PR | TOTAL | Priority |
|---|-----------|-------|----------|----|----|----|----|----|----|----|----|-----|-------|----------|
| 55 | shiyu-coder/Kronos | 28,871 | Python | 2 | 6 | 7 | 8 | 5 | 2 | 3 | 7 | 6 | **46** | P4 |
| 56 | braedonsaunders/codeflow | 3,395 | HTML | 6 | 5 | 6 | 6 | 6 | 4 | 5 | 4 | 5 | **47** | P3 |
| 57 | deanpeters/Product-Manager-Skills | 4,898 | Shell | 5 | 5 | 6 | 6 | 6 | 5 | 8 | 3 | 5 | **49** | P3 |
| 58 | open-gitagent/gitagent | 519 | TypeScript | 6 | 5 | 5 | 4 | 4 | 3 | 7 | 5 | 3 | **42** | P4 |
| 59 | cline/cline | 62,900 | TypeScript | 6 | 6 | 8 | 9 | 7 | 4 | 8 | 6 | 7 | **61** | P2 |
| 60 | Aider-AI/aider | 45,900 | Python | 5 | 6 | 8 | 9 | 7 | 4 | 7 | 5 | 7 | **58** | P3 |
| 61 | opensandbox-group/OpenSandbox | 11,370 | Python | 6 | 8 | 7 | 7 | 5 | 4 | 7 | 8 | 5 | **57** | P2 |

---

## 2. CAPABILITY MAPPING MATRIX

Maps each adopted/piloted repository to the capability it provides.

| Capability Category | Repository | What It Does | CRM Module Impact | Maturity |
|--------------------|-----------|-------------|-------------------|----------|
| **Database (Primary)** | supabase/supabase | PostgreSQL + Auth + Realtime + RLS + Edge Functions | All modules — foundational | Production |
| **Database (OLAP)** | ClickHouse/ClickHouse | Real-time analytics, columnar storage | Reports, Dashboard (Phase 2) | Production |
| **Database (Vector)** | milvus-io/milvus | Vector similarity search at scale | AI/ML features, semantic search | Production |
| **Database (Sharding)** | apache/shardingsphere | Distributed SQL, read-write splitting | Multi-tenant scaling (Phase 3) | Production |
| **Deployment (PaaS)** | coollabsio/coolify | Self-hosted PaaS, one-click deploys | DevOps, Sprint 0 infrastructure | Production |
| **Deployment (Container)** | opensandbox-group/OpenSandbox | Secure sandbox runtime for agents | Agent execution isolation | Beta |
| **Email (Server)** | Billionmail/BillionMail | Self-hosted mail server + newsletter | Communications module, Sequences | Production |
| **Email (API)** | usesend/useSend | Transactional email API (SES alternative) | Email Templates, Sequences | Beta |
| **Agent Framework** | langchain-ai/langchain | Agent engineering, chains, tools | All agent workflows | Production |
| **Agent Platform** | langgenius/dify | Visual agentic workflow builder | Workflow module, agent orchestration | Production |
| **Agent Orchestration** | triggerdotdev/trigger.dev | Background job + workflow engine | Workflow automation, scheduled tasks | Production |
| **Agent Coding** | OpenHands/openhands | AI-driven development agent | Engineering agents, code generation | Production |
| **Agent Coding** | cline/cline | Autonomous coding agent | Engineering agents | Production |
| **Agent Coding** | Aider-AI/aider | AI pair programming | Engineering agents | Production |
| **Agent Coding** | aaif-goose/goose | Extensible AI agent | Engineering agents | Production |
| **Memory (Persistent)** | gastownhall/beads | Agent memory system | All agents — working memory | Production |
| **Memory (Context DB)** | volcengine/OpenViking | Context database for agents | All agents — long-term memory | Beta |
| **Memory (Persistent)** | rohitg00/agentmemory | Persistent agent memory | All agents — cross-session memory | Production |
| **Code Intelligence** | colbymchenry/codegraph | Code knowledge graph | Engineering agents, code review | Production |
| **Code Intelligence** | tirth8205/code-review-graph | Code review graph | Code Review agent, Quality agents | Production |
| **Code Search** | MinishLab/semble | Token-efficient code search | Engineering agents | Beta |
| **Web Crawling** | unclecode/crawl4ai | LLM-friendly web crawler | Research agents, VoC, Market Intel | Production |
| **Web Scraping** | getmaxun/maxun | No-code web scraping | Research agents, data extraction | Production |
| **Web Research** | Panniantong/Agent-Reach | Multi-platform web research | Research agents, competitive intel | Beta |
| **Document Processing** | opendataloader-project/opendataloader-pdf | PDF parsing for AI | Document module | Production |
| **Security Testing** | usestrix/strix | AI-powered vulnerability scanning | DevSecOps agents | Production |
| **Security Testing** | aliasrobotics/cai | Cybersecurity AI framework | DevSecOps agents | Beta |
| **SQL Monitoring** | mickamy/sql-tap | Real-time SQL traffic monitor | DevOps, database debugging | Production |
| **Agent Skills** | addyosmani/agent-skills | Production engineering skills | All coding agents | Production |
| **Agent Skills** | vercel-labs/skills | Agent skill distribution | All agents — skill marketplace | Beta |
| **Agent Format** | agentsmd/agents.md | Standard agent coding format | All agents — interop standard | Beta |
| **Agent Skills** | VoltAgent/awesome-claude-code-subagents | 100+ specialized subagents | All agents — reference library | Reference |
| **Agent Skills** | midudev/autoskills | One-command skill installer | Agent setup automation | Beta |
| **Agent Skills** | SuperClaude-Org/SuperClaude_Framework | Claude Code enhancement | Engineering agents | Beta |
| **Agent Skills** | Leonxlnx/taste-skill | Design quality enforcement | Design agents | Beta |
| **Agent Skills** | pbakaus/impeccable | Design language for AI | Design agents | Beta |
| **Agent Skills** | darkrishabh/agent-skills-eval | Agent skill testing | Quality assurance | Beta |
| **Task Management** | BloopAI/vibe-kanban | Agent task management | Sprint management, Kanban | Beta |
| **Autonomous Execution** | snarktank/ralph | PRD-to-completion agent | Engineering agents | Beta |
| **Multi-Agent Coordination** | phodal/routa | Workspace-first multi-agent | All agents — coordination | Alpha |
| **Speech Recognition** | openai/whisper | Speech-to-text | Communications module (Phase 2) | Production |
| **Analytics** | ClickHouse/ClickHouse | Real-time OLAP | Reports, Dashboard | Production |
| **Knowledge Sharing** | Shubhamsaboo/awesome-llm-apps | LLM app reference collection | Reference only | Reference |
| **AI Education** | rohitg00/ai-engineering-from-scratch | AI engineering course | Reference only | Reference |
| **AI Education** | datawhalechina/easy-vibe | Vibe coding course | Reference only | Reference |
| **Personal AI** | danielmiessler/Personal_AI_Infrastructure | Personal AI setup patterns | Reference only | Reference |
| **Prompt Templates** | KhazP/vibe-coding-prompt-template | PRD/tech design templates | Reference only | Reference |
| **Architecture Viz** | braedonsaunders/codeflow | Code architecture visualization | Developer experience | Production |
| **PM Skills** | deanpeters/Product-Manager-Skills | PM frameworks for AI | Product agents | Reference |
| **Git-Native Agents** | open-gitagent/gitagent | Version-controlled agent config | Agent management | Alpha |
| **Web GUI Agent** | alibaba/page-agent | In-page GUI automation | UI testing agents | Beta |
| **Website Cloning** | firecrawl/open-lovable | Website to React app | Prototyping agents | Beta |
| **Token Optimization** | opensquilla/opensquilla | Token-efficient agent execution | Cost optimization | Alpha |
| **Agent OS** | RightNow-AI/openfang | Agent operating system | Agent infrastructure | Beta |
| **Agent OS** | unicity-astrid/astrid | Agent operating system | Agent infrastructure | Alpha |
| **Financial AI** | shiyu-coder/Kronos | Financial markets model | Not applicable | N/A |
| **Vector Index** | RyanCodrai/turbovec | High-performance vector index | Vector search (alternative to Milvus) | Beta |
| **Notion Alternative** | AppFlowy-IO/AppFlowy | Collaborative workspace | Internal docs (Phase 2) | Production |

---

## 3. AGENT MAPPING MATRIX

Maps each repository to the 104 agents defined in Phase 3.

| Repository | Primary Agents | Secondary Agents | Workflow |
|-----------|---------------|-----------------|----------|
| supabase/supabase | All agents (infrastructure) | — | Database operations, auth, realtime |
| langchain-ai/langchain | AI Engineer, Backend Architect | All agent workflows | Agent chain construction |
| langgenius/dify | AI Engineer, DevOps Automator | Workflow Orchestrator | Visual workflow building |
| triggerdotdev/trigger.dev | DevOps Automator, Infrastructure Maintainer | All agents (scheduled tasks) | Background job execution |
| crawl4ai | Market Intel Agent, VoC Analyst, Trend Researcher | Competitive Intel, Feedback Synthesizer | Web research, data collection |
| addyosmani/agent-skills | Frontend Developer, Backend Architect | All coding agents | Engineering skill execution |
| gastownhall/beads | All agents (memory layer) | — | Cross-session memory persistence |
| volcengine/OpenViking | All agents (context layer) | — | Context management |
| rohitg00/agentmemory | All agents (memory layer) | — | Persistent memory storage |
| colbymchenry/codegraph | Code Review Agent, Test Writer/Fixer | Frontend/Backend Developer | Code understanding, review |
| tirth8205/code-review-graph | Code Review Agent | Security Auditor | Code review intelligence |
| OpenHands/openhands | Frontend Developer, Backend Architect | Rapid Prototyper, Mobile App Builder | AI-driven code generation |
| cline/cline | Frontend Developer, Backend Architect | Rapid Prototyper | Autonomous coding |
| Aider-AI/aider | Frontend Developer, Backend Architect | — | AI pair programming |
| aaif-goose/goose | AI Engineer | All agents | Extensible agent execution |
| Billionmail/BillionMail | Support Responder, Content Creator | Email Agent, Marketing agents | Email delivery, newsletters |
| usesend/useSend | Support Responder, Content Creator | Email Agent | Transactional email |
| usestrix/strix | Security Auditor, Legal Compliance Checker | DevSecOps agents | Security testing |
| aliasrobotics/cai | Security Auditor | DevSecOps agents | Penetration testing |
| mickamy/sql-tap | Infrastructure Maintainer | Backend Architect | SQL debugging |
| coolify | Infrastructure Maintainer, DevOps Automator | — | Deployment management |
| opensandbox-group/OpenSandbox | All agents (sandbox) | — | Secure agent execution |
| pocketbase/pocketbase | Rapid Prototyper | Backend Architect | Lightweight backend |
| directus/directus | UI Designer, Content Creator | — | Headless CMS |
| milvus-io/milvus | AI Engineer | All AI-powered agents | Vector search |
| ClickHouse/ClickHouse | Analytics Reporter | Reports Agent | Real-time analytics |
| apache/shardingsphere | Infrastructure Maintainer | Backend Architect | Database scaling |
| vercel-labs/skills | All agents (skill distribution) | — | Skill management |
| agentsmd/agents.md | All agents (format standard) | — | Inter-agent communication |
| VoltAgent/awesome-claude-code-subagents | All agents (reference) | — | Subagent selection |
| midudev/autoskills | All agents (setup) | — | Skill installation |
| SuperClaude-Org/SuperClaude_Framework | Engineering agents | — | Claude Code enhancement |
| darkrishabh/agent-skills-eval | Quality agents | Test Writer/Fixer | Skill evaluation |
| Leonxlnx/taste-skill | UI Designer, Brand Guardian | Visual Storyteller | Design quality |
| pbakaus/impeccable | UI Designer, Brand Guardian | — | Design language |
| BloopAI/vibe-kanban | Sprint Prioritizer, Project Shipper | All agents (task mgmt) | Task orchestration |
| snarktank/ralph | Rapid Prototyper | Engineering agents | Autonomous PRD execution |
| phodal/routa | All agents (coordination) | — | Multi-agent workspace |
| openai/whisper | Support Responder | Communications agents | Speech-to-text |
| braedonsaunders/codeflow | All agents (code navigation) | — | Architecture visualization |
| deanpeters/Product-Manager-Skills | Product agents | Sprint Prioritizer, Feedback Synthesizer | PM methodology |
| open-gitagent/gitagent | All agents (git-native config) | — | Agent version control |
| alibaba/page-agent | UI Testing Agent | QA agents | In-page automation |
| firecrawl/open-lovable | Rapid Prototyper | Frontend Developer | Website cloning |
| opensquilla/opensquilla | All agents (cost optimization) | — | Token efficiency |
| RightNow-AI/openfang | All agents (agent OS) | — | Agent infrastructure |
| unicity-astrid/astrid | All agents (agent OS) | — | Agent infrastructure |
| AppFlowy-IO/AppFlowy | Content Creator | Internal docs agents | Collaborative docs |
| shiyu-coder/Kronos | N/A (financial domain) | — | N/A |
| RyanCodrai/turbovec | AI Engineer | Vector search agents | Vector indexing |
| Shubhamsaboo/awesome-llm-apps | N/A (reference) | — | Reference collection |
| rohitg00/ai-engineering-from-scratch | N/A (education) | — | Reference collection |
| datawhalechina/easy-vibe | N/A (education) | — | Reference collection |
| danielmiessler/Personal_AI_Infrastructure | N/A (reference) | — | Reference collection |
| KhazP/vibe-coding-prompt-template | Product agents | — | PRD templates |

---

## 4. CONSOLIDATION REVIEW

### 4.1 Duplicate Detection

| Group | Repositories | Overlap | Recommendation |
|-------|-------------|---------|----------------|
| **Agent Coding Tools** | cline/cline, Aider-AI/aider, OpenHands/openhands, aaif-goose/goose | All provide AI-assisted coding | Adopt cline (highest community, SDK mode) + aider (terminal-first, mature). Keep goose as alternative. Drop openhands (overlaps with cline). |
| **Agent Memory** | gastownhall/beads, volcengine/OpenViking, rohitg00/agentmemory | All provide persistent agent memory | Adopt beads (Go, native to our stack) + openviking (context DB). Drop agentmemory (TypeScript, overlaps with beads). |
| **Code Intelligence** | colbymchenry/codegraph, tirth8205/code-review-graph, MinishLab/semble | All provide code understanding | Adopt codegraph (highest stars, MCP support). Keep code-review-graph for review-specific use. Drop semble (overlaps with codegraph). |
| **Agent Skills** | addyosmani/agent-skills, vercel-labs/skills, midudev/autoskills, VoltAgent/awesome-claude-code-subagents, Leonxlnx/taste-skill, pbakaus/impeccable | All provide agent skill definitions | Adopt addyosmani/agent-skills (production-grade). Keep taste-skill and impeccable for design. Drop others (reference/overlaps). |
| **Agent OS** | RightNow-AI/openfang, unicity-astrid/astrid | Both provide agent operating systems | Pilot both. Drop opensquilla (overlaps, less mature). |
| **Email** | Billionmail/BillionMail, usesend/useSend | Both provide email capabilities | BillionMail for self-hosted SMTP. useSend for API-based transactional email. Complementary, not duplicative. |
| **Web Scraping** | unclecode/crawl4ai, getmaxun/maxun, Panniantong/Agent-Reach | All provide web data extraction | Adopt crawl4ai (LLM-optimized, highest community). Keep maxun for no-code use cases. Keep agent-reach for multi-platform research. |
| **Vector Search** | milvus-io/milvus, RyanCodrai/turbovec | Both provide vector search | Milvus for production vector DB. turbovec as lightweight alternative. Supabase pgvector may suffice initially. |
| **Task Management** | BloopAI/vibe-kanban, snarktank/ralph | Both manage agent tasks | vibe-kanban for visual task management. ralph for autonomous PRD execution. Complementary. |
| **Security** | usestrix/strix, aliasrobotics/cai | Both provide security testing | strix (higher community, more production-ready). CAI for advanced pentesting. |
| **Notion/Docs** | AppFlowy-IO/AppFlowy, directus/directus | Both provide content management | AppFlowy for collaborative docs (Phase 2). Directus for headless CMS (Phase 2). |

### 4.2 Better Alternatives Identified

| Repository | Superseded By | Reason |
|-----------|--------------|--------|
| opensquilla/opensquilla | addyosmani/agent-skills + gastownhall/beads | Token optimization achieved through better skills + memory, not a separate framework |
| midudev/autoskills | addyosmani/agent-skills | addyosmani has 8x stars, production-grade, better maintained |
| VoltAgent/awesome-claude-code-subagents | addyosmani/agent-skills | Reference list, not actionable tools |
| open-gitagent/gitagent | agentsmd/agents.md | agents.md is the emerging standard format |
| datawhalechina/easy-vibe | rohitg00/ai-engineering-from-scratch | Overlapping educational content |
| KhazP/vibe-coding-prompt-template | deanpeters/Product-Manager-Skills | PM Skills has broader coverage |
| darkrishabh/agent-skills-eval | Custom testing (built in-house) | Too early-stage for production use |
| firecrawl/open-lovable | Rapid prototyping via cline/cline | Website cloning is a niche use case |

### 4.3 Conflicts

| Conflict | Repositories | Issue | Resolution |
|----------|-------------|-------|-----------|
| Agent OS vs Agent Framework | openfang/astrid vs langchain/dify | Agent OS attempts to replace the entire stack; we're building our own | Reject agent OS projects — we control our own orchestration |
| PocketBase vs Supabase | pocketbase/supabase | Both provide PostgreSQL-backed backends | Supabase is already in the stack. PocketBase is a lightweight alternative for internal tools only |
| PHP in Go/TS stack | coolify | coolify is PHP — adds another language to maintain | Acceptable because it's a deployment tool, not application code |
| Java in Go/TS stack | opendataloader-pdf, shardingsphere | Java adds runtime complexity | opendataloader-pdf: evaluate Docker-based usage. shardingsphere: evaluate only at scale |

---

## 5. GAP ANALYSIS

### 5.1 Capabilities Still Missing

| Missing Capability | Why It Matters | Recommended Action |
|-------------------|---------------|-------------------|
| **API Gateway / Rate Limiting** | No repository addresses API gateway, rate limiting, or request routing at the edge | Evaluate: Traefik, Caddy, or Kong (open-source API gateway) |
| **Observability Stack** | No repository provides distributed tracing, metrics, or log aggregation | Evaluate: OpenTelemetry + Grafana + Prometheus (standard stack) |
| **CI/CD Pipeline** | No repository provides automated testing, building, and deployment | Evaluate: Woodpecker CI, Drone, or GitHub Actions (self-hosted) |
| **Backup & Disaster Recovery** | No repository addresses database backup, replication, or DR | Evaluate: pgBackRest, Barman, or Supabase built-in backups |
| **Multi-Tenant Isolation** | While RLS is implemented, no repository provides tenant-level resource quotas | Build custom: per-tenant rate limits, storage quotas, compute limits |
| **Audit Logging** | No repository provides structured audit trail for compliance | Evaluate: pgAudit extension for PostgreSQL |
| **Secret Management** | No repository addresses secrets rotation, vault integration | Evaluate: HashiCorp Vault (self-hosted) or SOPS |
| **Email Deliverability** | BillionMail provides SMTP, but no repository handles DMARC/DKIM/SPF setup | BillionMail includes this; verify during Sprint 0 |
| **Real-Time Notifications** | Supabase Realtime covers WebSocket, but no repository handles push notifications | Evaluate: OneSignal (self-hosted) or Firebase Cloud Messaging |
| **Search Engine** | No repository provides full-text search across CRM entities | Evaluate: Meilisearch or Typesense (self-hosted, fast) |
| **File Storage** | Supabase Storage exists, but no repository provides S3-compatible object storage | Evaluate: MinIO (self-hosted S3-compatible) |
| **Workflow Engine (Visual)** | While trigger.dev handles background jobs, no repository provides visual workflow builder | Dify covers this; evaluate for Phase 2 |
| **CRM-Specific Analytics** | No repository provides CRM-specific metrics (pipeline velocity, conversion rates) | Build custom in Go |
| **Data Import/Export** | No repository provides CRM-specific data migration tools | Build custom (already partially implemented in Sprint 6) |
| **API Documentation** | No repository provides OpenAPI/Swagger generation | Evaluate: swaggo/swag for Go, or Stoplight Elements |

### 5.2 Architecture Areas Unsupported

| Area | Current State | Gap | Recommended Repository |
|------|--------------|-----|----------------------|
| **Edge/CDN** | No edge layer | No request caching, no static asset CDN | Evaluate: Caddy or Traefik as reverse proxy |
| **Message Queue** | No async message system | Background jobs run in-process | Evaluate: NATS or Redis Streams (already have Redis) |
| **Service Mesh** | Monolithic Go API | No service-to-service communication layer | Not needed at current scale — revisit at 10x |
| **Feature Flags** | No feature flag system | No gradual rollout capability | Evaluate: Flipt (self-hosted, open-source) |
| **A/B Testing** | No experimentation framework | Cannot test UI variants | Build custom or evaluate: GrowthBook |
| **Webhook Management** | Basic webhook support | No webhook retry, delivery guarantees | Evaluate: Svix (self-hosted webhooks) |
| **Idempotency** | No idempotency layer | API requests may be processed twice | Build custom using Redis |

### 5.3 Recommended Additional Repositories

| Repository | Purpose | Priority | Stars |
|-----------|---------|----------|-------|
| Traefik/Caddy | Reverse proxy, TLS, routing | P0 for Sprint 0 | 50K+ |
| Meilisearch/Typesense | Full-text search | P1 for Phase 2 | 50K+/20K+ |
| MinIO | S3-compatible file storage | P1 for Phase 2 | 50K+ |
| OpenTelemetry | Distributed tracing | P1 for Phase 2 | 30K+ |
| Grafana + Prometheus | Monitoring dashboards | P1 for Phase 2 | 65K+/55K+ |
| pgAudit | PostgreSQL audit logging | P1 for Sprint 0 | 2K+ |
| Flipt | Feature flags | P2 for Phase 3 | 5K+ |
| Svix | Webhook delivery | P2 for Phase 3 | 5K+ |
| NATS | Message queue | P2 (Redis Streams may suffice) | 15K+ |
| Woodpecker CI | Self-hosted CI/CD | P2 for Sprint 0 | 5K+ |

---

## 6. ADOPTION ROADMAP

### Sprint 0: Foundation (Weeks 1-2)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Deploy Supabase | supabase/supabase | Database + Auth + Realtime foundation |
| Deploy PostgreSQL | postgres/postgres | Primary data store (via Supabase) |
| Deploy Reverse Proxy | Traefik or Caddy | TLS termination, routing, rate limiting |
| Setup Agent Skills | addyosmani/agent-skills | Engineering agents need skills immediately |
| Install pgAudit | pgAudit | Audit logging from day one |

### Sprint 1: Agent Infrastructure (Weeks 3-4)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Setup Agent Memory | gastownhall/beads | Agents need persistent memory |
| Setup Code Intelligence | colbymchenry/codegraph | Code review agents need code understanding |
| Deploy LangChain | langchain-ai/langchain | Agent chain construction |
| Setup Agent Format | agentsmd/agents.md | Standardize agent configuration |
| Deploy Crawl4AI | unclecode/crawl4ai | Research agents need web crawling |

### Sprint 2: Workflow & Automation (Weeks 5-6)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Deploy Trigger.dev | triggerdotdev/trigger.dev | Background jobs, scheduled workflows |
| Deploy Dify | langgenius/dify | Visual workflow builder for non-technical users |
| Deploy BillionMail | Billionmail/BillionMail | Self-hosted email delivery |
| Deploy useSend | usesend/useSend | Transactional email API |
| Setup Strix | usestrix/strix | Security testing in CI |

### Sprint 3: Development Velocity (Weeks 7-8)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Deploy Cline | cline/cline | AI coding agent for developers |
| Deploy Aider | Aider-AI/aider | Terminal-first AI pair programming |
| Deploy Code Review Graph | tirth8205/code-review-graph | Code review intelligence |
| Deploy OpenSandbox | opensandbox-group/OpenSandbox | Secure agent execution |
| Deploy Coolify | coollabsio/coolify | Self-hosted PaaS for deployment |

### Phase 2: Scale (Months 3-4)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Evaluate Milvus | milvus-io/milvus | Vector search at scale (if pgvector insufficient) |
| Deploy ClickHouse | ClickHouse/ClickHouse | Real-time analytics for reports |
| Deploy Meilisearch | Meilisearch | Full-text search across CRM |
| Deploy MinIO | MinIO | S3-compatible file storage |
| Deploy OpenViking | volcengine/OpenViking | Advanced context management |

### Phase 3: Enterprise (Months 5-6)

| Action | Repository | Why Now |
|--------|-----------|---------|
| Evaluate ShardingSphere | apache/shardingsphere | Multi-tenant database sharding |
| Deploy Flipt | Flipt | Feature flags for gradual rollout |
| Deploy Svix | Svix | Webhook delivery guarantees |
| Deploy OpenFang | RightNow-AI/openfang | Agent OS evaluation |
| Deploy AppFlowy | AppFlowy-IO/AppFlowy | Internal collaborative docs |

---

## 7. INSTALLATION PRIORITY

### P0: Install Immediately (5 repositories)

| Repository | Install Method | Effort | Dependency |
|-----------|---------------|--------|-----------|
| supabase/supabase | podman-compose (official) | Medium | PostgreSQL, Redis |
| postgres/postgres | Via Supabase | Low | None |
| addyosmani/agent-skills | Shell script copy | Low | None |
| unclecode/crawl4ai | pip install | Low | Python 3.11+ |
| triggerdotdev/trigger.dev | npm install + self-host | Medium | Node.js, PostgreSQL |

### P1: Strong Candidate (8 repositories)

| Repository | Install Method | Effort | Dependency |
|-----------|---------------|--------|-----------|
| langchain-ai/langchain | pip install | Low | Python 3.11+ |
| langgenius/dify | podman-compose (official) | Medium | PostgreSQL, Redis |
| gastownhall/beads | go install | Low | Go 1.22+ |
| volcengine/OpenViking | pip install | Low | Python 3.11+ |
| colbymchenry/codegraph | npm install | Low | Node.js |
| rohitg00/agentmemory | npm install | Low | Node.js |
| coollabsio/coolify | curl install script | Low | Linux server |
| OpenHands/openhands | pip install | Medium | Python 3.11+ |

### P2: Pilot First (12 repositories)

| Repository | Pilot Scope | Duration | Success Criteria |
|-----------|------------|----------|-----------------|
| cline/cline | 2 developers | 2 weeks | 20% code output increase |
| Aider-AI/aider | 2 developers | 2 weeks | Code quality improvement |
| Billionmail/BillionMail | Internal comms | 4 weeks | 95% email delivery rate |
| usesend/useSend | Transactional email | 4 weeks | API reliability >99.9% |
| RyanCodrai/turbovec | Vector search test | 2 weeks | Query latency <50ms |
| Panniantong/Agent-Reach | Research agents | 2 weeks | Data quality >80% |
| RightNow-AI/openfang | Agent orchestration | 4 weeks | Task completion >90% |
| snarktank/ralph | PRD execution | 2 weeks | PRD-to-code completion |
| usestrix/strix | Security scan | 1 week | Zero false positives |
| tirth8205/code-review-graph | Code review | 2 weeks | Review accuracy >85% |
| MinishLab/semble | Code search | 2 weeks | Search relevance >90% |
| opensandbox-group/OpenSandbox | Agent sandbox | 2 weeks | Isolation verified |

### P3: Nice to Have (15 repositories)

| Repository | When | Condition |
|-----------|------|-----------|
| openai/whisper | Phase 2 | When voice features needed |
| milvus-io/milvus | Phase 2 | When pgvector hits limits |
| ClickHouse/ClickHouse | Phase 2 | When analytics volume exceeds PostgreSQL |
| AppFlowy-IO/AppFlowy | Phase 3 | When internal docs needed |
| BloopAI/vibe-kanban | Phase 2 | When sprint management needed |
| phodal/routa | Phase 3 | When multi-agent coordination needed |
| open-gitagent/gitagent | Phase 3 | When agent versioning needed |
| directus/directus | Phase 2 | When headless CMS needed |
| deanpeters/Product-Manager-Skills | Sprint 1 | When product agents activated |
| braedonsaunders/codeflow | Sprint 1 | When architecture visualization needed |
| SuperClaude-Org/SuperClaude_Framework | Sprint 1 | When Claude enhancement needed |
| aliasrobotics/cai | Phase 3 | When advanced pentesting needed |
| mickamy/sql-tap | Sprint 0 | When SQL debugging needed |
| alibaba/page-agent | Phase 3 | When UI testing needed |
| Leonxlnx/taste-skill | Sprint 1 | When design quality needed |

### P4: Reject (22 repositories)

| Repository | Reason |
|-----------|--------|
| iOfficeAI/AionUiq1 | 404 Not Found — repository does not exist |
| shiyu-coder/Kronos | Financial markets domain — zero CRM relevance |
| opensquilla/opensquilla | Token optimization achieved through better skills/memory |
| midudev/autoskills | Superseded by addyosmani/agent-skills (8x community) |
| VoltAgent/awesome-claude-code-subagents | Reference list, not actionable tools |
| darkrishabh/agent-skills-eval | Too early-stage, evaluate later |
| datawhalechina/easy-vibe | Educational content, not production tool |
| Shubhamsaboo/awesome-llm-apps | Reference collection, not installable tool |
| rohitg00/ai-engineering-from-scratch | Educational content, not production tool |
| danielmiessler/Personal_AI_Infrastructure | Reference patterns, not installable tool |
| KhazP/vibe-coding-prompt-template | Superseded by deanpeters/Product-Manager-Skills |
| open-gitagent/gitagent | Superseded by agentsmd/agents.md format |
| firecrawl/open-lovable | Website cloning — niche use case, not CRM-relevant |
| apache/shardingsphere | Java runtime complexity — premature optimization |
| pocketbase/pocketbase | Overlaps with Supabase — already in stack |
| directus/directus | Overlaps with Supabase admin — not needed |
| AppFlowy-IO/AppFlowy | Dart runtime — premature, evaluate in Phase 3 |
| unicity-astrid/astrid | Agent OS — too early, we control our own orchestration |
| RightNow-AI/openfang | Agent OS — too early, evaluate in Phase 3 |
| tirth8205/code-review-graph | Overlaps with codegraph — codegraph is superior |
| pbakaus/impeccable | Design language — nice but not critical |
| RyanCodrai/turbovec | Vector index — Milvus or pgvector preferred |

---

## 8. RECOMMENDED REPOSITORY STACK

### Tier 1: Non-Negotiable (Must Have)

| Repository | Role | License | Stack Fit |
|-----------|------|---------|----------|
| supabase/supabase | Database + Auth + Realtime | Apache-2.0 | Perfect |
| postgres/postgres | Primary database | PostgreSQL | Perfect |
| langchain-ai/langchain | Agent engineering platform | MIT | Good |
| triggerdotdev/trigger.dev | Background jobs + workflows | Apache-2.0 | Perfect |
| addyosmani/agent-skills | Engineering skills for agents | MIT | Perfect |
| unclecode/crawl4ai | Web crawling for research | Apache-2.0 | Good |

### Tier 2: High Value (Should Have)

| Repository | Role | License | Stack Fit |
|-----------|------|---------|----------|
| gastownhall/beads | Agent memory system | MIT | Perfect (Go) |
| colbymchenry/codegraph | Code knowledge graph | MIT | Good |
| langgenius/dify | Visual workflow builder | Custom | Good |
| coollabsio/coolify | Self-hosted PaaS | Apache-2.0 | Acceptable (PHP) |
| Billionmail/BillionMail | Self-hosted email | AGPL-3.0 | Good (Go) |
| usestrix/strix | Security testing | Apache-2.0 | Good |

### Tier 3: Strategic (Nice to Have)

| Repository | Role | License | Stack Fit |
|-----------|------|---------|----------|
| cline/cline | AI coding agent | Apache-2.0 | Good |
| Aider-AI/aider | AI pair programming | Apache-2.0 | Good |
| volcengine/OpenViking | Context database | AGPL-3.0 | Good |
| milvus-io/milvus | Vector database | Apache-2.0 | Good (Go) |
| OpenSandbox | Agent sandbox | Apache-2.0 | Good |
| agentsmd/agents.md | Agent format standard | MIT | Perfect |

---

## 9. FINAL RECOMMENDATIONS

### 9.1 Immediate Actions (Sprint 0)

1. **Install Supabase** — Already planned, confirmed as #1 priority
2. **Install pgAudit** — Audit logging from day one
3. **Install Traefik or Caddy** — Reverse proxy, TLS, rate limiting
4. **Copy addyosmani/agent-skills** — Engineering agents need skills immediately
5. **Install crawl4ai** — Research agents need web crawling capability
6. **Install beads** — Agent memory system (Go, native stack fit)
7. **Install codegraph** — Code understanding for review agents

### 9.2 Architecture Decisions

| Decision | Recommendation | Rationale |
|----------|---------------|-----------|
| Primary Database | Supabase (PostgreSQL) | Already in stack, provides auth + realtime + RLS |
| Agent Framework | LangChain + custom Go orchestrator | LangChain for Python agents, Go for core orchestration |
| Agent Memory | beads + OpenViking | beads for working memory, OpenViking for context DB |
| Email Delivery | BillionMail (self-hosted SMTP) + useSend (API) | Complementary: SMTP server + API abstraction |
| Web Crawling | crawl4ai | LLM-optimized, highest community, production-ready |
| Code Intelligence | codegraph | MCP support, pre-indexed, works with multiple agents |
| Security Testing | strix | AI-powered, production-ready, Apache-2.0 |
| Deployment | Coolify + Podman | Self-hosted PaaS, container orchestration |
| Background Jobs | trigger.dev | TypeScript, workflow engine, MCP support |
| Visual Workflows | Dify | Low-code workflow builder for non-technical users |

### 9.3 What NOT to Adopt

1. **Do not adopt Agent OS projects** (openfang, astrid) — we control our own orchestration
2. **Do not adopt PocketBase** — Supabase is already the foundation
3. **Do not adopt Java tools** (ShardingSphere, opendataloader-pdf) unless Docker-contained
4. **Do not adopt educational repos** — reference only, not production tools
5. **Do not adopt token optimization frameworks** — achieve through better skills + memory

### 9.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| License conflicts (AGPL) | Medium | High | Audit BillionMail, OpenViking, useSend, maxun for AGPL obligations |
| Community abandonment | Low | Medium | Choose repos with >10K stars and active maintenance |
| Stack fragmentation | Medium | Medium | Limit to Go + TypeScript + Python (already in stack) |
| Security vulnerabilities | Medium | High | Run strix scans, monitor CVE databases, update regularly |
| Vendor lock-in | Low | High | All recommended repos are open-source with permissive licenses |
| Operational complexity | High | Medium | Phase adoption: Sprint 0 = 5 repos, Sprint 1 = 5 more, etc. |

### 9.5 Total Adoption Summary

| Priority | Count | Repositories |
|----------|-------|-------------|
| P0 (Install Immediately) | 5 | supabase, postgres, agent-skills, crawl4ai, trigger.dev |
| P1 (Strong Candidate) | 8 | langchain, dify, beads, openviking, codegraph, agentmemory, coolify, openhands |
| P2 (Pilot First) | 12 | cline, aider, BillionMail, useSend, turbovec, agent-reach, openfang, ralph, strix, code-review-graph, semble, OpenSandbox |
| P3 (Nice to Have) | 15 | whisper, milvus, ClickHouse, AppFlowy, vibe-kanban, routa, gitagent, directus, PM-Skills, codeflow, SuperClaude, CAI, sql-tap, page-agent, taste-skill |
| P4 (Reject) | 22 | AionUiq1 (404), Kronos, opensquilla, autoskills, subagents, skills-eval, easy-vibe, awesome-llm-apps, ai-engineering, Personal_AI, vibe-coding-template, gitagent, open-lovable, shardingsphere, pocketbase, directus, AppFlowy, astrid, openfang, code-review-graph, impeccable, turbovec |

**Net Result:** 25 repositories adopted (5 P0 + 8 P1 + 12 P2), 15 evaluated for later phases (P3), 22 rejected (P4).

---

*Document generated: June 7, 2026*
*Architecture reference: Phase 3 Agentic SDLC Operating Model + Phase 4 Runtime Specifications*
*Evaluation criteria: Architecture Fit, Security, Maintainability, Community Strength, Documentation Quality, CRM Relevance, Agentic SDLC Relevance, Scalability, Production Readiness*
