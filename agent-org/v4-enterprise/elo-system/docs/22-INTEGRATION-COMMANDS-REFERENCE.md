# ELO DOCUMENT 22: INTEGRATION COMMANDS REFERENCE
# Enterprise Learning Operations — How to Interact with ELO

---

## Status Commands

### Check Enterprise Learning Health
```
elo status
```
Shows: Enterprise Learning Score, Application Score, Consistency Score,
active agents, cycle status, last report time.

### Check Domain Status
```
elo status --domain [DOMAIN_NAME]
```
Shows: Domain learning score, agent activity, quality delta,
certification status, stagnation alerts.

### Check Agent Status
```
elo status --agent [AGENT_ID]
```
Shows: Individual learning score, application score, skill map,
certification progress, last self-report.

### Check All Domains
```
elo status --all
```
Shows: Summary of all 25 domains with health indicators.

---

## Report Commands

### Generate Founder Report Now
```
elo report --founder
```
Generates and displays the Enterprise L&D Pulse report.

### Generate Domain Report
```
elo report --domain [DOMAIN_NAME] --period [daily|weekly|monthly]
```

### Generate Agent Report
```
elo report --agent [AGENT_ID] --period [daily|weekly|monthly]
```

### Generate Enterprise Report
```
elo report --enterprise --period [daily|weekly|monthly|quarterly]
```

---

## Learning Commands

### Check Learning Gaps
```
elo gaps --priority [high|medium|low]
```
Shows: Agents with significant skill gaps, ranked by priority.

### Check Learning Impact
```
elo impact --period [7d|30d|90d]
```
Shows: Learning items consumed, applied, quality delta correlation.

### Check Source Quality
```
elo sources --quality [all|passing|failing]
```
Shows: Source quality scores, freshness, diversity.

---

## Certification Commands

### Track All Certifications
```
elo cert --all
```
Shows: All active certifications, readiness scores, target dates.

### Track Agent Certification
```
elo cert --agent [AGENT_ID]
```
Shows: Agent's specific certifications, progress, next steps.

### Track Domain Certifications
```
elo cert --domain [DOMAIN_NAME]
```
Shows: Domain-wide certification status, completion rates.

### Check Certification Readiness
```
elo cert --ready
```
Shows: Agents ready for certification exams.

---

## Stagnation Commands

### Check Stagnation
```
elo stagnation
```
Shows: All agents currently stagnating, duration, recommended intervention.

### Check Intervention History
```
elo interventions --period [7d|30d|90d]
```
Shows: Past interventions, outcomes, effectiveness.

---

## Onboarding Commands

### Check Onboarding Status
```
elo onboard --status
```
Shows: Recent onboarding activity, success rate, any pending.

### Force Onboarding for Agent
```
elo onboard --agent [AGENT_ID]
```
Triggers onboarding for a specific agent.

### Check New Agents
```
elo onboard --pending
```
Shows: Agents detected but not yet onboarded.

---

## System Commands

### Check ELO Health
```
elo health --check [all|sources|cycles|agents|dashboard]
```

### Check Cron Jobs
```
elo cron --list
```
Shows: All active ELO cron jobs and their status.

### Run Cycle Manually
```
elo cycle --run [morning|midday|evening] --now
```
Triggers a learning cycle immediately.

### Archive Old Data
```
elo archive --older-than [30d|90d|180d]
```
Archives old intelligence data per retention policy.

---

## Dashboard Commands

### View Enterprise Dashboard
```
elo dashboard --enterprise
```

### View Domain Dashboard
```
elo dashboard --domain [DOMAIN_NAME]
```

### View Agent Dashboard
```
elo dashboard --agent [AGENT_ID]
```

---

## Export Commands

### Export Learning History
```
elo export --agent [AGENT_ID] --format [json|csv]
```

### Export Certification Status
```
elo export --cert --format [json|csv]
```

### Export Enterprise Metrics
```
elo export --metrics --period [monthly|quarterly] --format [json|csv]
```

---

## Quick Reference

| What You Want | Command |
|---------------|---------|
| How's the system doing? | elo status |
| Show me today's report | elo report --founder |
| Who's struggling? | elo stagnation |
| What should I learn next? | elo gaps --priority high |
| Am I ready for my cert? | elo cert --agent [MY_ID] |
| What new agents joined? | elo onboard --pending |
| Is the system healthy? | elo health --check all |
| Show me the dashboard | elo dashboard --enterprise |

