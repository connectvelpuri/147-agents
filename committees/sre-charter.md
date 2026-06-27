# Standing Committee 4: SRE & Operations Charter

**Governed by:** Constitution Article VII
**Domain:** Deployment, reliability, observability, capacity planning
**Bi-weekly meeting:** Thursday 11:00 UTC

---

## COMMITTEE MANDATE

Ensure Sovereign CRM can be deployed reliably by any sysadmin, operated at scale, and recovered from any failure. Self-hosted must mean "production-ready," not "good luck."

---

## ENVIRONMENT STRATEGY

| Environment | Purpose | Data | Access | Deploy Method |
|-------------|---------|:----:|--------|---------------|
| Local | Developer machine | Seed data | Developer | docker compose |
| Dev | Integration testing | Anonymized prod copy | Dev team | CI auto-deploy |
| QA | Pre-release validation | Anonymized prod (10%) | QA + Dev | Manual promote |
| Staging | Release candidate | Full prod copy (anonymized) | Internal only | Manual promote |
| Production | Live customer data | Real data | Customers | Tagged release |

## RELIABILITY TARGETS

| Metric | Target | Measurement |
|--------|:------:|-------------|
| Availability (uptime) | 99.9% (8.76h downtime/year) | Synthetic monitoring |
| API P95 latency | < 500ms | k6 dashboard |
| API P99 latency | < 2000ms | k6 dashboard |
| Web P95 load time | < 2s | Lighthouse CI |
| Data durability | 99.999999% (no data loss) | WAL + backups |
| Recovery Point Objective (RPO) | < 5 minutes (CDC) | Last synced record |
| Recovery Time Objective (RTO) | < 30 minutes | Restore from backup |
| Deploy frequency | Weekly (Tues 10:00 UTC) | Release tags |
| Deploy success rate | > 99% | CI/CD pipeline |
| Mean Time To Detect (MTTD) | < 5 minutes | Alerting |
| Mean Time To Resolve (MTTR) | < 30 minutes (critical) | Incident response |

## OBSERVABILITY STACK

| Layer | Tool | Purpose |
|-------|------|---------|
| Metrics | Prometheus | System + application metrics |
| Dashboards | Grafana | Visualization + alerting |
| Logs | Loki (or ELK) | Centralized logging |
| Traces | OpenTelemetry | Distributed tracing |
| Alerts | Alertmanager | Notifications (email, Slack, PagerDuty) |
| Synthetic | Checkly / Grafana Synthetic | External uptime monitoring |

### Required Dashboards
1. **Service Health** - CPU, memory, disk, connections per service
2. **API Performance** - P50/P95/P99 latency, error rate, requests per second
3. **Database** - Query performance, connection pool, slow queries, replication lag
4. **Sync Health** - Pending sync count, sync latency, conflict rate
5. **Business Metrics** - Active users, deals created, activities logged (operational)

## UPGRADE STRATEGY

### Zero-Downtime Upgrade Process
1. Health check current state
2. Deploy new API version (rolling update)
3. Run database migrations (backward-compatible)
4. Run data migrations (async, background)
5. Verify health
6. Remove old API pods
7. Deploy new Web version
8. Run post-deploy smoke tests
9. If failure at any step: ROLLBACK (revert to previous tag, apply reverse migration)

### Migration Safety
- All DB migrations must be backward-compatible (no column drops or renames without deprecated period)
- Forward migration + reverse migration paired together
- Large migrations (affecting > 1M rows) run as background jobs, not in-request
- Migration dry-run runs in staging before production

### Rollback Procedure

| Incident | Trigger | Action | RTO |
|----------|---------|--------|:---:|
| Data corruption | Integrity check fails | Restore from latest backup | 30 min |
| Failed deploy | Smoke tests fail post-deploy | Revert to previous Docker tag | 5 min |
| Performance degradation | P95 latency > 2s for 5 min | Scale up pods, investigate | 15 min |

## CAPACITY PLANNING

### Benchmark Reference
| Tier | Users | Records | Postgres | Redis | ClickHouse | RAM | Storage |
|:----:|:-----:|:-------:|:--------:|:-----:|:----------:|:---:|:-------:|
| S | 10 | 10k | 1c, 2GB | 256MB | - | 4GB | 20GB |
| M | 100 | 100k | 2c, 4GB | 512MB | 2GB | 8GB | 50GB |
| L | 1000 | 1M | 4c, 8GB | 1GB | 8GB | 16GB | 200GB |
| XL | 10k | 10M | 8c, 16GB | 2GB | 16GB+r | 32GB | 1TB |
| XXL | 100k | 100M | 16c, 32GB+r | 4GB | Cluster | 64GB+ | 10TB+ |

### Auto-Scaling Rules
- API: CPU > 70% for 5 min -> +1 pod (max 10)
- Database: Connection pool > 80% for 5 min -> alert (not auto-scale)
- Background workers: Queue depth > 1000 for 5 min -> +1 worker (max 5)

## BACKUP STRATEGY

| Backup Type | Frequency | Retention | Location |
|-------------|:---------:|:---------:|:---------:|
| Full database | Daily (02:00 UTC) | 30 days | S3 + local |
| WAL archive | Continuous (every 5 min) | 7 days | S3 |
| Configuration | On every change | 90 days | Git |
| File uploads | Daily | 30 days | S3 |
| Encryption keys | On every rotation | Forever | Vault + offline |

### Backup Verification
- Weekly: Restore backup to staging environment
- Monthly: Run data integrity checks on restored backup
- Quarterly: Full disaster recovery drill (simulate region outage)

## FAILURE SCENARIOS

| Scenario | Detection | Action | RTO |
|----------|-----------|--------|:---:|
| Database corruption | Checksum mismatch | Restore from backup | 30 min |
| Disk full | Monitoring alert | Scale storage, clean WAL | 10 min |
| Region outage | Synthetic monitoring | DNS failover to secondary region | 5 min |
| Queue backlog | Queue depth alert | Scale workers, investigate consumer | 15 min |
| Storage full (uploads) | Monitoring alert | Clean temp files, scale | 10 min |
| Backup failure | Backup job alert | Retry, investigate root cause | 2 hours |
| Search unavailable | Query timeout | Fail to DB fallback, restore index | 15 min |
| Cache failure | Hit rate drops to 0 | Serve from DB, rebuild cache | 5 min |
