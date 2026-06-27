# Methodology Gap Analysis — Sovereign CRM vs Big 4 Standards

**Date:** 2026-06-06
**Source Research:** Deloitte (Connected Enterprise / CRM Core), PwC (Connected CRM), EY (NextWave Customer), KPMG (Powered Enterprise), Salesforce (Success Cloud), Industry Best Practices 2025-2026

---

## Executive Summary

We benchmarked Sovereign CRM's existing methodology (Constitution + 5 Committee Charters + Sprint Plan) against how Deloitte, PwC, EY, and KPMG approach CRM delivery. 

**Score:** 65/100 — Solid architectural governance, but missing entire domains that Big 4 treat as prerequisites.

**The 5 Critical Gaps (in priority order):**
1. Organizational Change Management (OCM) — missing entirely
2. Data Migration & Master Data Management (MDM) — missing entirely
3. Business Case / ROI Framework — missing entirely
4. Industry Configuration Patterns — missing entirely
5. Adoption Measurement & Post-Deploy Model — missing entirely

---

## Detailed Gap Analysis

### GAP 1: Organizational Change Management (OCM)
**Severity: CRITICAL — Most CRM failures are adoption failures, not tech failures.**

| What Big 4 does | What we have | Gap |
|---|---|---|
| EY: "User Adoption Diagnostic" — quantitative readiness assessment before build | Nothing | No adoption risk measurement |
| Deloitte: Train-the-Trainer program + role-based certification paths | Nothing | No training framework |
| Salesforce: Trailhead — self-paced learning, gamified adoption | Nothing | No learning infrastructure |
| PwC: "Experience Radar" — identifies moments that matter for user buy-in | Nothing | No stakeholder journey mapping |
| KPMG: TOM (Target Operating Model) — people + process redesign before tech | Nothing | No operating model design |

**Fix Required:**
- Add **Adoption Committee** as 6th Standing Committee (or fold into Community)
- Add **Role-Based Training Profiles** — map each persona (Rep, Manager, Admin) to required training
- Add **Adoption Metrics** — DAU/WAU, feature usage rates, pipeline completeness scores
- Add **User Onboarding Flows** — app-guided setup wizard for first login
- Add **Win-Loss Analysis** for feature adoption

---

### GAP 2: Data Migration & Master Data Management (MDM)
**Severity: CRITICAL — #1 technical failure mode for enterprise CRM projects.**

| What Big 4 does | What we have | Gap |
|---|---|---|
| Deloitte: "Digital Migrator" — proprietary ETL for CRM migrations | Nothing | No import framework |
| PwC: Legacy system assessment + data quality scoring | Nothing | No data quality audit |
| EY: TCO-weighted migration path analysis (lift-shift vs rebuild vs phased) | Nothing | No migration strategy decision tree |
| KPMG: Data governance framework for multi-source master data | Contact dedup hash only | No entity resolution or merge strategy |
| Salesforce: Data Import Wizard + Workbench + Data Loader CLI | Nothing | No bulk data tools |

**Fix Required:**
- **CSV Import/Export endpoint** (partially planned Sprint 3 — needs full spec)
- **Data Quality Rules** — uniqueness, completeness, consistency validations
- **Migration Playbook** — source system discovery, field mapping, transformation, validation, cutover
- **Entity Resolution** — beyond simple SHA256 dedup: fuzzy matching, supervised merge
- **Rollback Strategy** — if migration fails, how to revert

---

### GAP 3: Business Case / ROI Framework
**Severity: HIGH — Without a business case framework, buyers can't justify the investment.**

| What Big 4 does | What we have | Gap |
|---|---|---|
| Deloitte: 6-8 week "Discover" phase — business case before any tech | Nothing | No discovery phase |
| PwC: 21-Point CRM Review — health check + ROI projection | Nothing | No health check |
| EY: CRM Selection Navigator — weighted matrix for vendor/approach comparison | Nothing | No decision matrix |
| KPMG: Operating model business case — quantifies people/process/tech savings | Nothing | No TCO/ROI calculator |

**Fix Required:**
- **Single-tenant data isolation** — architectural pattern for sovereign deployment
- **Cost comparison tool** — Salesforce/Zoho/HubSpot equivalent pricing for N users
- **ROI Calculator** — time saved, pipeline velocity, win rate improvement projections
- **Discovery Sprint** — optional pre-project engagement template (Week 0)

---

### GAP 4: Industry Configuration Patterns
**Severity: MEDIUM — Big 4 differentiate by pre-built industry solutions.**

| What Big 4 does | What we have | Gap |
|---|---|---|
| Deloitte: Salesforce FSC (Financial Services Cloud), Health Cloud, Consumer Goods Cloud | Nothing | No industry accelerators |
| PwC: FS regulatory CRM templates, Life Sciences compliance | Nothing | No vertical configs |
| EY: "Carbon CRM" — sustainability tracking built into CRM | Nothing | No ESG module |
| Salesforce: Financial Services, Health, Manufacturing, Nonprofit clouds | Nothing | No vertical editions |

**Fix Required:**
- **Industry Configuration Profiles** — per-vertical field sets, layouts, workflows
- **IT Consulting profile** (our initial target) — project tracking, resource booking, SOW management
- **SaaS profile** — subscription tracking, renewal pipeline, usage metrics
- **Plugin architecture** (already in dev-platform-charter) — industry packs as plugins

---

### GAP 5: Adoption Measurement & Post-Deploy Model
**Severity: HIGH — Current methodology ends at deployment.**

| What Big 4 does | What we have | Gap |
|---|---|---|
| Deloitte: 2-4 week Hypercare war room post-go-live | Nothing | No hypercare |
| Deloitte: Quarterly Business Reviews (QBRs) + roadmap refresh | Nothing | No continuous improvement cycle |
| EY: User adoption diagnostic + adoption improvement plans | Nothing | No adoption analytics |
| Salesforce: Usage dashboards, login history, feature adoption reports | Nothing | No telemetry system |

**Fix Required:**
- **Telemetry Pipeline** — anonymous usage metrics (opt-in, AGPL compatible)
- **Hypercare Runbook** — first-week post-deploy support model
- **Feature Adoption Dashboard** — DAU, feature usage, p95 latency, error rates
- **Health Score** — composite metric of adoption, data quality, performance
- **Sprint Zero for new tenants** — guided onboarding sequence

---

## Additional Gaps (Medium Priority)

### GAP 6: Sovereign AI Architecture (Not In Scope Yet But 2025-2026 Imperative)
Big 4 are all pushing GenAI. EY has "Customer Analytics Engine", PwC has "AI-driven insights". Our mobile charter mentions Whisper.cpp for field voice, but no overall AI strategy.

**Fix:** Add **AI Working Group** — define local LLM integration (Ollama/MCP), AI copilot for rep workflows, AI-assisted pipeline scoring, natural language search. Not urgent for Sprint 3, but needs a formal charter.

### GAP 7: Composable/MACH Architecture — Formally Adopt the Label
MACH = Microservices, API-first, Cloud-native, Headless. This IS our architecture already, but we never named it. The MACH Alliance is a recognized industry standard that buyers look for.

**Fix:** Add "MACH-compliant" to marketing, reference MACH principles in ARCHITECTURE.md. No code changes needed.

### GAP 8: Security & Compliance Framework
GDPR, Schrems II, EU AI Act, India DPDP Act, HIPAA, SOC 2. We have basic RBAC and audit logging but no structured compliance posture.

**Fix:** Add **Compliance Matrix** to the SRE charter — which regulations apply, which features address them, which are TBD.

---

## Methodology Comparison Matrix

| Dimension | Deloitte | PwC | EY | KPMG | Salesforce | **Sovereign (Current)** | **Sovereign (Target)** |
|---|---|---|---|---|---|---|---|
| Strategy/Business Case | ✅ 6-8 wk discovery | ✅ 21-pt review | ✅ Selection Navigator | ✅ TOM business case | ❌ Partner-driven | ❌ Missing | Sprint 3 |
| Architecture | ✅ Industry clouds | ✅ Composable/API-first | ✅ Future-back | ✅ Multi-cloud patterns | ✅ Hyperforce | ✅ Strong (Constitution) | Already good |
| OCM/Adoption | ✅ Train-the-Trainer | ✅ Experience Radar | ✅ Adoption Diagnostic | ✅ TOM people pillar | ✅ Trailhead | ❌ Missing | NEW: OCM |
| Data Migration | ✅ Digital Migrator | ✅ Data quality scoring | ✅ TCO migration paths | ✅ Data governance | ✅ Data Import tools | ❌ Missing (partial dedup) | NEW: MDM |
| Delivery | ✅ Agile hybrid + gates | ✅ Lean-agile + accelerators | ✅ Wavespace co-creation | ✅ Powered Enterprise | ✅ Agile hybrid (MVP) | ✅ Sprint model | Refine |
| Testing | ✅ SIT/UAT + regress | ✅ Automated + manual | ✅ User acceptance + chaos | ✅ Governance compliance | ✅ Sandbox testing | ✅ Test pyramid (charter) | Already good |
| Post-Deploy | ✅ Hypercare + QBR | ✅ AMS support | ✅ Adoption monitoring | ✅ Continuous improvement | ✅ Success plans | ❌ Missing | NEW: Post-Deploy |
| Industry Configs | ✅ 12+ industry clouds | ✅ FS/Life sciences | ✅ Tax/Carbon CRM | ✅ Industry-specific TOM | ✅ 8+ industry clouds | ❌ Missing | NEW: Industries |

---

## Refinements Applied (This Session)

Based on this gap analysis, we've already:

1. **Added `search_vector` to contacts + organizations** — proactive search infrastructure
2. **Added version tracking** on contacts (CRDT prep)
3. **Added dedicated hash + merge endpoint** — dedup foundation
4. **Backfilled auth + RBAC tests** — closing the testing gap
5. **Wrote CONTRIBUTING.md** — open source community foundation
6. **Added issue/PR templates** — contributor experience

---

## What Changes Before Sprint 3

**I recommend three structural additions before Sprint 3 builds:**

### A. Add OCM & Adoption to the Community Charter
The Community & Ecosystem Committee should also own adoption and user success. Rename to **"Community, Adoption & Success"** with:
- Adoption metrics (DAU, feature usage, p95 latency)
- User onboarding flows
- Training materials
- Win-loss analysis

### B. Create a Data Migration Playbook in SRE Charter
Add to the SRE committee's remit:
- Migration path decision tree
- Data quality rules
- Bulk import/export spec
- Entity resolution strategy

### C. Add a Discovery Sprint / Phase 0
Before any new sprint, add a **1-week discovery** that validates the business outcome before building:
- What problem does this solve?
- How is it solved today?
- What is the simplest version?
- How do we measure success?

This already exists in the Constitution (10 Questions) — formalize it as a sprint pre-requisite.

---

## Quick Wins (Can Do Next Session)

1. Add OCM section to Community Charter
2. Write CSV Import/Export endpoint (needed for Sprint 3 anyway)
3. Write entity resolution doc
4. Add compliance matrix to SRE charter
5. Add adoption dashboard spec

---

*Research sources: Deloitte Connected Enterprise, Deloitte CRM Core, PwC Connected CRM, EY NextWave Customer, KPMG Powered Enterprise, Salesforce Success Cloud / Hyperforce, MACH Alliance standards, Gartner/Forrester CRM landscape reports.*
