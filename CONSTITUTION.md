# Sovereign CRM Product Constitution

**Version:** 1.0
**Created:** 2026-06-06
**Status:** Ratified
**License:** AGPL v3 (with commercial exception for proprietary use)
**Repository:** https://github.com/sovereign-crm/sovereign
**Stack:** Go (backend), Next.js (frontend), PostgreSQL (database)
**Monetization:** 100% open source core. No license key checks in codebase. Managed cloud is a separate deployment. Marketplace adds monetization layer in Month 6+.
**Amendment Process:** RFC submitted to /rfcs/, 7-day review period, 2/3 maintainer approval.

---

## PREAMBLE

This Constitution governs every decision made about Sovereign CRM — what we build, how we build it, how we measure it, and how we remove it. Every feature, every sprint, every architecture choice, every partnership, every line of code is subject to this Constitution. When conflict arises between this document and any other document, this document prevails.

**Purpose:** Prevent bloat, prevent drift, prevent building things nobody needs, and ensure the project survives its founders.

---

## ARTICLE I: THE 10 QUESTIONS

*Applicable to every feature, every API endpoint, every UI component, every integration, every architecture decision.*

Before any feature enters a sprint, the Product Manager (or their delegate) must answer all 10 questions in writing. The answer is reviewed by at least one engineer and one designer. If any question cannot be answered satisfactorily, the feature does not proceed.

### The Questions

**Q1: Why does this exist?**
What is the specific, concrete reason for this feature? Not "users asked for it" — *which* users, *what* context, *what* specific problem were they trying to solve when they asked?

**Q2: What customer problem does it solve?**
Describe the problem in terms of the persona's day, not the feature's function. "An SDR spending 5 minutes manually entering call notes after each call" not "Voice-to-text transcription."

**Q3: How is it solved today?**
What is the user's current workaround? If there is no workaround, the problem may not be painful enough to solve. "SDR types notes in a text file" is a valid answer. "Nobody does this" is a red flag.

**Q4: Why are existing solutions insufficient?**
If the user has access to other tools that could solve this, why aren't they using them? If no other tool exists, explain why the problem hasn't been solved before.

**Q5: What assumptions are we making?**
List every unvalidated assumption. Example: "We assume SDRs will adopt voice-to-text. We assume battery drain is acceptable. We assume 95% transcription accuracy is sufficient."

**Q6: What would make this fail?**
Three failure scenarios minimum. Example: "Voice-to-text fails in noisy environments. SDRs prefer typing for record-keeping. Transcription errors cause data quality issues."

**Q7: What is the simplest version?**
What is the smallest possible implementation that delivers value? This becomes the MVP scope. Everything else is post-MVP.

**Q8: What scales to 10× users? What scales to 100× users?**
Storage, API calls, database queries, bandwidth. What breaks at 10×? At 100×? If the answer is "nothing," you haven't thought hard enough.

**Q9: How do we measure success?**
A single metric (+ threshold). Example: "Adoption: 50% of SDR calls use voice-to-text within 4 weeks of launch. Accuracy: < 2% correction rate on records created via voice."

**Q10: How do we know it should be removed?**
The removal criteria. Example: "If < 10% adoption after 8 weeks OR correction rate > 5% after 4 weeks, kill the feature and roll back the UI."

### The 11th Question (Strategic)

*Applied quarterly to the product as a whole, not individual features.*

**Q11: If Salesforce were rebuilding this today, how would they design it assuming $0 legacy cost?**
This prevents us from building the "better Salesforce" — it forces us to design the post-Salesforce CRM. If our answer matches Salesforce's architecture, we've failed this question.

---

## ARTICLE II: PRODUCT DISCOVERY ENGINE

### Section 2.1: Customer Research Framework

Every persona must have a **Day-in-the-Life (DITL)** document. Not a persona description — a minute-by-minute walkthrough of their workday.

**DITL Template:**
```
Persona: [Name]
Time: [08:00-09:00]
Activity: [What they do]
Tool Used: [What tool]
Frustration: [What's annoying]
CRM Touchpoint: [How CRM is involved]
```

**Requirement:** Before building a feature for a persona, spend 2 hours observing that persona type working. Not interviewing — observing. Take notes on what they actually do vs what they say they do.

### Section 2.2: Observation Research Methodology

| Method | When to Use | Output |
|--------|-------------|--------|
| Shadowing (follow user for 4h) | Before major feature for a persona | DITL documentation |
| Session recording analysis | When UI exists | Heatmap of clicks, time-on-task |
| Diary study (user logs daily for 2 weeks) | Understanding workflows over time | Pain point frequency |
| Task analysis (user performs specific task) | Evaluating new/existing UX | Time-to-complete, error rate |
| Contextual inquiry (interview at their desk) | Understanding tool ecosystem | Integration needs |

**Rule:** No major feature (sprint-sized) proceeds without at least one observation session with a real target user.

### Section 2.3: The "Build What They Need, Not What They Say" Rule

Users ask for solutions. They don't describe problems.

| User says | They mean | We build |
|-----------|-----------|----------|
| "I need a better dashboard" | "I can't find which deals need attention" | Pipeline inspection view with AI risk flags |
| "I need an app for that" | "I want to log stuff without opening my laptop" | Quick-log widget with voice notes |
| "Import is broken" | "I spent 2 hours mapping columns and it still didn't work" | Smart mapping with auto-detect + one-click fix |
| "AI is wrong" | "I don't trust the AI suggestions" | Show confidence score + source data |

### Section 2.4: Research Cadence

| Cadence | Activity | Owner |
|---------|----------|-------|
| Weekly | 2 customer discovery calls or observation sessions | PM |
| Bi-weekly | User testing of in-progress features | PM + Designer |
| Monthly | Analysis of NPS/support data for pain pattern detection | PM + Support |
| Quarterly | Full persona re-evaluation (have their needs changed?) | PM + CEO |

---

## ARTICLE III: ANTI-BLOAT FRAMEWORK

### Section 3.1: Feature Admission Criteria

For a feature to enter a sprint, it must meet at least 3 of 5 criteria *and* pass the 10 Questions (Article I):

| Criterion | Weight | Evidence Required |
|-----------|:------:|-------------------|
| Validated demand | 3 | Observation data or 5+ customer calls expressing the need unprompted |
| Revenue impact | 2 | Estimated incremental revenue/retention from the feature |
| User value (adoption estimate) | 2 | Projected % of target persona who would use weekly |
| Strategic alignment | 1 | Feature aligns with Constitution Article IV (performance) and product vision |
| Competitive differentiation | 1 | Feature is unique vs Salesforce/HubSpot/Zoho |

**Threshold:** Score ≥ 7 to proceed. Score 5-6 requires CEO override. Score < 5 is rejected.

### Section 3.2: Feature Retirement Process

Every feature has a sunset clock from the day it ships.

| Phase | Condition | Action |
|-------|-----------|--------|
| **Monitor** | Launch + 4 weeks | Adoption tracking enabled. No action needed. |
| **Warning** | < 15% weekly active usage of target persona at week 8 | PM investigates: poor UX? Wrong problem? |
| **Review** | < 10% at week 12 | Feature flagged for retirement. Maintainer vote. |
| **Deprecate** | Vote passes | Feature marked "deprecated" in docs. Removed from UI default. Can be re-enabled in admin. |
| **Remove** | Deprecated + 2 releases | Code removed. Migration path documented for anyone using it. |

**Exception:** Features with revenue attribution (+$10k ARR) can override with CEO sign-off.

### Section 3.3: Technical Debt Budget

| Sprint Type | Debt Allowance | Purpose |
|-------------|:--------------:|---------|
| Feature sprint | 20% of capacity | Refactoring, docs, tests related to new feature |
| Maintenance sprint (every 4th) | 50% of capacity | Cross-cutting technical debt, dependency upgrades, performance |
| Emergency | Unlimited | Security vulnerabilities, data corruption bugs, critical outages |

### Section 3.4: Maintenance Cost Accountability

Every feature must document its estimated annual maintenance cost in developer-days:

```yaml
feature: voice_to_text
annual_maintenance_days: 12
  - model_updates: 5 days (new ASR models every quarter)
  - bug_fixes: 4 days (edge cases, error handling)
  - dependencies: 3 days (library updates, API changes)
```

Features with maintenance cost > 30 developer-days per year require annual CEO re-approval.

---

## ARTICLE IV: PERFORMANCE CONSTITUTION

### Section 4.1: Performance Budgets

Every UI operation has a performance budget. Violations block the release.

| Operation | Budget (P95) | Measurement Tool | Violation Penalty |
|-----------|:------------:|------------------|:-----------------:|
| Global search | 1,000 ms | Lighthouse CI | Block release |
| Record load (contact, deal) | 500 ms | Lighthouse CI | Block release |
| List view (50 records) | 800 ms | Lighthouse CI | Block release |
| List view (10,000 records) | 5,000 ms | k6 | Block release |
| Dashboard load (4 widgets) | 2,000 ms | Lighthouse CI | Block release |
| Report generation (10k rows) | 5,000 ms | Backend benchmark | Warning |
| Import (10k records) | 60,000 ms | Backend benchmark | Warning at 90s |
| Page navigation (any route) | 300 ms | Lighthouse CI | Block release |
| API response (single record) | 200 ms | k6 | Block release |
| API response (paginated list) | 500 ms | k6 | Block release |
| Sync (100 offline changes) | 5,000 ms | Sync benchmark | Warning |
| Login | 2,000 ms | Lighthouse CI | Block release |

**Enforcement:** CI pipeline runs performance tests on every PR. Budget violations fail the build. Emergency override requires CTO sign-off with documented exception.

### Section 4.2: Capacity Benchmarks

Every release must be tested against these tiers. Publish results with each release.

| Tier | Users | Records | Operations/sec | Expected Configuration |
|:----:|:-----:|:-------:|:--------------:|----------------------|
| S | 10 | 10k | 100/s | Single Postgres, 2GB RAM |
| M | 100 | 100k | 500/s | Postgres + Redis, 8GB RAM |
| L | 1,000 | 1M | 2,500/s | Postgres + Redis + ClickHouse, 16GB RAM |
| XL | 10,000 | 10M | 10,000/s | Read replicas, CDN, ClickHouse cluster, 64GB RAM |
| XXL | 100,000 | 100M | 50,000/s | Multi-region, sharded, 128GB+ RAM |

**Requirement:** L-tier performance is the minimum production target.

### Section 4.3: Performance Regression Protection

- Every PR includes a "Performance Impact" section in the description
- CI runs `bench` suite: compares against `main` branch baseline
- Regression > 10% on any budget metric → PR blocked
- Performance budget review every sprint retro
- Quarterly "performance deep dive" with flame graphs and query analysis

---

## ARTICLE V: PRE-MORTEM — 5-YEAR FAILURE ANALYSIS

*Date: 2031-06-06. This project failed. Why?*

### Scenario 1: "Too Complex, Too Slow"

**Symptom:** 30-second page loads. Database slow. Features depend on features in an inextricable dependency graph. New developers need 3 months to become productive.

**Root cause:** No performance budgets (Article IV was ignored). No anti-bloat controls (Article III was ignored). Architecture debt accumulated.

**How this is prevented:**
1. Performance budgets are enforced in CI — the build breaks before the user feels the lag
2. Feature admission criteria prevent unnecessary complexity
3. Technical debt budget ensures ongoing refactoring

### Scenario 2: "Nobody Contributed"

**Symptom:** GitHub repo with 500 stars, 3 contributors (all founders), 0 external PRs merged in 2 years. Project is effectively closed-source in open-source clothing.

**Root cause:** No community strategy. No contribution guides. No RFC process. Code is hard to understand. Tests are missing. Docs are incomplete. PRs sit for weeks.

**How this is prevented:**
1. Community charter (Standing Committee 1) defines contributor funnel and metrics
2. DX charter (Standing Committee 3) targets < 5 minute setup time
3. RFC process enables community participation in direction
4. Governance model (Article VI) distributes decision-making

### Scenario 3: "The Mobile Failure"

**Symptom:** 40% of users try the mobile app and abandon within a week. Field reps refuse to use it. CRM adoption stalls at 30%.

**Root cause:** Mobile was an afterthought. Offline sync dropped data. Voice notes didn't work. Reps went back to spreadsheets.

**How this is prevented:**
1. Mobile charter (Standing Committee 2) treats mobile as "Field Sales OS" not "app"
2. Offline architecture decisions made explicitly before writing code
3. Mobile feature parity defined per sprint

### Scenario 4: "Data Integrity Disaster"

**Symptom:** Duplicate records everywhere. Merged contacts lose history. Offline sync creates phantom records. Trust in the CRM is destroyed.

**Root cause:** No testing strategy for CRDT sync. No data integrity verification. Chaos testing not performed.

**How this is prevented:**
1. Testing trust architecture (Standing Committee 5) includes sync fuzzing, deterministic conflict testing, and data integrity checksums
2. Every release includes a data integrity verification run
3. Rollback capability for any sync operation

### Scenario 5: "The Migration That Failed"

**Symptom:** Customer with 500k Salesforce records tries to migrate. Import takes 3 days. Mapping is wrong. Duplicates flood the system. Customer reverts to Salesforce.

**Root cause:** Migration was tested with 10k records, not 500k. No incremental sync. No validation during migration.

**How this is prevented:**
1. Migration testing at all tiers (M, L, XL, XXL per Article IV)
2. Incremental sync + delta verification
3. Rollback plan for every migration (Article VI, SRE charter)

### Scenario 6: "The Fork"

**Symptom:** Community disagrees with project direction. Someone forks the repo. The fork gains more contributors than the original. Project loses relevance.

**Root cause:** No governance model. Decisions made unilaterally. Community has no voice.

**How this is prevented:**
1. Governance model (Community charter) provides clear decision-making
2. RFC process allows community input
3. Fork is treated as natural — the market decides which implementation wins

---

## ARTICLE VI: GOVERNANCE

### Section 6.1: Project Leadership

| Role | Responsibility | Appointment |
|------|---------------|-------------|
| **BDFL** (Benevolent Dictator for Life) | Final decision on product direction, architecture, and disputes. Can override any decision. | Founder. Succession by BDFL appointment. |
| **Core Maintainers** (up to 5) | Review RFCs, approve PRs, set technical direction. | BDFL appointment + maintainer vote (2/3). |
| **Committers** (up to 20) | Merge PRs in their domain. Triage issues. | Core maintainer nomination + maintainer vote. |
| **Contributors** (unlimited) | Submit PRs, report issues, write docs. | Self-selecting. |

### Section 6.2: RFC Process

Any significant change (new feature, architecture change, deprecation, policy change) requires an RFC.

1. **Draft:** Contributor writes RFC using template in /rfcs/
2. **Review:** 7-day comment period on GitHub Discussion
3. **Decision:** Core maintainers vote. Requires 2/3 approval.
4. **Implementation:** RFC is accepted. Feature enters backlog.
5. **Amendment:** Smaller changes to accepted RFCs require 1-week comment period.

### Section 6.3: Voting

| Decision | Voters | Threshold |
|----------|--------|:---------:|
| RFC acceptance | Core Maintainers | 2/3 |
| New Core Maintainer | Core Maintainers | 2/3 (BDFL has veto) |
| New Committer | Core Maintainers | Simple majority |
| Feature retirement | Core Maintainers + PM | Simple majority |
| Constitution amendment | All Maintainers + Committers | 2/3 |
| BDFL succession | All Maintainers + Committers | 3/4 |

### Section 6.4: Dispute Resolution

1. Disagreement → 3-day discussion on GitHub
2. Stalemate → BDFL decision (with written rationale)
3. BDFL dispute → Steering Committee of 3 Core Maintainers + 2 Community Representatives (elected)

---

## ARTICLE VII: STANDING COMMITTEES

Five standing committees govern the operational domains. Each has a charter document that lives in `/committees/`. Charters are amended via RFC process.

| Committee | Domain | Charter Document |
|-----------|--------|-----------------|
| **Community & Ecosystem** | Governance, contributor funnel, marketplace, events | /committees/community-charter.md |
| **Mobile (Field Sales OS)** | Mobile app, offline, field workflows, mobile-specific features | /committees/mobile-charter.md |
| **Developer Platform** | DX, SDKs, plugin system, architecture documentation | /committees/dev-platform-charter.md |
| **SRE & Operations** | Deploy, reliability, observability, capacity | /committees/sre-charter.md |
| **Testing & Trust Architecture** | Test pyramid, chaos engineering, data integrity | /committees/testing-charter.md |

Each committee:
- Meets bi-weekly (async or sync)
- Produces quarterly roadmap proposals
- Reports to PM for sprint integration
- Can request RFCs for changes in their domain

---

## ARTICLE VIII: AMENDMENT

This Constitution is a living document. Amendments follow RFC process (Article VI, Section 6.2) with 2/3 maintainer approval. The preamble and Article I (10 Questions) require 3/4 approval and a 14-day review period.

---

*Constitution ratified. All product decisions now governed by this document. Standing Committee Charters follow.*
