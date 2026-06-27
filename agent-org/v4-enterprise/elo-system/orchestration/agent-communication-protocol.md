# ELO Agent Communication Protocol V2.0

**Status:** COMPLETE (9.5+)
**Standard:** CrewAI + LangGraph compatible, enterprise-grade
**Purpose:** Standardized inter-agent message exchange with governance

## Protocol Layers

### Layer 1: Transport
| Mechanism | Use Case | Latency | Reliability |
|-----------|----------|---------|-------------|
| Direct call | Same-pod agents (synchronous) | <10ms | 99.999% |
| Message queue (Redis/AMQP) | Cross-pod, async | <50ms | 99.99% |
| Shared knowledge store | Cross-domain, persistent | <100ms | 99.9% |
| Event bus | Broadcast (status changes) | <200ms | 99.9% |

### Layer 2: Message Format
```json
{
  "protocol_version": "2.0",
  "message_id": "msg_<uuid>",
  "timestamp": "2026-06-09T15:00:00Z",
  "source": {
    "agent_id": "T2-207",
    "agent_name": "Security_Domain_Lead",
    "tier": "T2",
    "domain": "security"
  },
  "target": {
    "agent_id": "T1-103",
    "agent_name": "CTO_Agent",
    "tier": "T1"
  },
  "message_type": "alert | query | report | decision | handoff | sync | broadcast",
  "priority": "P1 | P2 | P3 | P4",
  "payload": {},
  "context": {
    "trace_id": "trace_<uuid>",
    "parent_message_id": "msg_<parent_uuid>"
  },
  "governance": {
    "requires_approval": false,
    "compliance_impact": "none | low | medium | high",
    "audit_logged": true
  }
}
```

### Layer 3: Message Types

**Alert** — Notifications requiring attention
```
alert_type: quality_drop | gaming_flag | system_failure | compliance_breach | deadline_risk
severity: info | warning | critical
expected_action: acknowledge | investigate | escalate | auto_resolve
```

**Query** — Information requests between agents
```
query_type: agent_status | metric_history | content_catalog | agent_capability
scope: single_agent | domain | system
time_range: {from, to}
```

**Report** — Periodic status updates, cycle completions
```
report_type: cycle_complete | weekly_summary | domain_health | incident_postmortem
period: {from, to}
payload: {metrics, highlights, action_items[]}
```

**Decision** — Recorded decisions
```
decision_type: scope_change | priority_change | exception_granted | resource_allocation
made_by: agent_id
rationale: string
alternatives_considered: [string]
effective_date: timestamp
expiry_date: timestamp
```

**Handoff** — Escalation or transfer of ownership
```
from_agent: agent_id
to_agent: agent_id
reason: scope_exceeded | tier_escalation | domain_transfer | shift_change
context_snapshot: {state, history[], pending_actions[]}
```

**Sync** — Cross-domain knowledge sync
```
domain: string
knowledge_topics: [{topic, last_updated, checksum, summary}]
sync_type: push | pull | full | delta
```

**Broadcast** — System-wide announcements
```
broadcast_type: policy_change | system_status | scheduled_maintenance | achievement
target_tiers: [T1 | T2 | T3 | all]
requires_acknowledgment: bool
```

## Protocol Rules
1. Every message is acknowledged (ACK/NACK within 5s, auto-retry 3x)
2. Every decision is recorded in decision log (immutable append)
3. Trace IDs propagate through all downstream messages
4. Audit logging is mandatory for governance-impacting messages
5. Priority dictates SLA: P1 <5min, P2 <30min, P3 <2h, P4 <24h
6. Rate limiting: max 100 msg/min per agent, burst 200
7. Message TTL: P1=24h, P2=72h, P3=1week, P4=indefinite
