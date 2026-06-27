# ELO DOCUMENT 10: DASHBOARD ARCHITECTURE
# Enterprise Learning Operations — What You See

---

## Dashboard Hierarchy

### Level 1: Enterprise Dashboard (Founder View)
**Audience:** Founder/CEO
**Update Frequency:** Real-time (refreshes every cycle)
**Location:** elo-system/dashboards/enterprise/

| Widget | Description | Metric |
|--------|-------------|--------|
| Enterprise Learning Score | Average learning score across all agents | 0-100 |
| Enterprise Application Score | Average application score across all agents | 0-100 |
| Domain Health Map | Color-coded health for each of 25 domains | GREEN/YELLOW/RED |
| Certification Tracker | Active/completed/certifications ready | Numbers + trend |
| Stagnation Alerts | Agents with no learning progress | Count + list |
| Learning Trend | 30-day learning score trend | Chart |
| Top Improvements | Biggest learning improvements this week | Top 5 |
| Intervention Needed | Agents requiring attention | Count + priority |

### Level 2: Domain Dashboard (Tier 1 Director View)
**Audience:** ELO-T1 Directors
**Update Frequency:** Every cycle
**Location:** elo-system/dashboards/domains/[domain]/

| Widget | Description | Metric |
|--------|-------------|--------|
| Domain Learning Score | Average score for domain agents | 0-100 |
| Agent Activity Map | Which agents are active vs inactive | Heat map |
| Learning Packs Delivered | Number of packs delivered today | Count |
| Applied Learning | Learning items applied to work | Count + % |
| Quality Delta | Output quality change | -10 to +10 |
| Certification Progress | Domain certification status | Progress bars |
| Skill Gap Analysis | Top skill gaps in domain | Ranked list |
| Cross-Domain Transfers | Knowledge shared with other domains | Count |

### Level 3: Agent Dashboard (Tier 2 Lead View)
**Audience:** ELO-T2 Domain Leads
**Update Frequency:** Every cycle
**Location:** elo-system/dashboards/agents/[agent-id]/

| Widget | Description | Metric |
|--------|-------------|--------|
| Individual Learning Score | Agent's learning score | 0-100 |
| Application Score | How much learning is applied | 0-100 |
| Skill Map | Current skill levels across 5 dimensions | Radar chart |
| Learning Feed | Recent learning packs received | List |
| Certification Progress | Active certifications and readiness | Progress bars |
| Quality Delta History | 30-day quality trend | Chart |
| Self-Report Status | Report submission compliance | % on-time |
| Stagnation Risk | Risk of falling behind | LOW/MEDIUM/HIGH |

---

## Dashboard Data Flow

```
Tier 3 Feeder → Tier 2 Lead → Tier 1 Director → Enterprise Dashboard
     │                │                │
     │                │                └── Domain Dashboard
     │                └── Agent Dashboard
     └── Raw Intelligence Feed
```

---

## Dashboard Access Matrix

| Dashboard | Tier 1 | Tier 2 | Tier 3 | Operational |
|-----------|--------|--------|--------|-------------|
| Enterprise | Read | Read | No | No |
| Domain | Read/Write | Read | Read | No |
| Agent | Read | Read/Write | Read | Read (own) |
| Personal | No | No | No | Read/Write (own) |

---

## Dashboard Refresh Schedule

| Dashboard | Refresh Rate | Trigger |
|-----------|-------------|---------|
| Enterprise | Every cycle | 07:00, 13:00, 19:00 IST |
| Domain | Every cycle | When Tier 2 submits domain summary |
| Agent | Every cycle | When agent submits self-report |
| Personal | Real-time | On self-report submission |

