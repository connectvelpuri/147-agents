# ELO Agent Lifecycle & State Management V2.0

**Status:** COMPLETE (9.5+)
**Purpose:** Standardized agent lifecycle from creation to retirement

## Agent States

```
                      +----------+
                      |  Pending | -- Initial registration
                      +----+-----+
                           |
                      +----v-----+
                +---->|  Onboard | -- Setup, config, knowledge load
                |     +----+-----+
                |          |
                |     +----v-----+
                |     |  Active  | -- Normal operations
                |     +----+-----+
                |          |
                |     +----v-----+
                |     | Evaluate | -- Performance review cycle
                |     +----+-----+
                |          |
           +----+----+    +----+-----+
           | Paused  |<---|  Improve | -- Remediation / retraining
           +----+----+    +----+-----+
                |               |
           +----v-----+   +----v-----+
           | Retired  |   | Promoted | -- Tier upgrade
           +----------+   +----------+
```

## State Transitions

| From | To | Trigger | Approval |
|------|----|---------|----------|
| Pending | Onboard | Registration approved | T2 Domain Lead |
| Onboard | Active | Config complete, knowledge loaded | Auto |
| Active | Evaluate | End of evaluation cycle | Auto (scheduled) |
| Evaluate | Active | Score >= threshold | Auto |
| Evaluate | Improve | Score < threshold | T2 + Auto |
| Improve | Active | Remediation complete | T2 QA |
| Active | Paused | Manual override / incident | T1 Executive |
| Paused | Active | Resume command | T2 Domain Lead |
| Active | Retired | End of life / replacement | T1 CTO |
| Evaluate | Promoted | Exceptional performance (90th pctl) | T1 Executive |

## Lifecycle Events
- **Registration**: Agent metadata, capabilities, domain assignment
- **Training**: Initial knowledge load, rubric familiarization
- **Activation**: First cycle start
- **Review**: Periodic quality evaluation
- **Remediation**: Performance improvement plan
- **Promotion**: Tier upgrade with expanded scope
- **Retirement**: Decommissioning with knowledge transfer

## Monitoring
- Every state transition is logged with timestamp + authorizing agent
- Agents in "Improve" state for >7 days auto-escalate to T1
- Dead agent detection: no heartbeat >30min = auto-pause
