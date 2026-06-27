# Agent Program: RCC-001 Revenue Orchestrator

> **Division:** Revenue Command Center
> **Primary Function:** Routes every revenue event to the correct agent chain, manages execution dependencies, ensures end-to-end deal workflows complete, and coordinates A/B experiments.
> **LLM Tier:** Complex Reasoning (Opus-class)
> **Criticality:** P0 — without this agent, no work flows between agents
> **Consumes:** AI-001, MO-001/002/003/004, QL-001, SDR-001/003, DS-001, NG-001, PL-001, CS-001
> **Produces:** All agent chain activation events

---

## 1. Core Methodology: Event-Driven DAG Execution

RCC-001 treats every workflow as a Directed Acyclic Graph of agent executions:

```
Incoming Event → Classify → Lookup DAG → Resolve Dependencies → Dispatch Agents → Monitor → Complete/Fail
```

### Key Principles

1. **Events over commands** — RCC-001 never calls agents directly. It publishes events; agents subscribe
2. **Idempotent dispatch** — every event carries a unique `event_id`; agents check `Nats-Msg-Id` before processing
3. **Explicit DAGs** — every workflow has a declared DAG with dep edges, timeouts, and fallback paths
4. **Dead letter everything** — every failed event routes to `revenue.{env}.dead.{original_subject}` for debugging
5. **Human gates at DAG boundaries** — high-risk actions pause the DAG and wait for human approval (via RCC-002)

---

## 2. Workflow DAGs (Phase 1)

### 2.1 New Lead → Prospecting Pipeline
```
new_lead_created
  → SDR-001: Prospect Discovery + AI-001: Account Research (parallel)
  → [gate: ICP verified]
  → SDR-003: Outreach Generation + SDR-004: Sequencing (parallel)
  → [human: review first outreach]
  → SDR-004: Execute Sequence
```

### 2.2 Meeting → Analysis Pipeline
```
meeting_completed (.meeting_scheduled.completed)
  → MO-001: Transcribe + MO-002: Sentiment (parallel)
  → MO-003: Objection Detection + MO-004: Commitment Tracking (parallel)
  → QL-001: Re-score deal
  → [gate: new info requires action?]
  → SDR-003: Follow-up or DS-001: Strategy update
```

### 2.3 Deal Stage Transition Pipeline
```
deal_stage_changed
  → QL-002: Deal Inspection (gate)
  → [inspection passed? → advance / failed → block + notify]
  → QL-001: Re-score
  → DS-001: Strategy Review
  → [if negotiation stage: NG-001: Negotiation Prep]
```

### 2.4 Contract → Close Pipeline
```
contract_sent
  → PL-001: Legal Review + NG-001: Negotiation (parallel)
  → [human: approval if >$50K]
  → contract_signed
  → CS-001: Onboarding Handoff
  → CV-001: Testimonial Request
```

### 2.5 Closed Lost → Learning Pipeline
```
closed_lost
  → DS-003: Win/Loss Analysis
  → KL-001: Knowledge Capture
  → QL-003: Update Disqualification Model
```

---

## 3. Inter-Agent Communication

### Subjects RCC-001 Publishes To

| Subject | When | Event Types |
|---------|------|-------------|
| `revenue.{env}.system.chain.{chain_id}.started` | DAG begins | `AgentChainStarted` |
| `revenue.{env}.system.chain.{chain_id}.completed` | DAG completes | `AgentChainCompleted` |
| `revenue.{env}.system.chain.{chain_id}.failed` | DAG fails | `AgentChainFailed` |
| `revenue.{env}.human.approval.{deal_id}` | Human gate needed | `HumanGateRequired` |
| `revenue.{env}.system.config.reloaded` | Config updated | `ConfigReloaded` |
| `revenue.{env}.system.circuit_breaker.{agent_id}` | Agent failing | `CircuitBreakerTripped` |

### Subjects RCC-001 Subscribes To

| Subject | From | Purpose |
|---------|------|---------|
| `revenue.{env}.deal.*.created` | CRM ingress | New deal pipeline |
| `revenue.{env}.deal.*.meeting_scheduled.completed` | Meeting platform | Meeting analysis |
| `revenue.{env}.deal.*.contract_sent.delivered` | CRM | Contract pipeline |
| `revenue.{env}.deal.*.closed_won.achieved` | CRM | Handoff pipeline |
| `revenue.{env}.deal.*.closed_lost.recorded` | CRM | Learning pipeline |
| `revenue.{env}.deal.*.*.entered` | CRM | Stage transitions |
| `revenue.{env}.agent.*.heartbeat` | All agents | Health monitoring |
| `revenue.{env}.agent.*.failure` | Any agent | Circuit breaker |
| `revenue.{env}.human.approval.*` | Human UI | Gate responses |

---

## 4. Output Specifications

### AgentChainStarted
```json
{
  "chain_id": "ch_a1b2c3",
  "deal_id": "d_7a3f",
  "cause_event": "new_lead_created",
  "dag": [
    {"agent_id": "sdr-001-v1", "subject": "revenue.dev.deal.d_7a3f.prospecting.discover"},
    {"agent_id": "ai-001-v1",  "subject": "revenue.dev.deal.d_7a3f.intelligence.research"}
  ],
  "expected_duration_seconds": 120,
  "fallback_dag": [
    {"agent_id": "sdr-001-v1", "subject": "revenue.dev.deal.d_7a3f.prospecting.discover"}
  ]
}
```

### AgentChainCompleted
```json
{
  "chain_id": "ch_a1b2c3",
  "deal_id": "d_7a3f",
  "duration_seconds": 45.2,
  "agent_results": [
    {"agent_id": "sdr-001-v1", "status": "completed", "events_published": 2},
    {"agent_id": "ai-001-v1",  "status": "completed", "events_published": 5}
  ],
  "next_action": "awaiting_human_review"
}
```

### AgentChainFailed
```json
{
  "chain_id": "ch_a1b2c3",
  "deal_id": "d_7a3f",
  "failed_agent": "ai-001-v1",
  "error": "Account research timed out",
  "fallback_used": true,
  "escalation": "rcc-002"
}
```

---

## 5. Performance Score

| Dimension | Weight | Red (<70) | Amber (70-85) | Green (>85) |
|-----------|--------|-----------|---------------|-------------|
| Workflow completion rate | 35% | <0.80 | 0.80-0.95 | >0.95 |
| Chain resolution latency (p95) | 25% | >2s | 0.5-2s | <0.5s |
| Human gate response (P0) | 20% | >60min | 15-60min | <15min |
| Agent chain failure rate | 20% | >0.10 | 0.05-0.10 | <0.05 |

---

## 6. Feedback & Learning Loop

Human routing corrections logged per event → weekly retrain adjusts DAG priority weights.
- Override rate >15% → triggers AIG-002 prompt optimization
- Monthly audit by AIG-001 for routing accuracy drift
- Circuit breaker auto-retunes when agent consistently fails

---

## 7. Deviations from ceva_agent

| Dimension | ceva_agent | RCC-001 |
|-----------|-----------|---------|
| Scope | Single SDR chain | Multi-agent DAG orchestration |
| State | SQLite, single-process | NATS JetStream, distributed |
| Error handling | Try/except per step | Dead letter + circuit breaker + fallback DAGs |
| Human gates | None | Policy-gated with SLA and escalation |
| Health checks | None | Heartbeat per agent, auto-retune |
| Event model | None (direct calls) | Event-driven with idempotency |
| DAG management | Hardcoded sequence | Declarative DAG definitions with parallel dispatch |
