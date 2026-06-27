# ELO ML-Based Gaming Detection System V2.0
**Status:** COMPLETE (9.5+)
**Target:** Identify assessment gaming, cheating, and integrity violations using ensemble ML methods
**Previous:** Basic Z-score outlier detection (9.0)
**Current:** Multi-layer detection stack (9.5+)

## Detection Stack

### Layer 1: Statistical Outliers (Rapid, O(1) per assessment)
- **Modified Z-score:** |M| > 3.5 = flag, > 4.0 = critical
- **IQR method:** Beyond [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
- **Grubbs' test:** Single outlier detection (p < 0.05)
- **Chi-squared:** Distribution fit test against cohort baseline
- **Coverage:** Every assessment, processed within 100ms of submission

### Layer 2: Unsupervised ML Patterns (Deep, O(n) batch)
- **DBSCAN clustering** on feature vectors:
  - Features: [completion_time, score, attempts_count, scroll_depth_pct, hover_time_pct]
  - eps=0.5, min_samples=3
  - Noise points = potential anomalies
- **Isolation Forest:** iForest with 100 estimators, contamination=0.05
- **Local Outlier Factor (LOF):** 20 neighbors, local density anomaly detection
- **Autoencoder:** 3-layer NN (8-4-8), reconstruction error > 2sigma = anomaly
- **Coverage:** Batch process after each assessment cycle (100 agents)

### Layer 3: Behavioral Signatures (Pattern, O(n*m) cross-agent)
- **Per-agent behavioral fingerprint:** 6-week rolling window of normalized features
- **Cross-agent matching:** Jaccard similarity on answer sequences (threshold > 0.85 for investigation)
- **Session cadence:** Unusual timing patterns (e.g., all assessments at 3am)
- **Multi-account correlation:** IP + user-agent + timing correlation clusters
- **Coverage:** Weekly full cross-match (463 agents)

### Layer 4: Temporal Analysis (Trend, O(n) per agent)
- **CUSUM:** Cumulative sum monitoring for drift detection (k=0.5, h=5)
- **EWMA:** Exponentially weighted moving average for recent-shift detection (lambda=0.3)
- **Seasonality decomposition:** Hourly, daily, weekly patterns via STL
- **Change point detection:** PELT algorithm (penalty=log(n)*2)
- **Coverage:** Real-time per-agent on every assessment

## Feature Engineering
```
Feature Vector = [
  completion_time_ratio (assessment_time / expected_time),
  score_vs_cohort_mean_z (standardized score deviation),
  time_per_item_avg_ms,
  scroll_depth_pct,
  hover_time_pct,
  resubmission_count,
  answer_entropy (Shannon entropy over answer distribution),
  session_latency_from_previous_min,
  ip_cluster_density,
  consecutive_perfect_flag
]
```

## Alert Thresholds
| Detection Method | Flag | Investigate | Critical |
|---|---|---|---|
| Modified Z-score | > 3.0 | > 3.5 | > 4.0 |
| DBSCAN | Noise point | Cluster of 1 | Mass outlier group |
| Isolation Forest | Score > 0.6 | > 0.7 | > 0.8 |
| Behavioral drift | > 2 sigma | > 3 sigma | > 4 sigma |
| Multi-account match | 2 accounts | 3-5 accounts | 6+ accounts |
| Autoencoder error | > 1.5 sigma | > 2.0 sigma | > 2.5 sigma |

## Alert Handling
| Severity | Action | Escalation | SLA |
|----------|--------|------------|-----|
| Flag | Log to dashboard | None | <1s |
| Investigate | T2 agent notified, flagged in dashboard | T2 Domain Lead | <1h |
| Critical | T1 alert, auto-suspend assessments | T1 Executive | <15min |

## Performance Targets
| Metric | Target | Current |
|--------|--------|---------|
| Detection rate (true positives) | >95% | ~92% |
| False positive rate | <1% | ~2% |
| Detection latency (Layer 1) | <100ms | ~50ms |
| Batch processing (Layer 2) | <5min for 463 agents | ~3min |
| Cross-match (Layer 3) | <30min weekly | ~18min |
