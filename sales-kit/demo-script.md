# Sovereign CRM — Demo Script (15 minutes)

## Audience: IT Consulting / SaaS founders, CTOs, Sales Ops directors
## Goal: Get them to say "I want to try this" — not close a deal, open a conversation

### Pre-Call Checklist
- [ ] Docker Compose running locally (or demo URL ready)
- [ ] Seed data loaded (50 contacts, 20 leads, 10 deals)
- [ ] Screen recorder ready (Loom / OBS)
- [ ] Pricing page open in a second tab
- [ ] Competitor comparison ready in notes
- [ ] Logged in as admin@sovereign.local
- [ ] Audio/video confirmed

---

### 0:00-2:00 — Context & Permission
"Thanks for taking the call. I'm building a CRM for [IT Consulting / SaaS] teams.
I want to show you what we've built so far and get your honest feedback — what's useful,
what's missing, and whether you'd consider switching from [their current CRM]."

**Key question to ask first:**
"Before I dive in — what CRM do you use today, and what's your single biggest frustration with it?"

*Write down their answer. Use it during the demo.*

---

### 2:00-5:00 — Value Prop (3 sentences)
1. "Sovereign CRM is built for teams that have outgrown spreadsheets but don't want
   Salesforce complexity or HubSpot pricing."
2. "It's open-source and self-hosted — your data stays on your infra, no per-seat tax."
3. "We focused on what actually matters: contacts, pipeline, deals, and the ability to
   add custom fields without a developer."

*Don't mention CRDTs, Go, or Postgres unless they ask. Sell outcomes, not architecture.*

---

### 5:00-8:00 — Live Demo (Show, Don't Tell)

#### Dashboard (30 seconds)
"Here's the dashboard — pipeline health, open leads, upcoming tasks. Your team's
daily pulse at a glance."

#### Custom Fields (1 min) ← CRITICAL 
"Most CRMs lock you into their data model. Here I can add a text field,
a dropdown, a date — whatever we need — in 30 seconds. No code."
*Create a new custom field live: 'Account Tier' as a select field with Gold/Silver/Bronze.*

#### Pipeline Kanban (1 min) ← VISUAL IMPACT
"Here's the pipeline. I can drag a deal from Proposal to Negotiation,
the probability updates automatically, and the forecast recalculates."
*Drag one deal live. Point out the forecast bar at the top.*

#### Lead Scoring (30 seconds)
"Leads are auto-scored based on title, source, and engagement. Sales reps
know exactly where to focus — no more guessing which lead to call first."

#### Global Search (30 seconds)
"The search bar at the top searches contacts, organizations, and deals
simultaneously. One box, everything."

---

### 8:00-12:00 — Discovery (This is where you learn)

Ask in order. Write down every answer verbatim.

1. **"What CRM are you on now, and what do you pay?"**
   - Establishes baseline. Tells us budget and migration complexity.

2. **"What would make you switch?"**
   - Open-ended. Listen for tension points.

3. **"If you could wave a magic wand, what would your CRM do that it doesn't today?"**
   - Uncovers unmet needs. Future roadmap input.

4. **"How many people on your team need CRM access?"**
   - Tells us seat count and tier.

5. **"How important is self-hosting to you vs. having someone else manage it?"**
   - Tests our core thesis. If they say "I'd rather pay $50/seat than manage a server," take notes.

6. **"Do you use CRM on mobile? How much?"**
   - Validates mobile priority.

7. **"What integrations would you need to consider switching?"**
   - Email, calendar, Slack, accounting, etc.

8. **"What would a reasonable monthly price be for a CRM that does everything we just showed?"**
   - Willingness to pay. Don't lead them — let them name the number.

9. **"If we had a hosted version ready in 30 days, would you pay $29/seat/month?"**
   - Direct WTP test at our target price.

10. **"Who else on your team should I talk to?"**
    - Next step and potential champion.

---

### 12:00-14:00 — Pricing (Show the Page)

"Here's our pricing. We're intentionally transparent:"

- **Free tier:** 5 users, core features
- **Team:** $29/seat/month — custom fields, pipeline, webhooks
- **Enterprise:** Custom — SSO, audit, self-hosted support, SLA

**Ask:** "Where does your team land on this?"

---

### 14:00-15:00 — Next Steps

"If you're interested, here's what I'd suggest:"

1. I'll send you a link to try it yourself
2. You get 30 min with a fully loaded demo
3. We schedule a follow-up in 2 weeks to discuss any questions

**Get the commitment:** "Can I send you the demo link today?"

---

## Post-Call (Within 30 minutes)

1. Log the call in the vault: customer-interviews/YYYY-MM-DD-company.md
2. Update CONTACT_FINDINGS.md with any surprises or pattern breaks
3. Tag the person as:
   - **Champion** — enthusiastic, would buy, introduced us to others
   - **Interested** — engaged, wants to follow up
   - **Lukewarm** — polite but no clear signal
   - **Not a fit** — wrong industry, wrong size, wrong problem
4. If Champion: add to beta waitlist and schedule deep-dive
5. If Interested: send demo link + follow-up calendar invite
