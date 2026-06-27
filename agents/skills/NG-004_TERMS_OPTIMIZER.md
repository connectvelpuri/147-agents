# NG-004 Terms Optimizer — Contract Term Analysis

## Purpose
Analyzes contract terms across 8 risk categories, benchmarks against market standards, and provides optimization recommendations with cash-flow impact modeling.

## Term Categories

| Category | Examples | Assessment Criteria |
|----------|----------|-------------------|
| PAYMENT | Payment timing, net terms, upfront vs milestone | Cash conversion cycle, discount potential |
| LIABILITY | Damage caps, indemnification, exclusions | Exposure quantification, mitigation feasibility |
| SLA | Uptime guarantees, credits, remedies | Industry benchmark deviation, credit risk |
| RENEWAL | Auto-renewal, notice period, price adjustment | Churn risk, revenue predictability |
| IP | Ownership, license scope, derivatives | Value capture, competitive protection |
| TERMINATION | For cause/convenience, notice, survival | Exit flexibility, lock-in risk |
| DATA | Processing, storage, security, residency | Compliance exposure, portability |
| COMPLIANCE | Regulatory, certification, audit rights | Penalty exposure, audit burden |

## Methodology

### Risk Scoring (HIGH / MEDIUM / LOW)
Each term category scored based on: deviation from market standard, financial exposure, regulatory risk, negotiation leverage.

### Payment Optimization
- Cash-flow impact of payment terms (Net 30 vs Net 90)
- Early-payment discount analysis (e.g., 2% for Net 30)
- Annual vs quarterly vs milestone payment structures

### Liability Exposure
- Quantified exposure (multiple of fees, uncapped, etc.)
- Market standard comparisons per industry
- Mitigation recommendations (carve-outs, insurance, caps)

### Market Standards
Benchmarking against enterprise SaaS norms:
- Liability: 1-2× fees typical, direct damages only
- SLA: 99.9%-99.95% for financial services
- Payment: Net 30-60 standard, Net 90 upper bound
- Renewal: 30-60 day notice typical

## Event Subscriptions
- `revenue.{env}.deal.{id}.contract.draft_received` — Analyze received contract draft
- `revenue.{env}.deal.{id}.contract.legal_review_completed` — Incorporate legal findings

## Published Events
- `revenue.{env}.deal.{id}.terms.optimization_ready` — Full term analysis with risks, recommendations, and priority actions
