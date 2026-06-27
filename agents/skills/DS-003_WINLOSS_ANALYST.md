# DS-003 Win/Loss Analyst — Clozd/Gong Root Cause Analysis

## Purpose
Analyzes closed-lost and closed-won deals using structured loss taxonomy, pattern detection, data completeness scoring, and actionable recommendations.

## Loss Reason Taxonomy (Clozd methodology)
1. **Price** — Cost exceeded value perception or budget constraints
2. **Product** — Missing features, integration issues, capability gaps
3. **Relationship** — No champion, poor rapport, trust deficit
4. **Process** — Sales process breakdown, poor discovery, misqualification
5. **No Decision** — Evaluation paralysis, status quo maintained, stalled
6. **Competitor** — Specific competitive loss with identified rival
7. **Timing** — Budget cycle, deprioritized, bad timing
8. **Vendor Risk** — Security, compliance, financial viability concerns
9. **Internal Politics** — Stakeholder conflict, reorg, priority shift

## Preventability Score (0.0-1.0)
- 0.0: Unavoidable (reorg, bankruptcy, product doesn't exist)
- 0.5: Partially preventable (different approach could have helped)
- 1.0: Fully preventable (process failure, relationship neglect)

## Win Reason Taxonomy
- Product Fit, Relationship, Price-Value, Timing, Existing Vendor, Executive Pull, Champion

## Pattern Detection
- **Price Sensitivity**: Recurring price-related losses
- **Process Flaw**: Repeated process breakdowns
- **Stalled Stage**: Deals dying in later stages
- **Missing Stakeholder**: Single-threaded loss pattern
- **Competitive Weakness**: Recurring competitive losses

## Clozd Principles
1. The buyer's perception IS reality — analyze from their frame
2. Loss reasons are rarely singular — look for contributing factors
3. "No decision" is often a decision for the status quo
4. Price objection usually masks value perception failure

## Event Subscriptions
- `revenue.{env}.deal.{id}.closed_lost.recorded`
- `revenue.{env}.deal.{id}.closed_won.achieved`
- `revenue.{env}.deal.{id}.winloss.analyze.requested`

## Published Events
- `revenue.{env}.deal.{id}.winloss.analyzed` — Primary reason, preventability, patterns, recommendations
