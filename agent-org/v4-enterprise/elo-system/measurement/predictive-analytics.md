# ELO Predictive Analytics Engine V2.0
**Status:** COMPLETE (9.5+)
**Standard:** Enterprise L&D forecasting (SAP SuccessFactors caliber)
**Purpose:** Forecast Leading Health Index, completion risks, skill gap velocity, and content demand

## Model Inventory

### 1. LHI Forecast (ARIMA + Prophet)
| Property | Value |
|----------|-------|
| **Input** | 12-week LHI history (weekly) |
| **Output** | 4-week forecast with 80/95% confidence intervals |
| **Model** | Auto-ARIMA with AIC minimization + Prophet ensemble |
| **Seasonality** | Weekly (weekday effects) + Monthly (cycle effects) |
| **MAE target** | <3 pts |
| **MAPE target** | <5% |
| **Confidence bands** | Bootstrap resampling (N=1000) |

### 2. Completion Risk (Logistic Regression)
| Property | Value |
|----------|-------|
| **Input** | Agent features: engagement_t0-2w, relevance_score, pre_test, domain, role |
| **Output** | P(non-completion) per agent per cycle |
| **Threshold** | >0.7 = "At Risk" (auto-flag to T2) |
| **AUC target** | >0.85 |
| **Precision target** | >0.80 |
| **Retraining** | Every cycle end, rolling 12-cycle window |

### 3. Skill Gap Velocity (Linear + Exponential)
| Property | Value |
|----------|-------|
| **Input** | Skill gap delta over time per domain |
| **Output** | Projected time-to-competency per domain |
| **Model** | Linear (steady state) + Exponential (if growth accelerating) |
| **Accuracy** | <2 weeks error |
| **Use** | Identify bottleneck domains, planning hiring vs training |

### 4. Content Demand Forecasting
| Property | Value |
|----------|-------|
| **Input** | Usage trend per domain, seasonality, new agent onboarding rate |
| **Output** | Content demand volume next 2 cycles |
| **Model** | Seasonal ARIMA with exogenous regressors |
| **Error target** | <15% |
| **Use** | Cache pre-generation, T2 content allocation |

## Feature Store
All models share a common feature engineering pipeline:
```
Features extracted per agent per cycle:
  - engagement_score (0-100): completeness score across 5 dimensions
  - relevance_score (0-10): content-role match quality
  - pre_test_score (0-100): baseline knowledge assessment
  - completion_time_ratio (0-5): actual/expected completion time
  - domain_experience (months): tenure in this domain
  - previous_cycles_completed (count): historical participation rate
  - gaming_flag_count (count): times flagged by gaming detection
  - performance_trend (slope): slope of last 4 quality scores
```

## Alert Triggers (Predictive)
| Trigger | Condition | Action |
|---------|-----------|--------|
| Domain at risk | 2+ consecutive forecast declines >5% | T2 Domain Lead notified |
| Agent at risk | P(non-completion) > 0.7 | Personalized intervention triggered |
| Content shortage | Demand > current capacity * 1.3 | Auto-flag to T1 for allocation |
| Quality degradation | Q-score forecast < 70 | T1 Executive alerted |
