# Operations / Admin Workflows — Complete Map

## 1. User & Role Management

### 1.1 User Provisioning
- **Trigger**: New hire, contractor onboarding, acquisition integration
- **Actor**: IT admin, HR system (automated via SCIM)
- **Steps**:
  1. Receive request: HRIS trigger (Workday/Bamboo), IT ticket, manager request
  2. Verify identity: email verification, HR record match
  3. Create user record: name, email, title, department, manager, location
  4. Assign license type: Sales, Service, Marketing, Platform, Community
  5. Assign role: determines object/field/record access
  6. Assign permission set: feature-level access (e.g., Export, API, Analytics)
  7. Assign profile: page layouts, tabs, app visibility
  8. Set default group membership: queues, public groups
  9. Send welcome email with login instructions, SSO link
  10. Trigger post-provisioning actions: create default dashboards, assign training
- **Inputs**: HR system data, manager approval, role template
- **Outputs**: User record, welcome email, license consumption, dashboard creation
- **Decisions**: Role = Sales Rep → assign standard Sales profile; Role = Manager → additional "Manager" permission set; Contractor → restricted profile, expiration date
- **Connected Workflows**: SSO (1.4), Permission sets (1.3), Deprovisioning (1.5)
- **SLA**: < 24h from request for standard roles; same-day for emergency
- **Error States**: License pool exhausted, email already in use, SCIM sync failure, duplicate user
- **Validations**: Email must be unique; manager must be active user; role hierarchy must not create circular reporting

### 1.2 Role Assignment
- **Trigger**: User creation, role change, restructuring
- **Actor**: Admin
- **Steps**:
  1. Select role and role hierarchy position
  2. Role determines: record visibility (hierarchy-based sharing), default access
  3. Test access: preview accounts/opportunities visible with this role
  4. Apply role, update sharing calculations
  5. Notify manager of role assignment
- **Connected Workflows**: Permission sets (1.3), Sharing rules
- **SLA**: < 2h

### 1.3 Permission Sets & Profiles
- **Trigger**: Need to grant additional access beyond profile
- **Actor**: Admin
- **Steps**:
  1. Identify permission need: "Can export reports", "Can delete contacts"
  2. Check if existing permission set fits → assign
  3. If new → create permission set, select enabled object permissions
  4. Assign to users or public group
  5. Audit assignment date, reason
- **Error States**: Conflicting permissions between profile and permission set

### 1.4 SSO & Authentication
- **Trigger**: User login, SAML/SSO configuration
- **Actor**: IT, user
- **Steps**:
  1. Admin configures IdP connection (Okta, Azure AD, OneLogin): SAML metadata exchange
  2. Configure Just-in-Time (JIT) provisioning: auto-create user on first SSO login
  3. User navigates to CRM → redirected to IdP login page
  4. IdP authenticates (password, MFA, device trust)
  5. SAML assertion returned → CRM validates signature
  6. User created (JIT) or matched (email) → session created
  7. Session timeout policy enforced (e.g., 8h max, idle 30 min)
- **Connected Workflows**: User provisioning (1.1), Security compliance (4.1)
- **SLA**: SSO response < 2s

### 1.5 User Deprovisioning
- **Trigger**: Employee termination, role change out of CRM, contractor end
- **Actor**: HR system, IT admin
- **Steps**:
  1. HR system triggers deactivation (offboarding flow)
  2. Immediate: disable login, expire sessions, revoke API tokens
  3. Reassign: cases → manager, opportunities → manager, leads → queue
  4. Archive or transfer private documents
  5. Set user status = "Inactive" after reassignment complete
  6. Send confirmation to manager
  7. After retention period → full deletion (GDPR compliance)
- **SLA**: < 4h from HR trigger for deactivation

### 1.6 Access Reviews
- **Trigger**: Quarterly compliance cycle, auditor request
- **Actor**: Admin, compliance officer, managers
- **Steps**:
  1. Generate access report: user → roles → permission sets → last login
  2. Flag inactive users (> 90 days), excessive permissions
  3. Manager reviews: approve, revoke, modify
  4. Apply approved changes
  5. Export signed review report for audit

---

## 2. Customization & Metadata

### 2.1 Object & Field Creation
- **Trigger**: Business need for new data structure
- **Actor**: Admin, developer (developer mode)
- **Steps**:
  1. Analyze requirement: what data, relationships, usage pattern
  2. Create custom object: label, plural label, optional features (activities, sharing)
  3. Add fields: name, data type, length, required, unique, default value
  4. Create relationships: lookup (optional), master-detail (required, cascade delete)
  5. Set field-level security: which profiles can read/edit
  6. Add to page layouts, search layouts, compact layouts
  7. Deploy to sandbox → test → deploy to production (change set or CI/CD)

### 2.2 Validation Rules
- **Trigger**: Need to enforce data quality at entry
- **Actor**: Admin
- **Steps**:
  1. Define condition: formula evaluates to true → error
  2. Write error message: user-friendly, actionable
  3. Set error location: field-level or page-level
  4. Test with records that should pass and should fail
  5. Activate (avoid bulk data entry conflicts)

### 2.3 Workflow Rules & Process Builder
- **Trigger**: Record creation, record edit, time-based
- **Actor**: Admin (or Flow Builder)
- **Steps**:
  1. Define evaluation criteria: created, edited, or created/edited
  2. Set condition formula
  3. Define actions: field update, email alert, task, outbound message
  4. Order of execution: before vs after save

### 2.4 Triggers & Apex
- **Trigger**: Complex logic beyond declarative tools
- **Actor**: Developer
- **Steps**:
  1. Write trigger on object (before insert, after update)
  2. Implement bulk-safe logic (> 200 records)
  3. Test in sandbox with large data volumes
  4. Deploy via change set/managed package
  5. Monitor: governor limits, CPU time, DML rows

---

## 3. Data Management

### 3.1 Data Import
- **Trigger**: Migration, third-party sync, spreadsheet upload
- **Actor**: Admin, data steward
- **Steps**:
  1. Validate source file: headers match field names, data types correct
  2. Map fields: source column → target field
  3. Set dedup rules: prevent duplicate creation
  4. Run import in batch (200 records per batch)
  5. Review errors: field length, format, lookup failures
  6. Rollback on critical failure
- **SLA**: < 10k records/hour

### 3.2 Data Export
- **Trigger**: Data request, backup, audit, migration out
- **Actor**: Admin, compliance
- **Steps**:
  1. Select objects and fields
  2. Filter by date/record type
  3. Choose format: CSV, Excel, JSON
  4. Export (weekly full, daily incremental)
  5. Encrypt at rest, send via secure link
- **SLA**: < 24h for standard exports

### 3.3 Data Deduplication
- **Trigger**: Post-import, scheduled maintenance
- **Actor**: System (dedup engine), admin
- **Steps**:
  1. Run matching rules (see Sales 2.2)
  2. Review groups for manual merge
  3. Purge exact duplicates
  4. Log merge activity

### 3.4 Data Quality Monitoring
- **Trigger**: Scheduled weekly, post-import
- **Actor**: System, data steward
- **Steps**:
  1. Validate completeness: required fields filled %
  2. Validate consistency: lookup relationships intact
  3. Score data quality: 0-100%
  4. Flag records below threshold
  5. Assign cleanup tasks to record owners

### 3.5 Archival & Purging
- **Trigger**: Record age exceeds retention policy
- **Actor**: System, admin
- **Steps**:
  1. Identify eligible records: Closed cases > 3 years, converted leads > 2 years
  2. Archive to external storage (S3, cold storage)
  3. Remove from active CRM, keep reference stub
  4. On deletion: verify no active related records
  5. Log archival for audit

---

## 4. Security & Compliance

### 4.1 Audit Logging
- **Trigger**: All record changes, login attempts, permission changes
- **Actor**: System
- **Steps**:
  1. Log: who, what, when, from where (IP), what changed
  2. Store in immutable audit trail
  3. Retain per compliance period (1-7 years)
  4. Provide searchable audit log UI for admins
  5. Alert on suspicious patterns: bulk delete, off-hours access, permission escalation

### 4.2 Data Encryption
- **Trigger**: Platform level, field level
- **Actor**: System, admin
- **Steps**:
  1. Data at rest: AES-256 encryption (platform managed)
  2. Data in transit: TLS 1.2+ for all API/UI traffic
  3. Field-level encryption: admin selects sensitive fields (SSN, credit card)
  4. Shield Platform Encryption: managed keys or BYOK
  5. Rotate keys annually

### 4.3 Breach Response
- **Trigger**: Security incident detected
- **Actor**: Security team, admin
- **Steps**:
  1. Isolate affected system/s
  2. Identify impact: what data, how many records, who accessed
  3. Preserve logs and snapshots
  4. Notify DPO, legal, management
  5. Contact affected customers (regulatory, GDPR 72h)
  6. Remediate: revoke access, patch, restore from clean backup
  7. Post-mortem: root cause, preventive measures

### 4.4 GDPR Compliance
- **Trigger**: Data subject request, consent change, retention expiry
- **Actor**: Privacy officer, system
- **Steps**:
  1. SAR (Subject Access Request): collect all data for person → package → deliver
  2. Right to Erasure: anonymize contact (preserve audit), remove personal data
  3. Data portability: export all data in machine-readable format
  4. Consent management: track purpose, channel, timestamp
  5. DPA (Data Processing Agreement) management with third parties

---

## 5. Integration Management

### 5.1 API Key & Webhook Management
- **Trigger**: New integration request, partner app
- **Actor**: Admin, developer
- **Steps**:
  1. Create connected app: OAuth 2.0 client credentials
  2. Set scopes: which API resources
  3. Configure IP allowlisting
  4. Generate API key/secret
  5. Set rate limits: per client, per user
  6. Monitor usage: API calls/day, error rate
  7. Rotate keys annually or on compromise

### 5.2 Third-Party Connections
- **Trigger**: Integration with external system (ERP, marketing automation, CPQ)
- **Actor**: Admin, integration specialist
- **Steps**:
  1. Select integration method: native connector, middleware (MuleSoft, Boomi), custom
  2. Configure connection: endpoint URL, authentication, credentials
  3. Map fields: source → target (both directions)
  4. Set sync frequency: real-time (webhook), hourly, daily
  5. Error handling: retry 3 times, dead letter queue, notify on failure
  6. Test in sandbox, then production

### 5.3 Sync Monitoring & Error Handling
- **Trigger**: Sync job runs, fails
- **Actor**: System, admin
- **Steps**:
  1. Sync job status: Running → Success/Failed/Partial
  2. Log records processed, errors, warnings
  3. Retry logic: 3 attempts with exponential backoff
  4. Dead letter queue: store failed records for manual review
  5. Alert admin on consecutive failures
  6. Provide re-sync button for failed records
