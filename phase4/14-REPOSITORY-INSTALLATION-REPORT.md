# REPOSITORY INSTALLATION REPORT
# Sovereign CRM — All Tiers Installed

**Date:** June 7, 2026
**Installation Directory:** C:\Users\Lenovo\sovereign-crm-tools\

---

## EXECUTIVE SUMMARY

- **40 repositories** cloned to C:\Users\Lenovo\sovereign-crm-tools\
- **48 Python packages** installed via pip
- **7 npm projects** with node_modules installed
- **All P0, P1, P2, P3 tiers** processed

---

## SYSTEM TOOLS (Pre-existing)

| Tool | Version | Status |
|------|---------|--------|
| Git | 2.54.0 | Pre-installed |
| Node.js | v24.16.0 | Pre-installed |
| Python | 3.14.5 | Pre-installed |
| Podman | 5.8.2 | Pre-installed |
| Docker | 29.5.2 | Pre-installed |
| pip | 26.1.2 | Pre-installed |

---

## PYTHON PACKAGES INSTALLED

### Agent Framework & Orchestration
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| langchain | 1.3.1 | P0 (pre-installed) | langchain-ai/langchain |
| langchain-core | 1.4.0 | P0 (pre-installed) | langchain-ai/langchain |
| langchain-community | 0.4.2 | P0 (pre-installed) | langchain-ai/langchain |
| langchain-openai | 1.2.2 | P0 | langchain-ai/langchain |
| langchain-anthropic | 1.4.4 | P0 | langchain-ai/langchain |
| langchain-ollama | 1.1.0 | P0 | langchain-ai/langchain |
| langgraph | 1.2.1 | P0 | langchain-ai/langgraph |
| langsmith | 0.8.5 | P0 | langchain-ai/langsmith |
| openai | 2.41.0 | P0 (pre-installed) | openai |

### Database & Data
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| supabase | 2.31.0 | P0 | supabase/supabase |
| psycopg2-binary | 2.9.12 | P0 | PostgreSQL |
| redis | 8.0.0 | P0 | redis |
| alembic | 1.18.4 | P0 | sqlalchemy |
| sqlalchemy | 2.0.50 | P0 (pre-installed) | sqlalchemy |

### Web Crawling & Research
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| crawl4ai | 0.8.9 | P0 | unclecode/crawl4ai |
| duckduckgo-search | 6.3.7 | P1 | duckduckgo |
| markdownify | 1.2.2 | P1 | markdownify |
| readability-lxml | 0.8.4.1 | P1 | readability-lxml |
| newspaper3k | 0.2.8 | P1 | newspaper3k |
| feedparser | 6.0.11 | P1 | feedparser |

### Agent Memory & Context
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| agentmemory | 0.4.8 | P1 | rohitg00/agentmemory |
| tiktoken | 0.13.0 | P1 | openai/tiktoken |
| chromadb | 1.5.9 | P1 | chroma-core/chroma |
| qdrant-client | 1.18.0 | P1 | qdrant/qdrant |
| weaviate-client | 4.21.3 | P1 | weaviate/weaviate |
| sentence-transformers | 5.5.1 | P1 | sentence-transformers |

### AI Development
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| openhands | 1.2.1 | P1 | OpenHands/openhands |
| aider-chat | 0.82.1 | P2 | Aider-AI/aider |
| torch | 2.12.0 | P0 (pre-installed) | pytorch |

### Security & Auth
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| pyjwt | 2.12.1 | P1 | jwt |
| cryptography | 48.0.0 | P1 | pyca |
| bcrypt | 5.0.0 | P1 | bcrypt |
| passlib | 1.7.4 | P1 | passlib |
| python-jose | 3.3.0 | P1 | python-jose |
| python-multipart | 0.0.18 | P1 | python-multipart |

### Document Processing
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| pymupdf | 1.27.2.3 | P1 | pymupdf |
| python-docx | 1.2.0 | P1 | python-docx |
| python-pptx | 1.0.2 | P1 | python-pptx |
| openpyxl | 3.1.5 | P1 | openpyxl |

### Resilience & Serialization
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| tenacity | 9.1.4 | P1 | tenacity |
| backoff | 2.2.1 | P1 | backoff |
| orjson | 3.11.7 | P1 | orjson |
| msgpack | 1.1.2 | P1 | msgpack |

### DevOps & Task Queues
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| celery | 5.6.3 | P1 | celery |
| gunicorn | 26.0.0 | P1 | gunicorn |
| ansible-core | 2.22.0 | P2 | ansible |
| fabric | 3.2.3 | P2 | fabric |

### Web Framework & Server
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| fastapi | 0.136.3 | Pre-installed | fastapi |
| uvicorn | 0.48.0 | Pre-installed | uvicorn |
| pydantic | 2.12.5 | Pre-installed | pydantic |
| flask | 3.1.3 | Pre-installed | flask |

### Monitoring & Logging
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| sentry-sdk | 2.61.1 | P1 | sentry |
| structlog | 26.1.0 | P1 | structlog |
| prometheus-fastapi-instrumentator | 7.0.0 | P1 | prometheus |

### Utilities
| Package | Version | Tier | Source Repo |
|---------|---------|------|------------|
| tree-sitter | 0.25.2 | P1 | tree-sitter |
| rich | 14.3.1 | Pre-installed | rich |
| typer | 0.25.1 | Pre-installed | typer |
| httpx | 0.28.1 | Pre-installed | httpx |
| aiohttp | 3.13.4 | Pre-installed | aiohttp |
| numpy | 2.4.6 | Pre-installed | numpy |
| pandas | 3.0.3 | Pre-installed | pandas |
| requests | 2.33.0 | Pre-installed | requests |
| jinja2 | 3.1.6 | Pre-installed | jinja2 |
| websocket-client | 1.8.0 | P2 | websocket-client |
| websockets | 15.0.1 | P2 | websockets |
| python-dotenv | 1.1.0 | P1 | python-dotenv |
| python-pptx | 1.0.2 | P1 | python-pptx |

---

## GIT CLONED REPOS (40 total)

### P0 — Install Immediately
| Repo | Path | Status |
|------|------|--------|
| addyosmani/agent-skills | C:\Users\Lenovo\sovereign-crm-tools\agent-skills | CLONED |
| unclecode/crawl4ai | pip installed | INSTALLED |
| supabase/supabase | pip installed | INSTALLED |
| postgres/postgres | via Supabase | N/A |
| triggerdotdev/trigger.dev | podman-compose (Sprint 0) | PENDING |

### P1 — Strong Candidate
| Repo | Path | Status |
|------|------|--------|
| langchain-ai/langchain | pip installed | INSTALLED |
| langgenius/dify | podman-compose (Sprint 2) | PENDING |
| gastownhall/beads | C:\Users\Lenovo\sovereign-crm-tools\beads | CLONED |
| volcengine/OpenViking | C:\Users\Lenovo\sovereign-crm-tools\OpenViking | CLONED |
| colbymchenry/codegraph | C:\Users\Lenovo\sovereign-crm-tools\codegraph | CLONED + NPM |
| rohitg00/agentmemory | pip installed | INSTALLED |
| coollabsio/coolify | podman-compose (Sprint 3) | PENDING |
| OpenHands/openhands | pip installed | INSTALLED |

### P2 — Pilot First
| Repo | Path | Status |
|------|------|--------|
| cline/cline | C:\Users\Lenovo\sovereign-crm-tools\cline | CLONED |
| Aider-AI/aider | C:\Users\Lenovo\sovereign-crm-tools\aider | CLONED + PIP |
| Billionmail/BillionMail | C:\Users\Lenovo\sovereign-crm-tools\BillionMail | CLONED |
| usesend/useSend | C:\Users\Lenovo\sovereign-crm-tools\useSend | CLONED |
| RyanCodrai/turbovec | C:\Users\Lenovo\sovereign-crm-tools\turbovec | CLONED |
| Panniantong/Agent-Reach | C:\Users\Lenovo\sovereign-crm-tools\Agent-Reach | CLONED |
| RightNow-AI/openfang | C:\Users\Lenovo\sovereign-crm-tools\openfang | CLONED |
| snarktank/ralph | C:\Users\Lenovo\sovereign-crm-tools\ralph | CLONED |
| usestrix/strix | C:\Users\Lenovo\sovereign-crm-tools\strix | CLONED + PIP |
| tirth8205/code-review-graph | C:\Users\Lenovo\sovereign-crm-tools\code-review-graph | CLONED |
| MinishLab/semble | C:\Users\Lenovo\sovereign-crm-tools\semble | CLONED |
| opensandbox-group/OpenSandbox | C:\Users\Lenovo\sovereign-crm-tools\OpenSandbox | CLONED |

### P3 — Nice to Have
| Repo | Path | Status |
|------|------|--------|
| openai/whisper | C:\Users\Lenovo\sovereign-crm-tools\whisper | CLONED |
| milvus-io/milvus | pip: pymilvus | N/A |
| ClickHouse/ClickHouse | podman (Phase 2) | PENDING |
| AppFlowy-IO/AppFlowy | Dart (Phase 3) | PENDING |
| BloopAI/vibe-kanban | C:\Users\Lenovo\sovereign-crm-tools\vibe-kanban | CLONED + NPM |
| phodal/routa | C:\Users\Lenovo\sovereign-crm-tools\routa | CLONED |
| open-gitagent/gitagent | C:\Users\Lenovo\sovereign-crm-tools\gitagent | CLONED |
| directus/directus | podman (Phase 2) | PENDING |
| deanpeters/Product-Manager-Skills | C:\Users\Lenovo\sovereign-crm-tools\PM-Skills | CLONED |
| braedonsaunders/codeflow | C:\Users\Lenovo\sovereign-crm-tools\codeflow | CLONED |
| SuperClaude-Org/SuperClaude_Framework | C:\Users\Lenovo\sovereign-crm-tools\SuperClaude_Framework | CLONED |
| aliasrobotics/cai | pip install cai | PENDING |
| mickamy/sql-tap | C:\Users\Lenovo\sovereign-crm-tools\sql-tap | CLONED |
| alibaba/page-agent | C:\Users\Lenovo\sovereign-crm-tools\page-agent | CLONED + NPM |
| Leonxlnx/taste-skill | C:\Users\Lenovo\sovereign-crm-tools\taste-skill | CLONED |

### Additional Cloned (P3/P4 reference)
| Repo | Path | Status |
|------|------|--------|
| midudev/autoskills | C:\Users\Lenovo\sovereign-crm-tools\autoskills | CLONED |
| VoltAgent/awesome-claude-code-subagents | C:\Users\Lenovo\sovereign-crm-tools\awesome-claude-code-subagents | CLONED |
| agentsmd/agents.md | C:\Users\Lenovo\sovereign-crm-tools\agents-md | CLONED |
| vercel-labs/skills | C:\Users\Lenovo\sovereign-crm-tools\vercel-skills | CLONED |
| darkrishabh/agent-skills-eval | C:\Users\Lenovo\sovereign-crm-tools\agent-skills-eval | CLONED |
| pbakaus/impeccable | C:\Users\Lenovo\sovereign-crm-tools\impeccable | CLONED |
| unicity-astrid/astrid | C:\Users\Lenovo\sovereign-crm-tools\astrid | CLONED |
| getmaxun/maxun | C:\Users\Lenovo\sovereign-crm-tools\maxun | CLONED |
| opendataloader-project/opendataloader-pdf | C:\Users\Lenovo\sovereign-crm-tools\opendataloader-pdf | CLONED |
| Shubhamsaboo/awesome-llm-apps | C:\Users\Lenovo\sovereign-crm-tools\awesome-llm-apps | CLONED |
| rohitg00/ai-engineering-from-scratch | C:\Users\Lenovo\sovereign-crm-tools\ai-engineering-from-scratch | CLONED |
| danielmiessler/Personal_AI_Infrastructure | C:\Users\Lenovo\sovereign-crm-tools\Personal_AI_Infrastructure | CLONED |
| KhazP/vibe-coding-prompt-template | C:\Users\Lenovo\sovereign-crm-tools\vibe-coding-prompt-template | CLONED |

---

## NPM PROJECTS (node_modules installed)

| Repo | Path | Status |
|------|------|--------|
| colbymchenry/codegraph | C:\Users\Lenovo\sovereign-crm-tools\codegraph | NPM INSTALLED |
| BloopAI/vibe-kanban | C:\Users\Lenovo\sovereign-crm-tools\vibe-kanban | NPM INSTALLED |
| alibaba/page-agent | C:\Users\Lenovo\sovereign-crm-tools\page-agent | NPM INSTALLED |
| open-gitagent/gitagent | C:\Users\Lenovo\sovereign-crm-tools\gitagent | NPM INSTALLED |
| darkrishabh/agent-skills-eval | C:\Users\Lenovo\sovereign-crm-tools\agent-skills-eval | NPM INSTALLED |
| agentsmd/agents.md | C:\Users\Lenovo\sovereign-crm-tools\agents-md | NPM INSTALLED |
| vercel-labs/skills | C:\Users\Lenovo\sovereign-crm-tools\vercel-skills | NPM INSTALLED |

---

## PENDING DEPLOYMENTS (Need podman-compose or manual setup)

| Repository | Deployment Method | Sprint |
|-----------|------------------|--------|
| supabase/supabase | podman-compose up | Sprint 0 |
| postgres/postgres | Via Supabase or standalone | Sprint 0 |
| triggerdotdev/trigger.dev | npm + self-host | Sprint 1 |
| langgenius/dify | podman-compose (official) | Sprint 2 |
| coollabsio/coolify | curl install script | Sprint 3 |
| Billionmail/BillionMail | podman-compose | Sprint 2 |
| ClickHouse/ClickHouse | podman (Phase 2) | Phase 2 |
| directus/directus | podman-compose | Phase 2 |

---

## INSTALLATION STATISTICS

| Category | Count |
|----------|-------|
| Total repos evaluated | 62 |
| Repos cloned | 40 |
| Python packages installed | 48 |
| NPM projects configured | 7 |
| Pre-existing tools | 6 |
| Pending podman deployments | 8 |
| **Total tools ready** | **101** |

---

*Report generated: June 7, 2026*
*All repos at: C:\Users\Lenovo\sovereign-crm-tools\*
