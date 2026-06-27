# ELO DOCUMENT 4: DATA INGESTION ARCHITECTURE
# Enterprise Learning Operations — How Intelligence Flows In

---

## Ingestion Sources (32 Categories)

### Tier 1: Primary Intelligence Sources
| Source | Type | Refresh Rate | Tier 3 Owner |
|--------|------|-------------|--------------|
| Google Search | Web search | Every cycle | Intelligence Scanner |
| Web Search | Web search | Every cycle | Intelligence Scanner |
| GitHub Repositories | Code intelligence | Every cycle | Intelligence Scanner |
| GitHub Issues | Problem intelligence | Every cycle | Practitioner Analyst |
| GitHub Discussions | Community intelligence | Daily | Practitioner Analyst |
| GitHub Release Notes | Tool intelligence | Daily | Intelligence Scanner |
| Official Documentation | Reference intelligence | Daily | Learning Curator |
| Product Release Notes | Vendor intelligence | Daily | Intelligence Scanner |

### Tier 2: Community Intelligence Sources
| Source | Type | Refresh Rate | Tier 3 Owner |
|--------|------|-------------|--------------|
| Reddit | Community intelligence | Every cycle | Practitioner Analyst |
| Stack Overflow | Problem intelligence | Every cycle | Practitioner Analyst |
| Dev.to | Practitioner articles | Daily | Practitioner Analyst |
| Hacker News | Trend intelligence | Every cycle | Intelligence Scanner |
| Medium | Practitioner articles | Daily | Practitioner Analyst |
| Technical Blogs | Expert intelligence | Daily | Intelligence Scanner |
| YouTube Experts | Video intelligence | Daily | Intelligence Scanner |
| Conference Talks | Expert intelligence | Weekly | Intelligence Scanner |
| Technical Podcasts | Audio intelligence | Weekly | Intelligence Scanner |

### Tier 3: Academic & Research Sources
| Source | Type | Refresh Rate | Tier 3 Owner |
|--------|------|-------------|--------------|
| Research Papers | Academic intelligence | Weekly | Intelligence Scanner |
| White Papers | Industry intelligence | Weekly | Intelligence Scanner |
| Academic Publications | Research intelligence | Weekly | Intelligence Scanner |
| Feedly | Aggregated intelligence | Every cycle | Intelligence Scanner |
| RSS Feeds | Subscribed intelligence | Every cycle | Intelligence Scanner |

### Tier 4: Certification & Learning Sources
| Source | Type | Refresh Rate | Tier 3 Owner |
|--------|------|-------------|--------------|
| AWS Certification | Certification intelligence | Weekly | Learning Curator |
| Google Cloud Certification | Certification intelligence | Weekly | Learning Curator |
| CNCF Certification | Certification intelligence | Weekly | Learning Curator |
| Coursera | Course intelligence | Weekly | Learning Curator |
| Udemy | Course intelligence | Weekly | Learning Curator |
| Pluralsight | Course intelligence | Weekly | Learning Curator |

### Tier 5: Production Intelligence Sources
| Source | Type | Refresh Rate | Tier 3 Owner |
|--------|------|-------------|--------------|
| Production Incidents | Failure intelligence | Real-time | Practitioner Analyst |
| Bug Reports | Defect intelligence | Daily | Practitioner Analyst |
| Postmortems | Learning intelligence | Weekly | Practitioner Analyst |
| Implementation Failures | Anti-pattern intelligence | Weekly | Practitioner Analyst |
| Architecture Case Studies | Design intelligence | Weekly | Practitioner Analyst |
| Practitioner War Stories | Experience intelligence | Weekly | Practitioner Analyst |
| User Complaints | Customer intelligence | Daily | Practitioner Analyst |
| Industry Communities | Ecosystem intelligence | Daily | Intelligence Scanner |

---

## Ingestion Pipeline

```
Source → Fetch → Classify → Rank → Filter → Summarize → Package → Deliver
                                                              │
                                                              ▼
                                                     Tier 2 Domain Leads
                                                              │
                                                              ▼
                                                     Operational Agents
```

### Pipeline Stages

1. **Fetch** — Retrieve content from source (API, RSS, scrape, search)
2. **Classify** — Assign domain, role relevance, content type
3. **Rank** — Score by timeliness, quality, actionability (1-10)
4. **Filter** — Remove stale (>7 days), generic, motivational, repeated content
5. **Summarize** — Extract key insights, actionable items, implementation guidance
6. **Package** — Format as learning pack with source attribution
7. **Deliver** — Push to assigned Tier 2 lead and operational agents

---

## Source Quality Standards

### What Gets Through
- Current (published within 7 days)
- Practical (directly applicable to work)
- Role-specific (relevant to assigned agent)
- Source-backed (attributed to credible source)
- Actionable (can be applied in same work cycle)
- High-signal (more than 80% useful content)
- Immediately useful (not theoretical or abstract)

### What Gets Filtered Out
- Generic summaries without specificity
- Motivational filler without substance
- Content older than 7 days (unless foundational)
- Repeated recommendations already delivered
- Content requiring prerequisites not yet learned
- Content requiring tools not yet available
- Content without source attribution
- Content without practical application path

---

## Intelligence Classification Taxonomy

```
Domain: [Frontend|Backend|QA|DevOps|SRE|Architecture|CRM|ERP|HR|Finance|...]
Type:   [Trend|Release|Pattern|Lesson|Certification|Tool|Framework|Practice]
Level:  [Beginner|Intermediate|Advanced|Expert]
Impact: [Low|Medium|High|Critical]
Urgency:[Can-Wait|This-Week|This-Sprint|Immediate]
Source: [Official|Community|Academic|Practitioner|Vendor]
```

