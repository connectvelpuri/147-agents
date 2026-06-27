# SOVEREIGN CRM — FUNCTIONAL SPECIFICATIONS

**Document Type:** Functional Specification  
**Created:** 2026-06-07  
**Author:** Hermes Agent  
**Classification:** INTERNAL — NOT FOR GIT PUSH

---

## 1. CONTACT MANAGEMENT

### 1.1 Contact Creation
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-1.1.1: User can create contact with required fields (first_name)
- FR-1.1.2: System validates email format if provided
- FR-1.1.3: System validates phone format if provided
- FR-1.1.4: System auto-generates UUID for contact
- FR-1.1.5: System sets created_at and updated_at timestamps
- FR-1.1.6: System assigns contact to current user's tenant
- FR-1.1.7: System allows optional fields (email, phone, job_title, etc.)
- FR-1.1.8: System supports custom fields via JSONB
- FR-1.1.9: System supports tags as text array
- FR-1.1.10: System allows assignment to owner (user)

**Validation Rules:**
- first_name: Required, max 100 chars
- email: Optional, valid email format, unique per tenant
- phone: Optional, max 50 chars
- lead_score: Optional, 0-100 integer

### 1.2 Contact Retrieval
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-1.2.1: User can list contacts with pagination
- FR-1.2.2: User can search contacts by name or email
- FR-1.2.3: User can filter by status, owner, organization
- FR-1.2.4: User can sort by any field
- FR-1.2.5: User can get single contact with all relationships
- FR-1.2.6: System returns 404 for non-existent contact
- FR-1.2.7: System respects RLS (only see tenant's contacts)

### 1.3 Contact Update
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-1.3.1: User can update any contact field
- FR-1.3.2: System updates updated_at timestamp
- FR-1.3.3: System allows partial updates
- FR-1.3.4: System validates updated fields
- FR-1.3.5: System prevents update of id, tenant_id, created_at

### 1.4 Contact Deletion
**Priority:** P1  
**Status:** ✅ Implemented (Soft Delete)

**Functional Requirements:**
- FR-1.4.1: System performs soft delete (sets status to 'archived')
- FR-1.4.2: User can restore archived contacts
- FR-1.4.3: System preserves contact data for audit
- FR-1.4.4: Hard delete requires admin role

---

## 2. ORGANIZATION MANAGEMENT

### 2.1 Organization CRUD
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-2.1.1: User can create organization with required fields (name)
- FR-2.1.2: System supports parent-child relationships
- FR-2.1.3: System supports industry classification
- FR-2.1.4: System supports company size categorization
- FR-2.1.5: System supports annual revenue tracking
- FR-2.1.6: System allows contact association
- FR-2.1.7: System supports custom fields

---

## 3. DEAL PIPELINE

### 3.1 Deal Management
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-3.1.1: User can create deal with required fields (name, stage)
- FR-3.1.2: System supports configurable pipeline stages
- FR-3.1.3: System tracks deal value and currency
- FR-3.1.4: System tracks expected close date
- FR-3.1.5: System tracks probability (0-100%)
- FR-3.1.6: System supports deal-contact relationships
- FR-3.1.7: System supports deal-organization relationships

### 3.2 Stage Transitions
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-3.2.1: User can move deal to any stage
- FR-3.2.2: System records stage change history
- FR-3.2.3: System allows notes on stage change
- FR-3.2.4: System updates deal probability on stage change
- FR-3.2.5: System supports win/loss tracking

---

## 4. ACTIVITY MANAGEMENT

### 4.1 Activity Logging
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-4.1.1: User can log calls, emails, meetings, tasks, notes
- FR-4.1.2: System associates activity with contact/deal/organization
- FR-4.1.3: System tracks activity direction (inbound/outbound)
- FR-4.1.4: System tracks duration (minutes)
- FR-4.1.5: System supports due dates and reminders
- FR-4.1.6: System tracks completion status

---

## 5. EMAIL TEMPLATES

### 5.1 Template Management
**Priority:** P1  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-5.1.1: User can create templates with subject and body
- FR-5.1.2: System supports variable placeholders ({{first_name}})
- FR-5.1.3: System categorizes templates
- FR-5.1.4: System tracks usage count
- FR-5.1.5: System allows template preview

---

## 6. EMAIL SEQUENCES

### 6.1 Sequence Management
**Priority:** P1  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-6.1.1: User can create multi-step sequences
- FR-6.1.2: System supports delay configuration (days/hours)
- FR-6.1.3: System supports conditional branching
- FR-6.1.4: System tracks enrollment and completion stats
- FR-6.1.5: System allows pause/resume

---

## 7. WORKFLOW AUTOMATION

### 7.1 Workflow Management
**Priority:** P1  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-7.1.1: User can create trigger-based workflows
- FR-7.1.2: System supports multiple trigger types (record_created, field_changed, schedule)
- FR-7.1.3: System supports action chaining
- FR-7.1.4: System tracks execution stats
- FR-7.1.5: System logs workflow execution

---

## 8. DATA IMPORT

### 8.1 CSV Import
**Priority:** P1  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-8.1.1: User can upload CSV files
- FR-8.1.2: System validates CSV format
- FR-8.1.3: System supports field mapping
- FR-8.1.4: System validates data against schema
- FR-8.1.5: System handles duplicates (skip/merge/overwrite)
- FR-8.1.6: System tracks import progress
- FR-8.1.7: System provides import summary with errors
- FR-8.1.8: System supports bulk import (multiple files)

---

## 9. MULTI-TENANCY

### 9.1 Tenant Isolation
**Priority:** P0  
**Status:** ✅ Implemented (RLS)

**Functional Requirements:**
- FR-9.1.1: Each tenant has isolated data
- FR-9.1.2: Users can only access their tenant's data
- FR-9.1.3: Cross-tenant queries are blocked at database level
- FR-9.1.4: Tenant context is set per request
- FR-9.1.5: System enforces tenant_id on all operations

---

## 10. REAL-TIME COLLABORATION

### 10.1 CRDT Sync
**Priority:** P0  
**Status:** ✅ Implemented

**Functional Requirements:**
- FR-10.1.1: Multiple users can edit same record simultaneously
- FR-10.1.2: System detects conflicts automatically
- FR-10.1.3: System provides conflict resolution UI
- FR-10.1.4: System supports offline mode
- FR-10.1.5: System syncs changes when online
- FR-10.1.6: System preserves edit history

---

*Document maintained by Hermes Agent. Never push to Git.*  
*Last Updated: 2026-06-07*
