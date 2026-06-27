# IT Consulting Industry Profile — Sovereign CRM

**Version:** 1.0
**Industry:** IT Consulting & Services
**Target Personas:** Partner, Engagement Manager, Resource Manager, Consultant, SDR, Account Manager, Practice Lead

---

## 1. Industry Overview

IT Consulting firms sell expertise, not products. Key workflows:
- **Opportunity-to-Proposal:** RFP response, SOW creation, pricing
- **Resource Management:** Staffing consultants on engagements, skills tracking
- **Time & Expense:** Timesheets, billable hours, expense tracking
- **Project Delivery:** Milestones, deliverables, client satisfaction
- **Pipeline:** Consulting deal stages (long cycle, high-touch)

## 2. Custom Fields & Objects

### Extended Contact Fields
```
Field                    | Type     | Purpose
consultant_skill_tags    | text[]   | e.g., ["AWS", "Python", "Kubernetes"]
consultant_rate          | currency | Standard bill rate
consultant_utilization   | pct      | Current utilization rate
consultant_availability  | date     | Next available date
certifications           | text[]   | e.g., ["AWS Solutions Architect", "CISSP"]
employment_type          | picklist | W2 / 1099 / Subcontractor / Partner
years_experience         | number   | Years in current specialty
```

### Extended Organization Fields
```
Field                     | Type     | Purpose
partner_tier             | picklist | Gold / Silver / Bronze / Transactional
contract_type             | picklist | Master SOW / T&M / Fixed Bid / Retainer
annual_contract_value    | currency | ACV this fiscal year
preferred_vendor         | boolean  | Preferred supplier status
payment_terms            | picklist | Net30 / Net60 / Net90 / Monthly
revenue_to_date          | currency | Revenue from this client (YTD)
```

### New Objects Needed

| Object | Purpose | Key Fields |
|--------|---------|------------|
| **Engagement** | A consulting project won | Client, SOW value, start/end date, team members, status, type (T&M/Fixed/Retainer) |
| **SOW/Proposal** | Statement of Work being proposed | Version, value, stage (draft/reviewed/approved/signed), line items, payment milestones |
| **Placement** | Consultant assigned to engagement | Consultant, engagement, rate, start date, end date, role, billable percentage |
| **Time Entry** | Timesheet record | Consultant, engagement, date, hours, billable/pcs, description, approved_by |
| **Skill** | Taxonomy of skills/competencies | Name, category, description |

## 3. Pipeline Stages (IT Consulting Specific)

```
1. Lead Qualification       → 5%     | Prospect identified, initial contact made
2. Needs Discovery          → 10%    | Requirements gathered, budget confirmed
3. Proposal Submitted       → 25%    | SOW/proposal delivered to client
4. Negotiation              → 50%    | Pricing and scope under negotiation
5. Reference/Background     → 70%    | Client checking references
6. Contract Review          → 85%    | Legal review of MSA/SOW
7. Closed Won               → 100%   | Signed SOW, engagement starts
8. Closed Lost              → 0%     | Did not win (capture reason)
```

## 4. Workflows & Automations

### Onboarding a New Engagement
1. Opportunity marked "Closed Won"
2. Auto-create Engagement record from deal data
3. Notify Resource Manager
4. Auto-create setup checklist: credentials, onboarding doc, kickoff meeting
5. Assign Engagement Manager

### Consultant Assignment
1. Resource manager searches available consultants by skill
2. View utilization heat map across current engagements
3. Assign consultant → Engagement (as Placement)
4. Auto-update consultant availability
5. Notify consultant with engagement details

### Monthly Billing (T&M Engagements)
1. Collect approved time entries (month end)
2. Generate invoice draft from time entries × rates
3. Engagement Manager reviews
4. Send to client
5. Track payment status

## 5. Dashboard Layouts

### Account Manager Dashboard
- My clients (orgs)
- Active engagements by client
- Revenue YTD vs target
- Renewal pipeline (contract end dates within 90 days)
- SOWs pending signature
- Client satisfaction score trend

### Resource Manager Dashboard
- Consultant utilization (by person, by week)
- Open staffing needs (engagement start date within 2 weeks)
- Skills gap analysis (demand vs supply)
- Bench report (unassigned consultants)

### Practice Lead Dashboard
- Pipeline by practice area
- Win rate by stage
- Average deal size trend
- Bill rate trends by skill
- Consultant certification status

## 6. Reports

| Report | Purpose | Frequency |
|--------|---------|:---------:|
| Utilization Report | Billable vs non-billable hours | Weekly |
| Pipeline by Practice Area | Revenue forecast by service line | Weekly |
| SOW Expiry Report | Contracts ending in next 60 days | Monthly |
| Consultant Skills Matrix | Skill coverage across team | Quarterly |
| Client Profitability | Revenue vs cost by client | Monthly |
| Win/Loss Analysis | Why we win or lose deals | Monthly |

## 7. Integration Points

| Integration | Purpose | Priority |
|-------------|---------|:--------:|
| QuickBooks/Xero | Invoicing & expense sync | P1 |
| Jira/Linear | Project management sync (engagement ↔ project) | P1 |
| Slack | Notifications: new SOW, consultant assignment, deal closed | P2 |
| Outlook/Google Calendar | Scheduling: meetings, kickoffs, reviews | P2 |
| Harvest/Toggl | Timesheet import | P2 |
| LinkedIn Recruiter | Consultant profile enrichment | P3 |

## 8. Compliance Considerations

- **1099 tracking:** Subcontractor rate agreements, W-9 collection
- **Export controls:** Consultants working on classified/government projects
- **NDA tracking:** Which consultants have signed NDA for each client
- **Certification expiry:** Auto-notify when certifications near expiration
