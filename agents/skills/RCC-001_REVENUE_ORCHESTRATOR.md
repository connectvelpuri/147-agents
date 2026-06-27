# RCC-001 Skill: Revenue Orchestrator

## Framework: Stage-Based Agent Routing

### Stage 1: Awareness → SDR-001 + SDR-002
- SDR-001 identifies target accounts
- SDR-002 monitors intent signals
- No outreach until intent threshold met
- Warm-up content via MO-002 sentiment monitoring

### Stage 2: Interest → SDR-003 + SDR-002
- SDR-003 generates initial outreach (BTL)
- SDR-002 tracks engagement signals
- MO-002 monitors response sentiment
- If BTL engagement → transition to ATL

### Stage 3: Consideration → SDR-003 + QL-001 + MO-003
- SDR-003 continues sequence (ATL, Give-Get)
- QL-001 scores prospect against L1-L2-L3
- MO-003 detects objections in responses
- Escalate to MO-003 when objection confidence > 0.7

### Stage 4: Evaluation → QL-001 + MO-003 + MO-004
- QL-001 scored L2 (100+) → deeper qualification
- MO-003 classifies objections by bucket
- MO-004 tracks commitments made on calls/emails
- Route objections to SDR-003 for reframing

### Stage 5: Decision → QL-001 + MO-004 + Close
- QL-001 scored L3 (200+) → buying-ready
- MO-004 tracks commitment escalation (L0→L5)
- If stalled at L3+ → MO-003 analyzes fear
- Route to close with complete qualification package

## DAG Routing Matrix

| Signal | Agent(s) | Priority | Timeframe |
|--------|----------|----------|-----------|
| Intent signal (BTL) | SDR-002 | Medium | 24h |
| Intent signal (ATL) | SDR-002 → SDR-001 | High | 1h |
| Prospect replied | MO-002 → MO-003 | High | 15min |
| Objection detected | MO-003 → SDR-003 | High | 1h |
| Reply rate < threshold | SDR-003 (A/B test) | Medium | Weekly |
| Sentiment shift | MO-002 → alert | Medium | Real-time |
| Commitment made | MO-004 → track | Low | Per interaction |
| Commitment stalled | MO-004 → MO-003 | Low | 7 days |
| L3 qualified | QL-001 → Close | High | Immediate |
| L2 qualified | QL-001 → Sales | High | 24h |
| L1 disqualified | QL-001 → Nurture | Low | Batch |

## Framework: Give-Get (Miller) — Cross-Agent
- Every agent handoff must articulate: what was GIVEN and what was GET from the last interaction
- SDR-003 gives value → tracks reply (GET)
- QL-001 gives qualification insight → tracks commitment (GET)
- MO-003 gives objection resolution → tracks language shift (GET)
- If handoff doesn't have a clear GET, don't hand off yet

## Framework: 5 Fears Mapping (Andy Paul) by Agent

| Fear | Primary Agent | Response |
|------|--------------|----------|
| Fear of Mistake | QL-001 | Risk reversal evidence |
| Fear of Change | SDR-003 | Status quo as risk, loss aversion |
| Fear of Losing Credibility | MO-003 | Peer proof, CBT validation |
| Fear of Commitment | MO-004 | Micro-commitments, clear timeline |
| Fear of Unknown | SDR-003 | Over-communicate, transparency |

## Hard Truths (Burns/Weiss)
- Most pipeline dies because agents work in silos, not as a system
- A handoff without context is a dead lead
- The system should route, not decide — humans decide
- If SDR-002 isn't detecting signals, SDR-003 is flying blind
- If MO-003 isn't classifying objections, SDR-003 can't adapt
- The orchestrator is only as good as its weakest agent
