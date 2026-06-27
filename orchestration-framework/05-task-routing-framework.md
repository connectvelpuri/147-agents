# 05 — Task Routing Framework

## Who Decides Who Does Work in a 548-Agent System

---

## Executive Summary

Without explicit task routing, work either piles up on busy agents while idle
agents do nothing, or goes to agents who lack the skills to do it well, or gets
lost entirely because no one claimed it. At 548 agents, manual task assignment
is impossible. The routing system must be automatic, intelligent, and fair.

This document defines how tasks flow from creation to assignment to execution to
completion. The routing system uses four routing strategies — role-based, skill-based,
capacity-aware, and priority-based — combined into a composite routing algorithm
that considers all four factors simultaneously.

---

## 1. Routing Philosophy

### 1.1 Why Routing Matters

Task routing is the difference between a well-oiled organization and chaos.
Without it:
  - Tasks duplicate because multiple agents pick up the same work
  - Tasks drop because no agent claims them
  - Tasks go to the wrong agent, producing low-quality output
  - Busy agents get overloaded while idle agents sit empty
  - Critical tasks wait in queue behind trivial ones

### 1.2 Routing Principles

  PRINCIPLE 1: EVERY TASK HAS AN OWNER
    No task exists without an assigned owner. The owner is accountable
    from assignment to completion. If ownership is unclear, the task
    is escalated to the routing layer.

  PRINCIPLE 2: ROUTING IS AUTOMATIC, OVERridable BY HUMANS
    The routing system assigns tasks automatically. Humans can override
    the assignment but must document why. Overrides are tracked for
    routing algorithm improvement.

  PRINCIPLE 3: ROUTING CONSIDERS FOUR DIMENSIONS
    Every assignment is evaluated against:
      1. Role fit: Is this agent's role designed for this type of work?
      2. Skill fit: Does this agent have the specific skills needed?
      3. Capacity: Does this agent have bandwidth for more work?
      4. Priority: How urgent/important is this task relative to others?

  PRINCIPLE 4: FAIRNESS IS MEASURABLE
    Workload distribution is monitored. No agent should consistently
    carry >20% more work than the pod average. Imbalances are flagged
    and rebalanced.

  PRINCIPLE 5: ROUTING LEARNS
    The routing system tracks outcomes (quality, speed, satisfaction)
    and uses this data to improve future assignments.

---

## 2. Task Taxonomy

### 2.1 Task Types

  | Task Type | Typical Owner | Routing Strategy | SLA |
  |-----------|--------------|------------------|-----|
  | Feature development | Senior Engineer | Skill + Role | Sprint scope |
  | Bug fix | Any Engineer | Skill + Priority | 1-3 days |
  | Code review | Peer Engineer | Role + Capacity | 4 hours |
  | Architecture decision | Architect | Role + Expertise | 48 hours |
  | Test design | QA Engineer | Role + Skill | Sprint scope |
  | Test execution | QA Engineer | Role + Capacity | 2 days |
  | Security review | Security Engineer | Role + Domain | 24 hours |
  | Deployment | DevOps Engineer | Role + Capacity | 1 day |
  | Incident response | SRE Engineer | Role + Severity | 1 hour (sev1) |
  | Documentation | Docs Lead | Role + Domain | 1 week |
  | Design review | UX Lead | Role + Domain | 24 hours |
  | Process improvement | Eng Manager | Role + Authority | 1 sprint |

### 2.2 Task Complexity Levels

  SIMPLE (L1):
    Description: Well-defined, single-skill, low-risk
    Examples: Typo fix, config change, simple query update
    Routing: Automatic assignment to any qualified agent
    Review: Self-merge after CI passes

  MODERATE (L2):
    Description: Requires domain knowledge, some coordination
    Examples: Feature implementation, bug investigation, test creation
    Routing: Skill-based assignment with capacity check
    Review: Peer review required

  COMPLEX (L3):
    Description: Multi-skill, cross-domain, significant risk
    Examples: Architecture change, database migration, security fix
    Routing: Expert assignment with lead approval
    Review: Lead review + architecture review

  CRITICAL (L4):
    Description: High-impact, irreversible, requires consensus
    Examples: Production outage fix, data migration, platform change
    Routing: Senior expert assignment with CTO notification
    Review: Full ARB review + security sign-off

---

## 3. Routing Strategies

### 3.1 Strategy: Role-Based Routing

  CONCEPT: Match task type to agent role
  HOW: Task classifier maps task type → required role → available agents with that role

  ROUTING TABLE:
    "implement feature"        → Senior Backend/Frontend Engineer
    "fix bug"                  → Engineer in affected domain
    "review code"              → Peer Engineer in same domain
    "design architecture"      → Solution Architect
    "write tests"              → QA Engineer
    "deploy"                   → DevOps Engineer
    "respond to incident"      → SRE Engineer
    "security review"          → Security Engineer
    "design UI"                → UI/UX Designer
    "write documentation"      → Knowledge/Docs Lead
    "prioritize backlog"       → Product Manager
    "allocate capacity"        → Engineering Manager

  STRENGTH: Simple, fast, predictable
  WEAKNESS: Doesn't consider individual skill variations or current capacity

### 3.2 Strategy: Skill-Based Routing

  CONCEPT: Match task requirements to agent skill profiles
  HOW: Each agent maintains a skill profile with proficiency levels

  SKILL PROFILE SCHEMA:
    {
      "agent_id": "crm-backend-eng-01",
      "skills": [
        {"skill": "python", "level": 9, "last_used": "2026-06-09"},
        {"skill": "postgresql", "level": 8, "last_used": "2026-06-08"},
        {"skill": "react", "level": 5, "last_used": "2026-05-15"},
        {"skill": "crdt", "level": 7, "last_used": "2026-06-07"},
        {"skill": "api-design", "level": 8, "last_used": "2026-06-06"},
        {"skill": "performance-tuning", "level": 6, "last_used": "2026-05-20"}
      ],
      "expertise_domains": ["crm-backend", "contacts-module"],
      "learning_areas": ["crdt", "distributed-systems"]
    }

  TASK REQUIREMENT SCHEMA:
    {
      "task_id": "CRM-501",
      "required_skills": [
        {"skill": "python", "min_level": 7},
        {"skill": "crdt", "min_level": 5},
        {"skill": "api-design", "min_level": 6}
      ],
      "preferred_domains": ["crm-backend", "contacts-module"],
      "nice_to_have": ["performance-tuning"]
    }

  MATCHING ALGORITHM:
    1. Filter agents by role (from role-based routing)
    2. Filter by minimum skill levels
    3. Score remaining agents:
       SCORE = sum(skill_match * recency_bonus) + domain_bonus + expertise_bonus
    4. Rank by score
    5. Select top candidate (subject to capacity check)

  STRENGTH: Precise matching, accounts for individual differences
  WEAKNESS: Requires maintained skill profiles, cold-start for new agents

### 3.3 Strategy: Capacity-Aware Routing

  CONCEPT: Don't assign work to agents who are already overloaded
  HOW: Track agent capacity utilization and only assign to agents below threshold

  CAPACITY MODEL:
    Each agent has a weekly capacity (e.g., 40 hours or 10 story points).
    Each assignment consumes capacity.
    Current utilization = assigned capacity / total capacity.

    ROUTING RULES:
      Utilization < 50%:  Available for new assignments (preferred)
      Utilization 50-75%: Available with caution (acceptable)
      Utilization 75-90%: Available for critical/high-priority only
      Utilization > 90%: BLOCKED from new assignments (overloaded)
      Utilization = 100%: Force-blocked (cannot accept any work)

  CAPACITY TRACKING:
    {
      "agent_id": "crm-backend-eng-01",
      "total_capacity": 40,  // hours per week
      "assigned_capacity": 32,
      "utilization": 0.80,
      "available_capacity": 8,
      "assignments": [
        {"task_id": "CRM-498", "hours": 16, "status": "active"},
        {"task_id": "CRM-499", "hours": 8, "status": "active"},
        {"task_id": "CRM-500", "hours": 8, "status": "in-review"}
      ],
      "overtime_budget": 8,  // extra hours this sprint if needed
      "pto_days": 0
    }

  REBALANCING:
    When the routing layer detects >20% utilization imbalance within a pod:
      1. Identify the most overloaded agent
      2. Identify the most available agent with matching skills
      3. Propose task transfer
      4. Delivery Manager approves or rejects
      5. If approved, transfer is executed with context handoff

  STRENGTH: Prevents overload, ensures fairness
  WEAKNESS: Requires accurate capacity tracking, may slow assignment

### 3.4 Strategy: Priority-Based Routing

  CONCEPT: More important tasks get routed first and to better agents
  HOW: Priority scoring determines routing order and agent quality threshold

  PRIORITY SCORING:
    PRIORITY = (Urgency × 0.4) + (Impact × 0.3) + (Strategic_Alignment × 0.2) + (Dependency_Blocking × 0.1)

    Urgency: 1 (days) to 10 (minutes)
    Impact: 1 (cosmetic) to 10 (revenue-critical)
    Strategic_Alignment: 1 (nice-to-have) to 10 (core strategy)
    Dependency_Blocking: 0 (no dependents) to 10 (blocks 5+ teams)

  PRIORITY TIERS:
    P0 — CRITICAL (score 8-10): Route immediately to senior expert
    P1 — HIGH (score 6-8): Route within 4 hours to qualified agent
    P2 — NORMAL (score 4-6): Route within 24 hours
    P3 — LOW (score 2-4): Route within sprint
    P4 — BACKLOG (score <2): Route when capacity available

  PRIORITY-BASED AGENT SELECTION:
    P0 tasks: Top expert in the domain, regardless of current load
    P1 tasks: Qualified agent with capacity
    P2 tasks: Qualified agent with best capacity match
    P3 tasks: Any qualified agent
    P4 tasks: Agent with most available capacity

  STRENGTH: Ensures critical work gets priority attention
  WEAKNESS: Can starve low-priority work if P0 tasks are frequent

---

## 4. Composite Routing Algorithm

The four strategies are combined, not used in isolation:

  STEP 1: CLASSIFY
    Task is classified by type, complexity, required skills, and priority.
    Output: Task requirement profile

  STEP 2: FILTER (Role-Based)
    Filter agents by required role.
    Output: Candidate agent list

  STEP 3: FILTER (Skill-Based)
    Filter candidates by minimum skill levels.
    Output: Qualified candidate list

  STEP 4: FILTER (Capacity-Based)
    Filter qualified candidates by available capacity.
    Output: Available candidate list

  STEP 5: RANK (Priority + Skill Score)
    Rank available candidates:
      RANKING = (skill_match_score × 0.4) + (capacity_score × 0.3) + (recency_bonus × 0.2) + (fairness_bonus × 0.1)

    skill_match_score: How well skills match requirements (0-1)
    capacity_score: How much capacity is available (0-1)
    recency_bonus: Has this agent worked on similar tasks recently? (0-1)
    fairness_bonus: Has this agent been assigned less than average? (0-1)

  STEP 6: ASSIGN
    Top-ranked agent is assigned.
    If top agent rejects within 30 minutes, next candidate is offered.
    If no candidates available, task is queued with escalation.

  STEP 7: CONFIRM
    Assigned agent acknowledges receipt within ACK SLA.
    If no acknowledgment, reassignment triggers.

---

## 5. Special Routing Rules

### 5.1 Emergency Routing
  When a P0 incident occurs:
    1. Incident is classified automatically (by monitoring rules)
    2. SRE on-call is notified immediately (regardless of capacity)
    3. Incident commander is assigned (SRE Lead or designated backup)
    4. Cross-pod specialists are pulled as needed (capacity override)
    5. Normal capacity limits are suspended for P0 incidents

### 5.2 Learning Routing
  When an agent needs to grow in a skill:
    - Assign lower-complexity tasks in that skill area
    - Pair with a senior agent for mentoring
    - Track improvement in skill level
    - Gradually increase complexity as skill improves

### 5.3 Load Balancing Across Pods
  When one pod is overloaded and another is available:
    1. Cross-pod task transfer is proposed by the Delivery Manager
    2. Receiving pod's Engineering Manager approves
    3. Task context is fully transferred (not just the ticket)
    4. Knowledge transfer session (15 min) if needed
    5. Originating pod is notified

### 5.4 Blocked Task Routing
  When a task is blocked:
    1. Blocker is analyzed (what is blocking it?)
    2. Blocker is routed to the appropriate agent/team
    3. Original task remains assigned but marked BLOCKED
    4. When blocker is resolved, original task resumes
    5. Block age is tracked and escalated if >24 hours

---

## 6. Routing Configuration

### 6.1 Pod Assignment Rules

  CRM Core Pod:
    Domains: contacts, companies, deals, activities
    Roles: PM, 2 Backend, 1 Frontend, 1 QA, 1 DevOps
    Capacity: 200 hours/sprint

  CRM Intelligence Pod:
    Domains: analytics, reporting, dashboards, AI features
    Roles: PM, 1 Backend, 1 Frontend, 1 Data Engineer, 1 QA
    Capacity: 160 hours/sprint

  CRM Integration Pod:
    Domains: API, webhooks, third-party connectors, CRDT sync
    Roles: PM, 2 Backend, 1 QA, 1 DevOps
    Capacity: 160 hours/sprint

  Platform Pod:
    Domains: CI/CD, infrastructure, monitoring, security
    Roles: Platform Architect, 2 Engineers, 1 SRE, 1 Security
    Capacity: 200 hours/sprint

### 6.2 Routing Priority Override

  The following can override automatic routing:
    - L1 Executive: Direct assignment to any agent
    - Delivery Manager: Cross-pod assignment
    - Engineering Manager: Intra-pod reassignment
    - Agent self-selection: Agent can claim a task (with manager approval)

---

## 7. Routing Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Task assignment time | <1 hour for P0, <4 hours for P1-P2 | Routing engine |
  | Assignment accuracy (right skill) | >90% | Quality outcome tracking |
  | Capacity utilization balance | <20% variance across pod | Capacity dashboard |
  | Task rejection rate | <5% | Routing logs |
  | Blocked task age | <24 hours average | Block tracking |
  | Cross-pod transfer rate | <10% of tasks | Transfer logs |
  | Routing learning improvement | >5% quality gain per quarter | Outcome analysis |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
