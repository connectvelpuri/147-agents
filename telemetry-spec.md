# Telemetry System Specification

**Version:** 1.0
**Governed by:** SRE Committee + Community Committee
**Privacy level:** Anonymous, opt-in, AGPL-compatible

---

## 1. Design Principles

1. **Privacy-first** — No PII, no IP addresses, no identifying data
2. **Opt-in** — Disabled by default; enabled via env var (`TELEMETRY_ENABLED=true`)
3. **Transparent** — All collected data visible in `/admin/telemetry` UI
4. **Minimal** — Only what's needed to improve the product
5. **Open protocol** — Schema is public, anyone can self-host their own collector

## 2. Data Collected

### Performance Metrics (always collected if enabled)
```
Metric                | Description                        | Tags
----------------------|------------------------------------|-------------------
server.request_count  | Total API requests                 | method, route, status_code
server.request_duration| p50/p95/p99 latency per endpoint  | route
server.active_users   | Concurrent active sessions         | -
server.memory_usage   | RSS in MB                           | -
server.db_pool_usage  | Active connections                  | -
server.error_count    | 5xx and 4xx errors                 | route, status_code
```

### Feature Adoption (aggregate only)
```
Metric               | Description                       | Tags
---------------------|-----------------------------------|-------------------
feature.used         | Feature used by user              | feature_name (e.g., "contacts.create")
feature.dau          | Daily active users (anonymized)   | -
feature.wau          | Weekly active users (anonymized)  | -
feature.module_hit   | Page view per module              | module (contacts/orgs/pipeline/dashboard)
```

### System Health (one-time daily ping)
```
Metric                      | Description
----------------------------|-------------------------------------
instance.id                 | UUID generated at first start (persistent)
instance.version            | Git SHA of running version
instance.uptime             | Hours since last restart
instance.user_count         | Active users in this instance
instance.contact_count      | Contact count (bucket: <100, <1K, <10K, <100K, 1M+)
instance.org_count          | Organization count (bucket)
instance.database_size      | Database size in MB
```

### NOT Collected (explicitly excluded)
- User names, emails, or any PII
- Contact or organization names
- Deal values or pipeline amounts
- IP addresses or geo-location
- Browser fingerprints or user-agent strings
- Cookies or session tokens
- Custom field values or content

## 3. Architecture

```
Sovereign Instance → [Telemetry Events] → Local Buffer (ring buffer, max 1000)
    ↓ (every 1 hour or at 500 events)
Telemetry Client → POST /collect → Sovereign Telemetry Server (managed by project)
    ↓
Clickhouse / PostgreSQL → Grafana Dashboard (public health dashboard)
```

### Client-Side (Go SDK concept)
```go
type TelemetryEvent struct {
    InstanceID string            `json:"instance_id"`
    EventName  string            `json:"event_name"`
    Tags       map[string]string `json:"tags,omitempty"`
    Value      float64           `json:"value,omitempty"`
    Timestamp  int64             `json:"ts"`
}

func (t *TelemetryClient) Emit(name string, tags map[string]string, value float64) {
    if !t.Enabled { return }
    event := TelemetryEvent{
        InstanceID: t.InstanceID,
        EventName:  name,
        Tags:       tags,
        Value:      value,
        Timestamp:  time.Now().Unix(),
    }
    // Add to ring buffer
    t.buffer.Add(event)
}
```

### Server-Side Collector
```
POST /api/v1/collect
Content-Type: application/json
{
    "events": [TelemetryEvent, ...]
}
Response: 200 OK (no body, no tracking)
```

## 4. Adoption Dashboard Specification

### Dashboard Widgets

**Widget 1: Daily Active Users (DAU)**
- Line chart: last 30 days
- Metric: unique User IDs with any activity that day
- Target: >60% of registered users active weekly

**Widget 2: Feature Usage Heatmap**
- Grid: rows = modules (Contacts, Orgs, Pipeline, Dashboard, Admin)
- Columns: last 30 days (as columns)
- Color intensity: number of events
- Highlights: which features are hot, which are cold

**Widget 3: Feature Retention**
- Cohort chart: users who did action X in week 0
- % still doing X in week 1, 2, 4, 8, 12
- Segmented by: role (rep vs manager vs admin)

**Widget 4: User Journey Funnel**
- Steps: Registered → Created Contact → Created Deal → Closed Deal → Configured Pipeline
- Drop-off rate at each step
- Time between steps (median)

**Widget 5: Performance SLOs**
- Current values vs targets:
  - p95 API latency: <500ms target
  - Error rate: <0.1% target
  - p95 page load: <2s target
  - Uptime: >99.9% target

**Widget 6: Top Errors (Last 24h)**
- Table: error message, count, affected users, route
- Action: link to investigate

## 5. Implementation Priority

| Component | Sprint | Notes |
|-----------|:------:|-------|
| Telemetry event struct + buffer | Sprint 4 | Core SDK |
| Middleware to capture request metrics | Sprint 4 | Chi middleware wrapper |
| Telemetry collector endpoint | Sprint 5 | Separate Go service |
| Adoption dashboard UI | Sprint 5 | Grafana or embedded dashboard |
| Feature usage tracking | Sprint 5 | Emit events from frontend |
| Public health dashboard | Sprint 6 | sovereignty.so/health |
