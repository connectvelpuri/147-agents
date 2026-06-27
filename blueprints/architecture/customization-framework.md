# Phase 8: Customization Framework (Dynamic Object Builder)

**Created:** 2026-06-06
**Purpose:** How admins extend the CRM without code. The metadata engine, dynamic entity system, and customization UX.

---

## 1. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  Dynamic UI Renderer  │  Dynamic API  │  Workflow Engine    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  METADATA ENGINE LAYER                       │
│                                                             │
│  Entity Registry  │  Field Registry  │  Layout Registry    │
│  Relationship Map │  Validation Engine │  Formula Engine    │
│                                                             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  PHYSICAL DATA LAYER                         │
│                                                             │
│  System Tables (User, Tenant, Role...)                      │
│  Dynamic Tables (created at runtime per entity)             │
│  JSONB Fallback (for entities < 100k records)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Two Modes:**
- **JSONB Mode (default):** Custom entities stored as records in `custom_entity_data` table with JSONB payload. Good for <100k records, zero schema changes at runtime.
- **Dynamic Table Mode (advanced):** Physical PostgreSQL table created per entity type. Better performance for >100k records. Requires schema migration.

---

## 2. CUSTOM ENTITY LIFECYCLE

### Step 1: Define Entity Type
Admin navigates: Admin → Entity Manager → + New Entity

Input:
- Label: "Engagement" → API Name: "Engagement__c"
- Plural: "Engagements"
- Description: "IT Consulting project engagement"
- Features: Enable Activities? Yes. Enable Notes? Yes. Enable Pipeline? No.

System creates:
- `CustomEntityDefinition` record
- If Dynamic Table Mode: `CREATE TABLE "Engagement__c" (...)` with system fields
- If JSONB Mode: nothing beyond the metadata record

### Step 2: Define Fields
Admin adds fields one by one:

| Step | Admin Input | System Action |
|------|-------------|---------------|
| 2a | Field Label: "Client Name" → Type: "Lookup" → Target: "Organization" | Creates CustomFieldDefinition with lookup_entity_id |
| 2b | Field Label: "Start Date" → Type: "Date" → Required: Yes | Creates date field with required constraint |
| 2c | Field Label: "Engagement Type" → Type: "Picklist" → Values: Fixed Bid, T&M | Creates picklist field with values |

### Step 3: Define Layout
Admin drags fields onto a page layout canvas:
- Left column: Client Name, Start Date, End Date
- Right column: Engagement Type, Status, Budget
- Section: "Financial" → Budget Amount, Currency, PO Number

### Step 4: Define Relationships
Admin links entities:
- "Engagement has many TimeEntry" → creates reverse lookup
- "Engagement belongs to Organization" → creates lookup field

System creates relationship metadata:
```
{
  "source_entity": "Engagement__c",
  "target_entity": "Organization",
  "type": "many_to_one",
  "field_name": "Client_Name__c"
}
```

### Step 5: Deploy
Admin clicks "Deploy". System:
1. Validates all field definitions, relationships, layouts
2. If Dynamic Table Mode: generates and runs `ALTER TABLE` / `CREATE TABLE`
3. If JSONB Mode: no schema change needed
4. Clears any metadata cache
5. Logs the deployment to audit

---

## 3. FIELD TYPE CATALOG

| # | Type | Storage | Config Options | Indexable |
|:-:|------|---------|----------------|:---------:|
| 1 | Text | VARCHAR(255) | max_length, default, unique | YES |
| 2 | TextArea | TEXT | max_length | NO (fulltext) |
| 3 | Rich Text | TEXT | — | NO |
| 4 | Number | DECIMAL | precision(0-10), scale(0-4), min, max | YES |
| 5 | Currency | DECIMAL(15,2) | currency_code | YES |
| 6 | Date | DATE | min, max | YES |
| 7 | DateTime | TIMESTAMPTZ | min, max | YES |
| 8 | Boolean | BOOLEAN | default | YES |
| 9 | Picklist | VARCHAR(100) | values[], multi_select, default | YES |
| 10 | MultiPicklist | TEXT | values[], separator | YES (GIN) |
| 11 | Lookup | UUID | target_entity, relationship_name | YES |
| 12 | Master-Detail | UUID | target_entity, cascade_delete | YES |
| 13 | Formula | COMPUTED | expression, return_type | NO |
| 14 | Auto-Number | VARCHAR(50) | prefix, start_number, min_digits | YES |
| 15 | Email | VARCHAR(255) | — | YES |
| 16 | Phone | VARCHAR(50) | — | YES |
| 17 | URL | VARCHAR(500) | — | YES |
| 18 | Address | JSONB | structured fields | NO |
| 19 | File | VARCHAR(500) | allowed_extensions, max_size | NO |
| 20 | Image | VARCHAR(500) | allowed_extensions, max_size | NO |
| 21 | JSON | JSONB | schema_validation schema | YES (GIN) |
| 22 | Geolocation | JSONB | lat, lng | YES (GIST) |

---

## 4. VALIDATION RULES

### Formula-Based Validation
```
Expression: AND(
  NOT(ISBLANK(Close_Date__c)),
  Close_Date__c < TODAY()
)
Error Message: "Close date must be in the future"
Trigger: before_save
```

### System Validations (auto-generated)
- Required field check
- Unique field check
- Picklist value membership
- Lookup existence check
- Data type format check
- Max length check

### Cross-Field Validations
```
Rule: "If Engagement Type = Fixed Bid AND Budget Amount > 1000000"
Action: "Require approval before save"
```

---

## 5. FORMULA ENGINE

### Supported Functions

| Category | Functions |
|----------|-----------|
| Math | ABS, ROUND, FLOOR, CEILING, MAX, MIN, SUM, AVG, MOD, EXP, LOG, SQRT, POW |
| Text | CONCATENATE, LEFT, RIGHT, MID, LEN, TRIM, LOWER, UPPER, PROPER, CONTAINS, BEGINSWITH, ENDSWITH, FIND, REPLACE, SUBSTITUTE, TEXT, VALUE, ISBLANK, NULLVALUE |
| Date | TODAY, NOW, DATE, YEAR, MONTH, DAY, HOUR, MINUTE, ADDDAYS, ADDMONTHS, ADDYEARS, DATE_DIFF, DAY_OF_YEAR, WEEKDAY, MONTH_NAME |
| Logical | IF, AND, OR, NOT, CASE, ISBLANK, ISNUMBER, ISTEXT, ISDATE, NULLVALUE |
| Aggregate | COUNT, COUNT_DISTINCT, SUM_UP, MIN_UP, MAX_UP, AVG_UP (for related records) |
| Cross-Object | LOOKUP(entity_id, field_name): "Get related value from lookup target" |
| Currency | CURRENCY_RATE(from, to, date): "Convert between currencies" |
| Special | HYPERLINK(url, label), IMAGE(url, alt) |

### Formula Examples
```
// Field: Discount Percent
IF(Amount__c > 100000, 0.15, IF(Amount__c > 50000, 0.10, 0.05))

// Field: Project Margin %
((Total_Billed__c - Total_Cost__c) / Total_Billed__c) * 100

// Field: Health Status
IF(Health_Score__c >= 80, "Green", IF(Health_Score__c >= 50, "Yellow", "Red"))

// Field: Account Executive Commission (cross-object)
LOOKUP(Owner__r, Commission_Rate__c) * Deal_Amount__c

// Rollup: Total Hours on Engagement (for parent)
SUM_UP(TimeEntry__c, Hours__c, EngagementId__c = Id)
```

---

## 6. LAYOUT ENGINE

### Page Layout Definition (JSON)
```json
{
  "columns": 2,
  "sections": [
    {
      "id": "sec1",
      "label": "General Information",
      "collapsible": false,
      "columns": 2,
      "fields": [
        {"api_name": "Name__c", "row": 0, "col": 0, "width": 1},
        {"api_name": "Client_Name__c", "row": 0, "col": 1, "width": 1},
        {"api_name": "Start_Date__c", "row": 1, "col": 0, "width": 1},
        {"api_name": "End_Date__c", "row": 1, "col": 1, "width": 1}
      ]
    },
    {
      "id": "sec2",
      "label": "Financial",
      "collapsible": true,
      "columns": 2,
      "fields": [
        {"api_name": "Budget_Amount__c", "row": 0, "col": 0, "width": 1},
        {"api_name": "Currency__c", "row": 0, "col": 1, "width": 1}
      ]
    }
  ],
  "related_lists": [
    {"entity": "TimeEntry__c", "label": "Time Entries", "fields": ["Date__c", "Hours__c", "Type__c"]},
    {"entity": "Expense__c", "label": "Expenses", "fields": ["Date__c", "Amount__c", "Category__c"]}
  ]
}
```

### Compact Layout (Kanban Card)
```json
{
  "fields": ["Name__c", "Client_Name__c", "Budget_Amount__c", "Status__c"],
  "color_field": "Status__c",
  "icon": "briefcase"
}
```

---

## 7. WORKFLOW BUILDER

### Visual Flow Editor (drag-and-drop)

```
[Nodes Palette]
  Trigger: When record is created/updated/deleted
  Condition: IF this field = value / formula true
  Action: Update field / Create record / Send email / Call webhook
  Approval: Submit for approval
  Loop: For each related record... (future)
  Timer: Wait X hours/days
  Branch: AND / OR split
```

### Example: "Welcome Email on New Lead"

```
TRIGGER: Lead created
  │
  ├── CONDITION: Lead.Source = "Website Form"
  │      │
  │      ├── ACTION: Send Email → Template "Welcome" to Lead.Email
  │      │
  │      ├── ACTION: Create Task → "Call within 24h" assigned to Lead.Owner
  │      │
  │      └── ACTION: Wait 24 hours
  │             │
  │             └── CONDITION: Lead.Status != "Contacted"
  │                    │
  │                    └── ACTION: Send Email → Alert to Lead.Owner.Manager
  │
  └── DEFAULT: No action (if source != "Website Form")
```

---

## 8. METADATA CACHE STRATEGY

| Concern | Strategy |
|---------|----------|
| Metadata read frequency | Every page load, every API call |
| Metadata change frequency | Rare (admin operations only) |
| Cache layer | In-memory (Redis or app local) with 5-minute TTL |
| Invalidation | On metadata change → publish cache invalidation event |
| Versioning | Metadata version number per tenant. Client sends version, server diffs. |
| Cold start | On first request, load all metadata for tenant. ~50ms for 100 entities. |

---

## 9. CUSTOMIZATION LIMITS (Safeguards)

| Resource | Free | Starter | Professional | Enterprise |
|----------|:----:|:-------:|:------------:|:----------:|
| Custom entities | 5 | 20 | 50 | Unlimited |
| Fields per entity | 50 | 100 | 200 | 500 |
| Workflow rules | 10 | 50 | 200 | Unlimited |
| Approval processes | 5 | 20 | 50 | Unlimited |
| Formula fields | 10 | 25 | 100 | 500 |
| Page layouts | 3 | 10 | 25 | Unlimited |
| Reports | 20 | 100 | 500 | Unlimited |
| Dashboards | 5 | 20 | 50 | 200 |
| Saved searches | 20 | 50 | 200 | Unlimited |

---

*Phase 8 complete. Customization Framework defines how admins extend the CRM without code. Next: Phase 9 — Customer & Buyer Journeys.*
