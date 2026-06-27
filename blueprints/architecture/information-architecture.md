# Phase 4: Information Architecture

**Created:** 2026-06-06
**Purpose:** Main menus, submenus, tabs, screens — the complete navigation structure of Sovereign CRM.

---

## 1. NAVIGATION DESIGN PRINCIPLES

| Principle | Application |
|-----------|-------------|
| **Persona-driven** | Most-used features for Personas 1,2,3,6,12,13,14 are 1 click away |
| **Progressive disclosure** | Start simple, reveal complexity on demand |
| **Role-adaptive** | Menu changes based on user role and permissions |
| **Vertical-aware** | IT Consulting users see Project objects; SaaS users see Subscription objects |
| **Search-first** | Global search is accessible from every screen (Cmd+K / Ctrl+K) |
| **Mobile-responsive** | Same IA, adapted for mobile with bottom navigation |

---

## 2. GLOBAL NAVIGATION (TOP-LEVEL MENU)

### Main Navigation Bar (Desktop)
```
[Home] [Pipeline] [Contacts] [Deals] [Activities] [Reports] [Admin] [Cmd+K Search] [Avatar/Profile]
```

### Bottom Navigation (Mobile)
```
[Home] [Pipeline] [Contacts] [Deals] [More...]
```

---

## 3. MAIN MENU EXPANSION

### 3.1 HOME Dashboard

**Purpose:** Persona-specific landing page. What the user sees first.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [Welcome, {Name}]                                           │
│  [Persona Role Selector: SDR / AE / Manager / Admin / ...]  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Pipeline    │  │ My Tasks    │  │ Upcoming    │        │
│  │ Summary     │  │ (Today)     │  │ Meetings    │        │
│  │ [+ Pie Viz] │  │ [5 items]   │  │ [3 today]   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Activity Feed (Last 20 interactions across all     │  │
│  │  accounts, deals, leads)                            │  │
│  │  [Activity] [Activity] [Activity] ...               │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Quick Stats │  │ AI Insight  │  │ Recently    │        │
│  │ (Deals Won) │  │ ("3 deals   │  │ Viewed      │        │
│  │             │  │  stale >7d")│  │ [Contacts]  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Home Widgets (Configurable):**
- Pipeline summary card (value, count by stage)
- My tasks (today's follow-ups, activities)
- Upcoming meetings (next 5, from calendar sync)
- Activity feed (most recent 20 across all entities)
- Quick stats (deals won this month, calls made today)
- AI Insight card (one AI-generated observation)
- Recently viewed (5 most recent records across all entities)
- Team activity (Manager/SDR: team calls, emails, meetings today)

---

### 3.2 CONTACTS (People)

**Entity Types:** Contact, Lead, Organization

```
Contacts
├── All Contacts
│   ├── List View (table: name, org, email, phone, owner, last activity)
│   ├── Kanban View (by status/owner/pipeline)
│   └── Map View (geographic distribution)
├── Organizations
│   ├── List View (table: name, industry, revenue, employee count, owner)
│   └── Hierarchy View (org chart / parent-child tree)
├── Leads (Untouched / In Progress / Disqualified)
│   ├── List View
│   └── Kanban View (by lead status)
└── [Quick Actions]
    ├── + New Contact
    ├── + New Organization
    └── + Import Contacts
```

**Contact Detail Screen (Tabs):**
```
[Summary] [Activity] [Deals] [Emails] [Notes] [Files] [Related]
```

| Tab | Contents |
|-----|----------|
| Summary | Key fields, quick actions, AI summary, activity snapshot |
| Activity | Timeline of calls, emails, meetings, notes (reverse chronological) |
| Deals | Related deals, won/lost/in-progress |
| Emails | Email history (synced) |
| Notes | All notes attached to this contact |
| Files | Attachments, documents, proposals |
| Related | Linked organizations, other contacts at same org |

---

### 3.3 DEALS (Opportunities)

```
Deals
├── Pipeline View
│   ├── Kanban Board (columns = stages)
│   │   ├── Drag-and-drop between stages
│   │   ├── Card detail: name, amount, contact, probability, age
│   │   └── Color coding: green (on track), yellow (stale), red (at risk)
│   └── Horizontal scroll for pipelines with many stages
├── List View
│   ├── Table: name, amount, stage, probability, close date, owner
│   ├── Sortable by any column
│   └── Filters: by stage, owner, amount range, close date range, age
├── Forecast View
│   ├── By rep (Manager/VP: team rollup)
│   ├── By stage (commit, best case, pipeline)
│   ├── By quarter
│   └── Confidence scoring (AI-adjusted)
├── Won Deals
│   └── Closed won list with reason, amount, close date
├── Lost Deals
│   └── Closed lost list with reason, competitor, amount
└── [Quick Actions]
    ├── + New Deal
    └── + Import Deals
```

**Deal Detail Screen (Tabs):**
```
[Summary] [Activity] [Contacts] [Products] [Documents] [Notes] [AI Insights] [Related]
```

| Tab | Contents |
|-----|----------|
| Summary | Key fields, AI risk assessment, next best action, deal timeline |
| Activity | Timeline of all interactions |
| Contacts | Associated contacts (buyer, champion, decision-maker, blocker) |
| Products | Products/services, quantities, discounts, total |
| Documents | Proposals, quotes, contracts attached |
| Notes | All notes |
| AI Insights | AI-generated: risk flags, next steps, similar deals, win probability |
| Related | Related organizations, support tickets, projects |

**Deal Card Fields (Kanban):**
```
┌─────────────────────────────────────┐
│ [Deal Name]                         │
│ $50,000  |  Close: 2026-07-15      │
│ Acme Corp  |  John Smith            │
│ [Stale: 12d]  (color: yellow)       │
│ [Last: Check-in call, Jun 1]        │
└─────────────────────────────────────┘
```

---

### 3.4 PIPELINE (Aggregated)

```
Pipeline
├── Funnel Visualization
│   ├── Leads → MQL → SQL → Opportunity → Proposal → Negotiation → Closed Won
│   └── Conversion rates between each stage
├── Stage Breakdown
│   ├── Value by stage (bar chart)
│   ├── Count by stage
│   └── Weighted pipeline value (amount x probability)
├── Velocity Report
│   ├── Average days in each stage
│   ├── Compare by rep, team, product
│   └── Trend over time (weekly/monthly)
└── Filters
    ├── By date range
    ├── By owner/team
    └── By product line
```

---

### 3.5 ACTIVITIES

```
Activities
├── My Activities (Today / This Week / This Month)
│   ├── Calls (logged, duration, outcome)
│   ├── Emails (sent, received, tracked opens/clicks)
│   ├── Meetings (upcoming, past, with notes)
│   ├── Tasks (to-do, overdue, completed)
│   └── Notes (all entities)
├── Team Activities (Manager+ — all team members)
│   └── Same sub-menus as above, filtered by team
├── Calendar Sync
│   ├── Connected calendars (Google, Outlook)
│   ├── Meeting auto-logging
│   └── Availability view
├── Sequences
│   ├── Active sequences (running)
│   ├── Sequence templates (drafts)
│   ├── Sequence stats (open rate, reply rate, click rate)
│   └── + New Sequence
└── [Quick Actions]
    ├── + Log Call
    ├── + Log Email
    ├── + Schedule Meeting
    ├── + Add Task
    └── + Write Note
```

**Activity Detail Screen:**
```
[Type Icon] [Subject/Title]
[Date/Time] [Duration] [Owner]
[Related To: Contact, Deal, Organization]
[Description / Notes]
[Attachments]
```

---

### 3.6 REPORTS

```
Reports
├── Dashboards
│   ├── Executive Dashboard (CEO/CRO view)
│   ├── Sales Manager Dashboard
│   ├── Rep Performance Dashboard
│   ├── Pipeline Dashboard
│   ├── Activity Dashboard
│   └── + New Dashboard
├── Standard Reports
│   ├── Pipeline Report (value by stage, by rep, by quarter)
│   ├── Forecast Report (commit vs best case vs pipeline)
│   ├── Win/Loss Report (by rep, by reason, by competitor)
│   ├── Activity Report (calls, emails, meetings per rep per period)
│   ├── Conversion Report (lead → MQL → SQL → Opp → Won)
│   ├── Sales Cycle Report (avg days by stage, by rep)
│   └── Team Performance Report
├── Custom Reports
│   ├── Report Builder (drag-and-drop: filters, groupings, metrics)
│   ├── Saved Reports
│   └── Scheduled Reports (email delivery daily/weekly/monthly)
└── [Quick Actions]
    ├── + New Dashboard
    ├── + New Report
    └── + Schedule Report
```

**Report Builder:**
```
┌─────────────────────────────────────────────┐
│ Report Builder                              │
├─────────────────────────────────────────────┤
│ Data Source: [Deals▼]                        │
│                                              │
│ Filters:                                     │
│  + [Stage] [Equals] [Closed Won]            │
│  + [Close Date] [Between] [Jan 1 - Dec 31] │
│                                              │
│ Group By: [Owner▼]  [Stage▼]                │
│                                              │
│ Metrics:                                     │
│  + [Sum] [Amount]                           │
│  + [Count] [ID]                             │
│  + [Average] [Days in Stage]                │
│                                              │
│ Visualize: [Bar Chart▼]  [Table▼]           │
│                                              │
│ [Preview] [Save] [Schedule] [Export CSV]    │
└─────────────────────────────────────────────┘
```

---

### 3.7 ADMINISTRATION

```
Admin
├── Users
│   ├── All Users
│   │   ├── List View (name, email, role, status, last login)
│   │   └── Detail View (profile, permissions, teams, activity)
│   ├── Roles (Administrator, Manager, Rep, Read-Only, Custom)
│   │   └── Role Editor (entity permissions, field permissions, action permissions)
│   ├── Teams (group users for sharing, reporting)
│   └── + New User
├── Permissions
│   ├── Permission Sets (named collections of permissions)
│   ├── Field-Level Security (which fields are visible/editable by role)
│   ├── Record Sharing Rules (territory, team, role-based)
│   └── Login Policies (IP restrictions, MFA requirements, session timeout)
├── Entity Manager (DYNAMIC OBJECT BUILDER)
│   ├── Entity Types (all entities: standard + custom)
│   │   ├── Standard: Contact, Organization, Deal, Lead, Activity
│   │   ├── Vertical: Engagement, SOW, Subscription, Invoice
│   │   └── Custom: [User-Defined]
│   ├── Field Definitions
│   │   ├── Field types: Text, Long Text, Number, Currency, Date, DateTime, Boolean
│   │   │                 Picklist (single/multi), Lookup (relation), Formula
│   │   │                 Email, Phone, URL, Address, Auto-Number, Image, File
│   │   ├── Validation Rules (field-level expressions)
│   │   └── Field Dependencies (picklist filtering)
│   ├── Layouts
│   │   ├── Page Layouts (which fields on which tabs)
│   │   ├── Compact Layouts (card/Kanban view)
│   │   └── Search Layouts (which fields in search results)
│   ├── Relationships (between entity types)
│   └── Pipelines (stage definitions per entity)
├── Workflows
│   ├── Workflow Rules (when X happens, do Y)
│   │   ├── Trigger: Before/After Create, Update, Delete, Stage Change
│   │   ├── Condition: Field match, Formula true, Time-based
│   │   └── Action: Update field, Create record, Send email, Call webhook
│   ├── Approval Processes
│   │   ├── Approval Chain (multi-level, parallel)
│   │   ├── Delegation Rules
│   │   ├── Escalation Rules (time-based)
│   │   └── Email Notifications
│   ├── Workflow Templates
│   └── Workflow Monitor (active instances, failures, history)
├── Pipelines & Stages
│   ├── Default Pipelines (per entity)
│   ├── Multi-Pipeline Support (different deal types = different pipelines)
│   ├── Stage Configuration (name, probability range, required fields)
│   └── Stage Transitions (which stages can move to which)
├── Formulas & Functions
│   ├── Formula Editor (calculate fields, validation rules)
│   ├── Formula Functions (math, text, date, logical, aggregate)
│   └── Formula Test Bench
├── Data Management
│   ├── Import Wizard
│   │   ├── Source: CSV, Excel, Salesforce, HubSpot, API
│   │   ├── Field Mapping (drag-and-drop)
│   │   ├── Duplicate Detection
│   │   ├── Preview & Validate (10 rows preview with errors)
│   │   └── Execute & Rollback (if errors)
│   ├── Export Wizard
│   │   ├── Select entities, fields, filters
│   │   ├── Format: CSV, Excel, JSON, XML
│   │   └── Schedule recurring export
│   ├── Duplicate Management
│   │   ├── Duplicate Rules (matching criteria per entity)
│   │   ├── Merge Wizard (which record survives, field-level choices)
│   │   └── Duplicate Dashboard (recent duplicates found, resolved)
│   ├── Data Quality
│   │   ├── Data Quality Score (per record and per entity)
│   │   ├── Data Health Dashboard (% complete, % valid, % duplicates)
│   │   └── Data Enrichment (auto-fill from public APIs)
│   └── Data Retention Policies
├── Integrations
│   ├── Email (IMAP/SMTP config, Gmail/Outlook OAuth)
│   ├── Calendar (Google Calendar, Outlook)
│   ├── Telephony (Twilio, VoIP providers)
│   ├── Webhooks (inbound and outbound)
│   ├── API Keys (REST, GraphQL)
│   └── Connectors (pre-built: Stripe, QuickBooks, Slack, Zapier)
├── Sandboxes
│   ├── + New Sandbox (copy of production data/config)
│   ├── Sandbox List (name, type, last refresh, status)
│   ├── Deploy from Sandbox (config snapshot → production)
│   └── Sandbox Refresh (refresh from production)
├── Audit Logs
│   ├── User Activity (login, logout, failed login)
│   ├── Record Changes (field-level, who, when, old value, new value)
│   ├── Configuration Changes (who changed entities/fields/workflows)
│   ├── Access Logs (who viewed what)
│   └── Export Audit Log
├── Security
│   ├── SSO/SAML Configuration
│   ├── OAuth Client Management
│   ├── Password Policy (complexity, expiry, history)
│   ├── Session Policy (timeout, concurrent sessions)
│   ├── MFA Configuration
│   └── IP Allow/Block Lists
└── System Settings
    ├── General (timezone, currency, date format, locale)
    ├── AI Configuration (Ollama URL, MCP server, model selection)
    ├── Tenant Settings (tenant name, logo, branding)
    ├── Email Templates (system emails, notifications)
    ├── Notification Preferences (in-app, email, push)
    └── Feature Flags (enable/disable features per tenant)
```

---

### 3.8 AI (MCP Agent)

```
AI
├── AI Assistant (Chat)
│   ├── Natural Language Query: "Show me deals over $50k that are stale"
│   ├── Natural Language Action: "Create a follow-up task for John about the demo"
│   ├── AI Report Generator: "Show me win rate by rep this quarter"
│   └── Conversation History
├── AI Insights
│   ├── Pipeline Health (risks, opportunities, anomalies)
│   ├── Deal Insights (per-deal: risk assessment, next actions)
│   ├── Activity Insights (coaching opportunities, rep engagement)
│   └── Data Quality Insights (missing fields, stale records)
├── AI CRM Administrator (Autonomous Agent)
│   ├── Task Execution: "Merge these 3 duplicate contacts"
│   ├── Workflow Building: "Create a workflow that flags deals over $100k"
│   ├── Report Building: "Create a dashboard for the QBR meeting"
│   └── Data Cleanup: "Find and merge contacts with missing email domains"
├── AI Configuration
│   ├── MCP Server Settings
│   ├── LLM Selection (Ollama model, OpenAI key, Anthropic key)
│   ├── Prompt Templates
│   └── Permissions (what AI can/cannot do)
└── AI Usage & Logs
    ├── AI Query History
    ├── AI Action Log
    └── Token Usage (if using cloud LLM)
```

---

## 4. QUICK ACTION COMMAND PALETTE (Cmd+K / Ctrl+K)

Universal command palette accessible from any screen:

```
> [Search: Contacts, Deals, Orgs, Notes...]
  ─────────────────────────────────
  + New Contact
  + New Deal
  + New Organization
  + Log Call
  + Log Email
  + Schedule Meeting
  + Add Task
  + Write Note
  + Create Report
  ─────────────────────────────────
  Go to Pipeline
  Go to Reports
  Go to Admin > Entity Manager
  ─────────────────────────────────
  AI: "Schedule follow-up tomorrow"
  AI: "Show me this quarter's pipeline"
  AI: "Find deals that need attention"
```

---

## 5. VERTICAL-SPECIFIC NAVIGATION EXTENSIONS

### IT Consulting Vertical (additional menu items)

```
┌─ Projects ──────────────────────────────┐
│  Engagements (list/kanban/detail)        │
│  SOWs (list/detail/approval)             │
│  Time Entries (weekly view, approval)    │
│  Resources (consultants, skills, rates)  │
│  Expenses (list/approval/export)         │
└──────────────────────────────────────────┘
```

### SaaS Vertical (additional menu items)

```
┌─ Subscriptions ─────────────────────────┐
│  Subscriptions (list/detail/churn)       │
│  Invoices (list/detail/status)           │
│  MRR Dashboard (trend, breakdown)        │
│  Health Scores (account health, alerts)  │
│  Renewals (calendar, risk)               │
└──────────────────────────────────────────┘
```

Both vertical extensions appear as top-level menu items when the template is activated. They are dynamic entities created by the Dynamic Object Builder, not hardcoded.

---

## 6. MOBILE NAVIGATION

### Bottom Tab Bar
```
[Home] [Pipeline] [Contacts] [Deals] [More ▸]

More:
  Activities
  Reports (mobile-optimized)
  Admin (admin users)
  AI Assistant (voice/text)
```

### Mobile Adaptations
- Kanban: single-column swipeable cards
- Tables: horizontal scroll, tap for detail
- Activity Log: optimized for quick entry
- Search: full-screen, voice input enabled
- Notifications: push for deals, tasks, mentions

---

## 7. NAVIGATION FLOW DIAGRAMS

### Primary Flow: SDR Daily Workflow
```
Home → Pipeline View (leads) → Lead Detail → Log Call → Next Lead (auto-advance)
                                    ↓
                              Sequence Activity
                                    ↓
                              → Task Created → End of Day Summary
```

### Primary Flow: AE Deal Workflow
```
Home → Deals Pipeline → Deal Detail (summary tab)
                           ↓
                    Activity Tab → Log Email/Meeting
                           ↓
                    Contacts Tab → Find Champion
                           ↓
                    Documents Tab → Send Proposal
                           ↓
                    AI Insights → Risk Analysis
                           ↓
                    Update Stage → Won!
```

### Primary Flow: Manager Review
```
Home → Pipeline View (team) → Filter by Rep → Drill into Deal
                                    ↓
                              Activity Report (rep metrics)
                                    ↓
                              Coaching Suggestions (AI)
                                    ↓
                              Forecast View → Update Forecast
```

### Primary Flow: Admin Configuration
```
Admin → Entity Manager → Create Custom Entity
                              ↓
                        Define Fields
                              ↓
                        Define Layout
                              ↓
                        Define Pipeline
                              ↓
                        Define Workflows
                              ↓
                        Assign Permissions
                              ↓
                        Deploy to Production
```

---

## 8. UI SURFACE MAP

| Surface | Desktop | Mobile | Email | API | AI (MCP) |
|---------|---------|--------|-------|-----|----------|
| Home Dashboard | YES | YES | YES (digest) | — | YES (summary) |
| Contact List | YES | YES | — | YES | YES (query) |
| Contact Detail | YES | YES | — | YES | YES (query) |
| Deal List | YES | YES | — | YES | YES (query) |
| Deal Detail | YES | YES | — | YES | YES (query) |
| Pipeline Kanban | YES | YES | — | — | YES (query) |
| Activity Log | YES | YES | — | YES | YES (action) |
| Reports | YES | Summary | YES (scheduled) | — | YES (generate) |
| Admin | YES | Limited | — | YES | YES (action) |
| AI Assistant | YES | YES | — | — | Native |
| Quick Entry | — | — | YES (email-to-CRM) | YES | YES (voice → text) |

---

*Phase 4 complete. Information Architecture defines all screens, menus, and navigation flows. Next: Phase 5 — Complete Module Inventory.*
