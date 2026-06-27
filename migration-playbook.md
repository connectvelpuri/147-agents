# CRM Migration Playbook

**Version:** 1.0
**Governed by:** SRE Committee + Constitution Anti-Bloat Framework
**Applies to:** All data migration into Sovereign CRM from legacy systems

---

## 1. Migration Decision Tree

Before any migration, answer these questions:

```
Is legacy CRM still in active use?
├── Yes
│   ├── Can we run both systems in parallel?
│   │   ├── Yes → Phased migration (recommended)
│   │   └── No → Big bang cutover (high risk)
│   └── Can we extract data directly?
│       ├── Yes → Direct export (API/CSV)
│       └── No → Custom ETL pipeline required
└── No
    └── Data dump available? → Import from files
```

## 2. Migration Phases

### Phase 1: Discovery (1-2 weeks)
- **Source system audit:** What data exists? What's active vs stale?
- **Data quality assessment:** Completeness, uniqueness, consistency
- **Field mapping:** Source → Target field mapping per entity
- **Volume estimate:** Record counts, attachment sizes
- **Risk assessment:** Data sensitivity, compliance requirements

#### Discovery Artifacts
```
Field Mapping Matrix:
| Source Field    | Target Field     | Transform.     | Required | Default |
|----------------|-----------------|----------------|----------|---------|
| opp.name       | deal.name        | Trim whitespace| Yes      | -       |
| acc.phone      | org.phone        | Strip formatting| No       | ''      |
| cst.field_X    | custom_fields.X  | JSON serialize  | No       | null    |

Data Quality Report:
| Dimension       | Score | Notes                |
|----------------|:-----:|----------------------|
| Completeness   | 87%   | 13% missing phone    |
| Uniqueness     | 94%   | 6% potential dupes   |
| Consistency    | 91%   | Mixed date formats   |
| Freshness      | 72%   | 28% > 6 months stale |
```

### Phase 2: Preparation (1-2 weeks)
- **Data cleansing:** Dedup, normalize addresses, validate emails
- **Template mapping:** Build import templates with defaults
- **Test import:** Import 10-50 sample records, verify
- **Rollback plan:** Define how to revert if migration fails
- **Validation scripts:** Automated checks against target data model

### Phase 3: Execution (varies by volume)
- **Dry run:** Full migration to staging environment
- **Validation:** Compare source vs target counts and value distributions
- **User verification:** Power users verify a sample of records
- **Production run:** Execute during maintenance window
- **Post-migration checks:** Data integrity audit

### Phase 4: Validation & Cutover (1 week)
- Record count match: ±1% tolerance
- Required fields filled: >95%
- Duplicate rate: <2%
- User acceptance: 5 power users confirm data looks right
- **Rollback gate:** If any check fails, scripts must revert within 2 hours

## 3. Field Mapping Rules

| Rule Type | Example | Implementation |
|-----------|---------|---------------|
| Direct | source.name -> contact.last_name | No transform |
| Concatenation | source.street + source.city -> contact.address_street | String join |
| Lookup | source.company -> organization_id | Org name -> ID |
| Normalization | source.phone -> +1 (555) 123-4567 | Strip non-digits, add country code |
| Enum mapping | source.status (1=Active, 2=Inactive) -> contact.status | Case statement |
| Default | Missing email -> '' | COALESCE with default |
| Skip | source.internal_id -> omit | Not mapped |

## 4. Validation Rules

Every imported record passes these checks:

```
REQUIRED_CHECKS = {
    "contact": [
        "first_name IS NOT NULL",
        "last_name IS NOT NULL",
        "email MATCHES email_pattern OR email IS NULL",
        "phone_mobile MATCHES phone_pattern OR phone_mobile IS NULL",
        "status IN ('active', 'inactive', 'do_not_contact')"
    ],
    "organization": [
        "name IS NOT NULL",
        "email MATCHES email_pattern OR email IS NULL"
    ]
}

COMPLIANCE_CHECKS = {
    "GDPR": [
        "No EU citizen data without processing basis",
        "Right to erasure supported via soft-delete"
    ],
    "CCPA": [
        "Opt-out tracking enabled",
        "Data inventory available"
    ]
}
```

## 5. Error Handling

| Error | Action | Retry? |
|-------|--------|:------:|
| Invalid email format | Flag for manual review | No |
| Duplicate detected | Link as duplicate via merge | Yes |
| Missing required field | Insert with NULL, flag row | No |
| Org not found | Auto-create org with minimal fields | Yes |
| Foreign key violation | Skip row, log error | No |

## 6. Rollback Procedure

**Before migration:** Take full database snapshot (pg_dump)
**After migration:** Keep snapshot for 30 days
**Rollback triggers:**
- >5% of records failed validation
- Data corruption detected (checksum mismatch)
- User-reported data loss within 48 hours

```bash
# Rollback commands
pg_restore -d sovereign -U admin --clean sovereign_backup_$(date +%Y%m%d).dump
```

## 7. Performance Budget

| Volume | Estimated Time | Notes |
|:------:|:--------------:|-------|
| <10K records | <30 seconds | Direct CSV import |
| 10K-100K | 1-5 minutes | Batch inserts of 500 |
| 100K-1M | 5-30 minutes | Disable triggers during import |
| 1M+ | 1-4 hours | Use pg_copy for bulk insert |

## 8. Post-Migration Checks

- [ ] Record counts match source (within 1%)
- [ ] Summation of pipeline values matches
- [ ] Required fields filled >95%
- [ ] Duplicate rate <2%
- [ ] Audit log shows import event
- [ ] Users confirmed data accuracy (sample of 50)
- [ ] Rollback snapshot verified
