# SOVEREIGN CRM — API REFERENCE

**Document Type:** Technical Specification — API Reference  
**Created:** 2026-06-07  
**Author:** Hermes Agent  
**Base URL:** https://your-domain.com/api  
**Classification:** INTERNAL — NOT FOR GIT PUSH

---

## 1. OVERVIEW

### API Style
- RESTful JSON API
- JWT Bearer token authentication
- Consistent error response format
- Pagination for list endpoints
- Filtering and sorting support

### Authentication
```http
Authorization: Bearer <jwt_token>
```

### Request Headers
```http
Content-Type: application/json
Accept: application/json
X-Request-ID: <uuid> (auto-generated if not provided)
```

### Response Format
```json
{
  "success": true,
  "data": {},
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

### Error Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {}
  }
}
```

---

## 2. AUTHENTICATION ENDPOINTS

### POST /auth/login
**Description:** Authenticate user and get tokens

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "expires_in": 900,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "role": "admin"
    }
  }
}
```

**Rate Limit:** 5 attempts per 15 minutes

### POST /auth/register
**Description:** Register new user

**Request:**
```json
{
  "email": "new@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "tenant_name": "My Company"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "user": {}
  }
}
```

### POST /auth/refresh
**Description:** Refresh access token

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "expires_in": 900
  }
}
```

### POST /auth/logout
**Description:** Blacklist current token (requires auth)

**Headers:** Authorization: Bearer <token>

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### POST /auth/change-password
**Description:** Change password (requires auth)

**Headers:** Authorization: Bearer <token>

**Request:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

### POST /auth/forgot-password
**Description:** Request password reset

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "If the email exists, a reset link has been sent"
}
```

---

## 3. CONTACT ENDPOINTS

### GET /contacts
**Description:** List contacts with filtering and pagination

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20, max: 100)
- `search` (string): Search by name/email
- `status` (string): Filter by status (active, inactive, archived)
- `owner_id` (uuid): Filter by owner
- `organization_id` (uuid): Filter by organization
- `sort` (string): Sort field (created_at, last_name, email)
- `order` (string): Sort order (asc, desc)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "organization": {
        "id": "uuid",
        "name": "Acme Inc"
      },
      "owner": {
        "id": "uuid",
        "first_name": "Jane"
      },
      "tags": ["lead", "enterprise"],
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

### GET /contacts/:id
**Description:** Get contact by ID

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "mobile": "+1234567891",
    "job_title": "CTO",
    "department": "Engineering",
    "address": {
      "line1": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "postal_code": "94105",
      "country": "USA"
    },
    "source": "website",
    "status": "active",
    "lead_score": 85,
    "tags": ["lead", "enterprise"],
    "custom_fields": {},
    "organization": {},
    "owner": {},
    "activities": [],
    "deals": [],
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-01T00:00:00Z"
  }
}
```

### POST /contacts
**Description:** Create new contact

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "organization_id": "uuid",
  "owner_id": "uuid",
  "tags": ["lead"],
  "custom_fields": {}
}
```

### PUT /contacts/:id
**Description:** Update contact

### DELETE /contacts/:id
**Description:** Delete contact (soft delete)

### POST /contacts/bulk
**Description:** Bulk create/update contacts

---

## 4. ORGANIZATION ENDPOINTS

### GET /organizations
**Description:** List organizations

### GET /organizations/:id
**Description:** Get organization with contacts and deals

### POST /organizations
**Description:** Create organization

### PUT /organizations/:id
**Description:** Update organization

### DELETE /organizations/:id
**Description:** Delete organization

---

## 5. DEAL ENDPOINTS

### GET /deals
**Description:** List deals with pipeline filtering

**Query Parameters:**
- `stage` (string): Filter by stage
- `owner_id` (uuid): Filter by owner
- `min_value` (number): Minimum deal value
- `max_value` (number): Maximum deal value
- `expected_close_after` (date): Expected close date filter
- `expected_close_before` (date): Expected close date filter

### GET /deals/:id
**Description:** Get deal with activities and contacts

### POST /deals
**Description:** Create deal

### PUT /deals/:id
**Description:** Update deal (including stage changes)

### PUT /deals/:id/stage
**Description:** Move deal to new stage

**Request:**
```json
{
  "stage": "proposal",
  "notes": "Moved to proposal after discovery call"
}
```

### DELETE /deals/:id
**Description:** Delete deal

---

## 6. ACTIVITY ENDPOINTS

### GET /activities
**Description:** List activities with filtering

**Query Parameters:**
- `type` (string): Filter by type (call, email, meeting, task)
- `contact_id` (uuid): Filter by contact
- `deal_id` (uuid): Filter by deal
- `status` (string): Filter by status (pending, completed)
- `due_before` (date): Due date filter

### POST /activities
**Description:** Create activity

### PUT /activities/:id
**Description:** Update activity

### PUT /activities/:id/complete
**Description:** Mark activity as completed

### DELETE /activities/:id
**Description:** Delete activity

---

## 7. EMAIL TEMPLATE ENDPOINTS

### GET /email-templates
**Description:** List email templates

### GET /email-templates/:id
**Description:** Get template with usage stats

### POST /email-templates
**Description:** Create template

### PUT /email-templates/:id
**Description:** Update template

### DELETE /email-templates/:id
**Description:** Delete template

---

## 8. SEQUENCE ENDPOINTS

### GET /sequences
**Description:** List sequences

### GET /sequences/:id
**Description:** Get sequence with steps and stats

### POST /sequences
**Description:** Create sequence

### PUT /sequences/:id
**Description:** Update sequence

### PUT /sequences/:id/activate
**Description:** Activate sequence

### PUT /sequences/:id/pause
**Description:** Pause sequence

### POST /sequences/:id/enroll
**Description:** Enroll contact in sequence

### DELETE /sequences/:id
**Description:** Delete sequence

---

## 9. WORKFLOW ENDPOINTS

### GET /workflows
**Description:** List workflows

### GET /workflows/:id
**Description:** Get workflow with execution stats

### POST /workflows
**Description:** Create workflow

### PUT /workflows/:id
**Description:** Update workflow

### PUT /workflows/:id/activate
**Description:** Activate workflow

### PUT /workflows/:id/pause
**Description:** Pause workflow

### DELETE /workflows/:id
**Description:** Delete workflow

---

## 10. IMPORT ENDPOINTS

### POST /import/bulk
**Description:** Upload CSV files for import

**Request:** multipart/form-data
- `files[]` (file): CSV files
- `entity_type` (string): contacts, organizations, deals
- `field_mapping` (JSON): Field mapping configuration

### GET /import/progress/:jobId
**Description:** Check import progress

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "processing",
    "total_rows": 100,
    "processed_rows": 50,
    "successful_rows": 45,
    "failed_rows": 5,
    "errors": []
  }
}
```

### GET /import/list
**Description:** List past imports

---

## 11. REPORT ENDPOINTS

### GET /reports/dashboard
**Description:** Get dashboard summary

### GET /reports/pipeline
**Description:** Get pipeline report

### GET /reports/activities
**Description:** Get activity report

### GET /reports/performance
**Description:** Get performance metrics

---

## 12. RATE LIMITS

| Endpoint | Limit | Window |
|----------|-------|--------|
| /auth/login | 5 requests | 15 minutes |
| /auth/register | 3 requests | 1 hour |
| /auth/forgot-password | 3 requests | 1 hour |
| All other endpoints | 100 requests | 1 minute |

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1623456789
```

---

*Document maintained by Hermes Agent. Never push to Git.*  
*Last Updated: 2026-06-07*
