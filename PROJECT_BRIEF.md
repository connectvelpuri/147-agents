# Sovereign CRM (RevOS) — Complete Project Blueprint

**Document Type:** Master Project Brief & Session Log
**Created:** 2026-06-06 16:04
**Location:** Sovereign Vault (INTERNAL — NOT FOR GIT PUSH)

---

## 1. PROJECT IDENTITY

**Name:** Sovereign CRM (Brand: RevOS — Revenue Operating System)
**Vision:** A local-first, open-source alternative to Salesforce, HubSpot, Zoho, LeadSquared
**Target Verticals:** IT Services & Consulting | SaaS Companies
**Philosophy:** "The best of all worlds"
- Power: Salesforce depth and customization
- UX: HubSpot intuitive, consumer-grade feel
- Modularity: Zoho "build-your-own" flexibility
- Velocity: LeadSquared high-volume lead capture speed

---

## 2. THE 4 MOATS (Competitive Advantages)

| # | Moat | Technology |
|---|------|-----------|
| 1 | Zero Latency | CRDTs (Automerge/Yjs/Go-native) — UI updates instantly, syncs async |
| 2 | Absolute Privacy | Self-hosted + Ollama local LLMs — data never leaves client hardware |
| 3 | Infinite Extensibility | Metadata-driven Dynamic Object Builder — define entities at runtime |
| 4 | Zero Cost Core | AGPL v3 — $0 licensing for self-hosted core |

---

## 3. INVISIBLE VARIABLES (Enterprise Layer)

### Data Governance
- Duplicate merge engine with intelligent resolution
- Master Data Management (MDM) — single source of truth
- Full audit trail via event-sourced CRDTs
- Data quality scoring and enforcement

### Sovereign Admin
- Sandbox environments for configuration testing
- Low-code formula engine for calculated fields
- Delegated administration — admins control their org without platform access
- Configuration versioning and rollback

### Agentic AI via MCP
- AI CRM Administrator — executes tasks, not just summarizes
- BYO-LLM via MCP (Ollama local, or any provider)
- AI workflow builder, AI report builder, AI sales coach
- No vendor lock-in for AI

### Connectivity
- API-first / Headless design
- CRM is a data hub first, UI is secondary
- Webhook framework, REST APIs, GraphQL
- Connector architecture for legacy systems

---

## 4. STRICT FOLDER SEPARATION

| Path | Purpose | Git Push? |
|------|---------|-----------|
| `C:\Users\Lenovo\sovereign_crm_vault\` | Strategy, blueprints, research, architecture docs, all planning artifacts | **NEVER** |
| `C:\Users\Lenovo\dev\sovereign-crm\` | Source code: Go backend, Next.js, Docker, deploy scripts | **YES — to GitHub** |

---

## 5. ARCHITECTURE DECISIONS

### 5.1 One Unified Platform + 2 Starter Templates
- **Decision:** Single metadata-driven platform with Dynamic Object Builder
- **Why:** Two separate CRMs = 2x bugs, 2x maintenance. One platform = lower risk, higher productivity
- **Templates:** IT Consulting (Projects, SOWs, Time) + SaaS (Subscriptions, MRR, Churn)

### 5.2 MVP Scope
- Leads -> Contacts -> Organizations
- Pipeline (Deals, Stages, Probabilities, Forecasting)
- Activities (Calls, Emails, Meetings, Tasks, Notes)
- Calendar sync
- Users + Roles + Permissions (RBAC)
- Reporting (pipeline value, conversion, activity metrics)
- Global search
- **Dynamic Object Builder (THE MOAT)**

### 5.3 Greenfield + Import Framework
- Cleanest data model possible — no legacy baggage
- Import framework with mapping UI, validation, rollback, audit
- Competitors' pain point #1: migrating OUT of Salesforce is impossible. We make it easy.

### 5.4 Single-Tenant Self-Hosted (Multi-Tenant Ready)
- Docker Compose for MVP
- Every query carries tenant_id from day one
- Single-tenant = absolute privacy (the moat)
- Multi-tenant routing layer can be added later without refactoring

### 5.5 Architecture Principles
- CRDT local-first for zero latency
- Event-sourced for full audit trail
- Metadata-driven for infinite extensibility
- MCP-native for AI integration
- Tenant-partitioned Postgres (BRIN/GIN indexes) for dense data performance

---

## 6. DUAL-CYCLE UPGRADE PROCESS

**Morning Scan (6 AM):** X (Twitter), GitHub trending, YouTube
**Evening Synthesis (6 PM):** Log in CAPABILITY_EVOLUTION.md, update blueprints

### Completed Scans
- **2026-06-06 Morning:** GitHub — CRDT (ygo, go-ds-crdt, yorkie) + MCP (mcp-golang, go-mcp, toolhive)
- **2026-06-06 Evening:** Pending

---

## 7. TECHNOLOGY DECISIONS

### Installed
- **headroom-ai v0.22.4** (npm global) — token compression, 60-95% fewer tokens

### Selected Stack
| Layer | Choice | Notes |
|-------|--------|-------|
| Backend | Go | Selected |
| Frontend | Next.js + TypeScript | Selected |
| Database | Postgres 16 | Selected |
| CRDT Sync | ygo (Deln0r/ygo) | Pure-Go Yjs port, wire-compatible |
| MCP Server | metoro-io/mcp-golang (1,223 stars) | Simplest Go MCP server |
| Container | Docker + Docker Compose | Selected |
| Auth | TBD | Pending research |
| Search | TBD | Pending research |

---

## 8. SPRINT ROADMAP

| Sprint | Weeks | Focus |
|--------|-------|-------|
| Planning | 1-2 | Complete all 15 blueprint phases in vault |
| Sprint 1 | 3-4 | Core platform: Go API, Postgres schema, Auth, CRDT foundation, Dynamic Object Builder schema |
| Sprint 2 | 5-6 | Objects & UI: Lead/Contact/Organization CRUD, Next.js, Dynamic Object Builder runtime, RBAC |
| Sprint 3 | 7-8 | Pipeline & Activities: Deals, Stages, Forecasting, Activities, Calendar sync |
| Sprint 4 | 9-10 | Reporting & Search: Reporting engine, Dashboard builder, Global search, Export |
| Sprint 5 | 11-12 | Integrations & Launch: Email, Webhooks, MCP/Ollama AI, Import framework, Docs |

---

## 9. COMPETITIVE SCORECARD

| CRM | Score | Our Advantage |
|-----|-------|---------------|
| Salesforce | 6.2/10 | Speed, cost, simplicity, no lock-in |
| HubSpot | 7.0/10 | Open source, no tier gating, unlimited customization |
| Zoho | 6.5/10 | Cohesive UX, modern architecture |
| LeadSquared | 5.5/10 | IT Consulting/SaaS vertical depth |

---

## 10. EXECUTIVE DIRECTIVES

1. Vault stays private. Forever.
2. Source code stays in the repo.
3. Research first. Code second.
4. Dual-cycle scans run daily.
5. Zero latency is non-negotiable.
6. Privacy is the #1 moat.
7. The Dynamic Object Builder is the differentiator.
8. MCP-native AI — no vendor lock-in.
9. Data belongs to the customer, not the platform.
10. Right, not rushed.

---

*Document maintained by Hermes Agent. Never push to Git.*
