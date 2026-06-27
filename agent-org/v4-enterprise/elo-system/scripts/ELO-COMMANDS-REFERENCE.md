# ELO Quick Reference Commands
# How to Interact with Enterprise Learning Operations

## Check System Status
```bash
python3 ~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system/scripts/elo-startup-trigger.py
```

## Onboard New Agents
```bash
python3 ~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system/scripts/elo-onboard-new-agents.py
```

## Check Cron Jobs
```bash
hermes cron list
```

## View Reports
```bash
ls ~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system/reports/daily/
```

## View Knowledge Base
```bash
ls ~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system/knowledge-base/
```

## View Agent Mapping
```bash
cat ~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system/mappings/agent-to-tier2-mapping.json
```

## Run ELO Cycles Manually
- Morning: Ask Hermes "run ELO morning cycle"
- Midday: Ask Hermes "run ELO midday cycle"
- Evening: Ask Hermes "run ELO evening cycle"
- Founder Report: Ask Hermes "generate ELO founder report"

## Check Cron Job Status
The 4 ELO cron jobs run automatically:
- 07:00 IST — Morning intelligence scan
- 13:00 IST — Midday applied learning
- 19:00 IST — Evening reflection
- 20:00 IST — Founder daily pulse

To check: hermes cron list
To pause: hermes cron pause [job_id]
To resume: hermes cron resume [job_id]
