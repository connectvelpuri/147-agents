# Phase 12: Security & Permissions Architecture

**Created:** 2026-06-06
**Purpose:** Complete security model — RBAC, field-level security, record sharing, encryption, audit, compliance. This is what CISO (Persona 13) evaluates.

---

## 0. SECURITY PRINCIPLES

| Principle | Explanation |
|-----------|-------------|
| **Least privilege** | Users get minimum access needed. No default admin. |
| **Defense in depth** | Network → Application → Data → Audit — multiple layers. |
| **Data isolation (multi-tenant)** | Every query includes tenant_id. RLS at DB level. |
| **Encryption at rest + transit** | TLS for transit. AES-256 for data at rest. Field-level encryption for PII. |
| **Audit everything** | Every read, write, config change, login logged immutably. |
| **Self-hosted sovereignty** | Customer controls everything on their infrastructure. No backdoors. |

---

## 1. RBAC (Role-Based Access Control)

### Permission Hierarchy
```
Tenant ──► Role ──► Permission Set ──► Object Permissions
                                          │
                                    Field-Level Security
                                          │
                                    Record Sharing Rules
```

### Object Permissions (CRUD)
| Permission | Description |
|------------|-------------|
| Read | View records of this entity type |
| Create | Create new records |
| Edit | Modify existing records |
| Delete | Soft-delete records (hard-delete = admin only) |
| View All | Bypass sharing rules for read |
| Modify All | Bypass sharing rules for write |
| Export | Export records to file |
| Import | Import records to this entity |
| Transfer | Transfer ownership of records |

### System Roles (Seeded)

| Role | Description | Who gets it |
|------|-------------|-------------|
| System Administrator | Full access to everything. Config, users, permissions, audit. | Internal IT/Admin team |
| CRM Manager | Config access (objects, fields, workflows) + view all data | CRM Admin (P6) |
| Sales Manager | View team data, edit own, view all team, approve deals | Sales Manager (P3) |
| Sales Rep | CRUD own records. View team records (read-only). | AE (P2), SDR (P1) |
| Read Only | View data. No create/edit/delete. | External auditors, executives (read-only) |
| Integration User | API-only access. Scoped to specific entities and operations. | System integrations |
| Support Agent | View customer records + create/edit tickets. | Support (P10) |
| Customer Success | View assigned accounts + edit health scores. | CSM (P9) |

### Custom Roles
Admins can create custom roles with any combination of permissions.

---

## 2. FIELD-LEVEL SECURITY (FLS)

### Field Permission Values
| Permission | Meaning |
|------------|---------|
| Visible + Editable | User can see and modify |
| Visible + Read-Only | User can see but not change |
| Hidden | User cannot see the field at all |

### Example: Contact Field Permissions by Role

| Field | Admin | Manager | Rep | Read-Only |
|-------|:-----:|:-------:|:---:|:---------:|
| Name | R/W | R/W | R/W | R |
| Email | R/W | R/W | R/W | R |
| Phone | R/W | R/W | R/W | R |
| Salary (custom) | R/W | Hidden | Hidden | Hidden |
| Lead Source | R/W | R/W | R/W | R |
| AI Summary | R/W | R/W | R | R |
| Owner | R/W | R/W | R | R |
| SSN (encrypted field) | R/W (masked) | Hidden | Hidden | Hidden |

### FLS Implementation
```
1. Role defines default FLS for all fields
2. Permission Set can override FLS per field (additive only — can grant, not revoke)
3. API and UI enforce FLS identically
4. Audit logging sees the real value; user sees masked/null
```

---

## 3. RECORD SHARING RULES

### Default Access
- **Private by default**: A user sees only records they own (or are shared with them).
- **Granted access via**:
  - Record ownership
  - Team membership (team sees team records)
  - Manager hierarchy (manager sees subordinate records)
  - Sharing rules (explicit criteria-based)
  - Manual sharing (user shares specific record)

### Sharing Rule Types

| Type | How it works | Use Case |
|------|-------------|----------|
| **Owner-based** | Creator/assignee gets full access | Default for all entities |
| **Role-based** | Manager role sees all subordinate records | Sales Manager sees team deals |
| **Team-based** | All team members see shared records | Cross-functional deal teams |
| **Criteria-based** | Records matching criteria shared with role | "All deals > $100k visible to VP Sales" |
| **Manual sharing** | User explicitly shares record with another user | AE shares deal with specialist |
| **Territory-based** | Users see records in their territory | Territory-aligned sales teams |

### Sharing Rule Example
```
Rule Name: "Enterprise Deals for VP Sales"
Criteria: Deal.Amount > 100000 AND Deal.Stage != "Closed Lost"
Shared With: Role "VP Sales"
Access Level: Read + Edit
```

---

## 4. RECORD OWNERSHIP MODEL

### Owners
- Every record has exactly 1 owner (User)
- Owner has full CRUD (unless FLS limits fields)
- Ownership can be transferred (with permission)

### Teams
- Teams are groups of users
- Team-based sharing: all team members see team records
- Multi-team: a user can be in multiple teams

### Manager Hierarchy
```
VP Sales (manager of managers)
  ├── Sales Manager East (manager of reps)
  │     ├── Rep A
  │     └── Rep B
  └── Sales Manager West (manager of reps)
        ├── Rep C
        └── Rep D
```

**Implication:** VP Sales sees all records owned by Sales Managers East/West AND their reps.

---

## 5. ENCRYPTION STRATEGY

| Layer | Method | Key Management |
|-------|--------|---------------|
| **Transit** | TLS 1.3 (mandatory) | Let's Encrypt / custom CA |
| **At rest (database)** | AES-256-GCM | Managed by host (self-hosted: customer manages) |
| **At rest (files)** | AES-256 | Per-file encryption keys stored in DB (encrypted with master key) |
| **Field-level (PII)** | AES-256-GCM + master key | Master key in environment/HSM. Field key derived from master + record ID. |
| **Secrets (API keys, tokens)** | AES-256 | Encrypted at rest. Only decrypted in-memory at use time. |
| **Backups** | AES-256 | Separate key from production |

### Field-Level Encryption Fields (by default)
- Contact: SSN, passport, salary, bank details
- User: password_hash (bcrypt, not AES), MFA secret
- Integration: API keys, tokens, webhook secrets

### Encryption Implementation
```sql
-- Field-level encryption: value stored as base64-encoded ciphertext
-- Type indicator stored alongside for proper display/validation

CREATE TABLE encrypted_fields (
    id UUID PRIMARY KEY,
    record_type VARCHAR(100),
    record_id UUID,
    field_name VARCHAR(100),
    ciphertext TEXT,       -- base64(AES-256-GCM(plaintext))
    encryption_key_id UUID, -- which master key version
    created_at TIMESTAMPTZ
);
```

---

## 6. SESSION & AUTHENTICATION

| Feature | Implementation |
|---------|---------------|
| **Password hashing** | bcrypt (cost factor 12) |
| **MFA** | TOTP (Time-based One-Time Password) via authenticator app |
| **SSO** | SAML 2.0, OIDC, OAuth 2.0 |
| **Session token** | JWT with RS256, 15 min access, 7 day refresh, stored in httpOnly cookie |
| **Session timeout** | Configurable: idle timeout (default 2h), absolute timeout (default 24h) |
| **Concurrent sessions** | Configurable limit (default unlimited, option to limit to 5) |
| **IP restrictions** | Optional whitelist per user or role |
| **Login tracking** | Last 50 logins stored. Failed login alert after 5 within 15 min. |
| **Password policy** | Configurable: length (min 8), complexity, history (no reuse of last 5), expiry (90 days) |

---

## 7. SELF-HOSTED SECURITY

| Aspect | How It Works |
|--------|--------------|
| **Network isolation** | CRM runs in customer's VPC. No external network required. |
| **No telemetry** | No data sent to us. Optional update checker (can be disabled). |
| **License key** | Offline license validation. No phone-home requirement. |
| **Database encryption** | Customer manages their own encryption keys. |
| **Update process** | Pull from our container registry. Staged rollout in sandbox first. |
| **Security patches** | CVE notification channel. Docker image updates. |

---

## 8. COMPLIANCE ALIGNMENT

| Standard | How We Support |
|----------|----------------|
| **GDPR** | Right to deletion, data export, consent tracking, data processing records |
| **SOC 2** | Audit logs, access controls, change management, incident response |
| **HIPAA** | Field-level encryption for PHI, BAA support, access logging |
| **ISO 27001** | Information security management, risk assessment, continuous monitoring |
| **CCPA** | Data inventory, deletion requests, opt-out mechanism |
| **PCI DSS** | If CRM stores card data (not recommended), field-level encryption. Better: tokenization via Stripe. |

---

## 9. AUDIT LOG SPECIFICATIONS

### Complete Event Catalog

| Category | Events |
|----------|--------|
| **Record** | Create, Read, Update (field-level), Delete, Undelete, Merge |
| **Auth** | Login, Logout, Failed Login, MFA Enroll, Password Change, Password Reset |
| **Admin** | Create/Update/Delete: User, Role, Permission Set, Field, Entity, Layout, Workflow |
| **Security** | Permission Change, Sharing Rule Change, Encryption Key Rotation, Export |
| **Integration** | Webhook Delivery, API Call, Import Job, Export Job, Sync Run |
| **AI** | AI Query, AI Action, AI Insight Generation, Model Change |
| **Session** | Session Create, Session Expire, Session Revoke |

### Audit Log Retention

| Tier | Retention |
|------|-----------|
| Free | 30 days |
| Starter | 90 days |
| Professional | 1 year |
| Enterprise | 7 years (or custom) |

---

## 10. INCIDENT RESPONSE PROCEDURES

| Event | Detection | Immediate Action | Resolution |
|-------|-----------|-----------------|------------|
| Multiple failed logins | Threshold alert | Lock account, notify admin | Investigate, unlock if legitimate |
| Suspicious data export | Audit log review | Alert admin, revoke API key | Investigate scope, tighten permissions |
| Permission escalation | Config audit | Rollback change, notify admin | Review change request, restore correct permissions |
| MFA bypass attempt | Failed MFA log | Lock account, alert security | Verify identity, reset MFA |
| Unusual API traffic | Rate limit exceeded | Throttle, alert admin | Investigate source IP, block if malicious |

---

*Phase 12 complete. Security architecture covers RBAC, FLS, record sharing, encryption, audit, compliance. Next: Phase 13 — Reporting & Analytics Architecture.*
