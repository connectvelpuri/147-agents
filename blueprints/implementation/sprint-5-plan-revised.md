# Sprint 5 — Revised Execution Plan

**Date:** 2026-06-07 (Revised post-audit)
**Theme:** "Deploy, Validate, Foundation, Then Build"
**Duration:** 3 weeks (15 working days)
**Philosophy:** Every task must either validate an assumption or build a differentiating moat.

---

## AUDIT FINDINGS INCORPORATED

### Sprint 4 Verification (Today):
- API cannot start — DB auth failure (CRITICAL)
- Frontend build suppressed via ignoreBuildErrors (HIGH)
- No endpoint tested end-to-end (CRITICAL)
- SMTP deliverability unknown (HIGH)

### 16-Persona Strategic Audit:
- Zero deployed product (CRITICAL)
- Zero customer interviews (CRITICAL)
- Core moats not built — CRDT, Dynamic Objects (CRITICAL)
- No test suite (HIGH)
- No documentation (HIGH)
- No monitoring/observability (MEDIUM)
- No backup/restore (HIGH)
- No email deliverability setup (HIGH)
- Global DB pattern prevents testing (MEDIUM)

---

## SPRINT 5 STRUCTURE

**Week 1:** Make It Work (Days 1-5)
**Week 2:** Make It Real (Days 6-10)
**Week 3:** Make It Different (Days 11-15)

---

## WEEK 1: MAKE IT WORK

### Day 1: Critical Fixes
- Task 1.1 Fix DB Connection (2h)
- Task 1.2 Fix Frontend Type Errors (3h)
- Task 1.3 Health Check Endpoint (1h)

### Day 2: API Smoke Tests
- Task 1.4 Auth Flow Test (2h)
- Task 1.5 Contact CRUD Test (2h)
- Task 1.6 Deal Pipeline Test (2h)

### Day 3: Email + Sequences
- Task 1.7 Email Account Test (2h)
- Task 1.8 Email Deliverability Test (2h)
- Task 1.9 Sequence CRUD Test (2h)

### Day 4: Integration Tests
- Task 1.10 Auth Tests (2h)
- Task 1.11 Contact Tests (2h)
- Task 1.12 Deal Tests (2h)

### Day 5: Deployment Prep
- Task 1.13 Docker Compose (2h)
- Task 1.14 Deployment Script (1h)
- Task 1.15 README.md (2h)
- Task 1.16 Checkpoint (1h)

---

## WEEK 2: MAKE IT REAL

### Day 6: Deploy
- Task 2.1 Deploy to Railway/Render (3h)
- Task 2.2 Custom Domain (1h)
- Task 2.3 Seed Demo Data (2h)

### Day 7: Testing
- Task 2.4 Internal Testing (3h)
- Task 2.5 Fix Critical Bugs (3h)

### Day 8: Feedback
- Task 2.6 Post to Reddit (2h)
- Task 2.7 DM 10 Target Users (2h)
- Task 2.8 Feedback Form (1h)

### Day 9: Analysis
- Task 2.9 Analyze Feedback (3h)
- Task 2.10 Update Sprint 6 Priorities (2h)

### Day 10: Checkpoint
- Task 2.11 Mid-Review (2h)
- Task 2.12 Fix Issues (3h)

---

## WEEK 3: MAKE IT DIFFERENT

### Day 11-12: Moats
- Task 3.1 CRDT Foundation (6h)
- Task 3.2 Dynamic Object Builder (4h)

### Day 13: Security
- Task 3.3 Rate Limiting (2h)
- Task 3.4 Input Validation (2h)
- Task 3.5 Structured Logging (2h)

### Day 14: Docs
- Task 3.6 API Docs (2h)
- Task 3.7 Deployment Guide (2h)
- Task 3.8 Contributing Guide (1h)

### Day 15: Review
- Task 3.9 Sprint Review (2h)
- Task 3.10 Sprint 6 Planning (2h)

---

## NEW VARIABLES

1. Email Deliverability — test SPF/DKIM/DMARC
2. DB Password Alignment — fix before anything else
3. Docker Compose — one-command deployment
4. Demo Data Seeding — empty CRM is useless
5. Rate Limiting — prevent API abuse
6. Input Validation — security
7. Structured Logging — observability
8. User Feedback Loop — validate before building more
9. CRDT Foundation — our #1 moat, deferred 5 sprints
10. Dynamic Object Builder — our #3 moat, deferred 5 sprints

---

## CAPACITY

| Week | Hours | Buffer |
|------|:-----:|:------:|
| Week 1 | 15h | 1h |
| Week 2 | 14h | 2h |
| Week 3 | 10h | 2h |
| Total | 39h | 5h |

### Cut (26h): AI Chat, Dashboard Builder, AI Enrichment, Risk Detection, Health Engine, Insight Cards

---

## RISKS

1. DB fix breaks things (LOW/HIGH) — test before/after
2. Frontend errors deeper (MED/MED) — fix critical first
3. Email fails without SPF (HIGH/HIGH) — document requirements
4. CRDT complex (MED/HIGH) — timebox 6h
5. Reddit no engagement (MED/MED) — try multiple subs
6. Users dont want self-hosted (LOW/CRIT) — pivot to cloud
7. Solo burnout (MED/CRIT) — strict capacity

---

## SUCCESS

Week 1: API starts, frontend builds, smoke tests pass
Week 2: Deployed, 5+ feedback responses, Sprint 6 prioritized
Week 3: CRDT works, Dynamic Objects exist, docs complete

---

## DEFERRALS

AI Chat → Sprint 7
Risk Detection → Sprint 7
Dashboard Builder → Sprint 8
OAuth Email → Sprint 7
Mobile PWA → Sprint 8
Calendar → Sprint 8
SSO → Sprint 9

---

*Created after 16-persona strategic audit. Validates before building.*
