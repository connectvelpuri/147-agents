# DS-005 Discount Authority — Role-Based Approval Matrix

## Purpose
Enforces discount approval policy through role-based authority tiers with LLM override for edge cases. Rule-first, judgment-when-needed.

## Authority Matrix

| Role | Max Discount | High-Value Override |
|------|-------------|-------------------|
| SDR | 5% | >$50K → escalate |
| AE | 10% | >$50K → escalate |
| Senior AE | 15% | >$50K → escalate |
| Manager | 20% | >$50K → escalate |
| Director | 25% | >$50K → escalate |

## Decision Flow
1. **Within authority AND not high-value?** → Auto-approve with conditions
2. **Out of authority OR high-value?** → LLM review with modified/denied decision

### Rule Path
Pure policy enforcement: checks role limits and value threshold. Returns approved discount at the role's maximum if within bounds.

### LLM Path
Evaluates: margin impact, competitive pressure, relationship value, deal size, historical patterns, buyer leverage. Can approve at a modified level (below requested) or deny with alternative concessions.

## Conditions
Approved discounts may carry conditions (reduction stored as an array):
- "Minimum 24-month contract term"
- "Annual upfront payment"
- "Sign before quarter-end"
- "Provide customer reference"

## Alternative Concessions
When discount denied or reduced, may offer:
- Free support/services extension
- Complimentary training
- Future upgrade credit
- Accelerated implementation
- Extended payment terms

## Event Subscriptions
- `revenue.{env}.deal.{id}.discount.rep_requested` — Rep requests discount approval
- `revenue.{env}.deal.{id}.quarter_end.approaching` — Quarterly close triggers

## Published Events
- `revenue.{env}.deal.{id}.discount.decision_made` — Approval decision with conditions and alternatives
