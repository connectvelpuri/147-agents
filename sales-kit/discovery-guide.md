# Customer Discovery Guide — Sovereign CRM

## Objective
Validate (or invalidate) every core assumption before building more features.
Each call should answer: "Does a real person with budget want this product?"

## Stack Ranking
After each call, score the prospect 1-5:

| Criterion | 1 (Weak) | 3 (Neutral) | 5 (Strong) |
|-----------|----------|-------------|------------|
| Pain level | "Our CRM is fine" | "We have some frustrations" | "We're actively looking to switch" |
| Budget availability | "No budget this year" | "Could find budget" | "Budget allocated" |
| Decision authority | "Need to ask my manager" | "I influence decisions" | "I sign the PO" |
| Timeline | "Maybe next year" | "3-6 months" | "This quarter" |
| Self-hosting comfort | "Never heard of Docker" | "We have DevOps" | "We self-host everything" |
| Fit score (you judge) | Wrong industry/size | Adjacent | Perfect ICP |

**Score ≥20:** Champion — fast-track to beta
**Score 12-19:** Interested — nurture with follow-up
**Score <12:** Not a fit — learn from them, don't sell

## CRM Landscape Reference (For Context)

| CRM | Starting Price | Self-Hosted? | Open Source? | Notes |
|-----|:-------------:|:------------:|:------------:|-------|
| Salesforce | $25/seat/mo | No | No | Enterprise standard |
| HubSpot | $20/seat/mo | No | No | Marketing-driven |
| Zoho | $14/seat/mo | No | No | Budget option |
| Twenty | Free (cloud) | Coming | Yes (AGPL) | Most direct competitor |
| SuiteCRM | Free | Yes | Yes (AGPL) | Old UI, mature |
| EspoCRM | Free | Yes | Yes (AGPL) | Lightweight |
| **Sovereign** | **$29/seat/mo (cloud) / Free (self-host)** | **Yes** | **Yes (AGPL)** | **Modern + local-first** |

## Objection Handling (Pre-prepared)

| Objection | Response |
|-----------|----------|
| "Why not Twenty?" | "Twenty is great — and it's our closest peer. The differences: Sovereign has field-level permissions out of the box, a richer pipeline Kanban with forecasting, and custom fields with 9 types today. Twenty has a beautiful UI and more community momentum. If you value features over polish today, try Sovereign." |
| "We need mobile" | "We don't have a native mobile app yet. Mobile web works. If mobile is a dealbreaker, I'm honest: we're targeting desktop-first teams right now. Does everyone on your team work from a laptop?" |
| "We need email integration" | "Email sync is our next sprint (Sprint 4 commitment). Today, you can log communications manually. If email sync is critical, I can show you the integration points and timeline." |
| "AGPL scares us" | "Fair concern. AGPL means any modifications you make and distribute must be open-sourced. If you use it internally (modified or not), no restrictions. We also offer a commercial license for teams that need proprietary use. What's your concern specifically?" |
| "Self-hosting is too much work" | "That's why we offer cloud hosting at $29/seat. If you don't want to manage servers, you don't have to. The self-hosted option is for teams that need data control." |
| "We're locked into Salesforce" | "Migration is hard. I won't pretend it's easy. But the ROI is real on $25/seat to free. We have a migration playbook and CSV import. Want to try a side-by-side for 30 days?" |
| "How do I know you'll be around in 2 years?" | "Open-source projects don't die the same way startups do. If we disappear, your code and data are still on your server, under a license that lets you continue. That said, we're building a community and welcome your contributions." |
| "We need SSO" | "SSO is on our roadmap (Sprint 5). For now, we support JWT-based auth with MFA. What SSO provider do you use? We'll prioritize it." |

## Post-Call Log Template

Save to: vault/customer-interviews/YYYY-MM-DD-company.md

```markdown
# Customer Interview: [Company Name]

**Date:** YYYY-MM-DD
**Contact:** [Name], [Title]
**Source:** [How they were found]
**Current CRM:** [Tool]
**Team Size:** [N] users

## Pain Points
- [What they hate most about current CRM]
- [What they wish was different]
- [What would make them switch]

## Key Quotes
> "..."

## Scoring
- Pain Level: /5
- Budget: /5
- Authority: /5
- Timeline: /5
- Self-Host Fit: /5
- **Total: /25**

## Verdict
[Champion / Interested / Lukewarm / Not a fit]

## Follow-up
- [ ] Send demo link
- [ ] Schedule follow-up
- [ ] Add to beta list
- [ ] Introduce to [other contact]

## Surprises
[Anything that contradicted our assumptions]

## Notes
[Free-form]
