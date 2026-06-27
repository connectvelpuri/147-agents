# Standing Committee 5: Testing & Trust Architecture Charter

**Governed by:** Constitution Article VII
**Domain:** Test strategy, chaos engineering, data integrity verification
**Bi-weekly meeting:** Tuesday 11:00 UTC

---

## COMMITTEE MANDATE

Design and enforce the testing architecture that makes Sovereign CRM worthy of trust. Every release must be provably correct — users should never wonder "did my data survive that update?"

---

## TEST PYRAMID (Target Ratios)

```
          /\
         /  \
        / E2E \          5% — Critical path smoke tests
       /   10  \
      /----------\
     /Integration\      25% — API, sync, workflow, migration
    /     50     \
   /----------------\
  /    Unit          \    70% — Models, services, utilities, formulas
 /      140          \
/======================\
    Total: 200 tests minimum per sprint
```

## TEST CATEGORIES

### Unit Tests (70%)
| Area | Coverage Target | Framework |
|------|:--------------:|-----------|
| Data models (Go structs, validation) | 95% | Go testing |
| Business logic (formulas, pipelines, scoring) | 95% | Go testing |
| Utility functions (dates, currencies, strings) | 95% | Go testing |
| Frontend components (individual) | 80% | Jest + Testing Library |
| Reducers / state logic | 90% | Jest |
| Validation rules | 100% of defined rules | Go testing |

### Integration Tests (25%)
| Area | Coverage Target | Framework |
|------|:--------------:|-----------|
| API endpoints (happy path + all 4xx/5xx) | 90% of endpoints | Go httptest |
| Database migrations (forward + reverse) | 100% of migrations | Go testing |
| Workflow engine (trigger -> condition -> action) | 90% of workflow paths | Go testing |
| Sync engine (CRDT merge, conflict resolution) | 95% of sync scenarios | Go testing + deterministic fuzzing |
| Authentication flow (login, MFA, token refresh) | 100% of flows | Go testing |
| Authorization (every CRUD per role) | 100% of role-permission combos | Go testing |
| Email integration (send, receive, track) | 80% | Mocked SMTP |
| Import pipeline (CSV parse -> map -> validate -> load) | 90% | Go testing |
| Webhook delivery (send, retry, sign) | 90% | Go testing |
| Plugin system (load, hook, execute) | 80% | Go testing |

### E2E Tests (5%)
| Critical Path | Test Scenario | Tool |
|---------------|---------------|------|
| User signup to first deal | Sign up -> create org -> create contact -> create deal -> move stage | Playwright |
| Lead to cash (SaaS) | Lead -> qualify -> create subscription -> invoice | Playwright + API |
| Lead to cash (ITC) | Lead -> qualify -> create SOW -> approve -> create engagement -> time entry -> invoice | Playwright + API |
| Offline sync | Create record offline -> go online -> verify synced | Custom test harness |
| Data import | Upload CSV -> map -> import -> verify data | Playwright + API |
| Admin customization | Create dynamic entity -> add fields -> deploy -> verify in UI | Playwright |
| AI query | "Show top 10 deals" -> verify results | API test |
| Role-based access | Create user with limited role -> verify access restrictions | API test |

## SYNC TESTING (CRDT Faithfulness)

This is the highest-risk area. Sync bugs destroy trust.

### Deterministic Test Scenarios
1. Single device, offline -> online — no conflicts
2. Two devices, offline, edit different fields — automatic merge
3. Two devices, offline, edit same field — LWW, log conflict
4. Device A offline for 7 days, Device B makes 50 changes — full sync
5. Network interruption mid-sync — resume without duplication
6. 10 devices, all offline, all editing — convergent state after sync
7. Delete then recreate same record — tombstone handling
8. Sync while user is editing — no data loss

### Chaos Testing Scenarios
1. Random network disconnections at any point
2. Corrupt payloads injected into sync stream
3. Out-of-order delivery of sync messages
4. Duplicate delivery (exactly-once verification)
5. Massive backlog (10,000 pending changes)
6. Clock skew between devices (timezone, drift)
7. Storage full during sync
8. App killed during sync commit

### Data Integrity Verification
Every sync cycle:
1. Checksum calculation per record: SHA256 of all fields
2. Checksum comparison: local vs server
3. Reconciliation report: matched / repaired / lost
4. Daily full reconciliation: compare every record's checksum
5. Alert on any mismatch: "Record #1234 has divergent checksums"

## CHAOS ENGINEERING (Production)

| Experiment | Frequency | Runbook |
|-----------|:---------:|---------|
| Kill API pod (random) | Weekly | Auto-restart by K8s, verify no dropped requests |
| Kill database (read replica) | Weekly | Read traffic fails over to primary |
| Network partition (API <-> DB) | Monthly | Connection pooling saves, queue builds up |
| CPU spike (stress test) | Monthly | Auto-scaling kicks in, P99 latency monitored |
| Disk full (simulate) | Quarterly | Alert fires, cleanup runs, no data loss |
| Offline sync conflict storm | Quarterly | 100 concurrent offline edits -> verify convergence |

## CI/CD TEST ENFORCEMENT

| Gate | Tests Run | Pass Required | Time Budget |
|:----:|-----------|:-------------:|:-----------:|
| Pre-commit | Lint + typecheck + 50% unit tests | Yes | < 2 min |
| PR | All unit + integration tests | Yes | < 10 min |
| Staging deploy | All tests + E2E critical paths | Yes | < 20 min |
| Pre-release | All tests + E2E all + performance benchmarks | Yes | < 30 min |
| Post-release | Smoke tests (10 critical paths) | Yes (monitor) | < 5 min |

## TESTING GLOSSARY (Shared Understanding)

| Term | Definition |
|------|------------|
| Unit test | Tests a single function/component in isolation. Mocks all dependencies. |
| Integration test | Tests a real interaction between 2+ components. Real DB, real API. |
| E2E test | Tests a complete user scenario. Browser + API + DB. Full stack. |
| Smoke test | Quick check that the system is running. Not exhaustive. |
| Deterministic test | Same input -> same output every time. No randomness. |
| Fuzz test | Random inputs to find edge cases and crashes. |
| Chaos test | Intentionally break things in production to verify resilience. |
| Data integrity test | Verify that data is not corrupted by operations (sync, migration, backup). |
