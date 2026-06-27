# CRM Business Case Calculator

**Version:** 1.0
**Purpose:** Quantify the ROI of switching to Sovereign CRM vs legacy systems
**Target:** Decision-makers evaluating CRM investment (CTO, VP Sales, COO)

---

## 1. Cost Comparison Matrix

Fill in the cells below to compare Sovereign CRM against alternatives.

| Cost Category | Salesforce Enterprise | HubSpot Enterprise | Zoho CRM | **Sovereign CRM (Self-Hosted)** |
|--------------|:--------------------:|:------------------:|:--------:|:--------------------------------:|
| Annual license (100 users) | $36,000 | $50,000 | $12,000 | **$0** |
| Implementation (one-time) | $50,000-$150,000 | $20,000-$60,000 | $10,000-$30,000 | **$5,000-$20,000** |
| Annual hosting/infra | N/A (included) | N/A (included) | N/A (included) | **$1,200-$6,000** (VPS/cloud) |
| Annual maintenance | 22% of license ($7,920) | Included | Included | **$0** |
| Training per user | $500/user | $300/user | $200/user | **$0** (self-service) |
| Custom development | $150-$250/hr | $150-$200/hr | $100-$150/hr | **$0** (open source) |
| Data export fees | $10,000+ | $3,000+ | $0 | **$0** |
| **Year 1 Total (100 users)** | **$93,920 - $183,920** | **$70,300 - $110,300** | **$22,200 - $42,200** | **$6,200 - $26,000** |
| **Year 2+ Total (100 users)** | **$43,920/year** | **$50,000/year** | **$12,000/year** | **$1,200-$6,000/year** |

**Estimated 5-Year TCO (100 users):**
- Salesforce: ~$270,000
- HubSpot: ~$270,000
- Zoho: ~$70,000
- **Sovereign CRM: ~$30,000 (89% savings vs Salesforce)**

---

## 2. ROI Calculator — Template

```
INPUTS:
  Number of users:       [___]
  Current CRM:           [___]
  Annual license cost:   [___]
  Annual support cost:   [___]
  Implementation cost:   [___]
  Hours/week on admin:   [___]  (per rep, currently)
  Average rep salary:    [___]
  Pipeline value/year:   [___]
  Win rate:              [___]%
  Average deal size:     [___]
  Sales cycle (days):    [___]

CALCULATED SAVINGS:
  → License savings:              [formula: (current - 0) * users]
  → Admin time savings (30%):     [formula: hours/week * 0.3 * hourly_rate * 52]
  → Pipeline visibility impact:   [formula: win_rate * 0.05 * pipeline_value]
  → Migration cost (one-time):    [formula: based on volume]
  → First year net savings:       [calculated]
  → 5-year net savings:           [calculated]

PAYBACK PERIOD:                    [calculated: months to break even]
```

### Assumptions for Default Calculation
- Sovereign CRM reduces admin time by ~30% (automated workflows, better UI)
- Win rate improves by ~5 percentage points with better pipeline visibility
- Implementation costs: $5K for <50 users, $10K for 50-200, $20K for 200+
- Hosting: $20/user/year for self-hosted (VPS), less at scale

---

## 3. Qualitative Value Drivers

| Driver | Impact | Measurement |
|--------|:------:|-------------|
| Data sovereignty | Controls where data lives | Compliance audit |
| No vendor lock-in | Zero switching cost at any time | Freedom score |
| Open source extensibility | Unlimited customizations | Time-to-new-feature |
| Offline capability | Field sales productivity | Offline hours logged |
| Local AI (Ollama) | AI features on your data | AI feature adoption |
| Community ecosystem | Shared plugins, no vendor gate | Plugin count |

---

## 4. Discovery Sprint Template

This template is used BEFORE every major feature sprint to validate the business outcome.

### Discovery Sprint — Week 0

**Day 1-2: Problem Definition**
- Who is the target user?
- What is their current workflow?
- What is broken today?
- How do they work around it?
- What is the cost of the current problem? (time, money, risk)

**Day 2-3: Solution Exploration**
- What is the simplest solution?
- Are there existing open-source solutions?
- What would Salesforce/HubSpot do?
- What is the 1-sentence value proposition?

**Day 3-4: Success Criteria Definition**
- How will we measure success? (quantitative)
- How will users describe success? (qualitative)
- What is the minimum adoption rate to call it successful?
- What is the anti-success? What would failure look like?

**Day 4-5: Sprint Planning**
- MVP scope (must have for launch)
- Phase 2 scope (next after validation)
- What we explicitly WILL NOT build now
- Risk assessment & mitigation
- Estimate: dev hours, test hours, docs hours

### Discovery Sprint Output
```
Feature: [name]
Problem Statement: [1-2 sentences]
Value Proposition: [1 sentence]
Primary Persona: [role]
Success Metric: [quantitative]
MVP Scope: [3-5 items]
Explicitly Out of Scope: [2-3 items]
Risk: [high/med/low] — [mitigation]
Estimated Effort: [story points or days]
Linked Constitution Question: [which of the 10 questions does this answer?]
```

---

## 5. TCO Comparison Calculator (Pricing Reference)

| Vendor | Per User/Mo (Enterprise) | What's Included | Hidden Costs |
|--------|:------------------------:|-----------------|
| Salesforce | $75-$300 | Sales Cloud, Service Cloud | Integration fees, API limits, storage overage, support tiers |
| HubSpot | $90-$150 | Marketing+Sales+Service Hub | Contact tier limits, API call limits |
| Zoho | $14-$65 | Full CRM suite | Low customization ceiling |
| Pipedrive | $30-$70 | Sales pipeline | Limited automation |
| Monday CRM | $30-$50 | Visual pipeline | Limited integrations |
| **Sovereign CRM** | **$0** | **Everything** | **Hosting + optional support** |
