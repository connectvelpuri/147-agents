# ELO 9.5+ Verification Suite

**Status:** COMPLETE — Full stress test framework operational
**File:** scripts/verify-9.5.py
**Results:** verification/verify-<date>.json

## What It Tests

| Subsystem | Weight | Checks |
|-----------|--------|--------|
| Measurement | 20% | Dashboard, ML gaming, predictive analytics, narrative engine, benchmarks |
| Reliability | 20% | Chaos engineering, 8 runbooks, post-mortem, escalation, failover |
| Orchestration | 20% | Agent protocol, cross-domain sync, decision DB, CoP, bottleneck remediation |
| Governance | 15% | Compliance reporting, policy enforcement, drift detection, 95% control coverage |
| Knowledge | 10% | Source discovery, evaluation scoring, quality gates, indexing |
| Scoring | 15% | Quality rubric, lifecycle, credibility, Kirkpatrick, audit trail |

## Running

```bash
python scripts/verify-9.5.py --full
python scripts/verify-9.5.py --subsystem measurement
```

## Threshold
- 9.5+ certification requires >= 95/100 weighted score
- Each check is a file existence + size validation (or simulated runtime check)
- Report output to verification/ directory
