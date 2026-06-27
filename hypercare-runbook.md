# Hypercare Runbook — Post-Deployment Support

**Duration:** 5 business days after go-live
**Team:** Eng + Support (at least 2 people on rotation)
**Channel:** #hypercare-sovereign (Slack/Discord)

---

## Day 1-2: Stabilization

### Priorities (in order)
1. **Data integrity** — Verify all migrated data is accessible
2. **Login/Auth** — Every user can log in
3. **Core workflows** — Contacts, pipeline, reports function correctly
4. **Performance** — Response times within SLOs

### Cadence
- **Morning standup** (15 min): Issues discovered overnight, today's priorities
- **Mid-day check** (30 min): Progress on blockers
- **End-of-day debrief** (15 min): Status update + next day plan

### Running the War Room
```python
# Daily check script
def run_daily_checks():
    checks = {
        "All users can login": test_login_sample(users_random_10),
        "DB connection pool <80%": check_db_pool_usage(),
        "API error rate <1%": check_error_rate_last_1h(),
        "No 5xx errors": check_5xx_count(),
        "Response time p95 <500ms": check_p95_latency(),
    }
    for name, passed in checks.items():
        log(f"{'PASS' if passed else 'FAIL'}: {name}")
```

### Severity Definitions

| Severity | Definition | Response Time | Escalation |
|:--------:|------------|:-------------:|------------|
| **S0** | System down, data loss, security breach | <15 min | Founder + Eng Lead |
| **S1** | Major feature broken, >10% users affected | <1 hour | Eng Lead |
| **S2** | Feature partially broken, workaround exists | <4 hours | On-call Engineer |
| **S3** | Minor issue, cosmetic, no work impact | <24 hours | Normal backlog |
| **S4** | Improvement request | Next sprint | PM |

## Day 3-5: Monitoring & Handoff

### Day 3
- Begin user acceptance verification (5 power users)
- Document workarounds found during Hypercare
- Identify any training gaps (users asking basic questions = need better docs)
- Update runbook with lessons learned

### Day 4
- Review errors: categorize by root cause (data issue / code bug / config / user error)
- Patch quick fixes (S0-S1 only)
- Defer S2-S3 issues to normal sprint planning
- Measure adoption metrics against targets

### Day 5
- Final hypercare report
- Handoff to BAU (Business as Usual) support
- Schedule post-mortem (within 1 week)
- Archive hypercare channel

## Hypercare Exit Criteria

Before ending hypercare, ALL must be true:
- [ ] All S0 and S1 issues resolved
- [ ] Data integrity confirmed (automated checks pass)
- [ ] All target users can login and perform their core workflow
- [ ] Error rate <0.1% for 24 consecutive hours
- [ ] Response times within SLOs (p95 <500ms)
- [ ] Known issues documented with assigned sprint
- [ ] Support knowledge base updated with common resolutions
- [ ] Post-mortem scheduled

## Runbook Templates

### Common Issue: User Can't Login
```
1. Check user exists in users table: SELECT * FROM users WHERE email = '...'
2. Check user is active: status = 'active'
3. Check user has role: SELECT * FROM user_roles WHERE user_id = '...'
4. Check tenant is active: SELECT status FROM tenants WHERE id = '...'
5. Try password reset: PUT /auth/password-reset-request
6. Check rate limiting: SELECT * FROM login_attempts WHERE email = '...' AND created_at > NOW() - INTERVAL '15 minutes'
```

### Common Issue: Data Missing After Migration
```
1. Check source vs target count: SELECT COUNT(*) FROM contacts vs CSV row count
2. Check for deleted_at IS NULL filter (soft delete)
3. Check tenant_id matches: SELECT DISTINCT tenant_id FROM contacts
4. Verify import audit log: SELECT * FROM audit_logs WHERE action = 'contacts.imported'
5. Check import errors: look for "skipped" rows in import result
6. If needed: re-import only missing records via CSV (check for duplicates first)
```

### Common Issue: Performance Slow
```
1. Check DB connection pool: SELECT count(*) FROM pg_stat_activity
2. Check slow queries: SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10
3. Check missing indexes: SELECT * FROM pg_stat_all_indexes WHERE idx_scan = 0
4. Check cache hit ratio: SELECT sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read),0) * 100 FROM pg_statio_user_tables
5. Check CPU/memory: docker stats or htop
6. If long-running query: EXPLAIN ANALYZE the slow query
```

## Communication Templates

### Hypercare Status Update
```
== Hypercare Status: Day [1-5] ==
Status: 🟢/🟡/🔴
New issues today: [N]
Resolved today: [N]
Active S0/S1: [N] — [details]
Active S2/S3: [N] — [details]
Adoption: [X]% DAU of registered users
Next actions: [ ]
```
