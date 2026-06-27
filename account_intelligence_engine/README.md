# Account Intelligence Engine — Open-Source Agent

## What It Is
A working, open-source enterprise account intelligence platform built with Python + SQLite.
No proprietary APIs (no Airtable, Notion, Linear, Salesforce required).

## Architecture
```
account_intelligence_engine/
├── agent.py                    # Main orchestrator — run this
├── modules/
│   ├── database.py             # SQLite schema (6 tables)
│   ├── rag.py                  # TF-IDF RAG search (no deps)
│   └── analytics.py            # Opportunity scoring engine
├── data/
│   ├── intel.db                # SQLite database (populated)
│   └── latest_report.md        # Latest generated report
└── notebooks/
    └── account_intel_analytics.ipynb
```

## Commands

### Run the agent
```
cd C:\Users\Lenovo\sovereign_crm_vault\account_intelligence_engine
python agent.py
```

### Launch Jupyter notebook
```
jupyter notebook notebooks/account_intel_analytics.ipynb
```

### Search intel via RAG
The agent.py demo shows RAG queries. Modify the `queries` list in agent.py or use the notebook.

## What's In The Database

| Table | Records | Description |
|-------|---------|-------------|
| accounts | 5 | Company profiles with research JSON |
| contacts | 48 | Leadership / decision-makers |
| pain_points | 54 | Identified pain points |
| intelligence_feed | 45 | News & events |
| transformation_signals | 51 | Digital transformation signals |

## MCP Servers (configured for next session)
Two open-source MCP servers are configured in `~/.hermes/config.yaml`:

1. **intel_db** — SQLite database access via `uvx mcp-server-sqlite`
   - Tools: `mcp_intel_db_read_query`, `mcp_intel_db_write_query` etc.
   
2. **filesystem** — File operations via `npx @modelcontextprotocol/server-filesystem`
   - Tools: `mcp_filesystem_read_file`, `mcp_filesystem_write_file`
   - Root: `C:\Users\Lenovo\sovereign_crm_vault`

## Cron Automation
- **Weekly refresh** every Monday 9AM (job_id: 2bedb5f0e1c1)
- Runs agent.py, pulls fresh news via web_search, delivers summary

## 5 Target Accounts — Opportunity Scores
| Company | Score | Priority | Key SAP Angle |
|---------|-------|----------|--------------|
| BFW | 100/100 | HIGH | S/4HANA RISE renewal, Hosur smart plant |
| Biological E | 100/100 | HIGH | S/4HANA migration in progress |
| Ace Designers | 93/100 | HIGH | Post-merger IT consolidation, new CIO |
| Pothys | 92/100 | HIGH | IPO-bound, needs clean core systems |
| Muthoot Group | 85/100 | HIGH | $300M IPO, in-house IT can be supplemented |

## Task B & C Ready
The engine architecture supports all 138 steps from the original spec.
Same SQLite schema extends to competitors (Task B) and deal tracking (Task C).
