# Customer Service Workflows — Complete Map

## 1. Ticket / Case Management

### 1.1 Case Creation
- **Trigger**: Customer email to support@, portal submission, chat transcript, phone call, social DM, API/integration
- **Actor**: Customer (self-service), agent, system (auto-creation from email)
- **Steps**:
  1. Ingest from channel: parse email subject/body, extract portal form fields, transcribe chat
  2. Identify customer: match email/phone/account number to existing contact
  3. If unknown → create as "Guest" contact with limited profile
  4. Auto-categorize: Product, Billing, Technical, Account, General
  5. Set initial priority: P1 (Critical), P2 (High), P3 (Medium), P4 (Low)
  6. Assign default case number, status = "New"
  7. Check for existing cases by same customer → surface "Related Cases" to agent
  8. Apply auto-response: "We've received your request, reference #12345"
- **Inputs**: Customer message, contact info, product/order context from portal
- **Outputs**: Case record, auto-response email, notification to queue
- **Decisions**: Customer has active contract → set entitlements; Known issue → link to KB article; Portal submission → already has account context
- **Connected Workflows**: Omnichannel inbox (2.1), Knowledge base (3.1), SLA management (5.1)
- **SLA**: Case creation < 1s; auto-response < 5 min
- **Error States**: Email unparseable, customer not identified (orphan case), attachment too large
- **Validations**: Required fields per case type; contact lookup must match at least email or phone

### 1.2 Case Categorization & Prioritization
- **Trigger**: Case creation, agent update
- **Actor**: System (AI/ML), agent
- **Steps**:
  1. Apply NLP classification: intent, product, subcategory (e.g., "Login issues" under "Technical")
  2. Extract sentiment: Positive, Neutral, Negative, Angry
  3. Set priority based on: customer tier (VIP→priority+1), contract SLA, issue impact
  4. Add tags: `[bug]`, `[feature-request]`, `[refund]`, `[escalation]`
  5. Check for known solution: if match > 90% in KB, suggest article to agent/customer
  6. Route to appropriate queue based on category + priority
- **Inputs**: Case text, contact tier, contract SLA, KB database, sentiment model
- **Outputs**: Category, priority, tags, suggested KB, queue assignment
- **Decisions**: Category confidence < 70% → mark "Uncategorized", manual review needed; VIP customer → auto-escalate priority one level; Known solution found → route to deflection path
- **Connected Workflows**: SLA management (5.1), Knowledge base (3.1)
- **SLA**: Real-time classification
- **Error States**: Classification model confidence too low across all categories, tag limit exceeded
- **Validations**: Category must exist in taxonomy; priority must be valid for contract SLA

### 1.3 Case Assignment
- **Trigger**: Case created, categorization complete, SLA breached
- **Actor**: System (assignment engine), supervisor (manual)
- **Steps**:
  1. Check skill-based routing: category → team (e.g., Billing → Finance team)
  2. Check capacity: agent has < max active cases
  3. Check availability: agent logged in, not on break, not at capacity
  4. Assign: round-robin within skill group, or by least active cases
  5. If P1 → assign immediately + notify supervisor + send SMS alert to agent
  6. Set assignment SLA timer
- **Inputs**: Case category, skill mapping, agent status, capacity limits
- **Outputs**: Assigned agent, notification, SLA timer start
- **Decisions**: No agent available in skill group → queue to group, escalate to supervisor; P1 + no agent → supervisor automatically assigned
- **Connected Workflows**: User management (Ops 1.1), SLA management (5.1)
- **SLA**: P1 < 5 min, P2 < 15 min, P3 < 1h, P4 < 4h
- **Error States**: All agents at capacity, skill group missing, agent status not synced
- **Validations**: Agent must have active license, correct skill set, and not be on leave

### 1.4 Case Diagnosis & Resolution
- **Trigger**: Agent accepts case
- **Actor**: Support agent
- **Steps**:
  1. Review case details: description, history, customer info, product, related cases
  2. Research: search KB, internal docs, colleague, or escalate to L2/L3
  3. Diagnose: reproduce issue, check logs, verify configuration
  4. Apply solution: provide instructions, change config, submit refund, file bug
  5. Set resolution type: Solved, Workaround, Duplicate, Won't Fix, Escalated
  6. Update case with resolution notes
  7. If solved → move to closure step
- **Inputs**: Case, KB articles, diagnostic tools, escalation team
- **Outputs**: Resolution notes, resolution type, solution applied
- **Decisions**: Cannot resolve → escalate to L2/L3 with diagnostic summary; Bug confirmed → file internal bug report, link case to bug; Customer unsatisfied → offer alternative or escalate to supervisor
- **Connected Workflows**: Knowledge base (3.1), Escalation, Bug tracking
- **SLA**: Based on priority: P1 < 4h, P2 < 8h, P3 < 48h, P4 < 5 business days
- **Error States**: Diagnostic tool unavailable, escalation not picked up, solution does not resolve issue
- **Validations**: Resolution notes required before close; resolution type must be selected

### 1.5 Case Closure & CSAT
- **Trigger**: Agent marks case as Solved
- **Actor**: Agent, system, customer
- **Steps**:
  1. Set case status = "Pending Customer Confirmation" (if not auto-close)
  2. Send satisfaction survey (CSAT/NPS) to customer
  3. Wait for customer response or close timer (24-72h)
  4. Customer confirms solved → status = "Closed"
  5. No response from customer in N hours → auto-close
  6. Customer marks as Unsolved → case re-opened, status back to "In Progress"
  7. On close: calculate handle time, resolution time, update CSAT score
- **Inputs**: Case, survey template, auto-close timer config
- **Outputs**: Closed case, survey response, CSAT score, case metrics
- **Decisions**: Customer did not respond → auto-close, but send a final follow-up email; Customer reply after auto-close → reopen with reference
- **Connected Workflows**: CSAT/NPS (6.1), Knowledge base (3.1)
- **SLA**: Survey sent immediately; auto-close after configurable window (24-72h)
- **Error States**: Survey send fails, CSAT calculation error, case stuck in pending state
- **Validations**: Closed cases cannot be edited (read-only); reopen must create new audit trail entry

---

## 2. Omnichannel Inbox

### 2.1 Channel Reception & Identification
- **Trigger**: Inbound message on any channel
- **Actor**: System
- **Steps**:
  1. Receive: Email, Chat, SMS, WhatsApp, Facebook Messenger, Twitter DM, Instagram DM, Voice call
  2. Normalize message into universal message format
  3. Identify contact: match sender identity across channels (email cross-ref from chat)
  4. Create/retrieve contact + conversation thread
  5. Append message to conversation history
- **Inputs**: Raw message from channel webhook/API
- **Outputs**: Normalized message, conversation thread, contact matched
- **Connected Workflows**: Case creation (1.1)
- **SLA**: Real-time

### 2.2 Agent Desktop & Macros
- **Trigger**: Agent opens conversation
- **Actor**: Agent
- **Steps**:
  1. View entire conversation history (all channels merged)
  2. Use canned responses (macros) for common replies
  3. Insert dynamic fields: customer name, case number, KB links
  4. Apply formatting: rich text, code blocks, attachments
  5. Submit response → sent via original channel
  6. Update wrap-up fields: category, resolution type, notes before moving to next
- **Connected Workflows**: Macros management, Case resolution (1.4)

### 2.3 Conversation Routing
- **Trigger**: New conversation without existing assignment
- **Actor**: System
- **Steps**:
  1. Check if existing open case for this customer → append to case
  2. If new → create case (or link if same issue)
  3. Route to agent via skill-based + capacity rules (same as 1.3)
  4. If chat → route to available agent immediately
  5. If after-hours → offer callback request or bot deflection

---

## 3. Knowledge Base

### 3.1 Article Drafting & Categorization
- **Trigger**: Knowledge gap identified, agent request, product release
- **Actor**: Content writer, SME, support agent
- **Steps**:
  1. Identify need: FAQ from support tickets, new feature documentation
  2. Draft article with structured format: Title, Summary, Steps, FAQ, Related
  3. Categorize: Product, Topic, Feature, Audience (Customer/Internal)
  4. Add metadata: keywords for search, product version, effective date
  5. Set visibility: Public (customer portal), Internal (agent only)
  6. Submit for review

### 3.2 Article Review & Publishing
- **Trigger**: Article drafted
- **Actor**: Reviewer, content manager
- **Steps**:
  1. Fact-check accuracy, test steps
  2. Verify brand tone, formatting, accessibility
  3. Approve or return with edits
  4. Schedule publish date (immediate or timed with release)
  5. Archive old version, link to new version
  6. Notify agents of new article

### 3.3 Search & Deflection
- **Trigger**: Customer search on portal, agent search in console
- **Actor**: System (search engine), customer, agent
- **Steps**:
  1. Parse query: apply NLP to understand intent
  2. Search KB: full-text + keyword + tag search
  3. Rank results by relevance + popularity
  4. Display top 5 results with match highlights
  5. If customer clicks and resolves → deflection tracked
  6. If unhelpful → prompt to create case
- **Connected Workflows**: Self-service portal (4.1), Case deflection
- **SLA**: Search results < 2s

### 3.4 KB Feedback & Analytics
- **Trigger**: Article viewed, feedback submitted
- **Actor**: System
- **Steps**:
  1. Track: views, helpful clicks, not helpful clicks, search-to-article ratio
  2. If article has > 30% "Not Helpful" → flag for review
  3. Report top-searched terms that return no results → content gap
  4. Report top deflection articles → highlight as best practice

---

## 4. Self-Service Portal

### 4.1 Portal Access & Search
- **Trigger**: Customer visits portal (authenticated or guest)
- **Actor**: Customer
- **Steps**:
  1. Authenticate (SSO, email+password, magic link) or browse as guest
  2. Show personalized dashboard: open cases, account info, recommended articles
  3. Search KB (see 3.3) — auto-suggest, recent searches, popular articles
  4. Track search-to-resolution funnel

### 4.2 Ticket Creation via Portal
- **Trigger**: Customer can't find answer
- **Actor**: Customer
- **Steps**:
  1. Pre-fill customer info from authenticated session
  2. Dynamic form based on category selection
  3. Show suggested articles as they type description (real-time)
  4. Submit → case created, confirmation displayed
  5. Option to upload files (screenshots, logs)

### 4.3 Community & Live Chat
- **Trigger**: Customer clicks "Community" or "Chat"
- **Actor**: Customer, system
- **Steps**:
  1. Community: browse forums, ask question (community answer)
  2. Chat: trigger bot (initial triage) → route to live agent if needed
  3. Chat transcript saved to case on creation

---

## 5. SLA Management

### 5.1 SLA Definition & Assignment
- **Trigger**: Contract signed, SLA template defined
- **Actor**: Admin, operations
- **Steps**:
  1. Define SLA: P1 first response < 1h, resolution < 4h; P2 first response < 4h, resolution < 24h
  2. Set business hours: 9am-6pm M-F, exclude holidays
  3. Set breach actions: notify supervisor, escalate, auto-penalty
  4. Assign SLA to contracts or case types
  5. Priority override per customer tier

### 5.2 SLA Timer & Breach Monitoring
- **Trigger**: Case created, SLA timer started
- **Actor**: System
- **Steps**:
  1. Start first-response timer on case creation
  2. Pause timer when awaiting customer response
  3. Start resolution timer on assignment
  4. Alert at 75% of SLA (warning), 100% (breach)
  5. On breach: notify supervisor, auto-escalate, log breach
  6. Track SLA compliance % per agent/team

---

## 6. CSAT / NPS Management

### 6.1 Survey Design & Deployment
- **Trigger**: Case closed, periodic (NPS), after interaction
- **Actor**: Admin, CX team
- **Steps**:
  1. Design survey: CSAT (1-5 scale), NPS (0-10), follow-up question
  2. Map to trigger events: case close → CSAT, quarterly → NPS, after chat → CES
  3. Set timing: send 1h after resolution, close survey after 7 days
  4. Configure language localization based on customer language

### 6.2 Response Collection & Analysis
- **Trigger**: Customer submits survey
- **Actor**: System, CX team
- **Steps**:
  1. Capture response: score, free-text comment
  2. Categorize comments: sentiment analysis, topic extraction
  3. Update contact/account with CSAT/NPS score
  4. Alert on Detractor (NPS 0-6) → trigger call-back request
  5. Report trends: CSAT by team, agent, product, time period
  6. Track actions taken from low-score feedback

### 6.3 Action Tracking
- **Trigger**: Detractor response, score drop trend
- **Actor**: CX manager, support manager
- **Steps**:
  1. Create action item from negative feedback
  2. Assign owner for root cause analysis
  3. Track action completion
  4. Follow-up survey after action to measure improvement
  5. Close action loop
