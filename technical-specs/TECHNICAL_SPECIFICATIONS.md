# SOVEREIGN CRM — TECHNICAL SPECIFICATIONS

**Document Type:** Technical Specification  
**Created:** 2026-06-07  
**Author:** Hermes Agent  
**Classification:** INTERNAL — NOT FOR GIT PUSH

---

## 1. SYSTEM ARCHITECTURE

### 1.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTS                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Web App   │  │  Mobile App │  │   CLI Tool  │        │
│  │  (Next.js)  │  │   (Future)  │  │   (Future)  │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
└─────────┼────────────────┼────────────────┼─────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                     REVERSE PROXY                          │
│                    (Caddy + SSL)                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
┌─────────────────┐             ┌─────────────────┐
│    Next.js      │             │     Go API      │
│   (Port 3000)   │             │   (Port 8080)   │
│   SSR + API     │             │  REST + CRDT    │
└─────────────────┘             └────────┬────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │   PostgreSQL    │  │      Redis      │  │     Ollama      │
          │  (Port 5432)    │  │  (Port 6379)    │  │ (Port 11434)    │
          │   Primary DB    │  │  Cache/Sessions  │  │   AI Engine     │
          └─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 1.2 Component Responsibilities

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Web App** | UI rendering, client-side logic | Next.js 14, TypeScript |
| **Go API** | Business logic, data access | Go 1.22, chi router |
| **PostgreSQL** | Persistent storage, ACID, RLS | PostgreSQL 16 |
| **Redis** | Caching, sessions, pub/sub | Redis 7 |
| **Ollama** | AI-powered features | Ollama, LLM models |
| **Caddy** | SSL termination, static files | Caddy 2 |

---

## 2. TECHNOLOGY STACK

### 2.1 Backend (Go API)

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Language | Go | 1.22 | Performance, deployment simplicity |
| Router | chi | 5.0.12 | Lightweight, idiomatic Go |
| Database | pgx | 5.5.5 | PostgreSQL native driver |
| Cache | go-redis | 9.5.1 | Redis client |
| Auth | golang-jwt | 5.2.1 | JWT handling |
| Crypto | golang.org/x/crypto | 0.21.0 | bcrypt, password hashing |
| Logging | zerolog | 1.32.0 | Structured logging |
| UUID | google/uuid | 1.6.0 | UUID generation |
| CRDT | ygo | latest | Go Yjs implementation |

### 2.2 Frontend (Next.js)

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Framework | Next.js | 14.x | React ecosystem, SSR |
| Language | TypeScript | 5.x | Type safety |
| Styling | Tailwind CSS | 3.x | Utility-first CSS |
| State | React Query | 5.x | Server state management |
| Forms | React Hook Form | 7.x | Form validation |
| CRDT | Yjs | latest | CRDT implementation |

### 2.3 Infrastructure

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Database | PostgreSQL | 16 | ACID, RLS, JSONB |
| Cache | Redis | 7 | Performance, sessions |
| Container | Podman | 4+ | Daemonless, rootless |
| Reverse Proxy | Caddy | 2.x | Auto-SSL, simple config |
| AI | Ollama | latest | Local LLM inference |

---

## 3. API DESIGN

### 3.1 RESTful Conventions
- **Resources:** Noun-based URLs (/contacts, /deals)
- **HTTP Methods:** GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes:** 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)
- **Pagination:** Page-based with meta object
- **Filtering:** Query parameters
- **Sorting:** Sort and order parameters

### 3.2 Authentication Flow
```
1. User submits credentials to /auth/login
2. Server validates credentials against database
3. Server generates JWT access token (15 min expiry)
4. Server generates refresh token (7 day expiry)
5. Server stores refresh token in Redis
6. Server returns both tokens to client
7. Client includes access token in Authorization header
8. Server validates token on each request
9. Client refreshes access token using refresh token
10. Server blacklists token on logout
```

### 3.3 Multi-Tenancy Flow
```
1. Request arrives with JWT token
2. Auth middleware validates token
3. Tenant context middleware extracts tenant_id from JWT
4. Middleware executes: SET LOCAL app.current_tenant_id = ?
5. All subsequent queries automatically filtered by RLS
6. Response only includes tenant's data
```

---

## 4. DATA ACCESS PATTERNS

### 4.1 Repository Pattern
```go
// Example: Contact Repository
type ContactRepository interface {
    Create(ctx context.Context, contact *Contact) error
    GetByID(ctx context.Context, id uuid.UUID) (*Contact, error)
    List(ctx context.Context, opts ListOptions) ([]Contact, int, error)
    Update(ctx context.Context, contact *Contact) error
    Delete(ctx context.Context, id uuid.UUID) error
}
```

### 4.2 Query Building
```go
// Parameterized queries prevent SQL injection
query := `
    SELECT id, first_name, last_name, email
    FROM contacts
    WHERE tenant_id = $1
    AND ($2 = '' OR first_name ILIKE '%' || $2 || '%')
    ORDER BY created_at DESC
    LIMIT $3 OFFSET $4
`
rows, err := db.Query(ctx, query, tenantID, search, limit, offset)
```

### 4.3 Transaction Management
```go
// Database transactions for data consistency
tx, err := db.Begin(ctx)
defer tx.Rollback(ctx)

// Perform multiple operations
err = tx.Exec(ctx, "INSERT INTO contacts ...", ...)
err = tx.Exec(ctx, "INSERT INTO activities ...", ...)

// Commit on success
err = tx.Commit(ctx)
```

---

## 5. SECURITY ARCHITECTURE

### 5.1 Authentication Security
- **Password Hashing:** bcrypt with cost factor 12
- **JWT Signing:** HS256 with configurable secret
- **Token Expiry:** Access (15 min), Refresh (7 days)
- **Token Blacklisting:** Redis-based for instant revocation
- **Rate Limiting:** 5 login attempts per 15 minutes

### 5.2 Authorization Security
- **Role-Based Access Control:** Admin, Manager, Rep, Read-Only
- **Endpoint Protection:** Middleware checks role on each route
- **Resource Ownership:** Users can only modify own resources (unless admin)

### 5.3 Data Security
- **Encryption at Rest:** PostgreSQL transparent encryption (optional)
- **Encryption in Transit:** TLS 1.2+ via Caddy
- **Input Validation:** Server-side validation on all inputs
- **Output Encoding:** HTML encoding for user content
- **SQL Injection Prevention:** Parameterized queries only

### 5.4 Network Security
- **CORS:** Restricted to known origins
- **Security Headers:** CSP, HSTS, X-Frame-Options
- **Rate Limiting:** Global and per-endpoint
- **Request IDs:** Unique ID for tracing

---

## 6. PERFORMANCE SPECIFICATIONS

### 6.1 Response Time Targets
| Metric | Target | Maximum |
|--------|--------|---------|
| API p50 | <50ms | <100ms |
| API p95 | <200ms | <500ms |
| API p99 | <500ms | <1000ms |
| Page Load | <2s | <5s |
| Time to Interactive | <3s | <7s |

### 6.2 Throughput Targets
| Metric | Target |
|--------|--------|
| Concurrent Users | 1000 |
| Requests per Second | 500 |
| Database Connections | 200 |
| WebSocket Connections | 1000 |

### 6.3 Resource Limits
| Resource | Container Limit |
|----------|----------------|
| API CPU | 1 core |
| API Memory | 512MB |
| Web CPU | 0.5 core |
| Web Memory | 256MB |
| PostgreSQL CPU | 2 cores |
| PostgreSQL Memory | 2GB |
| Redis CPU | 0.5 core |
| Redis Memory | 1GB |

---

## 7. DEPLOYMENT SPECIFICATIONS

### 7.1 Container Images
```dockerfile
# API Container (Multi-stage)
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main ./cmd/server

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

### 7.2 Environment Variables
```bash
# Database
DATABASE_URL=postgres://user:pass@localhost:5432/sovereign

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key

# Application
APP_ENV=production
APP_URL=https://your-domain.com
LOG_LEVEL=info
```

### 7.3 Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## 8. MONITORING SPECIFICATIONS

### 8.1 Metrics to Collect
- Request count and latency
- Error rate by endpoint
- Database connection pool usage
- Redis memory usage
- Container CPU/Memory usage
- Active WebSocket connections

### 8.2 Logging Standards
```json
{
  "timestamp": "2026-06-07T12:00:00Z",
  "level": "info",
  "message": "Request processed",
  "request_id": "uuid",
  "user_id": "uuid",
  "tenant_id": "uuid",
  "method": "GET",
  "path": "/api/contacts",
  "status": 200,
  "duration_ms": 45
}
```

### 8.3 Alerting Rules
| Alert | Condition | Severity |
|-------|-----------|----------|
| High Error Rate | >5% errors in 5 min | Critical |
| High Latency | p95 >500ms for 5 min | Warning |
| Database Down | Connection refused | Critical |
| Memory High | >80% usage | Warning |
| Disk High | >85% usage | Warning |

---

## 9. TESTING SPECIFICATIONS

### 9.1 Test Types
| Type | Coverage Target | Tools |
|------|-----------------|-------|
| Unit Tests | >80% | Go testing, Jest |
| Integration Tests | All endpoints | Go testing |
| E2E Tests | Critical flows | Playwright |
| Load Tests | 1000 users | k6, vegeta |
| Security Tests | OWASP Top 10 | Manual + automated |

### 9.2 Test Data Management
- Seed scripts for demo data
- Test isolation per test run
- Cleanup after tests
- Mock external services

---

## 10. SCALABILITY SPECIFICATIONS

### 10.1 Horizontal Scaling
- API: Stateless, can run multiple instances
- Web: Stateless, can run multiple instances
- PostgreSQL: Read replicas for scaling reads
- Redis: Cluster mode for scaling

### 10.2 Vertical Scaling
- PostgreSQL: Increase RAM for larger datasets
- Redis: Increase memory for more sessions
- API: Increase CPU for more concurrent requests

### 10.3 Data Limits
| Entity | Expected Volume | Growth Rate |
|--------|-----------------|-------------|
| Contacts | 100K per tenant | 10%/month |
| Organizations | 10K per tenant | 5%/month |
| Deals | 50K per tenant | 15%/month |
| Activities | 500K per tenant | 20%/month |

---

*Document maintained by Hermes Agent. Never push to Git.*  
*Last Updated: 2026-06-07*
