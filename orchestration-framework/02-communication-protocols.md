# 02 — Agent Communication Protocols

## How 548 Agents Talk to Each Other

---

## Executive Summary

Communication is the nervous system of the agent organization. Without explicit
protocols, agents either talk too much (causing noise), talk too little (causing
blind spots), or talk in incompatible formats (causing misunderstanding).

This document defines the complete communication stack: message formats, channels,
routing rules, timing guarantees, and failure handling. Every agent in the system
must implement these protocols to participate in the enterprise.

The protocols are designed to be:
  - MODEL-AGNOSTIC: Work with GPT-4, Claude, Gemini, Llama, or any future model
  - FRAMEWORK-AGNOSTIC: Work with CrewAI, LangGraph, Semantic Kernel, or custom code
  - SCALE-PROVEN: Handle 500 to 5,000 agents without redesign
  - OBSERVABLE: Every message is logged, traceable, and auditable

---

## 1. Communication Principles

### 1.1 Message Discipline

  PRINCIPLE: Every message must answer six questions:
    1. WHO sent it (agent ID, role, layer)
    2. WHO receives it (agent ID, role, or topic)
    3. WHAT it contains (structured payload with schema)
    4. WHY it was sent (purpose: inform, request, command, escalate)
    5. WHEN it was sent (timestamp, deadline if any)
    6. HOW to respond (expected response type and timeline)

  Violations:
    - Messages without correlation IDs cannot be traced → REJECTED
    - Messages without deadlines create infinite waits → TIMEOUT after SLA
    - Messages without response expectations create dead ends → AUTO-ACK

### 1.2 Communication Axioms

  AXIOM 1: No agent blocks waiting for a message
    Every message exchange is asynchronous. Agents publish, subscribe,
    and poll. No agent enters a "waiting for reply" state.

  AXIOM 2: Every message has exactly one owner
    The sender owns the message until it is acknowledged. If not
    acknowledged within the SLA, the sender escalates.

  AXIOM 3: Messages are immutable
    Once sent, a message cannot be modified. Corrections are new messages
    that reference the original. This preserves audit trails.

  AXIOM 4: Dead messages are detected and handled
    If a message is not acknowledged within its SLA, the system:
      - Alerts the sender
      - Retries once
      - Escalates if still unacknowledged
      - Logs the failure for post-mortem

  AXIOM 5: Channel failures are transparent
    If a communication channel fails, the system:
      - Detects the failure within 30 seconds
      - Routes messages through backup channel
      - Notifies affected agents
      - Replays queued messages when primary channel recovers

---

## 2. Message Formats

### 2.1 Universal Message Envelope

Every message in the system uses this envelope:

```json
{
  "message_id": "uuid-v4",
  "correlation_id": "uuid-v4 or null",
  "in_reply_to": "message_id or null",
  "timestamp": "2026-06-09T14:30:00.000Z",
  "sender": {
    "agent_id": "crm-backend-eng-01",
    "role": "Senior Backend Engineer",
    "layer": "L4",
    "pod": "crm-core-pod"
  },
  "recipient": {
    "type": "agent|topic|role|layer|broadcast",
    "target": "crm-qa-lead",
    "routing": "direct|pub-sub|broadcast|escalation"
  },
  "message_type": "directive|status|query|response|event|escalation|ack",
  "priority": "critical|high|normal|low",
  "ttl_seconds": 3600,
  "deadline": "2026-06-09T16:00:00.000Z or null",
  "response_expected": true,
  "response_type": "ack|decision|data|status",
  "response_ttl_seconds": 1800,
  "payload": {},
  "metadata": {
    "sprint": "12",
    "feature": "crdt-sync",
    "environment": "production"
  }
}
```

### 2.2 Message Type Definitions

  DIRECTIVE
    Purpose: Assign work, change direction, issue command
    Sender: Any layer above recipient
    Response: Ack + estimated completion
    Example: "Implement CRDT sync for contacts module by Friday"

  STATUS
    Purpose: Report progress, share current state
    Sender: Any agent
    Response: Ack only
    Example: "CRDT sync 60% complete, on track for Friday delivery"

  QUERY
    Purpose: Request information
    Sender: Any agent
    Response: Data response within SLA
    Example: "What is the current API response time for /contacts?"

  RESPONSE
    Purpose: Answer a query
    Sender: Agent with requested knowledge
    Response: None (completes the query-response cycle)
    Example: "API response time is 245ms (p95), within SLO"

  EVENT
    Purpose: Notify state change
    Sender: Any agent (usually automated)
    Response: None (informational)
    Example: "Deployment of crm-api v2.4.1 completed successfully"

  ESCALATION
    Purpose: Request help for a blocked or failed situation
    Sender: Any agent
    Response: Resolution or delegation within SLA
    Example: "BLOCKED: Database migration failed. Need DBA assistance."

  ACK
    Purpose: Acknowledge receipt of a message
    Sender: Recipient of any message type
    Response: None (completes the acknowledgment cycle)
    Example: "Received. Will implement CRDT sync. ETA: Friday EOD."

### 2.3 Message Schemas by Domain

  SPRINT EVENT SCHEMA:
    {
      "event_type": "sprint.started|planned|reviewed|completed",
      "sprint_id": "sprint-12",
      "team": "crm-core-pod",
      "velocity": null,
      "completed_items": [],
      "blocked_items": [],
      "carry_over_items": []
    }

  DEPLOYMENT EVENT SCHEMA:
    {
      "event_type": "deployment.started|completed|failed|rolled_back",
      "service": "crm-api",
      "version": "2.4.1",
      "environment": "staging|production",
      "triggered_by": "agent-id",
      "rollback_available": true,
      "health_check_passed": null
    }

  INCIDENT EVENT SCHEMA:
    {
      "event_type": "incident.detected|escalated|resolved|closed",
      "severity": "sev1|sev2|sev3|sev4",
      "service": "crm-api",
      "impact": "description of user impact",
      "root_cause": null,
      "resolution": null,
      "incident_commander": "agent-id"
    }

  QUALITY GATE SCHEMA:
    {
      "gate_id": "G5-build",
      "feature": "crdt-sync",
      "status": "pending|passed|failed",
      "evaluator": "agent-id",
      "criteria": [
        {"name": "PR approved", "met": true},
        {"name": "Tests pass", "met": true},
        {"name": "No sev-1 bugs", "met": true}
      ],
      "blocking": true
    }

---

## 3. Communication Channels

### 3.1 Channel Types

  CHANNEL 1: Event Bus (Primary)
    Protocol: Async pub/sub
    Latency: <100ms
    Throughput: >10,000 events/sec
    Persistence: 7-day retention
    Use: All event-driven communication
    Backup: File-based event log

  CHANNEL 2: Direct Message (Agent-to-Agent)
    Protocol: Request-response
    Latency: <500ms
    Throughput: >1,000 messages/sec per agent
    Persistence: 30-day retention
    Use: Specific queries, coordination between two agents
    Backup: Event bus with direct topic

  CHANNEL 3: Blackboard (Shared State)
    Protocol: Read-write to shared document
    Latency: <1 second
    Throughput: >100 concurrent writers
    Persistence: Permanent (versioned)
    Use: Collaborative problem-solving, incident response
    Backup: Message thread reconstruction

  CHANNEL 4: Workflow Engine (Gated)
    Protocol: DAG execution
    Latency: Depends on step duration
    Throughput: >50 concurrent workflows
    Persistence: Permanent (state machine)
    Use: SDLC processes, approval chains, release pipelines
    Backup: Manual advancement by Delivery Manager

  CHANNEL 5: Consensus Forum (Democratic)
    Protocol: Proposal → Review → Vote
    Latency: 4-48 hours
    Throughput: >10 concurrent proposals
    Persistence: Permanent (decision record)
    Use: Architecture decisions, standards, technology selection
    Backup: Enterprise Architect unilateral authority

### 3.2 Channel Selection Matrix

  | Interaction Type | Primary Channel | Backup Channel | Example |
  |-----------------|-----------------|----------------|---------|
  | Status update | Event Bus | Direct Message | Sprint progress report |
  | Task assignment | Workflow Engine | Direct Command | Sprint backlog item |
  | Question/Answer | Direct Message | Blackboard | "What's the API latency?" |
  | Incident response | Blackboard | Direct Message | Multi-agent debugging |
  | Architecture review | Consensus Forum | Blackboard | Database migration proposal |
  | Emergency alert | Event Bus (critical) | Direct Command | Production outage |
  | Knowledge sharing | Event Bus (learning) | Blackboard | New pattern discovered |
  | Escalation | Direct Command | Event Bus | Blocked dependency |

### 3.3 Channel Routing Rules

  RULE 1: Critical messages use ALL channels simultaneously
    Event Bus + Direct Message + Alert. Redundancy for emergencies.

  RULE 2: Normal messages use the PRIMARY channel only
    Backup channel activated only on failure detection.

  RULE 3: Cross-layer messages always go through the event bus
    Even if direct communication would be faster. Audit trail required.

  RULE 4: Within a pod, any channel is acceptable
    Pods have communication autonomy. They choose what works.

  RULE 5: External messages (to humans) use the Human Interface Channel
    Email, Slack, Telegram, or dashboard. Never raw event bus.

---

## 4. Communication Timing

### 4.1 Service Level Agreements

  | Message Type | ACK SLA | Response SLA | Escalation After |
  |-------------|---------|--------------|-----------------|
  | Critical directive | 30 seconds | 5 minutes | 2 minutes |
  | High directive | 5 minutes | 1 hour | 30 minutes |
  | Normal directive | 1 hour | 4 hours | 2 hours |
  | Query | 5 minutes | 1 hour | 30 minutes |
  | Status update | None | None | None (fire-and-forget) |
  | Event | None | None | None (fire-and-forget) |
  | Escalation | 5 minutes | 1 hour | 30 minutes |
  | ACK | Immediate | N/A | 1 minute |

### 4.2 Timing Guarantees

  GUARANTEE 1: No message goes unacknowledged for more than its ACK SLA
    If no ACK received within SLA:
      - Retry 1 (after ACK SLA)
      - Retry 2 (after 2x ACK SLA)
      - Escalate (after 3x ACK SLA)

  GUARANTEE 2: No directive goes unactioned for more than its Response SLA
    If no response within SLA:
      - Alert recipient's manager
      - Reassign if manager confirms unavailability

  GUARANTEE 3: No escalation goes unresolved for more than 2 hours
    If escalation unresolved after 2 hours:
      - Auto-escalate to next management layer
      - CTO or COO notified directly

### 4.3 Timezone Handling

  All timestamps are UTC. Agents convert to local time for display only.
  SLA calculations use UTC exclusively. No timezone ambiguity.

  If an agent is "offline" (timezone-based):
    - Messages queue until the agent's working hours
    - Critical messages override timezone restrictions
    - Auto-responder indicates return time

---

## 5. Communication Security

### 5.1 Authentication

  Every message must include a valid agent token.
  Tokens are issued by the Identity Service and expire after 24 hours.
  Expired tokens cause message rejection with a re-authentication challenge.

### 5.2 Authorization

  Message routing respects the layer hierarchy:
    - L1 can send to any layer
    - L2 can send to L2, L3, L4, L5, L6
    - L3 can send to L3, L4
    - L4 can send to L4, L5
    - L5 can send to L5, L6
    - L6 can send to L6

  Cross-layer communication against the hierarchy requires explicit authorization.

### 5.3 Encryption

  All messages are encrypted in transit (TLS 1.3).
  Sensitive payloads (credentials, PII, financial data) are encrypted at rest.
  Encryption keys rotate every 24 hours.

### 5.4 Audit Trail

  Every message is logged with:
    - Full envelope (without payload for non-sensitive)
    - Payload hash (for integrity verification)
    - Delivery status (sent, acked, responded, escalated)
    - Latency measurements

  Audit logs are immutable and retained for 90 days.
  Compliance-relevant messages are retained for 7 years.

---

## 6. Communication Patterns by Role

### 6.1 Executive Council (L1)
  Primary: Direct Command (downward), Event Bus (upward)
  Frequency: Daily briefing events, weekly strategy events
  Style: Brief, directive, high-signal
  Anti-pattern: Never sends operational messages directly to L4+

### 6.2 PMO Director (L2)
  Primary: Event Bus (receive status), Direct Command (issue directives)
  Frequency: Continuous (event-driven), weekly portfolio reviews
  Style: Structured, metric-driven, escalation-focused
  Anti-pattern: Never bypasses Delivery Manager to talk to engineers

### 6.3 Product Manager (L3)
  Primary: Workflow Engine (backlog management), Direct Message (clarifications)
  Frequency: Daily backlog updates, sprint ceremonies
  Style: Customer-focused, outcome-driven, acceptance-criteria-heavy
  Anti-pattern: Never changes scope without Delivery Manager awareness

### 6.4 Engineering Manager (L4)
  Primary: Workflow Engine (task assignment), Blackboard (technical decisions)
  Frequency: Daily standup, PR reviews, architecture discussions
  Style: Technical, detail-oriented, blockers-focused
  Anti-pattern: Never bypasses QA Lead to declare "done"

### 6.5 QA Lead (L5)
  Primary: Workflow Gate (quality gates), Event Bus (defect reports)
  Frequency: Continuous test execution, sprint exit criteria
  Style: Evidence-based, gate-focused, risk-aware
  Anti-pattern: Never approves release without test evidence

### 6.6 SRE Lead (L5/L6)
  Primary: Event Bus (monitoring alerts), Blackboard (incident response)
  Frequency: Continuous (monitoring), incident-driven
  Style: Urgency-aware, data-driven, resolution-focused
  Anti-pattern: Never closes an incident without RCA

---

## 7. Communication Anti-Patterns

  ANTI-PATTERN: SPAM BROADCAST
    Description: Agent sends non-critical messages to all agents
    Impact: Attention fragmentation, important messages buried
    Prevention: Topic-based subscriptions, message prioritization
    Detection: >50 messages/day from one agent to >10 recipients

  ANTI-PATTERN: DEAD LETTER
    Description: Message sent but never acknowledged or responded to
    Impact: Lost work, silent failures
    Prevention: ACK SLAs with automatic escalation
    Detection: Message age >2x ACK SLA with no delivery confirmation

  ANTI-PATTERN: TELEPHONE
    Description: Message passed through multiple agents, losing fidelity
    Impact: Distorted information, wrong decisions
    Prevention: Original message always referenced (correlation_id)
    Detection: Message chain depth >3 with content changes

  ANTI-PATTERN: BLAME GAME
    Description: Agents send messages attributing fault rather than solving problems
    Impact: Toxic culture, delayed resolution
    Prevention: Incident blameless post-mortem protocol
    Detection: NLP analysis of incident messages for blame language

  ANTI-PATTERN: MEETING HELL
    Description: Too many synchronous meetings, not enough async communication
    Impact: Productivity loss, context switching
    Prevention: Async-first policy, meeting budget per pod
    Detection: >4 hours/day in synchronous communication

---

## 8. Communication Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Message delivery rate | >99.9% | Event bus monitoring |
  | ACK compliance rate | >98% | Message tracking |
  | Average message latency | <100ms | Bus metrics |
  | Dead letter rate | <0.1% | Message tracking |
  | Escalation rate | <5% of directives | Escalation tracking |
  | Communication noise ratio | <10% non-essential messages | NLP analysis |
  | Cross-pod message volume | <100/day per pod | Bus metrics |
  | Human-facing message volume | <10/day per human | Notification tracking |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
