# Standing Committee 1: Community & Ecosystem Charter

**Governed by:** Constitution Article VII
**Domain:** Governance, contributor funnel, marketplace, events
**Bi-weekly meeting:** Thursday 10:00 UTC, async-first

---

## COMMITTEE MANDATE

Build and sustain an open-source community that contributes code, documentation, integrations, and plugins. Measured by contributor growth, PR velocity, and ecosystem breadth.

---

## ECOSYSTEM FLYWHEEL

```
Visitor -> Star -> Clone -> Run -> Use -> Report Bug
   |
   v
Contributor
   |
   v
Maintainer <----- Committer <----- Regular Contributor
   |
   v
Ecosystem (plugins, integrations, courses, jobs, consulting)
   |
   +-------> More Visitors
```

## CONTRIBUTOR FUNNEL METRICS

| Stage | Metric | Monthly Target |
|-------|--------|:--------------:|
| Visitor | Unique repo visitors | 5,000 |
| Star | Stars | 500 |
| Clone | Unique cloners | 200 |
| Run | Setup completions | 100 |
| First PR | First-time contributors | 20 |
| Repeat PR | 3+ contributions | 5 |
| Committer | Commit access | 3 |
| Ecosystem | Packages/plugins | 10 |

## GOVERNANCE MODEL

Per Constitution Article VI:
- BDFL: Founder (final decision on product direction)
- Core Maintainers (up to 5): RFC approvals, technical direction
- Committers (up to 20): Merge in domain, triage
- Contributors (unlimited): PRs, issues, docs

## CONTRIBUTOR EXPERIENCE STANDARDS

| Metric | Target | Enforcement |
|--------|:------:|-------------|
| First PR review time | < 24 hours | Auto-assign reviewer on PR creation |
| PR merge time (non-contentious) | < 72 hours | Stale PR bot pings after 48h |
| Issue first response | < 4 hours (business hours) | Auto-respond with triage template |
| Bug fix release cadence | Within 7 days of merge | Hotfix branch for critical bugs |
| Setup time (new developer) | < 5 minutes | Tracked in DX committee |

## ECOSYSTEM INCENTIVES

| Party | Why They Participate | Our Support |
|-------|---------------------|-------------|
| Developer building on CRM | Access to customer base | API docs, plugin SDK, marketplace listing |
| Consultant/agency | Implementation revenue | Certified partner program, referral fee |
| Integrator (SaaS vendor) | Distribution channel | Co-marketing, featured integration |
| Individual contributor | Resume, learning, community | Maintainer title, conference talks, swag |

## MARKETPLACE STRATEGY

| Phase | Timing | Model |
|-------|--------|-------|
| Beta | Day 1 | Open plugins (no marketplace, just a directory) |
| v1 | Month 6 | Curated plugin directory. Free to list. |
| v2 | Month 12 | Paid plugins (developer keeps 80%, project takes 20%) |
| v3 | Month 18 | Certification program, premium support ecosystem |

## COMMUNITY COMMUNICATION CHANNELS

| Channel | Purpose | SLA |
|---------|---------|:---:|
| GitHub Issues | Bug reports, feature requests | First response < 4h |
| GitHub Discussions | Q&A, RFCs, community support | First response < 8h |
| Discord | Real-time chat, help, community | Best-effort |
| Blog | Release notes, tutorials, case studies | 2 posts/month |
| X/Twitter | Announcements, community highlights | 5 posts/week |
| Monthly Newsletter | Updates, featured plugins, contributor spotlight | 1st of every month |

## FORK STRATEGY

Forking is natural and healthy. We do not:
- Attempt to prevent forks (license allows them)
- Attack or disparage forks
- Compete with forks for features

We do:
- Maintain clear differentiation
- Keep our community welcoming
- Accept patches from forks if contributors want to upstream

## SUCCESSION PLAN

If the BDFL disappears:
1. Core Maintainers assume BDFL responsibilities as a steering committee
2. Steering committee appoints a new BDFL within 90 days
3. If no consensus, the project transitions to a foundation model
4. Funds (if any) transferred to a legal entity controlled by Core Maintainers


## Organizational Change Management (OCM) — Added per Sprint 2.5

### Mandate
Drive user adoption, training, and organizational readiness for Sovereign CRM. OCM is the #1 predictor of CRM success — without it, the best technology fails.

### Principles
1. **Adoption is designed, not measured** — Build for user success from day 1, don't just track failure after launch
2. **Role-based enablement** — Sales Rep, Manager, Admin each need distinct onboarding paths
3. **Continuous adoption** — Not a one-time training event; ongoing reinforcement via in-app guidance
4. **Feedback-driven iteration** — Feature usage data drives product decisions, not guesses

### OCM Deliverables

| Artifact | Description | Priority |
|----------|-------------|:--------:|
| Persona-Based Training Profiles | Role-specific curricula: Rep (30min), Manager (45min), Admin (2hr), Developer (2hr) | P0 |
| In-App Setup Wizard | Guided first-run experience: create org, import contacts, invite team, configure pipeline | P0 |
| Adoption Metrics Dashboard | DAU/WAU, feature usage heatmap, pipeline completeness, data quality score | P1 |
| User Onboarding Flows | Email drip + in-app tour for first 7 days | P1 |
| Win-Loss Analysis | Quarterly review of features used vs not used, rationale for non-adoption | P2 |
| Champion Program | Identify power users, certify as internal trainers, reward contributions | P2 |

### Adoption Metrics — Team Targets
- **Day 7 activation:** >70% of new users complete setup wizard
- **Day 30 retention:** >60% DAU/WAU ratio
- **Data quality:** <5% contacts with missing required fields
- **Feature adoption:** >80% of users use contacts module within first week
- **Pipeline completeness:** >60% of deals have all required fields filled

### Training Framework
1. **Tier 1: Self-Service** (Trailhead-style) — Interactive in-app tutorials + video library
2. **Tier 2: Guided** — Role-based workshops (virtual or in-person)
3. **Tier 3: Certified** — Formal certification program for partners/consultants

### Failure Modes We Design Against
- User creates account, logs in once, never returns → **Fix: Day 0 setup wizard**
- User creates contacts but ignores pipeline → **Fix: Dashboard shows pipeline health prominently**
- Manager builds reports but nobody looks at them → **Fix: Push notifications with weekly metrics**
- Admin configures complex workflows that rep avoids → **Fix: Simplicity rule — every workflow must pass "can a rep explain it in 30 seconds" test**

### OCM Sprint Integration
Every sprint includes at least one OCM task:
- Sprint 1: Setup wizard (deferred to Sprint 3)
- Sprint 2: User onboarding email sequence (TBD)
- Sprint 3: Role-based training profiles
- Sprint 4: Adoption metrics dashboard
- Sprint 5: Champion program launch
