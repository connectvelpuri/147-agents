# NG-002 Concession Planner — Strategic Concession Sequencing

## Purpose
Plans concession sequences that maximize perceived value while minimizing actual cost, using principled negotiation frameworks and trade-off analysis.

## Frameworks

### 1. Principled Concession (Raiffa / Malhotra & Bazerman)
- Separate people from the problem
- Focus on interests, not positions
- Invent options for mutual gain
- Insist on objective criteria
- Concessions should be sequenced: low-cost-high-value first

### 2. Getting Past No (William Ury)
- Don't reject, reframe: Step to their side, reframe the problem
- Don't push, build them a golden bridge: Make it easy to say yes
- Don't escalate, use power to educate: Show the cost of no deal
- Don't attack, go to the balcony: See the negotiation from above

### 3. 3D Negotiation (Lax & Sebenius)
- **Tactics (1D)**: At-the-table moves, persuasion, framing
- **Deal Design (2D)**: Structure the deal for joint value
- **Setup (3D)**: Configure the right players, interests, and options before sitting down

## Methodology

### Concession Sequencing
Items ordered by cost/perceived-value ratio:
1. Low-cost-high-perceived-value (training, support hours, payment terms) — open with these
2. Moderate concessions (onboarding assistance, implementation)
3. Price concessions in incremental steps, each tied to buyer commitment

### Trade-Off Matrix
Four quadrants mapping concession types to value lost:
- Price/Payment quadrant
- Scope/Service quadrant
- Terms/Risk quadrant
- Relationship/Commitment quadrant

### Walk-Away Triggers
Predefined hard limits: maximum discount %, payment term cap, cost ceiling, scope boundary.

### Pacing
- Space concessions across negotiation rounds
- Each concession requires a buyer commitment
- Signal confidence through pacing: don't concede faster than they commit

## Event Subscriptions
- `revenue.{env}.deal.{id}.negotiation.concession_requested` — Plan concession strategy
- `revenue.{env}.deal.{id}.negotiation.buyer_demand` — Respond to new buyer demand

## Published Events
- `revenue.{env}.deal.{id}.negotiation.concession_plan_ready` — Full concession sequence with costs, triggers, pacing
