# Phase 6: Complete Data Model

**Created:** 2026-06-06
**Purpose:** Every entity, every field, every relationship, every index, every constraint. The single source of truth for schema design.

---

## 0. DATA MODEL DESIGN PRINCIPLES

| Principle | Rationale |
|-----------|-----------|
| **Metadata-driven** | All entities (except system core) are defined in metadata tables, not hardcoded. Enables the Dynamic Object Builder. |
| **Single-table-per-entity** on the physical side but virtual view layer for cross-entity queries | Optimizes read performance while keeping CRDT sync manageable |
| **Event-sourced** | Every field change is an event. Audit trail is native, not bolted on. |
| **Soft-delete everywhere** | No data loss. Deleted records are recoverable. |
| **UUID primary keys** throughout | Distributed/offline-first generation without collision risk |
| **Timestamps on every record** | created_at, updated_at, deleted_at (nullable). Mandatory. |
| **Tenant-isolated** | tenant_id on every root entity. Row-level security starts at the schema level. |

---

## 1. CORE ENTITIES

### 1.1 ENTITY: Tenant

Represents an organization using Sovereign CRM.

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| id | UUID | PK | auto | |
| name | String(255) | YES | — | Organization name |
| slug | String(100) | YES | — | URL-friendly unique ID |
| vertical | Enum | YES | 'generic' | 'generic', 'it_consulting', 'saas' |
| subscription_tier | Enum | YES | 'free' | 'free', 'starter', 'professional', 'enterprise' |
| status | Enum | YES | 'active' | 'active', 'suspended', 'cancelled', 'trial' |
| domain | String(255) | NO | null | Primary email domain |
| logo_url | String(500) | NO | null | |
| timezone | String(50) | YES | 'UTC' | |
| default_currency | String(3) | YES | 'USD' | ISO 4217 |
| date_format | String(20) | YES | 'YYYY-MM-DD' | |
| features | JSONB | NO | '{}' | Enabled feature flags |
| settings | JSONB | NO | '{}' | Tenant-level configurations |
| created_at | Timestamptz | YES | now() | |
| updated_at | Timestamptz | YES | now() | |
| deleted_at | Timestamptz | NO | null | |

**Indexes:** slug (unique), domain, status, vertical

---

### 1.2 ENTITY: User

Every person who logs into the system.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| email | String(255) | YES | Unique within tenant |
| password_hash | String(255) | YES | bcrypt |
| first_name | String(100) | YES | |
| last_name | String(100) | YES | |
| job_title | String(200) | NO | |
| phone | String(50) | NO | |
| mobile_phone | String(50) | NO | |
| timezone | String(50) | NO | Inherits from tenant |
| locale | String(10) | NO | 'en-US' default |
| avatar_url | String(500) | NO | |
| status | Enum | YES | 'active', 'inactive', 'locked' |
| last_login_at | Timestamptz | NO | |
| last_login_ip | String(45) | NO | |
| mfa_enabled | Boolean | NO | false |
| mfa_secret | String(100) | NO | encrypted |
| password_changed_at | Timestamptz | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Relationships:** belongs_to Tenant, has_many Activity, has_many Deal (as owner), has_many Contact, has_many Lead
**Indexes:** (tenant_id, email) unique, (tenant_id, status), last_login_at

---

### 1.3 ENTITY: Role

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(100) | YES | 'Sales Rep', 'Manager', 'Admin', 'Read Only' |
| description | String(500) | NO | |
| is_system | Boolean | YES | true for protected system roles |
| permissions | JSONB | YES | Full permission set (see Phase 12) |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

**Relationships:** has_many UserRole

---

### 1.4 ENTITY: UserRole

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| user_id | UUID | FK→User | |
| role_id | UUID | FK→Role | |
| assigned_at | Timestamptz | YES | |
| assigned_by | UUID | FK→User | |

**Indexes:** (user_id, role_id) unique

---

### 1.5 ENTITY: Team

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(100) | YES | |
| description | String(500) | NO | |
| manager_id | UUID | FK→User | Team lead |
| parent_team_id | UUID | FK→Team | null, for hierarchy |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

---

### 1.6 ENTITY: TeamMember

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| team_id | UUID | FK→Team | |
| user_id | UUID | FK→User | |
| role | Enum | YES | 'member', 'manager', 'viewer' |
| joined_at | Timestamptz | YES | |

---

### 1.7 ENTITY: Organization (Account)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| legal_name | String(255) | NO | |
| website | String(500) | NO | |
| phone | String(50) | NO | |
| email | String(255) | NO | |
| industry | String(100) | NO | |
| sub_industry | String(100) | NO | |
| employee_count | Integer | NO | Range or exact |
| annual_revenue | Decimal(15,2) | NO | |
| currency | String(3) | NO | |
| description | Text | NO | |
| type | Enum | YES | 'customer', 'prospect', 'partner', 'vendor', 'competitor', 'other' |
| owner_id | UUID | FK→User | |
| territory_id | UUID | FK→Territory | |
| lead_source | String(100) | NO | |
| rating | Integer | NO | 1-5 |
| sic_code | String(20) | NO | Standard Industrial Classification |
| naics_code | String(20) | NO | NAICS classification |
| parent_org_id | UUID | FK→Organization | null for top-level |
| billing_address | JSONB | NO | structured address |
| shipping_address | JSONB | NO | structured address |
| social_links | JSONB | NO | linkedin, twitter, facebook |
| custom_fields | JSONB | NO | Dynamic fields per tenant |
| ai_summary | Text | NO | AI-generated summary |
| health_score | Integer | NO | SaaS vertical |
| tags | String[] | NO | |
| status | Enum | YES | 'active', 'inactive', 'archived' |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Relationships:** belongs_to Tenant, belongs_to User (owner), has_many Contact, has_many Deal, has_many Activity
**Indexes:** (tenant_id, name), (tenant_id, owner_id), (tenant_id, industry), (tenant_id, type), status, created_at

---

### 1.8 ENTITY: Contact

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| organization_id | UUID | FK→Organization | null for individuals |
| first_name | String(100) | YES | |
| last_name | String(100) | YES | |
| job_title | String(200) | NO | |
| department | String(100) | NO | |
| email | String(255) | YES | Primary email |
| email_alt | String(255) | NO | Secondary |
| phone | String(50) | NO | Work |
| phone_mobile | String(50) | NO | |
| phone_home | String(50) | NO | |
| linkedin_url | String(500) | NO | |
| twitter_handle | String(100) | NO | |
| address | JSONB | NO | Structured address |
| description | Text | NO | |
| owner_id | UUID | FK→User | |
| lead_source | String(100) | NO | |
| lifecycle_stage | Enum | YES | 'lead', 'mql', 'sql', 'opportunity', 'customer', 'churned', 'evangelist' |
| email_opt_out | Boolean | NO | false |
| email_bounced | Boolean | NO | false |
| do_not_call | Boolean | NO | false |
| rating | Integer | NO | 1-5 |
| role | Enum | NO | 'decision_maker', 'champion', 'influencer', 'blocker', 'user', 'evaluator', 'other' |
| custom_fields | JSONB | NO | |
| ai_summary | Text | NO | AI-generated |
| tags | String[] | NO | |
| status | Enum | YES | 'active', 'inactive', 'archived' |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Relationships:** belongs_to Tenant, belongs_to Organization, belongs_to User (owner), has_many DealContact
**Indexes:** (tenant_id, email) unique, (tenant_id, organization_id), (tenant_id, owner_id), (tenant_id, lifecycle_stage), full_text search on (first_name || ' ' || last_name)

---

### 1.9 ENTITY: Lead

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| salutation | String(20) | NO | |
| first_name | String(100) | YES | |
| last_name | String(100) | YES | |
| job_title | String(200) | NO | |
| email | String(255) | NO | |
| phone | String(50) | NO | |
| company | String(255) | NO | Company name (before conversion to Organization) |
| website | String(500) | NO | |
| industry | String(100) | NO | |
| employee_count | Integer | NO | |
| lead_source | String(100) | NO | |
| lead_source_detail | String(200) | NO | Campaign/page specific |
| status | Enum | YES | 'new', 'contacted', 'qualified', 'disqualified', 'converted' |
| status_reason | String(200) | NO | Why disqualified |
| score | Integer | NO | 0 | Lead score |
| score_details | JSONB | NO | Scoring breakdown |
| rating | Enum | NO | 'hot', 'warm', 'cold' |
| owner_id | UUID | FK→User | |
| assigned_at | Timestamptz | NO | |
| converted_at | Timestamptz | NO | |
| converted_contact_id | UUID | FK→Contact | |
| converted_org_id | UUID | FK→Organization | |
| converted_deal_id | UUID | FK→Deal | |
| description | Text | NO | |
| custom_fields | JSONB | NO | |
| tags | String[] | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, email), (tenant_id, status), (tenant_id, owner_id), (tenant_id, score DESC), (tenant_id, created_at)

---

### 1.10 ENTITY: Deal (Opportunity)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| amount | Decimal(15,2) | YES | |
| currency | String(3) | YES | 'USD' |
| probability | Integer | YES | 0-100 |
| stage_id | UUID | FK→PipelineStage | |
| pipeline_id | UUID | FK→Pipeline | |
| close_date | Date | YES | |
| expected_revenue | Decimal(15,2) | NO | amount * probability |
| type | Enum | YES | 'new_business', 'renewal', 'expansion', 'upsell', 'cross_sell' |
| lead_source | String(100) | NO | |
| primary_contact_id | UUID | FK→Contact | |
| organization_id | UUID | FK→Organization | |
| owner_id | UUID | FK→User | |
| team_id | UUID | FK→Team | |
| territory_id | UUID | FK→Territory | |
| win_reason | Text | NO | |
| win_reason_category | String(100) | NO | |
| loss_reason | Text | NO | |
| loss_reason_category | String(100) | NO | |
| competitor | String(200) | NO | |
| discount_amount | Decimal(15,2) | NO | |
| discount_percent | Decimal(5,2) | NO | |
| forecast_category | Enum | YES | 'pipeline', 'best_case', 'commit', 'closed' |
| ai_win_probability | Decimal(5,2) | NO | ML-calculated |
| ai_risk_score | Integer | NO | 1-10 |
| ai_next_best_action | String(500) | NO | |
| ai_last_analysis | Timestamptz | NO | |
| custom_fields | JSONB | NO | |
| tags | String[] | NO | |
| status | Enum | YES | 'open', 'won', 'lost', 'abandoned' |
| closed_at | Timestamptz | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Relationships:** belongs_to Tenant, belongs_to Pipeline+Stage, belongs_to Contact, belongs_to Organization, belongs_to User, has_many DealContact, has_many DealProduct, has_many Activity
**Indexes:** (tenant_id, stage_id), (tenant_id, owner_id), (tenant_id, close_date), (tenant_id, organization_id), (tenant_id, status), (tenant_id, amount DESC), full_text on name

---

### 1.11 ENTITY: DealContact (Junction)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| deal_id | UUID | FK→Deal | |
| contact_id | UUID | FK→Contact | |
| role | Enum | YES | 'decision_maker', 'champion', 'influencer', 'blocker', 'evaluator', 'end_user', 'procurement', 'legal', 'other' |
| influence_level | Integer | NO | 1-5 |
| notes | Text | NO | |

**Indexes:** (deal_id, contact_id) unique

---

### 1.12 ENTITY: Pipeline

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(100) | YES | 'Default Sales Pipeline' |
| description | String(500) | NO | |
| entity_type | Enum | YES | 'deal', 'lead', 'custom' |
| is_default | Boolean | NO | false |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

---

### 1.13 ENTITY: PipelineStage

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| pipeline_id | UUID | FK→Pipeline | |
| name | String(100) | YES | |
| display_order | Integer | YES | |
| probability_default | Integer | YES | 0-100 |
| probability_min | Integer | NO | |
| probability_max | Integer | NO | |
| category | Enum | YES | 'pipeline', 'best_case', 'commit', 'closed_won', 'closed_lost' |
| required_fields | String[] | NO | Fields that must be filled before moving to this stage |
| is_active | Boolean | YES | true |
| created_at | Timestamptz | YES | |

**Indexes:** (pipeline_id, display_order)

---

### 1.14 ENTITY: Product

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| sku | String(100) | NO | |
| unit_price | Decimal(15,2) | YES | |
| currency | String(3) | YES | |
| cost | Decimal(15,2) | NO | |
| category | String(100) | NO | |
| type | Enum | YES | 'one_time', 'subscription', 'service', 'license', 'consumable' |
| billing_frequency | Enum | NO | 'monthly', 'quarterly', 'annual', 'one_time' |
| is_active | Boolean | YES | true |
| custom_fields | JSONB | NO | |
| created_at | Timestamptz | YES | |

---

### 1.15 ENTITY: DealProduct

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| deal_id | UUID | FK→Deal | |
| product_id | UUID | FK→Product | |
| quantity | Integer | YES | 1 |
| unit_price | Decimal(15,2) | YES | Override from Product |
| discount_percent | Decimal(5,2) | NO | |
| total_price | Decimal(15,2) | YES | Computed |
| description | Text | NO | |
| sort_order | Integer | NO | |

---

### 1.16 ENTITY: Activity (Polymorphic)

The universal activity record. Can be attached to any parent entity.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| type | Enum | YES | 'call', 'email', 'meeting', 'task', 'note', 'sms', 'chat', 'system', 'sequence_step' |
| subject | String(500) | YES | |
| description | Text | NO | |
| status | Enum | YES | 'planned', 'completed', 'cancelled', 'overdue' |
| priority | Enum | YES | 'low', 'medium', 'high', 'critical' |
| direction | Enum | NO | 'inbound', 'outbound', 'internal' — for calls/emails |
| start_date | Timestamptz | NO | |
| end_date | Timestamptz | NO | |
| duration_minutes | Integer | NO | |
| due_date | Date | NO | For tasks |
| completed_at | Timestamptz | NO | |
| owner_id | UUID | FK→User | Who did the activity |
| assigned_to_id | UUID | FK→User | For tasks |
| parent_type | String(50) | YES | Polymorphic: 'Contact', 'Deal', 'Lead', 'Organization', etc. |
| parent_id | UUID | YES | Polymorphic FK |
| is_completed | Boolean | NO | false |
| is_private | Boolean | NO | false |
| call_outcome | String(100) | NO | 'no_answer', 'left_voicemail', 'connected', 'meeting_set', 'not_interested' |
| call_disposition | String(100) | NO | |
| call_recording_url | String(500) | NO | |
| email_message_id | String(255) | NO | For threading |
| email_to | String[] | NO | |
| email_cc | String[] | NO | |
| email_bcc | String[] | NO | |
| email_opened_at | Timestamptz | NO | |
| email_clicked_at | Timestamptz | NO | |
| email_template_id | UUID | FK→EmailTemplate | |
| meeting_location | String(500) | NO | |
| meeting_attendees | UUID[] | NO | User IDs |
| meeting_notes | Text | NO | |
| meeting_recording_url | String(500) | NO | |
| task_category | String(100) | NO | |
| reminder_at | Timestamptz | NO | |
| recurrence_rule | String(255) | NO | RRULE format |
| custom_fields | JSONB | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, parent_type, parent_id), (tenant_id, owner_id), (tenant_id, type), (tenant_id, status), (tenant_id, due_date), (tenant_id, created_at DESC)
**Super-important:** This is the most-queried entity in the system. Must have aggressive indexing and partitioning (by created_at date range).

---

### 1.17 ENTITY: Note

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| title | String(500) | NO | |
| body | Text | YES | Rich text |
| body_plain | Text | NO | Plain text version |
| parent_type | String(50) | YES | Polymorphic |
| parent_id | UUID | YES | |
| owner_id | UUID | FK→User | |
| is_pinned | Boolean | NO | false |
| mentions | UUID[] | NO | @mentioned user IDs |
| custom_fields | JSONB | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, parent_type, parent_id), full_text on body

---

## 2. IT CONSULTING VERTICAL ENTITIES

### 2.1 ENTITY: Engagement (Project)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| engagement_type | Enum | YES | 'fixed_bid', 'time_materials', 'retainer', 'managed_service', 'staff_augmentation' |
| sow_id | UUID | FK→SOW | |
| organization_id | UUID | FK→Organization | Client |
| primary_contact_id | UUID | FK→Contact | Client POC |
| delivery_manager_id | UUID | FK→User | |
| status | Enum | YES | 'proposed', 'active', 'on_hold', 'completed', 'cancelled', 'closed' |
| start_date | Date | YES | |
| end_date | Date | NO | |
| planned_hours | Decimal(10,2) | NO | |
| budget_amount | Decimal(15,2) | YES | |
| budget_currency | String(3) | YES | |
| total_billed | Decimal(15,2) | NO | Computed from time entries |
| total_cost | Decimal(15,2) | NO | Computed |
| margin_percent | Decimal(5,2) | NO | Computed |
| billing_frequency | Enum | YES | 'weekly', 'biweekly', 'monthly', 'milestone' |
| billing_currency | String(3) | YES | |
| po_number | String(100) | NO | Purchase Order # |
| po_amount | Decimal(15,2) | NO | |
| po_expiry | Date | NO | |
| description | Text | NO | |
| risks | JSONB | NO | Risk register |
| milestones | JSONB | NO | Key dates |
| health_score | Enum | NO | 'green', 'yellow', 'red' |
| health_reason | Text | NO | |
| custom_fields | JSONB | NO | |
| tags | String[] | NO | |
| deal_id | UUID | FK→Deal | Optional link back |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, organization_id), (tenant_id, status), (tenant_id, delivery_manager_id), (tenant_id, start_date)
**Relationships:** belongs_to Organization, belongs_to SOW, has_many TimeEntry, has_many Expense, has_many EngagementResource

---

### 2.2 ENTITY: SOW (Statement of Work)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| sow_number | String(50) | YES | Auto-generated |
| version | Integer | YES | 1 |
| organization_id | UUID | FK→Organization | |
| engagement_id | UUID | FK→Engagement | null if not yet converted |
| status | Enum | YES | 'draft', 'pending_approval', 'approved', 'signed', 'active', 'completed', 'cancelled' |
| total_value | Decimal(15,2) | YES | |
| currency | String(3) | YES | |
| start_date | Date | YES | |
| end_date | Date | YES | |
| scope_description | Text | YES | |
| deliverables | JSONB | NO | Array of deliverables |
| milestones | JSONB | NO | Payment milestones |
| payment_terms | Text | NO | |
| resource_requirements | JSONB | NO | Skills, roles, counts |
| approver_id | UUID | FK→User | Internal approver |
| approved_at | Timestamptz | NO | |
| signed_at | Timestamptz | NO | |
| signed_by | String(200) | NO | Client signatory name |
| document_url | String(500) | NO | PDF location |
| template_id | UUID | FK→SOWTemplate | |
| custom_fields | JSONB | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, sow_number) unique, (tenant_id, organization_id), (tenant_id, status)

---

### 2.3 ENTITY: SOWTemplate

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| content_template | Text | YES | Rich text with merge fields |
| sections | JSONB | YES | Section structure |
| default_terms | Text | NO | |
| is_active | Boolean | YES | true |
| created_at | Timestamptz | YES | |

---

### 2.4 ENTITY: ChangeOrder

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| engagement_id | UUID | FK→Engagement | |
| change_order_number | String(50) | YES | |
| reason | Text | YES | |
| scope_change | Text | YES | |
| budget_change | Decimal(15,2) | YES | Signed + or - |
| schedule_change_days | Integer | NO | |
| status | Enum | YES | 'draft', 'pending_approval', 'approved', 'rejected', 'implemented' |
| approved_by | UUID | FK→User | |
| approved_at | Timestamptz | NO | |
| created_at | Timestamptz | YES | |

---

### 2.5 ENTITY: Resource (Consultant)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| user_id | UUID | FK→User | Links to CRM user |
| employee_id | String(50) | NO | HR code |
| skill_tags | String[] | NO | Array of skill names |
| certifications | JSONB | NO | [{name, issuer, expiry}] |
| role_title | String(200) | YES | 'Senior Consultant', 'Architect' |
| role_level | Enum | YES | 'junior', 'mid', 'senior', 'lead', 'principal', 'partner' |
| billable_target_hours | Integer | YES | Annual target |
| utilization_target_percent | Decimal(5,2) | YES | e.g., 80.00 |
| cost_rate | Decimal(10,2) | YES | Internal cost/hr |
| billable_rate_default | Decimal(10,2) | YES | Default bill rate |
| currency | String(3) | YES | |
| availability_status | Enum | YES | 'available', 'allocated', 'partial', 'leave', 'exited' |
| availability_start | Date | NO | When next available |
| location | String(200) | NO | City, office |
| timezone | String(50) | NO | |
| visa_status | String(100) | NO | For global consulting |
| custom_fields | JSONB | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, user_id) unique, (tenant_id, role_level), (tenant_id, availability_status), GIN on skill_tags

---

### 2.6 ENTITY: EngagementResource (Allocation)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| engagement_id | UUID | FK→Engagement | |
| resource_id | UUID | FK→Resource | |
| role_on_project | String(200) | YES | |
| allocation_percent | Integer | YES | 0-100 |
| start_date | Date | YES | |
| end_date | Date | YES | |
| billable_rate | Decimal(10,2) | YES | Project-specific rate |
| cost_rate | Decimal(10,2) | YES | |
| is_billable | Boolean | YES | true |
| status | Enum | YES | 'planned', 'active', 'completed', 'released' |
| notes | Text | NO | |
| created_at | Timestamptz | YES | |

**Indexes:** (engagement_id, resource_id), (resource_id, start_date, end_date)
**Constraint:** No overlapping allocations for same resource (exclusion constraint on daterange)

---

### 2.7 ENTITY: RateCard

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | 'Standard 2026', 'Acme Corp Special' |
| effective_date | Date | YES | |
| expiry_date | Date | NO | |
| is_default | Boolean | NO | false |
| organization_id | UUID | FK→Organization | null = company-wide |
| status | Enum | YES | 'draft', 'active', 'archived' |
| created_at | Timestamptz | YES | |

---

### 2.8 ENTITY: RateCardLine

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| rate_card_id | UUID | FK→RateCard | |
| role_level | Enum | YES | matches Resource.role_level |
| skill | String(100) | NO | null = all skills |
| bill_rate | Decimal(10,2) | YES | |
| cost_rate | Decimal(10,2) | YES | |
| currency | String(3) | YES | |
| overtime_rate_multiplier | Decimal(4,2) | NO | |
| created_at | Timestamptz | YES | |

---

### 2.9 ENTITY: TimeEntry

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| resource_id | UUID | FK→Resource | |
| engagement_id | UUID | FK→Engagement | |
| date | Date | YES | |
| hours | Decimal(5,2) | YES | |
| billable_hours | Decimal(5,2) | Yes | 0.00 |
| type | Enum | YES | 'billable', 'non_billable', 'pto', 'training', 'admin', 'bench', 'travel' |
| description | Text | NO | |
| category | String(100) | NO | 'development', 'architecture', 'meeting', 'research', 'documentation' |
| overtime | Boolean | NO | false |
| billable_rate | Decimal(10,2) | NO | Snapshot of rate at time |
| amount | Decimal(10,2) | NO | billable_hours * billable_rate |
| status | Enum | YES | 'draft', 'submitted', 'approved', 'rejected', 'billed' |
| approved_by | UUID | FK→User | |
| approved_at | Timestamptz | NO | |
| rejection_reason | Text | NO | |
| external_id | String(100) | NO | For Jira/Tempo sync |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

**Indexes:** (tenant_id, resource_id, date), (tenant_id, engagement_id), (tenant_id, status), (tenant_id, date), (resource_id, date)
**Critical index:** (engagement_id, status) for billing runs

---

### 2.10 ENTITY: Expense

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| engagement_id | UUID | FK→Engagement | |
| resource_id | UUID | FK→Resource | |
| category | Enum | YES | 'travel', 'lodging', 'meals', 'software', 'supplies', 'transportation', 'other' |
| amount | Decimal(10,2) | YES | |
| currency | String(3) | YES | |
| expense_date | Date | YES | |
| receipt_url | String(500) | NO | |
| description | Text | NO | |
| is_billable | Boolean | YES | true |
| billable_amount | Decimal(10,2) | NO | |
| status | Enum | YES | 'draft', 'submitted', 'approved', 'rejected', 'reimbursed', 'billed' |
| approved_by | UUID | FK→User | |
| approved_at | Timestamptz | NO | |
| created_at | Timestamptz | YES | |

---

## 3. SAAS VERTICAL ENTITIES

### 3.1 ENTITY: Subscription

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| organization_id | UUID | FK→Organization | |
| external_id | String(255) | NO | From Stripe/Zuora/etc |
| plan_name | String(200) | YES | |
| plan_tier | String(100) | YES | |
| status | Enum | YES | 'trial', 'active', 'past_due', 'cancelled', 'expired', 'paused' |
| mrr | Decimal(10,2) | YES | Monthly recurring revenue |
| arr | Decimal(10,2) | NO | Annualized |
| currency | String(3) | YES | |
| billing_frequency | Enum | YES | 'monthly', 'quarterly', 'semi_annual', 'annual' |
| seats | Integer | NO | Number of licenses |
| unit_price | Decimal(10,2) | NO | |
| trial_end_date | Date | NO | |
| current_term_start | Date | YES | |
| current_term_end | Date | YES | |
| renewal_date | Date | NO | |
| cancellation_date | Date | NO | |
| cancellation_reason | String(500) | NO | |
| churn_category | Enum | NO | 'voluntary', 'involuntary', 'dunning_failure' |
| payment_method | String(100) | NO | |
| auto_renew | Boolean | YES | true |
| health_score | Integer | NO | 1-100 |
| custom_fields | JSONB | NO | |
| tags | String[] | NO | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |
| deleted_at | Timestamptz | NO | |

**Indexes:** (tenant_id, organization_id), (tenant_id, status), (tenant_id, renewal_date), (tenant_id, mrr DESC), (tenant_id, external_id)

---

### 3.2 ENTITY: SubscriptionAddon

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| subscription_id | UUID | FK→Subscription | |
| name | String(200) | YES | |
| mrr | Decimal(10,2) | YES | |
| quantity | Integer | YES | 1 |
| created_at | Timestamptz | YES | |

---

### 3.3 ENTITY: Invoice

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| organization_id | UUID | FK→Organization | |
| subscription_id | UUID | FK→Subscription | |
| external_id | String(255) | NO | |
| invoice_number | String(100) | YES | |
| amount | Decimal(15,2) | YES | |
| amount_paid | Decimal(15,2) | YES | 0.00 |
| amount_due | Decimal(15,2) | YES | |
| currency | String(3) | YES | |
| status | Enum | YES | 'draft', 'sent', 'paid', 'past_due', 'cancelled', 'refunded', 'uncollectible' |
| issue_date | Date | YES | |
| due_date | Date | YES | |
| paid_at | Timestamptz | NO | |
| billing_period_start | Date | NO | |
| billing_period_end | Date | NO | |
| line_items | JSONB | NO | |
| pdf_url | String(500) | NO | |
| created_at | Timestamptz | YES | |

**Indexes:** (tenant_id, organization_id), (tenant_id, status), (tenant_id, due_date)

---

### 3.4 ENTITY: ProductUsage (Usage Metric)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| organization_id | UUID | FK→Organization | |
| metric_name | String(100) | YES | 'api_calls', 'active_users', 'storage_gb', 'reports_run' |
| metric_value | Decimal(15,2) | YES | |
| recorded_at | Date | YES | |
| source | String(100) | NO | 'product_api', 'stripe_metered', 'manual' |
| created_at | Timestamptz | YES | |

**Indexes:** (tenant_id, organization_id, metric_name, recorded_at), (tenant_id, recorded_at)

---

## 4. CUSTOMIZATION FRAMEWORK ENTITIES (Dynamic Object Builder)

### 4.1 ENTITY: CustomEntityDefinition

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(100) | YES | e.g., 'Engagement', 'Subscription' |
| api_name | String(100) | YES | e.g., 'Engagement__c' |
| plural_label | String(100) | YES | e.g., 'Engagements' |
| description | String(500) | NO | |
| is_standard | Boolean | YES | false for user-created |
| is_active | Boolean | YES | true |
| enable_activities | Boolean | YES | true |
| enable_notes | Boolean | YES | true |
| enable_files | Boolean | YES | true |
| enable_audit | Boolean | YES | true |
| enable_pipeline | Boolean | NO | false |
| enable_duplicate_rules | Boolean | NO | false |
| record_label_field | String(100) | NO | Field used as display name |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

---

### 4.2 ENTITY: CustomFieldDefinition

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| entity_id | UUID | FK→CustomEntityDefinition | |
| name | String(100) | YES | Display name |
| api_name | String(100) | YES | e.g., 'Billing_Contact__c' |
| field_type | Enum | YES | 'text', 'textarea', 'number', 'currency', 'date', 'datetime', 'boolean', 'picklist', 'multipicklist', 'lookup', 'formula', 'email', 'phone', 'url', 'address', 'autonumber', 'file', 'image', 'json' |
| is_required | Boolean | NO | false |
| is_unique | Boolean | NO | false |
| is_read_only | Boolean | NO | false |
| default_value | String(500) | NO | |
| max_length | Integer | NO | For text fields |
| precision | Integer | NO | Decimal places |
| picklist_values | String[] | NO | For picklist types |
| lookup_entity_id | UUID | FK→CustomEntityDefinition | For lookup fields |
| lookup_relationship_name | String(100) | NO | |
| formula_expression | Text | NO | For formula fields |
| autonumber_prefix | String(50) | NO | |
| autonumber_start | Integer | NO | |
| autonumber_min_digits | Integer | NO | |
| help_text | String(500) | NO | |
| display_order | Integer | NO | |
| section_id | UUID | FK→FieldSection | |
| is_audited | Boolean | NO | false |
| is_indexed | Boolean | NO | false |
| status | Enum | YES | 'active', 'inactive', 'deployed' |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

---

### 4.3 ENTITY: FieldSection

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| entity_id | UUID | FK→CustomEntityDefinition | |
| name | String(100) | YES | 'General Information', 'Financial Details' |
| display_order | Integer | YES | |
| is_collapsible | Boolean | NO | true |

---

### 4.4 ENTITY: Layout

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| entity_id | UUID | FK→CustomEntityDefinition | |
| name | String(100) | YES | 'Default Layout', 'Manager Layout' |
| type | Enum | YES | 'page', 'compact', 'search' |
| layout_definition | JSONB | YES | Column/row/field placements |
| is_default | Boolean | NO | false |
| assigned_roles | UUID[] | NO | Which roles see this layout |
| created_at | Timestamptz | YES | |

---

## 5. SYSTEM / ADMIN ENTITIES

### 5.1 ENTITY: WorkflowRule

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| entity_id | UUID | FK→CustomEntityDefinition | |
| trigger_type | Enum | YES | 'before_create', 'after_create', 'before_update', 'after_update', 'before_delete', 'stage_change', 'time_based', 'scheduled' |
| trigger_conditions | JSONB | YES | Condition tree (AND/OR groups) |
| actions | JSONB | YES | Action array (ordered) |
| is_active | Boolean | YES | false |
| evaluation_order | Integer | NO | |
| error_handling | Enum | YES | 'stop', 'skip', 'continue' |
| version | Integer | YES | 1 |
| created_by | UUID | FK→User | |
| created_at | Timestamptz | YES | |
| updated_at | Timestamptz | YES | |

**Action types:**
- `update_field`: Set field to value/formula
- `create_record`: Create related record
- `send_email`: Send email notification
- `call_webhook`: POST to URL
- `assign_owner`: Change record owner
- `add_to_sequence`: Enroll in sequence
- `update_score`: Modify lead score
- `create_task`: Create activity task

---

### 5.2 ENTITY: ApprovalProcess

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| entity_id | UUID | FK→CustomEntityDefinition | |
| trigger_conditions | JSONB | YES | When this approval is needed |
| steps | JSONB | YES | Ordered approval steps |
| is_active | Boolean | YES | false |
| created_at | Timestamptz | YES | |

**Step definition (JSON):**
```json
{
  "step_number": 1,
  "approver_type": "user|role|manager|field",
  "approver_id": "uuid or null",
  "approver_field": "field_api_name (if type=field)",
  "order_type": "parallel|sequential",
  "escalation_minutes": 1440,
  "escalation_approver_id": "uuid",
  "actions_on_approve": ["send_email", "update_field"],
  "actions_on_reject": ["send_email", "update_field"]
}
```

---

### 5.3 ENTITY: ApprovalInstance

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| approval_process_id | UUID | FK→ApprovalProcess | |
| record_id | UUID | YES | Polymorphic |
| record_type | String(100) | YES | |
| status | Enum | YES | 'pending', 'approved', 'rejected', 'escalated', 'withdrawn' |
| current_step | Integer | NO | |
| submitted_by | UUID | FK→User | |
| submitted_at | Timestamptz | YES | |
| completed_at | Timestamptz | NO | |

---

### 5.4 ENTITY: ApprovalAction

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| approval_instance_id | UUID | FK→ApprovalInstance | |
| step_number | Integer | YES | |
| approver_id | UUID | FK→User | |
| action | Enum | YES | 'approved', 'rejected', 'reassigned', 'escalated' |
| comments | Text | NO | |
| acted_at | Timestamptz | YES | |

---

### 5.5 ENTITY: EmailTemplate

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| subject | String(500) | YES | With merge fields |
| body_html | Text | YES | |
| body_plain | Text | NO | |
| category | String(100) | NO | 'sales', 'marketing', 'system', 'notification' |
| merge_fields | String[] | NO | Available merge fields |
| is_system | Boolean | NO | false |
| created_at | Timestamptz | YES | |

---

### 5.6 ENTITY: DocumentTemplate

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| type | Enum | YES | 'proposal', 'quote', 'sow', 'contract', 'report', 'other' |
| content | Text | YES | Rich text/DOCX template |
| merge_fields | String[] | NO | |
| created_at | Timestamptz | YES | |

---

### 5.7 ENTITY: Sequence

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| entity_type | Enum | YES | 'lead', 'contact' |
| steps | JSONB | YES | Ordered step array |
| stats | JSONB | NO | Performance metrics |
| is_active | Boolean | YES | false |
| created_at | Timestamptz | YES | |

**Step definition:**
```json
{
  "step_order": 1,
  "type": "email|call|sms|task|wait",
  "subject": "Follow-up",
  "content": "Hi {{first_name}}...",
  "delay_hours": 24,
  "condition": "{{lead.status}} != 'converted'"
}
```

---

### 5.8 ENTITY: SequenceEnrollment

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| sequence_id | UUID | FK→Sequence | |
| record_id | UUID | YES | Lead or Contact |
| record_type | String(50) | YES | |
| status | Enum | YES | 'active', 'paused', 'completed', 'exited' |
| current_step | Integer | YES | 0 |
| entered_at | Timestamptz | YES | |
| completed_at | Timestamptz | NO | |
| exit_reason | String(200) | NO | 'replied', 'converted', 'opted_out', 'manual' |

---

### 5.9 ENTITY: Webhook

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| url | String(500) | YES | |
| events | String[] | YES | Array of event types |
| secret | String(255) | YES | For HMAC signing |
| format | Enum | YES | 'json', 'xml' |
| is_active | Boolean | YES | true |
| retry_count | Integer | YES | 3 |
| retry_interval_seconds | Integer | YES | 300 |
| timeout_seconds | Integer | YES | 30 |
| created_at | Timestamptz | YES | |

---

### 5.10 ENTITY: WebhookLog

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| webhook_id | UUID | FK→Webhook | |
| event_type | String(100) | YES | |
| payload | JSONB | YES | |
| status | Enum | YES | 'success', 'failed', 'retrying' |
| http_status | Integer | NO | |
| response_body | Text | NO | |
| attempts | Integer | YES | 1 |
| executed_at | Timestamptz | YES | |

---

### 5.11 ENTITY: AuditEntry

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| actor_id | UUID | FK→User | Who did it |
| action | Enum | YES | 'create', 'update', 'delete', 'read', 'login', 'export', 'config_change' |
| entity_type | String(100) | YES | 'Contact', 'Deal', etc. |
| entity_id | UUID | YES | Record ID |
| field_name | String(100) | NO | For field-level updates |
| old_value | Text | NO | |
| new_value | Text | NO | |
| metadata | JSONB | NO | IP, user_agent, session_id |
| created_at | Timestamptz | YES | |

**Indexes:** (tenant_id, entity_type, entity_id), (tenant_id, actor_id), (tenant_id, created_at DESC), (tenant_id, action)
**Partitioning:** By month (created_at) for performance at scale

---

### 5.12 ENTITY: SavedSearch

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| entity_type | String(100) | YES | |
| filters | JSONB | YES | Filter tree |
| columns | String[] | YES | Visible columns |
| sort_by | String(100) | NO | |
| sort_order | Enum | NO | 'asc', 'desc' |
| is_shared | Boolean | NO | false |
| owner_id | UUID | FK→User | |
| created_at | Timestamptz | YES | |

---

## 6. REPORTING ENTITIES

### 6.1 ENTITY: Report

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| entity_type | String(100) | YES | |
| report_type | Enum | YES | 'tabular', 'summary', 'matrix', 'chart' |
| filters | JSONB | YES | |
| groupings | JSONB | NO | |
| metrics | JSONB | YES | |
| chart_type | Enum | NO | 'bar', 'line', 'pie', 'funnel', 'donut', 'area', 'pivot_table' |
| chart_config | JSONB | NO | Colors, labels, axis |
| is_scheduled | Boolean | NO | false |
| schedule_cron | String(100) | NO | |
| schedule_recipients | String[] | NO | Email addresses |
| owner_id | UUID | FK→User | |
| is_shared | Boolean | NO | false |
| created_at | Timestamptz | YES | |

---

### 6.2 ENTITY: Dashboard

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| description | Text | NO | |
| layout | JSONB | YES | Widget grid positions |
| is_shared | Boolean | NO | false |
| is_default | Boolean | NO | false |
| owner_id | UUID | FK→User | |
| created_at | Timestamptz | YES | |

---

### 6.3 ENTITY: DashboardWidget

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| dashboard_id | UUID | FK→Dashboard | |
| report_id | UUID | FK→Report | null for metric widgets |
| widget_type | Enum | YES | 'chart', 'metric', 'list', 'feed', 'html' |
| title | String(255) | YES | |
| metric_value | String(500) | NO | For simple metric display |
| metric_label | String(100) | NO | |
| width | Integer | YES | 1-4 (grid units) |
| height | Integer | YES | 1-3 |
| position_x | Integer | YES | |
| position_y | Integer | YES | |
| refresh_interval | Integer | NO | Minutes |

---

## 7. FILE & ATTACHMENT

### 7.1 ENTITY: FileAttachment

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | PK | |
| tenant_id | UUID | FK→Tenant | |
| name | String(255) | YES | |
| file_name | String(255) | YES | Original name |
| mime_type | String(100) | YES | |
| size_bytes | Integer | YES | |
| storage_path | String(500) | YES | Object store path |
| storage_provider | Enum | YES | 'local', 's3', 'gcs', 'azure' |
| parent_type | String(50) | YES | |
| parent_id | UUID | YES | |
| owner_id | UUID | FK→User | |
| is_deleted | Boolean | NO | false |
| created_at | Timestamptz | YES | |

---

## 8. ENTITY RELATIONSHIP MAP

```
Tenant ──┬── User ──────── TeamMember ─── Team
         │     │                │
         │     └── Role ─── UserRole
         │
         ├── Organization ──┬── Contact
         │                  ├── Deal
         │                  ├── Subscription (SaaS)
         │                  └── Engagement (ITC)
         │
         ├── Lead ──────┐
         │              ├── Contact
         │              ├── Organization
         │              └── Deal
         │
         ├── Deal ──────┬── DealContact ──── Contact
         │              ├── DealProduct ──── Product
         │              └── Activity
         │
         ├── Pipeline ─── PipelineStage
         │
         ├── Activity (polymorphic parent)
         ├── Note (polymorphic parent)
         ├── FileAttachment (polymorphic parent)
         │
         ├── Engagement ──┬── SOW
         │                ├── TimeEntry ──── Resource
         │                ├── Expense
         │                ├── EngagementResource ── Resource
         │                └── ChangeOrder
         │
         ├── Resource ──── RateCardLine ──── RateCard
         │
         ├── Subscription ──┬── Invoice
         │                  ├── SubscriptionAddon
         │                  └── ProductUsage
         │
         └── CustomEntityDefinition ──┬── CustomFieldDefinition
                                      ├── FieldSection
                                      └── Layout
```

---

## 9. INDEX STRATEGY

| Priority | Entity | Index | Reason |
|:--------:|--------|-------|--------|
| 1 | Activity | (tenant_id, parent_type, parent_id, created_at DESC) | Every record page loads activity timeline |
| 2 | Activity | (tenant_id, owner_id, created_at DESC) | Home dashboard "my activity" |
| 3 | Activity | (tenant_id, due_date) WHERE status != 'completed' | Task reminders |
| 4 | Contact | (tenant_id, email) | Dedup on create |
| 5 | Deal | (tenant_id, owner_id, stage_id) | Pipeline board per rep |
| 6 | Deal | (tenant_id, close_date) | Forecast queries |
| 7 | AuditEntry | (tenant_id, entity_type, entity_id) | Record audit trail |
| 8 | AuditEntry | (tenant_id, created_at DESC) | Audit log viewer |
| 9 | TimeEntry | (tenant_id, resource_id, date DESC) | Timesheet view |
| 10 | TimeEntry | (engagement_id, status) | Billing runs |
| 11 | Organization | (tenant_id, name) | Search |
| 12 | Lead | (tenant_id, score DESC) | Lead prioritization |
| 13 | Resource | GIN(skill_tags) | Skill search |
| 14 | Subscription | (tenant_id, renewal_date) | Renewal alerts |
| 15 | All entities | (tenant_id, deleted_at) | Soft-delete filtering |

---

## 10. DATA MODEL RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| **Activity table too large** | Partition by month from day 1. Archive > 2 years to cold storage. |
| **custom_fields JSONB slow** | Index GIN on custom_fields for filtered queries. Limit to 100 custom fields per entity. |
| **CRDT sync conflicts on same record** | Last-write-wins for simple fields. CRDT merge for text fields. Conflict UI for simultaneous edits on same field. |
| **Full-text search performance** | Use dedicated search index (Meilisearch/Typesense) synced via CDC, not SQL LIKE queries. |
| **UUID primary key fragmentation** | Use UUID v7 (time-sortable) for primary keys. Avoids B-tree fragmentation. |
| **Soft-delete query overhead** | Add `WHERE deleted_at IS NULL` to all default queries. Create filtered indexes per entity. |
| **Tenant data leakage** | Row-Level Security (RLS) enforced at database level, not just application level. Every query must include tenant_id. |
| **Time entry overlap** | Exclusion constraint on EngagementResource using daterange to prevent double-booking. |

---

## 11. IMPLEMENTATION NOTES

| Concern | Decision |
|---------|----------|
| **Primary keys** | UUID v7 (time-sortable) for all entities |
| **Created/Updated at** | Database triggers on every table |
| **Soft delete** | All entities have deleted_at. Cleanup job archives after 90 days. |
| **custom_fields** | JSONB column. Schema-less. Indexed with GIN. |
| **Tags** | String array column. Indexed with GIN. |
| **Full-text search** | Dedicated search service (Meilisearch/Typesense) synced via CDC from event stream |
| **JSONB fields** | Used for flexible config (settings, layout definitions, workflow conditions). Validate at application layer. |
| **Money** | Always Decimal(15,2) or Decimal(10,2). Never float. |
| **Timestamps** | Always timestamptz (TIMESTAMP WITH TIME ZONE). Store in UTC, display in user timezone. |
| **Enums** | String-based enums in DB (not native PG enum) for backward compatibility with migration. |

---

*Phase 6 complete. 50+ entities defined with all fields, relationships, indexes, and constraints. Next: Phase 7 — All Business Processes.*
