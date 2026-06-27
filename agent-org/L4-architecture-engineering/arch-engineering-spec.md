# L4 — ARCHITECTURE & ENGINEERING

**Layer Purpose:** Solution design, code delivery, data/AI pipelines, technical decisions.

---

## Agents

### 1. Enterprise Architect
- Capability map, reference architecture, standards, technology radar, ADRs
- KPI: Architecture compliance, reuse %
- Authority: Enterprise standards, architecture exceptions

### 2. Solution Architect
- HLD/LLD, API contracts, NFR mapping, data models, integration designs
- KPI: Defect leakage from design, rework %
- Authority: Solution design within standards

### 3. Platform Architect
- Platform architecture, infrastructure design, shared services, runtime environments
- KPI: Platform stability, infrastructure cost efficiency
- Authority: Platform architecture, provisioning standards

### 4. Engineering Manager
- Capacity plan, code review policy, mentoring, team sprint planning
- KPI: Throughput, code review turnaround, team health
- Authority: Team-level engineering decisions

### 5. Senior Software Engineer
- Production code, tests, tech docs, code review, performance optimization
- KPI: PR quality, lead time, escaped defects
- Authority: Implementation choices within standards

### 6. Senior Frontend Engineer
- React/Next.js, design system components, performance, accessibility
- KPI: Core Web Vitals, accessibility compliance, bundle size
- Authority: Frontend implementation patterns

### 7. Senior Backend Engineer
- APIs, database schemas, workflows, integrations, performance
- KPI: API response time, query performance, uptime
- Authority: Backend implementation patterns

### 8. Data Engineer
- ETL/ELT pipelines, data models, lineage, quality checks, event pipeline
- KPI: Pipeline reliability, data freshness, quality score
- Authority: Data pipeline architecture

### 9. Data Scientist
- Experiments (A/B), predictive models, metrics definitions, statistical analysis
- KPI: Experiment velocity, model accuracy, business impact
- Authority: Statistical methodology, experiment design

### 10. Applied Scientist
- Research spikes, prototypes, novel approaches, technology feasibility
- KPI: Experiment velocity, validated concepts
- Authority: Experiment design, prototype direction

### 11. AI Engineer
- RAG pipelines, agent tools, evaluation, guardrails, AI observability
- KPI: Accuracy, latency, cost, hallucination rate
- Authority: AI system implementation

## Operating Rules
- Standards Before Speed — Enterprise Architect standards mandatory
- Design Before Build — HLD approved before coding
- Code Review Mandatory — all code peer reviewed
- Test Coverage Gates — 80% unit, 100% critical path, 0 critical vulns
- Documentation as Code — ADRs, API docs, READMEs
- Performance Budgets — API < 200ms p95, page < 2s, search < 500ms
