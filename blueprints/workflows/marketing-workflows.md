# Marketing Workflows — Complete Map

## 1. Campaign Management

### 1.1 Campaign Brief & Planning
- **Trigger**: Marketing calendar event, product launch, demand gen goal
- **Actor**: Marketing manager, campaign owner, creative lead
- **Steps**:
  1. Define campaign objective: Awareness, Lead Gen, Engagement, Retention, Upsell
  2. Set KPIs: impressions, clicks, conversion rate, pipeline generated, ROI
  3. Identify target audience: segments, personas, account lists
  4. Set budget, timeline, channel mix
  5. Create creative brief: messaging, value prop, CTA, visuals
  6. Approve brief by marketing leadership
- **Inputs**: Campaign request, marketing calendar, budget allocation
- **Outputs**: Campaign record, creative brief, KPI targets, budget envelope
- **Decisions**: Campaign type = Always-On vs Blast vs Multi-wave → different execution paths
- **Connected Workflows**: Audience segmentation (2.5), Channel selection (1.3), Assets (1.4)
- **SLA**: Brief approval within 5 business days

### 1.2 Audience Definition & Segmentation
- **Trigger**: Campaign brief approval
- **Actor**: Marketing ops, campaign manager
- **Steps**:
  1. Define segment criteria: firmographic, demographic, behavioral, intent
  2. Build segment list (static) or criteria (dynamic)
  3. Estimate reach: total addresses, expected response rate
  4. Set exclusion rules: current customers (for acquisition), competitors, unsubscribes
  5. Validate sample: 50 records check for fit
  6. Save audience as campaign target
- **Inputs**: Segment criteria, CRM data, exclusion lists
- **Outputs**: Target audience list/population, reach estimate
- **Connected Workflows**: Contact segmentation (Sales 2.5), Campaign execution

### 1.3 Channel Selection & Orchestration
- **Trigger**: Campaign planning phase
- **Actor**: Campaign manager
- **Steps**:
  1. Select channels: Email, Social (LinkedIn/FB), Display, SEM, Events, Direct Mail, SMS
  2. Define channel sequence: email first → retarget social → direct mail
  3. Set channel-specific budgets per channel mix
  4. Configure tracking: UTM params per channel, phone numbers, landing pages
  5. Define cross-channel suppression: contacted via email → exclude from SMS for 48h
- **Connected Workflows**: Email marketing (2.2), Lead generation (2.3)

### 1.4 Asset Creation & Approval
- **Trigger**: Campaign brief approved
- **Actor**: Content creator, designer, copywriter, reviewer
- **Steps**:
  1. Create assets: emails, landing pages, social posts, ads, videos, whitepapers
  2. Submit for review (legal, brand, compliance)
  3. Run A/B variants for testing
  4. Version control and asset library storage
  5. Final approval before launch
- **Connected Workflows**: Content marketing (2.4)

### 1.5 Campaign Launch
- **Trigger**: All assets approved, audience ready
- **Actor**: Marketing ops, campaign manager
- **Steps**:
  1. Schedule launch date/time per channel
  2. Run QA playbook: send test emails, click links, verify tracking, check unsub link
  3. Activate campaign: deploy emails, activate ads, publish landing pages
  4. Monitor initial launch: delivery rate, errors, spam complaints
  5. Set phase timers for multi-wave campaigns
- **Inputs**: Approved assets, audience lists, channel configs
- **Outputs**: Live campaign, tracking pixels, UTM links, delivery confirmations
- **Decisions**: Suppression file update required? → trigger data sync; ISP throttling → adjust send rate
- **Connected Workflows**: Email delivery (2.2), Lead generation tracking (2.3)
- **SLA**: Campaign launch within designated time window (±15 min)
- **Error States**: Template render failure, list missing required fields, ESP reject, URL shortener down

### 1.6 Multi-Wave Execution
- **Trigger**: Campaign has multiple waves scheduled
- **Actor**: System (automated), campaign manager (trigger)
- **Steps**:
  1. Wave 1 sends to full audience
  2. Track opens/clicks/conversions over wave window
  3. Wave 2: send to non-openers with different subject line
  4. Wave 3: send to openers but non-clickers with different CTA
  5. Wave N: send to converters with upsell or thank-you
  6. Suppress converters from future waves
  7. End campaign after final wave

### 1.7 Campaign Tracking & Attribution
- **Trigger**: Campaign live, continuous
- **Actor**: System
- **Steps**:
  1. Track interactions: email opens, clicks, page visits, form fills, ad clicks
  2. Apply attribution model: first-touch, last-touch, multi-touch (linear/U-shaped)
  3. Map interactions to campaign and channel
  4. Update campaign member status: Sent → Opened → Clicked → Converted
  5. Calculate campaign influence on pipeline and revenue
  6. Roll up to campaign ROI reports
- **Inputs**: Interaction events, attribution model config
- **Outputs**: Campaign member records, attribution data, ROI calculations
- **Connected Workflows**: Lead generation (2.3), Revenue reporting (Finance 1.1)

### 1.8 Campaign Analysis & Optimization
- **Trigger**: Campaign end, milestone (mid-campaign)
- **Actor**: Marketing manager, campaign owner
- **Steps**:
  1. Compile KPI results vs targets: sends, delivery %, open %, click %, conversion %, cost/lead, ROI
  2. Compare A/B test results with statistical significance
  3. Segment performance analysis: which segments performed best
  4. Channel performance: CPA per channel
  5. Generate campaign report
  6. Document learnings for next campaign iteration

---

## 2. Email Marketing

### 2.1 Template Management
- **Trigger**: Campaign creation, new template request
- **Actor**: Designer, marketing ops
- **Steps**:
  1. Design HTML email template (responsive)
  2. Test rendering across clients: Outlook, Gmail, Apple Mail, mobile
  3. Add personalization fields: `{{FirstName}}`, `{{Company}}`, dynamic content blocks
  4. Add required elements: unsubscribe link, physical address, CAN-SPAM footer
  5. Version and store in template library
  6. Assign template categories: Newsletter, Promo, Event, Nurture, Transactional

### 2.2 Email Send & Delivery
- **Trigger**: Campaign launch, trigger-based automation
- **Actor**: System (ESP)
- **Steps**:
  1. Validate list: remove bounces, unsubscribes, spam traps, invalid format
  2. Apply sending limits: per-ISP throttling, warm-up schedule
  3. Personalize content per recipient
  4. Send via ESP (Salesforce MC, HubSpot, Marketo)
  5. Track delivery: sent, bounced (soft/hard), delivered, spam complaint
  6. Process feedback loops from ISPs (AOL, Yahoo, Microsoft)
  7. Update contact status: hard bounce → suppress permanently; soft bounce → retry, suppress after 3
  8. Monitor deliverability: inbox placement rate, sender reputation
- **Inputs**: Campaign, email template, recipient list, sending config
- **Outputs**: Sent emails, delivery log, bounce records, spam complaints
- **Decisions**: Hard bounce → suppress, soft bounce → retry after 24h (max 3)
- **Connected Workflows**: Campaign tracking (1.7), Lead generation (2.3)
- **SLA**: Batch sends within schedule window; transactional sends real-time
- **Error States**: ESP API timeout, DNS failure on sending domain, DMARC reject, rate-limited by ISP
- **Validations**: List size vs sending reputation; CAN-SPAM compliance mandatory; suppression list applied before send

### 2.3 A/B Testing
- **Trigger**: Campaign with A/B test configured
- **Actor**: System
- **Steps**:
  1. Split test group (default 20% of list)
  2. Send variant A (subject line A) to half of test group
  3. Send variant B (subject line B) to other half
  4. Wait for test duration (default 4h or 100 opens)
  5. Statistical analysis: pick winner at 95% confidence
  6. Send winning variant to remaining 80% of list
- **Connected Workflows**: Campaign optimization (1.8)
- **SLA**: Test duration configurable 1-24h

### 2.4 Email Analytics
- **Trigger**: Ongoing after send
- **Steps**: Track open rate, click rate, CTR, conversion rate, unsub rate → weekly digest

---

## 3. Lead Generation

### 3.1 Landing Pages & Forms
- **Trigger**: Campaign requires capture page
- **Actor**: Marketing ops, web team
- **Steps**:
  1. Define form fields (progressive profiling)
  2. Build landing page with CTA and form
  3. Add tracking: Google Analytics, UTM capture, pixel
  4. Set confirmation: thank-you page, auto-responder email
  5. Create lead record on form submission
  6. Test form: submit, validation, error handling
- **Connected Workflows**: Lead capture (Sales 1.1), Campaign tracking (1.7)

### 3.2 Lead Routing
- **Trigger**: Form submission, lead created
- **Actor**: System
- **Steps**:
  1. Determine lead source and campaign
  2. Apply routing rules: region, product interest, lead score
  3. Assign to SDR/BDR queue or round-robin
  4. Notify assigned rep
  5. Set SLA timer for first contact
- **Connected Workflows**: Lead distribution (Sales 1.5), MQL→SAL handoff (Cross 1.1)

### 3.3 Lead Attribution
- **Trigger**: Lead conversion to opportunity
- **Actor**: System
- **Steps**:
  1. Trace first-touch campaign: first campaign that created the lead
  2. Trace last-touch campaign: campaign that drove conversion
  3. Trace multi-touch: all campaigns touched
  4. Apply attribution weights per model
  5. Report pipeline revenue by campaign source

---

## 4. Content Marketing

### 4.1 Topic Research & Calendar
- **Trigger**: Content strategy cycle, SEO gap analysis
- **Actor**: Content manager, SEO specialist
- **Steps**:
  1. Research keywords, competitor content, industry trends
  2. Prioritize topics by search volume, relevance, funnel stage
  3. Create content calendar with deadlines, authors, channels
  4. Assign content pieces to writers/designers
  5. Track content production pipeline: Idea → Draft → Review → Published

### 4.2 Content Distribution & Engagement
- **Trigger**: Content published
- **Actor**: Content manager, social team
- **Steps**:
  1. Distribute: blog post → email newsletter → LinkedIn → Twitter → industry pubs
  2. Track engagement: views, shares, comments, backlinks, downloads
  3. Collect leads from gated content (whitepapers, webinars)
  4. Score engagement and pass to SDRs for follow-up

---

## 5. Event Management

### 5.1 Event Planning
- **Trigger**: Event added to marketing calendar
- **Actor**: Event manager, marketing team
- **Steps**:
  1. Define event type: Webinar, Conference, Roadshow, User Group
  2. Set date, venue (virtual/physical), capacity, budget
  3. Create event page with registration form
  4. Set up ticketing/payment if paid
  5. Plan agenda, speakers, sponsors
  6. Create promotional plan: email, social, paid

### 5.2 Event Registration & Check-in
- **Trigger**: Registration form submission
- **Actor**: System, event staff (check-in)
- **Steps**:
  1. Capture registrant data + session preferences
  2. Send confirmation email with calendar link
  3. Send reminder sequence (T-7, T-1, T-0)
  4. At event: check-in via QR code, badge print
  5. Track attendance: arrived, session attended, booth visited
- **Connected Workflows**: Lead capture (Sales 1.1), Event follow-up (5.3)

### 5.3 Event Follow-up & ROI
- **Trigger**: Event ends
- **Actor**: Marketing ops, SDR team
- **Steps**:
  1. Send thank-you email with resources, recording
  2. Score attendees by engagement: sessions attended, booth scans
  3. Route hot leads to SDRs within 24h
  4. Non-attendees: send recording, re-engage sequence
  5. Calculate event ROI: total cost vs pipeline generated
- **SLA**: Hot leads routed within 24h of event end

---

## 6. Account-Based Marketing (ABM)

### 6.1 Account Selection & Tiering
- **Trigger**: Quarterly planning, ICP refresh
- **Actor**: ABM manager, sales
- **Steps**:
  1. Define ICP criteria: industry, revenue range, tech stack, growth signals
  2. Score target accounts by fit + intent
  3. Tier accounts: Tier 1 (1:1), Tier 2 (1:few), Tier 3 (1:many)
  4. Assign ABM programs per tier
  5. Identify buying group contacts per account

### 6.2 ABM Orchestration
- **Trigger**: Account selection complete
- **Actor**: ABM platform (Demandbase, 6sense), marketing ops
- **Steps**:
  1. Run targeted ads to buying group members
  2. Send personalized direct mail
  3. Trigger sales plays when engagement detected
  4. Orchestrate multi-channel touches: Ad → Visit → Email → Call
  5. Track engagement across channels at account level

### 6.3 ABM Measurement (ROI)
- **Trigger**: Campaign cycle end
- **Steps**:
  1. Account engagement score (AES): % of target contacts engaged × depth
  2. Pipeline influenced vs target accounts
  3. Revenue from target accounts
  4. Compare ABM vs demand gen ROI per account tier
