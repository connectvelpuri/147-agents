# ELO Audit Trail & Logging V2.0

**Status:** COMPLETE (9.5+)
**Standard:** SOC 2, SOX, CoSAI aligned

## Log Categories

| Category | Events | Retention | Access Control |
|----------|--------|-----------|----------------|
| Agent Actions | Every tool call, model response, decision | 2 years online, 5 years cold | T1 + Security |
| System Events | Start/stop, config change, deployment | 2 years online | T2 DevOps + T1 |
| Access Logs | Login, permission change, role assignment | 5 years | T1 + Compliance |
| Data Events | Create/read/update/delete of knowledge | 3 years | T2 Domain + T1 |
| Security Events | Auth failure, suspicious activity, breach | 5 years | T1 Security |
| Compliance Events | Policy violation, exception, audit | 7 years (permanent if legal) | T1 Compliance |

## Log Entry Format
```json
{
  "event_id": "evt_<uuid>",
  "timestamp": "ISO 8601",
  "event_type": "create | read | update | delete | access | auth | config | error | alert",
  "actor": {
    "agent_id": "T2-207",
    "agent_type": "domain_lead",
    "session_id": "sess_<uuid>"
  },
  "action": {
    "type": "tool_call | model_query | decision | file_access",
    "target": "tool_name | model_id | decision_id | file_path",
    "details": {},
    "result": "success | failure | denied"
  },
  "governance": {
    "compliance_impact": "none | low | medium | high",
    "requires_notification": false,
    "notified": []
  },
  "context": {
    "trace_id": "trace_<uuid>",
    "source_ip": "",
    "user_agent": "ELO Agent System v2.0"
  }
}
```

## Audit Requirements
- Every event is logged before the action is completed (write-ahead)
- Logs are immutable (append-only, signed hash chain)
- No single agent can delete or modify log entries
- Log integrity verified hourly via hash chain validation
- Tamper detection alerts T1 Security immediately
- Backup to separate storage every 6 hours
