# ELO Automated Post-Mortem Generation V2.0
**Status:** COMPLETE (9.5+)
**Pattern:** Structured 5 Whys with auto-collected telemetry
**Turnaround target:** 6 hours (auto 2h + human review 4h)

## Pipeline

```
Incident Resolved
       ↓
Auto-collect all telemetry
  - Agent logs (all tool calls + model responses)
  - Error messages and stack traces
  - Heartbeat metrics (last 30min window)
  - Alert timeline from monitoring
  - Runbook execution log (which steps ran, which failed)
  - Checkpoint state (pre/post incident)
       ↓
Incident Classification
  - Type: tool_failure | model_degradation | context_poisoning | permission_error | state_corruption | orchestrator_failure | infrastructure | unknown
  - Severity: P1 (critical) | P2 (high) | P3 (medium) | P4 (low)
  - Scope: single_agent | multi_agent | domain | system
       ↓
Auto-generate timeline
  - Parse timestamps from all data sources
  - Merge into chronological sequence
  - First deviation → first detection → first action → resolution
       ↓
Run 5 Whys Analysis
  - Structured question chain from tool call logs + model responses
  - Root cause classification
  - Contributing factors
       ↓
Generate Draft Post-Mortem
  - Executive summary (Signal → Insight → Action)
  - Timeline
  - 5 Whys chain
  - Contributing factors
  - Action items (auto-linked to tracking system)
  - Runbook update recommendations
       ↓
Human Review
  - T2/T1 review and edit
  - Publish to knowledge base
  - Update runbook if applicable
  - Close loop with action item tracking
       ↓
Action Items Created
  - Auto-linked to Jira/GitHub Issues
  - Assigned to appropriate T2/T1
  - Due date: P1=24h, P2=72h, P3=1 week, P4=next sprint
