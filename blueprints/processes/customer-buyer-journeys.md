# Phase 9: Customer & Buyer Journeys

**Created:** 2026-06-06
**Purpose:** Full lifecycle maps for IT Consulting buyers, SaaS buyers, and their end-customers. Multi-stakeholder journey maps with gates, emotions, and system touchpoints.

---

## 1. DESIGN PRINCIPLES

| Principle | Application |
|-----------|-------------|
| **Map both buyer AND end-customer** | The CRM serves both. IT Consulting firms have buyers (clients) and end-customers (their users). |
| **Multi-stakeholder per decision** | Enterprise sales = 5-15 stakeholders. Each has different needs. |
| **Emotional journey matters** | CRM features at moments of frustration = adoption. Features at moments of delight = advocacy. |
| **Gates are where deals die** | Every gate is a handoff/approval. These need workflow support. |
| **Journey ≠ linear** | Real journeys loop back, stall, accelerate. CRM must handle all paths. |

---

## 2. IT CONSULTING BUYER JOURNEY

### Market: IT Services / Digital Transformation / Staff Augmentation

### Stakeholder Map

| Stakeholder | Role in Decision | Pain Point | Our CRM Feature |
|-------------|-----------------|------------|-----------------|
| **VP Engineering / CTO** | Technical decision-maker | Needs proof of delivery capability | Case studies, resource skill profiles, past engagement outcomes |
| **Procurement Manager** | Gatekeeper | Needs compliance, PO tracking, vendor management | SOW management, PO tracking, rate card audit trail |
| **Delivery Head** | Evaluator | Needs to assess resource availability | Resource planner, skill/capacity view, bench visibility |
| **Legal / Compliance** | Blocker | Data privacy, contract terms, liability | Data residency, encryption, contract template library |
| **Finance / CFO** | Economic buyer | Budget control, predictable costs, ROI | Budget tracking, milestone billing, P&L per engagement |

### Journey Map: IT Consulting Buyer

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: AWARENESS (14-60 days)  Emotion: 🔍 Curious → 😟 Concerned            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  TRIGGERS:                                                                      │
│  • Company needs new capability (cloud migration, AI, new tech stack)           │
│  • Internal team is overloaded / lacks skills                                   │
│  • Failed delivery from existing vendor                                         │
│  • Competitive pressure (rival launched faster)                                 │
│                                                                                  │
│  STAKEHOLDER ACTIVITIES:                                                        │
│  CTO:          Researches firms → reads case studies → checks LinkedIn          │
│  Delivery Head: Asks peers → reviews analyst reports (Gartner, Forrester)       │
│  Procurement:  Reviews existing vendor list → checks quals                      │
│                                                                                  │
│  CRM TOUCHPOINT: Content tracking, website visit → Lead created                 │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: EVALUATION (30-90 days)  Emotion: 🧐 Analytical → ⚠️ Cautious          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • RFP/RFI issued → 3-5 firms invited to bid                                   │
│  • Capability presentation by AE + Delivery Manager                             │
│  • Reference calls with similar clients                                         │
│  • Technical deep-dive with proposed architect                                  │
│  • Rate card review and negotiation                                             │
│                                                                                  │
│  KEY QUESTION: "Can they deliver on time, on budget, with our quality?"          │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • Deal tracking with engagement type = 'IT Consulting'                        │
│  • SOW draft shared and iterated                                                │
│  • Resource skill profiles shared via portal                                    │
│  • Past engagement outcomes as case studies (in CRM)                            │
│                                                                                  │
│  GATES:                                                                         │
│  │  Gate 1: CTO signs off on technical capability → Continue                   │
│  │  Gate 2: Procurement approves commercial terms → SOW issued                 │
│  │  Gate 3: Legal approves contract → Deal moves to Negotiation                │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: DECISION (14-45 days)  Emotion: 🤔 Weighing → 😬 Nervous              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Final commercial negotiation (rates, milestones, payment terms)              │
│  • Resource confirmation: named resources proposed                              │
│  • SOW final version with all appendices                                        │
│  • Contract signing (e-sign)                                                    │
│  • PO issuance                                                                  │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • SOW approval workflow in CRM                                                 │
│  • Contract generation from template                                            │
│  • Resource allocation created in CRM                                           │
│  • E-sign integration (DocuSign)                                                │
│                                                                                  │
│  WIN: Deal closed won → Engagement created → Resources allocated                │
│  LOSE: Win/loss reason logged → Nurture sequence for re-engagement              │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 4: ONBOARDING (30-60 days)  Emotion: 😌 Relief → 🤝 Hopeful               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Kick-off meeting (delivery team + client stakeholders)                        │
│  • Knowledge transfer sessions                                                  │
│  • Environment access and tooling setup                                         │
│  • First milestone planning                                                     │
│  • Governance cadence defined (weekly status, monthly steering)                 │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • Engagement status = Active                                                   │
│  • Kick-off meeting logged as Activity                                          │
│  • Milestone tracker created                                                    │
│  • Resource time tracking begins                                                │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 5: DELIVERY (90-365+ days)  Emotion: 📊 Mixed → 📈 Confident             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Weekly status reports                                                        │
│  • Sprint delivery and demos                                                    │
│  • Milestone achievement and invoicing                                          │
│  • Change order processing (scope changes)                                      │
│  • Governance meetings (monthly steering committee)                             │
│  • Timesheet submission weekly                                                  │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • Weekly timesheet approval cycle                                              │
│  • Milestone completion → Invoice generation                                    │
│  • Change order workflow from draft to approval                                 │
│  • Monthly P&L review per engagement                                            │
│  • Resource utilization tracking                                                │
│                                                                                  │
│  HEALTH CHECKPOINTS:                                                            │
│  • Monthly: Engagement health score (schedule, budget, quality, relationship)   │
│  • Quarterly: Executive sponsor check-in                                        │
│  • 90-days before engagement end: Renewal/expansion planning                    │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 6: RENEWAL / EXPANSION (30-90 days before end)  😊 Confident → 🚀 Excited│
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Engagement performance review (metrics, outcomes, feedback)                  │
│  • Expansion opportunity identification (new projects, add-ons)                 │
│  • New SOW for phase 2 / adjacent work                                          │
│  • Reference case creation                                                      │
│  • NPS/CSAT survey                                                              │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • Engagement health score triggers renewal workflow                            │
│  • New Deal created from expansion opportunity                                  │
│  • Reference case stored in CRM (attached to Organization)                      │
│  • NPS survey sent, response logged                                             │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. SAAS BUYER JOURNEY

### Market: B2B SaaS / Subscription Software (Sales, Marketing, CS tools)

### Stakeholder Map

| Stakeholder | Role | Pain | CRM Feature |
|-------------|------|------|-------------|
| **VP Sales / CRO** | Economic buyer | Need predictable revenue, pipeline visibility | Pipeline management, forecasting, AI insights |
| **RevOps Manager** | Evaluator/Implementer | Need clean data, automation, integration | Data quality, workflows, API, integrations |
| **Sales Manager** | User/Champion | Need team visibility, coaching | Team dashboards, activity reports, deal inspection |
| **CISO** | Blocker | Data security concerns | Self-hosted, encryption, audit, RBAC |
| **Sales Reps** | End-user adoption | CRM is overhead | 2-click logging, AI automation, mobile |
| **IT Admin** | Implementer | Need easy config, integration | Dynamic objects, import wizard, webhooks |

### Journey Map: SaaS Buyer

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: PROBLEM AWARENESS (7-30 days)  Emotion: 😤 Frustrated → 🔍 Curious    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  TRIGGER:                                                                       │
│  • "My Salesforce bill is $200k/year and my reps hate it"                       │
│  • "HubSpot went down again and we can't find our pipeline data"                │
│  • "I'm managing deals in spreadsheets — we're a $10M company now"              │
│  • "We need a CRM for our IT Consulting business but everything is overkill"    │
│                                                                                  │
│  STAKEHOLDER ACTIVITIES:                                                        │
│  CRO:  Searches "open source CRM alternatives" → finds Sovereign CRM           │
│        Reads landing page → "Self-hosted, $0 core, local-first"                 │
│  CISO: Checks security page → "Open source = auditable. Self-host = our data."  │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: SOLUTION EVALUATION (14-45 days)  Emotion: 🤔 Analytical → ⚠️ Wary    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Feature comparison (Sovereign vs Salesforce vs HubSpot vs Zoho)              │
│  • Architecture review: "Is this enterprise-grade?"                            │
│  • Security review: "Where is data stored? Encryption? Audit?"                 │
│  • Integration assessment: "Does it connect to our stack?"                     │
│  • Demo request / trial setup                                                   │
│                                                                                  │
│  KEY QUESTION: "Is this production-ready? Will it grow with us?"                │
│                                                                                  │
│  GATES:                                                                         │
│  │  Gate 1: RevOps validates features match requirements → Continue            │
│  │  Gate 2: CISO approves security posture → Technical eval cleared            │
│  │  Gate 3: CRO approves budget (infra cost for self-hosted) → Purchase        │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: TECHNICAL EVALUATION (14-30 days)  Emotion: 🧑‍💻 Hands-on → 😬 Critical │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • IT admin deploys trial instance (Docker Compose → 15 min)                    │
│  • Import sample data (CSV from existing CRM)                                   │
│  • Configure: custom fields, layouts, workflows                                 │
│  • Test integrations: email, calendar, API webhooks                             │
│  • Review audit logs, RBAC setup                                                │
│                                                                                  │
│  CRM TOUCHPOINTS:                                                               │
│  • Self-hosted deployment (no sales call needed)                                │
│  • Import wizard with Salesforce/HubSpot mapper                                 │
│  • API playground in docs                                                       │
│  • MCP server test (AI agent setup)                                            │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 4: PURCHASE (7-14 days)  Emotion: ✅ Confident → 📋 Procedural           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Choose tier (Self-hosted Free vs Enterprise with support)                    │
│  • Payment for enterprise tier / support contract                               │
│  • Tenant provisioning (if cloud) / License key (if self-hosted)                │
│  • Onboarding session with RevOps                                               │
│                                                                                  │
│  CRM TOUCHPOINT: Subscription record created                                    │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 5: ONBOARDING & ADOPTION (30-90 days)  Emotion: 🚀 Excited → 😤 Speed bump│
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Full data migration from old CRM                                             │
│  • Configure all objects, fields, workflows for production                      │
│  • User training (SDRs, AEs, Managers, Admin)                                   │
│  • Roll out in phases: 1 team first → company-wide                              │
│  • Set up integrations: email, calendar, telephony, billing                     │
│                                                                                  │
│  ADOPTION CHECKPOINTS:                                                          │
│  • Week 1: "Did every SDR log activity today?"                                 │
│  • Week 4: "Are managers using pipeline reports?"                               │
│  • Week 8: "Is forecasting being done in CRM?"                                 │
│                                                                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 6: EXPANSION (90+ days)  Emotion: 📈 Growing → 💪 Empowered              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ACTIVITIES:                                                                    │
│  • Add more teams/departments                                                  │
│  • Enable AI MCP agent for automation                                            │
│  • Build custom objects for vertical-specific needs                             │
│  • Connect additional integrations                                               │
│  • Provide case studies / testimonials                                          │
│  • Become reference account                                                     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. IT CONSULTING END-CUSTOMER JOURNEY

(Buyer of IT services and their internal customers — the users of the delivered system)

```
PROJECT INITIATION ──► REQUIREMENTS ──► BUILD ──► TEST ──► DEPLOY ──► OPERATE ──► SUPPORT
       │                    │              │        │         │          │            │
       ▼                    ▼              ▼        ▼         ▼          ▼            ▼
   Signed SOW          Spec review     Sprint    UAT      Go-live   Hypercare    BAU support
   Kick-off            Stakeholder    demos     sign-off            period       steady state
   Resource named      interviews                          
```

**CRM Touchpoints by Phase:**
- Initiation: Engagement created, resources allocated
- Requirements: Meeting notes, decision log
- Build: Milestone tracking, weekly status reports
- Deploy: UAT sign-off milestone
- Operate: Timesheet billing, expense tracking
- Support: Ticket creation (when support module active)

---

## 5. SAAS END-CUSTOMER JOURNEY

(End-users of the SaaS product whose teams are CRM users)

```
SIGN UP ───► ONBOARDING ──► ACTIVE USE ──► EXPAND ──► RENEW ──► ADVOCATE
   │             │              │             │         │          │
   ▼             ▼              ▼             ▼         ▼          ▼
Trial start   Setup wizard   Daily/Weekly   Add       Auto or   Reference,
Welcome email Training       usage          users/    manual    Case study
                             Feature        features  renewal   NPS 9-10
                             adoption                            
```

**CRM Touchpoints:**
- Sign up: Lead/Contact created from signup
- Onboarding: Sequence enrollment (welcome, training)
- Active use: Health score calculation, usage data import
- Expand: CSM triggers upsell workflow
- Renew: Renewal process auto-runs
- Advocate: NPS survey → reference request

---

## 6. BUYER JOURNEY VS CRM FEATURE MAP

| Journey Phase | Stakeholder Need | CRM Feature | Module |
|---------------|-----------------|-------------|--------|
| Awareness | "Show me similar case studies" | Content tracking, Lead source | Core |
| Evaluation | "Show me capability evidence" | Deal with engagement docs, resource profiles | Core + ITC |
| Evaluation (CISO) | "Prove you are secure" | Self-hosted, audit logs, encryption, RBAC | Admin |
| Technical Eval | "Can I configure it myself?" | Dynamic objects, import wizard, API | Admin |
| Purchase | "Simple procurement" | Subscription management, invoice | SaaS |
| Onboarding | "Get my team using it" | Activity import, user management, training | Admin |
| Delivery (ITC) | "Are we on track?" | Engagement health, P&L, timesheets | ITC |
| Delivery (SaaS) | "Is the product working?" | Health score, usage, NPS | SaaS |
| Renewal | "Should we continue?" | Renewal management, success metrics | SaaS |
| Expansion | "What else can we do?" | Expansion identification, cross-sell | SaaS/ITC |

---

## 7. JOURNEY FAILURE POINTS

| Failure Point | Why It Happens | CRM Mitigation |
|---------------|----------------|----------------|
| **Stakeholder lost** | Champion leaves company during sales cycle | Alert on contact job change, auto-reassign |
| **Procurement stall** | Legal/Procurement unreachable | Stakeholder matrix with roles, auto-reminder |
| **Post-sale handoff drops** | CSM doesn't get full context from AE | Activity history copied to Engagement/Subscription |
| **SOW scope creep** | Uncontrolled changes | Change order workflow with approval |
| **Champion leaves** | No relationship at new buyer | Account plan with multi-threaded contacts |
| **Low user adoption** | CRM seen as overhead | Persona-driven UX, 2-click rule, gamification |
| **Data quality decays** | No governance | Data quality dashboard, validation rules |
| **Stale pipeline** | Reps don't update stages | Activity-based stage validation, AI stale detection |

---

*Phase 9 complete. Customer and buyer journeys mapped for both verticals across full lifecycle with stakeholder maps and failure points. Next: Phase 10 — API Architecture & Integrations.*
