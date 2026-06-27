# DS-004 Price Optimizer — Value-Based Pricing

## Purpose
Optimizes pricing through value-based analysis, price sensitivity measurement, discount impact modeling, and Van Westendorp Price Sensitivity Meter methodology.

## Frameworks

### 1. Value-Based Pricing (Donovan & Hinterhuber)
- Price is determined by perceived value to the customer, not cost-plus or competitor match
- Customer willingness-to-pay (WTP) as the upper bound
- Market reference price as the anchor
- Value drivers: quantitative ROI, strategic value, competitive scarcity

### 2. Van Westendorp Price Sensitivity Meter (PSM)
- **Indifference Point (IDP)**: Price where "neither cheap nor expensive"
- **Optimal Price Point (OPP)**: Price where "both good value and starting to be expensive"
- **Point of Marginal Cheapness (PMC)**: Below this feels too cheap to be quality
- **Point of Marginal Expensiveness (PME)**: Above this feels too expensive to consider
- Range of acceptable prices: PMC to PME

### 3. Price Elasticity Modeling
- Win-rate elasticity: Δwin% / Δprice%
- Elasticity = 0 (perfectly inelastic buyers — rare) to >1 (highly elastic — commodity)
- B2B enterprise SaaS typical elasticity: 0.3–0.7
- Optimal price: maximizes expected value (price × win_probability)

### 4. Discount Impact Analysis
- Revenue impact: deal_value × discount%
- Margin compression: margin% impact from discount
- Break-even units needed at discounted price to match original margin
- Discount sensitivity: is the buyer price-sensitive or value-sensitive?

## Methodology
- Acceptable price range from market data and Van Westendorp
- Win-probability curve using elasticity estimate
- Expected value = price × P(win) for each candidate price
- Optimal price at peak of expected-value curve
- Discount analysis with alternatives (bundling, tiered, performance-based)

## Event Subscriptions
- `revenue.{env}.deal.{id}.pricing.requested` — Build price optimization
- `revenue.{env}.deal.{id}.discount.requested` — Analyze discount impact

## Published Events
- `revenue.{env}.deal.{id}.pricing.optimization_ready` — Optimal price, range, sensitivity, rationale
- `revenue.{env}.deal.{id}.pricing.discount_analyzed` — Discount impact, break-even, alternatives
