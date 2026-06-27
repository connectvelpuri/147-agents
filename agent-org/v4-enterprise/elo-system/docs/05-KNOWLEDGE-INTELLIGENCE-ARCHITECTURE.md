# ELO DOCUMENT 5: KNOWLEDGE INTELLIGENCE ARCHITECTURE
# Enterprise Learning Operations — How Knowledge Is Processed

---

## Knowledge Processing Layers

### Layer 1: Raw Intelligence
**Source:** External feeds, search results, RSS, API calls
**Format:** Raw text, URLs, metadata
**Storage:** knowledge-base/raw/
**Retention:** 30 days

### Layer 2: Classified Intelligence
**Source:** Layer 1 after classification
**Format:** Tagged content with domain, type, level, impact
**Storage:** knowledge-base/classified/
**Retention:** 90 days

### Layer 3: Curated Intelligence
**Source:** Layer 2 after ranking and filtering
**Format:** Ranked, deduplicated, quality-scored content
**Storage:** knowledge-base/curated/
**Retention:** 180 days

### Layer 4: Learning Packs
**Source:** Layer 3 after packaging for specific roles
**Format:** Role-specific learning packets with action items
**Storage:** learning-packs/[domain]/[date]/
**Retention:** 365 days

### Layer 5: Applied Knowledge
**Source:** Layer 4 after agent application
**Format:** Learning application logs with output improvements
**Storage:** knowledge-base/applied/
**Retention:** Permanent

---

## Knowledge Quality Scoring

Each intelligence item receives a quality score (0-100):

| Factor | Weight | Scoring |
|--------|--------|---------|
| Recency | 25% | 0-7 days: 100, 7-30 days: 70, 30-90 days: 40, 90+: 10 |
| Source Credibility | 20% | Official: 100, Expert: 85, Community: 70, Unknown: 30 |
| Practical Applicability | 25% | Can apply today: 100, this week: 70, this sprint: 40, theoretical: 10 |
| Role Relevance | 20% | Exact match: 100, related: 70, tangential: 40, unrelated: 0 |
| Actionability | 10% | Clear steps: 100, general guidance: 60, vague: 20 |

**Minimum threshold:** 60/100 to pass to operational agents

---

## Knowledge Graph Structure

```
Domain → Competency → Skill → Knowledge Item → Source
    ↓
Related Domain → Related Competency → Cross-Domain Learning
```

### Example:
```
Frontend → React Performance → Code Splitting → [Article: React.lazy patterns] → [Source: official React docs]
    ↓
Backend → API Performance → Response Optimization → [Article: caching patterns] → [Source: Redis docs]
```

---

## Knowledge Lifecycle

```
Discovery → Classification → Validation → Curation → Distribution → Application → Measurement → Archive
    ↑                                                                              │
    └──────────────────────── Feedback Loop ───────────────────────────────────────┘
```

1. **Discovery:** Tier 3 scanner finds new content
2. **Classification:** Content tagged with domain, type, level
3. **Validation:** Source verified, quality scored
4. **Curation:** Content ranked, filtered, summarized
5. **Distribution:** Learning packs delivered to agents
6. **Application:** Agent applies learning to work
7. **Measurement:** Output improvement measured
8. **Archive:** Knowledge stored for future reference
9. **Feedback:** Application results inform future discovery

---

## Knowledge Storage Structure

```
elo-system/knowledge-base/
├── raw/                    # Raw intelligence (30-day retention)
│   ├── [domain]/
│   │   └── [date]/
│   │       └── [source]-[timestamp].json
├── classified/             # Classified intelligence (90-day retention)
│   └── [domain]/
│       └── [date]/
├── curated/                # Curated intelligence (180-day retention)
│   └── [domain]/
│       └── [date]/
├── applied/                # Applied knowledge (permanent)
│   └── [domain]/
│       └── [agent-id]/
└── archive/                # Archived knowledge
    └── [year]/
        └── [quarter]/
```

