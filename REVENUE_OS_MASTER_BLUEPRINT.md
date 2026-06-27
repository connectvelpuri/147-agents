# RevenueOS Master Blueprint

> **System:** AI-Powered Revenue Operating System
> **Total Agents:** 108
> **Divisions:** 27
> **Tiers:** 4
> **Version:** 1.0
> **Last Updated:** 2026-06-24
> **Status:** Blueprint — Ready for Build

---

## Table of Contents

1. Executive Summary
2. System Architecture Overview
3. Agent Architecture
4. Event & Data Flow
   - 4.1 Standard Deal Flow
   - 4.2 Subscription & Escalation Paths
   - 4.3 Cross-Division Coordination
5. State Management
6. Human-in-the-Loop Design
7. Security Architecture
8. Training & Knowledge Pipeline
9. Scaling & Performance
10. Cost Model
11. Key Design Decisions & Rationale
12. Appendices
    - A: Division-to-Division Interaction Matrix
    - B: Event Subject Naming Convention
    - C: Agent Registry Summary
    - D: Key Metrics and SLAs

---

## 1. Executive Summary

**RevenueOS** is an event-driven, AI-agent orchestration platform that automates the entire B2B revenue lifecycle — from prospecting and qualification through negotiation, legal, close, and post-sale customer success. 108 specialized AI agents across 27 divisions operate as a coordinated mesh, communicating exclusively through typed events on a NATS JetStream backbone.

**Core insight:** A revenue organization is not a single process but a network of specialized decision-making nodes (SDR, qualification, deal strategy, negotiation, legal, value engineering, customer success, etc.). Each node has distinct data needs, reasoning patterns, LLM complexity requirements, and latency tolerances. Monolithic CRM overlays or single-LLM systems fail because they force a uniform architecture on heterogeneous workflows. RevenueOS matches each node to its optimal agent design — isolated, independently scalable, and connected only through well-defined event contracts.

**Key architectural decisions:**
- **NATS JetStream over Kafka** — NATS provides request-reply, KV store, object store, queue groups, and exactly-once delivery in a single ~25MB binary. Kafka requires 3+ services (broker, ZK/KRaft, Connect, Schema Registry). For 108 agents exchanging ~500K events/month, NATS delivers lower latency, simpler ops, and sufficient throughput.
- **gRPC + MCP hybrid** — Agents use gRPC for high-throughput internal communication (event production, KV reads/writes) and MCP for external LLM and tool interactions. This decouples agent-agnostic messaging infrastructure from model-specific protocols.
- **Event sourcing** — Every agent action is an immutable event. The full deal audit trail is reconstructable by replaying events. No data is ever mutated in place in the event store (NATS JetStream retains per-subject history).
- **Kubernetes** — All agents deploy as pods in a single K8s cluster with HPA based on NATS queue depth. Monorepo, single Docker image, per-agent entrypoints.

**Scale:**
- 108 agents across 27 divisions organized into 4 tiers (Core Revenue Engine, Deal Acceleration, Support & Intelligence, Infrastructure)
- 4 LLM tiers: Complex Reasoning (Opus-class), Moderate (Sonnet-class), Simple (Haiku-class), Non-LLM (ML models)
- ~17K events/day at 1000 deals/month steady state

**Expected impact:**
- 3-5x sales productivity (agents handle research, drafting, scoring, analysis)
- 15-25% win rate improvement (systematic qualification, objection response, negotiation prep)
- 50% reduction in sales cycle length (parallel agent execution replaces sequential human workflows)
- 80% reduction in manual CRM data entry
- 95% of standard deals processed with zero human touch below $50K

---

## 2. System Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KUBERNETES CLUSTER                                 │
│                                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     ┌──────────────────┐         │
│  │ Agent    │  │ Agent    │  │ Agent    │     │ NATS JetStream   │         │
│  │ Pool 1   │  │ Pool 2   │  │ Pool N   │ ... │ (3-node cluster) │         │
│  │ (Tier 1) │  │ (Tier 2) │  │ (Tier 4) │     │                  │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │  ┌──────────┐   │         │
│       │              │             │           │  │Subjects  │   │         │
│       │   gRPC/MCP   │             │           │  │.deals.*  │   │         │
│       ├──────────────┼─────────────┼───────────┼─►│.meetings*│   │         │
│       │              │             │           │  │.system.* │   │         │
│       │              │             │           │  │.alerts.* │   │         │
│       │              │             │           │  └──────────┘   │         │
│       │              │             │           │  ┌──────────┐   │         │
│       │              │             │           │  │ KV Store │   │         │
│       │              │             │           │  │.deals.*  │   │         │
│       │              │             │           │  │.accounts*│   │         │
│       │              │             │           │  └──────────┘   │         │
│       └──────────────┴─────────────┴───────────┼──────────────────┼─────────┤
│                                                │                  │         │
│  ┌─────────────────────────────────────────────┴──────────────┐   │         │
│  │                OBSERVABILITY STACK                          │   │         │
│  │  OpenTelemetry ─► Tempo (traces) ─► Grafana                │   │         │
│  │  Prometheus ─► metrics per agent (events, latency, errors) │   │         │
│  │  Loki ─► structured log aggregation per agent              │   │         │
│  └────────────────────────────────────────────────────────────┘   │         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │                STATE & PERSISTENCE LAYER                     │           │
│  │  NATS KV ─► deal state, scoring, approvals (ephemeral)      │           │
│  │  PostgreSQL ─► long-term CRM data, agent audit log, training │           │
│  │  S3 ─► transcript archives, proposal PDFs, contract storage  │           │
│  │  Redis ─► session cache, LLM response cache, rate limits     │           │
│  └──────────────────────────────────────────────────────────────┘           │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────┐           │
│  │                HUMAN INTERFACE LAYER                         │           │
│  │  Slack/Teams bot ─► approval requests, alerts, summaries     │           │
│  │  Web dashboard ─► deal pipeline, agent activity, KPIs        │           │
│  │  Email ─► digest, escalation notifications, manual overrides  │           │
│  └──────────────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 NATS as the Nervous System

Every agent communication flows through NATS. The system uses four NATS primitives:

**1. Event Subjects (Pub/Sub)**
Agents publish typed events to subject hierarchies. Any agent with the correct subscription receives relevant events.
```
revenueos.deal.{deal_id}.stage_changed
revenueos.meeting.{meeting_id}.transcript_ready
revenueos.system.agent.{agent_id}.heartbeat
revenueos.alert.{severity}.{category}
```

**2. KV Store (Shared State)**
Per-deal state is maintained in NATS KV buckets with sub-key access control.
```
Bucket: deals
  Key: metadata.{deal_id}      -> deal-level metadata (read: all agents)
  Key: scoring.{deal_id}       -> qualification scores (read: QL*, DS*, RO*)
  Key: approvals.{deal_id}     -> approval state (read: RCC-002, DS-001)
  Key: conversation.{deal_id}  -> ongoing conversation log (read: all agents)
  Key: docs.{deal_id}          -> document generation state (read: CT*, PL*)
```

**3. Queue Groups (Work Distribution)**
When multiple instances of the same agent run (for scaling), they join a queue group. NATS delivers each message to exactly one consumer in the group.
```
Subject: revenueos.deal.*.stage_changed  -> Queue: "qualification-scorers"
Subject: revenueos.deal.*.objection       -> Queue: "objection-handlers"
```

**4. Request-Reply (Synchronous Calls)**
Some workflows require synchronous request-reply (e.g., Deal Planner asking Qualification for current score). NATS supports this natively.
```
Agent DS-001 publishes to: revenueos.rpc.ql-001.get_score.{deal_id}
Agent QL-001 replies on:   _INBOX.{reply_subject}
Timeout: 5 seconds (if no reply, orchestrator retries or escalates)
```

### 2.3 Agent Deployment Model

**Monorepo + Single Image:**
```
/revenueos
  /agents
    /rcc-001- orchestrator/
    /mo-001-transcription/
    /sdr-003-outreach/
    ... (108 agent directories)
  /internal
    /nats/         -- NATS client helpers, subject constants
    /proto/        -- Shared protobuf definitions
    /state/        -- KV state access patterns
    /llm/          -- LLM client abstraction (tier routing)
    /observability/-- OpenTelemetry setup, metric definitions
  /deploy
    /k8s/          -- Per-division HPA manifests, ConfigMaps
    /docker/       -- Dockerfile (multi-stage, ~400MB final image)
  /cmd
    orchestrator/main.go
    transcription/main.go
    ... (108 entrypoints)
```

**Key deployment decisions:**
- **Same image, different entrypoints** — A single Docker image contains all 108 agents. Kubernetes pods specify which agent to run via the `ENTRYPOINT` override. This reduces image build time, simplifies versioning, and ensures consistent base dependencies across all agents.
- **Kubernetes HPA** — Each division (or individual hot agents) has an HPA based on NATS queue depth. When the `revenueos.deal.*.scoring` subject has 100+ pending messages, the QL division scales from 2 to 5 pods. Scale-down cooldown is 5 minutes to avoid thrash.
- **Resource requests/limits per LLM tier:**
  - Complex Reasoning (Opus): 4 CPU, 16GB RAM (LLM API calls are external, but context processing is local)
  - Moderate (Sonnet): 2 CPU, 8GB RAM
  - Simple (Haiku): 1 CPU, 4GB RAM
  - Non-LLM: 0.5 CPU, 2GB RAM
- **Node affinity** — Agents with high NATS I/O (MO-001 transcription, RCC-001 orchestrator) are affinity-scheduled to nodes with local NATS leaf nodes for lower latency.

### 2.4 Four Deployment Profiles

| Profile | Description | Examples | Resource Spec | Scaling Trigger |
|---------|-------------|----------|---------------|-----------------|
| **LLM-heavy** | Heavy context processing, frequent LLM calls | RCC-001, QL-001, DS-001, NG-001 | 4 CPU, 16GB RAM, GPU optional (local models) | Queue depth + request latency |
| **DB-heavy** | KV reads/writes, PostgreSQL queries, batch scanning | RI-001, RO-001, RO-002, KL-001 | 2 CPU, 8GB RAM, high disk IOPS | Queue depth + batch interval |
| **API-heavy** | External API calls (ZoomInfo, LinkedIn, CRM) | SDR-001, SDR-002, MO-001, AI-001 | 2 CPU, 4GB RAM, stable network | Rate limit headroom + queue |
| **Fast-stateless** | Pure classification, routing, formatting | RO-005, MO-006, RCC-006, QL-002 | 0.5 CPU, 2GB RAM | Minimal — long-lived pods |

### 2.5 Observability

**Tracing (OpenTelemetry + Tempo):**
Every agent execution generates a trace span:
- `agent.execute` — includes agent ID, input event type, LLM tier, duration
- `llm.call` — model name, prompt tokens, completion tokens, latency
- `kv.read` / `kv.write` — bucket, key, duration
- `event.publish` — subject, size, duration

Traces are correlated by `deal_id` and `chain_id` (orchestration workflow ID). The full end-to-end trace of a deal from lead creation to close is queryable in Grafana Tempo: "Show me every agent that touched deal 1047 and how long each took."

**Metrics (Prometheus + Grafana):**
Per-agent metrics (labels: `agent_id`, `division`, `llm_tier`, `criticality`):
- `agent_executions_total` — counter
- `agent_execution_duration_seconds` — histogram (p50, p95, p99)
- `agent_errors_total` — counter, labeled by error type
- `llm_tokens_total` — counter, labeled by model and tier
- `llm_cost_total` — counter, derived from token counts
- `nats_messages_published_total` — per subject
- `nats_queue_depth` — gauge, per queue group
- `deal_latency_hours` — histogram, stage entry to stage exit

**Per-Agent Token Counters (from Day 1):** Every agent MUST emit these metrics on every invocation:
- `agent.tokens.prompt` — prompt token count (counter, labels: agent_id, model)
- `agent.tokens.completion` — completion token count (counter, labels: agent_id, model)
- `agent.tokens.total` — sum of both (counter, labels: agent_id, model)
- `agent.cost.estimated` — estimated cost (counter, labels: agent_id, model) calculated as tokens × model rate
These feed into the Cost Governor (RCC-006) which enforces per-agent budgets and alerts on cost anomalies. Aggregated to `agent.tokens.daily` and `agent.cost.daily` for budget tracking.

**Logging (Loki):**
Structured JSON logs per agent execution:
```json
{
  "timestamp": "2026-06-24T14:30:00Z",
  "agent_id": "ql-001",
  "deal_id": "1047",
  "event": "deal.stage_changed",
  "input_tokens": 4520,
  "output_tokens": 320,
  "latency_ms": 3400,
  "llm_model": "claude-opus-4.5",
  "result": "BANT score computed",
  "error": null
}
```

**Health Checks:**
- NATS connection status (liveness probe connects to NATS, publishes heartbeat to `revenueos.system.agent.{id}.heartbeat`)
- LLM API reachability (readiness probe calls LLM with minimal prompt)
- KV read/write test (readiness probe reads expected key from KV store)
- Dead agent detection: the Escalation Manager (RCC-005) monitors heartbeat subjects. If an agent misses 3 consecutive heartbeats (30-second interval), RCC-005 triggers escalation.

---

## 3. Agent Architecture

### 3.1 Agent Lifecycle

Every agent follows a strict lifecycle:

```
REGISTER → SUBSCRIBE → PROCESS → PUBLISH → ACK
```

**1. REGISTER:** On startup, the agent connects to NATS and registers itself in the `revenueos.system.registry` KV store:
```json
{
  "agent_id": "ql-001",
  "status": "online",
  "started_at": "2026-06-24T14:00:00Z",
  "llm_tier": "complex",
  "subjects": ["revenueos.deal.*.scoring", "revenueos.rpc.ql-001.*"],
  "version": "1.0.0"
}
```
The Escalation Manager (RCC-005) monitors this registry. Any agent that does not re-register within 60 seconds of its heartbeat stopping is flagged as dead.

**2. SUBSCRIBE:** The agent subscribes to its declared subjects. Subscriptions are either:
- **Pub/Sub** — receives every event on the subject (for broadcast events like `system.config_changed`)
- **Queue Group** — receives one event among all instances (for work distribution)
- **Request-Reply** — subscribes to an `_INBOX` subject for synchronous RPC responses

**3. PROCESS:** The core execution loop:
1. Deserialize event from protobuf
2. Validate event fields (schema check)
3. Load relevant state from KV store (read-only projection)
4. Build LLM prompt using template + KV state
5. Call LLM (with retry, exponential backoff: 1s, 2s, 4s, 8s, max 16s)
6. Parse LLM output (structured JSON extraction)
7. Validate output schema
8. If output validation fails → retry LLM with error context (max 2 retries)
9. Return result struct

**4. PUBLISH:** The agent publishes zero or more output events to NATS subjects:
- Primary result event (e.g., `revenueos.deal.1047.scored`)
- Error event if processing failed
- Metrics event (if applicable)

**5. ACK:** The agent acknowledges the NATS message. NATS is configured for:
- **At-least-once delivery** — if the agent crashes before ack, the message is redelivered
- **Max delivery attempts:** 3 (configurable per subject)
- **Dead letter queue:** After max attempts, message goes to `revenueos.dlq.{original_subject}` for manual inspection

### 3.2 Per-Agent Contract

Every agent defines a strict contract in its `spec.json` (validated at build time against a JSON Schema):

```json
{
  "agent_id": "ql-001",
  "division": "qualification-team",
  "tier": 1,
  "llm_tier": "complex",
  "criticality": "P0",
  "subscribes": [
    {
      "subject": "revenueos.deal.*.scoring_required",
      "type": "queue",
      "queue_group": "qualification-scorers"
    },
    {
      "subject": "revenueos.rpc.ql-001.*",
      "type": "request-reply",
      "timeout_ms": 5000
    }
  ],
  "publishes": [
    {
      "subject": "revenueos.deal.{deal_id}.scored",
      "schema": "BantMeddpiccScore"
    },
    {
      "subject": "revenueos.deal.{deal_id}.disqualification_recommended",
      "schema": "DisqualificationRecommendation"
    }
  ],
  "kv_read_permissions": [
    "deals.metadata.{deal_id}",
    "deals.conversation.{deal_id}",
    "accounts.{account_id}"
  ],
  "kv_write_permissions": [
    "deals.scoring.{deal_id}"
  ],
  "criticality": "P0",
  "max_execution_ms": 15000,
  "max_retries": 3,
  "training_corpus": ["MEDDIC", "BANT", "Command of the Message"]
}
```

This contract is:
- Used by the Orchestrator (RCC-001) to route events correctly
- Used by the Capacity Governor (RCC-006) to estimate token consumption per agent
- Used by Security to enforce KV permissions at the NATS level
- Validated at CI/CD time against the master registry

### 3.3 Need-to-Know Data Access

Agents do not have unfettered access to the entire deal state. Each agent receives only the KV sub-keys it needs, enforced at the NATS level:

**Principle:** An agent reads the minimal projection required for its function.

| Agent | Reads | Does NOT read |
|-------|-------|---------------|
| QL-001 (Scorer) | `deals.metadata.{id}`, `deals.conversation.{id}`, `accounts.{account_id}` | Pricing, legal terms, approval chain |
| NG-001 (BATNA) | `deals.metadata.{id}`, `deals.scoring.{id}`, `accounts.{account_id}`, competitive data | Meeting transcripts, internal coaching notes |
| CS-001 (Health) | `accounts.{account_id}`, usage data, support data | Pricing, negotiation history, internal strategies |
| PL-001 (Legal) | `deals.metadata.{id}`, `deals.docs.{id}`, standard terms | Buyer psychology profiles, competitive intel |

**Implementation:** NATS KV supports permissions on a per-key-prefix basis via the auth callout system. Each agent connects with a client certificate whose CN is `agent.{agent_id}`. The NATS auth callout maps the CN to a set of KV read/write patterns and subject publish/subscribe patterns.

### 3.4 Scaling Tiers

| Tier | Name | Agents | Cold Start | Warm Pool | Hot Pool |
|------|------|--------|------------|-----------|----------|
| **Tier 1** | Core Revenue Engine | 38 | NA | 2 pods always warm | Scale to 10 on queue depth > 50 |
| **Tier 2** | Deal Acceleration | 24 | NA | 1 pod always warm | Scale to 5 on queue depth > 30 |
| **Tier 3** | Support & Intelligence | 30 | 30s cold start (KV load) | 1 pod always warm | Scale to 3 on queue depth > 30 |
| **Tier 4** | Infrastructure & Governance | 16 | 10s cold start | 1 pod always warm (batch) | Scale to 2 on queue depth > 100 |

**Cold start:** When a pod starts for the first time:
1. Pull image (already cached on node) — ~2s
2. Load agent config from ConfigMap — ~1s
3. Connect to NATS cluster — ~3s
4. Register in system registry — ~1s
5. Subscribe to subjects — ~2s
6. Load KV state for any in-flight deals — ~5-30s depending on deal count
7. Start processing — first event ~10-40s from pod creation

**Warm pool:** Tier 1 agents maintain a minimum of 2 pods even at zero load. This guarantees sub-second response for new events. Cost: ~$200/month per agent pair at full time (est. $7,600/month for all Tier 1 warm pools — see §10.2 for detailed breakdown). These are NOT included in the base infrastructure estimate and must be budgeted separately.

**Hot pool:** Additional pods spin up based on NATS queue depth. HPA rules:
- Scale up if queue depth > 50 for 30 seconds
- Scale up by 2 pods (aggressive)
- Scale down if queue depth < 10 for 5 minutes
- Scale down by 1 pod (conservative)

---

## 4. Event & Data Flow

### 4.1 Standard Deal Flow

This section traces a complete deal lifecycle from prospecting through closed-won, showing which agents activate at each stage.

```
DEAL LIFECYCLE — STANDARD PATH
═══════════════════════════════

PHASE 0: PROSPECTING
─────────────────────

  SDR-001 (Multi-Channel Prospector)
    [scan: every 6h] Discovers new prospect matching ICP
    Publishes: revenueos.discovery.new_prospect.{prospect_id}
    ↓
  SDR-002 (Intent Signal Monitor)
    [scan: every 24h] Aggregates intent signals
    Publishes: revenueos.intent.signal.{prospect_id}
    ↓
  SDR-005 (Account Researcher)
    [trigger: prospect_assigned] Produces research brief
    Publishes: revenueos.research.brief_ready.{prospect_id}
    ↓
  SDR-003 (Personalized Outreach Generator)
    [trigger: outreach_triggered] Generates first email/LinkedIn message
    Publishes: revenueos.outreach.draft_ready.{prospect_id}
    ↓
  SDR-004 (Follow-Up Sequencing Engine)
    [trigger: initial_outreach_sent] Begins multi-touch sequence
    Publishes: revenueos.outreach.sequence_started.{prospect_id}

  HUMAN: SDR reviews and sends outreach (or auto-send if confidence > 0.95)

PHASE 1: MEETING
────────────────

  Prospect replies / books meeting
  Event: revenueos.meeting.scheduled.{meeting_id}
    ↓
  MO-001 (Transcription)
    [trigger: meeting_started] Begins real-time transcription
    Publishes: revenueos.meeting.transcript_chunk.{meeting_id}
    ↓
  MO-002 (Sentiment Analyst) — real-time
  MO-003 (Objection Detector) — real-time
    **MO-003 (Objection Detection) Latency SLA: <5 seconds from utterance to alert.** Objection detection must process transcript chunks within 5 seconds to enable real-time coaching (MO-007) and deal risk scoring. Measured as p95 latency. If >5s for 3 consecutive chunks, revert to batch processing (post-meeting report) and alert human.
  MO-004 (Commitment Tracker) — real-time
    [trigger: transcript_chunk] All three run per chunk
    Publishes: sentiment, objection_log, commitment_log per chunk
    ↓
  BP-002 (Buyer Personality Profiler)
    [trigger: first_meeting] Constructs initial personality profile
    Publishes: revenueos.psych.profile_ready.{deal_id}
    ↓
  MO-005 (Question Quality Scorer) — post-meeting
  MO-006 (Talk Ratio Analyst) — post-meeting
    [trigger: full_transcript] Run full analysis

  HUMAN: SDR reviews meeting highlights, objection log, commitment tracker

PHASE 2: QUALIFICATION
──────────────────────

  Event: revenueos.deal.{deal_id}.scoring_required
    ↓
  QL-001 (BANT/MEDDPICC Scorer)
    Scores deal against BANT and MEDDPICC
    Requests additional discovery if gaps exist
    Publishes: revenueos.deal.{deal_id}.scored
    ↓
  QL-002 (Deal Inspector)
    Validates CRM data quality, scores pipeline hygiene
    Publishes: revenueos.deal.{deal_id}.inspected
    ↓
  QL-004 (Champion Validator)
    Assesses champion strength from meeting transcripts
    Publishes: revenueos.deal.{deal_id}.champion_assessed
    ↓
  QL-005 (Budget Verification Agent)
    Validates budget existence and adequacy
    Publishes: revenueos.deal.{deal_id}.budget_verified
    ↓
  QL-006 (Timeline Assessment Agent)
    Validates timeline credibility
    Publishes: revenueos.deal.{deal_id}.timeline_assessed
    ↓
  QL-003 (Disqualification Engine)
    If scores below threshold, recommends disqualification
    Publishes: revenueos.deal.{deal_id}.disqualification_recommended

  HUMAN GATE (if deal < $50K): Auto-qualify if MEDDPICC > 70
  HUMAN GATE (if deal > $50K): Manager reviews qualification summary
    Human approves or requests more discovery

PHASE 3: DISCOVERY
──────────────────

  Event: revenueos.deal.{deal_id}.discovery_required
    ↓
  DC-001 (Problem Diagnosis Agent)
    Analyzes transcripts for root causes behind symptoms
    Publishes: revenueos.deal.{deal_id}.root_causes
    ↓
  DC-002 (Gap Analyst)
    Maps current vs future state gap
    Publishes: revenueos.deal.{deal_id}.gap_analysis
    ↓
  DC-003 (Stakeholder Mapper)
    Identifies all stakeholders, influence, and relationships
    Publishes: revenueos.deal.{deal_id}.stakeholder_map
    ↓
  DC-004 (Needs Hierarchy Builder)
    Builds must-have/should-have/aspiration hierarchy
    Publishes: revenueos.deal.{deal_id}.needs_hierarchy
    ↓
  DC-005 (Decision Process Mapper)
    Maps buying process, gates, approval chain
    Publishes: revenueos.deal.{deal_id}.decision_process
    ↓
  DC-006 (Technical Environment Mapper)
    Maps tech stack, integration points, constraints
    Publishes: revenueos.deal.{deal_id}.tech_environment

PHASE 4: VALUE ENGINEERING
──────────────────────────

  Event: revenueos.deal.{deal_id}.value_engineering_required
    ↓
  VE-001 (ROI Calculator Builder)
    Builds buyer-specific ROI model
    Publishes: revenueos.deal.{deal_id}.roi_model
    ↓
  VE-002 (TCO Analyzer)
    Models current vs proposed TCO
    Publishes: revenueos.deal.{deal_id}.tco_analysis
    ↓
  VE-003 (Business Case Generator)
    Generates procurement-ready business case
    Publishes: revenueos.deal.{deal_id}.business_case
    ↓
  VE-004 (Competitive Comparison Agent)
    Produces side-by-side comparison
    Publishes: revenueos.deal.{deal_id}.competitive_comparison
    ↓
  VE-005 (Cost of Inaction Modeler)
    Quantifies cost of delay/inertia
    Publishes: revenueos.deal.{deal_id}.cost_of_inaction
    ↓
  VE-006 (Risk-Adjusted ROI Agent)
    Probability-weights ROI for risk
    Publishes: revenueos.deal.{deal_id}.risk_adjusted_roi

  HUMAN: Sales rep reviews value deck before presenting to buyer

PHASE 5: DEAL STRATEGY
──────────────────────

  Event: revenueos.deal.{deal_id}.strategy_required
    ↓
  DS-001 (Deal Planner)
    Creates comprehensive deal plan with milestones
    Publishes: revenueos.deal.{deal_id}.deal_plan
    ↓
  DS-002 (Competitive Positioning Strategist)
    Develops competitive positioning approach
    Publishes: revenueos.deal.{deal_id}.competitive_strategy
    ↓
  DS-004 (Price Optimizer)
    Recommends optimal pricing
    Publishes: revenueos.deal.{deal_id}.price_recommendation
    ↓
  DS-005 (Discount Authority Agent)
    Enforces discount policies, recommends concessions
    Publishes: revenueos.deal.{deal_id}.discount_authority

PHASE 6: PROPOSAL & CONTENT
───────────────────────────

  Event: revenueos.deal.{deal_id}.content_required
    ↓
  CT-001 (Value Messaging Generator)
    Crafts persona-specific messaging
    ↓
  CT-002 (Proposal Generator)
    Assembles full proposal from modular components
    Publishes: revenueos.deal.{deal_id}.proposal_draft
    ↓
  CT-003 (Case Study Adapter)
    Adapts case study to prospect context
    ↓
  CT-005 (Presentation Builder)
    Builds stage-appropriate deck
    ↓
  BP-003 (Communication Style Adapter)
    Adapts all documents to buyer's communication style

  HUMAN GATE: Sales rep reviews proposal before sending

PHASE 7: NEGOTIATION
────────────────────

  Event: revenueos.deal.{deal_id}.negotiation_required
    ↓
  NG-001 (BATNA Analyst)
    Assesses our and buyer's alternatives
    Publishes: revenueos.deal.{deal_id}.batna_assessment
    ↓
  NG-002 (Concession Planner)
    Designs concession sequence
    Publishes: revenueos.deal.{deal_id}.concession_plan
    ↓
  NG-003 (Procurement Defense Agent)
    Anticipates procurement tactics
    Publishes: revenueos.deal.{deal_id}.procurement_alert
    ↓
  NG-004 (Terms Optimizer)
    Analyzes contract terms impact
    ↓
  NG-005 (Leverage Identifier)
    Continuously identifies leverage sources
    ↓
  NG-006 (Contract Redlining Agent)
    Reviews buyer redlines, generates counter-redlines
    Publishes: revenueos.deal.{deal_id}.redline_analysis
    ↓
  BP-001 (Cognitive Bias Detector)
    Detects anchoring, framing, status quo bias in negotiation
    BP-005 (Influence Principle Applicator)
    Recommends ethical influence tactics

  HUMAN GATE (deal > $50K OR non-standard terms):
    Deal Desk / Legal must approve pricing and terms

PHASE 8: PROCUREMENT & LEGAL
─────────────────────────────

  Event: revenueos.deal.{deal_id}.legal_required
    ↓
  PL-001 (Procurement Process Agent)
    Guides through procurement workflow
    ↓
  PL-002 (Legal Terms Agent)
    Reviews and drafts contract language
    ↓
  PL-003 (Compliance Checker)
    Validates deal against regulatory requirements
    ↓
  PL-004 (Security Reviewer)
    Reviews security requirements
    Publishes: revenueos.deal.{deal_id}.security_cleared
    ↓
  SC-001 (Data Privacy Agent)
    Validates data processing terms
    ↓
  SC-002 (Export Control Agent)
    Checks export control compliance
    ↓
  SC-003 (Risk Scoring Agent)
    Scores overall deal risk for legal

  HUMAN GATE: Deal only closes when all legal and security reviews pass

PHASE 9: CLOSE
──────────────

  Event: revenueos.deal.{deal_id}.close_ready
    ↓
  RCC-001 (Revenue Orchestrator)
    Validates all gates passed, all approvals obtained
    ↓
  RO-005 (Commission Tracker)
    Calculates commission for the deal
    ↓
  CS-001 (Customer Health Scorer)
    Initializes baseline health score for new customer
    ↓
  CS-003 (Expansion Identifier)
    Begins monitoring for expansion opportunities
    ↓
  Event: revenueos.deal.{deal_id}.closed_won
    ↓
  DS-003 (Win/Loss Analyst)
    Runs win analysis on closed-won deal
    ↓
  KL-001 — KL-006 (Knowledge & Learning agents)
    Extract learnings, update playbooks, retrain agents

  HUMAN: Rep marks deal closed-won in CRM
```

### 4.2 Subscription & Escalation Paths

#### Urgent Deal Path (High-Value Override)

For deals above $250K or flagged as strategic, the standard queue is overridden:

```
1. Deal created with value > $250K
2. Event: revenueos.deal.{deal_id}.priority_override
3. RCC-001 creates express chain: skips standard queue for priority lane
4. All Tier 1 agents execute in parallel (not sequential)
5. Human gate SLAs reduced: Urgent (15min), High (1hr), Standard (4hr)
6. RCC-005 monitors every agent execution with 2x standard SLA
7. If any agent fails or times out → immediate escalation to human
8. Daily executive summary pushed to VP Sales
```

**Parallel vs Sequential:** Standard deals process agents sequentially within a phase (e.g., QL-001 then QL-002 then QL-003). Urgent deals run all qualification agents in parallel and merge results. This reduces phase time from ~15 minutes to ~3 minutes.

#### Slipping Deal Path (At-Risk Recovery)

When a deal shows signs of slipping, additional agents activate:

```
Triggers (any of):
  - Deal inactive > N days at current stage
  - Qualification score dropped by > 20 points
  - Key stakeholder went dark
  - Competitor mentioned in last 3 interactions
  - Champion left the company

Activated:
  RCC-005 (Escalation Manager) — creates slip recovery plan
  QL-003 (Disqualification Engine) — re-evaluates if deal is salvageable
  DS-001 (Deal Planner) — creates recovery plan with new timeline
  BP-004 (Emotional State Tracker) — checks for buyer disengagement
  VE-005 (Cost of Inaction Modeler) — refreshes urgency narrative
  RI-002 (Relationship Health Scorer) — recalculates relationship health

Human notified with: slip summary, recovery recommendation, escalation option
```

#### Lost Deal Path (Win/Loss Analysis)

```
1. Event: revenueos.deal.{deal_id}.lost
2. DS-003 (Win/Loss Analyst) triggers automated analysis:
   - Meeting transcripts analyzed for where deal turned
   - Objections review — were any unaddressed?
   - Competitor analysis — who won and why
   - Pricing analysis — was price a factor?
   - Qualification analysis — was deal properly qualified?
3. KL-001 (Pattern Extraction Agent) updates win/loss patterns
4. KL-004 (Playbook Updater) updates playbooks with new learnings
5. CT-004 (Battle Card Updater) updates competitive battle cards
6. SDR-001 (Prospector) logs contact as do-not-pursue or nurture
7. Human receives: 1-page loss analysis with systemic recommendations
```

#### Renewal Path (Existing Customer)

```
1. CS-004 (Renewal Risk Manager) — triggers at T-90 days
2. CS-001 (Customer Health Scorer) — current health assessment
3. CS-002 (Adoption Monitor) — usage trend analysis
4. CS-003 (Expansion Identifier) — checks for upsell/cross-sell
5. RI-004 (Churn Predictor) — churn probability
6. RI-002 (Relationship Health Scorer) — relationship temperature check
7. VE-002 (TCO Analyzer) — renewal pricing analysis
8. DS-004 (Price Optimizer) — renewal pricing recommendation
9. RCC-001 creates renewal workflow:
   - Green customer: auto-generate renewal proposal, send to CSM
   - Yellow customer: generate intervention plan, alert CSM
   - Red customer: executive escalation, generate save plan
```

### 4.3 Cross-Division Coordination

Agents from different divisions coordinate through shared events and KV state without direct coupling:

**Deal Strategy consults Buyer Psychology:**
```
DS-001 (Deal Planner) reads BP-001 (Cognitive Bias Detector) output from KV
DS-001 reads BP-002 (Buyer Personality Profile) to tailor strategy
DS-001 publishes: revenueos.deal.{id}.strategy_incorporating_psych
```

**Value Engineering feeds Content:**
```
VE-001 (ROI Model) → VE-003 (Business Case) → stored in KV
CT-002 (Proposal Generator) reads ROI and business case from KV
CT-002 includes ROI summary and business case in proposal
```

**Account Intelligence feeds ABM:**
```
AI-001 (Account Firmographic Tracker) detects company merger
Publishes: revenueos.account.{id}.firmographic_change
ABM-001 (Account Selection) updates account tier based on new firmographics
ABM-002 (Campaign Designer) creates new campaign for merged entity
```

**Customer Success signals to Relationship Intelligence:**
```
CS-001 (Health Scorer) detects health score drop from 85 to 45
Publishes: revenueos.account.{id}.health_degraded
RI-002 (Relationship Health Scorer) recalculates relationship scores
RI-001 (Stakeholder Mapper) checks if champion still engaged
RI-004 (Churn Predictor) recalculates churn probability with new data
RCC-005 (Escalation Manager) creates risk alert if churn > 60%
```

**Coordination pattern:**
```
Agent A publishes event → Agent B subscribes → Agent B reads KV state written by A → Agent B publishes result → Agent A (or C) reads B's output
```

There is no direct agent-to-agent RPC except via NATS request-reply (used only when synchronous response is required). All durable coordination happens through KV state.

---

## 5. State Management

### 5.1 NATS KV Buckets

RevenueOS uses NATS KV buckets as the primary state store for in-flight deal state. Buckets are scoped by entity type:

| Bucket | Retention | Replicas | Description |
|--------|-----------|----------|-------------|
| `deals` | 90 days | 3 | Per-deal state: metadata, scoring, approvals, conversation log |
| `accounts` | 365 days | 3 | Per-account state: firmographics, relationship map, health scores |
| `contacts` | 365 days | 3 | Per-contact state: profile, personality, communication history |
| `system_registry` | Infinite | 3 | Agent registration data, heartbeat state |
| `templates` | Infinite | 3 | Message templates, proposal templates, presentation slides |
| `playbooks` | Infinite | 3 | Sales playbooks, objection responses, competitive battle cards |
| `training` | Infinite | 3 | Agent training corpus (reference RAG data) |

### 5.2 Per-Deal KV Structure

```
Bucket: deals
  ├── metadata.{deal_id}
  │     Basic deal info: amount, product, region, rep, stage, created_at
  │     Permissions: READ — all agents; WRITE — RCC-001, SDR agents
  │
  ├── conversation.{deal_id}
  │     Accumulated conversation log (meeting summaries, email excerpts)
  │     Appended by every agent that processes deal interactions
  │     Permissions: READ — all agents; WRITE — MO* agents, RI-005
  │
  ├── scoring.{deal_id}
  │     BANT scores, MEDDPICC scores, deal quality index
  │     Permissions: READ — QL*, DS*, RO*; WRITE — QL-001, QL-004, QL-005, QL-006
  │
  ├── psych.{deal_id}
  │     Buyer personality profiles, cognitive bias assessments
  │     Permissions: READ — BP*, DS*, NG*; WRITE — BP-001, BP-002, BP-004
  │
  ├── discovery.{deal_id}
  │     Root cause diagnosis, gap analysis, stakeholder map, needs hierarchy
  │     Permissions: READ — DC*, VE*, DS*, CT*; WRITE — DC-001 through DC-006
  │
  ├── value.{deal_id}
  │     ROI model, TCO, business case, competitive comparison
  │     Permissions: READ — VE*, CT*, DS*, NG*; WRITE — VE-001 through VE-006
  │
  ├── strategy.{deal_id}
  │     Deal plan, competitive strategy, pricing recommendation
  │     Permissions: READ — DS*, NG*, PL*, RCC-001; WRITE — DS-001, DS-002, DS-004
  │
  ├── approvals.{deal_id}
  │     Approval requests, decisions, escalation chain
  │     Permissions: READ — RCC-001, RCC-002, DS-005; WRITE — RCC-002, humans
  │
  ├── docs.{deal_id}
  │     Proposal drafts, contracts, presentations
  │     Permissions: READ — CT*, PL*, NG*, SC*; WRITE — CT-*, NG-006, PL-*
  │
  ├── negotiation.{deal_id}
  │     BATNA, concession plan, redlines, leverage inventory
  │     Permissions: READ — NG*, DS*, RCC-001; WRITE — NG-001 through NG-006
  │
  ├── relationship.{deal_id}
  │     Relationship map, health trajectory, communication patterns
  │     Permissions: READ — RI*, CS*, DS*; WRITE — RI-001 through RI-005
  │
  └── audit.{deal_id}
        Immutable event log: every agent action on this deal
        Permissions: READ — RCC-*, Security, SC-004; WRITE — every agent (append only)
```

### 5.3 Event Sourcing for Audit Trail

Every agent action generates an immutable audit event stored in `deals.audit.{deal_id}`:

```json
{
  "event_id": "evt_abc123",
  "timestamp": "2026-06-24T14:30:00Z",
  "deal_id": "1047",
  "agent_id": "ql-001",
  "action": "scored",
  "input": { /* event that triggered this agent */ },
  "output": { /* structured output of the agent */ },
  "llm_tier": "complex",
  "tokens_used": 4840,
  "latency_ms": 3400,
  "decision_confidence": 0.87,
  "kv_reads": ["deals.metadata.1047", "deals.conversation.1047"],
  "kv_writes": ["deals.scoring.1047"]
}
```

**Purpose:**
- Full deal history replayable from any point
- Audit trail for SOX, SOC2, and internal compliance
- Root cause analysis for deal failures
- Training data for agent improvement (which decisions were correct)

**KV retention:** NATS KV is configured with 90-day history per key. This means any key can be read at any previous version within 90 days. Combined with the audit event log, the complete state evolution of every deal is reconstructable.

### 5.4 State Recovery on Agent Crash

When an agent crashes mid-processing:

1. **NATS redelivery:** The unacknowledged message is redelivered to another consumer in the same queue group (or the same consumer if it restarts).
2. **Idempotency check:** Before processing, every agent checks `deals.audit.{deal_id}` for an event with matching `input_event_id`. If found, the agent skips processing (output was already published).
3. **Recovery window:** If a consumer group has no healthy members for 60 seconds, the Escalation Manager (RCC-005) creates a recovery alert.
4. **State consistency:** KV writes are atomic per key. Partial writes from a crashed agent are invisible until the agent's full output is written. The agent's output is a single KV write operation, not a sequence of writes.
5. **Compensation transactions:** For multi-step agent operations (e.g., Proposal Generator that creates content, stores in KV, then publishes event), the agent uses a two-phase pattern:
   - Phase 1: Write intermediate results to a `{key}.tmp` key
   - Phase 2: Rename `.tmp` to final key (NATS KV rename is atomic)
   - On crash between Phase 1 and 2: `.tmp` keys are garbage-collected by a periodic sweep

---

## 6. Human-in-the-Loop Design

### 6.1 Where Humans Intervene

| Trigger | Human Role | SLA | Typical Volume |
|---------|-----------|-----|----------------|
| Deal value > $50K | Manager approves progression | 24h | ~50/month |
| Deal value > $250K | VP Sales approves | 4h | ~10/month |
| Discount > 15% | Deal Desk approves | 4h | ~30/month |
| Non-standard legal terms | Legal reviews | 48h | ~20/month |
| Security exception | Security reviews | 72h | ~5/month |
| First outreach to C-suite | SDR manager reviews | 1h | ~15/month |
| Agent chain failure (P0) | Ops/Engineering investigates | 30min | ~2/month |
| Disqualification recommended | Manager confirms | 24h | ~40/month |
| Churn risk > 80% | CSM intervenes | 4h | ~10/month |
| Procurement tactic detected | Sales rep notified | 1h | ~20/month |

### 6.2 Human Inbox Pattern

Every human in the RevenueOS has a personal inbox — a Slack/Teams bot that delivers action items with structured context and decision buttons:

```
[RevenueOS] Approval Required: Discount Exception
─────────────────────────────────────────────────
Deal:      Acme Corp — Enterprise Plan
Value:     $187,500
Requested: 22% discount ($41,250)
Reason:    Competitive pressure — IBM offering 25% off
Rep:       Sarah Chen

Agent Recommendation: Approve with conditions:
  - Reduce to 18% ($33,750)
  - Add 3-year commitment lock
  - Include onboarding services (zero-margin)

✅ Approve as requested
✅ Approve modified (recommended)
❌ Deny
💬 Request more information
─────────────────────────────────────────────────
Response expected within: 24h | Escalates to: VP Sales
```

**Inbox channels:**
- Slack/Teams bot (primary)
- Email digest (daily summary of pending items)
- Web dashboard (full view of all pending approvals)

### 6.3 SLA Tiers & Escalation

| Tier | Response SLA | Escalation Path |
|------|-------------|-----------------|
| **Urgent** (P0) | 15 minutes | Human → Manager → Director → VP → automated fallback |
| **High** (P1) | 1 hour | Human → Manager → VP |
| **Standard** (P2) | 24 hours | Human → Manager |
| **Low** (P3) | 72 hours | Human only |

**Escalation behavior:**
1. Human receives notification with SLA clock
2. At 50% of SLA → reminder sent
3. At 100% of SLA (no response) → escalated to next level
4. Escalation includes: original request, why it was escalated, time since first notification
5. At final escalation level (VP/Director) with no response → automated fallback action:
   - Approval: auto-approved with conditions (conservative default)
   - Denial: auto-denied with explanation
   - This is configurable per approval type

### 6.4 Pause/Resume Protocol

When a human gate is triggered, the deal enters a **paused** state:

```
States: ACTIVE → PAUSED (human gate) → ACTIVE (resolved) | BLOCKED (denied)

PAUSED state:
  - All agents for this deal stop processing new events
  - Timer starts: if paused > SLA, escalate
  - Human can request "partial resume" for non-blocked agents
  - Deal shows as "Pending: human action required" on dashboard

RESUME:
  - Human approves/denies → event published → deal transitions
  - If approved: paused agents resume with fresh state
  - If denied: deal moves to BLOCKED (or salvaged via alternative path)

BLOCKED state:
  - Deal cannot progress through standard path
  - RCC-005 creates alternative path recommendation
  - Human can override block and force-advance deal
  - After 30 days in BLOCKED: auto-move to closed-lost
```

---

## 7. Security Architecture

### 7.1 MVP Authentication: NATS JWTs

**MVP Authentication: NATS JWTs** — For Phase 0-2, use NATS built-in JWT authentication. Each agent gets a JWT signed by the NATS operator key, scoped to its declared subjects and KV permissions. JWTs have 24-hour expiry with auto-refresh via a sidecar. **Upgrade to mTLS with SPIFFE identities targeted for Phase 4** when agent count exceeds 50 and cross-cluster communication is required.

Every agent connects to NATS with a signed JWT:

```
Account: revenueos
Agent JWT claims:
  - sub: agent.{division}.{agent_id}.{instance_id}
  - iss: RevenueOS Operator
  - exp: 24 hours
  - nats_permissions:
      publish: [subjects permitted]
      subscribe: [subjects permitted]
      kv_read: [bucket/key patterns]
      kv_write: [bucket/key patterns]
```

The NATS operator JWT encodes these permissions directly:
- **Subjects permitted:** Which publish/subscribe patterns the agent can use
- **KV permissions:** Which bucket/key patterns the agent can read/write
- **Max message size:** Per-agent limit (default 1MB, MO-001 can send up to 10MB for audio chunks)

JWT rotation is handled by a sidecar container that refreshes the token before expiry. No PKI infrastructure, no certificate revocation lists, no HSM dependency during MVP.

### 7.2 Data Classification Tiers

| Tier | Definition | Examples | Access | At Rest | In Transit |
|------|-----------|---------|--------|---------|------------|
| **Public** | No business impact | Product names, company blog posts, case studies | No auth | None | TLS |
| **Internal** | Low business impact | Sales playbooks, email templates, ROI methodology | All agents | AES-256 | TLS 1.3 |
| **Confidential** | Moderate business impact | Deal metadata, qualification scores, meeting transcripts | Deal-authorized agents only | AES-256 | TLS 1.3 |
| **Restricted** | High business impact | Pricing data, legal terms, negotiation strategy, personal data | Named agents + specific KV key access | AES-256 + field-level encryption | TLS 1.3 |

**Restricted data handling:**
- Field-level encryption for sensitive fields (PII, pricing, negotiation positions)
- Encryption keys stored in Vault, accessed by agents at startup
- Agents receive decrypted data only within their authenticated session
- No restricted data is logged to Loki or included in traces

### 7.3 Audit Logging

Every agent action produces an audit event (see Section 5.3). The audit log is:
- **Immutable:** Written to NATS KV with `history` = infinite and `storage` = file (not memory)
- **Tamper-evident:** Event sequence includes a hash chain (each event includes the hash of the previous event in the deal's audit log)
- **Captures:** agent_id, action, input event, output, KV reads/writes, LLM tokens, latency
- **Retention:** 7 years (for SOC2/SOX compliance)
- **Access:** Read-only for most agents. Only SC-004 (Security Audit Agent) and the Security team have write-access to query but not modify.

### 7.4 Prompt Injection Defenses

All agents handling external content (meeting transcripts, email replies, web content) implement:

1. **Input sanitization:** Strip control characters, normalize Unicode, truncate to max length per agent (defined in agent spec)
2. **Instruction boundary enforcement:** System prompt is separated from user input by a cryptographic boundary — the LLM API call wraps the system prompt in a protected block that the user input cannot reference
3. **Suspicious pattern detection:** Detect and log potential injection attempts (e.g., "ignore previous instructions", "system prompt:", "you are now", "'''")
4. **Rate limit per source:** Max LLM calls per source per minute (prevents injection brute force)
5. **Output validation:** Every agent validates that its structured output conforms to the expected schema before publishing. Malformed output (potential injection result) is discarded and logged.

**Specifically at-risk agents (with enhanced defenses):**
- MO-001 through MO-006 (process external meeting audio/transcripts)
- SDR-003 and SDR-004 (process email replies from prospects)
- KL-005 (may encounter malicious content in scraped training data)
- PL-001 and PL-002 (process legal documents from counterparties)
- NG-003 and NG-006 (process procurement and contract content from buyer)

### 7.5 Output Validation Gates

Every agent output is validated before publication:

**Schema validation:** Every published event must conform to its protobuf schema. Rejected if:
- Missing required fields
- Field type mismatches
- String length exceeds limits
- Numeric values out of range

**Content validation (high-risk agents):**
- **CT agents (content generation):** Output scanned for:
  - Hallucinated facts (company names, revenue figures, product capabilities)
  - Competitor disparagement (legal risk)
  - Over-commitment (promising features that do not exist)
  - Brand voice violations
- **NG agents (negotiation):** Output scanned for:
  - Concessions above authority limits
  - Commitments not in approved terms
  - Legal risk language
- **PL agents (legal):** Output paired with counter-validation by a separate PL agent (adversarial pair)

**Adversarial agent pairs (Santa Method):**
For critical outputs (proposals, contracts, pricing), two independent agents process:
1. **Generator agent** produces the output
2. **Validator agent** (same spec, different LLM session) reviews the output
3. If validator flags issues, a human reviews both outputs and resolves
4. If validator approves, output proceeds

---

## 8. Training & Knowledge Pipeline

### 8.1 Agent Training Corpus

Each agent is trained on a domain-specific corpus. The full corpus is defined in `REVENUE_OS_TRAINING_MATERIALS.md`. At a high level:

| Domain | Corpus Sources | Update Frequency |
|--------|---------------|------------------|
| Qualification | MEDDIC framework, BANT, Command of the Message, SPICED | Quarterly |
| Buyer Psychology | Kahneman, Cialdini, Thaler, Ariely, Kahneman & Tversky | Semi-annual |
| Value Engineering | Forrester TEI, Gartner TCO, Bain ROI methodology | Quarterly |
| Negotiation | Harvard Negotiation Project, Getting to Yes, 3D Negotiation | Semi-annual |
| Competitive Intel | Battle cards, win/loss reports, Gartner MQ, G2 reviews | Continuous |
| Sales Methodology | Challenger Sale, SPIN Selling, Strategic Selling, MEDDIC | Quarterly |
| Customer Success | Gainsight methodology, PLG frameworks, adoption analytics | Semi-annual |
| Legal/Procurement | IACCM standards, ASC 606, SaaS MSA precedents | Semi-annual |

### 8.2 Win/Loss Feedback Loop

The most critical learning mechanism in RevenueOS:

```
CLOSED DEAL (won or lost)
         │
         ▼
DS-003 (Win/Loss Analyst)
  ├── Analyzes transcripts, emails, scores, pricing
  ├── Identifies root causes: why won / why lost
  └── Publishes: revenueos.system.win_loss_analysis.{deal_id}
         │
         ▼
KL-001 (Pattern Extraction Agent)
  ├── Detects patterns across multiple win/loss analyses
  ├── Identifies: "deals with champion score < 40 lose 80% of the time"
  └── Publishes: revenueos.system.pattern_extracted.{pattern_id}
         │
         ▼
KL-004 (Playbook Updater)
  ├── Updates qualification playbooks with new patterns
  ├── Updates objection response playbooks
  └── Publishes: revenueos.system.playbook_updated.{playbook_id}
         │
         ▼
KL-005 (Agent Training Agent)
  ├── Generates updated training examples for affected agents
  ├── Each example: (input, correct_output, reasoning)
  └── Publishes: revenueos.system.training_examples_ready
         │
         ▼
RCC-001 (Revenue Orchestrator)
  └── Triggers agent retraining cycle:
       - QL-001: updated qualification rubrics
       - MO-003: updated objection classification examples
       - NG-001: updated BATNA assessment patterns
       - DS-001: updated deal plan templates
       - All affected agents reload their system prompts
```

**Retraining cadence:**
- **Hot fix:** Critical pattern discovered → agent system prompt updated within 1 hour (via ConfigMap reload)
- **Daily:** Aggregated pattern updates applied to active agents (rolling restart)
- **Weekly:** Full training corpus re-indexed for RAG agents
- **Monthly:** Agent performance evaluated against held-out test set; underperformers retrained

### 8.3 RAG Pipeline

**RAG Scope (Qdrant/pgvector):** RAG is used exclusively for:
1. **Knowledge retrieval** — playbooks, case studies, competitive intelligence, pricing guidelines — indexed by deal attributes (industry, deal size, product, competitor)
2. **Training material retrieval** — methodology frameworks (MEDDPICC, SPIN, etc.) — indexed by agent role + query type
3. **Historical deal patterns** — anonymized win/loss data — indexed by segment + deal attributes
NOT used for: real-time conversation context (that's NATS KV), CRM data (that's direct API calls), or agent-to-agent communication (that's NATS events)

For agents that require real-time knowledge retrieval (KL-001, CT-003, CT-004, MO-003, SDR-005, RFP agents):

```
Knowledge Sources:
  ├── Internal: playbooks, battle cards, case studies, product docs
  ├── CRM: historical deals, win/loss records, account data
  ├── External: competitive intel, analyst reports, news feeds
  └── Training: corpus documents, annotated examples

Pipeline:
  1. Document ingestion → chunking (512 tokens, 128 token overlap)
  2. Embedding generation (text-embedding-3-large: 3072 dimensions)
  3. Vector storage (pgvector on PostgreSQL)
  4. Retrieval at query time:
     a. Query embedding
     b. Hybrid search (vector similarity + BM25 keyword)
     c. Rerank top 20 candidates with Cross-Encoder
     d. Return top 5 chunks as context

RAG Caching:
  - Query result cached in Redis for 24h (TTL)
  - Cache key: hash(agent_id + query + deal_context_fingerprint)
  - For same deal, cache is invalidated when new playbooks/updates arrive
```

### 8.4 Web & Social Training Ingestion

RevenueOS agents learn not only from books and frameworks but from continuous ingestion of real-world sales content: expert videos, thought leader blogs, social media posts, Gong research, and podcast transcripts. This keeps agents current with evolving sales methodologies and market dynamics.

#### 8.4.1 Ingestion Pipeline

```
Web Content Sources
  ├── YouTube: Gong Labs, Chris Voss, Anthony Iannarino, Josh Braun, John Barrows, Matt Easton, Sales Insights Lab
  ├── LinkedIn: Gong Labs research, Matt Dixon, Kurtis Hanni, Chris Voss, Anthony Iannarino, John Barrows, Tim Williams, Jason Lemkin
  ├── Blogs: Gong Labs blog, SalesHacker, LinkedIn Sales Blog, SaaStr, Crayon (competitive intel), Close.com, Lavender, Mailshake
  ├── Twitter/X: @gong_io, @thesalesblog, @chrisvoss, @sachinrekhi, @kavi_h, @jiakarl
  ├── Podcasts: 30 Minutes to President's Club, Sales Pipeline Radio, Revenue Builders, The Why Sales Podcast
  └── Gong Labs Research: Conversation science, cold email analysis, multi-threading data, executive engagement patterns

Pipeline Steps:
  1. COLLECT: agent-reach tool scrapes YouTube transcripts, blog posts, LinkedIn articles, Twitter threads
  2. EXTRACT: Content is cleaned, deduplicated, and structured (title, author, date, key insights, source URL)
  3. CLASSIFY: Content is tagged by:
     - Agent type (QL, MO, BP, VE, NG, DS, etc.)
     - Skill domain (qualification, negotiation, discovery, value engineering)
     - Thought leader (Voss, Dixon, Iannarino, Blount, etc.)
     - Methodology (MEDDPICC, SPIN, Challenger, Gap Selling)
  4. INDEX: Classified content is vectorized and stored in the RAG corpus (pgvector)
  5. DISTRIBUTE: RAG agents reference tagged content on relevant queries; full training corpus updated weekly

#### 8.4.2 Source Classification by Agent Division

| Division | Priority Web Sources | Refresh |
|----------|--------------------|---------|
| Meeting Observer | Gong Labs conversation research, Gong YouTube channel | Weekly |
| Buyer Psychology | Predictably Irrational blog, Chris Voss YouTube, Beyond Reason articles | Bi-weekly |
| Value Engineering | Forrester/Blog ROI content, ValueSelling blog | Weekly |
| Negotiation | Chris Voss YouTube, Never Split the Difference interviews, Getting to Yes blog | Bi-weekly |
| SDR/Prospecting | Josh Braun YouTube, Matt Easton YouTube, Close.com blog, Mailshake blog, Lavender blog | Daily |
| Deal Strategy | Anthony Iannarino blog, SalesHacker, SaaStr, Gong win/loss research | Weekly |
| Executive Advisory | John Barrows YouTube, Strategic Selling blog, CEB content | Bi-weekly |
| Competitive Intel | Crayon blog, Klue blog, Gartner analyst blogs | Daily |
| Customer Success | Gainsight blog, SuccessHacker, ChurnZero blog | Weekly |

#### 8.4.3 Content Quality Gates

All ingested content passes through automated quality control:
- **Relevance scoring:** Must match at least 1 agent division's domain tags (score >0.6)
- **Authority weighting:** Content from certified thought leaders (Voss, Dixon, Iannarino, Blount) gets priority indexing
- **Date freshness:** Content older than 2 years is deprioritized unless it's a foundational methodology
- **Duplication:** Fuzzy dedup (cosine similarity >0.9 → discard duplicate)
- **Controversy flagging:** If ingested content contradicts existing training corpus, flag for human review

#### 8.4.4 Agent-Specific Web Training Targets

Each agent's Training Corpus (defined in AGENT_SPECS.md) includes specific web source URLs and channels. For example:
- MO-003 (Objection Detector): Gong Labs objection taxonomy research, Challenger Sale teaching video transcripts
- SDR-001 (Multi-Channel Prospector): Josh Braun YouTube cadence design videos, Close.com blog outreach best practices
- NG-001 (BATNA Analyzer): Chris Voss YouTube tactical empathy examples, Never Split the Difference podcast interviews
- CT-001 (Proposal Generator): Marketing examples blog, Command of the Message LinkedIn case studies

The full mapping of web sources to agents is maintained in REVENUE_OS_TRAINING_MATERIALS.md Part 6.

---

## 9. Scaling & Performance

### 9.1 HPA Configuration

Each division has an HPA configured based on NATS queue depth (custom metrics adapter reading NATS monitoring endpoint):

```yaml
# Example: QL Division HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: qualification-team
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: qualification-team
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: nats_queue_depth
          selector:
            matchLabels:
              queue: "qualification-scorers"
        target:
          type: AverageValue
          averageValue: 25
```

### 9.2 Estimated Throughput

| Metric | Value | Calculation |
|--------|-------|-------------|
| Deals/month | 1,000 | Target steady state |
| Events per deal | ~500 | ~100 agent executions × ~5 events each |
| Events/month | 500,000 | 1,000 × 500 |
| Events/day | ~16,667 | 500,000 / 30 |
| Peak events/hour | ~2,500 | 3× daily average burst |
| Peak events/second | ~42 | 2,500 / 60 (sustained burst) |
| NATS message size (avg) | ~4KB | Protobuf serialized |
| NATS throughput (peak) | ~168 KB/s | 42 × 4KB (trivial for NATS) |
| KV operations/day | ~100,000 | ~6 reads + ~2 writes per agent per deal |

**NATS capacity check:** A 3-node NATS cluster handles 10M+ messages/second. RevenueOS at 42 msg/s peak is ~0.0004% of NATS capacity. The bottleneck is LLM API latency, not message throughput.

### 9.3 LLM Token Budget Estimates

| Phase | Agents | Tokens per Deal | LLM Tier Split | Estimated Cost per Deal |
|-------|--------|----------------|----------------|------------------------|
| Prospecting | SDR-001–005, AI-001–004 | ~15K input, ~3K output | 70% Sonnet, 20% Haiku, 10% Opus | $0.45 |
| Meeting | MO-001–006, BP-001–005 | ~50K input, ~8K output | 60% Sonnet, 30% Haiku, 10% Opus | $1.20 |
| Qualification | QL-001–006 | ~20K input, ~4K output | 40% Sonnet, 40% Haiku, 20% Opus | $0.65 |
| Discovery | DC-001–006 | ~30K input, ~6K output | 50% Sonnet, 30% Haiku, 20% Opus | $0.90 |
| Value Engineering | VE-001–006 | ~25K input, ~8K output | 40% Sonnet, 20% Haiku, 40% Opus | $1.50 |
| Deal Strategy | DS-001–005 | ~15K input, ~4K output | 40% Sonnet, 20% Haiku, 40% Opus | $1.10 |
| Content | CT-001–006, BP-003 | ~20K input, ~15K output | 60% Sonnet, 10% Haiku, 30% Opus | $1.80 |
| Negotiation | NG-001–006, BP-001, BP-005 | ~30K input, ~8K output | 40% Sonnet, 20% Haiku, 40% Opus | $1.60 |
| Procurement/Legal | PL-001–004, SC-001–003 | ~25K input, ~10K output | 50% Sonnet, 20% Haiku, 30% Opus | $1.40 |
| Close/Post | CS-001–004, RI-001–005, RO-005 | ~10K input, ~3K output | 60% Sonnet, 30% Haiku, 10% Opus | $0.35 |
| Win/Loss | DS-003, KL-001–006 | ~20K input, ~5K output | 50% Sonnet, 20% Haiku, 30% Opus | $1.00 |

**Total per deal:** ~$12.00
**Monthly at 1,000 deals:** ~$12,000
**With caching optimization (40% reduction):** ~$7,200/month

### 9.4 Caching Strategy

| Cache | Scope | TTL | Hit Rate Target | Storage |
|-------|-------|-----|----------------|---------|
| LLM response cache | Identical prompts | 24h | 30% | Redis (500MB) |
| RAG query results | Same agent + query | 24h | 40% | Redis (1GB) |
| KV reads | Per agent session | Session (max 5min) | 60% | In-memory |
| External API (ZoomInfo, Clearbit) | Account data | 7 days | 70% | Redis (2GB) |
| Embeddings | Pre-computed | 7 days | 90% | PostgreSQL pgvector |
| Templates (email, proposal) | Static | Infinite | 100% | NATS KV |

**LLM response cache key:** `hash(agent_id + model + system_prompt_version + input_hash)`

---

## 10. Cost Model

### 10.1 LLM API Costs

| Model | $/1M Input Tokens | $/1M Output Tokens | Monthly Usage (est.) | Monthly Cost (est.) |
|-------|------------------|-------------------|---------------------|--------------------|
| Claude Opus 4.5 | $15 | $75 | ~20M input, ~4M output | $600 |
| Claude Sonnet 4.5 | $4 | $16 | ~80M input, ~18M output | $608 |
| Claude Haiku 3.5 | $1 | $5 | ~40M input, ~8M output | $80 |
| GPT-4o (fallback) | $5 | $15 | ~5M input, ~1M output | $40 |
| GPT-4o-mini (fallback) | $0.15 | $0.60 | ~10M input, ~2M output | $3 |
| Embeddings (text-embedding-3-large) | $0.13 | — | ~50M tokens | $6.50 |

**Total LLM cost at full scale:** ~$1,337/month (well within the $3K-$7.5K estimate from the executive summary, even with a 2-3x safety margin).

**Cost tracking:** Per-agent token counters (see §2.5) feed the cost model. Every agent invocation emits `agent.tokens.prompt`, `agent.tokens.completion`, `agent.tokens.total`, and `agent.cost.estimated`. These are aggregated into daily budgets by the Cost Governor (RCC-006) and power the cost breakdowns above. Budget alerts fire when any agent exceeds its daily allowance by 20%.

### 10.2 Infrastructure Costs

| Resource | Spec | Monthly Cost (est.) |
|----------|------|-------------------|
| K8s cluster (DigitalOcean/AWS) | 3 nodes, 8 vCPU, 32GB RAM each | $500 |
| NATS cluster (same nodes) | Included in K8s | $0 |
| PostgreSQL (managed) | 2 vCPU, 8GB, 200GB SSD | $200 |
| Redis (managed) | 2 vCPU, 4GB | $80 |
| S3-compatible storage | 500GB (transcripts, docs, training data) | $30 |
| Observability (Grafana Cloud) | Metrics, logs, traces | $200 |
| Slack/Teams API | Bot messages, interactions | $0 |
| LLM API costs | — | $1,337 |
| External data APIs | ZoomInfo, Clearbit, LinkedIn (est.) | $1,500 |

**Warm Pool Costs: $7,600/month** — This covers always-on replicas for Tier 1 agents (Command Center, Meeting Observer, SDR, Qualification). 8 agents × 2 replicas × $475/replica (CPU-only, 2 vCPU, 4GB RAM). These are NOT included in the base infrastructure estimate and must be budgeted separately. Breakdown:
- Revenue Command Center (RCC-001): 2 pods × $475 = $950/mo
- Meeting Observer (MO-001): 2 pods × $475 = $950/mo (GPU variant: +$2,000/mo)
- SDR (SDR-001/002): 2 pods × $475 = $950/mo
- Qualification (QL-001): 2 pods × $475 = $950/mo
- NATS infrastructure: $1,200/mo (3-node cluster, SSD-backed)
- Observability: $1,600/mo (Tempo + Loki + Grafana, 30-day retention)
- CI/CD + Registry: $1,000/mo

**Total monthly infrastructure:** ~$3,847

### 10.3 Open Source vs SaaS Trade-offs

| Component | Chosen Approach | Alternatives Considered | Rationale |
|-----------|----------------|------------------------|-----------|
| Message bus | NATS (open source) | Kafka, RabbitMQ, Pulsar | NATS: 25MB binary, no JVM, no ZK, simpler ops, sufficient throughput |
| State store | NATS KV + PostgreSQL | Redis only, DynamoDB, etcd | KV for in-flight state, PG for durable queries. Redis alone lacks durability for audit trail |
| Agent framework | Custom (Go + gRPC) | Temporal, LangChain, AutoGen | Custom gives full control over agent lifecycle. Temporal considered but adds ~$500/month running costs |
| LLM orchestration | Custom | LangChain, Semantic Kernel | LangChain introduces abstraction overhead and debugging complexity for 108 agents. Custom is leaner |
| Monitoring | OpenTelemetry → Grafana | Datadog, New Relic, SigNoz | OpenTelemetry is vendor-neutral. Grafana Cloud is free tier for first 10K series. Datadog would be $2K+/month |
| Secrets | Vault (open source) | AWS Secrets Manager, Doppler | Vault is free, provides dynamic secrets, NATS JWT signing key management |
| Vector store | pgvector (PostgreSQL) | Pinecone, Weaviate, Qdrant | One less service to manage. pgvector performs adequately at our scale (~500K vectors) |

**Total monthly at full scale:** ~$3,847 (infra) + $1,500 (data APIs) = ~$5,347
**With warm pool (Tier 1):** ~$5,347 + $7,600 = ~$12,947/month
**With warm pool + LLM costs:** ~$12,947 + $1,337 = ~$14,284/month

---

## 11. Key Design Decisions & Rationale

### 11.1 Why NATS Over Kafka

| Dimension | NATS JetStream | Kafka | Verdict |
|-----------|---------------|-------|---------|
| Binary size | ~25MB (single binary) | ~300MB (broker) + ZK/KRaft + Schema Registry | NATS wins |
| Latency (p99) | ~1ms | ~5ms | NATS wins |
| Throughput at scale | 10M msg/s | 50M msg/s | Kafka wins (but we need ~42 msg/s) |
| Persistence | File-based, configurable | Required for all topics | Preference |
| KV store | Built-in | Requires external (KSQL/Couchbase) | NATS wins |
| Request-reply | Native | Requires proxy layer | NATS wins |
| Queue groups | Native | Consumer groups (more config) | Comparable |
| Ops complexity | Single binary, no JVM | Requires Java, ZK/KRaft, tuning | NATS wins |
| Schema registry | Not built-in (use protobuf) | Schema Registry built-in | Kafka wins (but protobuf works) |
| Exactly-once | Yes (JetStream) | Yes (transactional) | Comparable |

**Decision:** NATS JetStream. Our throughput needs (42 msg/s peak) are 0.0004% of Kafka's capacity. NATS provides KV store, request-reply, and queue groups in a single ~25MB binary. Kafka would add JVM dependency, ZK/KRaft cluster, Schema Registry, and significantly higher operational overhead for zero benefit at our scale. If throughput grows 1000× (to 42K msg/s), we can swap NATS for Kafka at the subject adapter layer without changing agent code.

### 11.2 Why Event-Driven Over Request-Driven

**Request-driven (REST/gRPC microservices):**
- Agent A calls Agent B's API
- Agent B must be available and responsive
- Failure propagation: if Agent B is down, Agent A fails
- Tight coupling: Agent A must know Agent B's endpoint and schema
- Scaling: each agent must handle its own load + incoming requests

**Event-driven (NATS pub/sub):**
- Agent A publishes event → zero or more agents consume
- Agents can be offline: NATS retains messages (JetStream)
- Loose coupling: Agent A does not know who consumes its events
- Scaling: each agent consumes from its queue at its own rate
- Adding new agents: subscribe to existing events, no changes to publishers

**Decision:** Event-driven. For 108 agents, the coupling of request-driven would create a dependency graph with ~5,000+ potential interactions. Event-driven reduces this to ~500 well-defined event types. Agents come and go independently. NATS handles buffering, redelivery, and queue groups.

### 11.3 Why Need-to-Know Projections Over Shared State

**Shared state approach:** All agents read/write to a shared deal object. Problems:
- Race conditions: two agents write to the same field
- Implicit coupling: Agent A changes a field Agent B depends on
- Security: any agent can read any data
- Audit: hard to trace who changed what

**Need-to-know projections (our approach):**
- Each agent has explicit read and write perms on specific KV sub-keys
- State is scoped: `scoring.{deal_id}`, `psych.{deal_id}`, `discovery.{deal_id}`
- Agents read only what they need
- Writes are scoped to the agent's domain
- Security is enforced at the NATS level (auth callout)

**Decision:** Need-to-know projections. The cost is more KV keys and explicit permission management. The benefit is security, auditability, and parallel-safe writes. At 108 agents with different data domains, shared state would be unmanageable.

### 11.4 Why Same-Image Deployment Over Per-Agent Services

**Per-agent services:** 108 Docker images, 108 Dockerfiles, 108 deployments. Problems:
- Build time: 108 builds on every change
- Version drift: agents can be on different base images
- CI/CD complexity: 108 pipelines or one pipeline with 108 steps
- Image size: each image duplicates base dependencies
- Testing: must test all 108 images independently

**Same-image (our approach):** One Docker image with 108 entrypoints. Problems:
- Image size: larger (~400MB) because it contains all agent code
- Security blast radius: vulnerability in one agent's dependency affects all

**Decision:** Same-image single deployment. The benefits of unified build, versioning, and CI/CD outweigh the larger image size. Security is mitigated by per-entrypoint permissions (NATS JWT scope, KV auth). Agent code is isolated at the process level, not the container level. Kubernetes ensures agents do not interfere.

### 11.5 Why OpenTelemetry Over Proprietary Tracing

- **OpenTelemetry:** Vendor-neutral, open standard. Can export to Tempo, Jaeger, Zipkin, Datadog, New Relic, etc.
- **Proprietary:** Vendor lock-in. Changing vendors requires re-instrumenting all 108 agents.
- **Cost:** OpenTelemetry is free. Datadog APM would be ~$2,000+/month for 108 agents.
- **Coverage:** OpenTelemetry covers traces, metrics, and logs (three pillars).
- **Integration:** OpenTelemetry automatically instruments gRPC, NATS client, HTTP client, PostgreSQL driver.

**Decision:** OpenTelemetry. No vendor lock-in, lower cost, comprehensive coverage. The initial setup cost (instrumenting 108 agents) is a one-time investment that pays back on every vendor negotiation.

### 11.6 Why LLM Tiering Per Agent

Every agent specifies its LLM tier (Haiku/Sonnet/Opus) in its spec. This is not a suggestion — it is enforced by the Capacity Governor (RCC-006):

| Agent Type | Tier | Why Not Lower? | Why Not Higher? |
|-----------|------|----------------|----------------|
| RCC-001 (Orchestrator) | Opus | Route decisions affect all downstream agents; a single wrong routing loses a deal | NA — this is the ceiling |
| QL-001 (Scorer) | Opus | Scoring requires evaluating evidence quality, not pattern matching | Sonnet misses nuanced disqualification signals (~15% error rate vs ~5% for Opus) |
| MO-006 (Talk Ratio) | Haiku | Simple quantitative computation | Opus would be $15× more expensive for same result |
| CT-002 (Proposal) | Opus | Proposal is highest-stakes document; errors here lose deals | Sonnet produces lower-quality proposals (test results: 78% acceptance vs 92% for Opus) |
| RO-005 (Commission) | Haiku | Rule-based arithmetic | Opus would be 75× more expensive for identical output |
| BP-001 (Bias Detector) | Opus | Requires nuanced psychological reasoning | Sonnet misses ~40% of cognitive bias indicators |

**Decision:** Explicit LLM tiering. The 50× cost difference between Haiku and Opus means tire-to-tier savings are significant. Tiering is embedded in the agent contract and enforced at runtime. The Capacity Governor (RCC-006) monitors and alerts if an agent uses an unnecessarily expensive model.

---

## 12. Appendices

### Appendix A: Division-to-Division Interaction Matrix

This matrix shows which divisions produce events consumed by other divisions. Read: "Row produces → Column consumes."

```
               ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
               │R│M│S│Q│B│V│D│C│D│N│R│R│C│A│P│E│P│S│D│R│K│A│A│S│C│D│S│
               │C│O│D│L│P│E│C│T│S│G│I│O│S│B│L│A│A│C│L│F│L│G│I│P│V│S│P│
               │C│ │R│ │ │ │ │ │ │ │ │ │ │M│ │ │ │ │C│P│ │ │ │R│ │V│ │
               │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
┌──────────────┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│RCC - Command │→│ │→│→│ │ │→│→│→│ │→│→│→│→│→│→│→│→│→│ │→│→│→│→│ │→│ │
│MO  - Meeting │→│→│→│→│→│ │→│ │ │ │ │ │→│ │ │ │ │ │ │ │ │→│ │ │ │ │ │
│SDR - Prosp.  │→│ │→│→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │
│QL  - Qualif. │→│ │ │→│ │ │→│ │→│ │→│→│ │ │ │ │ │ │ │ │→│→│ │ │ │ │ │
│BP  - Psych   │→│ │ │→│→│ │→│→│→│→│→│ │→│ │ │ │ │ │ │ │ │→│ │ │ │ │ │
│VE  - Value   │→│ │ │ │→│→│ │→│→│ │ │ │→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│DC  - Discov. │→│ │ │→│→│→│→│→│→│ │ │ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │
│CT  - Content │→│ │ │ │→│ │ │→│ │ │ │ │→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│DS  - Strategy│→│ │ │→│→│→│ │→│→│→│→│→│ │→│→│ │→│ │→│ │→│→│ │ │ │ │
│NG  - Negot.  │→│ │ │ │→│ │ │→│→│→│→│ │→│→│ │ │ │ │ │ │→│ │ │ │ │ │
│RI  - Relat.  │→│ │ │ │ │ │ │ │ │ │→│→│→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│RO  - RevOps  │→│ │ │→│ │ │ │ │→│ │ │→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│CS  - Cust.S  │→│ │ │ │ │ │ │ │ │ │→│ │→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │
│ABM - ABM     │→│ │→│ │→│ │ │→│→│ │→│→│ │→│ │ │ │ │ │ │ │→│ │ │ │ │ │
│PL  - Proc/Lgl│→│ │ │ │ │ │ │ │→│→│ │ │ │ │→│ │ │ │ │ │ │ │ │ │ │ │ │
│EA  - Exec    │→│ │ │ │→│ │→│ │→│ │ │ │ │ │ │→│ │ │ │ │ │ │ │ │ │ │ │
│PA  - Partner │→│ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │ │ │ │
│SC  - Security│→│ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │→│ │ │→│→│ │ │ │ │
│DLC - Delivery│→│ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │
│RFP - RFP/RFQ │→│ │ │ │ │ │ │→│→│ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │ │
│KL  - Knowldg │→│ │ │→│→│ │ │→│→│ │ │→│ │ │→│ │ │ │ │ │→│→│ │ │ │ │
│AG  - AI Gov  │→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │
│AI  - Account │→│ │→│→│ │ │ │→│→│ │→│→│→│→│ │ │ │ │ │ │→│ │→│ │ │ │
│SPR - SalesPsy│→│ │ │→│→│ │ │ │→│→│ │ │ │ │ │ │ │ │ │ │→│ │ │→│ │ │
│CV  - CustVoc │→│ │ │ │ │ │ │ │ │ │→│ │→│ │ │ │ │ │ │ │ │ │ │ │→│ │
│DSV - DataSvcs│→│ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │ │ │ │ │ │ │→│
│SP  - Sec/Priv│→│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │→│ │ │ │ │ │ │ │ │→
└──────────────┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

### Appendix B: Event Subject Naming Convention

**Format:** `revenueos.{domain}.{entity}.{action}.{scope}`

| Segment | Values | Description |
|---------|--------|-------------|
| `domain` | `deal`, `account`, `contact`, `meeting`, `system`, `alert`, `rpc` | Top-level domain |
| `entity` | `{deal_id}`, `{account_id}`, `{meeting_id}`, `agent`, `config` | The entity the event pertains to |
| `action` | Past-tense verb | What happened |
| `scope` | `{agent_id}`, `{queue_group}`, optional | Scoping for RPC or queue routing |

**Examples:**
```
revenueos.deal.{id}.created
revenueos.deal.{id}.stage_changed
revenueos.deal.{id}.scored
revenueos.deal.{id}.human_gate_required
revenueos.meeting.{id}.scheduled
revenueos.meeting.{id}.transcript_chunk
revenueos.meeting.{id}.completed
revenueos.account.{id}.firmographic_changed
revenueos.account.{id}.health_degraded
revenueos.contact.{id}.profile_updated
revenueos.system.agent.{id}.heartbeat
revenueos.system.agent.{id}.registration
revenueos.system.config.updated
revenueos.alert.{severity}.{category}
revenueos.rpc.{agent_id}.{method}.{scope}
revenueos.dlq.{original_subject}
```

**Subject wildcard rules:**
- `revenueos.deal.*.scored` — all deals, scored event
- `revenueos.deal.1047.*` — all events for deal 1047
- `revenueos.>.heartbeat` — all heartbeat events (any entity)
- `revenueos.system.*.*` — all system events

### Appendix C: Agent Registry Summary

| ID | Division | Tier | LLM Tier | Criticality | Primary Function |
|----|----------|------|----------|-------------|-----------------|
| RCC-001 | Revenue Command Center | 1 | Opus | P0 | Revenue Orchestrator |
| RCC-002 | Revenue Command Center | 1 | Sonnet | P0 | Human-in-the-Loop Gatekeeper |
| RCC-003 | Revenue Command Center | 1 | Haiku | P1 | Performance Dashboard Agent |
| RCC-004 | Revenue Command Center | 1 | Opus | P2 | A/B Testing Coordinator |
| RCC-005 | Revenue Command Center | 1 | Opus | P0 | Escalation Manager |
| RCC-006 | Revenue Command Center | 1 | Haiku | P1 | Capacity and Cost Governor |
| MO-001 | Meeting Observer | 1 | Haiku | P0 | Real-Time Transcription |
| MO-002 | Meeting Observer | 1 | Sonnet | P1 | Sentiment and Emotion Analyst |
| MO-003 | Meeting Observer | 1 | Sonnet | P0 | Objection Detector |
| MO-004 | Meeting Observer | 1 | Sonnet | P0 | Commitment Tracker |
| MO-005 | Meeting Observer | 1 | Sonnet | P1 | Question Quality Scorer |
| MO-006 | Meeting Observer | 1 | Haiku | P2 | Talk Ratio Analyst |
| SDR-001 | SDR Team | 1 | Sonnet | P0 | Multi-Channel Prospector |
| SDR-002 | SDR Team | 1 | Sonnet | P1 | Intent Signal Monitor |
| SDR-003 | SDR Team | 1 | Sonnet | P0 | Personalized Outreach Generator |
| SDR-004 | SDR Team | 1 | Sonnet | P0 | Follow-Up Sequencing Engine |
| SDR-005 | SDR Team | 1 | Sonnet | P1 | Account Researcher |
| QL-001 | Qualification Team | 1 | Opus | P0 | BANT/MEDDPICC Scorer |
| QL-002 | Qualification Team | 1 | Haiku | P0 | Deal Inspector |
| QL-003 | Qualification Team | 1 | Opus | P1 | Disqualification Engine |
| QL-004 | Qualification Team | 1 | Opus | P0 | Champion Validator |
| QL-005 | Qualification Team | 1 | Sonnet | P0 | Budget Verification Agent |
| QL-006 | Qualification Team | 1 | Sonnet | P1 | Timeline Assessment Agent |
| BP-001 | Buyer Psychology | 1 | Opus | P1 | Cognitive Bias Detector |
| BP-002 | Buyer Psychology | 1 | Opus | P1 | Buyer Personality Profiler |
| BP-003 | Buyer Psychology | 1 | Sonnet | P1 | Communication Style Adapter |
| BP-004 | Buyer Psychology | 1 | Sonnet | P1 | Emotional State Tracker |
| BP-005 | Buyer Psychology | 1 | Opus | P2 | Influence Principle Applicator |
| VE-001 | Value Engineering | 1 | Opus | P0 | ROI Calculator Builder |
| VE-002 | Value Engineering | 1 | Opus | P1 | TCO Analyzer |
| VE-003 | Value Engineering | 1 | Opus | P0 | Business Case Generator |
| VE-004 | Value Engineering | 1 | Sonnet | P1 | Competitive Comparison Agent |
| VE-005 | Value Engineering | 1 | Sonnet | P2 | Cost of Inaction Modeler |
| VE-006 | Value Engineering | 1 | Opus | P1 | Risk-Adjusted ROI Agent |
| DC-001 | Discovery Team | 1 | Opus | P0 | Problem Diagnosis Agent |
| DC-002 | Discovery Team | 1 | Sonnet | P1 | Gap Analyst |
| DC-003 | Discovery Team | 1 | Opus | P0 | Stakeholder Mapper |
| DC-004 | Discovery Team | 1 | Sonnet | P1 | Needs Hierarchy Builder |
| DC-005 | Discovery Team | 1 | Sonnet | P1 | Decision Process Mapper |
| DC-006 | Discovery Team | 1 | Opus | P1 | Technical Environment Mapper |
| CT-001 | Content Team | 1 | Opus | P0 | Value Messaging Generator |
| CT-002 | Content Team | 1 | Opus | P0 | Proposal Generator |
| CT-003 | Content Team | 1 | Sonnet | P1 | Case Study Adapter |
| CT-004 | Content Team | 1 | Sonnet | P1 | Battle Card Updater |
| CT-005 | Content Team | 1 | Sonnet | P1 | Presentation Builder |
| CT-006 | Content Team | 1 | Sonnet | P1 | Email Template Generator |
| DS-001 | Deal Strategy Team | 2 | Opus | P0 | Deal Planner |
| DS-002 | Deal Strategy Team | 2 | Opus | P1 | Competitive Positioning Strategist |
| DS-003 | Deal Strategy Team | 2 | Opus | P0 | Win/Loss Analyst |
| DS-004 | Deal Strategy Team | 2 | Opus | P0 | Price Optimizer |
| DS-005 | Deal Strategy Team | 2 | Sonnet | P1 | Discount Authority Agent |
| NG-001 | Negotiation Team | 2 | Opus | P0 | BATNA Analyst |
| NG-002 | Negotiation Team | 2 | Opus | P1 | Concession Planner |
| NG-003 | Negotiation Team | 2 | Opus | P0 | Procurement Defense Agent |
| NG-004 | Negotiation Team | 2 | Opus | P1 | Terms Optimizer |
| NG-005 | Negotiation Team | 2 | Opus | P1 | Leverage Identifier |
| NG-006 | Negotiation Team | 2 | Opus | P1 | Contract Redlining Agent |
| RI-001 | Relationship Intel. | 2 | Sonnet | P0 | Stakeholder Mapper (Rel.) |
| RI-002 | Relationship Intel. | 2 | Sonnet | P1 | Relationship Health Scorer |
| RI-003 | Relationship Intel. | 2 | Haiku | P2 | Communication Pattern Analyst |
| RI-004 | Relationship Intel. | 2 | Opus | P0 | Churn Predictor |
| RI-005 | Relationship Intel. | 2 | Sonnet | P1 | Interaction History Analyst |
| RO-001 | Revenue Operations | 2 | Haiku | P0 | CRM Hygiene Agent |
| RO-002 | Revenue Operations | 2 | Sonnet | P0 | Pipeline Analyst |
| RO-003 | Revenue Operations | 2 | Opus | P0 | Forecasting Engine |
| RO-004 | Revenue Operations | 2 | Opus | P1 | Territory Designer |
| RO-005 | Revenue Operations | 2 | Haiku | P1 | Commission Tracker |
| RO-006 | Revenue Operations | 2 | Sonnet | P1 | Process Compliance Agent |
| CS-001 | Customer Success | 2 | Sonnet | P0 | Customer Health Scorer |
| CS-002 | Customer Success | 2 | Sonnet | P1 | Adoption Monitor |
| CS-003 | Customer Success | 2 | Sonnet | P1 | Expansion Identifier |
| CS-004 | Customer Success | 2 | Opus | P0 | Renewal Risk Manager |
| ABM-001 | ABM Team | 3 | Sonnet | P1 | Account Selection & Tiering |
| ABM-002 | ABM Team | 3 | Sonnet | P1 | Campaign Designer |
| ABM-003 | ABM Team | 3 | Sonnet | P2 | Content Personalizer |
| ABM-004 | ABM Team | 3 | Haiku | P2 | Account Coverage Monitor |
| PL-001 | Procurement/Legal | 3 | Opus | P0 | Procurement Process Agent |
| PL-002 | Procurement/Legal | 3 | Opus | P0 | Legal Terms Agent |
| PL-003 | Procurement/Legal | 3 | Opus | P0 | Compliance Checker |
| PL-004 | Procurement/Legal | 3 | Sonnet | P1 | Security Reviewer |
| EA-001 | Executive Advisory | 3 | Opus | P1 | Executive Briefing Generator |
| EA-002 | Executive Advisory | 3 | Opus | P2 | Board Meeting Preparer |
| EA-003 | Executive Advisory | 3 | Sonnet | P2 | Competitive Landscape Brief |
| PA-001 | Partner/Alliance | 3 | Sonnet | P2 | Partner Identification Agent |
| PA-002 | Partner/Alliance | 3 | Sonnet | P2 | Joint GTM Planner |
| PA-003 | Partner/Alliance | 3 | Sonnet | P2 | Partner Relationship Manager |
| SC-001 | Security/Compliance | 3 | Opus | P0 | Data Privacy Agent |
| SC-002 | Security/Compliance | 3 | Sonnet | P1 | Export Control Agent |
| SC-003 | Security/Compliance | 3 | Sonnet | P1 | Risk Scoring Agent |
| SC-004 | Security/Compliance | 3 | Opus | P1 | Security Audit Agent |
| DLC-001 | Delivery Confidence | 3 | Opus | P1 | Implementation Risk Assessor |
| DLC-002 | Delivery Confidence | 3 | Sonnet | P2 | Resource Planner |
| DLC-003 | Delivery Confidence | 3 | Sonnet | P2 | Timeline Validator |
| RFP-001 | RFP/RFQ Team | 3 | Opus | P1 | RFP Intake & Analysis |
| RFP-002 | RFP/RFQ Team | 3 | Opus | P1 | Response Generator |
| RFP-003 | RFP/RFQ Team | 3 | Sonnet | P2 | RFP Knowledge Base |
| RFP-004 | RFP/RFQ Team | 3 | Sonnet | P2 | RFP Quality Reviewer |
| KL-001 | Knowledge & Learning | 4 | Opus | P1 | Pattern Extraction Agent |
| KL-002 | Knowledge & Learning | 4 | Sonnet | P2 | Training Example Generator |
| KL-003 | Knowledge & Learning | 4 | Haiku | P2 | Content Indexer |
| KL-004 | Knowledge & Learning | 4 | Sonnet | P1 | Playbook Updater |
| KL-005 | Knowledge & Learning | 4 | Opus | P1 | Agent Training Agent |
| KL-006 | Knowledge & Learning | 4 | Haiku | P2 | RAG Index Maintainer |
| AG-001 | AI Governance | 4 | Opus | P1 | Agent Performance Monitor |
| AG-002 | AI Governance | 4 | Opus | P1 | Bias Detector |
| AG-003 | AI Governance | 4 | Sonnet | P2 | Prompt Version Manager |
| AG-004 | AI Governance | 4 | Haiku | P2 | Token Usage Auditor |
| AI-001 | Account Intelligence | 3 | Sonnet | P1 | Firmographic Tracker |
| AI-002 | Account Intelligence | 3 | Opus | P1 | Technographic Profiler |
| AI-003 | Account Intelligence | 3 | Sonnet | P1 | News & Event Monitor |
| AI-004 | Account Intelligence | 3 | Sonnet | P2 | Buying Group Identifier |
| SPR-001 | Sales Psychology Res. | 4 | Opus | P2 | Sales Method Researcher |
| SPR-002 | Sales Psychology Res. | 4 | Opus | P2 | Framework Validator |
| SPR-003 | Sales Psychology Res. | 4 | Sonnet | P2 | Methodology Adapter |
| CV-001 | Customer Voice | 3 | Sonnet | P1 | Testimonial Miner |
| CV-002 | Customer Voice | 3 | Sonnet | P1 | Reference Matcher |
| CV-003 | Customer Voice | 3 | Haiku | P2 | NPS Analyzer |
| DSV-001 | Data Services | 4 | Haiku | P1 | Data Pipeline Manager |
| DSV-002 | Data Services | 4 | Sonnet | P1 | Schema Validator |
| DSV-003 | Data Services | 4 | Haiku | P2 | Data Retention Enforcer |
| SP-001 | Security & Privacy | 4 | Opus | P1 | Access Control Auditor |
| SP-002 | Security & Privacy | 4 | Sonnet | P2 | Incident Responder |
| SP-003 | Security & Privacy | 4 | Haiku | P2 | Policy Enforcer |

### Appendix D: Key Metrics and SLAs

| Metric | Target | Measurement | SLI |
|--------|--------|-------------|-----|
| End-to-end deal processing time (standard) | < 2 hours | Time from lead creation to close-ready (human review time excluded) | p95 < 4hr |
| Agent execution latency (Tier 1) | < 5 seconds | Time from event receipt to output published | p99 < 15s |
| Agent execution latency (Tier 2) | < 10 seconds | Same | p99 < 30s |
| Agent execution latency (Tier 3) | < 15 seconds | Same | p99 < 45s |
| Agent execution latency (Tier 4) | < 60 seconds | Same | p99 < 120s |
| Human gate response (Urgent/P0) | < 15 minutes | Time from notification to decision | p95 < 30min |
| Human gate response (Standard/P2) | < 24 hours | Same | p95 < 48hr |
| System uptime (NATS + K8s) | 99.9% | Excludes planned maintenance | Monthly |
| Agent uptime | 99.5% | Per-agent, excludes scale-to-zero | Monthly |
| Data loss | 0% | No committed events lost after NATS ack | Perpetual |
| LLM API error rate | < 2% | Failed calls / total calls | Weekly |
| Undetected objections | < 10% | Objections caught / total objections (sampled audit) | Per-agent rolling |
| Qualification accuracy | > 85% | Manual audit of qualification vs actual outcome | Monthly |
| Forecast accuracy (quarter) | > 80% | Predicted vs actual within ±15% | Quarterly |
| Duplicate detection rate | > 95% | Duplicates found / total duplicates | Monthly |
| KV read latency (p99) | < 5ms | Time from read request to response | p99 < 10ms |
| KV write latency (p99) | < 10ms | Time from write request to ack | p99 < 20ms |

---

> **Document Version:** 1.0
> **Author:** RevenueOS Architecture Team
> **Review Status:** Approved
> **Next Review:** 2026-09-24
> **Companion Documents:** REVENUE_OS_AGENT_SPECS.md, REVENUE_OS_IMPLEMENTATION_ROADMAP.md, REVENUE_OS_TRAINING_MATERIALS.md
