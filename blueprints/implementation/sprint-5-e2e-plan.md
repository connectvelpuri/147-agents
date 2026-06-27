# Sprint 5 — Complete End-to-End Execution Plan

**Date:** 2026-06-07
**Author:** Hermes Agent (16-Persona Audit)
**Status:** AWAITING APPROVAL
**Theme:** "Deploy, Validate, Foundation, Then Build"
**Duration:** 3 weeks / 15 working days / 39 hours

---

## EXECUTIVE SUMMARY

Sprint 5 is NOT a feature sprint. It is a VALIDATION and FOUNDATION sprint.

We have 33 Go files, 58 TypeScript files, 23 frontend pages, 28 database tables,
and zero runtime verification. The API has never started successfully. The frontend
has suppressed type errors. No tests exist. No deployment exists. No user has ever
touched this product.

Sprint 5 fixes this. By the end, we will have:
1. A running, tested API server
2. A live deployment accessible via URL
3. Feedback from real humans
4. Integration tests protecting against regressions
5. The foundation of our actual moats (CRDT + Dynamic Objects)
6. Documentation enabling others to use and contribute

---

## METHODOLOGY

Every workstream in this plan has been validated through:

1. **Constitution Article I (10 Questions)** — Why does this exist? What problem?
2. **Big 4 Audit** — Strategic, product, technical quality assessment
3. **Persona Challenge** — Would a sales rep, CRO, admin actually use this?
4. **Architecture Review** — Does this scale? Is it maintainable?
5. **Risk Assessment** — What could go wrong? Mitigations?
6. **Capacity Validation** — Can a solo dev actually ship this in 3 weeks?

---

## CURRENT STATE AUDIT

### What Exists (Code):
| Layer | Files | Status |
|-------|:-----:|--------|
| Go API | 33 files | Builds but cannot start (DB auth failure) |
| Next.js Frontend | 58 files / 23 pages | Builds with suppressed type errors |
| Database | 28 tables | Schema exists, migrations applied |
| Tests | 2 scaffold files | Non-functional |
| Documentation | 0 files | Nothing exists |
| Deployment | 0 configs | No Docker, no CI/CD |

### What Does NOT Exist:
| Capability | Impact |
|-----------|--------|
| Runtime verification | Cannot confirm any feature works |
| User feedback | Building blind |
| CRDT sync | Our #1 moat is unimplemented |
| Dynamic Objects | Our #3 moat is unimplemented |
| Integration tests | Every change is a regression risk |
| Documentation | Nobody can use or contribute |
| Deployment | Product is invisible to the world |
| Monitoring | Silent failures in production |

---

## WEEK 1: MAKE IT WORK (Days 1-5)

**Goal:** Every endpoint works. Every page renders. The product is testable.

---

### Day 1: Critical Fixes (6h)

#### Task 1.1: Fix Database Connection [2h] P0

**Why:** The API server cannot start. This blocks ALL subsequent work.

**Constitution Check:**
- Q1: Why? Because the DSN password in db.go doesn't match the PostgreSQL user.
- Q7: Simplest version? Change one string. Test connection.

**Implementation:**
1. Read current DSN in `api/internal/database/db.go`
2. Update password to match PostgreSQL sovereign user
3. Test: `psql -h localhost -U sovereign -d sovereign -c "SELECT 1"`
4. Rebuild: `cd api && go build -o server ./cmd/server/`
5. Start: `./server` — verify health check responds
6. Fix Redis connection (optional — skip if Redis not installed)

**Files:** `api/internal/database/db.go`
**Gate:** `curl localhost:8080/health` returns HTTP 200
**Risk:** LOW — single variable change, easily reversible

**Architectural Note:** The global `database.DB`/`database.Pool` pattern is a known
technical debt item. We are NOT fixing this in Sprint 5. We are documenting it for
Sprint 7 when we refactor for testability. For now, we just make it work.

---

#### Task 1.2: Fix Frontend Type Errors [3h] P0

**Why:** `ignoreBuildErrors: true` hides real bugs. Every page could have runtime errors.

**Constitution Check:**
- Q1: Why? Because suppressed type errors = unknown runtime failures
- Q6: What would fail? Pages crash in production, data loss, bad UX
- Q7: Simplest version? Fix critical paths (auth, contacts, deals, dashboard)

**Implementation:**
1. Remove `ignoreBuildErrors: true` from `next.config.js`
2. Run `npx next build` — capture ALL errors
3. Fix errors by priority:
   a. Auth context — ensure `useAuth()` returns correct types
   b. Dashboard — fix AuthContext usage, state types
   c. Contacts — fix Contact type, api usage
   d. Deals — fix Deal type, pipeline types
   e. Leads — fix Lead type
   f. Pipeline — fix drag-drop types
   g. Admin pages — fix template literals, api usage
4. Run `npx next build` — verify 0 errors

**Files:**
- `web/next.config.js` (remove ignoreBuildErrors)
- `web/app/dashboard/page.tsx`
- `web/app/contacts/page.tsx`, `contacts/[id]/page.tsx`, `contacts/new/page.tsx`
- `web/app/deals/page.tsx`, `deals/[id]/page.tsx`
- `web/app/leads/page.tsx`, `leads/[id]/page.tsx`, `leads/new/page.tsx`
- `web/app/pipeline/page.tsx`
- `web/app/admin/*/page.tsx`
- `web/components/auth-provider.tsx`
- `web/types/` (may need shared type definitions)

**Gate:** `npx next build` completes with 0 errors
**Risk:** MEDIUM — some type errors may require significant refactoring
**Fallback:** If errors are too deep, create `web/types/index.ts` with `any` types for legacy pages, fix Sprint 4 pages properly

---

#### Task 1.3: Health Check Endpoint [1h] P1

**Why:** Operational visibility. We cannot monitor what we cannot measure.

**Constitution Check:**
- Q8: What scales? Health check must be lightweight (<1ms)
- Q9: How to measure success? Returns correct DB status

**Implementation:**
1. Add GET `/health` to `api/cmd/server/main.go`
2. Returns: `{"status": "ok", "db": "connected", "uptime": N}`
3. Add GET `/health/db` — runs `SELECT 1` against PostgreSQL
4. Add GET `/health/redis` — pings Redis (optional)

**Files:** `api/cmd/server/main.go`
**Gate:** `curl localhost:8080/health` returns correct JSON
**Risk:** LOW — simple addition

---

### Day 1 Gate Check:
- [ ] API starts without errors
- [ ] Health check returns 200
- [ ] Frontend builds with 0 TS errors
- [ ] Both servers can run simultaneously

---

### Day 2: API Smoke Tests (6h)

**Methodology:** Each task follows the pattern:
1. Write the test manually first (what SHOULD happen)
2. Run it against the live API
3. Fix any failures
4. Document the result

---

#### Task 1.4: Auth Flow Test [2h] P0

**Why:** Auth is the gateway. If it's broken, nothing works.

**Persona: Small Business Owner**
- "Can I register and log in without calling support?"
- "Is my password secure?"
- "Can I get back in if I forget my password?"

**Test Cases:**
```
1. POST /auth/register — valid data → 201 + user object
2. POST /auth/register — duplicate email → 409 conflict
3. POST /auth/register — missing fields → 400 validation error
4. POST /auth/login — valid credentials → 200 + JWT token
5. POST /auth/login — wrong password → 401 unauthorized
6. POST /auth/login — non-existent user → 401 unauthorized
7. GET /auth/me — valid token → 200 + user profile
8. GET /auth/me — expired token → 401 unauthorized
9. GET /auth/me — no token → 401 unauthorized
10. POST /auth/refresh — valid refresh token → 200 + new JWT
```

**Implementation:**
1. Create `api/tests/auth_test.go`
2. Use `httptest.NewServer` with the chi router
3. Create test database `sovereign_test`
4. Run each test case
5. Document pass/fail

**Files:** `api/tests/auth_test.go`
**Gate:** All 10 test cases pass
**Risk:** LOW — testing existing code

---

#### Task 1.5: Contact CRUD Test [2h] P0

**Why:** Contacts are the core entity. Every other feature references them.

**Persona: Sales Rep**
- "Can I add a new contact quickly?"
- "Can I find a contact by name or company?"
- "Can I see all contacts for my pipeline?"

**Test Cases:**
```
1. POST /contacts — valid data → 201 + contact object
2. POST /contacts — duplicate email → dedup or 409
3. GET /contacts — list → 200 + paginated results
4. GET /contacts?page=1&limit=10 — pagination works
5. GET /contacts?search=John — search works
6. GET /contacts/{id} — get single → 200 + contact
7. GET /contacts/{id} — non-existent → 404
8. PUT /contacts/{id} — update → 200 + updated contact
9. DELETE /contacts/{id} — delete → 204
10. POST /contacts/{id}/merge — merge duplicate → 200
```

**Files:** `api/tests/contacts_test.go`
**Gate:** All 10 test cases pass

---

#### Task 1.6: Deal Pipeline Test [2h] P0

**Why:** Pipeline is the revenue engine. Must work flawlessly.

**Persona: Sales Manager**
- "Can I see my pipeline at a glance?"
- "Can I move deals between stages?"
- "Can I forecast revenue?"

**Test Cases:**
```
1. POST /deals — create deal → 201 + deal object
2. GET /deals — list deals → 200 + paginated
3. GET /deals/{id} — get deal → 200 + deal with stage
4. PUT /deals/{id}/stage — move to next stage → 200
5. PUT /deals/{id}/stage — move to invalid stage → 400
6. GET /reports/pipeline — pipeline report → 200 + stage breakdown
7. GET /reports/overview — overview → 200 + summary metrics
8. DELETE /deals/{id} — delete deal → 204
9. GET /deals?stage=qualified — filter by stage → 200
10. POST /deals — deal with organization → 201 + org linked
```

**Files:** `api/tests/deals_test.go`
**Gate:** All 10 test cases pass

---

### Day 2 Gate Check:
- [ ] Auth flow works end-to-end
- [ ] Contact CRUD works end-to-end
- [ ] Deal pipeline works end-to-end
- [ ] All 30 test cases pass

---

### Day 3: Email + Sequences Verification (6h)

#### Task 1.7: Email Account Test [2h] P1

**Why:** Email integration is Sprint 4's primary feature. Must work.

**Persona: Sales Rep**
- "Can I connect my Gmail in 2 minutes?"
- "Do my emails show up automatically?"
- "Can I send emails from the CRM?"

**Test Cases:**
```
1. POST /email-accounts — create with IMAP/SMTP → 201
2. GET /email-accounts — list accounts → 200
3. DELETE /email-accounts/{id} — delete → 204
4. POST /email-templates — create template → 201
5. PUT /email-templates/{id} — update template → 200
6. GET /email-templates — list templates → 200
7. POST /email-messages/send — send email → 200 (if SMTP configured)
8. GET /email-messages — list messages → 200
```

**Files:** `api/tests/email_test.go`
**Gate:** Account CRUD works; send status documented

---

#### Task 1.8: Email Deliverability Test [2h] P1

**Why:** Sending emails that land in spam is worse than not sending at all.

**VoC Evidence:** Frustration #60 — "Email sync is unreliable — emails disappear from CRM" (88 confidence)

**Test Protocol:**
1. Send 5 test emails via SMTP to different providers:
   - Gmail (check primary + spam)
   - Outlook (check primary + junk)
   - Yahoo (check primary + spam)
   - ProtonMail (check inbox + spam)
   - Self-hosted (check delivery)
2. Record: delivered, bounced, spam, timing
3. Check SPF/DKIM/DMARC records for sending domain
4. Document findings and recommendations

**Deliverables:**
- Email deliverability report (which providers work)
- SPF/DKIM/DMARC setup guide
- Recommendations for improving deliverability

**Gate:** Report complete with actionable recommendations
**Risk:** HIGH — email deliverability is provider-dependent

---

#### Task 1.9: Sequence CRUD Test [2h] P1

**Why:** Sequences are the automation layer. Must be functional.

**Persona: Sales Rep**
- "Can I set up a follow-up sequence?"
- "Will it send emails automatically?"
- "Can I pause a sequence if a prospect replies?"

**Test Cases:**
```
1. POST /sequences — create sequence → 201
2. GET /sequences — list sequences → 200
3. GET /sequences/{id} — get with steps → 200
4. POST /sequences/{id}/enroll — enroll contact → 200
5. GET /sequences/{id}/enrollments — list enrollments → 200
6. PUT /sequences/{id} — update sequence → 200
7. DELETE /sequences/{id} — delete → 204
```

**Files:** `api/tests/sequences_test.go`
**Gate:** All 7 test cases pass

---

### Day 3 Gate Check:
- [ ] Email account CRUD works
- [ ] SMTP send works (deliverability documented)
- [ ] Sequence CRUD works
- [ ] Email deliverability report complete

---

### Day 4: Integration Test Foundation (6h)

**Why:** We need automated tests to prevent regressions. Every future sprint depends on this.

**Constitution Check:**
- Q8: What scales? Tests scale — they catch bugs before users do
- Q9: How to measure? `go test ./tests/ -v` passes
- Q10: How to know to remove? Never — tests are permanent infrastructure

---

#### Task 1.10: Auth Integration Tests [2h]

**Implementation:**
1. Create `api/tests/auth_test.go`
2. Test database setup: create `sovereign_test` schema, run migrations
3. Test helpers: createTestUser, getAuthToken, makeRequest
4. Test cases from Task 1.4 (automated)
5. Teardown: clean test database after each test

**Files:**
- `api/tests/auth_test.go`
- `api/tests/helpers_test.go` (shared test utilities)

**Gate:** `go test ./tests/ -run TestAuth -v` passes

---

#### Task 1.11: Contact Integration Tests [2h]

**Implementation:**
1. Create `api/tests/contacts_test.go`
2. Test cases from Task 1.5 (automated)
3. Test edge cases: empty fields, long strings, special characters
4. Test pagination with large datasets (100+ contacts)

**Files:** `api/tests/contacts_test.go`
**Gate:** `go test ./tests/ -run TestContacts -v` passes

---

#### Task 1.12: Deal Integration Tests [2h]

**Implementation:**
1. Create `api/tests/deals_test.go`
2. Test cases from Task 1.6 (automated)
3. Test stage transitions (can't skip stages?)
4. Test pipeline report accuracy

**Files:** `api/tests/deals_test.go`
**Gate:** `go test ./tests/ -run TestDeals -v` passes

---

### Day 4 Gate Check:
- [ ] Test helpers exist (createTestUser, getAuthToken, makeRequest)
- [ ] Auth tests pass (10 cases)
- [ ] Contact tests pass (10 cases)
- [ ] Deal tests pass (10 cases)
- [ ] `go test ./tests/ -v` runs clean

---

### Day 5: Deployment Prep (6h)

---

#### Task 1.13: Docker Compose [2h]

**Why:** Self-hosted deployment must be one command. This is our distribution model.

**Constitution Check:**
- Q2: What problem? Users need to self-host without being sysadmins
- Q4: Why insufficient? Manual deployment is error-prone and slow
- Q7: Simplest version? docker-compose up

**Implementation:**
1. Create `docker-compose.yml`:
   ```yaml
   services:
     api:
       build: ./api
       ports: ["8080:8080"]
       depends_on: [db]
       environment:
         DATABASE_URL: postgres://sovereign:sovereign123@db:5432/sovereign
     web:
       build: ./web
       ports: ["3000:3000"]
       depends_on: [api]
     db:
       image: postgres:16
       volumes: [pgdata:/var/lib/postgresql/data]
       environment:
         POSTGRES_USER: sovereign
         POSTGRES_PASSWORD: sovereign123
         POSTGRES_DB: sovereign
   volumes:
     pgdata:
   ```
2. Create `api/Dockerfile` (multi-stage Go build)
3. Create `web/Dockerfile` (multi-stage Next.js build)
4. Test: `docker-compose up --build`

**Files:**
- `docker-compose.yml`
- `api/Dockerfile`
- `web/Dockerfile`

**Gate:** `docker-compose up --build` starts all services
**Risk:** LOW — standard Docker setup

---

#### Task 1.14: Deployment Script [1h]

**Implementation:**
1. Create `deploy.sh`:
   ```bash
   #!/bin/bash
   set -e
   echo "Building..."
   docker-compose build
   echo "Starting..."
   docker-compose up -d
   echo "Seeding..."
   docker-compose exec api ./migrate
   echo "Done! http://localhost:3000"
   ```
2. Create `deploy-dev.sh` (local development, no Docker)
3. Create `.env.example` (environment variable template)

**Files:**
- `deploy.sh`
- `deploy-dev.sh`
- `.env.example`

**Gate:** `./deploy-dev.sh` runs successfully

---

#### Task 1.15: README.md [2h]

**Why:** Nobody can use the product without documentation. This is our front door.

**Structure:**
```markdown
# Sovereign CRM

> Open-source, self-hosted CRM with local AI. Your data never leaves your server.

## Quick Start
1. git clone https://github.com/sovereign-crm/sovereign
2. cd sovereign
3. docker-compose up --build
4. Open http://localhost:3000
5. Register your account

## Architecture
[ASCII diagram of components]

## Features
- Contact management
- Deal pipeline
- Email integration (IMAP/SMTP)
- Sequences and workflows
- Reports and analytics
- Role-based access control
- Custom fields

## API Reference
[Link to /docs or Swagger]

## Self-Hosting Guide
[Step-by-step deployment]

## Contributing
[Link to CONTRIBUTING.md]

## License
AGPL v3 (with commercial exception)
```

**Files:**
- `README.md`

**Gate:** README renders correctly on GitHub
**Risk:** LOW — documentation only

---

#### Task 1.16: Sprint 1 Checkpoint [1h]

**Implementation:**
1. Review all Week 1 tasks
2. Verify all gates passed
3. Document any carryover items
4. Update todo list
5. Brief retrospective: what went well, what was harder than expected

**Gate:** All Week 1 gates verified
**Risk:** N/A — review only

---

### WEEK 1 SUMMARY

| Task | Hours | Priority | Gate |
|------|:-----:|:--------:|------|
| 1.1 Fix DB Connection | 2 | P0 | Health check returns 200 |
| 1.2 Fix Frontend Types | 3 | P0 | Next.js build passes |
| 1.3 Health Check | 1 | P1 | Endpoint returns status |
| 1.4 Auth Flow Test | 2 | P0 | 10 test cases pass |
| 1.5 Contact CRUD Test | 2 | P0 | 10 test cases pass |
| 1.6 Deal Pipeline Test | 2 | P0 | 10 test cases pass |
| 1.7 Email Account Test | 2 | P1 | CRUD works |
| 1.8 Email Deliverability | 2 | P1 | Report complete |
| 1.9 Sequence CRUD Test | 2 | P1 | 7 test cases pass |
| 1.10 Auth Integration Tests | 2 | P0 | go test passes |
| 1.11 Contact Integration Tests | 2 | P0 | go test passes |
| 1.12 Deal Integration Tests | 2 | P0 | go test passes |
| 1.13 Docker Compose | 2 | P1 | docker-compose up works |
| 1.14 Deployment Script | 1 | P1 | deploy-dev.sh works |
| 1.15 README.md | 2 | P1 | Renders on GitHub |
| 1.16 Checkpoint | 1 | P0 | All gates verified |
| **TOTAL** | **15h** | | |

---

## WEEK 2: MAKE IT REAL (Days 6-10)

**Goal:** Product is live. Real humans are using it. We have feedback.

---

### Day 6: Deploy to Live (6h)

---

#### Task 2.1: Deploy to Railway/Render [3h] P0

**Why:** If the product isn't accessible via URL, it doesn't exist.

**Constitution Check:**
- Q1: Why? Because we need real users to validate assumptions
- Q2: Problem? Users can't try what they can't reach
- Q9: Measure? Product accessible at public URL

**Implementation:**
1. Create Railway account (free tier: $5 credit)
2. Connect GitHub repository
3. Configure environment:
   - DATABASE_URL (Railway PostgreSQL)
   - JWT_SECRET
   - REDIS_URL (optional)
4. Deploy Go API service
5. Deploy Next.js web service
6. Configure custom domain (if available)
7. Verify: health check passes, frontend loads

**Alternative:** Render.com (free tier available)

**Gate:** Public URL accessible, health check passes
**Risk:** MEDIUM — deployment platforms can have issues
**Fallback:** Deploy to user's own WSL2 with ngrok for temporary public URL

---

#### Task 2.2: Custom Domain [1h] P2

**Implementation:**
1. Purchase domain (if not already owned)
2. Point DNS to Railway/Render
3. Configure SSL (automatic)
4. Verify HTTPS works

**Gate:** https://demo.sovereigncrm.com loads
**Risk:** LOW — DNS propagation can take time

---

#### Task 2.3: Seed Demo Data [2h] P1

**Why:** An empty CRM is useless for demos. Users need to see value immediately.

**VoC Evidence:** Frustration #79 — "No guided setup — you're dropped into an empty system" (85 confidence)

**Implementation:**
1. Create `api/cmd/seed/main.go` or `api/seeds/seed.sql`
2. Seed data:
   - 1 admin user (admin@demo.com / demo123)
   - 50 contacts (realistic names, companies, emails)
   - 20 deals across pipeline stages
   - 100 activities (calls, emails, meetings)
   - 5 email accounts (test configurations)
   - 3 sequences (active, paused, completed)
   - 2 workflows (active, inactive)
   - 10 organizations
3. Run seed: `go run cmd/seed/main.go`

**Files:**
- `api/cmd/seed/main.go` (or `api/seeds/seed.sql`)

**Gate:** Demo data loads, frontend shows populated data
**Risk:** LOW — seed data creation

---

### Day 6 Gate Check:
- [ ] Public URL accessible
- [ ] SSL working
- [ ] Demo data loaded
- [ ] Frontend shows populated data

---

### Day 7: First User Testing (6h)

---

#### Task 2.4: Internal Testing [3h] P0

**Why:** Find bugs before users do.

**Test Protocol:**
1. Register new account
2. Create contact (fill all fields)
3. Create organization
4. Link contact to organization
5. Create deal
6. Move deal through pipeline (all stages)
7. Log activity (call, email, meeting)
8. Send email (if SMTP configured)
9. Create sequence
10. Create workflow
11. View reports (all tabs)
12. Test admin pages (users, roles, custom fields)
13. Test search
14. Test pagination across all list views

**Documentation:**
- Create `BUGS.md` — list every bug found
- Severity: CRITICAL (crash), HIGH (data loss), MEDIUM (functional), LOW (UX)
- Screenshot/video for each bug

**Gate:** Complete user flow works without crashes
**Risk:** MEDIUM — bugs expected

---

#### Task 2.5: Fix Critical Bugs [3h] P0

**Priority Order:**
1. CRITICAL bugs — application crashes
2. HIGH bugs — data loss or corruption
3. MEDIUM bugs — feature doesn't work as expected
4. LOW bugs — cosmetic issues (defer to Sprint 6)

**Gate:** 0 CRITICAL bugs, 0 HIGH bugs remaining
**Risk:** MEDIUM — fixes may introduce new bugs

---

### Day 7 Gate Check:
- [ ] Complete user flow tested
- [ ] All bugs documented
- [ ] CRITICAL and HIGH bugs fixed
- [ ] Product stable for external testing

---

### Day 8: External Feedback (5h)

---

#### Task 2.6: Post to Reddit [2h] P0

**Why:** This is our first real market validation. Everything before this is assumption.

**Posts:**

**r/selfhosted (50K+ members):**
Title: "I built an open-source self-hosted CRM with local AI — looking for feedback"
Body: Live demo link, GitHub link, 3-sentence description, ask for feedback

**r/CRM (10K+ members):**
Title: "Built a CRM alternative — would love feedback from sales teams"
Body: Problem statement, what's different, demo link

**Hacker News:**
Title: "Show HN: Sovereign CRM (open-source, self-hosted, local AI)"
Body: Technical details, architecture, what we're building

**Monitoring:**
- Check every 2 hours for first 24h
- Respond to ALL comments (positive and negative)
- Take notes on every question asked

**Gate:** Posts live, monitoring active
**Risk:** MEDIUM — may get no engagement

---

#### Task 2.7: DM 10 Target Users [2h] P1

**Why:** Direct conversations produce deeper insights than public posts.

**Target Profile:**
- People who posted about CRM frustrations on Reddit
- People asking for CRM recommendations
- Small business owners looking for alternatives

**Outreach Template:**
```
Hey [name], I saw your post about [CRM frustration]. I'm building
an open-source CRM that addresses exactly that. Would you be open
to a 15-min call to give feedback? I'd give you lifetime access
and credit you as a co-creator.
```

**Gate:** 10 DMs sent, tracking responses
**Risk:** LOW — worst case, no response

---

#### Task 2.8: Create Feedback Form [1h] P1

**Platform:** Tally.so (free, no account needed)

**Questions:**
1. What CRM do you currently use? (dropdown)
2. What's your biggest CRM frustration? (open text)
3. What features are must-haves? (checkbox list)
4. Would you try a self-hosted CRM? (yes/no/maybe)
5. What would make you switch? (open text)
6. How many people on your team? (dropdown)
7. What's your budget per user/month? (dropdown)

**Gate:** Form live, link included in Reddit posts
**Risk:** LOW — form creation

---

### Day 8 Gate Check:
- [ ] Reddit posts live
- [ ] 10 DMs sent
- [ ] Feedback form live
- [ ] Monitoring active

---

### Day 9: Feedback Analysis (5h)

---

#### Task 2.9: Collect and Analyze Feedback [3h] P0

**Methodology:**
1. Collect all feedback from:
   - Reddit comments and DMs
   - Feedback form responses
   - Direct conversations
2. Categorize by:
   - Pain points (what they hate)
   - Must-haves (features they need)
   - Deal-breakers (what prevents adoption)
   - Nice-to-haves (features they want but can live without)
3. Score by frequency and intensity
4. Create feedback summary document

**Deliverable:** `vault/feedback/sprint-5-feedback.md`

**Gate:** Feedback document complete with categorized findings
**Risk:** LOW — analysis only

---

#### Task 2.10: Update Sprint 6 Priorities [2h] P0

**Why:** Sprint 6 must be informed by real feedback, not assumptions.

**Implementation:**
1. Map feedback to existing Sprint 6+ backlog items
2. Identify NEW items not previously considered
3. Prioritize using MoSCoW:
   - Must have (address top 3 pain points)
   - Should have (address next 3)
   - Could have (nice-to-haves)
   - Won't have (not this time)
4. Create Sprint 6 draft plan

**Deliverable:** `vault/blueprints/implementation/sprint-6-draft.md`

**Gate:** Sprint 6 priorities aligned with feedback
**Risk:** LOW — planning only

---

### Day 9 Gate Check:
- [ ] Feedback categorized and scored
- [ ] Sprint 6 priorities updated
- [ ] Top 3 user pain points identified

---

### Day 10: Sprint 2 Checkpoint (5h)

---

#### Task 2.11: Mid-Review [2h] P0

**Checklist:**
- [ ] All Week 2 tasks complete
- [ ] Deployment stable
- [ ] Feedback collected (minimum 5 responses)
- [ ] Sprint 6 priorities updated
- [ ] Any blockers for Week 3 identified

**Deliverable:** Updated todo list, risk register

---

#### Task 2.12: Fix Remaining Issues [3h] P1

**Scope:**
- Fix any deployment issues
- Fix bugs reported by external users
- Optimize performance if needed
- Update documentation based on feedback

**Gate:** Stable deployment, 0 critical issues
**Risk:** MEDIUM — scope depends on feedback

---

### WEEK 2 SUMMARY

| Task | Hours | Priority | Gate |
|------|:-----:|:--------:|------|
| 2.1 Deploy to Railway/Render | 3 | P0 | Public URL accessible |
| 2.2 Custom Domain | 1 | P2 | HTTPS works |
| 2.3 Seed Demo Data | 2 | P1 | Data loaded |
| 2.4 Internal Testing | 3 | P0 | Complete flow works |
| 2.5 Fix Critical Bugs | 3 | P0 | 0 critical bugs |
| 2.6 Post to Reddit | 2 | P0 | Posts live |
| 2.7 DM 10 Target Users | 2 | P1 | DMs sent |
| 2.8 Create Feedback Form | 1 | P1 | Form live |
| 2.9 Analyze Feedback | 3 | P0 | Document complete |
| 2.10 Update Sprint 6 | 2 | P0 | Priorities aligned |
| 2.11 Mid-Review | 2 | P0 | Checkpoint complete |
| 2.12 Fix Issues | 3 | P1 | Stable deployment |
| **TOTAL** | **14h** | | |

---

## WEEK 3: MAKE IT DIFFERENT (Days 11-15)

**Goal:** Build the foundation of our actual moats. Make us different from Twenty.

---

### Day 11-12: Core Moat Foundation (10h)

---

#### Task 3.1: CRDT Foundation [6h] P0

**Why This Is The #1 Priority:**

From Project Brief: "Zero Latency is non-negotiable."
From 4 Moats: Moat #1 — CRDT (Automerge/Yjs/Go-native)
From Strategic Audit: "Every sprint without CRDT makes retrofit harder."

**Constitution Check:**
- Q1: Why? Because CRDT enables real-time collaboration, our #1 differentiator
- Q2: Problem? Two reps editing the same deal causes conflicts (VoC #96)
- Q4: Why insufficient? Without CRDT, we're just another CRUD app
- Q5: Assumptions? ygo works with our data model, performance is acceptable
- Q7: Simplest version? Contact name + email sync only

**Implementation:**

**Phase 1: Schema (2h)**
1. Create `api/internal/crdt/` package
2. Create `crdt_documents` table:
   ```sql
   CREATE TABLE crdt_documents (
       id UUID PRIMARY KEY,
       entity_type VARCHAR(50) NOT NULL,
       entity_id UUID NOT NULL,
       document JSONB NOT NULL,
       clock BIGINT DEFAULT 0,
       updated_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```
3. Create `crdt_operations` table:
   ```sql
   CREATE TABLE crdt_operations (
       id UUID PRIMARY KEY,
       document_id UUID REFERENCES crdt_documents(id),
       operation JSONB NOT NULL,
       clock BIGINT NOT NULL,
       created_by UUID,
       created_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```

**Phase 2: Core Logic (2h)**
4. Create `crdt/crdt.go` — document operations:
   - `NewDocument(id, entityType, entityID, initialData)`
   - `ApplyOperation(doc, op)` — apply CRDT operation
   - `MergeDocuments(doc1, doc2)` — merge two document states
   - `GetState(doc)` — get current state

**Phase 3: WebSocket Transport (1h)**
5. Add WebSocket endpoint: `GET /ws/crdt/{entity_type}/{entity_id}`
6. On connect: send current document state
7. On operation: broadcast to all connected clients
8. On disconnect: cleanup

**Phase 4: Integration (1h)**
9. Modify contact update handler to also update CRDT document
10. Add WebSocket connection to contact detail page
11. Test: two browser tabs editing same contact sync in <100ms

**Files:**
- `api/internal/crdt/crdt.go`
- `api/internal/crdt/websocket.go`
- `api/internal/database/migrations/009_crdt.sql`
- `web/lib/crdt-client.ts`
- `web/app/contacts/[id]/page.tsx` (add WebSocket)

**Gate:** Two browser tabs editing same contact sync in <100ms
**Risk:** MEDIUM — CRDT complexity, but timeboxed to 6h
**Fallback:** If ygo integration is too complex, implement basic last-writer-wins with WebSocket

**Architectural Decision:**
- We are NOT replacing PostgreSQL with CRDT storage
- CRDT is a SYNC layer on top of PostgreSQL
- PostgreSQL remains the source of truth
- CRDT enables real-time collaboration, not offline-first (yet)
- This is a pragmatic first step toward the full CRDT vision

---

#### Task 3.2: Dynamic Object Builder Schema [4h] P0

**Why This Is The #2 Priority:**

From Project Brief: "Infinite Extensibility" — Moat #3
From 4 Moats: Metadata-driven Dynamic Object Builder
From Strategic Audit: "Without this, we're just another CRUD app"

**Constitution Check:**
- Q1: Why? Because every business has unique entities (projects, tickets, subscriptions)
- Q2: Problem? Users can't model their specific workflow in generic CRMs
- Q4: Why insufficient? Airtable proved this works; we need it
- Q5: Assumptions? JSONB is flexible enough, API design is intuitive
- Q7: Simplest version? Create/read/update custom objects via API

**Implementation:**

**Phase 1: Schema (1h)**
1. Create migration `010_metadata_objects.sql`:
   ```sql
   CREATE TABLE metadata_objects (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       name VARCHAR(100) NOT NULL UNIQUE,
       label VARCHAR(100) NOT NULL,
       description TEXT,
       icon VARCHAR(50),
       created_at TIMESTAMPTZ DEFAULT NOW(),
       updated_at TIMESTAMPTZ DEFAULT NOW()
   );

   CREATE TABLE metadata_fields (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       object_id UUID REFERENCES metadata_objects(id) ON DELETE CASCADE,
       name VARCHAR(100) NOT NULL,
       label VARCHAR(100) NOT NULL,
       field_type VARCHAR(50) NOT NULL, -- text, number, date, select, boolean, reference
       required BOOLEAN DEFAULT false,
       options JSONB, -- for select fields: {values: [...]}
       reference_to UUID, -- for reference fields: which object
       created_at TIMESTAMPTZ DEFAULT NOW(),
       UNIQUE(object_id, name)
   );

   CREATE TABLE metadata_records (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       object_id UUID REFERENCES metadata_objects(id) ON DELETE CASCADE,
       data JSONB NOT NULL DEFAULT '{}',
       created_by UUID,
       created_at TIMESTAMPTZ DEFAULT NOW(),
       updated_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```

**Phase 2: API (2h)**
2. Create `handlers/metadata.go`:
   - `POST /metadata/objects` — create object definition
   - `GET /metadata/objects` — list all objects
   - `GET /metadata/objects/{id}` — get object with fields
   - `POST /metadata/objects/{id}/fields` — add field
   - `DELETE /metadata/objects/{id}/fields/{field_id}` — remove field
   - `POST /metadata/objects/{id}/records` — create record
   - `GET /metadata/objects/{id}/records` — list records
   - `PUT /metadata/objects/{id}/records/{record_id}` — update record
   - `DELETE /metadata/objects/{id}/records/{record_id}` — delete record

**Phase 3: Validation (1h)**
3. Validate record data against field definitions:
   - Required fields present
   - Correct types (number is number, date is date)
   - Select fields have valid options
   - Reference fields point to valid records

**Phase 4: Register Routes (0.5h)**
4. Add routes to `main.go`

**Files:**
- `api/internal/database/migrations/010_metadata_objects.sql`
- `api/internal/handlers/metadata.go`
- `api/cmd/server/main.go` (add routes)

**Gate:** Can create "Projects" object with custom fields via API
**Risk:** MEDIUM — schema design must be flexible enough
**Fallback:** If field types are too complex, start with text/number/date only

**Architectural Decision:**
- JSONB for record data (flexible, PostgreSQL-native)
- No separate table per custom object (would defeat the purpose)
- Validation happens at API layer, not database layer
- Reference fields create relationships between custom objects
- This is the foundation — UI comes in Sprint 7

---

### Day 11-12 Gate Check:
- [ ] CRDT sync works for contact edits (<100ms)
- [ ] Two browser tabs stay in sync
- [ ] Dynamic Object schema implemented
- [ ] Can create/read/update custom objects via API
- [ ] Can create/read/update custom fields via API
- [ ] Can create/read/update records via API

---

### Day 13: Security + Infrastructure (6h)

---

#### Task 3.3: Rate Limiting [2h] P1

**Why:** Self-hosted instances are vulnerable to abuse without rate limiting.

**Implementation:**
1. Create `middleware/ratelimit.go`
2. Use token bucket algorithm (stdlib or `golang.org/x/time/rate`)
3. Limits:
   - Unauthenticated: 100 requests/minute per IP
   - Authenticated: 1000 requests/minute per user
   - Auth endpoints: 10 requests/minute per IP
4. Return 429 with `Retry-After` header
5. Add to chi middleware chain

**Files:**
- `api/internal/middleware/ratelimit.go`
- `api/cmd/server/main.go` (add middleware)

**Gate:** Rate limiting works, documented in README
**Risk:** LOW — standard middleware

---

#### Task 3.4: Input Validation [2h] P1

**Why:** SQL injection and XSS are real risks.

**Implementation:**
1. Create `middleware/validation.go`
2. Validate all API inputs:
   - Email format (regex)
   - Phone format (basic)
   - Required fields present
   - String length limits
3. Sanitize all string inputs:
   - Strip HTML tags
   - Escape special characters
4. Verify all queries use parameterized statements (no string concatenation)
5. Add Content-Security-Policy headers

**Files:**
- `api/internal/middleware/validation.go`
- `api/cmd/server/main.go` (add middleware)

**Gate:** Invalid inputs return 400 with clear error messages
**Risk:** LOW — standard security practice

---

#### Task 3.5: Structured Logging [2h] P1

**Why:** Debugging self-hosted instances without logs is impossible.

**Implementation:**
1. Replace `fmt.Println` with `zerolog` (already in go.mod)
2. Configure log levels via environment variable:
   - `LOG_LEVEL=debug|info|warn|error`
3. Add request ID tracking:
   - Generate UUID per request in middleware
   - Propagate through context
   - Include in all log entries
4. Structured JSON output:
   ```json
   {"level":"info","time":"...","request_id":"...","method":"GET","path":"/contacts","status":200,"duration":"12ms"}
   ```
5. Error logging with stack traces

**Files:**
- `api/internal/middleware/logging.go`
- `api/cmd/server/main.go` (add middleware)

**Gate:** Logs are structured JSON, filterable by level
**Risk:** LOW — logging library swap

---

### Day 13 Gate Check:
- [ ] Rate limiting active (429 returned when exceeded)
- [ ] Input validation active (400 returned for invalid data)
- [ ] Structured logging active (JSON logs)
- [ ] Request ID tracking working

---

### Day 14: Documentation + Tests (5h)

---

#### Task 3.6: API Documentation [2h] P1

**Why:** Nobody can integrate without API docs.

**Implementation:**
1. Create `docs/api/openapi.yaml` (OpenAPI 3.0 spec)
2. Document all endpoints:
   - Request/response examples
   - Authentication requirements
   - Error codes
   - Rate limits
3. Serve Swagger UI at `/docs` (using swaggo/swag)
4. Add API overview to README

**Files:**
- `docs/api/openapi.yaml`
- `api/internal/docs/swagger.go` (Swagger UI handler)

**Gate:** Swagger UI loads at /docs
**Risk:** LOW — documentation

---

#### Task 3.7: Deployment Guide [2h] P1

**Why:** Self-hosted users need step-by-step instructions.

**Structure:**
```markdown
# Self-Hosting Guide

## Prerequisites
- Docker and Docker Compose
- 2GB RAM minimum
- Port 3000 and 8080 available

## Installation
1. Clone the repository
2. Configure environment variables
3. Run docker-compose up
4. Access at http://localhost:3000

## Configuration
### Email Setup
- IMAP settings
- SMTP settings
- SPF/DKIM/DMARC (for deliverability)

### SSL/HTTPS
- Using Let's Encrypt
- Using reverse proxy (nginx/Caddy)

## Backup and Restore
- Database backup: pg_dump
- Full backup: docker volume
- Restore procedure

## Troubleshooting
- Common issues and solutions
- Log locations
- Getting help
```

**Files:** `docs/self-hosting.md`

**Gate:** Guide complete, tested on fresh machine
**Risk:** LOW — documentation

---

#### Task 3.8: Contributing Guide [1h] P2

**Implementation:**
1. Create `CONTRIBUTING.md`:
   - Development setup
   - Code style (gofmt, prettier)
   - PR process
   - Issue templates
   - Code of conduct reference

**Files:** `CONTRIBUTING.md`
**Gate:** Guide complete
**Risk:** LOW — documentation

---

### Day 14 Gate Check:
- [ ] API docs complete
- [ ] Deployment guide complete
- [ ] Contributing guide complete

---

### Day 15: Sprint Review (4h)

---

#### Task 3.9: Sprint 5 Final Review [2h] P0

**Checklist:**
- [ ] All Week 3 tasks complete
- [ ] All success criteria met
- [ ] Carryover items documented
- [ ] Lessons learned captured
- [ ] Risk register updated

**Deliverable:** Sprint 5 retrospective document

---

#### Task 3.10: Sprint 6 Planning [2h] P0

**Based on:**
1. User feedback from Week 2
2. Technical debt identified in Week 1
3. CRDT/Dynamic Objects foundation from Week 3
4. Capacity reality from Sprint 5

**Sprint 6 Candidates (to be prioritized by feedback):**
- AI Chat (if users want it)
- OAuth email (if IMAP/SMTP is insufficient)
- Mobile PWA (if users need mobile)
- Dynamic Objects UI (if custom objects are popular)
- Workflow executor (if sequences are popular)
- Import/Export (if migration is requested)

**Gate:** Sprint 6 plan drafted with priorities
**Risk:** N/A — planning only

---

### WEEK 3 SUMMARY

| Task | Hours | Priority | Gate |
|------|:-----:|:--------:|------|
| 3.1 CRDT Foundation | 6 | P0 | <100ms sync |
| 3.2 Dynamic Objects | 4 | P0 | Custom objects via API |
| 3.3 Rate Limiting | 2 | P1 | 429 when exceeded |
| 3.4 Input Validation | 2 | P1 | 400 for invalid data |
| 3.5 Structured Logging | 2 | P1 | JSON logs |
| 3.6 API Documentation | 2 | P1 | Swagger UI works |
| 3.7 Deployment Guide | 2 | P1 | Guide complete |
| 3.8 Contributing Guide | 1 | P2 | Guide complete |
| 3.9 Sprint Review | 2 | P0 | Review complete |
| 3.10 Sprint 6 Planning | 2 | P0 | Plan drafted |
| **TOTAL** | **10h** (with overlap) | | |

---

## COMPLETE TASK INDEX

| # | Task | Day | Hours | Priority | Status |
|---|------|:---:|:-----:|:--------:|:------:|
| 1.1 | Fix DB Connection | 1 | 2 | P0 | Pending |
| 1.2 | Fix Frontend Types | 1 | 3 | P0 | Pending |
| 1.3 | Health Check Endpoint | 1 | 1 | P1 | Pending |
| 1.4 | Auth Flow Test | 2 | 2 | P0 | Pending |
| 1.5 | Contact CRUD Test | 2 | 2 | P0 | Pending |
| 1.6 | Deal Pipeline Test | 2 | 2 | P0 | Pending |
| 1.7 | Email Account Test | 3 | 2 | P1 | Pending |
| 1.8 | Email Deliverability | 3 | 2 | P1 | Pending |
| 1.9 | Sequence CRUD Test | 3 | 2 | P1 | Pending |
| 1.10 | Auth Integration Tests | 4 | 2 | P0 | Pending |
| 1.11 | Contact Integration Tests | 4 | 2 | P0 | Pending |
| 1.12 | Deal Integration Tests | 4 | 2 | P0 | Pending |
| 1.13 | Docker Compose | 5 | 2 | P1 | Pending |
| 1.14 | Deployment Script | 5 | 1 | P1 | Pending |
| 1.15 | README.md | 5 | 2 | P1 | Pending |
| 1.16 | Sprint 1 Checkpoint | 5 | 1 | P0 | Pending |
| 2.1 | Deploy to Railway/Render | 6 | 3 | P0 | Pending |
| 2.2 | Custom Domain | 6 | 1 | P2 | Pending |
| 2.3 | Seed Demo Data | 6 | 2 | P1 | Pending |
| 2.4 | Internal Testing | 7 | 3 | P0 | Pending |
| 2.5 | Fix Critical Bugs | 7 | 3 | P0 | Pending |
| 2.6 | Post to Reddit | 8 | 2 | P0 | Pending |
| 2.7 | DM 10 Target Users | 8 | 2 | P1 | Pending |
| 2.8 | Create Feedback Form | 8 | 1 | P1 | Pending |
| 2.9 | Analyze Feedback | 9 | 3 | P0 | Pending |
| 2.10 | Update Sprint 6 | 9 | 2 | P0 | Pending |
| 2.11 | Mid-Review | 10 | 2 | P0 | Pending |
| 2.12 | Fix Issues | 10 | 3 | P1 | Pending |
| 3.1 | CRDT Foundation | 11-12 | 6 | P0 | Pending |
| 3.2 | Dynamic Objects | 11-12 | 4 | P0 | Pending |
| 3.3 | Rate Limiting | 13 | 2 | P1 | Pending |
| 3.4 | Input Validation | 13 | 2 | P1 | Pending |
| 3.5 | Structured Logging | 13 | 2 | P1 | Pending |
| 3.6 | API Documentation | 14 | 2 | P1 | Pending |
| 3.7 | Deployment Guide | 14 | 2 | P1 | Pending |
| 3.8 | Contributing Guide | 14 | 1 | P2 | Pending |
| 3.9 | Sprint Review | 15 | 2 | P0 | Pending |
| 3.10 | Sprint 6 Planning | 15 | 2 | P0 | Pending |
| **TOTAL** | | **15 days** | **39h** | | |

---

## RISK REGISTER

| # | Risk | Prob | Impact | Mitigation | Owner |
|---|------|:----:|:------:|------------|:-----:|
| 1 | DB fix breaks other things | LOW | HIGH | Test before/after | Dev |
| 2 | Frontend errors deeper | MED | MED | Fix critical first | Dev |
| 3 | Email fails without SPF | HIGH | HIGH | Document requirements | Dev |
| 4 | CRDT complex | MED | HIGH | Timebox 6h, fallback to LWW | Dev |
| 5 | Dynamic Objects schema wrong | LOW | HIGH | Start simple, iterate | Dev |
| 6 | Reddit no engagement | MED | MED | Try multiple subs | Dev |
| 7 | Users dont want self-hosted | LOW | CRIT | Pivot to managed cloud | Dev |
| 8 | Deployment issues | LOW | MED | Fallback to local+ngrok | Dev |
| 9 | Tests reveal deep bugs | MED | HIGH | Fix critical, document known | Dev |
| 10 | Solo burnout | MED | CRIT | Strict capacity, 5h buffer | Dev |

---

## CONSTITUTION COMPLIANCE

### Article I (10 Questions) — Applied to Sprint 5:

**Q1: Why does this exist?**
We have code that compiles but has never been tested, deployed, or used. We cannot build features for a product that doesn't work.

**Q2: What customer problem does it solve?**
The problem is our own: we are building blind without validation.

**Q3: How is it solved today?**
It isn't. Zero deployment, zero tests, zero feedback.

**Q4: Why are existing solutions insufficient?**
N/A — this is infrastructure, not a feature.

**Q5: What assumptions are we making?**
1. The API can be fixed to start (HIGH confidence)
2. Frontend errors are fixable (MEDIUM confidence)
3. Users want self-hosted CRM (UNVALIDATED)
4. Users want local AI (UNVALIDATED)
5. CRDT is achievable in Go (UNVALIDATED)

**Q6: What would make this fail?**
1. DB fix reveals deeper issues
2. Frontend errors require rewrite
3. Reddit gets zero engagement
4. Users explicitly say they don't want self-hosted

**Q7: What is the simplest version?**
Week 1 only: fix bugs, run tests. Skip CRDT/Dynamic Objects if time runs out.

**Q8: What scales to 10x/100x users?**
Rate limiting and logging prepare for scale. CRDT determines real-time scalability.

**Q9: How do we measure success?**
- Week 1: API starts, frontend builds, tests pass
- Week 2: Deployed, 5+ feedback responses
- Week 3: CRDT works, Dynamic Objects exist, docs complete

**Q10: How do we know it should be removed?**
If Week 1 fixes reveal unfixable problems, pause and redesign.

---

## ARCHITECTURE DECISIONS IN THIS SPRINT

| Decision | Choice | Rationale | Trade-off |
|----------|--------|-----------|-----------|
| CRDT approach | Sync layer over PostgreSQL | PostgreSQL is source of truth; CRDT is collaboration layer | More complex than pure CRDT |
| Dynamic Objects storage | JSONB in metadata_records | Flexible, PostgreSQL-native | Query performance at scale |
| Rate limiting | Token bucket per IP/user | Standard, battle-tested | Memory per IP |
| Logging | zerolog JSON | Structured, fast | Learning curve |
| Deployment | Docker Compose | Simple, reproducible | Not Kubernetes-scale |
| Testing | httptest.NewServer | Isolated, fast | Not full integration |

---

## SUCCESS CRITERIA (FINAL)

### Must Pass (Sprint 5 is a failure if these fail):
- [ ] API starts and responds to health check
- [ ] Frontend builds with 0 TypeScript errors
- [ ] Auth, Contact, Deal flows work end-to-end
- [ ] Product deployed to public URL
- [ ] At least 5 feedback responses collected
- [ ] CRDT sync works for contact edits
- [ ] Dynamic Object Builder schema implemented

### Should Pass (Sprint 5 is weakened if these fail):
- [ ] Email send works (deliverability documented)
- [ ] Sequence CRUD works
- [ ] Integration tests pass (30+ cases)
- [ ] Docker Compose works
- [ ] README.md complete
- [ ] Rate limiting active
- [ ] Input validation active
- [ ] Structured logging active

### Nice to Have (Sprint 5 is fine without these):
- [ ] Custom domain configured
- [ ] Swagger UI working
- [ ] Contributing guide complete
- [ ] Deployment guide complete

---

## WHAT THIS SPRINT DOES NOT DO

| Feature | Deferred | Reason |
|---------|:--------:|--------|
| AI Chat (NL→Query) | Sprint 7 | Unvalidated, need feedback |
| AI Chat (NL→Action) | Sprint 7 | Unvalidated |
| Deal risk detection | Sprint 7 | Needs real data |
| Pipeline health | Sprint 7 | Needs real data |
| Dashboard builder | Sprint 8 | Low priority |
| AI enrichment | Sprint 8 | High hallucination risk |
| OAuth email | Sprint 7 | IMAP/SMTP sufficient |
| Mobile PWA | Sprint 8 | Desktop-first MVP |
| Visual workflow builder | Sprint 8 | Basic triggers sufficient |
| Calendar sync | Sprint 8 | Email higher priority |
| Import/Export | Sprint 7 | Important, not critical |
| SSO/SAML | Sprint 9 | Enterprise, not MVP |
| Multi-tenancy | Sprint 9 | Single-tenant for MVP |

---

*This plan was created through 16-persona strategic audit, Constitution compliance
review, architecture assessment, and capacity validation. Every task has been
validated against the principle: "Every task must either validate an assumption
or build a differentiating moat."*
