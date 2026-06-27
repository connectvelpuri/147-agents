# Phase 13: Reporting & Analytics Architecture

**Created:** 2026-06-06
**Purpose:** Complete analytics framework — KPI tree, metric definitions, report/dashboard builder, data warehouse strategy, export pipeline.

---

## 1. METRICS FRAMEWORK

### KPI Tree (Revenue Operations)

```
REVENUE GROWTH
├── New Bookings (net new ACV)
│   ├── Pipeline Coverage Ratio (pipeline / quota)
│   ├── Win Rate (won / closed)
│   ├── Avg Deal Size
│   ├── Sales Cycle Length (days)
│   ├── Lead Conversion Rate (lead → deal)
│   └── Lead Velocity Rate (MoM growth in qualified leads)
├── Retention
│   ├── Net Revenue Retention (NRR)
│   ├── Gross Revenue Retention (GRR)
│   ├── Logo Retention Rate
│   ├── Churn Rate (monthly/quarterly/annual)
│   └── Churn Reason Breakdown
└── Expansion
    ├── Net Dollar Expansion Rate (NDR)
    ├── Upsell Rate
    ├── Cross-sell Rate
    └── Expansion Multiplier

SALES EFFICIENCY
├── Activity Metrics
│   ├── Calls per Rep per Day
│   ├── Emails Sent per Rep per Day
│   ├── Meetings per Rep per Week
│   ├── Activities per Deal
│   └── Connect Rate (calls that reached someone)
├── Funnel Metrics
│   ├── Stage Conversion Rate (Lead→MQL, MQL→SQL, etc.)
│   ├── Stage Velocity (avg days in each stage)
│   ├── Drop-off Rate per Stage
│   └── Funnel Leakage (lost at each stage)
└── Rep Metrics
    ├── Quota Attainment %
    ├── Pipeline Generated
    ├── Deals Created
    ├── Deals Closed
    └── Avg Activities per Won Deal

FINANCIAL
├── Bookings (total contract value booked)
├── Billings (invoiced amount)
├── Revenue Recognized vs Deferred
├── ARR / MRR
│   ├── New MRR
│   ├── Expansion MRR
│   ├── Contraction MRR
│   ├── Churn MRR
│   └── Reactivation MRR
├── Cash Flow (collections)
├── Sales Cost per Rep
├── CAC (Customer Acquisition Cost)
└── LTV:CAC Ratio

IT CONSULTING METRICS
├── Utilization Rate (billable hours / total hours)
├── Billable vs Non-Billable Ratio
├── Average Bill Rate
├── Project Margin %
├── Revenue per Consultant
├── Resource Allocation %
├── Bench Size and Cost
├── On-Time Delivery %
├── Budget Adherence %
├── SOW-to-Revenue Conversion Rate
└── Client Satisfaction Score (post-engagement)
```

---

## 2. METRIC DEFINITIONS (Standardized)

Each metric defined with calculation, source, and display format.

### Example: Win Rate
```json
{
  "id": "win_rate",
  "name": "Win Rate",
  "category": "pipeline",
  "description": "Percentage of closed deals that were won",
  "formula": "(COUNT(deals WHERE status = 'won') / COUNT(deals WHERE status IN ('won', 'lost'))) * 100",
  "data_source": "deals",
  "filters": ["close_date >= period_start", "close_date <= period_end"],
  "dimensions": ["owner_id", "team_id", "product_line", "lead_source", "deal_type"],
  "display": {
    "default": "percentage",
    "format": "0.0%",
    "chart_type": "trend_line",
    "color": "green"
  },
  "benchmark": {
    "good": "> 30%",
    "average": "20-30%",
    "needs_attention": "< 20%"
  }
}
```

### Example: Utilization Rate (IT Consulting)
```json
{
  "id": "utilization_rate",
  "name": "Consultant Utilization Rate",
  "description": "Percentage of available hours that are billable",
  "formula": "(SUM(time_entries WHERE type = 'billable').hours / (available_working_days * 8)) * 100",
  "data_source": "time_entries + resource_calendar",
  "filters": ["date >= period_start", "date <= period_end"],
  "dimensions": ["resource_id", "engagement_id", "role_level", "skill_tags"],
  "display": {
    "default": "percentage",
    "format": "0.0%",
    "chart_type": "bar",
    "color_field": "value >= 80 ? 'green' : value >= 60 ? 'yellow' : 'red'"
  },
  "benchmark": {
    "target": "> 80%",
    "warning": "60-80%",
    "critical": "< 60%"
  }
}
```

---

## 3. REPORT BUILDER ARCHITECTURE

### Report Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Tabular** | Row-based data table | Contact list, deal list |
| **Summary** | Grouped with subtotals | Pipeline by stage, by rep |
| **Matrix** | Row + Column cross-tab | Win rate by rep × quarter |
| **Chart** | Visual-only | Bar, line, pie, funnel |
| **Dashboard** | Multi-widget canvas | Executive overview |
| **Pivot** | Interactive cross-tab | Drag fields to rows/columns/values |

### Report Builder Capabilities

```
Data Source: Select entity + related entities (up to 3 levels deep)
Filters: AND/OR groups, field operators (=, !=, >, <, contains, in, between, is_null)
Grouping: Up to 3 levels (e.g., Pipeline → Stage → Owner)
Metrics: Sum, Count, Count Distinct, Average, Min, Max, Percent of Total
Calculated Fields: Formula using metric results
Chart: Type, X-axis, Y-axis, Color, Size, Tooltip
Scheduling: Daily, Weekly, Monthly → Email CSV/PDF/Image
Sharing: Private, Specific roles, Organization-wide
Export: CSV, Excel, PDF, PNG, JSON, embeddable URL
```

### Report Performance Limits

| Concern | Limit |
|---------|-------|
| Max rows in result | 10,000 (with warning > 5,000) |
| Max grouped rows | 500 per group level |
| Max related entity joins | 3 |
| Max metrics | 10 per report |
| Max filters | 20 per report |
| Timeout | 30 seconds |
| Scheduled report max | 50 per tenant |
| Dashboard widgets per page | 12 |

---

## 4. DATA WAREHOUSE STRATEGY

### Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  CRM Postgres    │────►│  CDC Pipeline    │────►│  ClickHouse      │
│  (Transactional) │     │  (Redpanda)      │     │  (Analytics)     │
│                  │     │                  │     │                  │
│  Normalized      │     │  Real-time sync  │     │  Denormalized    │
│  Row-level       │     │  No data loss    │     │  Columnar        │
│  Current state   │     │  Exactly-once    │     │  Sub-second      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                          │
                                                          ▼
                                                  ┌──────────────────┐
                                                  │  Report Builder  │
                                                  │  Dashboards      │
                                                  │  Export          │
                                                  └──────────────────┘
```

### Why Separate DW?
- Transactional DB (Postgres) is optimized for CRUD, not aggregation
- ClickHouse is 100-1000x faster for analytical queries
- No impact on user-facing performance from heavy reports
- Historical snapshots for trend analysis

### Denormalized View Examples

```sql
-- Deal Analytics View (denormalized)
CREATE MATERIALIZED VIEW mv_deal_analytics AS
SELECT
    d.id AS deal_id,
    d.name AS deal_name,
    d.amount,
    d.probability,
    d.expected_revenue,
    d.close_date,
    d.created_at,
    d.closed_at,
    d.forecast_category,
    d.status,
    d.win_reason_category,
    d.loss_reason_category,
    d.competitor,
    d.discount_amount,
    d.type AS deal_type,
    ps.name AS stage_name,
    p.name AS pipeline_name,
    o.name AS organization_name,
    o.industry AS org_industry,
    CONCAT(u.first_name, ' ', u.last_name) AS owner_name,
    t.name AS team_name,
    EXTRACT(DAYS FROM d.closed_at - d.created_at) AS sales_cycle_days,
    EXTRACT(YEAR FROM d.close_date) AS close_year,
    EXTRACT(QUARTER FROM d.close_date) AS close_quarter,
    EXTRACT(MONTH FROM d.close_date) AS close_month
FROM deals d
JOIN pipeline_stages ps ON d.stage_id = ps.id
JOIN pipelines p ON d.pipeline_id = p.id
LEFT JOIN organizations o ON d.organization_id = o.id
LEFT JOIN users u ON d.owner_id = u.id
LEFT JOIN teams t ON d.team_id = t.id;
```

---

## 5. DASHBOARD TEMPLATES

### Pre-Built Dashboards

| # | Dashboard | Personas | Purpose |
|:-:|-----------|:--------:|---------|
| 1 | Executive Overview | CRO, CEO, VP Sales | Pipeline, forecast, bookings, team KPIs |
| 2 | Sales Manager Dashboard | Sales Manager | Team activity, pipeline, coaching, forecast |
| 3 | Rep Performance | AE, SDR | Personal pipeline, activity, quota attainment |
| 4 | Pipeline Health | VP Sales, Manager | Funnel, velocity, conversion, stale deals |
| 5 | Activity Dashboard | Manager | Calls/emails/meetings per rep, trends |
| 6 | Forecasting Dashboard | VP Sales, CRO | Commit vs best case vs pipeline, accuracy |
| 7 | Win/Loss Analysis | CRO, Product | Win rate, loss reasons, competitor analysis |
| 8 | ITC: Project P&L | Delivery Manager, Practice Head | Margin, utilization, budget adherence |
| 9 | ITC: Resource Planning | Delivery Manager | Allocation, bench, skills, availability |
| 10 | SaaS: MRR Dashboard | CRO, VP CS | MRR breakdown, cohort, churn, NRR |
| 11 | SaaS: Health Dashboard | CSM, VP CS | Health scores, at-risk accounts, renewals |
| 12 | Data Quality | Admin, RevOps | Completeness, duplicates, freshness |

---

*Phase 13 complete. Reporting & Analytics covers KPI tree, metric definitions, report builder architecture, data warehouse strategy, and dashboard catalog. Next: Phase 14 — Sprint Breakdown & Implementation Roadmap.*
