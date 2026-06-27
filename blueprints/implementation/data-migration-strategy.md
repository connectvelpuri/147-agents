# Phase 15: Data Migration & Onboarding Strategy

**Created:** 2026-06-06
**Purpose:** How customers move from Salesforce, HubSpot, Zoho, LeadSquared, or spreadsheets to Sovereign CRM. Phased approach with validation at each step.

---

## 1. MIGRATION PHILOSOPHY

| Principle | Application |
|-----------|-------------|
| **No data loss** | Source data preserved. Rollback available within 30 days. |
| **Incremental, not big bang** | Start with one team, validate, expand. |
| **Transform, don't just copy** | Schema mapping, enrichment, deduplication during migration. |
| **User adoption = migration success** | Training and validation bundled with migration. |

---

## 2. SOURCE-SPECIFIC MIGRATION STRATEGIES

### From Salesforce
**Challenges:** 200+ standard objects, custom objects, Apex logic, complex sharing rules.
**Strategy:**
1. Export via Salesforce Bulk API (all objects, all fields)
2. Metadata extraction: objects, fields, layouts, workflows (via Metadata API)
3. Object mapping: Salesforce standard → Sovereign standard, Custom → Dynamic Object
4. Data transformation: picklist values, currencies, record types
5. Incremental sync: last-modified-date delta for cutover weekend
6. Validation: record count match, field-by-field sample (1% of records)

### From HubSpot
**Challenges:** Contact/Company/Deal/Ticket structure. Custom properties. Workflows.
**Strategy:**
1. HubSpot Export (all objects as CSV/JSON via API)
2. Property mapping: HubSpot property type → Sovereign field type
3. Association mapping: Contacts to Companies to Deals
4. Note/Activity migration (hubspot engagement API → activity records)
5. Pipeline/stage mapping (deal pipelines + stages)

### From Zoho
**Challenges:** Module-based structure. Picklist dependencies.
**Strategy:**
1. Zoho CRM API export (module by module)
2. Module mapping → Dynamic Object creation
3. Picklist dependency recreation
4. Blueprint (Zoho workflow) analysis → Sovereign workflow recreation

### From Spreadsheets
**Challenges:** No schema, inconsistent data, no relationships.
**Strategy:**
1. Column header analysis → field type detection (ML-assisted)
2. Relationship inference (company name → organization lookup)
3. Data cleaning in migration: standardize names, emails, phone formats
4. Manual review: "Please confirm these 3 contacts are duplicates"
5. Progressive enrichment: auto-fill enrichment post-migration

---

## 3. MIGRATION WORKFLOW

### Phase 1: Assessment (Week 1)
```
1. Inventory all source entities and fields
2. Count records per entity
3. Identify customizations (workflows, automations)
4. Identify integrations (current connected systems)
5. Data quality assessment: completeness, duplicates, stale
6. Create mapping document: source → target schema
```

### Phase 2: Mapping & Test (Week 2)
```
1. Create mapping config in migration tool
2. Extract sample (1000 records) from each entity
3. Run test import into Sovereign (sandbox tenant)
4. Validate: 
   a. Record counts match
   b. Sample 100 records: field-by-field comparison
   c. Activity history preserved
   d. Relationships correct (contact→org, contact→deal)
5. Fix mapping issues
6. User acceptance: "Does this look right?" (stakeholder reviews)
```

### Phase 3: Full Migration (Week 3 — Cutover Weekend)
```
Friday 5pm:
1. Freeze source system changes (all updates logged for delta sync)
2. Begin full export from source

Saturday:
3. Run full import into Sovereign production
4. Run delta sync (changes from freeze time)

Saturday-Sunday:
5. Validation batch:
   a. Record counts: source vs target (every entity)
   b. Field-by-field spot check: 5% of records per entity
   c. Relationship integrity: orphan records, missing lookups
   d. Activity count match

Sunday 8pm:
6. Users get access to Sovereign
7. Source system available read-only for 30 days
8. Rollback plan: if critical issues found, revert to source
```

### Phase 4: Post-Migration (Week 4-8)
```
1. Daily validation for first week: record counts, activity sync
2. User issue tracking: data quality tickets
3. Data cleanup: duplicates found post-migration, missing enrichment
4. Workflow recreation: re-implement source workflows in Sovereign
5. Integration reconnection: point tools to Sovereign API
6. Source system sunset after 30 days
```

---

## 4. MIGRATION TOOL ARCHITECTURE

```
┌────────────────────────────────────────────────────────────┐
│                    MIGRATION MANAGER                        │
│                                                            │
│  Source Connectors     Target Connector     Orchestrator    │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Salesforce      │  │ Sovereign    │  │ Extract     │  │
│  │ HubSpot         │  │ REST API     │  │ Transform   │  │
│  │ Zoho            │  │ Bulk Import  │  │ Load        │  │
│  │ CSV/Excel       │  │              │  │ Validate    │  │
│  │ Generic REST    │  │              │  │ Rollback    │  │
│  └─────────────────┘  └──────────────┘  └─────────────┘  │
│                                                            │
│  Mapping Engine: source_field → target_field + transform   │
│  Validation Engine: count, sample, integrity, business     │
│  Progress Dashboard: records/sec, ETA, errors              │
└────────────────────────────────────────────────────────────┘
```

---

## 5. ONBOARDING PLAYBOOK

### Customer Onboarding (Enterprise)

| Phase | Week | Activities | Owners |
|-------|:----:|-----------|--------|
| Kickoff | W1 | Project charter, stakeholder map, success criteria | PM + Customer Sponsor |
| Discovery | W1 | Current CRM audit, pain points, workflow inventory | RevOps + Admin |
| Migration Prep | W2 | Schema mapping, data cleanup, integration plan | Admin + TM |
| Migration | W3 | Data migration, validation, rollback plan | Admin + PM |
| Training | W4 | Role-based training sessions (SDR, AE, Manager, Admin) | PM + TM |
| Go-Live | W4 | Cutover, first week hypercare | Entire team |
| Optimization | W5-8 | Workflow tuning, report creation, adoption metrics | Admin + RevOps |

### Role-Based Training Modules

| Module | Duration | Audience | Content |
|--------|:--------:|----------|---------|
| CRM Basics | 1h | All users | Search, navigation, activity logging, profiles |
| Lead Management | 1h | SDRs | Lead queue, call logging, sequence enrollment |
| Deal Management | 1.5h | AEs | Pipeline, deal updates, forecasting |
| Manager Tools | 1h | Managers | Reports, pipeline inspection, coaching tools |
| Admin Training | 4h | Admins | Dynamic objects, workflows, users, integrations |
| AI Assistant | 30min | All users | How to ask questions, execute actions |

---

## 6. ADOPTION METRICS

### Week 1-4
| Metric | Target | How to Measure |
|--------|:------:|----------------|
| Users logged in | 100% | Login count / total users |
| Activities logged per rep per day | > 10 | Activity count per rep |
| Deals in pipeline with updates | > 80% | Deals with activity in last 7 days |
| Pipeline value coverage | > 3x quota | Total pipeline / total quota |
| Search usage per user per day | > 5 | Search bar queries |

### Month 2-3
| Metric | Target |
|--------|:------:|
| Forecast submitted on time | 100% |
| Reports used by managers | > 90% |
| AI assistant queries per user/week | > 3 |
| Support tickets about CRM | < 5/month |
| NPS survey (post-onboarding) | > 40 |

---

## 7. ROLLBACK PLAN

| Scenario | Trigger | Action | Recovery Time |
|----------|---------|--------|:------------:|
| Data quality below threshold | Validation failure > 1% sample | Stop migration, fix mapping, retry | +24h |
| Critical feature missing | Users cannot complete core workflow | Revert to source system, add feature | +1 sprint |
| Performance unacceptable | Page load > 5s for 90th percentile | Optimize indexes, caching, revert if > 10s | +48h |
| Integration failure | Key connector (email, billing) broken | Keep source system for that function, fix connector | +72h |

**Rollback Procedure:**
1. Disable Sovereign CRM login
2. Re-enable source CRM access
3. Run reverse delta sync (Sovereign → source for data created during migration)
4. Notify all users
5. Investigate and fix root cause
6. Schedule re-migration

---

*Phase 15 complete. Data migration and onboarding strategy covers source-specific approaches, 4-phase migration workflow, tool architecture, onboarding playbook, adoption metrics, and rollback plan. Next: Phase 16 — Failure Mode Analysis & Mitigation.*
