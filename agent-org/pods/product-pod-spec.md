# PRODUCT PODS

**Version:** 1.0

---

## Standard Pod Composition
- Pod Lead (Delivery Manager) — sprint planning, blockers, status
- Product Manager — requirements, acceptance criteria, scope
- Engineering Manager — code quality, capacity, mentoring
- Senior Engineer(s) — implementation, code review, tech docs
- QA Lead / Senior QA — test strategy, execution, quality gates
- UX Designer — wireframes, flows, design system compliance
- DevOps Lead (shared) — CI/CD, deployment
- Security Engineer (shared) — threat modeling, security review
- Specialists (as needed) — Data Engineer, AI Engineer, etc.

## Sovereign CRM Pod Structure

### Pod 1: Core CRM
Features: Contacts, Orgs, Deals, Activities, Search
Moats: CRDT Sync, Dynamic Object Builder

### Pod 2: AI & Intelligence
Features: AI Copilot, Lead Scoring, Email Intelligence, Forecasting
Moats: AI Copilot, MCP Server

### Pod 3: Platform & Infrastructure
Features: CI/CD, Monitoring, Security, Deployment, Performance
Moats: Self-hosted deployment, IaC

### Pod 4: Product Experience
Features: Dashboard Builder, Mobile App, Design System, UX
Moats: Dashboard Builder, Mobile App

### Pod 5: Integrations & Data
Features: Email, Calendar, Import/Export, Data Pipelines, Analytics
Moats: Data pipelines, Event streaming

## Operating Rules
- Pod Lead owns delivery; PM owns scope; Eng Manager owns quality
- Daily sync 15 min; 2-week sprints
- Shared resources scheduled by PMO Director
- Pod > 9 members = split into two pods
- Cross-pod dependencies tracked in RAID log
