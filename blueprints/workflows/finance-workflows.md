# Finance Workflows — Complete Map

## 1. Quote to Cash

### 1.1 Quote Generation (Finance View)
- **Trigger**: Sales rep finalizes quote in CPQ
- **Actor**: Sales rep, system (pricing engine)
- **Steps**:
  1. Verify price book assignment: correct product catalog, currency, locale
  2. Apply product pricing: list price, discounts, promotions, tiered pricing
  3. Validate deal terms: minimum commitment, contract length, payment frequency
  4. Run margin analysis: unit cost, discount %, expected margin
  5. Apply tax calculation: nexus-based, product-based (Avalara/TaxJar API)
  6. Set payment terms: Net 15/30/45/60, upfront, milestone-based
  7. Generate quote PDF with all terms, pricing, validity (30 days)

### 1.2 Order Creation & Validation
- **Trigger**: Quote accepted (signed/e-signed)
- **Actor**: System, finance ops
- **Steps**:
  1. Convert quote to order record
  2. Validate product availability: inventory check, provisioning status
  3. Check credit: for credit terms, run credit check on account (D&B score)
  4. Set order status: Pending Fulfillment (if products), Pending Activation (if services)
  5. Apply revenue schedule: one-time, monthly subscription, annual prepaid
  6. Send order confirmation to customer
- **Inputs**: Signed quote, order record, price book, inventory system
- **Outputs**: Order, fulfillment request, invoice (if one-time), subscription schedule
- **Decisions**: Product requires fulfillment → route to provisioning; Service only → activate immediately; Credit check fails → flag for finance review
- **Connected Workflows**: Subscription management (2.1), Order fulfillment
- **SLA**: Order creation < 1 min

### 1.3 Invoice Generation
- **Trigger**: Order activated, subscription milestone, recurring billing cycle
- **Actor**: System (billing engine)
- **Steps**:
  1. Generate invoice document: line items, quantities, unit price, discounts, taxes
  2. Apply billing rules: proration on mid-cycle changes, credit memo handling
  3. Route invoice for approval (if > threshold amount)
  4. Deliver to customer: email (PDF), portal, EDI, e-invoice network
  5. Post invoice to accounting system (ERP: NetSuite, Sage, QuickBooks)
  6. Set invoice status: Draft → Approved → Sent → Paid/Overdue
- **Inputs**: Order, subscription schedule, billing rules, tax rates
- **Outputs**: Invoice record, PDF, accounting journal entry, GL codes
- **Decisions**: Amount > $50k → CFO approval required; Manual invoice → finance team processes
- **Connected Workflows**: Payment processing (1.4), Revenue recognition (1.5)
- **SLA**: Invoice within 24h of order activation
- **Error States**: Missing tax rate for location, ERP sync failure, duplicate invoice generation
- **Validations**: Line total must equal order total; tax calculation must match expected rate

### 1.4 Payment Processing
- **Trigger**: Invoice sent, payment due, customer submits payment
- **Actor**: System (payment gateway: Stripe, Adyen, Braintree), customer, finance
- **Steps**:
  1. Customer pays: credit card, ACH, wire, check, credit memo
  2. Process via payment gateway: card → capture (authorize + settle), ACH → verify (micro-deposits)
  3. Handle declined transactions: retry logic (3 attempts, card: immediate, 3, 7 days)
  4. Apply payment to invoice: full or partial
  5. Update invoice status: Paid, Partial Paid, Overdue
  6. Update account balance: credit limit consumption
  7. Reconcile with bank statement (weekly match)
- **Inputs**: Invoice, payment method, gateway config
- **Outputs**: Payment record, gateway transaction, reconciled bank entry
- **Decisions**: Partial payment → remaining balance still due; Wire received but no invoice match → unapplied cash
- **Connected Workflows**: Collections (manual), Dunning (automated payment reminders)
- **SLA**: Payment capture immediate; reconciliation nightly
- **Error States**: Card declined (insufficient funds, expired), ACH returned (NSF), Gateway timeout
- **Validations**: Payment amount ≤ invoice remaining balance; currency match required

### 1.5 Revenue Recognition
- **Trigger**: Invoice created, payment received, milestone met (ASC 606)
- **Actor**: System (RevRec engine: Zuora RevPro, NetSuite), finance
- **Steps**:
  1. Determine performance obligations: products, services, support, maintenance
  2. Allocate transaction price to each obligation (standalone selling price method)
  3. Recognize revenue over time (services) or at point in time (products)
  4. Apply schedule: monthly, quarterly, annually
  5. Post revenue entries to ERP/GL
  6. Track deferred revenue balance
  7. Run RevRec reports: recognized vs deferred, by product, region, period
- **Inputs**: Order, invoice, contract terms, product config
- **Outputs**: Revenue schedule, GL entries, deferred revenue report
- **SLA**: Revenue recognized per period close schedule
- **Error States**: Missing standalone selling price, product unbundled incorrectly

---

## 2. Subscription Management

### 2.1 Plan Definition & Billing
- **Trigger**: New product launch, pricing change
- **Actor**: Product ops, finance
- **Steps**:
  1. Define subscription plan: name, features, price, billing frequency (monthly/annual)
  2. Set plan tiers: Basic, Pro, Enterprise
  3. Configure billing rules: charge upfront, prorate on change, minimum commitment
  4. Define renewal terms: auto-renew with notice period (30/60/90 days)
  5. Activate plan in price book
  6. Publish to customer portal

### 2.2 Upgrade / Downgrade
- **Trigger**: Customer requests plan change, usage exceeds tier limits
- **Actor**: Sales rep, customer (self-service), system
- **Steps**:
  1. Validate eligibility: no pending invoices, contractual minimum period met
  2. Calculate proration: credits for unused time on old plan, charges for new plan
  3. Generate credit memo (down) or additional invoice (up)
  4. Apply feature entitlements: enable/disable based on new plan
  5. Create subscription amendment record
  6. Sync to provisioning

### 2.3 Churn & Reactivation
- **Trigger**: Non-payment, cancellation request, auto-expire
- **Actor**: System, retention team, customer
- **Steps**:
  1. Subscription expiration: auto-renew fails (payment declined)
  2. Enter grace period (7-30 days)
  3. Service degradation: reduced feature access after grace
  4. Final suspension: access revoked, data retained (90 days retention)
  5. Reactivation: charge payment, restore services
  6. Churn reason captured: voluntary (cancellation reason) vs involuntary (payment failure)
- **Connected Workflows**: Revenue forecasting (4.1), Collections

### 2.4 Revenue Reporting (MRR/ARR)
- **Trigger**: Monthly/quarterly close
- **Actor**: Finance, FP&A
- **Steps**:
  1. Calculate MRR/ARR: sum of recurring charges for active subscriptions
  2. Breakdown: New (new customers), Expansion (upgrades), Contraction (downgrades), Churn (cancellations)
  3. Track net revenue retention (NRR): (Start MRR + Expansion - Contraction - Churn) / Start MRR
  4. Forecast forward 12 months based on current churn rate
  5. Report by segment: product line, region, customer tier

---

## 3. Commission Calculation

### 3.1 Commission Plan Structure
- **Trigger**: Fiscal year planning, sales comp revision
- **Actor**: RevOps, finance, sales leadership
- **Steps**:
  1. Define compensation plan: base salary, commission rate, accelerators, caps
  2. Set attribution: quota attainment % = payout trigger
  3. Define accelerators: e.g., 1x for 80%, 1.5x for 100%, 2x for 120%+
  4. Set clawback terms: if deal churns within 6 months → commission clawback
  5. Plan approved and published to reps

### 3.2 Commission Calculation
- **Trigger**: Monthly/quarterly close, deal closed won
- **Actor**: System (Xactly, Spiff, CaptivateIQ), finance
- **Steps**:
  1. Pull closed-won opportunities with amounts, close dates, rep attribution
  2. Validate deal eligibility: not clawback, payment received (if policy requires)
  3. Apply commission rate per rep plan
  4. Apply accelerators/caps based on YTD attainment
  5. Calculate commission payout: Amount × Rate × Accelerator
  6. Generate commission statement for each rep
  7. Submit to payroll

### 3.3 Commission Disputes
- **Trigger**: Rep disputes calculation
- **Actor**: Rep, finance, sales ops
- **Steps**:
  1. Rep submits dispute with justification
  2. Investigate: check deal attribution, plan version, clawback status
  3. Adjust if valid: recalculate, re-approve
  4. Log dispute resolution for audit
- **SLA**: Dispute investigated within 5 business days

---

## 4. Expense Tracking

### 4.1 Expense Entry & Approval
- **Trigger**: Employee incurs business expense
- **Actor**: Employee, manager, finance
- **Steps**:
  1. Submit expense report: receipts (OCR), category, amount, date, project
  2. Apply policy rules: per-diem limits, mileage rate, approval thresholds
  3. Route to manager for approval
  4. If > $500 → finance review; > $5000 → CFO approval
  5. Approved → queue for reimbursement
- **Connected Workflows**: Reimbursement (4.2)

### 4.2 Reimbursement & Reporting
- **Trigger**: Expense approved
- **Steps**: Batch to payroll (with salary) or separate ACH → employee paid
- **Reporting**: Expense by department, category, period

---

## 5. Revenue Forecasting (Finance View)

### 5.1 Pipeline-to-Revenue Mapping
- **Trigger**: Monthly/quarterly forecast cycle
- **Actor**: FP&A, RevOps
- **Steps**:
  1. Pull weighted pipeline from CRM: all open opportunities × probability
  2. Apply conversion rates from historical close rates (by source, region)
  3. Segment: new business vs expansion vs renewal
  4. Convert pipeline $ to expected booking dates
  5. Cross-reference with contractual revenue schedule (subscriptions)
  6. Generate forecast: expected new revenue, expected churn, net growth

### 5.2 Forecast vs Actual Analysis
- **Trigger**: Period close
- **Actor**: FP&A
- **Steps**:
  1. Compare forecasted revenue to actual booked
  2. Calculate variance: absolute $ and %
  3. Analyze by segment: which pipeline stages over/under-performed
  4. Identify bias: systemic over-optimism or under-promising
  5. Update forecast model assumptions
  6. Publish forecast accuracy scorecard by team/sales rep
