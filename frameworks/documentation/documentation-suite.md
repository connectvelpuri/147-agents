# SOVEREIGN CRM — DOCUMENTATION SUITE
# Version: 2.0 | User Docs, API Docs, Onboarding, SOPs, Runbooks

---

## 1. DOCUMENTATION STANDARDS

### Documentation Principles
1. **Documentation is First-Class** — No feature is done without docs
2. **Documentation as Code** — All docs live in version control
3. **Documentation is Tested** — Doc examples must work
4. **Documentation is Fresh** — Updated within 7 days of change
5. **Documentation is Accessible** — Clear, concise, beginner-friendly

### Documentation Taxonomy

| Type | Audience | Location | Update Cadence |
|------|----------|----------|----------------|
| **User Guide** | End users | /docs/user-guide/ | Per feature release |
| **API Reference** | Developers | /docs/api/ | Per API change |
| **Admin Guide** | System admins | /docs/admin/ | Per deployment change |
| **Developer Guide** | Contributors | /docs/developer/ | Per architecture change |
| **Onboarding** | New users | /docs/onboarding/ | Monthly review |
| **SOPs** | Operations team | /docs/sops/ | Quarterly review |
| **Runbooks** | SRE/DevOps | /docs/runbooks/ | After every incident |
| **ADRs** | Architecture team | /docs/adrs/ | Per decision |
| **Changelog** | Everyone | /CHANGELOG.md | Per release |

---

## 2. USER GUIDE STRUCTURE

### /docs/user-guide/
```
user-guide/
├── README.md                    # Overview and quick start
├── getting-started/
│   ├── installation.md          # Installation guide
│   ├── first-steps.md           # First steps tutorial
│   └── configuration.md         # Configuration options
├── core-features/
│   ├── contacts.md              # Contact management
│   ├── deals.md                 # Deal/opportunity management
│   ├── leads.md                 # Lead management
│   ├── activities.md            # Activities and tasks
│   └── notes.md                 # Notes and comments
├── ai-features/
│   ├── copilot.md               # AI Copilot usage
│   ├── scoring.md               # Predictive scoring
│   └── automation.md            # Smart automation
├── customization/
│   ├── dynamic-objects.md       # Custom objects
│   ├── custom-fields.md         # Custom fields
│   └── workflows.md             # Workflow automation
├── integrations/
│   ├── email.md                 # Email integration
│   ├── calendar.md              # Calendar integration
│   └── api.md                   # API integration
├── reporting/
│   ├── dashboard.md             # Dashboard usage
│   ├── reports.md               # Report builder
│   └── analytics.md             # Analytics and insights
├── settings/
│   ├── user-settings.md         # User preferences
│   ├── team-settings.md         # Team management
│   └── security.md              # Security settings
└── troubleshooting/
    ├── faq.md                   # Frequently asked questions
    ├── common-issues.md         # Common issues and solutions
    └── contact-support.md       # How to contact support
```

### User Guide Template

```markdown
# [Feature Name]

## Overview
[1-2 sentence description of what this feature does and why it matters]

## Prerequisites
- [What the user needs before using this feature]

## Getting Started
1. [Step 1 with screenshot]
2. [Step 2 with screenshot]
3. [Step 3 with screenshot]

## Advanced Usage
### [Sub-feature 1]
[Detailed instructions]

### [Sub-feature 2]
[Detailed instructions]

## Tips & Best Practices
- [Tip 1]
- [Tip 2]

## Troubleshooting
### [Common Issue 1]
**Symptom:** [What the user sees]
**Solution:** [How to fix it]

## Related Features
- [Link to related feature 1]
- [Link to related feature 2]
```

---

## 3. API DOCUMENTATION

### OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: Sovereign CRM API
  description: |
    Self-hosted, AI-native CRM API with 19+ MCP tools.
    Privacy-first: Your data never leaves your infrastructure.
  version: 1.2.0
  contact:
    name: Sovereign CRM Support
    email: support@sovereign-crm.com

servers:
  - url: http://localhost:8080
    description: Local development
  - url: https://your-domain.com
    description: Production

paths:
  /api/contacts:
    get:
      summary: List contacts
      description: Retrieve a paginated list of contacts
      tags: [Contacts]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: search
          in: query
          schema:
            type: string
          description: Search contacts by name or email
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Contact'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /api/contacts/{id}:
    get:
      summary: Get contact by ID
      tags: [Contacts]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Contact'

components:
  schemas:
    Contact:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
        phone:
          type: string
        company:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        pages:
          type: integer
```

### API Documentation Pages

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| /api/contacts | GET, POST | List/create contacts | Yes |
| /api/contacts/{id} | GET, PUT, DELETE | Get/update/delete contact | Yes |
| /api/deals | GET, POST | List/create deals | Yes |
| /api/deals/{id} | GET, PUT, DELETE | Get/update/delete deal | Yes |
| /api/leads | GET, POST | List/create leads | Yes |
| /api/leads/{id} | GET, PUT, DELETE | Get/update/delete lead | Yes |
| /api/activities | GET, POST | List/create activities | Yes |
| /api/activities/{id} | GET, PUT, DELETE | Get/update/delete activity | Yes |
| /api/mcp | POST | MCP tool execution | Yes |
| /api/mcp/health | GET | MCP health check | No |
| /api/auth/login | POST | User login | No |
| /api/auth/refresh | POST | Refresh token | Yes |

---

## 4. ONBOARDING DOCUMENTATION

### New User Onboarding Flow

```
Step 1: Welcome (Day 0)
├── Welcome email with login credentials
├── Link to onboarding guide
└── Quick start video (2 min)

Step 2: Setup (Day 0-1)
├── Complete profile setup
├── Import first contacts (CSV or manual)
├── Connect email integration
└── Set up calendar integration

Step 3: Core Features (Day 1-3)
├── Create first deal
├── Add activities and notes
├── Use AI Copilot for first query
└── Explore dashboard

Step 4: Advanced Features (Day 3-7)
├── Create custom fields
├── Set up workflows
├── Generate first report
└── Invite team members

Step 5: Mastery (Day 7-14)
├── Advanced AI features
├── Dynamic objects
├── Custom dashboards
└── API integration
```

### Onboarding Checklist Template

```markdown
# Welcome to Sovereign CRM!

## Your First Week Checklist

### Day 1: Get Started
- [ ] Log in and complete your profile
- [ ] Import your first contacts
- [ ] Create your first deal
- [ ] Try the AI Copilot

### Day 2-3: Core Features
- [ ] Add activities to your deals
- [ ] Use notes and comments
- [ ] Explore the dashboard
- [ ] Set up email integration

### Day 4-5: Advanced Features
- [ ] Create custom fields
- [ ] Set up a workflow
- [ ] Generate a report
- [ ] Invite a team member

### Day 6-7: Master It
- [ ] Use dynamic objects
- [ ] Create a custom dashboard
- [ ] Explore the API
- [ ] Complete onboarding survey

## Need Help?
- 📖 [User Guide](/docs/user-guide/)
- 🎥 [Video Tutorials](/docs/videos/)
- 💬 [Community Forum](https://community.sovereign-crm.com)
- 📧 [Support Email](mailto:support@sovereign-crm.com)
```

---

## 5. STANDARD OPERATING PROCEDURES (SOPs)

### SOP Template

```markdown
# SOP: [Procedure Name]

**Version:** 1.0
**Effective Date:** YYYY-MM-DD
**Owner:** [Agent/Role]
**Review Cadence:** Quarterly

## Purpose
[Why this SOP exists]

## Scope
[What this SOP covers and doesn't cover]

## Prerequisites
[What's needed before executing this SOP]

## Procedure
### Step 1: [Action]
1. [Detailed instruction]
2. [Detailed instruction]
3. [Expected outcome]

### Step 2: [Action]
1. [Detailed instruction]
2. [Detailed instruction]
3. [Expected outcome]

## Verification
- [How to verify the procedure was successful]

## Troubleshooting
### [Common Issue]
**Symptom:** [What you see]
**Solution:** [How to fix]

## Related SOPs
- [Link to related SOP 1]
- [Link to related SOP 2]

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial version |
```

### Required SOPs

| SOP | Owner | Review Cadence |
|-----|-------|----------------|
| New User Onboarding | Customer Success | Monthly |
| Contact Import/Export | Product Manager | Quarterly |
| Data Backup & Restore | DevOps Lead | Quarterly |
| Security Incident Response | Security Engineer | Quarterly |
| Release Deployment | Release Manager | Per release |
| Agent Onboarding | Eng Manager | Quarterly |
| Vendor Assessment | CISO | Annually |
| Compliance Audit | CISO | Annually |

---

## 6. RUNBOOKS

### Runbook Template

```markdown
# Runbook: [Scenario Name]

**Severity:** Sev-X
**Owner:** [Agent/Role]
**Last Updated:** YYYY-MM-DD
**Last Tested:** YYYY-MM-DD

## Symptoms
[What indicates this scenario]

## Impact
[What is affected and how]

## Diagnosis
### Step 1: Check [Component]
```bash
[command to run]
```
**Expected:** [What you should see]
**If abnormal:** [What it means]

### Step 2: Check [Component]
```bash
[command to run]
```
**Expected:** [What you should see]
**If abnormal:** [What it means]

## Mitigation
### Option 1: [Quick Fix]
1. [Step 1]
2. [Step 2]
3. [Expected outcome]

### Option 2: [Proper Fix]
1. [Step 1]
2. [Step 2]
3. [Expected outcome]

## Recovery
1. [Step 1]
2. [Step 2]
3. [Verify recovery]

## Escalation
If unresolved after [time], escalate to:
1. [Primary contact]
2. [Secondary contact]
3. [Executive]

## Post-Incident
- [ ] Update runbook if needed
- [ ] Create postmortem if Sev-1/2
- [ ] Update monitoring if needed

## Related Runbooks
- [Link to related runbook 1]
- [Link to related runbook 2]
```

### Required Runbooks

| Runbook | Owner | Last Tested |
|---------|-------|-------------|
| API Server Down | SRE Lead | — |
| Database Performance Degradation | DBA | — |
| AI Copilot Failure | AI Engineer | — |
| Security Incident | Security Engineer | — |
| Memory/CPU Exhaustion | DevOps Lead | — |
| Backup Failure | DevOps Lead | — |
| Deployment Failure | Release Manager | — |
| SSL Certificate Expiry | DevOps Lead | — |

---

*Framework based on: Write the Docs Best Practices, Google Documentation Standards, API Documentation Best Practices*
