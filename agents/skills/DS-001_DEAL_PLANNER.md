# DS-001 Deal Planner — Strategic Deal Planning

## Purpose
Produces comprehensive deal plans combining situation assessment, milestone planning, stakeholder engagement, risk management, competitive positioning, and critical path analysis — grounded in military strategy and strategic selling methodology.

## Frameworks

### 1. Miller Heiman Strategic Selling
- **Economic Buyer**: Person with budget authority and final say
- **Negative Consequences**: What happens if they don't act?
- **PBO (Preferred Business Outcome)**: What does success look like in measurable terms?
- **Required Capabilities**: What must the solution do?
- **Decision Process**: Who's involved, what are the criteria, what's the timeline?
- **Stakeholder Consensus**: Who's for/against/neutral?
- **Timeline Urgency**: What event makes them need to decide now?
- **Competitive Position**: Where do we stand vs alternatives?

### 2. MEDDIC
- **M**etrics: Quantified business impact
- **E**conomic Buyer: Identified and engaged
- **D**ecision Criteria: Clear and favorable
- **D**ecision Process: Mapped with stages
- **I**ndividual Pain: Personal stake per stakeholder
- **C**hampion: Internal advocate confirmed

### 3. Military Strategy (Sun Tzu, von Clausewitz)
- **Know yourself, know your enemy**: Self-assessment balanced with competitive intelligence
- **Highest victory without fighting**: Position so compelling that competition is preempted
- **Fog of war**: Explicit unknowns and how to resolve them
- **Center of gravity**: The single most important factor that wins the deal
- **Coup d'oeil**: "Quick glance" intuition from pattern recognition

## Methodology

### Situation Assessment
Buyer context, strategic relevance, win probability, relationship strength, recommended next action.

### Milestone Planning
Critical events on the path to close: timeline, dependencies, owners, success criteria.

### Stakeholder Engagement
Per-stakeholder: role, influence level, current stance, engagement strategy, last contact.

### Risk Register
Category, severity, likelihood, impact, mitigation plan, owner, status.

### Competitive Positioning
Per-competitor: strength, vulnerability, our narrative, key differentiator.

### Critical Path
Sequence of must-complete actions with blocking risks, longest-chain analysis.

## Event Subscriptions
- `revenue.{env}.deal.{id}.plan.requested` — Build/refresh deal plan
- `revenue.{env}.deal.{id}.stalled` — Create recovery plan for stalled deal
- `revenue.{env}.deal.{id}.stakeholder.new` — Incorporate new stakeholder

## Published Events
- `revenue.{env}.deal.{id}.plan.created` — Full deal plan with assessment, milestones, stakeholders, risks
- `revenue.{env}.deal.{id}.stall.recovery_plan` — Recovery strategy for stalled deals
