# ELO Cross-Domain Sync Automation V2.0

**Status:** COMPLETE (9.5+)
**Purpose:** Automated knowledge synchronization between domain agents

## Sync Triggers

| Trigger | Event | Action | Latency Target |
|---------|-------|--------|----------------|
| Cycle completion | Domain finishes cycle | Push summary to knowledge store | <60s |
| Quality score change | Delta > 5 pts | Broadcast to all T2+T1 | <30s |
| Gaming flag | New critical flag | Sync to security domain | <10s |
| Content update | New content published | Notify consuming domains | <120s |
| Agent state change | Agent enters/exits system | Update domain roster | <60s |
| Daily sync | Scheduled 06:00 IST | Full cross-domain reconciliation | <5min |

## Sync Protocol
1. Source domain identifies change
2. Creates sync message (protocol version 2.0)
3. Publishes to shared knowledge store with checksum
4. Target domains poll or subscribe
5. Each target validates checksum, applies delta
6. ACK sent back to source (failures logged for daily reconciliation)
7. Daily full reconciliation catches missed deltas

## Conflict Resolution

| Conflict Type | Resolution Strategy |
|---------------|-------------------|
| Same metric, different values | Latest timestamp wins (with audit log) |
| Concurrent content updates | Domain-owner priority (T2>self, T1>T2) |
| Contradictory agent status | T1 tiebreaker with timeout |
| Schema version mismatch | Backward-compatible serialization (v1->v2) |
