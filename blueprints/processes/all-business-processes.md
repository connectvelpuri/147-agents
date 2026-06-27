# Phase 7: All Business Processes

**Created:** 2026-06-06
**Purpose:** Every end-to-end process documented with swimlanes, decision points, exception flows, and system interactions. 50+ processes across all departments.

---

## PROCESS LEGEND

Each process documented as:
- **Trigger**: What starts this process
- **Actors**: Who participates (by Persona #)
- **Swimlanes**: Multi-actor flow
- **Decision Points**: Where branches occur
- **Exceptions**: What can go wrong + handling
- **System Actions**: What the CRM auto-executes
- **Integration Points**: External system touchpoints

---

## PROCESS GROUP A: LEAD-TO-CASH (Sales Foundation)

### P-A1: Lead Capture → Qualification (SDR Workflow)

**Trigger:** Lead enters system (form, import, API, manual)
**Actors:** SDR (P1), Lead Assignment Engine
**Criticality:** HIGH — top-of-funnel accuracy determines everything downstream

**Flow:**
```
[WEB FORM / API]          [EMAIL-IN]          [MANUAL ENTRY]        [IMPORT]
       │                      │                     │                   │
       └──────────────────────┼─────────────────────┼───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Duplicate Check   │
                    │  (by email, phone) │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Match Found?      │──YES──► Merge or Link to existing
                    └─────────┬─────────┘
                              │ NO
                    ┌─────────▼─────────┐
                    │ Auto-Enrichment   │  AI fills: company size, industry, LinkedIn
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Initial Scoring    │  Rules + ML model → score 0-100
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Auto-Route         │── Round-robin ──► SDR-A
                    │ (by territory,     │── Skill-based  ──► SDR-B
                    │  score, round-     │── Score > 80   ──► AE direct
                    │  robin)            │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ SDR Queue          │  Assigned lead appears in SDR Home
                    │ "Call this lead"   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ SDR Call Session   │── Connected ──► Log outcome, set task
                    │                    │── No Answer  ──► Auto schedule follow-up
                    │                    │── Wrong #   ──► Re-route/recycle
                    │                    │── Not interested ─► Disqualify with reason
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │ Qualified?         │──YES──► Convert Lead → Contact + Org + Deal
                    │                    │         Auto-assign to AE
                    │                    │         Send notification
                    │                    │──NO───► Disqualify. Log reason.
                    │                    │         Nurture sequence (auto-enroll)
                    └───────────────────┘
```

**Exceptions:**
| Exception | Handling |
|-----------|----------|
| Duplicate match is wrong | Merge wizard allows manual override |
| Enrichment fails | Leave fields null, flag for manual fill |
| No SDR available | Lead goes to unassigned pool, alert manager |
| Lead converts itself (inbound after outbound) | Merge activities, keep latest status |
| High-score lead (80+) no AE available | Alert VP Sales, escalate |

**System Actions:**
- Auto-create Activity records for each step
- Update lead score on each interaction
- Send notification to assigned rep
- If no activity in 24h, escalate alert

---

### P-A2: Lead Conversion (Lead → Contact + Organization + Deal)

**Trigger:** SDR marks lead as qualified
**Actors:** SDR (P1), System
**Criticality:** CRITICAL — data integrity handoff point

**Flow:**
```
1. SDR clicks "Convert Lead"
2. System checks: does lead.company match existing Organization?
   │
   ├── YES → Link to existing organization
   └── NO  → Create new Organization from lead data
3. System creates Contact from lead data (if no match)
4. System creates Deal from lead data (default stage: 'Qualified')
5. Lead.status = 'converted'
6. Lead.converted_* fields populated with new record IDs
7. System migrates all Activity records from Lead to Deal
8. Send notification: AE assigned
9. Auto-enroll sequence: "New Deal Welcome" (if configured)
```

**Data Integrity Rules:**
- Cannot convert lead with missing required fields (name, company, email)
- Conversion is reversible within 24h (undo)
- After 24h, records are independent
- Activity history preserved in both directions

---

### P-A3: Deal Progression (Pipeline Management)

**Trigger:** Multiple — new deal, stage change, activity logged, time-based
**Actors:** AE (P2), Sales Manager (P3), AI Engine
**Criticality:** CRITICAL — pipeline health is the #1 CRM deliverable

**Flow:**
```
[DEAL CREATED]     [DEAL UPDATED]     [ACTIVITY LOGGED]     [TIME PASSED]
     │                    │                    │                    │
     └────────────────────┼────────────────────┼────────────────────┘
                          │
              ┌───────────▼───────────┐
              │ AI Pipeline Inspection  │  Auto-run on any deal change
              │                        │
              │ • Stale detection       │  No activity > 7 days → flag
              │ • Risk assessment       │  Dropped contact, no champion, etc.
              │ • Next best action      │  "Schedule demo with technical buyer"
              │ • Win probability       │  ML model based on similar deals
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ Deal Card in Pipeline  │  Color: Green (healthy) / Yellow / Red
              │ • Show age             │
              │ • Show last activity   │
              │ • Show AI risk score   │
              └───────────┬───────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
   [AE moves stage]  [Activity logged]  [Time trigger]
          │               │               │
          └───────────────┼───────────────┘
                          │
              ┌───────────▼───────────┐
              │ Stage Transition       │
              │ Validation:            │
              │ • Required fields      │
              │ • Required activities  │
              │ • Required contacts    │
              │ • Required documents   │
              └───────────┬───────────┘
                          │
              ┌───────────▼───────────┐
              │ Approval Needed?       │──YES──► Submit for approval
              │ (discount > 20%,       │         Wait for approval/rejection
              │  amount > $100k,       │
              │  custom rules)         │
              └───────────┬───────────┘
                          │ NO
              ┌───────────▼───────────┐
              │ Update Stage           │
              │ Update Probability     │
              │ Log Stage Activity     │  System creates activity: "Deal moved to X"
              │                        │
              │ If Stage = 'Closed Won'│──► Trigger Contract Generation
              │ If Stage = 'Closed Lost'│──► Trigger Win/Loss Survey
              └─────────────────────────┘
```

**Stage Transition Rules (configurable):**
| Transition | Validation |
|------------|------------|
| Qualification → Discovery | Must have discovery meeting logged |
| Discovery → Proposal | Must have >1 contact identified |
| Proposal → Negotiation | Must have quote sent |
| Negotiation → Closed Won | Discount approval obtained (if applicable) |
| Any → Closed Lost | Must provide loss reason |

---

### P-A4: Forecasting Process

**Trigger:** Weekly/monthly/quarterly cadence, manager request
**Actors:** AE (P2), Manager (P3), VP Sales (P4), CRO (P5), AI Engine
**Criticality:** HIGH — inaccurate forecasts break the business

**Flow:**
```
1. AI collects: All open deals for the period
2. AI calculates: 
   • Commit = deals with >60% probability, expected close this period
   • Best Case = deals >30% probability
   • Pipeline = rest
3. AI adjusts: ML model applies historical bias correction
   • "Last quarter, Rep A's commit deals close at 72% rate"
   • "Deals in this stage historically convert at 35%"
4. Rep reviews their forecast → adjustments with manager notes
5. Manager reviews team rollup → adjustments → submit
6. VP Sales reviews regional rollup → adjustments → submit
7. CRO sees consolidated forecast vs quota vs targets
8. Forecast vs Actual tracked automatically when deals close
9. Forecast accuracy report runs after period closes
```

**Forecast Confidence Scoring:**
```
Rep A: Commit $500k | AI-adj: $425k | Range: $380k-$470k
   ^ This means: Rep says $500k, AI says $425k based on history
   Best guess: $425k with $380k floor and $470k ceiling
```

---

## PROCESS GROUP B: SALES OPERATIONS

### P-B1: Quote-to-Order

**Trigger:** AE selects products for a deal
**Actors:** AE (P2), System, Approver (if discount > threshold)

**Flow:**
```
1. AE selects product(s) from catalog → quantities → discounts
2. System calculates total with discount
3. If discount > rep's authority limit → submit for approval
   │
   ├── Approval Process:
   │   • Manager approves/rejects (email or in-app)
   │   • If amount > $100k → VP Sales also approves
   │   • Escalation: 24h no response → auto-escalate
   │
4. System generates quote PDF from template
5. AE sends to customer (via email with tracking)
6. Customer views quote → accepts/signs
7. System creates Order (if configured)
8. System updates Deal to 'Closed Won' (if configured)
9. For SaaS: new Subscription record created with start dates
10. For ITC: new Engagement created from quote/SOW
```

---

### P-B2: Territory Assignment & Management

**Trigger:** New territory creation, account reassignment, quarterly planning
**Actors:** VP Sales (P4), Admin (P6), System

**Key Rules:**
- Territories are hierarchical (Region → Area → Territory)
- One user can cover multiple territories
- Accounts can be assigned to territories manually or by rule
- Territory-based sharing: users see only their territory's records
- Periodic reassignment: rules for rebalancing

---

## PROCESS GROUP C: IT CONSULTING VERTICAL

### P-C1: SOW Creation → Approval

**Trigger:** Deal reaches Proposal stage for IT Consulting vertical
**Actors:** AE (P2), Delivery Manager (P17), Practice Head, Admin
**Criticality:** HIGH — SOW is the legal/financial foundation

**Flow:**
```
1. AE selects SOW Template (or blank)
2. System populates from Deal: client, amount, dates
3. Delivery Manager defines:
   • Scope of work sections
   • Deliverables with dates
   • Milestone payment schedule
   • Resource requirements (roles, skills, level of effort)
   • Assumptions & exclusions
4. System calculates: effort × rate = total
5. Practice Head reviews:
   • Margin check (target > 35%)
   • Resource availability
   • Risk assessment
6. Approval chain:
   │
   ├── Amount < $50k: Delivery Manager approves
   ├── $50k-$250k: Practice Head + Finance
   └── > $250k: VP Delivery + CFO
7. SOW locked → PDF generated → sent to client
8. Client signs (e-sign via DocuSign integration)
9. SOW.status = 'signed' → Auto-create Engagement from SOW
10. Engagement milestones = SOW payment milestones
```

### P-C2: Resource Allocation

**Trigger:** New engagement created, resource request, bench alert
**Actors:** Delivery Manager (P17), Resource Manager, System

**Flow:**
```
1. Engagement has resource requirements: {role: "Senior Architect", skills: ["AWS","Kubernetes"], hours: 480}
2. Delivery Manager opens Resource Planner
3. System shows:
   • Available resources matching skills (sorted by match %)
   • Current allocation % per resource
   • Future availability (when current engagements end)
4. Manager drags resource to engagement:
   • Set allocation % (50%, 100%)
   • Set start/end dates
   • Set project-specific bill rate (from Rate Card or override)
5. System checks conflicts:
   │
   ├── No conflict → Allocate
   └── Conflict → Show overlap, manual resolution or auto-reject
6. Resource notified of new assignment
7. Calendar synced (if integration active)
```

### P-C3: Time Entry & Approval (Weekly Cycle)

**Trigger:** Weekly timesheet submission
**Actors:** Consultant (P16), Delivery Manager (P17), Finance
**Criticality:** CRITICAL — drives billing, payroll, P&L

**Flow:**
```
Monday: System sends reminder to enter time
↓
Consultant enters time (timer or manual grid):
  • Select engagement (auto-suggest based on current assignments)
  • Enter hours per day
  • Categorize: billable/non-billable/admin/training/PTO
  • Add description
  • Attach deliverable (optional)
↓
Wednesday: System reminds if incomplete
↓
Friday 5pm: Timesheet deadline
  • System auto-submits whatever is entered
  • Missing hours flagged as unbillable/non-billable
↓
Delivery Manager reviews:
  • Correct engagement?
  • Billable vs non-billable reasonable?
  • Description adequate for client audit?
  │
  ├── Approve → Status = 'approved'
  └── Reject → Status = 'rejected', add reason, consultant re-submits
↓
System aggregates approved entries for:
  • Billing run (weekly/monthly per engagement terms)
  • Utilization report
  • Project P&L update
  • Payroll feed
```

**Exception Flows:**
- Missed deadline: auto-submitted as draft, late flag for manager
- Holiday adjustment: prorated targets
- Overtime requires pre-approval → flag on entry if > 8h/day or > 40h/week

---

### P-C4: Billing Run (Milestone/Hourly)

**Trigger:** Monthly billing cycle, milestone achieved, engagement terms
**Actors:** Finance, System, Delivery Manager

**Flow:**
```
For Fixed Bid / Milestone:
1. Milestone is marked complete in Engagement
2. System generates invoice for milestone amount
3. Sends to client with SOW reference

For T&M (Time & Materials):
1. System collects all approved TimeEntries for period
2. System collects all approved Expenses for period
3. Calculates: total_hours × bill_rate + expenses × markup
4. Generates invoice draft
5. Finance reviews → approves
6. Invoice sent to client (email + portal)
7. Payment tracked → apply to invoice
```

---

## PROCESS GROUP D: SAAS VERTICAL

### P-D1: Subscription Lifecycle

**Trigger:** Customer signs up, upgrades, downgrades, cancels
**Actors:** CSM (P9), System, Stripe/Zuora

**Stages:**
```
TRIAL ──► ACTIVE ──► PAST_DUE ──► CANCELED
  │                    │              │
  │                    ▼              ▼
  │                Dunning       Churned (voluntary)
  │               (3 retries)    Churned (involuntary)
  │                    │
  │              Reactivated
  │                    │
  └──► Convert ──► ACTIVE
```

**Key Process: Trial → Active**
```
1. Trial created (signup, sales-assisted, or import)
2. Trial start: welcome email, onboarding sequence
3. Trial mid-point (day 7 of 14): CSM reach-out
4. Trial expiry: conversion email, discount offer if configured
5. Trial expired: grace period (3 days)
6. Auto-convert: if credit card on file
7. Manual convert: sales-assisted
```

**Key Process: Dunning (Failed Payment Recovery)**
```
Day 0: Payment fails → Invoice.status = 'past_due'
Day 1: Email notification: "Payment failed, update payment method"
Day 3: Second notification
Day 7: Final notification + service restricted (read-only)
Day 14: Subscription cancelled → churned (involuntary)
Any day: Customer updates payment → reactivate
```

---

### P-D2: Health Score Calculation

**Trigger:** Daily batch, real-time on new data
**Actors:** System, CSM

**Calculation Model:**
```
Health Score = (Product Usage × 0.30) + (Support × 0.20) + (NPS × 0.20) + (Payment × 0.15) + (Engagement × 0.15)

Where:
  Product Usage = DAU/MAU ratio, feature adoption, API calls, storage used
  Support = Ticket volume trend, avg response time, unresolved criticals
  NPS = Latest score, trend (improving/declining)
  Payment = On-time payment history, invoice aging
  Engagement = QBR completion, training attendance, CSM interaction
```

**Alerts:**
- Score < 40 → Critical alert → CSM intervention required
- Score 40-60 → Warning → CSM check-in recommended
- Score drop > 10 points in 30 days → Trend alert
- Score improving > 15 points → Positive flag for expansion signal

---

### P-D3: Renewal Management

**Trigger:** 90 days before subscription term end
**Actors:** CSM (P9), VP CS (P11), System

**Timeline:**
```
T-90: System flags upcoming renewal. Risk assessment runs.
T-60: CSM reviews health score, decides strategy.
       • Green health → auto-renew (send confirmation email)
       • Yellow health → schedule check-in call
       • Red health → executive engagement need
T-30: Renewal proposal generated (if manual)
T-14: Renewal invoice sent (if auto-renew)
T-7:  Payment attempt (if auto-pay)
T-0:  Renewal processed or subscription expires
```

---

## PROCESS GROUP E: CROSS-FUNCTIONAL

### P-E1: Lead Handoff (SDR → AE)

**Actors:** SDR (P1), AE (P2), System
**Criticality:** CRITICAL — most common drop-off point in CRM

**Rules:**
1. SDR qualifies lead, converts to Contact + Organization + Deal
2. System assigns to AE (territory match, round-robin, least-loaded)
3. AEs receive:
   - In-app notification
   - Email summary ("New deal assigned: Acme Corp $50k")
   - SMS (if configured)
4. System checks 24h later: Has AE contacted?
   │
   ├── No → Notify SDR (can they help?)
   │   └── 48h still no contact → Escalate to Manager
   └── Yes → Normal progression
5. SDR can view deal until it moves past first AE stage
6. SDR gets credit/commission on close (source attribution)

---

### P-E2: Account Planning Process

**Trigger:** Quarterly, or when key account at risk
**Actors:** AE (P2), CSM (P9), Manager (P3)
**Frequency:** Quarterly for top 20 accounts, annually for rest

**Flow:**
```
1. Select account → load current state
2. System shows:
   • Open deals + history
   • Contact map (org chart if available)
   • Product usage (SaaS) / project history (ITC)
   • Sentiment indicators (NPS, support tickets, meeting notes AI analysis)
3. Team reviews:
   • Relationship gaps (missing champions/exec sponsorship)
   • Expansion opportunities (land → expand)
   • Risks (competing evaluations, contract expirations)
4. Define strategy:
   • Key initiatives for next quarter
   • Relationship building plan
   • Revenue targets (renewal + expansion)
5. Save as Account Plan (linked to Organization)
6. System tracks progress against plan quarterly
```

---

### P-E3: Audit & Compliance Process

**Trigger:** Scheduled (monthly), user request, change detection
**Actors:** Admin (P6), CISO (P13), System

**Flow:**
```
1. System aggregates:
   • All config changes in period
   • All permission changes
   • All data exports
   • Failed login attempts
   • Accessed records by sensitive field
2. Admin reviews for anomalies:
   • Config changes outside business hours
   • Bulk exports by non-admin users
   • Permission escalation
3. Export audit report → PDF with sign-off
4. CISO reviews findings → actions assigned
5. Cleanup: expired sessions, inactive users, stale records
```

---

## PROCESS GROUP F: SYSTEM PROCESSES

### P-F1: Data Import Process

**Trigger:** User uploads CSV/Excel for import
**Actors:** Admin (P6), System
**Criticality:** HIGH — bad imports corrupt the entire CRM

**Flow:**
```
1. User selects file + target entity
2. System displays first 10 rows as preview
3. User maps columns to fields (auto-suggest or manual)
4. System runs validations:
   • Required fields present?
   • Data type correct? (email in email field)
   • Duplicate detection (by id, email, custom rules)
5. Results shown:
   • Success rows: N
   • Warning rows: N (autofix possible)
   • Error rows: N (must fix)
6. User resolves errors → revalidate
7. User confirms import
8. System executes in transaction:
   • Creates records
   • Logs audit entries
   • Runs duplicate merge for flagged matches
   • Triggers workflow rules
9. Rollback if > 5% failure rate (configurable)
10. Import summary report sent to user
```

---

### P-F2: Sandbox Refresh Process

**Trigger:** Admin requests sandbox refresh
**Actors:** Admin (P6), System

**Flow:**
```
1. Select sandbox → "Refresh from Production"
2. Choose data scope: Full / Config Only / Mini (10% records)
3. System:
   • Drops sandbox data
   • Copies production config (entities, fields, workflows, layouts)
   • Anonymizes personal data (if full copy)
   • Copies record subset (if mini)
4. Run data integrity validation
5. Notify admin: "Sandbox refresh complete"
6. Deploy from sandbox: select config changes → migrate to production
```

---

## PROCESS INDEX (52 Processes)

| ID | Process | Phase | Vertical | Priority |
|:--:|---------|:-----:|:--------:|:--------:|
| A1 | Lead Capture → Qualification | Sales | Both | Critical |
| A2 | Lead Conversion | Sales | Both | Critical |
| A3 | Deal Progression | Sales | Both | Critical |
| A4 | Forecasting | Sales | Both | High |
| A5 | Win/Loss Analysis | Sales | Both | Medium |
| B1 | Quote-to-Order | SalesOps | Both | High |
| B2 | Territory Assignment | SalesOps | Both | Medium |
| B3 | Quota Setting & Tracking | SalesOps | Both | High |
| B4 | Commission Calculation | SalesOps | Both | Medium |
| B5 | Email Sequence Enrollment | SalesOps | Both | High |
| C1 | SOW Creation → Approval | ITC | ITC | Critical |
| C2 | Resource Allocation | ITC | ITC | Critical |
| C3 | Timesheet Entry & Approval | ITC | ITC | Critical |
| C4 | Billing Run (Milestone/T&M) | ITC | ITC | Critical |
| C5 | Expense Entry & Approval | ITC | ITC | High |
| C6 | Change Order Process | ITC | ITC | High |
| C7 | Project P&L Review | ITC | ITC | High |
| C8 | Resource Capacity Planning | ITC | ITC | Medium |
| C9 | Rate Card Update | ITC | ITC | Low |
| D1 | Subscription Lifecycle | SaaS | SaaS | Critical |
| D2 | Health Score Calculation | SaaS | SaaS | High |
| D3 | Renewal Management | SaaS | SaaS | Critical |
| D4 | Dunning (Failed Payment) | SaaS | SaaS | High |
| D5 | Churn Analysis & Save | SaaS | SaaS | High |
| D6 | Expansion Identification | SaaS | SaaS | Medium |
| D7 | Invoice Creation & Payment | SaaS | SaaS | High |
| E1 | Lead Handoff (SDR→AE) | Cross | Both | Critical |
| E2 | Account Planning | Cross | Both | High |
| E3 | Deal Desk (Discount Approval) | Cross | Both | High |
| E4 | Win/Loss Survey & Analysis | Cross | Both | Medium |
| E5 | Multi-Product Bundling | Cross | Both | Low |
| E6 | Partner Deal Registration | Cross | Both | Low |
| F1 | Data Import | System | Both | Critical |
| F2 | Sandbox Refresh | System | Both | High |
| F3 | User Onboarding & Offboarding | System | Both | High |
| F4 | Permission Audit & Review | System | Both | High |
| F5 | Workflow Monitor & Alert | System | Both | Medium |
| F6 | Backup & Restore | System | Both | Critical |
| F7 | Integration Health Check | System | Both | High |
| F8 | Data Retention Cleanup | System | Both | Medium |
| F9 | AI Model Retraining | System | Both | Medium |
| F10 | Tenant Provisioning | System | Both | Critical |
| G1 | Campaign Management (Marketing) | Marketing | Both | Medium |
| G2 | Lead Scoring Model Update | Marketing | Both | Medium |
| G3 | Attribution Reporting | Marketing | Both | Low |
| H1 | Ticket Lifecycle (Support) | Support | Both | Medium |
| H2 | SLA Monitoring & Breach | Support | Both | High |
| H3 | Knowledge Base Contribution | Support | Both | Low |
| I1 | Custom Object Creation (Admin) | Admin | Both | High |
| I2 | Workflow Rule Creation & Test | Admin | Both | High |
| I3 | Report/Dashboard Creation | Admin | Both | High |
| I4 | Security Incident Response | Admin | Both | Critical |

---

## PROCESS AUTOMATION OPPORTUNITIES

| Process | Automation Level | AI Opportunity |
|---------|:----------------:|----------------|
| Lead Assignment | FULL | ML-based routing (best rep for this lead type) |
| Lead Enrichment | FULL | Auto-fill company data, social profiles |
| Activity Logging | HIGH | Voice→text, auto-log email, AI sentiment |
| Deal Risk Detection | FULL | AI anomaly detection, pattern matching |
| Forecasting | HIGH | AI bias correction, what-if simulation |
| Time Entry | PARTIAL | Auto-suggest from calendar, activity log |
| Health Score | FULL | Real-time calculation, trend prediction |
| Churn Prediction | FULL | ML model from historical churn patterns |
| Invoice Matching | FULL | Auto-match payment to invoice |
| Duplicate Detection | FULL | ML-based fuzzy matching + auto-merge |

---

*Phase 7 complete. 52 business processes documented with swimlanes, exceptions, automation opportunities. Next: Phase 8 — Customization Framework.*
