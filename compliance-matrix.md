# Compliance & Regulatory Matrix

**Version:** 1.0
**Governed by:** SRE Committee + Constitution Anti-Bloat Framework

---

## Applicable Regulations

| Regulation | Region | Applies When | Status |
|------------|:------:|--------------|:------:|
| GDPR | EU/EEA | Processing EU citizen data | ✅ Covered |
| CCPA/CPRA | California, USA | >25K CA residents' data | ✅ Partial |
| SOC 2 | USA | Enterprise customers requiring SOC 2 | 📋 Sprint 8 |
| HIPAA | USA | Protected health information | 📋 Sprint 9 |
| PCI DSS | Global | Credit card data in CRM | 🚫 Out of scope (use separate payment processor) |
| Schrems II | EU→USA | EU data transferred to US | ✅ Covered by self-hosting |
| EU AI Act | EU | AI/ML features processing EU data | 📋 Sprint 10 |
| India DPDP | India | Indian citizen data | 📋 Sprint 10 |
| LGPD | Brazil | Brazilian citizen data | 📋 Sprint 10 |

## GDPR Compliance Map

| Requirement | Feature | Details |
|-------------|---------|---------|
| Right to be informed | Privacy policy + in-app notices | TBD (Sprint 8) |
| Right of access | Contact/Org export | ✅ CSV export endpoint |
| Right to rectification | Update contact/org | ✅ CRUD endpoints |
| Right to erasure | Soft delete + purge job | ✅ Soft delete exists; purge job TBD |
| Right to restrict processing | Status: 'do_not_contact' | ✅ Field exists on contacts |
| Data portability | Full data export | ✅ CSV export |
| Right to object | Opt-out flags | ✅ Email/Call/SMS opt-out |
| Automated decision-making | AI scoring transparency | TBD |

## SOC 2 Readiness (Planned for Sprint 8)

| Trust Principle | Current Status | Gaps |
|----------------|:--------------:|------|
| Security | ✅ RBAC, audit logging, JWT auth | Need: penetration testing, vulnerability scanning |
| Availability | ✅ Docker Compose health checks, CI/CD | Need: SLA definition, incident response plan, DR test |
| Processing Integrity | ✅ Data validation in API models | Need: formal data integrity verification |
| Confidentiality | ✅ Tenant isolation, RBAC | Need: encryption at rest, key management |
| Privacy | ✅ Opt-out flags, data export | Need: formal privacy program, DPA template |
