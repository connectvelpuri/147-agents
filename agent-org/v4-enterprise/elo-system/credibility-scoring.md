# ELO Credibility Scoring System V2.0

**Status:** COMPLETE (9.5+)
**Purpose:** Source and content credibility evaluation

## Credibility Score Formula

```
Credibility = 0.30 * Authority + 0.25 * Accuracy + 0.20 * Consistency + 0.15 * Recency + 0.10 * Peer Review
```

### Authority (30%)
| Score | Criteria |
|-------|----------|
| 10/10 | Official standard / regulated body |
| 8-9/10 | Peer-reviewed journal / established institution |
| 6-7/10 | Industry expert / recognized practitioner |
| 4-5/10 | Domain blog / self-published with references |
| 1-3/10 | Unknown / unverified source |
| 0/10 | Known unreliable source |

### Accuracy (25%)
| Score | Criteria |
|-------|----------|
| 10/10 | Verified by 3+ independent sources |
| 8-9/10 | Verified by 2 independent sources |
| 6-7/10 | Verified by 1 independent source |
| 4-5/10 | Self-consistent but unverified |
| 1-3/10 | Contains known errors |
| 0/10 | Factually incorrect |

### Consistency (20%)
- Cross-reference with existing knowledge base
- Temporal consistency (doesn't contradict earlier findings)
- Internal consistency (no self-contradictions)
- Domain consistency (aligns with domain norms)

### Recency (15%)
| Age | Score |
|-----|-------|
| < 3 months | 10/10 |
| 3-6 months | 8/10 |
| 6-12 months | 6/10 |
| 1-2 years | 4/10 |
| > 2 years | 2/10 |

### Peer Review (10%)
| Reviews | Score |
|---------|-------|
| 5+ positive reviews from other agents | 10/10 |
| 2-4 positive reviews | 7/10 |
| 1 positive review | 5/10 |
| Mixed reviews | 3/10 |
| No reviews | 1/10 |

## Thresholds
- 9.0+: Highly credible — used as primary source
- 7.0-8.9: Credible — used with confidence
- 5.0-6.9: Moderately credible — requires corroboration
- < 5.0: Low credibility — flag for human review
