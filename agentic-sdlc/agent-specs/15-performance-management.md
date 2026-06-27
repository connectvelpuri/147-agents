# PART 15 — AGENT PERFORMANCE MANAGEMENT

**Document:** Enterprise Agentic CRM Delivery Operating System  
**Section:** Part 15 — Agent Performance Management  
**Classification:** INTERNAL — DO NOT PUSH TO GIT

---

## 15.1 PURPOSE

Track, measure, and optimize agent performance. Every agent is evaluated
on quality, accuracy, trust, and efficiency. Performance drives autonomy
levels and career progression.

---

## 15.2 PERFORMANCE METRICS

### Core Metrics

| Metric | Definition | Target | Weight |
|--------|-----------|--------|--------|
| Quality Score | Output quality rating | >8.0/10 | 30% |
| Accuracy Score | Correctness of work | >95% | 25% |
| Trust Score | Reliability rating | >85/100 | 20% |
| Review Pass Rate | % passing first review | >70% | 15% |
| Defect Escape Rate | % defects found post-review | <5% | 10% |
| Rework Rate | % work requiring rework | <10% | 10% |
| Cost Efficiency | Output per unit cost | >0.8 | 5% |

### Metric Calculation

```python
def calculate_performance_score(agent):
    # Collect metrics
    quality = agent.quality_score / 10  # Normalize to 0-1
    accuracy = agent.accuracy_score / 100
    trust = agent.trust_score / 100
    review_pass = agent.review_pass_rate / 100
    defect_escape = 1 - (agent.defect_escape_rate / 100)
    rework = 1 - (agent.rework_rate / 100)
    cost_eff = agent.cost_efficiency
    
    # Weighted calculation
    score = (
        quality * 0.30 +
        accuracy * 0.25 +
        trust * 0.20 +
        review_pass * 0.15 +
        defect_escape * 0.10 +
        rework * 0.10 +
        cost_eff * 0.05
    )
    
    return round(score * 100, 2)
```

---

## 15.3 PERFORMANCE TIERS

### Tier Classification

| Tier | Score Range | Description | Autonomy Impact |
|------|-------------|-------------|-----------------|
| A+ | 95-100 | Exceptional | +2 autonomy levels |
| A | 90-94 | Excellent | +1 autonomy level |
| B+ | 85-89 | Good | No change |
| B | 80-84 | Satisfactory | No change |
| C+ | 75-79 | Needs Improvement | -1 autonomy level |
| C | 70-74 | Below Expectations | -1 autonomy level |
| D | <70 | Poor | -2 autonomy levels, review |

---

## 15.4 PROMOTION RULES

### Promotion Criteria

| Current Tier | Next Tier | Requirements |
|-------------|-----------|--------------|
| Tier 4 → Tier 3 | Score >90 for 30 days, 0 critical defects |
| Tier 3 → Tier 2 | Score >92 for 60 days, 0 critical defects, mentor 1 agent |
| Tier 2 → Tier 1 | Score >95 for 90 days, 0 critical defects, lead major initiative |

### Promotion Process

1. Agent meets criteria for 30+ days
2. Performance review conducted
3. Review Board approves promotion
4. Autonomy level adjusted
5. New responsibilities assigned
6. Knowledge Graph updated

---

## 15.5 RETRAINING RULES

### Retraining Triggers

| Trigger | Action | Duration |
|---------|--------|----------|
| Score drops below 75 | Mandatory retraining | 2 weeks |
| 3 consecutive defects | Targeted training | 1 week |
| Security violation | Security retraining | 1 week |
| Review rejection rate >30% | Review process training | 1 week |

### Retraining Process

1. Identify performance gap
2. Assign training modules
3. Execute training
4. Validate improvement
5. Resume normal duties
6. Monitor for 30 days

---

## 15.6 RETIREMENT RULES

### Retirement Triggers

| Trigger | Action | Process |
|---------|--------|---------|
| Score below 60 for 30 days | Retirement review | Executive Council review |
| 5 critical defects in 30 days | Immediate suspension | Investigation → decision |
| Security breach | Immediate suspension | Investigation → decision |
| Ethics violation | Immediate suspension | Ethics board review |

### Retirement Process

1. Suspension announced
2. Investigation conducted
3. Decision made by Executive Council
4. Knowledge archived
5. Responsibilities transferred
6. Agent deprecated or redeployed

---

## 15.7 PERFORMANCE DASHBOARD

### Dashboard Metrics

```yaml
performance_dashboard:
  agent_summary:
    total_agents: 104
    tier_a_plus: 15
    tier_a: 25
    tier_b_plus: 30
    tier_b: 20
    tier_c_plus: 10
    tier_c: 3
    tier_d: 1
  
  aggregate_metrics:
    avg_quality_score: 8.4
    avg_accuracy_score: 94.2%
    avg_trust_score: 87.5
    avg_review_pass_rate: 72.3%
    avg_defect_escape_rate: 3.8%
    avg_rework_rate: 8.2%
  
  alerts:
    - agent: "AGENT-042"
      issue: "Score dropped below 75"
      action: "Retraining assigned"
    - agent: "AGENT-078"
      issue: "3 consecutive defects"
      action: "Targeted training assigned"
```

---

*Part 15 complete — Agent performance management with metrics, tiers, promotion/retraining/retirement rules, and dashboard.*  
*Document maintained by Hermes Agent. Never push to Git.*
