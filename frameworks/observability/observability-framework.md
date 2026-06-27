# SOVEREIGN CRM — OBSERVABILITY & MONITORING FRAMEWORK
# Version: 2.0 | Target Maturity: 9.5/10

---

## 1. OBSERVABILITY STACK

### Recommended: Grafana Open-Source Stack

| Signal | Tool | Purpose |
|--------|------|---------|
| Metrics | Prometheus | Pull-based metrics collection via /metrics endpoints |
| Logs | Loki | Log aggregation without full-text indexing (label-based) |
| Traces | Tempo | Distributed tracing (Jaeger, Zipkin, OTLP formats) |
| Visualization | Grafana | Unified dashboards, alerting, exploration |
| Collection | OpenTelemetry Collector | Vendor-neutral telemetry pipeline |
| Go Backend | OTel Go SDK | Auto-instrumentation for Go |
| Frontend | @vercel/otel | Next.js tracing and RUM |
| Database | postgres_exporter | PostgreSQL metrics to Prometheus |
| On-Call | Grafana OnCall | Escalation, rotation, alerting |
| Status Page | Atlassian Statuspage | Public/system status communication |

### Alternative Managed Options
- Datadog: All-in-one, excellent Go support, $23+/host/month
- New Relic: Generous free tier (100GB/month), full-stack
- Grafana Cloud: Managed version of open-source stack
- Honeycomb: Best-in-class for trace-based debugging

---

## 2. SLO/SLI FRAMEWORK

### Four Golden Signals (Google SRE)

Every service dashboard shows these at the top:
1. **Latency:** Time to service a request (p50, p95, p99)
2. **Traffic:** Demand on the system (requests/sec)
3. **Errors:** Rate of failed requests (5xx, 4xx)
4. **Saturation:** How "full" the system is (CPU, memory, connections)

### Service-Level Objectives

| Service | SLI | SLO Target | Error Budget (30d) |
|---------|-----|------------|-------------------|
| Go Backend API | Availability: successful requests / total requests | >= 99.9% | ~43.8 min downtime |
| Go Backend API | Latency: p95 response time | <= 200ms | — |
| Go Backend API | Throughput: requests per second | Baseline + 10x | — |
| Next.js Frontend | Availability: successful page loads / total | >= 99.95% | ~21.9 min downtime |
| Next.js Frontend | Performance: LCP at p95 | <= 2.5s | — |
| PostgreSQL | Availability: successful queries / total | >= 99.99% | ~4.3 min downtime |
| PostgreSQL | Latency: p95 query time | <= 100ms | — |
| Ollama LLM | Availability: successful inferences / total | >= 99.5% | ~3.6 hours downtime |
| Ollama LLM | Latency: p95 inference time | <= 5s | — |
| MCP Server | Availability: successful tool calls / total | >= 99.9% | ~43.8 min downtime |
| MCP Server | Latency: p95 tool execution | <= 500ms | — |

### Error Budget Policy

| Error Budget Remaining | Action |
|----------------------|--------|
| > 50% | Normal development, feature velocity high |
| 25-50% | Caution, increase testing rigor |
| 10-25% | Feature freeze consideration, focus on reliability |
| < 10% | Hard feature freeze, all effort on reliability |
| 0% | Complete feature freeze, emergency reliability sprint |

---

## 3. ALERTING FRAMEWORK

### Burn-Rate Alerting (Google SRE Method)

Instead of simple threshold alerts, alert on the RATE at which your error budget is being consumed.

Burn rate = actual error rate / error rate allowed by SLO

| Burn Rate | Time to Exhaust Budget | Severity | Action |
|-----------|----------------------|----------|--------|
| 14.4x | 1 hour | Critical | Page immediately |
| 6x | 6 hours | Warning | Page soon |
| 3x | 1 day | Info | Ticket, investigate |
| 1x | 30 days | Normal | Informational |

### Alert Severity Levels

| Severity | Description | Response Time | Notification |
|----------|-------------|---------------|--------------|
| Critical | Complete outage, data loss, security breach | 15 min | PagerDuty + Slack + SMS |
| Major | Major feature degraded, no workaround | 30 min | PagerDuty + Slack |
| Minor | Minor issue, workaround exists | 4 hours | Slack + ticket |
| Info | Cosmetic, monitoring, informational | Next business day | Dashboard only |

### Alert Rules (Prometheus/Grafana)

```yaml
# Burn-rate alerts for Go Backend
groups:
  - name: go-backend-slo
    rules:
      # 14.4x burn rate - 1 hour window (PAGE)
      - alert: GoBackend_ErrorBudgetBurn_1h
        expr: |
          job:http_requests_total:ratio_rate5m{job="crm-api"}
          > (14.4 * 0.001)
          and
          job:http_requests_total:ratio_rate1h{job="crm-api"}
          > (14.4 * 0.001)
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Go Backend error budget burning at 14.4x for 1h"
          runbook: "docs/runbooks/api-error-budget-burn.md"

      # 3x burn rate - 6 hour window (TICKET)
      - alert: GoBackend_ErrorBudgetBurn_6h
        expr: |
          job:http_requests_total:ratio_rate30m{job="crm-api"}
          > (3 * 0.001)
          and
          job:http_requests_total:ratio_rate6h{job="crm-api"}
          > (3 * 0.001)
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Go Backend error budget burning at 3x for 6h"

  - name: postgres-slo
    rules:
      - alert: PostgreSQL_HighQueryLatency
        expr: pg_stat_activity_query_duration_p95 > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "PostgreSQL p95 query latency exceeds 100ms"

      - alert: PostgreSQL_HighConnections
        expr: pg_stat_activity_count > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "PostgreSQL connection count exceeds 80% of max"

  - name: ollama-slo
    rules:
      - alert: Ollama_HighInferenceLatency
        expr: ollama_inference_duration_p95 > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Ollama p95 inference time exceeds 5s"

      - alert: Ollama_HighErrorRate
        expr: rate(ollama_requests_errors_total[5m]) / rate(ollama_requests_total[5m]) > 0.005
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Ollama error rate exceeds 0.5%"
```

### Alerting Best Practices
- Page on user-visible symptoms, not causes
- Every alert MUST be actionable (someone must do something)
- Every critical/warning alert MUST have a linked runbook
- Use severity levels consistently across all services
- Implement escalation policies with timeouts
- Suppress alerts during maintenance windows
- Use Alertmanager grouping to avoid alert storms
- Review alert quality monthly; delete noisy/ignored alerts
- Track MTTR (Mean Time to Recovery) and reduce over time

---

## 4. DASHBOARD FRAMEWORK

### Dashboard Hierarchy

```
Level 1: Executive Overview
  - Global health score (all SLOs pass/fail)
  - Error budget remaining per service
  - Revenue-impacting incidents count
  - Status: All systems operational / Degraded / Major Outage
  - Uptime (last 30 days)
  - MTTR (last 30 days)
  - Deployment frequency (last 30 days)

Level 2: Service Overview (one per service)
  - The Four Golden Signals for that service
  - Current SLO compliance
  - Recent deployments (last 10)
  - Active alerts
  - Error budget burn rate

Level 3: Deep Dive (per component)
  - Go Backend: goroutines, GC pause, heap, goroutine leaks, pprof
  - PostgreSQL: connections, slow queries, replication lag, bloat, WAL
  - Ollama LLM: inference latency, queue depth, model load times, VRAM
  - Next.js: SSR render time, client-side errors, Core Web Vitals, bundle size
  - MCP Server: tool call latency, tool error rate, tool usage distribution

Level 4: Debugging (on-demand, during incidents)
  - Trace explorer (find slow spans)
  - Log search (filter by trace ID)
  - Flame graphs for profiling
  - Ad-hoc queries
```

### Dashboard Design Rules
- Red/Green/Yellow color coding for at-a-glance status
- Consistent time ranges across related panels
- Avoid chartjunk (3D effects, unnecessary decorations)
- Group related metrics together with clear section headers
- Use threshold lines on graphs to show SLO targets
- Make dashboards actionable: link to runbooks, deploy pages, log search
- Keep dashboards focused; split into multiple dashboards rather than one giant one
- Use variables/templates for environment, service, and pod selection

---

## 5. LOGGING FRAMEWORK

### Structured Logging Standard

All services MUST output structured JSON logs:

```json
{
  "timestamp": "2026-06-09T14:30:00Z",
  "level": "info",
  "service": "crm-api",
  "trace_id": "abc123def456",
  "span_id": "789ghi012",
  "user_id": "user-123",
  "tenant_id": "tenant-456",
  "method": "GET",
  "path": "/api/contacts",
  "status": 200,
  "duration_ms": 45,
  "message": "Request processed successfully"
}
```

### Log Levels

| Level | When to Use | Retention |
|-------|-------------|-----------|
| ERROR | Unexpected failures requiring attention | 90 days |
| WARN | Unexpected but recoverable situations | 30 days |
| INFO | Normal business operations | 14 days |
| DEBUG | Detailed diagnostic information | 7 days |

### Log Search Examples (Loki/LogQL)

```
# Find all errors in last hour
{service="crm-api"} |= "error" | json | level="error"

# Find slow requests
{service="crm-api"} | json | duration_ms > 500

# Find errors for specific user
{service="crm-api"} | json | user_id="user-123" | level="error"

# Find all logs for a specific trace
{service="crm-api"} | json | trace_id="abc123def456"
```

---

## 6. DISTRIBUTED TRACING FRAMEWORK

### Trace Context Propagation

```
Browser → Next.js → Go Backend → PostgreSQL
         │         │             │
         └─span────┴──span───────┘
              (single trace)
```

### Instrumentation Points

| Service | Instrument | Method |
|---------|-----------|--------|
| Go Backend | HTTP handlers | OTel Go SDK auto-instrumentation |
| Go Backend | Database queries | OTel SQL driver instrumentation |
| Go Backend | External HTTP calls | OTel HTTP client instrumentation |
| Next.js | API routes | @vercel/otel |
| Next.js | Server components | @vercel/otel |
| PostgreSQL | Query execution | pg_stat_statements + postgres_exporter |

### Trace Attributes (Custom)

| Attribute | Description | Example |
|-----------|-------------|---------|
| crm.tenant_id | Multi-tenant identifier | "tenant-456" |
| crm.user_id | Authenticated user | "user-123" |
| crm.entity_type | CRM entity being accessed | "contact" |
| crm.entity_id | Specific entity identifier | "contact-789" |
| crm.operation | CRUD operation | "read" |
| crm.mcp.tool | MCP tool name (if applicable) | "list_contacts" |

---

## 7. INCIDENT MANAGEMENT FRAMEWORK

### Incident Response Process (Google SRE)

1. **VERIFY** — Confirm it's real, not a false alarm
2. **ASSESS** — Determine severity (user impact, revenue impact, scope)
3. **DECLARE** — Open incident channel, notify stakeholders
4. **ASSIGN ROLES:**
   - Incident Commander (IC): Coordinates response
   - Operations Lead: Leads technical investigation
   - Communications Lead: Updates stakeholders
5. **DIAGNOSE** — Identify root cause (not just symptoms)
6. **MITIGATE** — Apply fix or rollback (mitigate first, then fix)
7. **RESOLVE** — Confirm recovery, close incident
8. **REVIEW** — Postmortem within 48 hours (blameless)

### Incident Severity Levels

| Severity | Description | Response Time | Resolution Target | Escalation |
|----------|-------------|---------------|-------------------|------------|
| Sev-1 | Complete outage of core functionality | 15 min | 1 hour | Immediate to L1 |
| Sev-2 | Major feature degraded, no workaround | 30 min | 4 hours | L2 within 30 min |
| Sev-3 | Minor issue, workaround exists | 4 hours | 24 hours | L2 within 4 hours |
| Sev-4 | Cosmetic/minor issue | Next business day | 1 week | Standard |

### On-Call Rotation

- **Rotation:** 1 week on, 1 week off
- **Handoff:** Written handoff document at shift change
- **Escalation:** Primary → Secondary → Team Lead → Manager → L1
- **Tooling:** Grafana OnCall (open-source) or PagerDuty
- **Compensation:** Time off in lieu or on-call stipend
- **Maximum:** 2 consecutive weeks on-call (prevent burnout)

### Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date:** YYYY-MM-DD
**Severity:** Sev-X
**Duration:** X hours Y minutes
**Impact:** [Description of user/business impact]
**Author:** [Name]

## Timeline (UTC)
- HH:MM — Event description
- HH:MM — Event description

## Root Cause
[Technical explanation of what went wrong]

## What Went Well
- [Item]

## What Went Wrong
- [Item]

## Where We Got Lucky
- [Item]

## Action Items
| # | Action | Owner | Due Date | Priority | Status |
|---|--------|-------|----------|----------|--------|
| 1 | [Action] | [Name] | [Date] | [P0-P3] | Open |

## Lessons Learned
- [Key takeaway]

## Metrics
- Time to detect: X minutes
- Time to mitigate: X minutes
- Time to resolve: X hours
- Error budget consumed: X%
```

---

## 8. IMPLEMENTATION PLAN

### Phase 1: Foundation (Week 1-2)
- [ ] Set up OpenTelemetry Collector (Docker Compose)
- [ ] Set up Grafana + Prometheus + Loki + Tempo
- [ ] Enable pg_stat_statements in PostgreSQL
- [ ] Add basic Go metrics (net/http middleware with OTel)
- [ ] Add basic Next.js tracing (@vercel/otel)
- [ ] Create Level 1 dashboard (Four Golden Signals)

### Phase 2: Structured Logging (Week 3)
- [ ] Add structured JSON logging to Go backend (slog or zerolog)
- [ ] Add OpenTelemetry log bridge to export logs via OTel
- [ ] Configure Loki as log backend
- [ ] Create log-based alerts for error patterns

### Phase 3: Distributed Tracing (Week 3-4)
- [ ] Add OTel tracing to Go backend HTTP/gRPC handlers
- [ ] Add OTel tracing to PostgreSQL queries
- [ ] Add OTel tracing to Next.js API routes and server components
- [ ] Add trace context propagation between Go ↔ Next.js
- [ ] Create trace explorer dashboard in Grafana

### Phase 4: SLOs and Alerting (Week 4-5)
- [ ] Define SLIs for all services (see Section 2)
- [ ] Create Prometheus recording rules for SLI computation
- [ ] Set up burn-rate alerts in Grafana
- [ ] Configure Grafana OnCall for escalation
- [ ] Create error budget dashboard

### Phase 5: Incident Management (Week 5-6)
- [ ] Create incident runbooks for top 5 failure scenarios
- [ ] Set up incident Slack channel templates
- [ ] Configure escalation policies
- [ ] Run first on-call drill/tabletop exercise
- [ ] Set up status page (internal or public)
- [ ] Schedule first postmortem review

### Phase 6: Optimization (Ongoing)
- [ ] Tune alert thresholds based on false positive rate
- [ ] Add custom business metrics (LLM usage, conversion, etc.)
- [ ] Set up profiling (pprof) for Go backend
- [ ] Add Real User Monitoring (RUM) for frontend
- [ ] Review and refine dashboards quarterly
- [ ] Track MTTR and reduce over time

---

*Framework based on: Google SRE Book, Grafana Observability Stack, OpenTelemetry Standard, Prometheus Alerting Best Practices*
