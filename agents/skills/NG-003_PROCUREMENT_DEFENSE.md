# NG-003 Procurement Defense — Tactic Detection & Counter-Strategy

## Purpose
Detects procurement negotiation tactics in real time and provides counter-strategies from a 10-tactic classification library.

## Tactic Library

| Tactic | Description | Severity | Common Signals |
|--------|-------------|----------|----------------|
| Good Cop / Bad Cop | Friendly negotiator + tough counterpart | medium | "I'd love to but my boss..." |
| Nibbling | Small last-minute concessions | low | "Just one more thing..." |
| Deadline Pressure | Artificial urgency to force decision | high | "Proposal expires today" |
| Reopening Closed | Revisiting agreed points | high | "Can we revisit pricing?" |
| Walk-Away Threat | Threatens to leave negotiation | critical | "We'll look elsewhere" |
| Standard Terms Push | Insists on their paper | low | "This is our standard" |
| Silence Ploy | Silent after your ask | medium | Extended pause after price |
| Splitting Difference | "Meet in the middle" appeals | medium | "Let's split the gap" |
| Delay Tactic | Stalling for advantage | medium | "Let's wait until next quarter" |
| Limited Authority | "My hands are tied" | low | "I need approval for..." |

## Methodology

### Classification
Rule-based keyword detection with confidence scoring + LLM enrichment for nuanced cases. Outputs: tactic enum, confidence (0-100%), severity, evidence text.

### Counter-Strategy
Each tactic has:
- **Immediate Response**: First thing to say
- **Fallback Position**: Next move if immediate fails
- **Escalation Trigger**: When to involve management

### Delivery
Per-tactic response with framing guidance, calibrated to deal size, relationship, and stage.

## Event Subscriptions
- `revenue.{env}.deal.{id}.procurement.tactic_detected` — Analyze tactic in communication
- `revenue.{env}.deal.{id}.procurement.department_involved` — Procurement enters deal

## Published Events
- `revenue.{env}.deal.{id}.procurement.defense_ready` — Detected tactics with counter-strategies
