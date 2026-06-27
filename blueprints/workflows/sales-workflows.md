# Sales Workflows — Complete Map

## 1. Lead Management Lifecycle

### 1.1 Lead Capture
- **Trigger**: Web form submission, chat widget, email inbound, event scan, API ingestion, partner referral
- **Actor**: Anonymous visitor, system (automated capture), partner portal
- **Steps**:
  1. Source detection — track UTM parameters, campaign ID, referrer URL, QR code ID
  2. Form data validation — required fields (email, company), format checks, spam score (reCAPTCHA/honeypot)
  3. Duplicate check — fuzzy match on email, phone, company domain; merge if score > 85%
  4. Default assignment — round-robin or region-based owner; unassigned pool fallback
  5. Status set to "New" — audit trail stamped with source, timestamp, IP, user agent
- **Inputs**: Lead form fields, UTM params, source metadata, landing page ID
- **Outputs**: Lead record, audit log entry, assignment notification
- **Decisions**:
  - Duplicate found → route to merge queue or auto-merge (configurable threshold)
  - Spam detected → quarantine pool, tag `[SPAM]`, notify admin
  - Missing required data → partial record, status "Incomplete", auto-reminder to source
- **Connected Workflows**: Marketing lead generation (1.3), Contact creation (2.1)
- **SLA**: Real-time (< 1s sync), batch ingestion < 5 min for CSV/API bulk
- **Error States**: Invalid email format, blocked domain, IP blacklisted, CAPTCHA failure
- **Validations**: Email regex, phone E.164, domain MX record check, Salesforce duplicate rules

### 1.2 Lead Enrichment
- **Trigger**: Lead creation, scheduled batch, field update trigger
- **Actor**: System (ZoomInfo, Clearbit, Lusha, DiscoverOrg API connectors)
- **Steps**:
  1. Submit domain/email to enrichment provider
  2. Parse returned data: company size, industry, revenue range, tech stack, social profiles
  3. Map to custom fields: `AnnualRevenue`, `EmployeeCount`, `Technologies__c`
  4. Append intent signals if provider supports (surge topics, buying stage)
  5. Score confidence level — if < 60%, flag for manual review
  6. Update lead record, set `EnrichmentDate__c`, increment enrichment counter
- **Inputs**: Lead ID, email, company domain
- **Outputs**: Enriched fields, confidence score, enrichment log
- **Decisions**: Provider returned partial data → partial update, no error; Provider down → queue retry (3 attempts, exponential backoff)
- **Connected Workflows**: Lead scoring (1.3), Lead qualification (1.4)
- **SLA**: < 30s per lead, batch < 10 min per 1000 records
- **Error States**: API timeout, rate limit hit (429), provider auth expired, domain not found
- **Validations**: JSON schema validation on API response, null-check before field overwrite

### 1.3 Lead Scoring
- **Trigger**: Lead creation, enrichment completion, behavior event (page visit, email click)
- **Actor**: System (rules engine or ML model)
- **Steps**:
  1. Aggregate demographic score: industry fit (0-30), company size (0-20), seniority (0-25), geography (0-10)
  2. Aggregate behavioral score: email open (5), click (10), form visit (3), pricing page (15), demo request (30)
  3. Aggregate engagement score: recency multiplier (1.0-0.1 decay over 90 days), frequency weight
  4. Compute total = demographic + behavioral + engagement — range 0-100
  5. Apply threshold rules: > 80 = Hot, 60-79 = Warm, 30-59 = Cold, < 30 = Nurture
  6. If Hot and not yet assigned → trigger qualification workflow
  7. Update score history object for trend tracking (score velocity)
- **Inputs**: Lead fields, activity history, enrichment data, scoring model config
- **Outputs**: Composite score, score breakdown, lead status change, score history record
- **Decisions**: Score drops across threshold → downgrade status; Score surges → alert assigned rep (if any)
- **Connected Workflows**: Lead qualification (1.4), Email engagement tracking (2.2)
- **SLA**: Real-time on behavior events, batch recalculation nightly
- **Error States**: Missing scoring model, null field causing weight calc failure, divided-by-zero on recency
- **Validations**: Score range 0-100 clamped, all weights sum to 100, decay factor ∈ (0, 1]

### 1.4 Lead Qualification
- **Trigger**: Lead score crosses threshold, manual rep action, BDR assignment
- **Actor**: BDR, SDR, automated qualification bot
- **Steps**:
  1. Load lead record + enrichment + activity history + score breakdown
  2. Apply BANT/CHAMP/MEDDIC framework (configurable per org):
     - Budget: confirmed or estimated?
     - Authority: decision-maker or influencer?
     - Need: pain point articulated?
     - Timeline: buying window (< 30, 30-90, > 90 days)?
  3. Score qualification — pass/fail with reason
  4. If pass → status to `Qualified`, create opportunity draft (if BANT all confirmed)
  5. If fail → status to `Disqualified`, reason code, nurture track assignment
  6. Notify assignment owner
- **Inputs**: Lead record, score, enrichment, BANT responses
- **Outputs**: Qualified lead, opportunity draft, disqualification reason code, nurture program ID
- **Decisions**: BANT partially met → "In Progress" status, schedule follow-up task; Disqualification reason "No Budget" → add to long-term nurture; "No Authority" → attempt stakeholder chain
- **Connected Workflows**: Opportunity creation (3.1), Lead distribution (1.5), Nurture campaign assignment
- **SLA**: BDR must action within 24h of score crossing threshold
- **Error States**: BANT field not filled, missing decision criteria config, duplicate opportunity creation
- **Validations**: At least "Need" must be confirmed to qualify; opportunity cannot exist without linked lead

### 1.5 Lead Distribution
- **Trigger**: Lead qualification, round-robin trigger, territory assignment rule
- **Actor**: System (assignment engine), admin (manual override), sales manager
- **Steps**:
  1. Evaluate assignment rules in priority order: named account, territory match, industry, round-robin, capacity
  2. Check rep capacity (open leads < max, active opportunities < cap)
  3. Exclude out-of-office reps, vacation auto-away
  4. Assign owner and share record
  5. Send notification (email, Slack, in-app) with lead summary
  6. Set assignment date for SLA tracking
- **Inputs**: Lead record, territory map, rep capacity config, OOO calendar
- **Outputs**: Assigned owner, notification, assignment SLA timer start
- **Decisions**: No eligible rep → queue to unassigned pool, escalate to manager; Multi-match → apply tiebreaker (fewest active leads)
- **Connected Workflows**: Territory management (7.1), User provisioning (Ops 1.1)
- **SLA**: Auto-assignment < 1 min; manual review queue SLA 4h
- **Error States**: All reps over capacity, no reps in territory, assignment rule infinite loop
- **Validations**: Rep must have active status and appropriate role; circular assignment rules flagged

### 1.6 Lead Conversion
- **Trigger**: Rep clicks "Convert", qualification confirmed
- **Actor**: Sales rep, system
- **Steps**:
  1. Match or create Contact: fuzzy search on email, phone; update existing or create new
  2. Match or create Account: match on domain, merge if needed
  3. Convert Lead → Opportunity: carry custom fields, campaign history, activity timeline
  4. Set Opportunity fields: Stage = Prospecting, Amount = estimated value, Close Date = inferred timeline
  5. Set Lead status = Converted, mark conversion date/time
  6. Post-conversion actions: enroll in sequence, create onboarding task, notify account team
- **Inputs**: Lead ID, contact match config, field mapping config
- **Outputs**: Contact record, Account record, Opportunity record, conversion audit, campaign member update
- **Decisions**: Multiple contact matches → show picklist to rep; No account match → create with auto-enrich; Field mapping collision → use source field, log conflict
- **Connected Workflows**: Contact management (2.1), Account management (3.1), Deal pipeline (4.1)
- **SLA**: Real-time on rep action
- **Error States**: Lead already converted, missing required opportunity field, account name too long
- **Validations**: Lead-Count lookup prevents double conversion; required opp fields must be populated; duplicate contact check mandatory

### 1.7 Lead Rejection & Recycling
- **Trigger**: Rep marks lead as disqualified, nurture score never recovers
- **Actor**: Rep, system (time-based), admin
- **Steps**:
  1. Capture disqualification reason from picklist: No Budget, No Authority, No Need, Timing Wrong, Duplicate, Not a Fit
  2. Set lead status = "Disqualified" or "Recycled"
  3. If recycled → assign to nurture program based on reason: Timing → 90-day nurture; No Budget → 180-day drip
  4. If disqualified → archive with reason, suppress from active queues
  5. Log disqualification date, rep, reason for analysis
  6. Trigger re-engagement rules: if lead interacts again (site visit, email open) and was recycled, re-score
- **Inputs**: Lead ID, disqualification reason, nurture program mapping
- **Outputs**: Status change, audit log, nurture enrollment, suppression list entry
- **Decisions**: Recycled + subsequent engagement → re-enter scoring; Disqualified + new form fill → create fresh lead? (configurable)
- **Connected Workflows**: Nurture campaigns (Marketing 2.2), Lead capture (1.1)
- **SLA**: Immediate status update
- **Error States**: No reason code selected (block save), re-engagement without recycle flag
- **Validations**: Reason code required; archived leads blocked from reassignment

---

## 2. Contact Management

### 2.1 Contact Creation
- **Trigger**: Manual entry, lead conversion, form submission with matching contact, API import, meeting sync
- **Actor**: Rep, system, integration
- **Steps**:
  1. Ingest person data: name, email, phone, company, title, social links
  2. Run dedup against existing contacts (fuzzy match on email, phone, name+company)
  3. If unique → create record
  4. If duplicate → surface to user with match details; auto-merge if config set
  5. Enrich from company domain info
  6. Set default fields: owner, source, privacy consent, language, timezone
  7. Create audit record with creation source, timestamp
- **Inputs**: Person data, dedup rules, enrichment config
- **Outputs**: Contact record, duplicate audit, enrichment log
- **Decisions**: Duplicate match confidence > 90% → auto-merge; 70-90% → suggest merge; < 70% → create as new
- **Connected Workflows**: Account association (2.6), GDPR (2.7), Contact dedup (2.2)
- **SLA**: Real-time on UI creation; batch API < 5 min
- **Error States**: Missing email when required, email format invalid, phone format unparseable
- **Validations**: Email uniqueness (configurable), required field presence, privacy opt-in if GDPR

### 2.2 Contact Deduplication
- **Trigger**: Contact creation, scheduled batch job, data import completion
- **Actor**: System (dedup engine), admin (review)
- **Steps**:
  1. Run matching rules: exact email, fuzzy email, phone, name+company, social handle
  2. Group potential duplicates by match type and score
  3. Rank groups by confidence score (0-100)
  4. Auto-merge groups > threshold (default 90%)
  5. Queue groups in threshold band (70-89%) for admin review
  6. Apply survivorship rules: most recent update wins, or field-level priority
  7. Merge: update surviving record, archive duplicate, reparent related records
- **Inputs**: Contact records, matching rules config, survivorship rules
- **Outputs**: Merged contacts, merge audit, orphan link report
- **Decisions**: Match score < 70% → no action; Same record found across three lists → choose most complete
- **Connected Workflows**: Data quality (Ops 3.3), Contact merge (2.3)
- **SLA**: Daily batch; real-time on import
- **Error States**: Merge lock contention, related record reparenting failure, field value collision on merge
- **Validations**: Cannot merge contact into itself; merge survivorship must have at least one rule

### 2.3 Contact Merge
- **Trigger**: Admin or rep initiates merge from UI, dedup engine auto-merge
- **Actor**: Admin, power user, system
- **Steps**:
  1. Select master and duplicate records
  2. Preview merge: show field-by-field which value survives
  3. Allow manual field override: pick master value per field
  4. Execute merge: master retains ID, duplicate ID archived
  5. Reparent: opportunities, cases, tasks, events, emails re-linked to master
  6. Log merge action in audit trail
- **Inputs**: Master Contact ID, Duplicate Contact IDs, field survivorship map
- **Outputs**: Unified contact record, merge audit log, unlink report
- **Decisions**: Conflicting field values → apply survivorship rule or prompt user
- **Connected Workflows**: Account merge (3.3), Data quality (Ops 3.3)
- **SLA**: Real-time

### 2.4 Contact Enrichment (Continuous)
- **Trigger**: Contact creation, scheduled weekly batch, title change detected
- **Actor**: System (API connectors)
- **Steps**:
  1. Check last enriched date — skip if < 30 days ago (rate limit)
  2. Submit contact email/company to enrichment API
  3. Receive updated title, phone, social profiles, company info
  4. Apply changes only if newer than existing data (timestamp compare)
  5. Log enrichment event with before/after values
  6. If title changed → trigger segmentation re-evaluation
- **Connected Workflows**: Segmentation (2.5), Lead enrichment (1.2)
- **SLA**: Weekly batch
- **Error States**: Same as Lead enrichment (1.2)

### 2.5 Contact Segmentation
- **Trigger**: Contact creation, field update, scheduled batch, campaign targeting
- **Actor**: System (dynamic list builder), admin (manual list)
- **Steps**:
  1. Evaluate contact against all active segment criteria (filters, formulas)
  2. Industry ∈ {Tech, SaaS}, EmployeeCount > 50, Title = VP or above
  3. Add/remove contact from static or dynamic lists
  4. Recalculate list membership on field changes
  5. Track list membership history for campaign exclusion
  6. Trigger campaign enrollment if auto-assign flag is set
- **Inputs**: Contact fields, segment rules, static list membership
- **Outputs**: List membership changes, campaign enrollment, segment count updates
- **Decisions**: Multiple segments matched → enroll in all; No segments matched → remove from all dynamic lists
- **Connected Workflows**: Email campaigns (Marketing 2.2), ABM (Marketing 2.7)
- **SLA**: Near-real-time on update, full recalc nightly
- **Error States**: Circular segment dependency, formula evaluation timeout, too many list memberships per contact
- **Validations**: List membership must be unique per contact per list; static list cannot exceed 500k records (perform)

### 2.6 Account Association
- **Trigger**: Contact creation, contact update (company field), bulk re-parenting
- **Actor**: System, rep
- **Steps**:
  1. Match contact company/domain to existing Account
  2. If match found → set `AccountId`
  3. If no match → create Account or flag for manual association
  4. Set contact role: Decision Maker, Influencer, Champion, User, Blocked
  5. Update Account contact roles report
- **Inputs**: Contact company name, domain, role
- **Outputs**: Account-Contact link, role mapping, account contact count
- **Decisions**: Domain matches multiple accounts → prompt for selection; No account but domain valid → auto-create
- **Connected Workflows**: Account management (3.1), Organization hierarchy (3.2)
- **SLA**: Real-time

### 2.7 GDPR/Privacy Management
- **Trigger**: Contact creation, consent form submission, data subject request, scheduled re-consent
- **Actor**: System, privacy officer, contact (via portal)
- **Steps**:
  1. Capture consent: purpose, channel, timestamp, IP, consent version
  2. Store consent record linked to contact
  3. Process opt-out: suppress from marketing, update `DoNotEmail`, `DoNotCall`, `DoNotTrack`
  4. Handle data subject requests: export, delete, rectify within 30 days
  5. Set data retention expiry based on inactivity
  6. Anonymize or purge expired records on schedule
- **Inputs**: Consent form, preference center choices, data subject request ticket
- **Outputs**: Consent records, suppression list entries, anonymized records, deletion audit
- **Decisions**: Request type = Export → generate JSON/CSV; Request type = Delete → anonymize (not hard delete); Consent version mismatch → flag for re-consent campaign
- **Connected Workflows**: Data management (Ops 3.1), Security compliance (Ops 4.1)
- **SLA**: Deletion/export < 30 days (regulatory); opt-out < 24h
- **Error States**: Cannot delete contact with active opportunities (must flag), partial deletion due to related records
- **Validations**: Right to Erasure must preserve audit logs (anonymize not destroy); consent must be version-stamped

---

## 3. Account / Organization Management

### 3.1 Account Hierarchy
- **Trigger**: Account creation, parent field update, merger/acquisition event
- **Actor**: Admin, system
- **Steps**:
  1. Define parent-child account relationships via lookup field `ParentAccountId`
  2. Set hierarchy level: Global (L0), Region (L1), HQ (L2), Subsidiary (L3)
  3. Roll-up fields: total employees, total opportunities, total revenue (child→parent)
  4. Inherit settings: territory, assignment rules from parent
  5. Visualize hierarchy tree in account detail
  6. On parent change → re-evaluate territory, sharing, roll-up formulas
- **Inputs**: Account records, hierarchy config
- **Outputs**: Hierarchy tree, roll-up field values, territory assignments
- **Decisions**: Account has no parent → top-level; Circular parent reference → block save
- **Connected Workflows**: Territory management (7.1), Account planning (3.2)
- **SLA**: Real-time

### 3.2 Account Planning
- **Trigger**: Quarterly business review, new strategic account creation, rep initiative
- **Actor**: Sales rep, account manager, CSM
- **Steps**:
  1. Assess current state: revenue, products, relationship map, open opportunities
  2. Set goals: expansion revenue, retention rate, product adoption targets
  3. Map stakeholders: executive sponsor, economic buyer, technical buyer, champion
  4. Identify risks: competitor presence, churn signals, support tickets, sentiment
  5. Build action plan: key milestones, tasks, engagement cadence
  6. Share plan with account team, set review date
- **Inputs**: Account data, opportunity history, support history, relationship map
- **Outputs**: Account plan record, stakeholder list, action items, risk register
- **Decisions**: Account classified as Strategic → mandatory annual plan; Standard → optional
- **Connected Workflows**: Relationship mapping (3.3), Health scoring (3.6)
- **SLA**: Plan must be completed within 2 weeks of QBR trigger

### 3.3 Relationship Mapping
- **Trigger**: Account plan creation, contact association, org chart import
- **Actor**: Rep, admin, integration (LinkedIn, OrgChart)
- **Steps**:
  1. Map all contacts at account with roles and influence level
  2. Identify relationship strength (Strong/Weak/None) per rep-contact pair
  3. Map decision flow: who influences whom, who makes final call
  4. Identify gaps: missing stakeholder types (e.g., no technical buyer)
  5. Visualize map in account dashboard
  6. Track coverage ratio: % of stakeholder roles filled
- **Connected Workflows**: Account planning (3.2), Contact management (2.1)
- **SLA**: Updated within account planning cycle

### 3.4 Territory Definition & Assignment
- **Trigger**: Fiscal year start, restructuring, rep departure
- **Actor**: Admin, sales ops, revenue operations
- **Steps**:
  1. Define territory boundaries: geographic (zip, state, country), industry, revenue band, named accounts
  2. Build territory hierarchy: Region → Area → Territory
  3. Assign reps to territories with primary/backup roles
  4. Set capacity per territory: max accounts, max leads per day
  5. Assign accounts/leads via territory match rules
  6. Review coverage gaps: unassigned accounts, lead overflow
- **Connected Workflows**: Lead distribution (1.5), Quota management (7.2)
- **SLA**: Updated start of fiscal, change requests processed within 5 business days

### 3.5 Account Health Scoring
- **Trigger**: Weekly batch, significant event (support ticket, usage drop, renewal)
- **Actor**: System (rules/ML), CSM (manual override)
- **Steps**:
  1. Gather signals: product usage (% active users), support tickets (volume, severity), payment timeliness, NPS score, sentiment from call transcripts
  2. Normalize each signal to 0-100 score
  3. Weight and composite into health score (0-100)
  4. Classify: Green (80-100), Yellow (50-79), Red (0-49)
  5. Flag Red accounts to CSM team for intervention
  6. Log score history for trend analysis
- **Connected Workflows**: Service workflows (3.0), Renewal management
- **SLA**: Weekly recalculation, real-time on critical events

---

## 4. Deal / Pipeline Management

### 4.1 Deal Creation
- **Trigger**: Lead conversion, manual rep action, partner referral, renewal opportunity
- **Actor**: Sales rep, system
- **Steps**:
  1. Populate from lead conversion or blank slate
  2. Set required fields: Amount, Close Date, Stage, Account, Contact Role
  3. Optionally link products (from price book) with quantities
  4. Set default probability based on stage
  5. Assign owner (typically the rep who converted the lead)
  6. Create initial note capturing discovery summary
- **Inputs**: Lead record, quote, product catalog
- **Outputs**: Opportunity record, stage history entry, pipeline report inclusion
- **Decisions**: Amount exceeds auto-convert threshold → require manager approval
- **Connected Workflows**: CPQ (4.5), Forecast (8.1), Stage progression (4.2)
- **SLA**: Real-time

### 4.2 Stage Progression
- **Trigger**: Rep updates stage field, manager override, automation rule
- **Actor**: Sales rep, manager, system
- **Steps**:
  1. Validate progression is forward (except "Lost" → recycle to previous allowed)
  2. Check required fields per stage: e.g., Stage=Proposal requires solution document
  3. Apply stage-dependent probability (10% Prospecting → 90% Negotiation)
  4. Record stage history with timestamp, user, duration
  5. Calculate time-in-stage, flag if stalled > 30 days
  6. Trigger stage-entry actions: send proposal template, assign task for demo
  7. If Stage = Closed Won → trigger order creation
  8. If Stage = Closed Lost → capture loss reason, competitor info
- **Inputs**: Current stage, target stage, field validation rules
- **Outputs**: Stage history record, probability update, notification, action tasks
- **Decisions**: Skipping stages allowed? (config per org); Lost → Warm/Lost or Cold/Lost classification
- **Connected Workflows**: Quote-to-order (5.1), Forecasting (8.1), Win/loss analysis
- **SLA**: Real-time
- **Error States**: Required field missing for stage transition, stage not in picklist, backwards skip

### 4.3 Probability & Commit Status
- **Trigger**: Stage change, manual overrides, forecast calls
- **Actor**: System, rep, manager
- **Steps**:
  1. Set default probability from stage mapping (standard)
  2. Allow rep override: Commit (90-100%), Best Case (50-89%), Pipeline (< 50%)
  3. Allow manager override/override of rep commit
  4. Weighted amount = Probability × Amount
  5. Sum weighted amounts for forecast rollup
  6. Flag deals where probability ≠ stage default for manager review
- **Connected Workflows**: Forecasting (8.1), Pipeline review (4.4)
- **SLA**: Real-time

### 4.4 Pipeline Review
- **Trigger**: Weekly forecast meeting, deal stage change to specific gates
- **Actor**: Sales rep, manager, sales ops
- **Steps**:
  1. Rep presents pipeline: key deals, next steps, close dates, risks
  2. Manager reviews deal velocity, aging, commit status
  3. Identify deals needing intervention: stalled, low engagement, competitor threat
  4. Coach on next step strategy
  5. Update next step, close date, commit status as needed
  6. Document review summary

### 4.5 CPQ (Configure, Price, Quote)
- **Trigger**: Rep clicks "Generate Quote" from opportunity
- **Actor**: Sales rep, system
- **Steps**:
  1. Select product bundle from price book
  2. Configure product options, quantities, service terms
  3. Apply pricing: list price, discounts, promotions, tiered rates
  4. Run validation: inventory check, approval rules, eligibility
  5. Generate quote document (PDF) with terms
  6. Submit for discount approval if discount > threshold
- **Connected Workflows**: Quote-to-order (5.1), Discount approval (5.2)

### 4.6 Deal Close (Win/Loss)
- **Trigger**: Rep sets Stage = Closed Won or Closed Lost
- **Actor**: Rep, system
- **Steps** (Win):
  1. Validate all required fields, documents, approvals
  2. Set Closed Won, capture actual close date, final amount
  3. Generate contract (e-signature trigger)
  4. Create order from quote
  5. Notify fulfillment, provisioning, CSM teams
  6. Enroll customer in onboarding sequence
- **Steps** (Loss):
  1. Capture loss reason: Price, Competitor, Feature Gap, Budget, No Decision
  2. Capture competitor name if applicable
  3. Set Re-engage date if evergreening
  4. Create loss analysis record for reporting
- **Connected Workflows**: Quote-to-order (5.1), Order fulfillment, Onboarding
- **SLA**: Real-time

---

## 5. Quote-to-Order

### 5.1 Quote Generation
- **Trigger**: CPQ output, rep creates quote from opportunity
- **Actor**: Sales rep
- **Steps**:
  1. Populate from opportunity products and price book
  2. Apply customer-specific discounts if within rep authority
  3. Set payment terms, delivery schedule, validity period (30/60/90 days)
  4. Generate quote PDF with branding
  5. Send to customer (email, portal, or e-sign link)
  6. Track quote status: Draft → Sent → Viewed → Accepted/Rejected
- **Connected Workflows**: CPQ (4.5), Discount approval (5.2), E-signature

### 5.2 Discount Approval
- **Trigger**: Discount > rep's authority threshold
- **Actor**: Manager, VP, Finance (escalating tiers)
- **Steps**:
  1. Rep submits discount request with justification
  2. System routes to correct approver based on discount tier
  3. Approver reviews: margin impact, deal size, strategic value
  4. Approve, reject, or counter with modified discount
  5. Notify rep of decision
  6. Updated quote reflects approved discount
- **SLA**: < 4 business hours for tier-1, < 24h for tier-2

### 5.3 Order Creation
- **Trigger**: Quote accepted (e-signature complete)
- **Actor**: System
- **Steps**:
  1. Convert quote to order record
  2. Set order status = "Pending Fulfillment"
  3. Apply billing schedule: one-time, monthly, annual
  4. Create invoice (if one-time) or subscription schedule (if recurring)
  5. Send order confirmation to customer
  6. Notify provisioning team
- **Connected Workflows**: Fulfillment, Invoice generation (Finance 1.1), Subscription management (Finance 2.1)

---

## 6. Sales Cadences / Sequences

### 6.1 Sequence Creation
- **Trigger**: Admin defines new sequence
- **Actor**: Sales ops, manager
- **Steps**:
  1. Define sequence name, goal, target audience
  2. Add steps: Email (template), Call (script), LinkedIn, Task
  3. Set delays between steps (e.g., 2 days after email, 1 day after call)
  4. Set branching rules: if open email → skip next email; if call connects → end sequence
  5. Set finish condition: sequence ends after N steps or on positive response
  6. Activate sequence

### 6.2 Sequence Assignment
- **Trigger**: Lead creation, opportunity stage change, manual enrollment
- **Actor**: System, rep
- **Steps**: Enroll record → start step timer → execute first step action.

### 6.3 Response Detection
- **Trigger**: Email reply, call connected, link clicked, meeting booked
- **Actor**: System
- **Steps**:
  1. Parse inbound email: detect reply, auto-reply, bounce
  2. Classify response: Positive, Negative, Neutral, Out of Office
  3. Log response to sequence step
  4. Execute branching rule (pause, skip, end, advance) per sequence logic

---

## 7. Territory & Quota Management

### 7.1 Territory Definition
- **Trigger**: Annual planning, org restructuring
- **Actor**: RevOps, Sales leadership
- **Steps**:
  1. Define territories with criteria: region, industry, revenue, named accounts
  2. Build hierarchy: Region → Area → Territory → Rep
  3. Assign reps as primary/backup
  4. Run coverage analysis: accounts per rep, leads per rep
  5. Publish territory model, assign records
- **Connected Workflows**: Lead distribution (1.5)

### 7.2 Quota Management
- **Trigger**: Fiscal year start, quarterly refresh
- **Steps**:
  1. Set quota per rep + per territory
  2. Allocate by product/division if multi-line
  3. Track attainment: pipeline coverage, weighted pipeline vs quota
  4. Ramp new reps: reduced quota for first 2 quarters
  5. Adjustments: mid-quarter changes with reason log
- **Inputs**: Quota plan, territory map, rep ramp schedule
- **Outputs**: Quota records, attainment dashboards, adjustment audit

---

## 8. Sales Forecasting

### 8.1 Forecast Pipeline Review
- **Trigger**: Weekly/monthly forecast cycle
- **Actor**: Rep, manager, sales ops
- **Steps**:
  1. Reps review pipeline, set commit status per deal
  2. Managers run rollup: commit, best case, pipeline
  3. Weighted forecast = sum(Amount × Probability)
  4. Commit forecast = sum(deals marked Commit)
  5. Compare to quota: gap analysis
  6. Identify upside (deals in Best Case) and risk (deals slipping)
  7. Submit forecast snapshot (dated) for historical tracking
- **Connected Workflows**: Quota management (7.2), Pipeline management (4.1)

### 8.2 Forecast Accuracy Tracking
- **Trigger**: Month/quarter close
- **Actor**: Sales ops, finance
- **Steps**:
  1. Compare forecasted commit vs actual booked revenue
  2. Calculate accuracy % per rep, per team
  3. Track bias: systemic over-commit or under-commit
  4. Publish forecast accuracy scorecard
  5. Use to calibrate future forecasts
