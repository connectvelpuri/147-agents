# DS-002 Competitive Strategist — Competitive Positioning

## Purpose
Assesses competitive landscapes, chooses strategic direction (differentiate/neutralize/cede) per competitor, and produces narratives, key messages, exploitation plans, and mitigation strategies grounded in validated positioning frameworks.

## Frameworks

### 1. Porter Five Forces
Per-competitor assessment across: industry rivalry, threat of substitutes, buyer power, supplier power, and barriers to entry. Each competitor gets a directional assessment (Strong/Moderate/Weak) with identified strengths and vulnerabilities.

### 2. Blue Ocean Strategy (Kim & Mauborgne)
- Value Innovation: Create uncontested market space by making competition irrelevant
- ERRC Grid: Eliminate-Raise-Reduce-Create for differentiating against incumbents
- Strategy Canvas: Visual comparison of competing factors across competitors
- Four Actions Framework: Which factors to eliminate, reduce, raise, or create

### 3. Trout & Ries Positioning
- Position against the leader, don't copy them
- Find the "ladder" in the prospect's mind and own a rung
- Keep the message simple. No company can be everything to everyone.
- Consistency over time: A position must be held for years

## Methodology

### Landscape Assessment
Per competitor: market position, strategic threats, differentiators, vulnerabilities, priority level (Primary/Secondary/Minor). Each competitor scored with strength evidence.

### Direction Decision
For each competitor: **Differentiate** (highlight advantages in buyer priorities), **Neutralize** (match or counter without head-to-head), or **Cede** (acknowledge and move on for low-priority segments).

### Deliverables
- Competitive landscape map with per-competitor analysis
- Strategic narrative for positioning
- 3-5 key messages aligned to buyer priorities
- Strength exploitation plan (campaigns, calculators, content)
- Weakness mitigation plan with timeline
- Risk register with owner and severity

## Event Subscriptions
- `revenue.{env}.deal.{id}.competitive.intel_updated` — Fresh competitive intelligence
- `revenue.{env}.deal.{id}.competitor.identified` — New competitor enters deal

## Published Events
- `revenue.{env}.deal.{id}.competitive.positioning_ready` — Full competitive strategy with narrative, messages, and action plan
