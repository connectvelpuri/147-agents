# Product Hunt Launch Kit — Sovereign CRM

## Launch Title (3 options)
1. "Sovereign CRM — Open-source alternative to Salesforce with custom fields and pipeline Kanban"
2. "Sovereign CRM: Self-hosted CRM with lead scoring, pipeline forecasting, and webhooks"
3. "Sovereign CRM — The open-source CRM that respects your data and your budget"

## Tagline
"The open-source CRM with custom fields, pipeline Kanban, and lead scoring — free for 5 users, self-hosted forever."

## Description (max 600 chars)
Sovereign CRM is an open-source (AGPL), self-hosted alternative to Salesforce, HubSpot, and Zoho. Built for IT consulting firms and SaaS teams that need CRM power without the per-seat tax.

What's inside:
- Multi-tenant RBAC with field-level permissions
- Contacts & Organizations with automatic dedup
- Custom Fields (9 types — no developer required)
- Global Search across all entities
- Lead Management with 7-factor auto-scoring
- Pipeline Kanban with drag-to-move and weighted forecasting
- Deal Tracking with stage transitions and lost-reason capture
- Webhooks (8 event types, HMAC-signed payloads)
- CSV Import/Export
- First-run Setup Wizard

Stack: Go + Next.js + PostgreSQL + Redis.
License: AGPL v3 (with commercial exception for enterprises).

Try the live demo below or deploy in 2 minutes with Docker Compose.

## First Comment
"We built Sovereign CRM because we were tired of paying $25-50/seat for CRM features we barely use. We wanted something modern, self-hosted, and extensible.

Sprints 1-3 took us 3 weeks and delivered: RBAC, contacts, custom fields (9 types), global search, webhooks, lead scoring, pipeline Kanban, deal forecasting, and a setup wizard.

We're open-sourcing it under AGPL with a commercial exception for enterprise teams.

The live demo is loaded with 50 sample contacts, 20 leads, and 10 deals. You can try it right now without signing up.

Would love your feedback — what's missing? What would make you switch from your current CRM?"

## Maker Comment Strategy
- Reply to every comment within 2 hours for the first 48 hours
- Have a 2-sentence answer prepared for the top 5 likely questions:
  1. "How is this different from Twenty?" → See one-pager
  2. "AGPL? Really?" → Explain commercial exception
  3. "Mobile app?" → Honest: not yet, mobile web works
  4. "Email integration?" → Next sprint
  5. "Can I contribute?" → Yes, here's how (link to CONTRIBUTING.md)

## Screenshots to Capture
1. Dashboard with pipeline health widget
2. Pipeline Kanban with 7 stages, deal cards, forecast bar
3. Custom Fields admin page (9 types)
4. Lead detail page with score breakdown and activity timeline
5. Global search results
6. Deal forecast view

## Launch Checklist
- [ ] Demo URL working and seeded
- [ ] GitHub repo public with README updated
- [ ] CONTRIBUTING.md and CLA merged
- [ ] Pricing page published
- [ ] Discord server ready for incoming traffic
- [ ] Screenshots taken and compressed
- [ ] 48-hour availability for comment replies
- [ ] Notify existing network (Twitter/LinkedIn/email list)

## Hacker News "Show HN" Draft
**Title:** Show HN: Sovereign CRM – self-hosted Salesforce alternative with custom fields and forecasting

**Body:**
We built an open-source CRM because we hated paying per-seat for features we barely use.

Stack: Go + Next.js + PostgreSQL + Redis. Self-hosted with Docker Compose.

Built so far (3 sprints over 3 weeks):
- Contacts & Organizations with dedup
- Custom Fields (9 types – text, number, date, boolean, select, multi, URL, email, phone)
- Lead Management with 7-factor auto-scoring
- Pipeline Kanban with drag-to-move and weighted forecasting
- Deal Tracking with stage transitions
- Webhooks (HMAC-signed payloads)
- RBAC with field-level permissions
- Global Search across all entities
- CSV Import/Export
- Setup Wizard

What's next: Email integration (IMAP/SMTP sync), SSO/SAML, mobile PWA.

AGPL-licensed. Commercial exception available for enterprise teams.

Demo: [demo.sovereigncrm.com]
Repo: [github.com/sovereign-crm/sovereign]

Would love your feedback – especially what's missing or what would make you switch from your current CRM.

---

## Reddit Posts

### r/selfhosted
**Title:** I built a self-hosted Salesforce alternative with custom fields and a pipeline Kanban

**Body:** [Same as HN but emphasize self-hosting angle, Docker Compose, no per-seat cost]

### r/crm
**Title:** We're building an open-source CRM — what features would make you switch?

**Body:** [Ask for feedback, show what's been built, invite to try demo]
