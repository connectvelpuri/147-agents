# Phase 3: 17 User Personas

**Created:** 2026-06-06
**Purpose:** Every feature, workflow, and UI decision is validated against these personas. If it doesn't serve one, question it.

---

## PERSONA 1: SDR/BDR (Sales Development Representative)

| Attribute | Detail |
|-----------|--------|
| Title | Sales Development Representative / Business Development Rep |
| Employer Size | Mid-market to Enterprise |
| Technical Level | Low |
| CRM Proficiency | Low — CRM is a tool they are forced to use |
| Daily CRM Time | 3-4 hours (logging calls, emails, updating leads) |
| Devices | Laptop (primary), Mobile (secondary for quick updates) |
| Motivation | Hit quota. Don't miss a follow-up. Show activity volume. |
| Frustration | Data entry takes time away from calling. CRM is slow. Forced fields cause data quality issues. |

### Core Workflows
1. **Morning queue:** Review assigned leads, prioritize by score, plan call order
2. **Call session:** Log call outcome, set follow-up, move to next
3. **Email sequence:** Open sequenced emails, see replies, log manual outreach
4. **Handoff:** Mark lead as qualified, assign to AE, document key context
5. **End of day:** Log all activities, update lead statuses, send notes to manager

### Needs
- Rapid lead prioritization (who to call first)
- 1-click activity logging (call, email, SMS)
- Sequence automation with reply detection
- Auto-dialer integration
- Lead scoring visibility
- Manager activity visibility without extra reporting work

### Pain Points — Solved by Us
| Pain | Solution |
|------|----------|
| Too many leads, no prioritization | AI lead scoring + next-best-action suggestions |
| 5 clicks to log a call | 1-click call logging with auto-duration, auto-disposition |
| Manual follow-up tracking | Sequence automation with auto-pause on reply |
| No visibility into lead quality | Lead scoring dashboard on home screen |
| Late-night data entry | Voice notes transcribed by AI, auto-logged |

### Quotes
> "I spend more time in Salesforce than I do on the phone."
> "I just want to know who to call next."
> "If it takes more than two clicks, I will not do it."

### Design Implications
- Home dashboard = prioritized task list, not a graph
- Activity logging = 1-click, pre-populated where possible
- Mobile = full activity logging (not view-only)
- Search = must be instant (they need phone/email fast)

---

## PERSONA 2: ACCOUNT EXECUTIVE (AE)

| Attribute | Detail |
|-----------|--------|
| Title | Account Executive / Sales Representative |
| Employer Size | Mid-market to Enterprise |
| Technical Level | Low-Medium |
| CRM Proficiency | Medium — they enter what is required, nothing more |
| Daily CRM Time | 2-3 hours |
| Motivation | Close deals. Hit quota. Manage pipeline accurately. |
| Frustration | Forecasting is inaccurate. Too much manual data entry. Deal stage reporting is political. |

### Core Workflows
1. **Pipeline review:** Review active deals, update stages, check next steps
2. **Deal work:** View deal record, check contact info, review history, prepare for call/meeting
3. **Discovery:** Log meeting notes, record pain points, update requirements
4. **Proposal:** Generate quote, send to client, track status
5. **Negotiation:** Update discount amounts, track approval
6. **Close:** Mark won/lost, log reason, trigger contract/billing
7. **Account planning:** Review existing accounts, identify expansion, create relationship maps

### Needs
- Clean pipeline visualization
- Quick deal updates (stage, amount, close date)
- Activity history for context before any interaction
- Meeting notes with AI summarization
- Document generation (proposals, quotes)
- Forecasting that reflects reality (not politics)
- Account map for enterprise accounts

### Pain Points — Solved by Us
| Pain | Solution |
|------|----------|
| Pipeline is slow to load | CRDT local-first — pipeline loads in under 200ms |
| Deal stage does not reflect reality | Activity-based stage validation: stale deal detection |
| Forecasting is guesswork | AI forecasting from historical patterns + pipeline inspection |
| Meeting notes are lost | AI transcription + auto-log to deal and contact records |
| Too many tools | CRM = single source of truth |

### Quotes
> "My pipeline is always 30 days behind reality."
> "I trust my spreadsheet more than the CRM."

---

## PERSONA 3: SALES MANAGER

| Attribute | Detail |
|-----------|--------|
| Title | Sales Manager / Director of Sales |
| Reports To | VP of Sales |
| Team Size | 5-15 reps |
| Technical Level | Medium |
| CRM Proficiency | High (for reports, pipeline inspection) |
| Daily CRM Time | 1-2 hours |
| Motivation | Coach reps, forecast accurately, identify problems early. |
| Frustration | Cannot see rep activity patterns. Reports are slow. Forecasting is unreliable. |

### Core Workflows
1. **Morning inspection:** Review team pipeline, check stale deals, identify coaching opportunities
2. **Pipeline call review:** Scrub through deals, ask reps for updates, update forecast
3. **Coaching:** Review rep activity metrics, call recordings, deal progression rate
4. **Forecasting:** Update rolling forecast, submit to VP, review gaps
5. **Team reporting:** Pipeline value, win rate, activity metrics, conversion rates
6. **1:1 prep:** Review rep pipeline, deals needing help, activity trends

### Needs
- Real-time pipeline by rep with deal-level drill-down
- Activity metrics per rep (calls, emails, meetings)
- Stale deal alerts
- Forecast rollup with confidence scoring
- Coaching tools: call recording review, deal progression analysis
- Team dashboard (not custom report building)

### Quotes
> "I do not know if my team is actually working or just clicking buttons."
> "By the time I see a problem in a deal, it is too late."
> "I spend more time building reports than coaching."

---

## PERSONA 4: VP OF SALES

| Attribute | Detail |
|-----------|--------|
| Title | VP of Sales |
| Reports To | CRO / CEO |
| Team Size | 20-100+ reps |
| CRM Proficiency | Medium (drill-down, dashboards) |
| Daily CRM Time | 30-60 min |
| Motivation | Predictable revenue. Accurate forecasting. Team productivity. |
| Frustration | Forecast accuracy is poor. Cannot see real metrics. Reporting is compiled manually. |

### Core Workflows
1. **Weekly forecast call:** Review rollup, check key deals, identify risks, adjust forecast
2. **Team performance review:** Compare teams/regions, identify gaps, reallocate resources
3. **Territory planning:** Review territory coverage, reassign accounts, balance load
4. **Quarterly business review:** Present results, analyze win/loss, plan next quarter
5. **Sales process audit:** Review stage progression, identify bottlenecks, optimize process

### Needs
- Executive dashboard (pipeline, forecast, bookings, team metrics)
- Territory and quota management
- Win/loss analysis with trend data
- Forecast accuracy tracking (compare forecast vs actual)
- Team comparison report
- Sales cycle analysis and benchmarking

---

## PERSONA 5: CHIEF REVENUE OFFICER (CRO)

| Attribute | Detail |
|-----------|--------|
| Title | Chief Revenue Officer |
| Reports To | CEO / Board |
| Team | Sales + CS + Marketing + RevOps |
| CRM Proficiency | Low — needs summaries, not details |
| Daily CRM Time | 15-30 min |
| Motivation | Predictable, growing revenue. Healthy funnel. Team alignment. |
| Frustration | Data is fragmented across tools. No single source of truth. |

### Core Workflows
1. **Monthly board prep:** Revenue metrics, pipeline coverage, NRR, churn
2. **Revenue review:** New bookings, renewals, expansion, contraction
3. **Funnel health:** Top-of-funnel volume, conversion rates, velocity
4. **Team alignment:** Sales handoff to CS, renewal coverage, churn signals
5. **Strategy planning:** Go-to-market analysis, segment penetration, growth initiatives

### Needs
- Revenue intelligence dashboard (not just pipeline)
- Historical trend analysis
- Cohort analysis (ARR by cohort, retention curves)
- Real-time revenue health score
- AI-powered insights (not just charts)

---

## PERSONA 6: CRM ADMINISTRATOR

| Attribute | Detail |
|-----------|--------|
| Title | CRM Administrator / Salesforce Admin |
| Employer Size | Mid-market to Enterprise |
| Technical Level | Medium-High (config, not code) |
| CRM Proficiency | Expert |
| Daily CRM Time | 6-8 hours |
| Motivation | Keep CRM running. Users happy. Data clean. |
| Frustration | Users break things. Data quality is poor. Request backlog. Changes require code. |

### Core Workflows
1. **User management:** Create/deactivate users, assign profiles/permissions, reset passwords
2. **Configuration:** Create/modify fields, layouts, workflows, validation rules
3. **Data management:** Import/export data, deduplication, data cleanup
4. **Report building:** Create custom reports for managers
5. **Integration setup:** Connect email, calendar, telephony, ERP
6. **Troubleshooting:** Investigate user issues, fix broken workflows
7. **Sandbox management:** Test changes before deploying

### Needs
- Drag-and-drop workflow builder (not code)
- Point-and-click entity/field creator
- Data import wizard with mapping, validation, rollback
- Bulk data operations (update, delete, merge)
- Change management with versioning and rollback
- Sandbox environments
- Audit log viewer
- Role/permission management UI

### IT Consulting Admin Variant
- Also configures: Engagement/SOW/resource types, project workflows, time entry approval chains
- Needs: Rate card management, resource skill mapping, utilization reports

### SaaS Admin Variant
- Also configures: Subscription/invoice types, MRR/churn workflows, health score calculations
- Needs: Product usage import, subscription lifecycle management

### Quotes
> "If I had a dollar for every time a user asked 'where did my data go?'..."
> "Salesforce gave me a job. But it gave me ulcers too."
> "I maintain 200 custom fields that nobody uses."

---

## PERSONA 7: REVENUE OPERATIONS (RevOps)

| Attribute | Detail |
|-----------|--------|
| Title | Revenue Operations Manager |
| Reports To | CRO |
| Teams Supported | Sales + Marketing + CS |
| Technical Level | High |
| CRM Proficiency | Expert |
| Daily CRM Time | 4-6 hours |
| Motivation | Clean data, accurate metrics, efficient processes. |
| Frustration | Siloed data systems. Manual data wrangling. No single source of truth. |

### Core Workflows
1. **Data governance:** Deduplication, data quality monitoring, enrichment
2. **Process optimization:** Analyze funnel metrics, identify bottlenecks, suggest improvements
3. **Integration management:** Maintain connections between CRM, billing, support, marketing
4. **Analytics:** Build executive reports, track KPIs, identify trends
5. **Tool stack management:** Evaluate, onboard, manage connected tools
6. **Sales compensation:** Track commission data, verify attainment

### Needs
- Data quality dashboard (scoring, trends, top issues)
- Funnel analysis with segment filters
- Integration health monitoring
- Custom report builder (no limitations)
- API access for programmatic operations
- Data transformation and normalization tools

---

## PERSONA 8: MARKETING MANAGER

| Attribute | Detail |
|-----------|--------|
| Title | Marketing Manager / Demand Gen Manager |
| Technical Level | Medium |
| CRM Proficiency | Medium |
| Daily CRM Time | 1-2 hours |
| Motivation | Show ROI. Generate qualified leads. Align with sales. |
| Frustration | Limited marketing automation in CRM. Poor lead tracking. Attribution is guesswork. |

### Core Workflows
1. **Campaign management:** Create campaign, set budget, track leads
2. **Lead capture:** Forms, landing pages, webinar registrations
3. **Lead nurturing:** Email sequences, drip campaigns, scored behavior
4. **Lead handoff:** Assign qualified leads to sales, track conversion
5. **Attribution:** Which campaigns drove revenue? Multi-touch attribution
6. **Performance reporting:** Campaign ROI, conversion rates, pipeline sourced

### Needs
- Campaign creation and tracking
- Email marketing (not just sequences)
- Form builder with CRM integration
- Lead scoring (behavioral + demographic)
- Attribution reporting (first-touch, last-touch, multi-touch)
- Landing page builder (basic)
- Marketing calendar

### Scope Decision
Marketing Automation is NOT in MVP. MVP covers: lead capture forms, campaign tracking fields, basic attribution (source/channel). Full Marketing Hub comes in Sprint 6+.

---

## PERSONA 9: CUSTOMER SUCCESS MANAGER

| Attribute | Detail |
|-----------|--------|
| Title | Customer Success Manager |
| Reports To | VP of Customer Success |
| Technical Level | Medium |
| CRM Proficiency | Medium |
| Daily CRM Time | 2-3 hours |
| Motivation | Retain customers. Drive expansion. Monitor health. |
| Frustration | No single view of customer health. Data spread across CRM + support + product. |

### Core Workflows
1. **Health scan:** Review customer health scores, identify at-risk accounts
2. **Outreach:** Reach out to at-risk accounts, schedule check-in calls
3. **QBR prep:** Gather customer data, prepare usage report, create presentation
4. **Renewal management:** Track upcoming renewals, engage early, identify blockers
5. **Expansion identification:** Identify upsell/cross-sell opportunities based on usage
6. **Escalation handling:** Flag issues to support, track resolution, confirm satisfaction

### Needs
- Customer health score (composite: product usage + support tickets + NPS + payment)
- Renewal calendar with risk indicators
- Usage data import from product analytics
- NPS/CES survey tool
- Communication history with customer
- Playbook engine (automated actions based on triggers)

---

## PERSONA 10: SUPPORT AGENT

| Attribute | Detail |
|-----------|--------|
| Title | Customer Support Agent |
| Reports To | Support Manager |
| Technical Level | Medium |
| CRM Proficiency | Medium |
| Daily CRM Time | 6-8 hours (ticket-focused) |
| Motivation | Resolve issues fast. Keep customers happy. Hit SLAs. |
| Frustration | Ticket systems are separate from CRM. No visibility into customer history. |

### Core Workflows
1. **Ticket triage:** Review new tickets, assess priority, assign
2. **Investigation:** Look up customer account, review product usage, check similar issues
3. **Resolution:** Respond to customer, troubleshoot, provide solution
4. **Escalation:** Escalate complex issues, track SLAs, follow up
5. **Documentation:** Create/update knowledge base articles
6. **Post-resolution:** Verify customer satisfaction, close ticket

### Needs
- Ticket management with SLA tracking
- Knowledge base (native)
- Macros/canned responses
- Customer 360 (account, contacts, deals, issues, history)
- Omni-channel inbox (email, chat, phone)
- CSAT survey integration

### Scope Decision
Support Hub (Tickets, KB, SLA, Omni-channel) is NOT in MVP. Sprint 7+.

---

## PERSONA 11: VP OF CUSTOMER SUCCESS

| Attribute | Detail |
|-----------|--------|
| Title | VP of Customer Success |
| Reports To | CRO / CEO |
| Team Size | 10-50 CSMs |
| Technical Level | Medium |
| CRM Proficiency | Medium (dashboards, reports) |
| Daily CRM Time | 30-60 min |
| Motivation | Retention, expansion, NRR growth. |
| Frustration | No unified customer data. CS metrics require manual work. |

### Core Workflows
1. **Renewal forecast:** Review upcoming renewals, risk ratings, coverage plan
2. **Health score review:** Team-wide health distribution, segment trends
3. **NRR analysis:** Expansion vs contraction analysis, churn root cause
4. **Team performance:** CSM activity, QBR completion, satisfaction scores
5. **Escalation management:** Review escalated accounts, intervention plans

### Needs
- Executive CS dashboard (NRR, churn, health, renewal coverage)
- NRR waterfall chart
- Churn analysis with root cause breakdown
- Cohort retention analysis
- Team activity and performance metrics

---

## PERSONA 12: IT / DEVELOPER

| Attribute | Detail |
|-----------|--------|
| Title | IT Manager / Integration Developer |
| Reports To | CTO / VP Engineering |
| Technical Level | High |
| CRM Proficiency | Low (views CRM as system to integrate) |
| Daily CRM Time | 30-60 min |
| Motivation | Keep systems connected. Data flowing. No outages. |
| Frustration | API limitations. Poor documentation. Proprietary technologies. |

### Core Workflows
1. **Integration management:** Maintain connections between CRM and other systems
2. **API development:** Build custom integrations using REST/GraphQL APIs
3. **Data migration:** Import/export data between systems
4. **Monitoring:** Monitor API usage, error logs, sync health
5. **Custom development:** Build custom features using the platform API

### Needs
- Open API (REST + GraphQL)
- Webhook framework with retry
- API documentation (OpenAPI spec)
- Event logs and monitoring
- Rate limit management (or no limits on self-hosted)
- Data export tools (full data access)
- Sandbox for testing integrations

### Quotes
> "I cannot believe Salesforce requires Apex to do this."
> "If the API is good, I can build anything. If it is bad, nothing works."
> "Open source means I can fix things myself. That is priceless."

---

## PERSONA 13: CISO / COMPLIANCE OFFICER

| Attribute | Detail |
|-----------|--------|
| Title | Chief Information Security Officer |
| Reports To | CEO / Board |
| Technical Level | High |
| CRM Proficiency | Very Low (cares about security, not features) |
| Daily CRM Time | 15 min |
| Motivation | Data security. Compliance. Audit readiness. |
| Frustration | Cloud CRMs cannot guarantee data isolation. Audit logs are incomplete. |

### Core Workflows
1. **Security review:** Review security controls, access logs, encryption
2. **Audit preparation:** Export audit logs, review user access, verify compliance
3. **Policy enforcement:** Ensure RBAC matches policy, monitor admin actions
4. **Incident response:** Investigate suspicious activity, revoke access, document
5. **Vendor assessment:** Review CRM provider security (if cloud-hosted)

### Needs
- Self-hosted deployment option (data never leaves our network)
- Field-level encryption (PII, PCI, PHI)
- Full event-sourced audit trail (every change, every read)
- Role-based access control with field-level security
- Session management and SSO (SAML, OIDC)
- Data retention and deletion policies
- Export all customer data (data portability)

### This Persona BUYS Sovereign CRM
CISO is the decision-maker who blocks Salesforce/HubSpot because of privacy concerns.

---

## PERSONA 14: CEO / BUSINESS OWNER

| Attribute | Detail |
|-----------|--------|
| Title | CEO / Founder / Business Owner |
| Technical Level | Low-Medium |
| CRM Proficiency | Very Low |
| Daily CRM Time | 10-15 min |
| Motivation | Revenue visibility. Team productivity. Business intelligence. |
| Frustration | Cannot trust the numbers. Reports take too long. Data quality is poor. |

### Core Workflows
1. **Revenue check:** View pipeline, forecast, bookings, cash flow
2. **Team check:** Review team performance, identify gaps, assign resources
3. **Customer check:** View health scores, churn trends, satisfaction
4. **Strategy review:** Market trends, win/loss analysis, competitive positioning
5. **Investment decisions:** Where to invest

### Needs
- Executive dashboard (5-minute summary)
- AI executive summary: "Here is what happened yesterday, here is what is at risk today"
- Mobile push notifications for key events
- Email-delivered daily digest (no login required)
- Trusted, accurate data (no manual compilation)

---

## PERSONA 15: PARTNER / RESELLER

| Attribute | Detail |
|-----------|--------|
| Title | Partner Manager / Channel Partner |
| Reports To | VP of Partnerships |
| Technical Level | Medium |
| CRM Proficiency | Medium |
| Daily CRM Time | 1-2 hours |
| Motivation | Manage partner relationships. Track deal registration. |
| Frustration | Partner management is an afterthought in most CRMs. |

### Core Workflows
1. **Partner management:** Onboard partners, track relationship, manage agreements
2. **Deal registration:** Partners register deals, track approval, monitor progress
3. **Commission tracking:** Track partner commissions, payments, performance
4. **Partner portal:** Self-service access for partners
5. **Performance reports:** Partner sales activity, deal registration conversion

### Needs
- Partner portal (self-service)
- Deal registration workflow
- Commission tracking and reporting
- Partner performance dashboard
- Contract and agreement management

### Scope Decision
Partner management is post-MVP. Sprint 9+.

---

## PERSONA 16: CONSULTANT (IT CONSULTING VERTICAL)

| Attribute | Detail |
|-----------|--------|
| Title | Consultant / Senior Consultant / Architect |
| Employer | IT Services/Consulting firm |
| Technical Level | High |
| CRM Proficiency | Low (CRM is for sales, not delivery) |
| Daily CRM Time | 15-30 min (time entry + notes) |
| Motivation | Track billable hours. Log deliverables. Communicate with client. |
| Frustration | Time tracking is separate from CRM. No visibility into project health. |

### Core Workflows
1. **Time entry:** Log hours to project/client, categorize as billable/non-billable
2. **Deliverable log:** Submit work products, track review status
3. **Project communication:** Log client interactions, document decisions
4. **Expense tracking:** Log travel, software, other billable costs
5. **Status updates:** Update project status, flags, risks

### Needs
- Quick time entry (timer, manual, weekly view)
- Project dashboard: deliverables, milestones, hours
- Expense logging with receipt upload
- Client communication history
- Personal utilization tracking

### Quotes
> "I forget to log my hours and then spend Friday catching up."
> "Why cannot the CRM track my projects the way Jira does?"

---

## PERSONA 17: DELIVERY MANAGER (IT CONSULTING VERTICAL)

| Attribute | Detail |
|-----------|--------|
| Title | Delivery Manager / Engagement Manager |
| Reports To | Practice Head / VP Delivery |
| Technical Level | Medium-High |
| CRM Proficiency | Medium |
| Daily CRM Time | 1-2 hours |
| Motivation | Deliver on time, on budget. Manage resources. Client satisfaction. |
| Frustration | Resource allocation is manual. Project profitability is unclear. |

### Core Workflows
1. **Resource allocation:** Assign consultants to projects, balance workload
2. **Project health:** Review timeline, budget, milestones, risks, issues
3. **Time approval:** Review and approve team time entries
4. **Client communication:** Review engagement status, governance meetings
5. **Change management:** Process change orders, scope changes, budget adjustments
6. **Invoicing:** Review billable hours and expenses, send to billing

### Needs
- Resource dashboard: allocation %, availability, skills
- Project P&L: budget vs actual, margin by project
- Time entry approval workflow
- Milestone tracking with status
- Change order workflow
- Client governance report generator

### Quotes
> "I have 15 consultants on 8 projects and I manage it all in spreadsheets."
> "By the time I see a project is over budget, it is too late."

---

## PERSONA PROFILE DISTRIBUTION

| Persona | Vertical | MVP | Sprint 3 | Sprint 6 | Sprint 9+ |
|---------|----------|:---:|:--------:|:--------:|:---------:|
| 1. SDR/BDR | Both | YES | | | |
| 2. Account Executive | Both | YES | | | |
| 3. Sales Manager | Both | YES | | | |
| 4. VP of Sales | Both | YES | | | |
| 5. CRO | Both | | YES | | |
| 6. CRM Admin | Both | YES | | | |
| 7. RevOps | Both | | YES | | |
| 8. Marketing Manager | Both | | | YES | |
| 9. CSM | SaaS | | | YES | |
| 10. Support Agent | Both | | | | YES |
| 11. VP Customer Success | SaaS | | | YES | |
| 12. IT/Developer | Both | YES | | | |
| 13. CISO | Both | YES | | | |
| 14. CEO | Both | YES | | | |
| 15. Partner Manager | Both | | | | YES |
| 16. Consultant | IT Consulting | | YES | | |
| 17. Delivery Manager | IT Consulting | | YES | | |

---

## PERSONA-DRIVEN DESIGN RULES

1. **Every new feature maps to at least one persona.** If no persona needs it, it is not built.
2. **Prioritize by persona density** — features serving Personas 1-6 and 12-14 (MVP) ship first.
3. **Test every UI change against Persona 1 (SDR)** — more than 2 clicks to log an activity = redesign.
4. **Test every report against Persona 3 (Sales Manager)** — cannot find answer in 10 seconds = simplify.
5. **Test every admin feature against Persona 6 (CRM Admin)** — if it requires code, they will not use it.
6. **Persona 13 (CISO) is our wedge persona** — their privacy requirements are why enterprises choose us.
