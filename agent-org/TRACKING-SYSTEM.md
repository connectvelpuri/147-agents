# TRACKING SYSTEM
# Sovereign CRM — Every Code Change, Every Action, Every Update Tracked

**Date:** 2026-06-08
**Tool:** Plane (https://plane.so) — Open Source Jira Alternative
**Status:** DESIGNED

---

## WHY PLANE

| Criterion | Plane | Jira | Linear | GitHub Projects |
|-----------|-------|------|--------|----------------|
| Self-hosted | YES | Cloud only | Cloud only | Cloud only |
| Open source | YES (AGPLv3) | No | No | No |
| API-first | YES | YES | YES | YES |
| Custom workflows | YES | YES | Limited | Limited |
| Cycles (Sprints) | YES | YES | YES | YES |
| Modules (Epics) | YES | YES | YES | Limited |
| Custom attributes | YES | YES | Limited | Limited |
| Webhooks | YES | YES | YES | YES |
| Audit trail | YES | YES | YES | Limited |
| Cost | FREE | $8/user/mo | $8/user/mo | FREE |
| Fits sovereignty thesis | YES | No | No | No |

**Decision:** Plane — self-hosted, open source, API-first, full audit trail.

---

## TRACKING REQUIREMENTS

### What Must Be Tracked

| Category | Items | Frequency |
|----------|-------|-----------|
| **Code Changes** | Every commit, PR, merge, deploy | Real-time |
| **Agent Actions** | Every decision, review, challenge, approval | Real-time |
| **Sprint Progress** | Every status change, blocker, completion | Daily |
| **Architecture Decisions** | Every ADR, review, approval | Per decision |
| **Security Events** | Every scan, finding, remediation | Real-time |
| **Quality Events** | Every test run, defect, fix | Real-time |
| **Deployment Events** | Every build, deploy, rollback | Real-time |
| **Incident Events** | Every incident, escalation, resolution | Real-time |
| **Communication Events** | Every review, challenge, brainstorm | Per event |
| **Compliance Events** | Every audit, finding, remediation | Per audit |

### Timestamp Requirements

Every tracked item MUST include:
- **Created timestamp** (ISO 8601)
- **Updated timestamp** (ISO 8601)
- **Agent ID** (who performed the action)
- **Action type** (what was done)
- **Context** (what triggered the action)
- **Outcome** (what resulted)

---

## PLANE CONFIGURATION

### Workspace Structure

```
Sovereign CRM Workspace
├── Projects
│   ├── Core CRM (Pod 1)
│   ├── AI & Intelligence (Pod 2)
│   ├── Platform (Pod 3)
│   ├── Product Experience (Pod 4)
│   ├── Integrations (Pod 5)
│   └── Infrastructure & DevOps
├── Cycles (Sprints)
│   ├── Sprint 1, Sprint 2, ...
│   └── Configured for 2-week cadence
├── Modules (Epics)
│   ├── CRDT Sync Engine
│   ├── Dynamic Object Builder
│   ├── AI Copilot
│   ├── MCP Server
│   ├── Dashboard Builder
│   ├── Mobile App
│   └── [Feature modules]
├── Custom Fields
│   ├── Agent ID (dropdown: all 68 agents)
│   ├── Layer (dropdown: L1-L6)
│   ├── Pod (dropdown: Pod 1-5)
│   ├── Review Status (dropdown: Pending/Challenged/Approved/Rejected)
│   ├── Security Review (dropdown: Pending/Pass/Fail)
│   ├── Quality Gate (dropdown: Pending/Pass/Fail)
│   ├── Accessibility Review (dropdown: Pending/Pass/Fail)
│   ├── Priority Score (number: 1-100)
│   └── Business Impact (dropdown: Critical/High/Medium/Low)
└── Views
    ├── Portfolio Dashboard
    ├── Sprint Board
    ├── Architecture Board
    ├── Quality Dashboard
    ├── Security Dashboard
    └── Agent Activity Log
```

### Issue Types

| Type | Fields | Workflow |
|------|--------|----------|
| **Epic** | Title, Description, Owner, Priority, Status | Backlog → In Progress → Done |
| **Story** | Title, Description, Acceptance Criteria, Priority, Estimate | Backlog → Ready → In Progress → Review → Done |
| **Task** | Title, Description, Assignee, Estimate, Due Date | Backlog → In Progress → Done |
| **Bug** | Title, Description, Severity, Steps, Agent | Open → In Progress → Fixed → Verified → Closed |
| **ADR** | Title, Context, Decision, Consequences, Reviewers | Proposed → Reviewed → Accepted/Rejected |
| **Security Finding** | Title, Severity, CVSS, Affected Component, Fix | Open → Triaged → Fixed → Verified → Closed |
| **Incident** | Title, Severity, Impact, Timeline, Root Cause | Open → Investigating → Resolved → Post-mortem |
| **Review Request** | Title, Type, Requester, Reviewers, Decision | Requested → In Review → Approved/Rejected |

### Workflow States

```
Backlog → Ready → In Progress → In Review → Approved → Done
                                        ↓
                                    Rejected → In Progress
                                        ↓
                                    Challenged → Defended → In Review
```

---

## GIT INTEGRATION

### Commit Tracking
Every git commit must reference a Plane issue:

```
git commit -m "feat(crdt): implement sync protocol [CORE-123]"
git commit -m "fix(auth): resolve token expiry [SEC-456]"
git commit -m "test(api): add integration tests [QA-789]"
```

### PR Tracking
Every PR must:
1. Reference the Plane issue
2. Link to the ADR (if architectural)
3. Include test evidence
4. Include security scan results
5. Include accessibility review (if UI change)

### Deployment Tracking
Every deployment must:
1. Reference the release in Plane
2. Include deployment log
3. Include verification results
4. Update Plane status

---

## WEBHOOK INTEGRATION

### Git → Plane
- On commit: Update issue status, add comment with commit hash
- On PR merge: Move issue to "Done", add merge evidence
- On PR reject: Move issue back to "In Progress", add rejection reason

### CI/CD → Plane
- On build success: Add build evidence to issue
- On build failure: Create bug, link to issue
- On deploy success: Update release status
- On deploy failure: Create incident, link to release

### Security Scanner → Plane
- On vulnerability found: Create security finding
- On vulnerability fixed: Update finding status
- On scan complete: Add scan report to issue

### Agent Actions → Plane
- On review requested: Create review request
- On review completed: Update review status
- On challenge issued: Create challenge record
- On challenge resolved: Update challenge status
- On decision made: Create ADR, link to issue

---

## AUDIT TRAIL

### What Gets Logged

| Event | Data Captured | Retention |
|-------|--------------|-----------|
| Code commit | Hash, author, timestamp, issue ref, diff summary | Permanent |
| PR created | Author, timestamp, reviewers, description | Permanent |
| PR merged | Merger, timestamp, merge commit, CI results | Permanent |
| Issue created | Creator, timestamp, type, fields | Permanent |
| Issue updated | Updater, timestamp, field changes | Permanent |
| Review requested | Requester, timestamp, reviewers, type | Permanent |
| Review completed | Reviewer, timestamp, decision, comments | Permanent |
| Challenge issued | Challenger, timestamp, assumption, evidence | Permanent |
| Challenge resolved | Defender, timestamp, resolution, outcome | Permanent |
| Decision made | Decision maker, timestamp, decision, rationale | Permanent |
| Deployment | Deployer, timestamp, version, environment, result | Permanent |
| Incident | Reporter, timestamp, severity, timeline, resolution | Permanent |
| Security finding | Scanner, timestamp, severity, component, fix | Permanent |

### Audit Query API

```plane
# Get all actions by an agent
GET /api/workspaces/{workspace}/audit?agent_id=L4-08&from=2026-01-01

# Get all actions on an issue
GET /api/workspaces/{workspace}/issues/{issue_id}/audit

# Get all actions in a time range
GET /api/workspaces/{workspace}/audit?from=2026-06-01&to=2026-06-08

# Get all security events
GET /api/workspaces/{workspace}/audit?action_type=security_finding

# Get all deployment events
GET /api/workspaces/{workspace}/audit?action_type=deployment
```

---

## AGENT ACTIVITY TRACKING

### Every Agent Action Must Be Tracked

| Agent | Action | How Tracked |
|-------|--------|-------------|
| CEO | Strategic decision | ADR in Plane + Decision Record |
| COO | Delivery decision | Issue update + comment |
| CTO | Technology decision | ADR in Plane |
| CPO | Product decision | PRD in Plane + comment |
| EA | Architecture decision | ADR in Plane |
| CISO | Security decision | Security finding in Plane |
| PM | Feature decision | Story in Plane |
| SA | Solution design | ADR in Plane |
| EM | Code review | PR review in Git + Plane |
| Engineer | Code commit | Git commit + Plane issue |
| QA Lead | Quality gate | Quality gate in Plane |
| Security Eng | Security scan | Security finding in Plane |
| DevOps | Deployment | Deployment record in Plane |
| SRE | Incident | Incident in Plane |
| Designer | Design review | Review request in Plane |

### Agent Dashboard

```
Agent Activity Dashboard
├── Actions Today: [count]
├── Actions This Week: [count]
├── Actions This Sprint: [count]
├── Pending Reviews: [count]
├── Pending Challenges: [count]
├── Completed Actions: [count]
└── Activity Timeline: [list of recent actions]
```

---

## DASHBOARD VIEWS

### 1. Portfolio Dashboard
- All pods, all sprints, all status
- Capacity vs allocation
- Risk heat map
- Dependency graph

### 2. Sprint Board
- Kanban board per pod
- WIP limits
- Blocked items highlighted
- Velocity chart

### 3. Architecture Board
- All ADRs, status
- Architecture compliance
- Technology radar
- Debt tracking

### 4. Quality Dashboard
- Test coverage trends
- Defect trends
- Quality gate status
- Automation coverage

### 5. Security Dashboard
- Vulnerability status
- Compliance status
- Security scan schedule
- Incident tracker

### 6. Agent Activity Log
- All agent actions, filterable by agent/type/time
- Communication network visualization
- Review chain visualization
- Challenge/resolution timeline

---

## SETUP STEPS

1. Deploy Plane (Docker Compose)
2. Configure workspace and projects
3. Set up custom fields and workflows
4. Configure git integration (webhooks)
5. Configure CI/CD integration (webhooks)
6. Configure security scanner integration
7. Create dashboard views
8. Set up agent activity tracking
9. Train all agents on Plane usage
10. Establish audit trail review cadence

---

## INTEGRATION ARCHITECTURE

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Git Repo   │───>│   Plane API  │<───│   CI/CD      │
│  (GitHub)    │    │  (Webhooks)  │    │  (ArgoCD)    │
└──────────────┘    └──────────────┘    └──────────────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                    ┌───────┴───────┐
                    │   Plane       │
                    │  (Self-hosted)│
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────┴───────┐  ┌───────┴───────┐  ┌───────┴───────┐
│  Agent        │  │  Dashboard    │  │  Audit        │
│  Activity     │  │  Views        │  │  Trail        │
│  Tracker      │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
```
