# Cross-Module Workflows — Connected Map

## 1. Marketing → Sales Handoff

### 1.1 MQL → SAL → SQL → Opportunity
- **Trigger**: Lead reaches MQL status (score threshold or behavior event)
- **Actors**: Marketing → SDR/BDR → Sales rep
- **Connected Modules**: Marketing (Lead Gen, Campaigns) → Sales (Lead Management, Pipeline)
- **Steps**:
  1. **Marketing**: Lead crosses MQL threshold (score ≥ Critical Score, e.g. 80/100)
  2. **Marketing**: Lead status updated to MQL, stamped with `MQLDate__c`, source campaign
  3. **Marketing**: Lead added to MQL report for SDR review queue
  4. **Notification**: SDR team alerted via Slack/email — "New MQL: Acme Corp — VP Engineering"
  5. **SDR**: Reviews lead: checks enrichment, intent signals, account fit
  6. **SDR**: Accepts lead → status = SAL (Sales Accepted Lead) with timestamp
  7. **SDR**: Rejects lead → status = MQL Rejected, reason code (bad fit, wrong contact)
  8. **SDR**: Attempts contact — call, email, LinkedIn
  9. **SDR**: Qualifies lead (BANT) → status = SQL (Sales Qualified Lead)
  10. **SDR**: Disqualifies → recycled to nurture, reason logged
  11. **SDR**: Converts or reassigns — SQL routed to closer/AE
  12. **AE**: Accepts SQL → opportunity created (auto-populated from lead)
  13. **AE**: Starts pipeline stage progression
- **Data Flow**: Lead → enriched fields → score → MQL status → SAL timestamps → SQL conversion → Opportunity
- **Validation Points**:
  - Lead must have valid email to be MQL
  - SDR must action within SLA (typically 24h from MQL→SAL)
  - Opportunity cannot exist without an approved SQL reason
- **Error States**: Lead stuck at MQL (no SDR available), SAL timer expired without action (escalated)
- **SLA**: MQL→SAL < 24h, SAL→SQL < 5 business days
- **Gap/Friction**: MQL quality (marketing sends low-fit leads → SDRs ignore queue); Score threshold too low → SDRs flooded; Score threshold too high → leads age out

### 1.2 Campaign → Pipeline Attribution
- **Trigger**: Opportunity created, contact campaign history exists
- **Actors**: System (automated attribution engine)
- **Connected Modules**: Marketing (Campaigns) → Sales (Opportunities)
- **Steps**:
  1. Lead created → campaign membership stamped (first-touch campaign)
  2. Lead progresses through nurture → additional campaign touches logged
  3. Lead converts to contact/opportunity → campaign history copied to opportunity
  4. Attribution model applied: first-touch, last-touch, multi-touch
  5. Pipeline revenue reported by campaign source
- **Data Flow**: Campaign → CampaignMember (Lead) → CampaignMember (Contact) → OpportunityContactRole → Attribution report
- **SLA**: Attribution calculation within 24h of opportunity creation

### 1.3 Marketing Influenced Pipeline
- **Trigger**: Any touch from marketing during opportunity lifecycle
- **Steps**: Track campaigns associated to contact → report influenced pipeline = sum of opportunities where contact has marketing campaign history

---

## 2. Sales → Service Handoff

### 2.1 Closed Won → Onboarding → Support → Renewal
- **Trigger**: Opportunity stage = Closed Won
- **Actors**: Sales rep → CSM → Support team → Renewal manager
- **Connected Modules**: Sales (Pipeline) → Service (Case, Onboarding)
- **Steps**:
  1. **Sales**: Rep closes deal, status = Closed Won
  2. **System**: Creates Customer record (if not existing), links to Account
  3. **System**: Creates onboarding project/case with template: Kickoff, Setup, Training, Go-Live
  4. **Notification**: CSM assigned, notified with onboarding packet
  5. **CSM**: Conducts kickoff call, sets success milestones
  6. **System**: During onboarding, auto-creates support entitlement
  7. **Support**: Customer creates cases → handled per SLA
  8. **CSM**: Quarterly business reviews (QBRs), health score monitoring
  9. **System**: Renewal timer starts 90 days before contract end → notifies renewal manager
  10. **Renewal**: Renewal manager engages for contract renewal
- **Data Flow**: Opportunity (Closed Won) → Account (Active Customer) → Onboarding Project → Support Cases → Renewal Opportunity
- **Validation Points**:
  - Onboarding must start within 5 business days of close
  - Support entitlement must be active before first case
  - Renewal opportunity must be created at 90-day mark
- **Error States**: No CSM assigned (onboarding delayed), entitlement not created (support cannot log case), renewal opportunity never created
- **SLA**: Onboarding kickoff < 5 business days; Support response = contract SLA; Renewal engagement at T-90 days

### 2.2 Case → Account Health → Renewal Risk
- **Trigger**: Case volume spike, P1 case opened
- **Steps**:
  1. Case created at account with P1 severity
  2. Account health score recalculated (support signal weight applied)
  3. If health score drops to Yellow/Red → alert CSM, renewal manager
  4. Renewal manager adds risk flag to renewal opportunity
  5. Executes mitigation: exec check-in, discount offer, product credits

---

## 3. Service → Sales Follow-Up

### 3.1 Support → Upsell → Opportunity
- **Trigger**: Support interaction reveals customer need
- **Actors**: Support agent → Sales rep
- **Connected Modules**: Service (Case) → Sales (Opportunity)
- **Steps**:
  1. Support agent identifies expansion opportunity during case resolution
  2. Agent logs case with "Upsell Opportunity" checkbox + notes
  3. System routes case to sales for review (or assigns AE)
  4. Sales rep reviews case, contacts customer
  5. If opportunity → create new opportunity, link to case and account
  6. Track: revenue from service-originated opportunities
- **Friction Point**: Agents don't flag upsells (no incentive), sales doesn't follow up on flagged cases in time
- **SLA**: Sales must contact customer within 48h of flag

### 3.2 Churn Prevention → Retention Opportunity
- **Trigger**: Churn signal detected (sentiment, usage drop, support spike)
- **Steps**:
  1. Health score drops to Red
  2. CSM creates retention action plan
  3. If discount/product change needed → create retention opportunity
  4. Track: saved revenue from retention efforts

---

## 4. Activity → Pipeline Correlation

### 4.1 Activity Logging Pipeline Impact
- **Trigger**: Task/event completed (call, email, meeting)
- **Connected Modules**: Activity → Pipeline
- **Steps**:
  1. Rep logs activity: type, duration, notes, related opportunity
  2. Activity metrics: calls/week per rep, meetings per deal stage
  3. Pipeline velocity: correlate activity frequency with stage progression speed
  4. Report: deals with > 5 activities/quarter close at X% higher rate
  5. Coaching: flag deals with no activity in 7 days
- **Data Flow**: Task → Opportunity → Pipeline Velocity → Activity Correlation Report
- **Error States**: Activities not linked to opportunity (orphan), activity logged with no outcome

### 4.2 Meeting → Next Step → Stage Progression
- **Trigger**: Meeting completed with next steps
- **Steps**:
  1. Rep logs meeting, captures next-step action
  2. System creates follow-up task from next step
  3. If next step = demo/presentation → advance stage
  4. Track meeting-to-stage-progression conversion rate

---

## 5. Custom Field → Everywhere Propagation

### 5.1 Custom Field Addition Propagation
- **Trigger**: New custom field created
- **Connected Modules**: Ops (Metadata) → All modules
- **Steps**:
  1. Admin creates field on Lead object
  2. Add to page layouts: Lead, Contact (if mapped at conversion)
  3. Add to search layouts (if searchable)
  4. Add to report types (if needed for reporting)
  5. Add to validation rules, workflow, flows
  6. Add to API field map for integrations
  7. Add to import/export templates
  8. Test field in sandbox → push to production
- **Gap**: Field often missed in reports, search layouts, or API mappings → data captured but invisible

---

## 6. Webhook → External System Integration

### 6.1 Webhook Trigger on Record Event
- **Trigger**: Record created, updated, deleted (per config)
- **Connected Modules**: All → External systems (ERP, Slack, custom app)
- **Steps**:
  1. Admin configures webhook: object, event (create/update/delete), fields, endpoint URL
  2. On event → CRM sends HTTP POST with payload (record data, event type, timestamp)
  3. External system receives, processes, responds with 200 OK
  4. On failure (4xx/5xx or timeout) → retry 3 times (1min, 5min, 15min)
  5. After 3 failures → dead letter queue, admin notified
  6. Admin reviews dead letter and replays

---

## 7. Report → Dashboard → Alert Pipeline

### 7.1 Report Generation & Dashboard Publication
- **Trigger**: Scheduled or on-demand
- **Connected Modules**: Reports → Dashboards → Alerts
- **Steps**:
  1. Create report: object, filters, grouping, summary formula, chart type
  2. Add to dashboard as component: text, chart, gauge, table
  3. Set dashboard filters: date range, role-based visibility
  4. Schedule dashboard refresh: hourly, daily, weekly
  5. Set alert thresholds: e.g., pipeline < 3x quota → email manager
  6. Alert sent: email, Slack, SMS (per recipient config)

---

## 8. Complete Cross-Module Dependency Map

```
Marketing ──┬──> MQL → SAL → SQL → Opp ──> Sales
            │                                   │
            ├──> Campaign Attribution ──────────>│
            │                                   │
            └──> Lead Nurture (recycle) ───────>│
                                                │
Sales ──────┬──> Closed Won → Onboarding ──────> Service
            │                                   │
            ├──> Renewal Opportunity ───────────>│
            │                                   │
            └──> Contract → SLA ───────────────>│
                                                │
Service ────┬──> Case → Upsell Flag ───────────> Sales
            │                                   │
            ├──> Health Score → Churn Risk ────>│
            │                                   │
            └──> CSAT → Account Health ────────>│
                                                │
Finance ────┬──> Invoice → Payment ────────────> All (Customer Status)
            │                                   │
            ├──> Commission → Rep Attainment ───> Sales (Motivation)
            │                                   │
            └──> RevRec → Deferred Rev ────────> Executive Reporting
                                                │
Ops ────────┬──> User Provisioning ────────────> All (Access)
            │                                   │
            ├──> Data Quality ─────────────────> All (Clean Data)
            │                                   │
            └──> Integration Sync ─────────────> All ↔ External
                                                │
Reports ────┬──> Dashboard ────> Alert ────────> All (Action)
            │                                   │
            └──> Forecast ──────> Quota ────────> Sales Management
```
