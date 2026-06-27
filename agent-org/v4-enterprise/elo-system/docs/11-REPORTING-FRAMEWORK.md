# ELO DOCUMENT 11: REPORTING FRAMEWORK
# Enterprise Learning Operations — How Reports Flow

---

## Report Types

### Daily Reports
| Report | Author | Audience | Frequency | Format |
|--------|--------|----------|-----------|--------|
| Learning Pack | Tier 3 | Operational Agent | 3x/day | JSON |
| Agent Self-Report | Operational Agent | Tier 2 Lead | 3x/day | JSON |
| Domain Summary | Tier 2 Lead | Tier 1 Director | Daily | Markdown |
| Enterprise Pulse | Tier 1 Director | Founder | Daily (20:00) | Text |

### Weekly Reports
| Report | Author | Audience | Frequency | Format |
|--------|--------|----------|-----------|--------|
| Domain Performance | Tier 2 Lead | Tier 1 Director | Weekly | Markdown |
| Certification Status | Tier 2-23 | All Tier 1 | Weekly | Markdown |
| Cross-Domain Insights | Tier 2-25 | All Tier 1 | Weekly | Markdown |
| Stagnation Report | Tier 2-25 | Tier 1 + Founder | Weekly | Markdown |

### Monthly Reports
| Report | Author | Audience | Frequency | Format |
|--------|--------|----------|-----------|--------|
| L&D Metrics Summary | Tier 1 Director | Founder | Monthly | Markdown |
| Technology Radar | Tier 2-24 | All Tier 1 | Monthly | Markdown |
| Certification ROI | Tier 2-23 | Founder | Monthly | Markdown |
| L&D System Health | Tier 2-25 | All Tier 1 | Monthly | Markdown |

### Quarterly Reports
| Report | Author | Audience | Frequency | Format |
|--------|--------|----------|-----------|--------|
| Learning ROI Report | Tier 1 Council | Founder | Quarterly | Full doc |
| Competency Maturation | Tier 1 Council | Founder | Quarterly | Full doc |
| L&D Self-Assessment | Tier 2-25 | All Tier 1 | Quarterly | Full doc |
| Strategic L&D Review | Tier 1 Council | Founder | Quarterly | Full doc |

---

## Report Delivery Channels

| Channel | Reports | Delivery Method |
|---------|---------|-----------------|
| Terminal | Daily Pulse, Quick Status | Direct text output |
| File System | All reports | elo-system/reports/ |
| Cron Job | Daily Pulse | Scheduled delivery |
| Dashboard | Real-time metrics | elo-system/dashboards/ |

---

## Report Quality Standards

1. Every report must include a timestamp
2. Every report must include the author (agent ID)
3. Every report must be actionable (next steps clear)
4. Every report must be concise (no filler)
5. Every report must include data (not just narrative)
6. Every report must be archived (for trend analysis)
7. Every report must include escalation items if any
8. Every report must follow the defined template

