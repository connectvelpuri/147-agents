# 08 — Shared Context Framework

## How 548 Agents Maintain a Consistent View of Reality

---

## Executive Summary

Without shared context, each agent operates in its own version of reality.
Agent A thinks the contact API has 200ms latency because it measured that last
Tuesday. Agent B thinks it has 2 seconds latency because it measured it during
peak load yesterday. Agent C thinks the feature is complete because its branch
merged. Agent D thinks it is incomplete because the integration tests failed.
They are all "right" in their own context. They are all wrong about the current
state of reality.

Shared context is the mechanism that ensures all 548 agents have access to the
same truth — the same data, the same state, the same decisions, the same history.
Without it, duplication grows, contradictions multiply, quality drops, and
coordination becomes impossible.

This document defines the complete shared context system: what context exists,
how it is maintained, how agents access it, and how contradictions are resolved.

---

## 1. Shared Context Philosophy

### 1.1 Why Shared Context Matters

  The cost of shared context failure is exponential with agent count:
    - 2 agents: 1 potential contradiction pair
    - 10 agents: 45 potential contradiction pairs
    - 100 agents: 4,950 potential contradiction pairs
    - 548 agents: 149,828 potential contradiction pairs

  Without shared context:
    - Agents duplicate work because they don't know someone else is doing it
    - Agents make contradictory decisions because they have different information
    - Agents build against outdated assumptions because they don't see changes
    - Agents miss dependencies because they don't know about related work
    - Quality drops because agents cannot see the full picture

### 1.2 Context Principles

  PRINCIPLE 1: SINGLE SOURCE OF TRUTH
    For every piece of information, exactly ONE authoritative source exists.
    All other copies are derived from that source. If two sources disagree,
    one is wrong and must be corrected.

  PRINCIPLE 2: EVENTUAL CONSISTENCY
    Context updates propagate to all agents within seconds, not minutes.
    During propagation, agents may have slightly stale data, but the system
    self-heals as updates arrive. Strong consistency is reserved for
    critical operations (releases, deployments, security actions).

  PRINCIPLE 3: CONTEXT IS PROACTIVE
    Agents do not poll for context. Context is pushed to agents when it
    changes. "You should know this" is the default, not "ask and you
    shall receive."

  PRINCIPLE 4: CONTEXT IS SCOPED
    Agents receive only the context relevant to their role, domain, and
    current task. Full-context dumps are for incident response only.
    Scoped context prevents information overload.

  PRINCIPLE 5: CONTEXT IS VERIFIED
    Every context entry has a timestamp, a source, and a version.
    Agents can verify they are working with current context by checking
    the version against the authoritative source.

---

## 2. Shared Context Types

### 2.1 Product Context

  WHAT: Current state of all products being built
  OWNER: Product Manager / CPO
  UPDATE FREQUENCY: Daily (sprint), Weekly (roadmap)
  ACCESS: All agents

  CONTENTS:
    - Product roadmap (current quarter and next)
    - Feature status (discovery, design, building, testing, released)
    - Sprint goals and current progress
    - Customer feedback themes
    - Competitive intelligence updates
    - Revenue and adoption metrics
    - Technical debt inventory

  PRODUCT STATE SCHEMA:
    {
      "product": "CRM",
      "version": "2.5.0",
      "sprint": "sprint-12",
      "sprint_goal": "Complete CRDT sync + dashboard v2",
      "features": [
        {
          "id": "CRM-498",
          "name": "CRDT Sync for Contacts",
          "status": "in-progress",
          "phase": "build",
          "owner": "crm-backend-eng-01",
          "progress": 0.65,
          "blockers": [],
          "eta": "2026-06-13"
        }
      ],
      "customer_themes": [
        "Real-time collaboration is #1 request",
        "Mobile experience needs improvement",
        "API reliability concerns at scale"
      ],
      "last_updated": "2026-06-09T09:00:00Z"
    }

### 2.2 Architecture Context

  WHAT: Current system architecture and design decisions
  OWNER: Enterprise Architect / Solution Architect
  UPDATE FREQUENCY: On change (ADR-driven)
  ACCESS: All engineering agents

  CONTENTS:
    - Current architecture diagram (service map)
    - Architecture Decision Records (ADRs)
    - API contracts (OpenAPI specs)
    - Data models (entity-relationship diagrams)
    - Deployment architecture
    - Infrastructure topology
    - Security architecture

  ARCHITECTURE STATE SCHEMA:
    {
      "architecture_version": "3.2",
      "services": [
        {
          "name": "crm-api",
          "domain": "crm-backend",
          "version": "2.4.1",
          "status": "healthy",
          "dependencies": ["crm-db", "crm-cache", "auth-service"],
          "api_contract": "https://docs.internal/api/crm-api/v2.4.1"
        }
      ],
      "adrs": [
        {
          "id": "ADR-042",
          "title": "Use LWW-Register for CRDT sync",
          "status": "accepted",
          "date": "2026-06-05",
          "deciders": ["crm-arch-01", "enterprise-arch-01"]
        }
      ],
      "last_updated": "2026-06-09T10:00:00Z"
    }

### 2.3 Operational Context

  WHAT: Current operational state of all services
  OWNER: SRE Lead / DevOps Lead
  UPDATE FREQUENCY: Real-time (continuous monitoring)
  ACCESS: All agents (summary), SRE/DevOps (detail)

  CONTENTS:
    - Service health status (healthy, degraded, down)
    - Current SLO compliance (error rate, latency, availability)
    - Active incidents (sev-1 through sev-4)
    - Recent deployments (last 24 hours)
    - Capacity status (CPU, memory, disk, network)
    - Alert status (firing, resolved)
    - Maintenance windows

  OPERATIONAL STATE SCHEMA:
    {
      "timestamp": "2026-06-09T14:30:00Z",
      "services": [
        {
          "name": "crm-api",
          "status": "healthy",
          "slo_compliance": {
            "availability": 0.9995,
            "latency_p95": 245,
            "error_rate": 0.001
          },
          "active_incidents": [],
          "last_deployment": "2026-06-08T16:00:00Z",
          "capacity": {
            "cpu": 0.45,
            "memory": 0.62,
            "disk": 0.38
          }
        }
      ],
      "active_incidents": [],
      "firing_alerts": []
    }

### 2.4 Team Context

  WHAT: Current state of each pod and cross-pod dependencies
  OWNER: Delivery Manager / Engineering Manager
  UPDATE FREQUENCY: Daily (standup), Sprint (planning)
  ACCESS: All agents in the pod, Delivery Manager (all pods)

  CONTENTS:
    - Pod membership and current assignments
    - Sprint progress (committed vs. completed)
    - Active blockers and their resolution status
    - Cross-pod dependencies and their status
    - Velocity trends and capacity forecasts
    - Team morale indicators

  TEAM STATE SCHEMA:
    {
      "pod": "crm-core-pod",
      "sprint": "sprint-12",
      "members": [
        {"agent": "pm-01", "role": "Product Manager", "capacity": 0.8},
        {"agent": "be-01", "role": "Senior Backend", "capacity": 0.7},
        {"agent": "be-02", "role": "Backend Engineer", "capacity": 0.85},
        {"agent": "fe-01", "role": "Frontend Engineer", "capacity": 0.6},
        {"agent": "qa-01", "role": "QA Engineer", "capacity": 0.75},
        {"agent": "devops-01", "role": "DevOps Engineer", "capacity": 0.9}
      ],
      "velocity": {"current": 42, "average": 38, "trend": "improving"},
      "blockers": [
        {
          "task": "CRM-500",
          "blocker": "Waiting for platform-pod database migration",
          "since": "2026-06-07",
          "escalated": false
        }
      ],
      "cross_pod_dependencies": [
        {
          "dependent_on": "platform-pod",
          "item": "Database index creation",
          "status": "completed"
        }
      ],
      "last_updated": "2026-06-09T09:15:00Z"
    }

### 2.5 Decision Context

  WHAT: Recent decisions and their rationale
  OWNER: Various (tracked by Enterprise Architect)
  UPDATE FREQUENCY: On decision (continuous)
  ACCESS: All agents

  CONTENTS:
    - Architecture Decision Records (ADRs)
    - Product decisions (feature scope, priority changes)
    - Process decisions (workflow changes, tool selections)
    - Personnel decisions (team changes, role assignments)
    - Financial decisions (budget allocations, vendor selections)

### 2.6 Customer Context

  WHAT: Customer data, feedback, and relationship state
  OWNER: Product Manager / Customer Success
  UPDATE FREQUENCY: Weekly (feedback), Daily (usage)
  ACCESS: Product, Customer Success, UX (full); Engineering (summary)

  CONTENTS:
    - Customer segments and personas
    - Feature usage analytics
    - Customer satisfaction scores (NPS, CSAT)
    - Support ticket themes and trends
    - Customer interview insights
    - Churn risk indicators

---

## 3. Context Synchronization Mechanisms

### 3.1 Push Updates (Event-Driven)

  WHEN: Context changes that affect multiple agents
  HOW: Event published to relevant topic
  LATENCY: <100 seconds from change to all subscribers

  EXAMPLE:
    SRE detects latency spike on crm-api.
    Event: enterprise.platform.infra.latency.spike
    All agents subscribed to crm-api context receive:
      "CRM API latency increased from 200ms to 1.2s at 14:30 UTC.
       Investigation in progress. No action required from non-SRE agents."

### 3.2 Pull Updates (On-Demand)

  WHEN: Agent needs specific context not in its current view
  HOW: Agent queries the context store
  LATENCY: <1 second for cached, <5 seconds for fresh

  EXAMPLE:
    Backend engineer starts working on CRM-498 (CRDT sync).
    Agent queries: "What is the current architecture for contacts module?"
    Response: Current architecture diagram, ADRs, API contracts for contacts.

### 3.3 Context Inheritance

  WHEN: Agent joins a pod or takes on a new task
  HOW: Agent receives all relevant context for its new assignment
  LATENCY: <30 seconds from assignment to full context

  EXAMPLE:
    Agent assigned to crm-core-pod for sprint 12.
    Agent receives:
      - Pod context (members, goals, conventions)
      - Sprint context (backlog, priorities, dependencies)
      - Domain context (crm-backend patterns, ADRs, known issues)
      - Task context (CRM-498 requirements, acceptance criteria)

### 3.4 Context Checkpointing

  WHEN: Long-running tasks or incidents
  HOW: Context snapshots saved at key milestones
  LATENCY: Immediate (synchronous write)

  EXAMPLE:
    Incident response creates a context checkpoint every 15 minutes:
      - Current hypothesis
      - Actions taken
      - Evidence gathered
      - Timeline of events
    If incident commander changes, new commander gets full context from checkpoint.

---

## 4. Context Contradiction Resolution

### 4.1 Detection

  Contradictions are detected by:
    - Automated consistency checks (every context update)
    - Agent conflict reporting (when two agents see different facts)
    - Human observation (during reviews or standups)

  CONSISTENCY CHECK EXAMPLES:
    - Agent A says feature X is complete; Agent B says it has 3 open bugs
    - Architecture diagram shows service A depends on B; B's config shows no A
    - Sprint report says 10 points completed; task board shows 8
    - Security scan says clean; vulnerability database shows open findings

### 4.2 Resolution

  When a contradiction is detected:

  1. IDENTIFY: Which context entry is authoritative?
     - Check timestamp (newer is more likely correct)
     - Check source (authoritative source wins)
     - Check evidence (what do the actual logs/data show?)

  2. CORRECT: Update the stale or incorrect entry
     - Reference the authoritative source
     - Document the correction with rationale
     - Notify affected agents of the correction

  3. PREVENT: Why did the contradiction occur?
     - Was the update mechanism broken?
     - Was the source ambiguous?
     - Was the agent using stale cache?
     - Add guardrail to prevent recurrence

### 4.3 Consistency Levels

  STRONG CONSISTENCY (required for):
    - Production deployments
    - Security actions
    - Financial transactions
    - Data migrations
    Mechanism: Synchronous write + read verification
    Latency: 100-500ms

  EVENTUAL CONSISTENCY (acceptable for):
    - Sprint progress updates
    - Documentation changes
    - Non-critical status updates
    - Knowledge base entries
    Mechanism: Async propagation with version tracking
    Latency: <100 seconds

---

## 5. Context Security

### 5.1 Access Control

  Not all context is available to all agents:

  | Context Type | L1-L2 | L3 | L4 | L5 | L6 |
  |-------------|-------|-----|-----|-----|-----|
  | Product (summary) | Full | Full | Full | Full | Full |
  | Product (detail) | Full | Full | Summary | Summary | Summary |
  | Architecture | Full | Full | Full | Full | Summary |
  | Operational | Full | Summary | Summary | Full | Full |
  | Team | Full | Full | Own pod | Own pod | Own pod |
  | Decision | Full | Full | Full | Summary | Summary |
  | Customer (PII) | Full | Summary | None | None | None |
  | Financial | Full | Summary | None | None | None |
  | Security | Full | None | Summary | Full | Summary |

### 5.2 Data Protection

  - PII data is encrypted at rest and in transit
  - Financial data requires COO-level access
  - Security vulnerability data requires CISO-level access
  - Customer data is anonymized for non-Customer-facing agents
  - All context access is logged for audit

---

## 6. Context Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Context freshness | >95% of entries <1 hour old | Timestamp audit |
  | Context accuracy | >99% of entries match authoritative source | Consistency checks |
  | Contradiction rate | <0.1% of context entries | Contradiction detection |
  | Contradiction resolution time | <4 hours | Resolution tracking |
  | Context access latency | <1 second (cached) | Performance monitoring |
  | Context propagation latency | <100 seconds | Event bus metrics |
  | Context completeness | >95% of required context available | Completeness audit |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
