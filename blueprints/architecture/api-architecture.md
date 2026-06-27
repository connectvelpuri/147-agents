# Phase 10: API Architecture, Integrations & Connectors

**Created:** 2026-06-06
**Purpose:** Complete API surface, integration framework, connector architecture — from REST to GraphQL to Webhooks to legacy bridge.

---

## 0. PHILOSOPHY: API-FIRST

Every UI action calls the same API an integrator would. No internal shortcuts. This means:
- API is always at parity with UI (same features, same permissions)
- API is versioned from day 1
- API is self-documenting (OpenAPI 3.1)
- Rate limits can be disabled on self-hosted

---

## 1. API STACK OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENTS                                    │
│   Web App  │  Mobile App  │  MCP Client  │  External Systems         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                    API GATEWAY (Kong / Envoy)                       │
│  Auth (JWT/SAML/OAuth2)  │  Rate Limiting  │  Logging  │  CORS     │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                    API LAYER (Go/Next.js API Routes)                 │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  REST API  │  │GraphQL API │  │ WebSocket  │  │ Streaming  │   │
│  │  (Primary) │  │ (Complex   │  │ (Real-time │  │ (Events,   │   │
│  │            │  │  queries)  │  │  sync)     │  │  CDC)      │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Service Layer: Auth / CRM / Workflow / AI / Admin / Export │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                    INTEGRATION GATEWAY                               │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Webhooks   │  │ Connectors │  │ Legacy     │  │ ETL Engine │   │
│  │ Outbound   │  │ (Stripe,   │  │ Bridge     │  │ (Data sync)│   │
│  │ + Inbound  │  │  Gmail...) │  │ (SOAP,     │  │            │   │
│  │            │  │            │  │  Flat File) │  │            │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────┐
│                  EVENT BUS / CDC (Change Data Capture)               │
│                    (Kafka / Redpanda / NATS)                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. REST API SPECIFICATION

### Base URL
```
https://{instance}/api/v1/
```

### Authentication
```
Authorization: Bearer <jwt_token>
X-Tenant-ID: <tenant_uuid>  // Required for all requests
```

### Standard Response Envelope
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 50,
    "total": 1234,
    "total_pages": 25
  },
  "error": null
}
```

### Error Response
```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      {"field": "email", "message": "cannot be blank", "code": "REQUIRED"}
    ],
    "request_id": "req_abc123"
  }
}
```

### Versioning
- URL-based: `/api/v1/`, `/api/v2/`
- Deprecation: header `Sunset: Sat, 01 Jan 2028 00:00:00 GMT`
- Minimum support: 2 versions back, 12 months

---

## 3. ENDPOINT CATALOG

### Core CRM Endpoints

| Method | Endpoint | Description | MVP? |
|--------|----------|-------------|:----:|
| GET | /contacts | List contacts (paginated, filtered, sorted) | YES |
| POST | /contacts | Create contact | YES |
| GET | /contacts/{id} | Get contact detail | YES |
| PATCH | /contacts/{id} | Update contact fields | YES |
| DELETE | /contacts/{id} | Soft-delete contact | YES |
| GET | /contacts/{id}/activities | Contact's activity timeline | YES |
| POST | /contacts/batch | Batch create/update (up to 100) | S3 |
| GET | /contacts/search | Full-text search contacts | YES |
| POST | /contacts/{id}/merge | Merge with another contact | S3 |
| POST | /contacts/import | CSV import job | S2 |

(Same pattern for: /organizations, /leads, /deals, /activities, /notes, /products)

### Pipeline & Sales Endpoints

| Method | Endpoint | Description | MVP? |
|--------|----------|-------------|:----:|
| GET | /pipelines | List pipelines | YES |
| GET | /pipelines/{id}/stages | Stage definitions | YES |
| PATCH | /deals/{id}/stage | Move deal to stage (with validation) | YES |
| POST | /deals/{id}/products | Add product to deal | YES |
| GET | /forecasts | Get forecast rollup | S3 |
| GET | /forecasts/reps/{id} | Per-rep forecast | S3 |

### Admin Endpoints

| Method | Endpoint | Description | Sprint |
|--------|----------|-------------|:------:|
| GET | /metadata/entities | List all entities (system+custom) | S2 |
| GET | /metadata/entities/{api_name}/fields | Entity fields definition | S2 |
| POST | /metadata/entities | Create custom entity | S2 |
| POST | /metadata/fields | Create custom field | S2 |
| GET | /workflows | List workflow rules | S3 |
| POST | /workflows | Create workflow | S3 |
| GET | /users | List users | YES |
| POST | /users | Create user | YES |
| GET | /audit-logs | Query audit trail | S2 |
| GET | /imports/{id}/status | Check import job status | S2 |

### IT Consulting Endpoints

| Method | Endpoint | Sprint |
|--------|----------|:------:|
| GET / POST / PATCH | /engagements | S5 |
| GET / POST / PATCH | /sows | S5 |
| GET / POST / PATCH | /time-entries | S5 |
| POST | /time-entries/batch | S5 (weekly timesheet) |
| GET / POST / PATCH | /resources | S5 |
| GET / POST / PATCH | /expenses | S5 |
| GET | /engagements/{id}/p&l | S5 |

### SaaS Endpoints

| Method | Endpoint | Sprint |
|--------|----------|:------:|
| GET / POST / PATCH | /subscriptions | S5 |
| GET / POST / PATCH | /invoices | S5 |
| POST | /product-usage/batch | S5 (usage data ingestion) |
| GET | /subscriptions/{id}/health | S5 |
| GET | /mrr | S5 |

### AI/MCP Endpoints

| Method | Endpoint | Sprint |
|--------|----------|:------:|
| POST | /ai/query | NL query → response | S4 |
| POST | /ai/action | NL action → execute | S4 |
| GET | /ai/insights/deals | AI deal insights | S4 |
| GET | /ai/insights/pipeline | AI pipeline insights | S4 |
| POST | /ai/agent/run | Run autonomous agent | S6 |

---

## 4. GRAPHQL API

### Use Case: Complex Queries for Reporting & Analytics

```graphql
query {
  deals(
    filter: { stage: "negotiation", amount_gte: 50000 }
    sort: { field: "created_at", order: DESC }
  ) {
    id
    name
    amount
    stage {
      name
    }
    owner {
      id
      first_name
      last_name
    }
    contact {
      id
      email
    }
    activities(limit: 5) {
      type
      subject
      created_at
    }
  }
}
```

### Mutations
```graphql
mutation {
  createContact(input: {
    first_name: "John"
    last_name: "Doe"
    email: "john@acme.com"
    organization_id: "org_uuid"
  }) {
    id
    name
    email
  }
}
```

---

## 5. WEBHOOK SYSTEM

### Event Catalog (Outbound)

| Event | Payload Description | Priority |
|-------|-------------------|:--------:|
| contact.created | Full contact record | HIGH |
| contact.updated | Changed fields only | HIGH |
| contact.deleted | ID + timestamp | MEDIUM |
| deal.created | Full deal record | HIGH |
| deal.stage_changed | Deal ID, old stage, new stage | HIGH |
| deal.won | Deal ID, amount, close date | CRITICAL |
| deal.lost | Deal ID, reason, competitor | HIGH |
| activity.created | Activity record | MEDIUM |
| time_entry.submitted | Time entry for sync | HIGH (ITC) |
| invoice.paid | Invoice record | HIGH (SaaS) |
| subscription.churned | Subscription + reason | CRITICAL (SaaS) |

### Webhook Delivery Contract
```json
POST https://example.com/webhook
Headers:
  Content-Type: application/json
  X-Sovereign-Signature: sha256=HMAC(timestamp.body.secret)
  X-Sovereign-Timestamp: 1700000000
  X-Sovereign-Event: deal.won

Body:
{
  "event": "deal.won",
  "event_id": "evt_abc123",
  "created_at": "2026-06-06T12:00:00Z",
  "tenant_id": "tenant_uuid",
  "data": { /* full or partial record */ }
}
```

### Inbound Webhooks
- Receive POST from external systems
- Register via API: POST /api/v1/webhooks/inbound
- Payload mapped to CRM entities via config
- Source verification via signature header

---

## 6. CONNECTOR ARCHITECTURE

### Connector Framework

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        CONNECTOR INTERFACE                                 │
│                                                                             │
│  authenticate() → token                                                      │
│  fetch_entities(entity_type, since) → records[]                             │
│  push_entity(entity_type, records[]) → results[]                           │
│  webhook_subscribe(events) → subscription_id                               │
│  health_check() → status                                                   │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

### Pre-Built Connectors (Priority Order)

| # | Connector | Direction | Type | Sprint | Priority |
|:-:|-----------|:--------:|:----:|:-----:|:--------:|
| 1 | Gmail | Bidirectional | OAuth + API | S3 | CRITICAL |
| 2 | Outlook/365 | Bidirectional | Graph API | S3 | CRITICAL |
| 3 | Google Calendar | Bidirectional | OAuth + API | S3 | CRITICAL |
| 4 | Outlook Calendar | Bidirectional | Graph API | S3 | CRITICAL |
| 5 | Twilio (Voice/SMS) | Inbound → CRM | Webhook | S3 | HIGH |
| 6 | Stripe | Stripe → CRM | Webhook | S6 | HIGH (SaaS) |
| 7 | DocuSign | Bidirectional | API | S6 | HIGH |
| 8 | Slack | Bidirectional | Webhook + API | S6 | MEDIUM |
| 9 | Salesforce (Import) | One-time | REST API | S6 | HIGH |
| 10 | HubSpot (Import) | One-time | REST API | S6 | HIGH |
| 11 | Zapier | Outbound | Webhook | S3 | HIGH |
| 12 | Jira | Bidirectional | REST API | S6 | HIGH (ITC) |
| 13 | QuickBooks | Accounting → CRM | OAuth | S6 | MEDIUM |
| 14 | Xero | Accounting → CRM | OAuth | S6 | MEDIUM |
| 15 | LDAP / SAML/SSO | Identity | SAML/OIDC | S3 | HIGH |
| 16 | Zoom/Teams | Meeting → CRM | API | S6 | MEDIUM |

### Connector Implementation Pattern (Example: Gmail)

```
1. User OAuth: browser → Gmail consent → callback → store refresh token (encrypted)
2. Background sync: poll Gmail API every 5 min for new emails
3. Email matched to Contact by: from/to address match
4. Auto-create Activity attached to Contact
5. Email tracking: open pixel, link rewrite → track opens/clicks
6. Reply detection: thread matching → auto-pause sequence
```

---

## 7. LEGACY BRIDGE ARCHITECTURE

### Problem
IT Consulting firms run on legacy systems: SAP, Oracle ERP, home-grown CRMs, flat-file exports from ERPs. They need integration without replacing legacy.

### Bridge Strategy

```
┌──────────┐    ┌──────────────────────────────────┐    ┌──────────┐
│ Legacy   │    │        BRIDGE SERVICE             │    │  CRM     │
│ System   │◄──►│                                  │◄──►│          │
│          │    │ • SOAP/XML adapter               │    │          │
│ SAP/Oracle│   │ • Flat file parser (CSV, EDI)    │    │  REST    │
│          │    │ • Scheduled batch sync            │    │  API     │
│ Homegrown│    │ • Idempotent (no duplicates)      │    │          │
│ CRM      │    │ • Error queue + retry             │    │          │
│          │    │ • Mapping transform engine         │    │          │
└──────────┘    └──────────────────────────────────┘    └──────────┘
```

### Legacy Data Mapping Engine

Each mapping definition:
```json
{
  "name": "SAP Customer Import",
  "source_type": "flat_file",
  "source_format": "CSV",
  "schedule": "0 2 * * *",
  "mappings": [
    {"source": "KUNNR", "target": "Organization.External_ID__c", "transform": "trim"},
    {"source": "NAME1", "target": "Organization.Name"},
    {"source": "ORT01", "target": "Organization.Billing_City__c"},
    {"source": "PSTLZ", "target": "Organization.Billing_Zip__c"}
  ],
  "dedup_field": "Organization.External_ID__c",
  "error_handling": "skip_and_log"
}
```

---

## 8. API SECURITY & GOVERNANCE

| Concern | Implementation |
|---------|---------------|
| Authentication | JWT with RS256. Token lifetime: 15 min access, 7 day refresh. |
| Authorization | Permission check on EVERY endpoint (same as UI). |
| Rate Limiting | 1000 req/min per user (configurable). Disabled on self-hosted enterprise. |
| CORS | Configurable origin whitelist per tenant. |
| API Keys | For server-to-server. Scoped to specific endpoints. Rotatable. |
| Logging | Every API call logged to audit. Body logged for mutating calls. |
| IP Whitelist | Optional: restrict API access to known IP ranges. |
| Request Validation | OpenAPI spec validation on every request. |

---

## 9. EVENT BUS / CDC (Change Data Capture)

### Why CDC
- Real-time sync to search index (Meilisearch)
- Real-time sync to analytics (ClickHouse)
- Webhook delivery without polling
- CRDT sync for local-first clients
- Audit log streaming

### Architecture
```
Postgres WAL → Debezium → Kafka/Redpanda → Consumers
                                               │
                                 ┌─────────────┼─────────────┐
                                 ▼             ▼             ▼
                           Search Index   Webhook       Analytics
                           (Meilisearch)  Delivery      (Clickhouse)
```

### Event Schema
```json
{
  "schema": "com.sovereign.crm.v1.deal.updated",
  "payload": {
    "before": {"stage_id": "old_stage", "amount": 50000},
    "after": {"stage_id": "new_stage", "amount": 55000},
    "source": {
      "tenant_id": "tenant_uuid",
      "user_id": "user_uuid",
      "ip_address": "1.2.3.4"
    },
    "op": "u",
    "ts_ms": 1700000000000
  }
}
```

---

*Phase 10 complete. Full API architecture with REST, GraphQL, Webhooks, Connectors, Legacy Bridge, and Event Bus. Next: Phase 11 — AI & Agent Architecture.*
