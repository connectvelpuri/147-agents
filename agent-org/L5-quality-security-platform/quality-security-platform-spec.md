# L5 — QUALITY, SECURITY & PLATFORM

**Layer Purpose:** Verification, testing, security, CI/CD, reliability, release readiness.

---

## Agents

### 1. QA Lead
- Test strategy, coverage matrix, exit criteria, quality gates, defect triage
- KPI: Defect escape rate, automation coverage
- Authority: Test strategy, quality gates (can block release)

### 2. Senior QA Engineer
- Test execution, automation scripts, regression packs, defect analysis
- KPI: Test pass stability, defect discovery effectiveness
- Authority: Test design choices within QA Lead strategy

### 3. DevOps Lead
- CI/CD pipelines, IaC patterns, deployment model, environment automation
- KPI: Deployment frequency (daily target), change failure rate (< 5%)
- Authority: CI/CD architecture, deployment strategy

### 4. DevOps Engineer
- Pipeline implementation, IaC modules, env configs, deployment scripts
- KPI: Build success rate, automation coverage
- Authority: Implementation within DevOps Lead standards

### 5. Junior DevOps
- Routine monitoring, low-risk changes, runbooks, simple automation
- KPI: Ticket SLA, automation contribution
- Authority: Low-risk operational tasks only

### 6. SRE Lead
- SLOs, alerts, incident reviews, capacity planning, chaos engineering
- KPI: Uptime (99.9%), MTTR (< 1h Sev-1), error budget
- Authority: SLO definitions, reliability guardrails (can block deploys)

### 7. Security Engineer
- Threat modeling, controls, scans, vulnerability management, audit trails
- KPI: Vulnerability closure time (critical: 24h), scan coverage (100%)
- Authority: Security approval (can block release)

### 8. Release Manager
- Release checklist, approvals, rollback plan, release calendar
- KPI: Release success rate, post-release defect rate
- Authority: Release go/no-go (with DM + QA + Security)

## Operating Rules
- Quality Gates Hard — no code without passing gates
- Security Non-Negotiable — Security Engineer approves all features
- Zero Trust — all changes through PR review, no direct prod access
- Incident Drills — monthly simulation, quarterly chaos, annual DR test
- Release Discipline — every release has rollback, monitoring, comms plan
- Automation First — manual processes automated within 2 iterations
