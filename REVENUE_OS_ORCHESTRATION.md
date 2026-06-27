# Revenue OS — Agent Orchestration Protocol v2.0

> **Executable specification for the inter-agent communication layer.**
> 108 agents across 12 divisions, coordinated via NATS, registered via Consul, observed via OpenTelemetry.

---

## Table of Contents

1. [NATS Subject Convention](#1-nats-subject-convention)
2. [Event Schema](#2-event-schema)
3. [Agent Manifest Format](#3-agent-manifest-format)
4. [State Machine Per Workflow](#4-state-machine-per-workflow)
5. [Error Handling Protocol](#5-error-handling-protocol)
6. [Human-in-the-Loop Protocol](#6-human-in-the-loop-protocol)
7. [Observability Contract](#7-observability-contract)
8. [Agent Discovery & Registration](#8-agent-discovery--registration)
9. [Testing & Simulation Protocol](#9-testing--simulation-protocol)
10. [Security Protocol](#10-security-protocol)

---

## 1. NATS Subject Convention

### 1.1 Subject Tree

```
revenue.{env}.deal.{deal_id}.{stage}.{action}
revenue.{env}.system.{component}.{event}
revenue.{env}.agent.{agent_id}.{event}
revenue.{env}.human.{inbox_type}.{deal_id}
revenue.{env}.dead.{original_subject}          # dead-letter mirror
```

**Env values:** `dev`, `staging`, `prod`

### 1.2 Deal Subjects

Pattern: `revenue.{env}.deal.{deal_id}.{stage}.{action}`

| Subject | Example |
|---|---|
| Deal created | `revenue.prod.deal.d_7a3f.created` |
| Stage transition | `revenue.prod.deal.d_7a3f.qualifying.entered` |
| Scoring request | `revenue.prod.deal.d_7a3f.qualifying.scoring.request` |
| Scored | `revenue.prod.deal.d_7a3f.qualifying.scored` |
| Value estimated | `revenue.prod.deal.d_7a3f.discovery.value.estimated` |
| Meeting scheduled | `revenue.prod.deal.d_7a3f.meeting_scheduled.booked` |
| Meeting completed | `revenue.prod.deal.d_7a3f.meeting_scheduled.completed` |
| Contract sent | `revenue.prod.deal.d_7a3f.contract_sent.delivered` |
| Contract signed | `revenue.prod.deal.d_7a3f.contract_sent.signed` |
| Closed won | `revenue.prod.deal.d_7a3f.closed_won.achieved` |
| Closed lost | `revenue.prod.deal.d_7a3f.closed_lost.recorded` |
| Disqualified | `revenue.prod.deal.d_7a3f.disqualified.recorded` |
| Win/loss triggered | `revenue.prod.deal.d_7a3f.winloss.triggered` |
| Forecast updated | `revenue.prod.deal.d_7a3f.forecast.updated` |
| Pipeline snapshotted | `revenue.prod.deal.d_7a3f.pipeline.snapshotted` |

Wildcards:
- `revenue.prod.deal.*.created` — all new deals
- `revenue.prod.deal.d_7a3f.*` — everything for one deal
- `revenue.prod.deal.*.contract_sent.*` — all contract events

### 1.3 System Subjects

Pattern: `revenue.{env}.system.{component}.{event}`

| Subject | Example |
|---|---|
| Pipeline snapshot trigger | `revenue.prod.system.pipeline.snapshot.triggered` |
| Forecast cycle start | `revenue.prod.system.forecast.cycle.started` |
| Forecast cycle end | `revenue.prod.system.forecast.cycle.completed` |
| Agent registry sync | `revenue.prod.system.registry.sync.requested` |
| Playbook updated globally | `revenue.prod.system.playbook.updated` |
| Configuration reload | `revenue.prod.system.config.reloaded` |
| Schema version change | `revenue.prod.system.schema.version.changed` |
| Circuit breaker tripped | `revenue.prod.system.circuit_breaker.tripped` |

### 1.4 Agent Lifecycle Subjects

Pattern: `revenue.{env}.agent.{agent_id}.{event}`

| Subject | Example |
|---|---|
| Heartbeat | `revenue.prod.agent.deal-scorer-v2.heartbeat` |
| Started | `revenue.prod.agent.deal-scorer-v2.started` |
| Shutdown | `revenue.prod.agent.deal-scorer-v2.shutdown` |
| Failure | `revenue.prod.agent.deal-scorer-v2.failure` |
| Recovery | `revenue.prod.agent.deal-scorer-v2.recovery` |
| Config update ack | `revenue.prod.agent.deal-scorer-v2.config.updated` |
| Health check response | `revenue.prod.agent.deal-scorer-v2.health.check` |

### 1.5 Human Inbox Subjects

Pattern: `revenue.{env}.human.{inbox_type}.{deal_id}`

| Subject | Example |
|---|---|
| Approval needed | `revenue.prod.human.approval.d_7a3f` |
| Escalation | `revenue.prod.human.escalation.d_7a3f` |
| Review requested | `revenue.prod.human.review.d_7a3f` |
| Notification | `revenue.prod.human.notification.d_7a3f` |
| Manual intervention | `revenue.prod.human.intervention.d_7a3f` |

Inbox types: `approval`, `escalation`, `review`, `notification`, `intervention`

---

## 2. Event Schema

### 2.1 Envelope

Every NATS message is wrapped in a standard envelope:

```json
{
  "spec_version": "2.0",
  "event_id": "evt_f8a2c9e1b3",
  "event_type": "DealCreated",
  "source_agent": "deal-ingress-v1",
  "trace_id": "tr_d4e5f6a7b8c9",
  "span_id": "sp_1a2b3c4d",
  "timestamp": "2026-06-24T14:30:00.123Z",
  "deal_id": "d_7a3f",
  "correlation_id": "corr_001",
  "causation_id": "evt_f8a2c9e1b2",
  "data": { }
}
```

**NATS header propagation:**
- `Nats-Msg-Id` → `event_id` (idempotency)
- `Traceparent` → W3C trace context
- `X-Event-Type` → `event_type`
- `X-Source-Agent` → `source_agent`

### 2.2 Event Type Definitions

#### DealCreated

```json
{
  "event_type": "DealCreated",
  "required": ["deal_id", "source", "created_at"],
  "optional": ["customer_id", "initial_value", "owner_id", "lead_source", "territory"],
  "data": {
    "deal_id": "d_7a3f",
    "source": "webform",
    "customer_id": "cus_a1b2",
    "initial_value": 50000.00,
    "currency": "USD",
    "owner_id": "usr_99",
    "lead_source": "organic_search",
    "product_line": "enterprise-suite",
    "territory": "emea",
    "created_at": "2026-06-24T14:30:00.123Z",
    "metadata": {
      "utm_campaign": "q2-enterprise",
      "referrer": "google.com"
    }
  }
}
```

#### DealScored

```json
{
  "event_type": "DealScored",
  "required": ["deal_id", "score", "score_components"],
  "data": {
    "deal_id": "d_7a3f",
    "score": 72.5,
    "score_components": {
      "budget_fit": 0.85,
      "authority_presence": 0.60,
      "need_urgency": 0.90,
      "timeline_alignment": 0.55,
      "competitor_risk": 0.30
    },
    "score_version": "v3.1",
    "scored_by": "deal-scorer-v2",
    "model": "sonnet-4.5-qualification",
    "confidence_interval": [68.2, 76.8],
    "scored_at": "2026-06-24T14:30:05.456Z"
  }
}
```

#### DealQualified

```json
{
  "event_type": "DealQualified",
  "required": ["deal_id", "qualification_result", "qualified_by"],
  "data": {
    "deal_id": "d_7a3f",
    "qualification_result": "passed",
    "qualified_by": "qualification-engine-v1",
    "qualification_framework": "bant-v2",
    "bant_assessment": {
      "budget": "confirmed",
      "authority": "identified",
      "need": "validated",
      "timeline": "this_quarter"
    },
    "confidence": 0.88,
    "next_action": "schedule_discovery",
    "qualified_at": "2026-06-24T14:30:10.789Z"
  }
}
```

#### DealDisqualified

```json
{
  "event_type": "DealDisqualified",
  "required": ["deal_id", "reason", "disqualified_by"],
  "data": {
    "deal_id": "d_7a3f",
    "reason": "budget_unavailable",
    "detail": "Contact confirmed no budget allocation until next fiscal year",
    "disqualified_by": "qualification-engine-v1",
    "disqualification_source": "email_analysis",
    "evidence_refs": ["email_e_4b5c", "meeting_m_8d2e"],
    "disqualified_at": "2026-06-24T14:30:15.234Z"
  }
}
```

#### DealValueEstimated

```json
{
  "event_type": "DealValueEstimated",
  "required": ["deal_id", "estimated_value", "confidence"],
  "data": {
    "deal_id": "d_7a3f",
    "estimated_value": 125000.00,
    "currency": "USD",
    "confidence": 0.74,
    "value_range_low": 95000.00,
    "value_range_high": 155000.00,
    "estimation_method": "deal-comparison-model-v2",
    "features_used": [
      "deal_size_similar_deals",
      "company_revenue",
      "employee_count",
      "industry_vertical",
      "engagement_intensity"
    ],
    "top_similar_deal": "d_2c1e",
    "estimated_at": "2026-06-24T14:35:00.456Z"
  }
}
```

#### MeetingScheduled

```json
{
  "event_type": "MeetingScheduled",
  "required": ["deal_id", "meeting_id", "scheduled_at", "participants"],
  "data": {
    "deal_id": "d_7a3f",
    "meeting_id": "m_8d2e",
    "meeting_type": "discovery",
    "scheduled_at": "2026-06-28T10:00:00Z",
    "duration_minutes": 45,
    "participants": [
      {"id": "usr_99", "role": "owner", "name": "Alice Chen"},
      {"id": "con_5b", "role": "prospect", "name": "Bob Martinez"},
      {"id": "con_6c", "role": "prospect", "name": "Carol Wu"}
    ],
    "location": "video/zoom",
    "notes": "First discovery call",
    "scheduled_by": "meeting-scheduler-v1",
    "booking_channel": "calendly",
    "created_at": "2026-06-24T14:40:00.789Z"
  }
}
```

#### MeetingTranscriptAvailable

```json
{
  "event_type": "MeetingTranscriptAvailable",
  "required": ["deal_id", "meeting_id", "transcript_url"],
  "data": {
    "deal_id": "d_7a3f",
    "meeting_id": "m_8d2e",
    "transcript_url": "s3://revenue-transcripts/prod/d_7a3f/m_8d2e.vtt",
    "duration_seconds": 2700,
    "word_count": 8452,
    "language": "en",
    "speaker_count": 3,
    "available_at": "2026-06-28T10:48:00.123Z",
    "processing_info": {
      "provider": "deepgram",
      "model": "nova-2",
      "confidence": 0.96
    }
  }
}
```

#### MeetingInsightExtracted

```json
{
  "event_type": "MeetingInsightExtracted",
  "required": ["deal_id", "meeting_id", "insights"],
  "data": {
    "deal_id": "d_7a3f",
    "meeting_id": "m_8d2e",
    "insights": {
      "pain_points": [
        "Current CRM integration costs are too high",
        "Manual data entry consuming 12h/week per rep"
      ],
      "budget_clues": ["Looking at 6-figure solutions", "Have used similar tools before"],
      "decision_process": ["CFO approval needed", "Evaluation committee of 4"],
      "competitors_mentioned": ["Salesforce", "HubSpot"],
      "sentiment_trend": "positive",
      "action_items": [
        "Send pricing proposal by Friday",
        "Schedule technical demo for next week"
      ]
    },
    "key_quotes": [
      {"speaker": "Bob Martinez", "text": "If this works as advertised, we'd want to roll it out across all 5 regions", "timestamp_sec": 1245}
    ],
    "summary": "Prospect is actively evaluating CRM alternatives, motivated by cost and efficiency. Strong fit signaled.",
    "extracted_by": "meeting-intelligence-v2",
    "extracted_at": "2026-06-28T10:50:00.456Z"
  }
}
```

#### EmailSent

```json
{
  "event_type": "EmailSent",
  "required": ["deal_id", "email_id", "from", "to", "subject"],
  "data": {
    "deal_id": "d_7a3f",
    "email_id": "e_4b5c",
    "from": "alice@acme.com",
    "to": ["bob@example.com"],
    "cc": [],
    "subject": "Discovery call follow-up",
    "body_preview": "Hi Bob, thanks for the great conversation...",
    "email_type": "follow_up",
    "sequence_step": 2,
    "generated_by_agent": "email-composer-v1",
    "sent_at": "2026-06-28T11:00:00.789Z",
    "message_id": "<abc123@mail.acme.com>"
  }
}
```

#### EmailOpened

```json
{
  "event_type": "EmailOpened",
  "required": ["deal_id", "email_id"],
  "data": {
    "deal_id": "d_7a3f",
    "email_id": "e_4b5c",
    "opened_at": "2026-06-28T14:22:00.123Z",
    "device": "mobile",
    "location_city": "London",
    "opens_count": 2
  }
}
```

#### EmailReplied

```json
{
  "event_type": "EmailReplied",
  "required": ["deal_id", "email_id", "reply_email_id"],
  "data": {
    "deal_id": "d_7a3f",
    "email_id": "e_4b5c",
    "reply_email_id": "e_7d8f",
    "from": "bob@example.com",
    "to": ["alice@acme.com"],
    "subject": "Re: Discovery call follow-up",
    "body_preview": "Looks good. Let's set up the technical demo for next Tuesday...",
    "sentiment": "positive",
    "replied_at": "2026-06-28T15:00:00.456Z"
  }
}
```

#### ContractSent

```json
{
  "event_type": "ContractSent",
  "required": ["deal_id", "contract_id", "sent_to"],
  "data": {
    "deal_id": "d_7a3f",
    "contract_id": "c_9a0b",
    "contract_version": "2",
    "sent_to": ["bob@example.com"],
    "cc": ["legal@example.com"],
    "value": 120000.00,
    "currency": "USD",
    "term_months": 12,
    "contract_type": "saas_enterprise",
    "esign_provider": "docusign",
    "esign_envelope_id": "env_5x7y8z",
    "sent_by_agent": "contract-engine-v2",
    "sent_at": "2026-07-10T09:00:00.789Z",
    "key_terms_hash": "sha256:a1b2c3d4e5f6..."
  }
}
```

#### ContractSigned

```json
{
  "event_type": "ContractSigned",
  "required": ["deal_id", "contract_id", "signed_by"],
  "data": {
    "deal_id": "d_7a3f",
    "contract_id": "c_9a0b",
    "signed_by": [
      {"name": "Bob Martinez", "email": "bob@example.com", "role": "signer", "signed_at": "2026-07-12T16:30:00.123Z", "ip_address": "203.0.113.42"}
    ],
    "signed_at": "2026-07-12T16:30:00.123Z",
    "executed_copy_url": "s3://revenue-contracts/prod/d_7a3f/c_9a0b_signed.pdf",
    "esign_provider": "docusign",
    "esign_envelope_id": "env_5x7y8z",
    "signature_verification": "passed"
  }
}
```

#### ContractAmended

```json
{
  "event_type": "ContractAmended",
  "required": ["deal_id", "contract_id", "amendment_summary"],
  "data": {
    "deal_id": "d_7a3f",
    "contract_id": "c_9a0b",
    "contract_version": "3",
    "previous_version": "2",
    "amendment_summary": "Changed payment terms from net-30 to net-60 per CFO request",
    "changes": [
      {"field": "payment_terms", "old_value": "net-30", "new_value": "net-60"},
      {"field": "start_date", "old_value": "2026-08-01", "new_value": "2026-09-01"}
    ],
    "requested_by": "bob@example.com",
    "approved_by_agent": true,
    "amended_at": "2026-07-14T10:00:00.456Z"
  }
}
```

#### WinLossAnalyzed

```json
{
  "event_type": "WinLossAnalyzed",
  "required": ["deal_id", "outcome", "analysis"],
  "data": {
    "deal_id": "d_7a3f",
    "outcome": "won",
    "analysis": {
      "primary_win_reason": "Superior integration capabilities",
      "secondary_factors": ["Price competitiveness", "Existing vendor relationship"],
      "competitor": "Salesforce",
      "deal_velocity": 32,
      "key_moments": [
        {"day": 5, "event": "Technical demo — prospect impressed"},
        {"day": 18, "event": "CFO approved budget"}
      ]
    },
    "recommended_playbook_updates": [
      "Emphasize integration speed in discovery calls",
      "Prepare competitor comparison matrix for Salesforce prospects"
    ],
    "analyzed_by": "winloss-analyzer-v1",
    "analyzed_at": "2026-07-13T08:00:00.789Z"
  }
}
```

#### ForecastUpdated

```json
{
  "event_type": "ForecastUpdated",
  "required": ["deal_id", "forecast_category", "probability"],
  "data": {
    "deal_id": "d_7a3f",
    "forecast_category": "commit",
    "probability": 0.85,
    "weighted_value": 102000.00,
    "previous_probability": 0.60,
    "change_reason": "Contract sent for signature",
    "owner_id": "usr_99",
    "forecast_period": "2026-Q3",
    "updated_at": "2026-07-10T09:05:00.123Z"
  }
}
```

#### PipelineSnapshotted

```json
{
  "event_type": "PipelineSnapshotted",
  "required": ["snapshot_id", "snapshot_time", "total_value", "deal_count"],
  "data": {
    "snapshot_id": "snap_2026_06_24_235959",
    "snapshot_time": "2026-06-24T23:59:59Z",
    "total_value": 5842000.00,
    "weighted_value": 3100000.00,
    "deal_count": 147,
    "by_stage": {
      "prospecting": {"count": 42, "value": 1200000.00},
      "qualifying": {"count": 28, "value": 890000.00},
      "discovery": {"count": 31, "value": 1450000.00},
      "negotiating": {"count": 35, "value": 1750000.00},
      "contract_sent": {"count": 11, "value": 552000.00}
    },
    "by_territory": {
      "amer": {"count": 58, "value": 2400000.00},
      "emea": {"count": 62, "value": 2642000.00},
      "apac": {"count": 27, "value": 800000.00}
    },
    "snapshotted_by": "pipeline-snapshotter-v1"
  }
}
```

#### ApprovalRequired

```json
{
  "event_type": "ApprovalRequired",
  "required": ["deal_id", "request_id", "approval_type", "requested_by", "required_approvers"],
  "data": {
    "deal_id": "d_7a3f",
    "request_id": "apr_1122",
    "approval_type": "discount_exception",
    "requested_by": "usr_99",
    "required_approvers": ["usr_88", "usr_77"],
    "approval_deadline": "2026-07-11T17:00:00Z",
    "context": {
      "current_discount": 0.35,
      "requested_discount": 0.45,
      "standard_max": 0.30,
      "deal_value": 120000.00,
      "customer_tenure_months": 0
    },
    "slack_channel": "#deal-approvals",
    "slack_message_ts": "1687628400.123456",
    "requested_at": "2026-07-10T09:00:00.789Z"
  }
}
```

#### ApprovalGranted

```json
{
  "event_type": "ApprovalGranted",
  "required": ["deal_id", "request_id", "approved_by"],
  "data": {
    "deal_id": "d_7a3f",
    "request_id": "apr_1122",
    "approval_type": "discount_exception",
    "approved_by": "usr_88",
    "approved_at": "2026-07-10T11:30:00.123Z",
    "conditions": "One-time exception. Standard pricing applies to renewals.",
    "decision_notes": "Approved due to strategic account potential"
  }
}
```

#### ApprovalDenied

```json
{
  "event_type": "ApprovalDenied",
  "required": ["deal_id", "request_id", "denied_by", "reason"],
  "data": {
    "deal_id": "d_7a3f",
    "request_id": "apr_1122",
    "approval_type": "discount_exception",
    "denied_by": "usr_88",
    "reason": "Deal does not meet strategic exception criteria",
    "denied_at": "2026-07-10T11:30:00.123Z",
    "feedback": "Consider value-selling rather than discounting. Use case study ROI calculator."
  }
}
```

#### EscalationTriggered

```json
{
  "event_type": "EscalationTriggered",
  "required": ["deal_id", "escalation_level", "reason", "triggered_by"],
  "data": {
    "deal_id": "d_7a3f",
    "escalation_level": "level_2",
    "reason": "Deal stalled in negotiation for 14 days with no response",
    "triggered_by": "deal-stale-watcher-v1",
    "detail": "Last contact: 14 days ago. 3 follow-up emails sent with no reply.",
    "assigned_to": "usr_77",
    "priority": "high",
    "triggered_at": "2026-07-24T09:00:00.789Z"
  }
}
```

#### AgentHeartbeat

```json
{
  "event_type": "AgentHeartbeat",
  "required": ["agent_id", "version", "status"],
  "data": {
    "agent_id": "deal-scorer-v2",
    "version": "1.2.3",
    "status": "healthy",
    "uptime_seconds": 86400,
    "processed_total": 15420,
    "failed_total": 12,
    "last_failure_at": null,
    "queue_depth": 5,
    "memory_mb": 256,
    "cpu_pct": 12.5,
    "timestamp": "2026-06-24T14:30:00.000Z"
  }
}
```

#### AgentFailure

```json
{
  "event_type": "AgentFailure",
  "required": ["agent_id", "failure_type", "message"],
  "data": {
    "agent_id": "deal-scorer-v2",
    "failure_type": "model_timeout",
    "message": "LLM inference exceeded 30s timeout",
    "detail": "Model sonnet-4.5-qualification timed out on deal d_7a3f after 30000ms",
    "traceback": "File 'src/scorer.py', line 142, in score_deal...",
    "failed_at": "2026-06-24T14:30:15.234Z",
    "recoverable": true,
    "affected_deal_id": "d_7a3f"
  }
}
```

#### AgentRecovery

```json
{
  "event_type": "AgentRecovery",
  "required": ["agent_id", "recovery_type"],
  "data": {
    "agent_id": "deal-scorer-v2",
    "recovery_type": "automatic_restart",
    "downtime_seconds": 12,
    "failed_events_replayed": 3,
    "recovered_at": "2026-06-24T14:30:27.456Z"
  }
}
```

#### AgentConfigUpdate

```json
{
  "event_type": "AgentConfigUpdate",
  "required": ["agent_id", "config_version", "changes"],
  "data": {
    "agent_id": "deal-scorer-v2",
    "config_version": "1.2.4",
    "previous_version": "1.2.3",
    "changes": [
      {"key": "scoring.model", "old_value": "sonnet-4.5-qualification", "new_value": "opus-4.5-qualification"},
      {"key": "scoring.timeout_ms", "old_value": "30000", "new_value": "45000"}
    ],
    "updated_by": "config-manager-v1",
    "effective_immediately": false,
    "requires_restart": false,
    "rollout_strategy": "rolling",
    "updated_at": "2026-06-24T14:00:00.000Z",
    "applied_at": "2026-06-24T14:01:00.000Z"
  }
}
```

---

## 3. Agent Manifest Format

### 3.1 Schema

Every agent must ship a `manifest.yaml` in its root directory. The orchestrator reads these on registration.

```yaml
agent_id: deal-scorer                # unique identifier across all 108 agents
version: 1.2.3                       # semver
division: qualification               # one of: ingestion, qualification, discovery, negotiation, contracting, renewals, winloss, forecasting, pipeline, intelligence, orchestration, human_interface
llm_tier: sonnet                      # none | haiku | sonnet | opus | custom:<model>
criticality: p1                       # p0 (system-down) | p1 (critical-biz) | p2 (important) | p3 (best-effort)

description: |
  Scores deals on BANT+ fit using LLM analysis of customer data.
  Publishes scored events for qualification engine consumption.

tags:
  - scoring
  - bant
  - llm-inference

owner: team-qualification
slack_channel: "#deal-scoring-alerts"

dependencies:
  - agent: data-enrichment-v1         # must be running
    required: true
  - service: crm-api
    required: true
  - service: llm-gateway
    required: true
    timeout_ms: 30000

subscribes:
  - subject: revenue.prod.deal.*.created
    queue_group: deal-scorers
    description: "Score every new deal on creation"
  - subject: revenue.prod.deal.*.scoring.request
    queue_group: deal-scorers
    description: "Re-score on explicit request"
  - subject: revenue.prod.system.config.reloaded
    description: "Reload model config on broadcast"

publishes:
  - subject: revenue.prod.deal.*.scored
    description: "Deal scored successfully"
  - subject: revenue.prod.deal.*.scoring.failed
    description: "Scoring failed (recoverable)"
  - subject: revenue.prod.agent.deal-scorer-v2.heartbeat
    description: "Liveness signal"

kv_access:                            # NATS KV Store permissions
  read_keys:
    - metadata                        # deal metadata bucket
    - customer                        # customer data bucket
    - scoring                         # scoring results bucket
  write_key: scoring                  # only scoring bucket

resources:
  min_replicas: 1
  max_replicas: 10
  scaling_threshold: 100              # queue depth triggers scale-up
  cpu_request: "0.5"
  memory_request: "512Mi"
  cpu_limit: "2.0"
  memory_limit: "1Gi"

sla:
  p95_latency_ms: 5000                # 5s to score a deal
  p99_latency_ms: 15000
  error_rate_max: 0.01                # 1% max error rate
  availability: 0.995
  throughput_per_sec: 50

retry:
  max_retries: 3
  backoff_strategy: exponential       # exponential | linear | fixed
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retry_on: [model_timeout, rate_limited, service_unavailable]

circuit_breaker:
  failure_threshold: 10               # per 60s window
  cooldown_seconds: 30
  half_open_max_requests: 3

shutdown:
  graceful_timeout_seconds: 30        # max time to drain + cleanup
  drain_first: true

health:
  liveness_port: 8090
  liveness_path: "/health/live"
  readiness_port: 8090
  readiness_path: "/health/ready"
  heartbeat_interval_seconds: 15

security:
  nats_token_secret: "agents/deal-scorer/nats-token"
  mls_cert_secret: "agents/deal-scorer/tls-cert"
  allow_origins: ["revenue.prod.deal.*"]
  audit_log: true
```

### 3.2 Manifest Discovery

The orchestrator loads manifests from a versioned KV store:

```
NATS KV Bucket: agent-manifests
  Key: deal-scorer    → {manifest YAML}
  Key: deal-scorer.v1.2.3 → {manifest YAML, pinned}
```

---

## 4. State Machine Per Workflow

### 4.1 New Deal Workflow

```
                    ┌─────────────────────────────────────────────────────────────────────┐
                    │                                                                     │
                    v                                                                     │
CREATED ──→ PROSPECTING ──→ MEETING_SCHEDULED ──→ MEETING_COMPLETED ──→ QUALIFYING ──→ QUALIFIED ──→ DISCOVERY ──→ VALUE_ESTIMATED ──→ STRATEGY_DEVELOPED ──→ NEGOTIATING ──→ CONTRACT_SENT ──→ CONTRACT_SIGNED ──→ CLOSED_WON
    │              │                   │                    │                  │              │              │                    │                       │                    │                    │                    │
    │              │                   │                    │                  │              │              │                    │                       │                    │                    │                    │
    │              v                   v                    v                  v              v              v                    v                       v                    v                    v                    v
    └──→ DISQUALIFIED ←─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
     ──→ CLOSED_LOST  ←─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| State | Entry Condition | Exit Condition | Timeout | Allowed Transitions |
|---|---|---|---|---|
| CREATED | DealCreated event received | Prospecting started or disqualified | 24h | PROSPECTING, DISQUALIFIED |
| PROSPECTING | Research + outreach initiated | Meeting booked or disqualified | 72h | MEETING_SCHEDULED, DISQUALIFIED |
| MEETING_SCHEDULED | Calendar slot confirmed | Meeting completed or disqualified | — (held at scheduled time) | MEETING_COMPLETED, DISQUALIFIED |
| MEETING_COMPLETED | Transcript available | Qualification result produced | 4h | QUALIFYING, DISQUALIFIED |
| QUALIFYING | Score request published | Qualified or disqualified | 30min | QUALIFIED, DISQUALIFIED |
| QUALIFIED | Qualification = passed | Discovery initiated | 48h | DISCOVERY, DISQUALIFIED |
| DISCOVERY | Value estimation requested | Value estimated or disqualified | 72h | VALUE_ESTIMATED, DISQUALIFIED, QUALIFYING (back) |
| VALUE_ESTIMATED | Estimated value published | Strategy developed | 24h | STRATEGY_DEVELOPED, DISQUALIFIED |
| STRATEGY_DEVELOPED | Strategy document created | Negotiation started | 48h | NEGOTIATING, DISQUALIFIED |
| NEGOTIATING | Counteroffer cycle active | Contract sent or lost | 14d | CONTRACT_SENT, CLOSED_LOST, DISQUALIFIED |
| CONTRACT_SENT | Esign envelope delivered | Signed, lost, or amended | 7d | CONTRACT_SIGNED, CLOSED_LOST, CONTRACT_SENT (amended) |
| CONTRACT_SIGNED | All signatures collected | Revenue recognized | 24h | CLOSED_WON |
| CLOSED_WON | Deal marked won | Win/loss analysis triggered | — | WINLOSS_TRIGGERED (workflow transition) |
| DISQUALIFIED | Disqualification reason recorded | Terminal | — | — |
| CLOSED_LOST | Loss reason recorded | Win/loss analysis triggered | — | WINLOSS_TRIGGERED (workflow transition) |

**Timeout handling:** When a state timeout fires, an `EscalationTriggered` event is published. The escalation agent escalates to the human owner.

**HIBERNATING** — added after any state when deal is stalled >7 days without activity
- **Entry condition:** No events on deal subjects for 7 consecutive days + deal not in CLOSED_WON, CLOSED_LOST, or DISQUALIFIED
- **Exit condition:** Any new event on deal subjects, or manual wake via `deal.wake`
- **Timeout:** 90 days → auto CLOSED_LOST
- **Side effects:** RCC-005 (Deal Slippage Monitor) publishes `deal.hibernated` notification. Agent processing paused — only RCC-001 monitors hibernated deals.
- **Transitions:** from any active state → HIBERNATING → back to previous state on wake

State machine addition:
```
NEGOTIATING → HIBERNATING (7 days no activity)
↓
HIBERNATING → NEGOTIATING (on new event)
HIBERNATING → CLOSED_LOST (90 day timeout)
```

### 4.2 Renewal Workflow

```
RENEWAL_DETECTED ──→ HEALTH_ASSESSED ──→ EXPANSION_EVALUATED ──→ RENEWAL_PROPOSED ──→ RENEWAL_NEGOTIATING ──→ RENEWAL_COMPLETED ──→ CLOSED_RENEWED
                         │                      │                        │                       │                     │
                         v                      v                        v                       v                     v
                      └──→ CLOSED_CHURNED ←─────────────────────────────────────────────────────────────────────────────────┘
```

| State | Entry Condition | Exit Condition | Timeout | Allowed Transitions |
|---|---|---|---|---|
| RENEWAL_DETECTED | 90 days before contract end | Health assessed or churned | 24h | HEALTH_ASSESSED, CLOSED_CHURNED |
| HEALTH_ASSESSED | Usage + sentiment data analyzed | Expansion evaluated or churned | 48h | EXPANSION_EVALUATED, CLOSED_CHURNED |
| EXPANSION_EVALUATED | Upsell/cross-sell opportunities scored | Renewal proposed | 72h | RENEWAL_PROPOSED, CLOSED_CHURNED |
| RENEWAL_PROPOSED | Renewal contract generated | Negotiation started | 7d | RENEWAL_NEGOTIATING, CLOSED_CHURNED |
| RENEWAL_NEGOTIATING | Terms discussed | Completed or churned | 14d | RENEWAL_COMPLETED, CLOSED_CHURNED |
| RENEWAL_COMPLETED | Contract executed | Revenue recognized | 24h | CLOSED_RENEWED |
| CLOSED_RENEWED | Renewal recorded | Win/loss triggered | — | WINLOSS_TRIGGERED |
| CLOSED_CHURNED | Churn recorded | Win/loss triggered | — | WINLOSS_TRIGGERED |

### 4.3 Win/Loss Analysis

```
DEAL_CLOSED ──→ WINLOSS_TRIGGERED ──→ DATA_GATHERED ──→ ANALYSIS_COMPLETED ──→ INSIGHT_PUBLISHED ──→ PLAYBOOK_UPDATED
```

| State | Entry Condition | Exit Condition | Timeout | Allowed Transitions |
|---|---|---|---|---|
| DEAL_CLOSED | CLOSED_WON or CLOSED_LOST event | Analysis triggered | 1h | WINLOSS_TRIGGERED |
| WINLOSS_TRIGGERED | Analysis request published | Data gathered | 30min | DATA_GATHERED |
| DATA_GATHERED | Transcripts, emails, notes collected | Analysis completed | 1h | ANALYSIS_COMPLETED |
| ANALYSIS_COMPLETED | LLM analysis produced | Insight published | 15min | INSIGHT_PUBLISHED |
| INSIGHT_PUBLISHED | Raw insight stored to KV | Playbook updated | 24h | PLAYBOOK_UPDATED |
| PLAYBOOK_UPDATED | Playbook agent generates recommendations | Terminal | — | — |

---

## 5. Error Handling Protocol

### 5.1 Retry Policy

Every agent declares its retry policy in its manifest. The platform overrides for criticality levels:

| Criticality | Max Retries | Backoff | Initial Delay | Max Delay |
|---|---|---|---|---|
| p0 (system-down) | 5 | exponential | 500ms | 30s |
| p1 (critical-biz) | 3 | exponential | 1s | 30s |
| p2 (important) | 3 | exponential | 2s | 60s |
| p3 (best-effort) | 1 | fixed | 5s | 5s |

**Backoff formula:**
```
delay = min(initial_delay_ms * 2^(retry_count - 1), max_delay_ms)
jitter = random(0, delay * 0.1)
sleep(delay + jitter)
```

### 5.2 Circuit Breaker Parameters

| Parameter | Default | Description |
|---|---|---|
| failure_threshold | 10 | Consecutive failures within window |
| window_seconds | 60 | Sliding window for counting failures |
| cooldown_seconds | 30 | Time in OPEN state before half-open |
| half_open_max_requests | 3 | Requests allowed in half-open state |

**States:**
- **CLOSED** — normal operation, requests pass through
- **OPEN** — requests fail immediately, cooldown timer starts
- **HALF_OPEN** — limited requests allowed; success → CLOSED, failure → OPEN

**Circuit breaker events published on state transitions:**
- `revenue.{env}.system.circuit_breaker.opened` — agent_id, failure_count, window
- `revenue.{env}.system.circuit_breaker.half_opened` — agent_id
- `revenue.{env}.system.circuit_breaker.closed` — agent_id, recovery_count

### 5.3 Saga Compensation Events

Each workflow step that mutates state must have a compensating action:

| Step | Forward Event | Compensating Event | Compensation Action |
|---|---|---|---|
| Deal creation | DealCreated | DealVoided | Mark deal as void, revert pipeline totals |
| Deal scoring | DealScored | DealScoreRevoked | Remove score, reset to unscored state |
| Qualification | DealQualified | DealQualificationReversed | Demote to prospecting |
| Value estimation | DealValueEstimated | DealValueRecalculated | Update with new estimate |
| Meeting booking | MeetingScheduled | MeetingCancelled | Free calendar slot, notify participants |
| Email send | EmailSent | EmailRecalled | Mark as recalled (if supported by provider) |
| Contract send | ContractSent | ContractVoided | Void esign envelope, revert pipeline stage |
| Contract sign | ContractSigned | ContractSigningInvalidated | Invalidate signature, reopen negotiation |
| Approval | ApprovalGranted | ApprovalRevoked | Reverse action, re-lock workflow |

**Compensation flow:**
```
1. Agent publishes forward event
2. Saga coordinator stores event in commit log
3. If downstream processing fails:
   a. Saga coordinator publishes compensating event
   b. Original agent (or compensation handler) executes rollback
   c. Saga commit log marked as ROLLED_BACK
4. If all downstream succeeds:
   a. Saga commit log marked as COMMITTED
```

### 5.4 Dead Letter Queue

Events that fail all retries are published to the dead letter queue:

```
Subject: revenue.{env}.dead.{original_subject}
Example: revenue.prod.deal.revenue.prod.deal.d_7a3f.scoring.request
```

**Dead letter payload:**
```json
{
  "original_event": { /* full original event envelope */ },
  "failure_reason": "Exceeded max retries (3). Final error: model_timeout",
  "failure_trace": [
    {"attempt": 1, "error": "model_timeout", "at": "2026-06-24T14:30:15.234Z"},
    {"attempt": 2, "error": "model_timeout", "at": "2026-06-24T14:30:20.456Z"},
    {"attempt": 3, "error": "model_timeout", "at": "2026-06-24T14:30:30.789Z"}
  ],
  "dead_lettered_at": "2026-06-24T14:30:32.000Z",
  "dead_letter_reason": "retries_exhausted"
}
```

**Dead letter consumer responsibilities:**
1. Log the failure to the alerting system
2. Notify the owning team via Slack channel
3. For p0/p1 agents: page on-call immediately
4. Store in DLQ archive bucket (S3) with TTL of 90 days
5. Provide replay mechanism: re-publish from DLQ after fix

### 5.5 Agent Failure Notification Flow

```
Agent detects failure
  → publishes AgentFailure to revenue.{env}.agent.{agent_id}.failure
  → orchestrator receives AgentFailure
  → orchestrator checks circuit breaker
  → orchestrator evaluates recovery action:
      a. If recoverable: auto-restart agent → publish AgentRecovery
      b. If not recoverable: escalate to human → publish EscalationTriggered
  → orchestrator notifies:
      - Slack: #agent-alerts channel
      - PagerDuty: if p0/p1
      - Dashboard: metrics tile turns red
```

### 5.6 Agent Dependency Timeout & Degrade Patterns

Every agent that depends on another agent's output MUST define:

**Timeout Policy:**
- Default timeout: 30s for synchronous request-reply via NATS
- Per-agent override: declared in agent manifest under `sla.p95_latency_ms`
- On timeout: agent publishes `{subject}.timeout` event with dependency and duration
- After 3 consecutive timeouts: circuit opens for that dependency (60s cooldown)

**Degrade Patterns by Dependency Type:**
| Dependency Type | Primary Behavior | Degraded Behavior |
|----------------|-----------------|-------------------|
| Scorer (QL-001) | Full MEDDPICC score | QL-007 Haiku-tier fallback score |
| Enricher (AI-001) | Full firmographic data | Use available CRM data only |
| Sentiment (MO-002) | Real-time sentiment stream | Static sentiment from last known state |
| ROI (VE-001) | Full ROI model | Simplified TCO estimate |
| Any external API | Live data | Cached data (<1hr stale) |

**Implementation:** Each agent's manifest has an optional `dependency` block:
```yaml
dependencies:
  - agent: ql-001
    timeout_ms: 5000
    degrade_to: ql-007
    fallback_value: null
    circuit_breaker:
      failure_threshold: 3
      cooldown_ms: 60000
```

---

## 6. Human-in-the-Loop Protocol

### 6.1 Human Inbox Subjects

| Inbox Type | Subject | Description |
|---|---|---|
| Approval | `revenue.{env}.human.approval.{deal_id}` | Discount/exception/override requests |
| Escalation | `revenue.{env}.human.escalation.{deal_id}` | Stalled deals, timeout warnings |
| Review | `revenue.{env}.human.review.{deal_id}` | AI-generated content awaiting human review |
| Notification | `revenue.{env}.human.notification.{deal_id}` | Informational, no action required |
| Intervention | `revenue.{env}.human.intervention.{deal_id}` | Manual action required (e.g., enter data) |

### 6.2 Approval Request Payload

```json
{
  "event_type": "ApprovalRequired",
  "envelope": { /* standard envelope */ },
  "data": {
    "request_id": "apr_1122",
    "deal_id": "d_7a3f",
    "approval_type": "discount_exception",
    "title": "Discount exception requested for Acme Corp",
    "priority": "high",
    "requested_by": "Alice Chen (usr_99)",
    "required_approvers": [
      {"id": "usr_88", "name": "David Lee", "role": "Sales Director"},
      {"id": "usr_77", "name": "Eva Johnson", "role": "VP Revenue"}
    ],
    "approval_deadline": "2026-07-11T17:00:00Z",
    "context": {
      "current_discount": "35%",
      "requested_discount": "45%",
      "standard_max_discount": "30%",
      "deal_value": "$120,000",
      "customer": "Acme Corp",
      "owner": "Alice Chen",
      "notes": "Competitive pressure from Salesforce. Customer indicated they'll sign by Friday if approved."
    },
    "links": {
      "deal_in_crm": "https://acme.salesforce.com/opportunity/7a3f",
      "slack_thread": "https://acme.slack.com/archives/C01ABC123/p1687628400",
      "dashboard": "https://revenue.acme.com/deals/d_7a3f"
    },
    "actions": [
      {"type": "approve", "label": "Approve 45% discount"},
      {"type": "deny", "label": "Deny — offer standard max 30%"},
      {"type": "modify", "label": "Suggest different terms"}
    ]
  }
}
```

### 6.3 SLA Enforcement

| Priority | Approval SLA | Escalation SLA | Notification SLA |
|---|---|---|---|
| p0 (deal at risk) | 1h | 30min | — |
| p1 (high value) | 4h | 2h | 1h |
| p2 (standard) | 24h | 8h | 4h |
| p3 (informational) | — | 24h | 24h |

### 6.4 Escalation Chain

```
Level 0: Agent auto-resolves (within retry budget)
Level 1: Deal owner notified (Slack DM + email)
Level 2: Deal owner's manager notified (Slack + email + dashboard alert)
Level 3: VP of Revenue notified (Slack + email + SMS)
Level 4: CRO notified (Slack + SMS + phone call via PagerDuty)
```

**Escalation trigger conditions:**
- Level 1: SLA 50% elapsed
- Level 2: SLA 100% elapsed (breached)
- Level 3: SLA 200% elapsed + deal value > $100k
- Level 4: SLA 400% elapsed + deal value > $500k

### 6.5 Notification Delivery Channels

| Channel | Protocol | Use Case |
|---|---|---|
| Slack | Incoming webhook + chat.postMessage | All alerts (approval requests, escalations, notifications) |
| Email | SMTP via SES | Approval requests, daily digests |
| Dashboard | WebSocket push via NATS → dashboard agent | Real-time in-app notifications |
| SMS | Twilio API | p0/p1 escalations only |
| PagerDuty | Events API v2 | Agent failures, circuit breaker trips |

### 6.6 Pause/Resume Mechanics

**Pause:**
```
Subject: revenue.{env}.human.intervention.{deal_id}
Event: HumanInterventionRequired
Action: Agent publishes workflow paused event
  → state machine transitions to PAUSED state
  → NATS subscription for that deal_id is suspended
  → Human receives full context + action form
```

**Resume:**
```
Subject: revenue.{env}.human.intervention.{deal_id}.resumed
Event: HumanInterventionComplete
Action: Human submits decision
  → Agent resumes processing
  → State machine transitions from PAUSED to next state
  → Deal continues with human decision as input
```

**Paused deal subject mirror:**
When a deal is paused, all events for that deal mirror to `revenue.{env}.human.intervention.{deal_id}` so the human sees the full history.

### 6.7 Business-Hours SLA Calculation

SLA timers run only during business hours (defined per deal territory). Default configuration:
- **Americas:** Mon-Fri 9:00-18:00 local time
- **EMEA:** Mon-Fri 8:00-17:00 local time
- **APAC:** Mon-Fri 9:00-18:00 local time

**SLA Clock Behavior:**
- Standard queue (24h): 24 business hours
- Urgent queue (1h): 1 business hour during business hours, else next-day 9am
- VIP queue (15min): runs 24/7 regardless of business hours

**On-call escalation:** If human does not respond within SLA, escalate to next tier:
1. Assigned rep (within SLA)
2. Team lead (SLA + 50%)
3. Manager (SLA + 100%)
4. VP (SLA + 200%)

**Holiday calendar:** Each territory has a holiday calendar. SLA clock does not tick on holidays. If a deal enters human-in-box at 4:59 PM Friday, the SLA starts at 9:00 AM Monday.

---

## 7. Observability Contract

### 7.1 Tracing (OpenTelemetry)

**Span attributes every agent MUST set:**

| Attribute | Key | Example |
|---|---|---|
| Agent ID | `revenue.agent.id` | `deal-scorer-v2` |
| Agent version | `revenue.agent.version` | `1.2.3` |
| Deal ID | `revenue.deal.id` | `d_7a3f` |
| Event type | `revenue.event.type` | `DealScored` |
| Stage | `revenue.deal.stage` | `qualifying` |
| Division | `revenue.agent.division` | `qualification` |
| Criticality | `revenue.agent.criticality` | `p1` |
| Retry attempt | `revenue.retry.attempt` | `2` |
| Queue group | `revenue.nats.queue_group` | `deal-scorers` |

**Trace context propagation:**
- W3C `traceparent` header in NATS message headers
- Format: `{version}-{trace_id}-{span_id}-{trace_flags}`
- Example: `00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01`

**Span lifecycle per event:**
```
1. Consumer receives message → creates consumer span
2. Consumer processes → creates process span (nested)
3. Consumer publishes result → creates publish span (nested)
4. Consumer acks message → closes consumer span
Total: 4 spans per event processed
```

### 7.2 Metrics

**Mandatory metrics every agent MUST expose:**

| Metric | Type | Description | Labels |
|---|---|---|---|
| `revenue_events_processed_total` | Counter | Total events successfully processed | `agent_id`, `event_type` |
| `revenue_events_failed_total` | Counter | Total events that failed | `agent_id`, `event_type`, `failure_reason` |
| `revenue_processing_duration_seconds` | Histogram | Processing latency buckets (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 30) | `agent_id`, `event_type` |
| `revenue_queue_depth` | Gauge | Current NATS subscription queue depth | `agent_id`, `subject` |
| `revenue_circuit_breaker_state` | Gauge | 0=closed, 1=half_open, 2=open | `agent_id` |
| `revenue_memory_bytes` | Gauge | RSS memory in bytes | `agent_id` |
| `revenue_cpu_ratio` | Gauge | CPU usage as fraction of core | `agent_id` |
| `revenue_llm_inference_duration` | Histogram | LLM call latency (buckets: 0.1, 0.5, 1, 2, 5, 10, 30, 60) | `agent_id`, `model` |
| `revenue_llm_tokens_total` | Counter | Total tokens consumed | `agent_id`, `model`, `type` (prompt/completion) |
| `revenue_nats_messages_in_flight` | Gauge | Unacknowledged messages | `agent_id`, `subject` |

### 7.2.1 Per-Agent Token & Cost Metrics (MANDATORY from Day 1)

Every agent MUST emit these counter metrics on every LLM invocation:
| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `agent.tokens.prompt` | Counter | agent_id, model, deal_id | Prompt tokens |
| `agent.tokens.completion` | Counter | agent_id, model, deal_id | Completion tokens |
| `agent.tokens.total` | Counter | agent_id, model, deal_id | Total tokens |
| `agent.cost.estimated` | Counter | agent_id, model, deal_id | tokens * model per-token rate |

These aggregate to:
- `agent.tokens.daily` — sum by agent_id (used for budget tracking)
- `agent.cost.daily` — sum by agent_id (used for cost allocation)
- `agent.tokens.monthly` — sum by division (used for invoice reconciliation)

**Enforcement:** RCC-006 (Cost Governor) subscribes to `agent.cost.estimated` and maintains running budget counters. If any agent exceeds 80% of its daily budget, RCC-006 publishes `cost.budget_warning`. At 100%, it can optionally throttle the agent (delay non-critical tasks) or alert human.

**Implementation:** A base class/NATS middleware injects token counting automatically — individual agents do not need to implement this manually.

### 7.3 Logging

**Every log entry MUST be structured JSON:**

```json
{
  "timestamp": "2026-06-24T14:30:00.123Z",
  "level": "info",
  "logger": "deal-scorer-v2",
  "trace_id": "tr_d4e5f6a7b8c9",
  "span_id": "sp_1a2b3c4d",
  "agent_id": "deal-scorer-v2",
  "agent_version": "1.2.3",
  "deal_id": "d_7a3f",
  "event_type": "DealScored",
  "message": "Deal scored successfully",
  "duration_ms": 2340,
  "metadata": {
    "score": 72.5,
    "model": "sonnet-4.5-qualification"
  },
  "error": null
}
```

**Log levels:**
| Level | When to use |
|---|---|
| `debug` | Detailed internal flow (not emitted in prod by default) |
| `info` | Normal operation: event received, processed, published |
| `warn` | Degraded but handled: retry attempt, slow processing |
| `error` | Failure: processing failed, unrecoverable error, circuit opened |
| `fatal` | Agent cannot continue: startup failure, config corruption |

**Log output format:** JSON lines (`\n` delimited), written to stdout/stderr only (no file logging — handled by platform).

### 7.4 Health Checks

**Each agent MUST expose:**

```
GET /health/live  → 200 OK { "status": "alive", "uptime_seconds": 86400 }
GET /health/ready → 200 OK { "status": "ready", "dependencies": { "llm-gateway": "up", "crm-api": "up" } }
```

**Readiness checks verify:**
1. NATS connection is active
2. All dependent services are reachable
3. KV store is accessible
4. Agent has capacity (queue depth < max)

**Heartbeat on NATS:**
```
Subject: revenue.{env}.agent.{agent_id}.heartbeat
Interval: every 15 seconds (configurable in manifest)
```

**Orchestrator heartbeat monitoring:**
- If no heartbeat for 3x interval (45s): mark as `SUSPECT`
- If no heartbeat for 6x interval (90s): mark as `DEAD`
- If `DEAD`: orchestrate restart via Consul health check

---

## 8. Agent Discovery & Registration

### 8.1 Startup Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│ Agent Bootstrap Sequence                                             │
│                                                                      │
│  1. Load manifest.yaml                                               │
│  2. Load secrets (NATS token, TLS certs) from vault                  │
│  3. Connect to NATS with mTLS + auth token                           │
│  4. Register in Consul (service: {agent_id}, port: {health_port})   │
│  5. Subscribe to declared NATS subjects with queue groups            │
│  6. Perform readiness check (dependencies must be healthy)           │
│  7. Publish AgentStarted event                                       │
│  8. Start heartbeat loop                                             │
│  9. Begin processing messages                                        │
└─────────────────────────────────────────────────────────────────────┘
```

### 8.2 Shutdown Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│ Agent Graceful Shutdown                                              │
│                                                                      │
│  1. Receive SIGTERM or drain signal                                  │
│  2. Drain: stop accepting new messages (NATS unsubscribe)            │
│  3. Check for in-flight messages                                     │
│  4. Process remaining messages (up to graceful_timeout_seconds)      │
│  5. Unsubscribe from all subjects                                    │
│  6. Deregister from Consul                                           │
│  7. Publish AgentShutdown event                                      │
│  8. Close NATS connection                                            │
│  9. Exit                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 8.3 Consul Service Registry Schema

```json
{
  "ID": "deal-scorer-v2-node-1",
  "Name": "deal-scorer-v2",
  "Tags": ["division:qualification", "criticality:p1", "version:1.2.3"],
  "Address": "10.0.1.42",
  "Port": 8090,
  "Meta": {
    "agent_id": "deal-scorer-v2",
    "version": "1.2.3",
    "division": "qualification",
    "criticality": "p1",
    "llm_tier": "sonnet",
    "nats_subjects": "revenue.prod.deal.*.created,revenue.prod.deal.*.scoring.request",
    "health_endpoint": "/health/live",
    "started_at": "2026-06-24T14:00:00Z"
  },
  "Checks": [
    {
      "Name": "NATS Connection",
      "Status": "passing",
      "Notes": "Connected to nats://nats-cluster:4222"
    },
    {
      "Name": "HTTP Health",
      "HTTP": "http://10.0.1.42:8090/health/live",
      "Interval": "15s",
      "Timeout": "5s"
    }
  ],
  "Connect": {
    "Native": true,
    "TLS": true
  }
}
```

### 8.4 NATS KV Store Layout

| Bucket | Keys | Description |
|---|---|---|
| `agent-manifests` | `{agent_id}`, `{agent_id}.v{version}` | Agent manifests |
| `deal-state` | `{deal_id}` | Current state machine state per deal |
| `system-config` | `global`, `{division}`, `{agent_id}` | Runtime configuration |
| `scoring` | `{deal_id}` | Scoring results |
| `customer` | `{customer_id}` | Enriched customer data |
| `contracts` | `{contract_id}` | Contract metadata |
| `forecast` | `{period}` | Forecast snapshots |
| `pipeline` | `{date}` | Pipeline snapshots |
| `saga-log` | `{saga_id}` | Saga commit log entries |
| `dlq` | `{event_id}` | Dead letter entries |

---

## 9. Testing & Simulation Protocol

### 9.1 Test Event Fixtures

Every event type MUST have a corresponding fixture in `tests/fixtures/events/`:

```
tests/fixtures/events/
├── deal_created.json
├── deal_scored.json
├── deal_qualified.json
├── deal_disqualified.json
├── deal_value_estimated.json
├── meeting_scheduled.json
├── meeting_transcript_available.json
├── meeting_insight_extracted.json
├── email_sent.json
├── email_opened.json
├── email_replied.json
├── contract_sent.json
├── contract_signed.json
├── contract_amended.json
├── win_loss_analyzed.json
├── forecast_updated.json
├── pipeline_snapshotted.json
├── approval_required.json
├── approval_granted.json
├── approval_denied.json
├── escalation_triggered.json
├── agent_heartbeat.json
├── agent_failure.json
├── agent_recovery.json
├── agent_config_update.json
```

Each fixture matches the schema in section 2 with realistic test data.

### 9.2 Simulation Harness

The simulation harness (`sim/harness.py` or equivalent) provides:

```python
# Pseudocode interface
class SimulationHarness:
    def __init__(self, nats_url: str, kv_bucket: str):
        self.nats = connect(nats_url)
        self.results = []

    async def inject(self, subject: str, event: dict, trace_id: str = None) -> str:
        """Inject a fake event, return event_id"""
        event_id = generate_id()
        envelope = make_envelope(event, source="simulation-harness")
        await self.nats.publish(subject, json.dumps(envelope))
        self.results.append({"event_id": event_id, "subject": subject, "envelope": envelope})
        return event_id

    async def capture(self, subject_pattern: str, timeout_sec: int = 5) -> list[dict]:
        """Capture all events published to matching subjects within timeout"""
        captured = []
        sub = await self.nats.subscribe(subject_pattern)
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            try:
                msg = await sub.next_msg(timeout=0.5)
                captured.append(json.loads(msg.data))
            except TimeoutError:
                break
        await sub.unsubscribe()
        return captured

    async def run_workflow(self, workflow_type: str, seed_data: dict) -> SimulationResult:
        """Run a complete workflow simulation"""
        steps = WORKFLOW_DEFINITIONS[workflow_type]
        for step in steps:
            event_id = await self.inject(step.subject, step.make_event(seed_data))
            outputs = await self.capture(step.expected_output_subject)
            step.validate(outputs)
        return SimulationResult(passed=all(s.passed for s in steps))

    def assert_event(self, expected: dict, actual: dict, strict: bool = True):
        """Assert event matches schema. strict=True checks exact match."""
        # Schema validation against section 2
        # strict: all fields must match
        # not strict: only required fields must match
```

### 9.3 Chaos Testing

| Test | Description | Expected Behavior |
|---|---|---|
| Kill agent mid-processing | SIGKILL agent while processing a deal event | Agent restarts, replays unacked events, deal continues |
| NATS disconnect | Cut NATS connection for 30s | Agent buffers in memory, reconnects, replays |
| KV store timeout | Make KV store unresponsive | Agent retries with backoff, circuit opens, escalates |
| Duplicate event injection | Publish same event_id twice | Agent detects via Nats-Msg-Id, silently drops duplicate |
| Order violation | Publish events out of order | State machine rejects invalid transitions, escalates |
| Resource exhaustion | Run agent with 64MB memory limit | Agent triggers OOM killer, restart recovers |
| Slow dependency | Make LLM gateway respond in 60s | Circuit breaker opens, fails fast on subsequent requests |
| Network partition | Isolate agent from rest of cluster | Agent queues locally, replays on reconnection |
| Clock skew | System clock jumps 5 minutes | All timestamps validated against nats timestamp header |

### 9.4 Contract Testing

Every agent MUST pass contract tests that verify its input/output schema:

```yaml
# tests/contracts/deal-scorer.yaml
agent_id: deal-scorer-v2
input_subjects:
  - subject: revenue.prod.deal.*.created
    expected_schema:
      event_type: DealCreated
      required_fields: [deal_id, source, created_at]
      optional_fields: [customer_id, initial_value, owner_id]
    validation_rules:
      - field: deal_id
        pattern: "^d_[a-z0-9]+$"
      - field: source
        enum: [webform, email, api, manual, referral, event]
      - field: created_at
        type: iso8601_timestamp

output_subjects:
  - subject: revenue.prod.deal.*.scored
    expected_schema:
      event_type: DealScored
      required_fields: [deal_id, score, score_components]
    validation_rules:
      - field: score
        range: [0, 100]
      - field: score_components
        type: object
        keys_match: "^[a-z_]+$"
        values_range: [0, 1]

failure_subjects:
  - subject: revenue.prod.deal.*.scoring.failed
    expected_schema:
      event_type: AgentFailure
      required_fields: [agent_id, failure_type, message]
    validation_rules:
      - field: failure_type
        enum: [model_timeout, rate_limited, service_unavailable, invalid_input, internal_error]
      - field: recoverable
        type: boolean
```

---

## 10. Security Protocol

### 10.1 mTLS Configuration

| Parameter | Value |
|---|---|
| TLS version | 1.3 |
| Certificate authority | Internal PKI (Vault PKI engine) |
| Certificate rotation | Every 90 days, auto-renewed by sidecar |
| Client cert required | Yes (mutual TLS) |
| Cipher suites | TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256 |
| Certificate SAN | `spiffe://revenue.acme.com/agent/{agent_id}` |

**SPIFFE identity format:**
```
spiffe://revenue.acme.com/agent/deal-scorer-v2
spiffe://revenue.acme.com/agent/qualification-engine-v1
spiffe://revenue.acme.com/system/orchestrator
```

### 10.2 NATS Auth Tokens/Users

```
# NATS resolver config
accounts: {
  revenue_prod: {
    users: [
      { user: "deal-scorer-v2", token: "$AGENT_NATS_TOKEN", permissions: { publish: { allow: ["revenue.prod.deal.*.scored", "revenue.prod.deal.*.scoring.failed", "revenue.prod.agent.deal-scorer-v2.heartbeat"] }, subscribe: { allow: ["revenue.prod.deal.*.created", "revenue.prod.deal.*.scoring.request"] } } },
      { user: "orchestrator", token: "$ORCHESTRATOR_TOKEN", permissions: { publish: { allow: [">"] }, subscribe: { allow: [">"] } } },
      { user: "simulation-harness", token: "$SIM_TOKEN", permissions: { publish: { allow: ["revenue.dev.>", "revenue.staging.>"] }, subscribe: { allow: ["revenue.dev.>", "revenue.staging.>"] } } }
    ],
    default_permissions: { publish: { deny: [">"] }, subscribe: { deny: [">"] } }
  }
}
```

**Token storage:** Tokens are stored in Vault/KV and injected as environment variables at container start. Never committed to version control.

### 10.3 KV Access Control Enforcement

```yaml
# NATS KV Store ACL
kv_buckets:
  scoring:
    write: [deal-scorer-v2, scoring-engine-v1]
    read: [deal-scorer-v2, scoring-engine-v1, deal-router-v1, orchestrator]
  deal-state:
    write: [state-manager-v1, orchestrator]
    read: [">"]  # all agents can read deal state
  agent-manifests:
    write: [orchestrator, config-manager-v1]
    read: [">"]
  customer:
    write: [data-enrichment-v1]
    read: [">"]
```

### 10.4 Audit Event Format

Every sensitive operation MUST produce an audit event:

```json
{
  "audit_version": "1.0",
  "audit_id": "aud_9f8e7d6c",
  "timestamp": "2026-06-24T14:30:00.123Z",
  "action": "kv.write",
  "actor": {
    "type": "agent",
    "id": "deal-scorer-v2",
    "spiffe_id": "spiffe://revenue.acme.com/agent/deal-scorer-v2"
  },
  "resource": {
    "type": "kv_bucket",
    "bucket": "scoring",
    "key": "d_7a3f"
  },
  "result": "success",
  "detail": {
    "old_value_hash": "sha256:aaaa...",
    "new_value_hash": "sha256:bbbb..."
  },
  "trace_id": "tr_d4e5f6a7b8c9"
}
```

**Audit-worthy actions:**
| Action | Description |
|---|---|
| `kv.read` | Read from KV store (sensitive buckets only) |
| `kv.write` | Write to KV store |
| `kv.delete` | Delete from KV store |
| `nats.publish` | Publish a message |
| `nats.subscribe` | Subscribe to a subject |
| `agent.start` | Agent started |
| `agent.stop` | Agent stopped |
| `agent.failure` | Agent failed |
| `config.change` | Configuration changed |
| `approval.grant` | Human approved a request |
| `approval.deny` | Human denied a request |
| `escalation.trigger` | Escalation raised |
| `contract.sign` | Contract was signed |
| `deal.void` | Deal was voided (compensation) |

**Audit storage:** Audit events are published to `revenue.{env}.system.audit.{action}` and stored in an immutable audit log (AWS CloudTrail or equivalent) with 7-year retention.

---

## Appendix A: Agent Inventory (All 108 Agents)

| ID | Division | Criticality | LLM Tier | Key Subjects |
|---|---|---|---|---|
| deal-ingress-v1 | ingestion | p1 | none | deal.created |
| deal-router-v1 | orchestration | p1 | none | deal.*.scored, deal.*.qualified, deal.*.created |
| data-enrichment-v1 | ingestion | p2 | sonnet | customer.enriched |
| deal-scorer-v2 | qualification | p1 | sonnet | deal.*.scored |
| qualification-engine-v1 | qualification | p1 | opus | deal.*.qualified, deal.*.disqualified |
| meeting-scheduler-v1 | discovery | p2 | sonnet | meeting_scheduled.booked |
| meeting-intelligence-v2 | discovery | p1 | opus | meeting_insight.extracted |
| value-estimator-v2 | discovery | p1 | opus | value.estimated |
| strategy-advisor-v1 | discovery | p2 | opus | strategy.developed |
| email-composer-v1 | engagement | p2 | sonnet | email.sent |
| email-analyzer-v1 | intelligence | p2 | sonnet | email.opened, email.replied |
| contract-engine-v2 | contracting | p1 | sonnet | contract_sent.delivered |
| contract-signature-watcher-v1 | contracting | p1 | none | contract_sent.signed |
| winloss-analyzer-v1 | winloss | p2 | opus | winloss.analyzed |
| forecast-engine-v1 | forecasting | p1 | sonnet | forecast.updated |
| pipeline-snapshotter-v1 | pipeline | p2 | none | pipeline.snapshotted |
| approval-router-v1 | human_interface | p1 | none | human.approval.* |
| escalation-agent-v1 | human_interface | p1 | haiku | human.escalation.* |
| notification-delivery-v1 | human_interface | p3 | none | human.notification.* |
| deal-stale-watcher-v1 | orchestration | p1 | haiku | escalation.triggered |
| config-manager-v1 | orchestration | p1 | none | config.reloaded |
| saga-coordinator-v1 | orchestration | p1 | none | saga.* |
| circuit-breaker-watcher-v1 | orchestration | p2 | haiku | circuit_breaker.* |
| playbook-manager-v1 | intelligence | p3 | opus | playbook.updated |
| ... (108 total) |

---

## Appendix B: Default Timeout Configuration

| Parameter | Default | Per-agent override |
|---|---|---|
| NATS message ack wait | 30s | manifest.sla.p95_latency_ms × 2 |
| NATS reconnect interval | 2s | — |
| NATS max reconnect attempts | 60 | — |
| Consul health check interval | 15s | manifest.health.heartbeat_interval_seconds |
| Consul deregister after | 3m | — |
| Heartbeat dead threshold | 45s (3× interval) | — |
| Heartbeat purge threshold | 90s (6× interval) | — |
| Graceful shutdown drain | 30s | manifest.shutdown.graceful_timeout_seconds |
| Saga commit timeout | 60s | — |
| Circuit breaker window | 60s | — |
| DLQ retention | 90d | — |
| Audit retention | 7yr | — |

---

## Appendix C: NATS Stream Configuration

```yaml
# Stream: revenue-events
subjects:
  - "revenue.prod.deal.>"
  - "revenue.prod.system.>"
  - "revenue.prod.agent.>"
retention: limits       # remove after max_age or max_msgs
max_age: 7d
max_msgs: 10000000
max_bytes: 50GB
storage: file
replicas: 3
ack: true
discard: old            # drop oldest when hitting limits
duplicate_window: 2m    # Nats-Msg-Id dedup window

# Stream: revenue-human-inbox
subjects:
  - "revenue.prod.human.>"
retention: workqueue    # remove on ack (each human consumes once)
max_age: 30d
max_msgs: 1000000
storage: file
replicas: 3
ack: true

# Stream: revenue-dead-letter
subjects:
  - "revenue.prod.dead.>"
retention: limits
max_age: 90d
max_msgs: 10000000
storage: file
replicas: 3
```

---

*End of specification. This document is the single source of truth for the inter-agent communication layer of the AI-Powered Revenue Operating System (108 agents). All implementation must conform to the schemas, conventions, and protocols defined above.*
