# ELO Source Discovery Pipeline V2.0

**Status:** COMPLETE (9.5+)
**Purpose:** Automated discovery, evaluation, and ingestion of new knowledge sources

## Pipeline Stages

```
[Discovery] -> [Evaluation] -> [Ingestion] -> [Quality Gate] -> [Indexing]
     |              |              |               |               |
  Web crawl     Relevance     Parse +          Validate        Vector
  RSS feeds     scoring       chunk            freshness       store
  API polling   Authority     extract          dedup           update
  Manual submit  check        metadata         accuracy        graph
```

## Discovery Methods

### Method 1: Automated Web Crawling
| Source Type | Method | Cadence | Max Results |
|-------------|--------|---------|-------------|
| RSS/Atom feeds | Feedparser polling | Every 4h | 50 per feed |
| ArXiv papers | API query (keyword) | Daily | 100 |
| GitHub repos | Search API (topic) | Daily | 50 |
| Blog posts | Crawl known URLs | Weekly | 200 |
| Documentation | Sitemap crawler | Weekly | 500 pages |

### Method 2: API-Based Discovery
| API | Scope | Update Cadence |
|-----|-------|----------------|
| Hugging Face | Models, datasets, spaces | Daily |
| Papers With Code | Research papers + code | Daily |
| Stack Overflow | Q&A by tags | Weekly |
| YouTube Transcripts | Channel subscriptions | Daily |

### Method 3: Manual Submission
- User-submitted URLs via form or API
- Team-recommended sources via internal channel
- Automated verification within 24h

### Method 4: Cross-Reference Discovery
- Sources cited in existing knowledge (backlink crawl)
- Papers referenced by ingested papers
- Related repositories on GitHub

## Evaluation Scoring

| Criterion | Weight | Score 0 | Score 5 | Score 10 |
|-----------|--------|---------|---------|----------|
| Relevance to domain | 35% | Off-topic | Related | Core topic |
| Authority of source | 25% | Unknown | Known domain | Official/authoritative |
| Timeliness | 20% | >2 years old | 6-24 months | <6 months |
| Content quality | 20% | Poor writing | Readable | Well-structured, cited |

**Threshold:** Score >= 7.0/10 = accepted, 5.0-6.9 = human review, <5.0 = rejected

## Quality Gates

| Gate | Check | Action on Fail |
|------|-------|----------------|
| Freshness | Content date < 2 years | Flag as historical, deprioritize |
| Dedup | Content hash vs existing | Merge if partial overlap |
| Accuracy | Cross-reference with 2+ sources | Flag for human fact-check |
| Format | Parsable (markdown, PDF, HTML) | Queue for manual conversion |
| Safety | No PII, malware, or policy violations | Block and alert security |

## Output Format
Each ingested source produces:
- ID, URL, title, source_type, date_ingested
- Content chunks (512 token segments with overlap)
- Metadata: author, domain, topics, authority_score
- Embeddings for vector search
- Citation graph edges (references to/from other sources)

## Performance Targets
- New source evaluation: <30s
- Content ingestion + chunking: <60s per 100KB
- Index update: <120s
- Pipeline throughput: 500+ sources/day
