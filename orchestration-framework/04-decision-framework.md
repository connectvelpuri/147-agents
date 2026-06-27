# 04 — Decision-Making Framework

## How 548 Agents Make Decisions Without Exploding Decision Latency

---

## Executive Summary

Without an explicit decision-making framework, every disagreement becomes a
negotiation, every decision requires escalation, and decision latency grows
exponentially with agent count. At 548 agents, unstructured decision-making
would produce weeks of delay for simple architectural choices.

This document defines the complete decision-making system: who decides what,
using which model, with what authority limits, and through what process. The
framework assigns specific decision types to specific agents using models drawn
from RACI, DACI, RAPID, and domain ownership — not as abstract frameworks but
as executable rules that the coordination layer enforces automatically.

---

## 1. Decision Philosophy

### 1.1 Why Decisions Need a Framework

In a 548-agent system, decisions happen constantly:
  - Architecture decisions (database choice, API design, caching strategy)
  - Product decisions (feature priority, scope, design approach)
  - Process decisions (sprint length, review process, deployment cadence)
  - Resource decisions (capacity allocation, team composition)
  - Quality decisions (release readiness, test coverage, security posture)
  - Escalation decisions (severity classification, response priority)

Without a framework:
  - Agents wait for someone else to decide → DECISION LATENCY
  - Multiple agents make conflicting decisions → CONTRADICTION
  - Decisions are made without context → POOR QUALITY
  - Decisions are reversed without process → INSTABILITY
  - No one knows who decided what → ACCOUNTABILITY GAP

### 1.2 Decision Principles

  PRINCIPLE 1: DECIDE AT THE LOWEST COMPETENT LEVEL
    Don't escalate what can be decided locally.
    If a backend engineer can choose between two equivalent libraries,
    they should decide. Don't ask the CTO.

  PRINCIPLE 2: DECIDE WITHIN YOUR DOMAIN
    Product managers decide scope. Engineers decide implementation.
    QA decides quality. Security decides risk. Don't cross domains
    without explicit authority.

  PRINCIPLE 3: DECIDE WITH EVIDENCE
    Every decision should reference: what was considered, what evidence
    was used, what alternatives were rejected, and why.
    "I felt like it" is not a decision rationale.

  PRINCIPLE 4: DECIDE REVERSIBLY WHEN POSSIBLE
    Prefer reversible decisions (can be undone cheaply) over irreversible
    ones (expensive to change). Make reversible decisions fast. Make
    irreversible decisions carefully.

  PRINCIPLE 5: DECIDE TRANSPARENTLY
    Every decision is recorded with its rationale, alternatives considered,
    and expected outcomes. This creates institutional memory and prevents
    "I didn't know we decided that" problems.

---

## 2. Decision Models

The Sovereign Enterprise uses FIVE decision models, each assigned to specific
decision types.

### 2.1 Model: RACI (Responsible, Accountable, Consulted, Informed)

  WHEN TO USE:
    Routine operational decisions
    Sprint-level prioritization
    Standard process execution
    Daily operational choices

  HOW IT WORKS:
    For each decision type, four roles are defined:
      R (Responsible): Does the work to make the decision happen
      A (Accountable): Ultimately answerable for the decision's outcome
      C (Consulted): Provides input before the decision is made
      I (Informed): Notified after the decision is made

  DECISION AUTHORITY:
    The Responsible agent makes the recommendation.
    The Accountable agent makes the final call.
    Consulted agents must be heard (their input is logged) but not obeyed.
    Informed agents receive the decision after it is made.

  EXAMPLE — SPRINT BACKLOG PRIORITIZATION:
    R: Product Manager (proposes priority order)
    A: Delivery Manager (final approval)
    C: Engineering Manager (feasibility), QA Lead (test capacity), Security Engineer (risk)
    I: All pod members, PMO Director

  EXAMPLE — CODE REVIEW APPROVAL:
    R: Author (writes the code)
    A: Reviewer (approves or requests changes)
    C: Tech lead (for complex decisions)
    I: Engineering Manager (metrics tracking)

  ESCALATION:
    If R and A disagree, the decision escalates to A's manager.
    If A is unavailable for >4 hours, A's manager assumes accountability.

### 2.2 Model: DACI (Driver, Approver, Contributor, Informed)

  WHEN TO USE:
    Cross-functional initiatives
    Feature development from concept to launch
    Projects requiring multiple team contributions
    Strategic initiatives with broad impact

  HOW IT WORKS:
    D (Driver): Owns the decision process, drives consensus, delivers the outcome
    A (Approver): Has final say; can be overridden only by their manager
    C (Contributors): Provide expertise, data, and perspective
    I (Informed): Updated on decision and rationale

  KEY DIFFERENCE FROM RACI:
    DACI has ONE approver. RACI can have shared accountability.
    DACI is better for complex, cross-functional decisions.
    RACI is better for routine, well-defined decisions.

  EXAMPLE — CRM DATABASE MIGRATION:
    D: Data Architect (drives the evaluation process)
    A: CTO (final approval)
    C: Backend Lead (impact on APIs), DBA (operational impact),
       Security Engineer (compliance), QA Lead (test strategy impact)
    I: All affected pods, PMO Director, COO

  EXAMPLE — NEW PRODUCT FEATURE:
    D: Product Manager (drives discovery and definition)
    A: CPO (final scope approval)
    C: UX Lead (design), BA (requirements), Eng Manager (feasibility),
       QA Lead (testability), Security Engineer (threat model)
    I: All team members, Delivery Manager, PMO

  DECISION PROCESS:
    1. Driver documents the decision with context, options, and recommendation
    2. Contributors provide input (must respond within SLA)
    3. Driver synthesizes input and refines recommendation
    4. Approver makes final decision
    5. Decision is recorded and communicated to Informed

  TIMELINE:
    - Standard: 48 hours from Driver initiation to Approver decision
    - Urgent: 8 hours
    - Emergency: 2 hours

### 2.3 Model: RAPID (Recommend, Agree, Perform, Input, Decide)

  WHEN TO USE:
    High-stakes decisions with significant organizational impact
    Technology selection (platform, framework, database)
    Architecture decisions affecting multiple teams
    Investment decisions (build vs. buy, vendor selection)

  HOW IT WORKS:
    R (Recommend): Proposes a course of action with evidence
    A (Agree): Must agree BEFORE the decision is finalized (veto power)
    P (Perform): Executes the decision after it is made
    I (Input): Provides information to the Recommender (no veto)
    D (Decide): Makes the final call

  KEY FEATURE: "Agree" has VETO power
    If the "Agree" party does not agree, the decision CANNOT proceed.
    This ensures critical stakeholders are not bypassed.

  EXAMPLE — CRM TECHNOLOGY STACK SELECTION:
    R: Solution Architect (evaluates options, recommends)
    A: Enterprise Architect (must agree it fits enterprise standards)
    A: Security Engineer (must agree it meets security requirements)
    P: Engineering Manager + team (implements the choice)
    I: Backend Lead, Frontend Lead, DevOps Lead (provide input)
    D: CTO (final decision)

  EXAMPLE — CRDT SYNC ARCHITECTURE:
    R: Backend Architect (proposes CRDT approach)
    A: Enterprise Architect (must agree it fits patterns)
    A: Performance Engineer (must agree it meets latency requirements)
    P: Backend Engineers (implement)
    I: Frontend Lead, QA Lead (provide input on API impact)
    D: CTO (final decision)

  DECISION PROCESS:
    1. Recommender documents proposal with evidence and alternatives
    2. Input providers respond with their analysis (within SLA)
    3. Recommender refines proposal based on input
    4. Agree parties review and approve/veto (within SLA)
    5. If all Agree parties approve, Decide party makes final call
    6. If any Agree party vetoes, decision is reworked or escalated
    7. Decision is recorded, Performers begin execution

### 2.4 Model: Domain Ownership

  WHEN TO USE:
    Day-to-day decisions within a well-defined domain
    Technical decisions within a service or component
    Process decisions within a team
    Quality decisions within a testing domain

  HOW IT WORKS:
    Each domain has a designated owner with full authority over decisions
    within that domain. The owner can delegate but remains accountable.

    Domain boundaries are clearly defined:
      - Backend domain: API design, database schema, service architecture
      - Frontend domain: UI design, component library, accessibility
      - QA domain: test strategy, test execution, quality gates
      - Security domain: threat modeling, access control, compliance
      - DevOps domain: CI/CD, infrastructure, deployment
      - Data domain: data models, pipelines, analytics
      - Product domain: scope, priorities, user experience

    Domain owners make decisions without external approval IF:
      - The decision stays within their domain
      - The decision doesn't affect other domains
      - The decision is within budget/capacity constraints

  EXAMPLE — DATABASE SCHEMA CHANGE:
    Domain: Backend
    Owner: Backend Lead
    Decision: Add index to contacts table
    Authority: Full (within their domain)
    Escalation: None needed if no cross-domain impact

  EXAMPLE — NEW UI COMPONENT LIBRARY:
    Domain: Frontend
    Owner: UI/UX Lead
    Decision: Migrate from Material UI to custom component library
    Authority: Full within frontend domain
    Escalation: If it affects backend API contracts → consult Backend Lead
    Escalation: If it affects design system → consult UX Design Lead

### 2.5 Model: Consensus (Democratic)

  WHEN TO USE:
    Architecture decisions affecting multiple domains
    Enterprise standards and conventions
    Technology selections with long-term implications
    Process changes affecting multiple teams

  HOW IT WORKS:
    Defined in detail in Document 01 (Coordination Architecture).
    Summary:
      - Proposal published with evidence and alternatives
      - Reviewers respond: APPROVE / APPROVE WITH CONDITIONS / OBJECTION / ABSTAIN
      - 0-2 objections: Pass with condition resolution
      - 3+ objections: Redesign required
      - CISO objection on security: Automatic hold

  TIMELINE:
    - Standard: 48 hours
    - Urgent: 4 hours
    - Emergency: 30 minutes (CTO override)

---

## 3. Decision Authority Matrix

### 3.1 By Decision Type

  | Decision Type | Model | Recommend | Decide | Escalation |
  |--------------|-------|-----------|--------|------------|
  | Feature priority | RACI | PM | Delivery Manager | CPO |
  | Sprint scope | RACI | PM + Eng Mgr | Delivery Manager | COO |
  | Architecture pattern | RAPID | Solution Arch | CTO | Founder/CEO |
  | Technology selection | RAPID | Tech Lead | CTO | Founder/CEO |
  | Code review | RACI | Author | Reviewer | Eng Manager |
  | Test strategy | Domain | QA Lead | QA Lead | CTO |
  | Release readiness | RAPID | Release Mgr | Delivery Mgr + QA Lead + Security | COO |
  | Security exception | RAPID | Security Eng | CISO | COO + CTO |
  | Budget allocation | DACI | Finance Agent | COO | Executive Council |
  | Team composition | RACI | Eng Manager | COO | Executive Council |
  | Incident severity | Domain | SRE Lead | SRE Lead | CTO |
  | Incident action | Domain | Incident Cmdr | SRE Lead | COO |
  | Customer escalation | DACI | Customer Success | CPO | COO |
  | Compliance violation | RAPID | Security Eng | CISO | Founder/CEO |
  | Process change | Consensus | Any agent | Consensus | Enterprise Arch |
  | Standards change | Consensus | Domain Lead | Enterprise Arch | CTO |

### 3.2 By Layer

  L1 (Executive Council):
    Decides: Strategy, investment, risk appetite, organizational structure
    Model: Consensus (full council)
    Authority: Unlimited (final authority on all matters)
    Speed: Weekly cadence (emergency: immediate)

  L2 (Portfolio & PMO):
    Decides: Portfolio priorities, capacity allocation, reporting standards
    Model: DACI (PMO Director drives, COO approves)
    Authority: Cross-pod decisions within portfolio
    Speed: Daily (urgent: within hours)

  L3 (Product & Design):
    Decides: Feature scope, UX design, business rules, acceptance criteria
    Model: DACI (PM drives, CPO approves)
    Authority: Product scope within roadmap
    Speed: Sprint cadence (urgent: within hours)

  L4 (Architecture & Engineering):
    Decides: Implementation approach, technology choices, code standards
    Model: RAPID (Tech Lead recommends, CTO approves)
    Authority: Implementation within architectural guardrails
    Speed: Daily (urgent: within hours)

  L5 (Quality, Security & Platform):
    Decides: Quality gates, security posture, deployment readiness
    Model: Domain + RAPID (domain owners decide within domain)
    Authority: Gate authority (can block releases)
    Speed: Continuous (urgent: immediate)

  L6 (Operate & Improve):
    Decides: Incident response, operational improvements, documentation
    Model: Domain (SRE Lead for operations, Docs Lead for knowledge)
    Authority: Operational within SLOs
    Speed: Immediate (incidents), weekly (improvements)

---

## 4. Decision Process Templates

### 4.1 Architecture Decision Record (ADR)

  When any agent makes an architecture decision, they create an ADR:

  ADR-NNN: [Title]
    Status: Proposed | Accepted | Deprecated | Superseded by ADR-XXX
    Date: YYYY-MM-DD
    Deciders: [List of agents involved]
    Context: [What is the situation that requires a decision?]
    Decision: [What did we decide?]
    Alternatives Considered:
      1. [Alternative 1] — [Pros/Cons] — Rejected because [reason]
      2. [Alternative 2] — [Pros/Cons] — Rejected because [reason]
    Consequences: [What are the implications of this decision?]
    Evidence: [Data, experiments, benchmarks that informed the decision]
    Review Date: [When should this decision be revisited?]

### 4.2 Decision Log

  Every decision is logged with:
    - Decision ID (sequential)
    - Decision type (RACI/DACI/RAPID/DOMAIN/CONSENSUS)
    - Decision content
    - Agent roles involved
    - Timestamp
    - Rationale
    - Expected outcome
    - Actual outcome (filled in later)
    - Review date

  The decision log is queryable:
    - "What decisions were made about the contacts API?"
    - "Who decided to use PostgreSQL for the CRM?"
    - "What was the last architecture decision by the Enterprise Architect?"

---

## 5. Decision Speed Guarantees

  | Decision Type | Maximum Latency | Auto-Escalation |
  |--------------|----------------|-----------------|
  | Code review | 4 hours | → Eng Manager |
  | Sprint scope | 24 hours | → Delivery Manager |
  | Architecture review | 48 hours | → Enterprise Architect |
  | Technology selection | 72 hours | → CTO |
  | Release approval | 24 hours | → COO |
  | Incident action | 2 hours | → CTO + COO |
  | Security exception | 48 hours | → CISO |
  | Budget allocation | 1 week | → COO |
  | Process change | 1 week | → Enterprise Architect |

---

## 6. Decision Anti-Patterns

  ANTI-PATTERN: DECISION BY COMMITTEE
    Description: Every decision requires approval from 5+ agents
    Impact: Decision latency explodes, accountability diffuses
    Prevention: Assign clear R/A/C/I for every decision type
    Detection: Average decision time >2x target

  ANTI-PATTERN: DECISION BY FIAT
    Description: One agent makes all decisions unilaterally
    Impact: Poor decisions due to lack of input, team disengagement
    Prevention: Mandatory consultation for cross-domain decisions
    Detection: Single agent making >50% of decisions in a domain

  ANTI-PATTERN: DECISION PARALYSIS
    Description: Agents avoid making decisions, waiting for perfect information
    Impact: Nothing moves, work stalls
    Prevention: "70% confidence is enough" principle, time-boxed analysis
    Detection: Decision pending >3x target latency

  ANTI-PATTERN: DECISION AMNESIA
    Description: Decisions are made but not recorded
    Impact: Same decisions re-litigated repeatedly
    Prevention: Mandatory ADR for architecture decisions, decision log for all
    Detection: "I didn't know we decided that" conversations

  ANTI-PATTERN: DECISION REVERSAL
    Description: Decisions are overturned without process
    Impact: Team confusion, wasted work, eroded trust
    Prevention: Reversal requires same authority level + documented rationale
    Detection: Same decision made and reversed >2 times

---

## 7. Decision Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Average decision latency | <48 hours | Decision log |
  | Decision quality (outcome vs expectation) | >80% alignment | Quarterly review |
  | Decision documentation rate | >95% | ADR log audit |
  | Escalation rate | <10% of decisions | Escalation tracking |
  | Decision reversal rate | <5% | Decision log |
  | Stakeholder consultation rate | >90% for cross-domain | Consultation log |
  | Decision-to-action time | <24 hours | Workflow tracking |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
