# Vertical CRM Requirements: IT Services & Consulting + SaaS

**Phase 1 — Market Research | Created:** 2026-06-06 16:06

---

## PART 1: IT SERVICES & CONSULTING VERTICAL

### The Core Problem
IT Consulting firms sell **expertise and time**, not products. Their CRM needs are fundamentally different from product companies.

### Key Business Processes

1. **Lead to SOW:**
   - Lead capture (RFP, referral, inbound)
   - Qualification (skills match, budget, timeline)
   - Discovery / scoping
   - Proposal creation (SOW — Statement of Work)
   - Resource estimation (roles, hours, rates)
   - SOW approval and signature
   - Project kickoff

2. **Project Delivery:**
   - Resource allocation and scheduling
   - Time tracking (billable vs non-billable)
   - Expense tracking
   - Milestone tracking
   - Change orders / scope changes
   - Client communication logs
   - Deliverable management

3. **Billing & Revenue:**
   - Time & Material billing
   - Fixed price milestones
   - Retainer management
   - Invoice generation from timesheets
   - Revenue recognition

4. **Account Management:**
   - Relationship mapping (stakeholder org chart)
   - Contract management (MSAs, SOWs, amendments)
   - Renewals and expansions
   - CSAT / NPS tracking per engagement

### Required Objects (Not Standard CRM)

| Object | Description |
|--------|-------------|
| Engagement / Project | Time-bounded work with scope, budget, resources |
| SOW (Statement of Work) | Legal agreement with deliverables, timeline, pricing |
| Time Entry | Billable/non-billable hours by consultant per project |
| Expense Entry | Travel, software, other billable costs |
| Resource | Consultant profile with skills, rate cards, availability |
| Skill / Certification | Expertise areas, certifications, proficiency levels |
| Rate Card | Standard and discounted billing rates |
| Change Order | Modifications to scope/budget mid-engagement |
| Deliverable | Outputs: documents, code, reports, decks |

### KPIs for IT Consulting (not standard CRM)

| KPI | Why |
|-----|-----|
| Utilization Rate | Billable hours / total hours — the #1 consulting metric |
| Average Bill Rate | Revenue per billable hour |
| SOW Win Rate | % of proposals that convert |
| Resource Allocation % | How fully are consultants booked? |
| Project Margin | Revenue - cost per engagement |
| Time to Bill | Days from work to invoice |
| Days Sales Outstanding (DSO) | Payment collection speed |
| Account Penetration | % of client's IT spend captured |

### Persona: Consulting Delivery Manager
- **Daily activities:** Review resource allocation, check project health, approve time entries, handle escalations
- **Pain points:** No visibility into resource availability. Spreadsheets for tracking. Late time entries
- **Our solution:** Resource scheduling dashboard, utilization heatmap, automated reminders

### Persona: Consulting Partner (Practice Head)
- **Daily activities:** Pipeline review, staff planning, revenue forecasting, account planning
- **Pain points:** Can't see pipeline by skill area. No forecasting by practice. Poor visibility into margins
- **Our solution:** Pipeline by practice/vertical, margin forecasting, skill gap analysis

---

## PART 2: SAAS VERTICAL

### The Core Problem
SaaS companies sell **subscriptions**, not one-time products. Their CRM revolves around recurring revenue, churn, and expansion.

### Key Business Processes

1. **Lead to Subscription:**
   - Demand generation (content, trial, referral)
   - Trial management (signup -> activation -> conversion)
   - Sales-led vs product-led motions
   - Pricing and packaging
   - Contract negotiation (annual vs monthly, seats)
   - eSignature and billing integration

2. **Revenue Management:**
   - MRR/ARR tracking
   - Subscription management (seats, tiers, add-ons)
   - Usage-based billing
   - Discount and promo management
   - Renewal forecasting
   - Churn analysis

3. **Customer Success:**
   - Onboarding and activation
   - Health scoring (product usage, support tickets, NPS)
   - QBR (Quarterly Business Review) tracking
   - Expansion/upsell identification
   - Renewal management
   - Churn prediction

4. **Product-Led Growth:**
   - Free trial / freemium tracking
   - Feature adoption analytics
   - PQL (Product Qualified Lead) scoring
   - User-level activity tracking
   - Account expansion signals

### Required Objects (Not Standard CRM)

| Object | Description |
|--------|-------------|
| Subscription | Recurring revenue record with tier, seats, term |
| Invoice | Billing record from Stripe/Chargebee |
| Payment | Individual payment transaction |
| Usage Metric | Product usage data by user/account |
| Health Score | Composite score from multiple signals |
| Onboarding Task | Steps to activate a new customer |
| Renewal | Upcoming renewal with probability, amount |
| Churn Reason | Classification of why customer left |
| NPS Response | Survey responses with follow-up |

### KPIs for SaaS (not standard CRM)

| KPI | Why |
|-----|-----|
| MRR / ARR | Monthly/Annual Recurring Revenue |
| Net Revenue Retention (NRR) | Expansion - contraction - churn |
| Logo Retention | % of customers retained |
| Customer Acquisition Cost (CAC) | Sales + marketing cost per customer |
| LTV:CAC Ratio | Lifetime value vs acquisition cost |
| Time to Value (TTV) | Days from signup to activation |
| Monthly Active Users (MAU) | Product engagement |
| Churn Rate | % of customers lost per period |
| Expansion Revenue | Upsells + cross-sells per period |
| PQL Conversion Rate | Product-qualified leads that convert |

### Persona: SaaS Customer Success Manager
- **Daily activities:** Review health scores, reach out to at-risk accounts, conduct QBRs, identify expansion opportunities, track NPS
- **Pain points:** No unified health score. Siloed data (product usage in app, support in Zendesk, billing in Stripe)
- **Our solution:** Unified customer 360 with health scoring, automated alerts, playbook-driven outreach

### Persona: SaaS VP of Revenue
- **Daily activities:** Review pipeline, churn metrics, NRR, forecast accuracy. Plan growth initiatives
- **Pain points:** Data fragmented between CRM, billing, product analytics. Can't get a single view of revenue health
- **Our solution:** Revenue intelligence dashboard combining CRM data + subscription metrics + product usage

---

## PART 3: SHARED REQUIREMENTS (Both Verticals)

| Requirement | IT Consulting | SaaS | Both |
|-------------|:-------------:|:----:|:----:|
| Pipeline management | Yes | Yes | Both |
| Contact/Account management | Yes | Yes | Both |
| Activity tracking | Yes | Yes | Both |
| Email integration | Yes | Yes | Both |
| Calendar sync | Yes | Yes | Both |
| Mobile access | Critical (field) | Important | Both |
| Reporting & dashboards | Yes | Yes | Both |
| API access | Yes | Yes | Both |
| Security & RBAC | Yes | Yes | Both |
| Audit trail | Yes | Yes | Both |
| {vertical_object} | SOW/Engagement | Subscription | — |
| {vertical_kpi} | Utilization | MRR/Churn | — |
| {vertical_workflow} | Resource scheduling | Renewal management | — |

---

## PART 4: SOVEREIGN CRM VERTICAL STRATEGY

### The Winning Approach

| | IT Consulting Template | SaaS Template |
|---|----------------------|---------------|
| **Custom Objects** | Engagement, SOW, Time Entry, Resource, Skill | Subscription, Health Score, Usage Metric, Invoice |
| **Default Pipelines** | Discovery -> Proposal -> Negotiation -> Won | Trial -> Active -> Negotiation -> Won |
| **Workflows** | Time submission, SOW approvals, Resource request | Onboarding, Renewal, Churn detection |
| **Reports** | Utilization, Margin, SOW Win Rate, Pipeline by Practice | MRR, Churn, NRR, LTV:CAC, Health Score trends |
| **Integrations** | Jira (projects), QuickBooks (invoicing), Calendly (scheduling) | Stripe (billing), Product analytics, Slack (alerts) |
| **KPIs** | Utilization, Bill Rate, Margin | MRR, Churn, NRR, LTV:CAC |

### The Dynamic Object Builder Advantage

When a consulting firm needs "Certification" tracking or a SaaS company needs "API Usage Tier" — they don't call support. They open the Dynamic Object Builder and create it. **This is the differentiator.**

---

*This analysis will inform the data model, workflows, and default configurations for both vertical templates.*
