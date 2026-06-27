# NG-001 BATNA Analyst — HNP Negotiation Science

## Purpose
Analyzes negotiation power dynamics using Harvard Negotiation Project methodology: BATNA (Fisher & Ury), ZOPA (Raiffa), leverage factors, power timeline projection, multi-structure pricing, and ROI defenses.

## Frameworks

### 1. BATNA — Best Alternative To Negotiated Agreement (Fisher & Ury, Getting to Yes)
- Your walkaway: the minimum acceptable deal value
- A strong BATNA = leverage. A weak BATNA = urgency to settle.
- Never reveal your BATNA; research theirs.
- Strengthening actions: build pipeline depth, develop alternatives

### 2. Their BATNA Estimation
- What alternatives do they have?
- Weak BATNA signals: rushed timeline, single-source eval, no competitor
- Confidence scoring based on intelligence quality

### 3. ZOPA — Zone Of Possible Agreement (Raiffa)
- Range between our minimum and their maximum
- No ZOPA = no deal possible without restructuring
- Midpoint is often the natural landing zone

### 4. Leverage Factors
- **Toward us**: Strong alternatives, timeline flexibility, stakeholder consensus
- **Toward them**: Competitive pressure, urgency, single-threaded
- **Weighted** (0.0-1.0) per factor

### 5. Power Timeline
- Does leverage improve or decay over time?
- Accelerate when power is declining
- Let time work when power is improving

### 6. Multi-Structure Options
- Never negotiate on price alone
- Expand the pie: term, scope, payment, risk allocation, services
- Standard options: Multi-year, Volume, Phased, Flexible terms

## Event Subscriptions
- `revenue.{env}.deal.{id}.negotiation.prepare` — Build initial power profile
- `revenue.{env}.deal.{id}.negotiation.reanalyze` — Update with new data

## Published Events
- `revenue.{env}.deal.{id}.negotiation.profile_ready` — Full power profile with BATNA, ZOPA, leverage, options, ROI defenses
