# Revenue OS — Phased Implementation Roadmap

**Scope:** 80–120 agents across 27 divisions, orchestrated via NATS JetStream + Kubernetes
**Team:** 3–5 engineers
**Timeline:** 24 weeks (6 phases)
**Repository:** `sovereign_crm_vault/`

---

## Contents

1. [Dependency Graph (full)](#dependency-graph)
2. [Phase 0: Foundation](#phase-0-foundation-weeks-1-2)
3. [Phase 1: Core Engine](#phase-1-core-engine-weeks-3-6)
4. [Phase 2: Deal Velocity](#phase-2-deal-velocity-weeks-7-12)
5. [Phase 3: Strategic Enablement](#phase-3-strategic-enablement-weeks-13-18)
6. [Phase 4: Optimization](#phase-4-optimization-weeks-19-24)
7. [Resource Estimates](#resource-estimates)
8. [Testing Strategy](#testing-strategy)
9. [Go/No-Go Gates](#go-no-go-gates)
10. [Team Composition Per Phase](#team-composition-per-phase)

---

## Dependency Graph

```
Phase 1 (MVP)
  revenue-command-center ───────────────────┐
  meeting-observer ─────────────────────────┤
  sdr ──────────────────────────────────────┤
  qualification ────────────────────────────┤
                                            ▼
Phase 2 (Deal Velocity)
  buyer-psychology ─────┐
  value-engineering ────┤
  discovery ────────────┤
  content ──────────────┤
  deal-strategy ────────┤──▶ negotiation ──▶ revenue-ops
  relationship-intel ───┤
  account-intelligence ─┤
  sales-psych-research ─┘
  data-services ────────────────────────────▶ all agents
  customer-success ─────────────────────────▶ (standalone)

Phase 3 (Strategic Enablement)
  executive-advisory ───┐
  partner-alliance ─────┤
  security-compliance ──┤
  delivery-confidence ──┤
  rfp-rfq ──────────────┤──▶ procurement-legal
  knowledge-learning ───┤
  customer-voice ───────┤
  ai-governance ────────┤
  security-privacy ─────┘
  abm ──────────────────────────────────────▶ (standalone)

Phase 4 (Optimization)
  win-loss-analysis ────▶ agent-training-pipeline
  a-b-testing ──────────▶ performance-opt
  all agents ───────────▶ documentation / hardening
```

### Agent dependency table

| Agent | Depends on |
|-------|-----------|
| negotiation | deal-strategy, buyer-psychology |
| revenue-ops | all Phase 2 agents (data inputs) |
| procurement-legal | rfp-rfq, security-compliance |
| agent-training-pipeline | win-loss-analysis, customer-voice |
| qualification | sdr, meeting-observer |
| deal-strategy | discovery, buyer-psychology, value-engineering |

---

## Phase 0: Foundation (Weeks 1–2)

### Start condition

Nothing — this is the starting point. Requires:
- Cloud provider account (AWS/GCP/Azure) with kubectl access
- NATS JetStream license or OSS deployment
- Docker registry credentials
- Git repository with CI/CD runner (GitHub Actions / GitLab CI)

### Tasks

| Area | Deliverable | Owner |
|------|------------|-------|
| **Kubernetes** | Single cluster, 3 node pools (general, GPU, ingress). Helmfile for infra. | DevOps |
| **NATS JetStream** | 3-node cluster, KV + Object store buckets, stream configs per agent class | DevOps + Backend |
| **Observability** | Prometheus + Grafana + Loki + Tempo. Agent-level metrics: latency, token count, error rate per agent_id | DevOps |
| **Agent template** | Base agent class: NATS subscription → LLM call → NATS publish. Retry, timeout, circuit-breaker built in. MCP server client. | Backend |
| **Common libraries** | LLM router (OpenRouter / litellm), embedding cache, CRM connector base (HubSpot/Salesforce), authn/z | Backend |
| **CI/CD** | Build → lint → unit test → container scan → deploy to staging. Approval gate for prod. | DevOps |
| **MCP registry** | Service registry via NATS KV: `mcp.servers.<agent_id>` → `{endpoint, auth, rate_limit}` | Backend |
| **Developer env** | Kind cluster locally, Telepresence for live debugging, `.env` templates | DevOps |

### Milestones

1. `kubectl get pods -A` shows healthy cluster with monitoring stack
2. NATS JetStream `nats str ls` returns configured stream for `agent.test`
3. Base agent compiles, subscribes to `agent.test.in`, publishes to `agent.test.out`
4. CI pipeline builds + deploys a hello-world agent to staging
5. Developer can run `make dev` and hit a local agent with curl

### Validation criteria

- Agent round-trip latency under 500ms (NATS → LLM → NATS)
- CI pipeline completes under 5 minutes
- Logs from all cluster pods appear in Grafana/Loki within 30s

### Risk factors

| Risk | Mitigation |
|------|-----------|
| NATS JetStream misconfiguration | Start with single-node dev cluster, then 3-node prod |
| LLM API key management | Use External Secrets Operator + Vault |
| Team unfamiliar with NATS | Week 1 spike: build one agent end-to-end before scaffolding |

### Rollback plan

- Helmfile `helmfile destroy` tears down entire cluster infra
- Git revert to initial commit restores CI/CD

---

## Phase 1: Core Engine (Weeks 3–6) — 4 MVP Agents

### Start condition

- Phase 0 complete: cluster healthy, NATS streams ready, agent template compiles, CI/CD green
- At least 1 LLM API key configured (OpenRouter / Anthropic / OpenAI)
- CRM sandbox accessible (HubSpot Developer Sandbox or Salesforce Scratch Org)

### Agents to build

| Agent ID | Division | Purpose |
|----------|----------|---------|
| `rev-cmd-center` | Revenue Command Center | Orchestrates all agents via NATS request-reply. Human-in-box dashboard for approvals, overrides, escalations. State machine per deal (stages: prospecting → qualification → discovery → proposal → negotiation → closed). |
| `meeting-observer` | Meeting Intelligence | Real-time transcription (Whisper/Deepgram), speaker diarization, sentiment per segment, action item extraction. Publishes structured events to `meeting.observed`. |
| `sdr` | SDR | Prospecting: company fit scoring, contact enrichment (Clearbit/Apollo-style), email sequence trigger. Publishes leads to `sdr.qualified_lead`. |
| `qualification` | Qualification | MEDDPICC scoring: Metrics, Economic buyer, Decision criteria, Decision process, Paper process, Identify pain, Champion, Competition. Reads `sdr.qualified_lead` + `meeting.observed`. |

### Architecture (Phase 1)

```
CRM webhook ──▶ sdr ──▶ qualification ──▶ rev-cmd-center ──▶ dashboard
                    ↗
meeting-observer ───┘
     ▲
 mic input
```

### Milestones

1. **Week 3:** `meeting-observer` transcribes a 15-min test call, extracts action items. `rev-cmd-center` skeleton subscribes to all agent topics.
2. **Week 4:** `sdr` scores 100 leads from CRM, enriches contacts, publishes scored leads.
3. **Week 5:** `qualification` reads leads + meeting transcripts, outputs MEDDPICC scores. `rev-cmd-center` dashboard shows deal pipeline with scores.
4. **Week 6:** End-to-end demo: CRM webhook → SDR scores → Qualification scores → dashboard updates. Human-in-box override works.

### Validation criteria

| Metric | Target |
|--------|--------|
| Meeting transcription accuracy | >90% WER on clear audio |
| MEDDPICC score consistency | 3 human reviewers agree within 1 point |
| End-to-end latency (lead → score) | <30s p95 |
| SDR lead enrichment coverage | >60% of leads get contact email |
| Human-in-box override acknowledgement | <5s |

### Risk factors

| Risk | Mitigation |
|------|-----------|
| Whisper latency too high for real-time | Use Deepgram streaming API; Whisper as fallback batch processor |
| MEDDPICC scoring too subjective | Start with 5 of 9 criteria; add remaining 4 in Phase 2 |
| CRM API rate limits | Implement circuit breaker + exponential backoff in base agent |
| Human-in-box UI scope creep | Ship MVP dashboard as read-only table with approve/reject buttons only |

### Rollback plan

- `helm rollback` previous release of any agent
- `rev-cmd-center` can be disabled: agents still publish to NATS, but no orchestration
- CRM connector falls back to webhook replay from CRM's own queue

---

## Phase 2: Deal Velocity (Weeks 7–12) — +12 Agents

### Start condition

- Phase 1 agents running in production with 7 days of uptime
- At least 50 real deals flowing through the pipeline
- MEDDPICC scores being logged; accuracy baseline established
- `rev-cmd-center` state machine handling all 6 deal stages

### Agents to build

| Agent ID | Division | Depends on |
|----------|----------|-----------|
| `buyer-psychology` | Buyer Psychology | — (standalone) |
| `value-engineering` | Value Engineering | — (standalone) |
| `discovery` | Discovery | buyer-psychology, value-engineering |
| `content` | Content | discovery |
| `deal-strategy` | Deal Strategy | discovery, buyer-psychology, value-engineering |
| `negotiation` | Negotiation | deal-strategy, buyer-psychology |
| `relationship-intel` | Relationship Intelligence | meeting-observer |
| `revenue-ops` | Revenue Operations | all of Phase 2 (analytics + forecasting) |
| `customer-success` | Customer Success | — (standalone) |
| `account-intelligence` | Account Intelligence | relationship-intel, revenue-ops |
| `data-services` | Data Services | — (foundational: enrichment, normalization, dedup) |
| `sales-psych-research` | Sales Psychology Research | buyer-psychology |

### Milestones

1. **Week 7:** `data-services` online — lead dedup, company normalization, enrichment cache. All Phase 1 agents benefit immediately.
2. **Week 8:** `buyer-psychology` + `value-engineering` scoring active. `discovery` generates structured discovery question sets per deal.
3. **Week 9:** `content` generates personalized email drafts, battle cards, and case study snippets per deal.
4. **Week 10:** `deal-strategy` produces ranked action plans. `negotiation` generates fallback paths, BATNA analysis, concession maps.
5. **Week 11:** `relationship-intel` maps org chart + sentiment heatmap. `account-intelligence` rolls up cross-deal insights.
6. **Week 12:** `revenue-ops` produces forecast with confidence intervals. `customer-success` hooks into closed-won deals. System handles 200+ concurrent deals.

### Validation criteria

| Metric | Target |
|--------|--------|
| Discovery question relevance | 80%+ questions marked "helpful" by reps |
| Content generation acceptance | 60%+ drafts used without major edits |
| Forecast accuracy (30-day) | ±15% of actual |
| Negotiation scenario coverage | >90% of common objection types handled |
| Relationship intel accuracy | Org chart matches CRM >85% |
| Concurrent deal throughput | 200+ without p95 latency >2s |
| Lead enrichment rate | >80% of inbound leads get company + contact data |

### Risk factors

| Risk | Mitigation |
|------|-----------|
| LLM cost explosion (12 new agents) | Per-agent token budget enforced via NATS rate limiter; cache identical LLM calls |
| Content agent generating low-quality output | Human-in-box approval gate; feedback loop (Phase 4 adds training) |
| Forecast model overfitting | Ensemble: ARIMA + Prophet + LLM-based. Cross-validation on hold-out deals |
| Agent-to-agent dependency deadlocks | NATS request timeout + fallback default scores for any downstream agent failure |

### Rollback plan

- Per-agent feature flag in `rev-cmd-center`. Disable any agent independently.
- `revenue-ops` has a fallback mode using simple linear regression (no LLM) for forecast
- `data-services` is the hardest to roll back — pin to previous version, re-run dedup on next batch cycle

---

## Phase 3: Strategic Enablement (Weeks 13–18) — +15 Agents

### Start condition

- Phase 2 agents handling 200+ concurrent deals with stable cost per deal
- Forecast accuracy validated across 3+ months of data
- Reps actively using negotiation + deal strategy outputs (adoption >40%)
- No critical P0 bugs open for >48 hours

### Agents to build

| Agent ID | Division | Depends on |
|----------|----------|-----------|
| `abm` | ABM | account-intelligence, content |
| `procurement-legal` | Procurement/Legal | rfp-rfq, security-compliance |
| `executive-advisory` | Executive Advisory | deal-strategy, account-intelligence |
| `partner-alliance` | Partner/Alliance | discovery, account-intelligence |
| `security-compliance` | Security/Compliance | — (standalone) |
| `delivery-confidence` | Delivery Confidence | value-engineering, discovery |
| `rfp-rfq` | RFP/RFQ | content, knowledge-learning |
| `knowledge-learning` | Knowledge & Learning | — (standalone — ingests docs, wikis, call recordings) |
| `ai-governance` | AI Governance | all agents (monitors prompt quality, bias, drift) |
| `customer-voice` | Customer Voice | customer-success, meeting-observer |
| `security-privacy` | Security & Privacy | — (standalone — PII redaction, data retention) |
| `competitive-intel` | Competitive Intelligence | sales-psych-research, content |
| `channel-ops` | Channel Operations | partner-alliance |
| `territory-planning` | Territory Planning | revenue-ops, account-intelligence |
| `compensation` | Compensation | revenue-ops |

### Milestones

1. **Week 13:** `knowledge-learning` ingests all available docs, past call recordings, product materials. `security-privacy` deploys PII redaction layer for all agents.
2. **Week 14:** `abm` generates account-tiered playbooks. `rfp-rfq` skeleton handles simple RFP questions.
3. **Week 15:** `executive-advisory` produces exec briefing docs per strategic account. `partner-alliance` identifies co-sell opportunities.
4. **Week 16:** `delivery-confidence` scores each deal on delivery risk. `procurement-legal` generates redlines for standard terms.
5. **Week 17:** `customer-voice` aggregates NPS, support tickets, meeting sentiment into per-account health score. `competitive-intel` maintains live competitor battle cards.
6. **Week 18:** `ai-governance` produces weekly drift/bias report. `territory-planning` + `compensation` online for annual planning cycle.

### Validation criteria

| Metric | Target |
|--------|--------|
| RFP auto-response accuracy | >70% first-draft acceptance |
| PII redaction recall | >99.5% (audited weekly) |
| Executive briefing quality | >80% "ready to send" rating by sales management |
| Account health score churn prediction | Detects 60%+ of at-risk accounts 14+ days early |
| AI governance drift detection | Flag score drift >5% within 24h |
| Partner-sourced pipeline | >10% of total pipeline within 2 months |
| Delivery confidence accuracy | Deals scored "high risk" churn at 3x rate of "low risk" |

### Risk factors

| Risk | Mitigation |
|------|-----------|
| RFP agent hallucinating compliance answers | Restrict to retrieval-augmented generation from approved doc corpus only; no free-form reasoning |
| PII redactor missing novel patterns | Weekly audit with test set; human-in-loop for edge cases |
| Agent count strains NATS cluster | Partition by division: `agent.rev-ops.>`, `agent.strategic.>`, `agent.compliance.>` |
| Knowledge ingestion stale | Scheduled daily re-ingestion; version-pinned embeddings |

### Rollback plan

- `ai-governance` and `security-privacy` are mandatory — if they fail, block all agent traffic
- `abm` and `territory-planning` are advisory-only; rollback has zero revenue impact
- `procurement-legal` redlines never auto-send; always gated by human

---

## Phase 4: Optimization (Weeks 19–24) — Remaining Agents + Polish

### Start condition

- All Phase 1–3 agents deployed and stable
- At least 1 quarter of deal data collected (500+ deals)
- Agent cost per deal is tracked and understood
- No active security incidents

### Agents to build (remaining)

| Agent ID | Division | Depends on |
|----------|----------|-----------|
| `win-loss-analysis` | Win/Loss | revenue-ops, customer-voice, deal-strategy |
| `agent-training-pipeline` | Training | win-loss-analysis, customer-voice, knowledge-learning |
| `a-b-testing` | Optimization | revenue-ops, rev-cmd-center |
| `performance-opt` | Performance | all agents (latency monitoring + auto-tuning) |
| `documentation` | Documentation | all agents (auto-generated runbooks, decision logs) |
| `production-hardening` | Hardening | all agents (chaos engineering, failover testing) |

### Milestones

1. **Week 19:** `win-loss-analysis` produces monthly report with root causes by agent-influenced stage.
2. **Week 20:** `agent-training-pipeline` uses win/loss data to fine-tune prompts for negotiation, content, and SDR agents.
3. **Week 21:** `a-b-testing` framework live — randomly splits deals into control/treatment groups per agent configuration.
4. **Week 22:** `performance-opt` auto-tunes batch sizes, LLM model selection per agent, and cache TTLs. Latency improvement measured.
5. **Week 23:** `production-hardening` runs weekly chaos experiments (kill random agent pods, inject NATS latency). `documentation` generates agent runbooks.
6. **Week 24:** Full system audit, final documentation, team handoff, production readiness review.

### Validation criteria

| Metric | Target |
|--------|--------|
| Win/loss classification accuracy | >85% vs human-labeled root causes |
| A/B test statistical significance | Detect 5% lift in conversion within 2 weeks |
| Training pipeline improvement per cycle | >10% reduction in prompt error rate |
| p95 end-to-end latency | <3s (all agents, all stages) |
| Chaos engineering: MTTR after pod kill | <2 min |
| Documentation coverage | 100% of agents have runbook + decision log |

### Risk factors

| Risk | Mitigation |
|------|-----------|
| Agent training loop overfits to recent deals | Hold-out validation set; freeze training if win rate degrades |
| A/B testing leaks between control/treatment | Deals randomly assigned at creation; NATS subjects include experiment ID |
| Chaos engineering causes real customer impact | Run in staging first; production chaos limited to business hours with on-call |
| Documentation stale immediately | Auto-regenerated weekly from agent source; manual review only before release |

### Rollback plan

- A/B test: toggle `experiment_id: control` on any deal reverts to default agent behavior
- Agent training: previous prompt version stored in NATS KV; rollback is a key update
- Chaos: `production-hardening` itself can be disabled; cluster reverts to pre-chaos state
- Full rollback to Phase 3: keep `win-loss-analysis` + `a-b-testing` offline, revert agent prompts

---

## Resource Estimates

### LLM token consumption (estimated)

| Phase | Agents | Tokens/day (all agents) | Monthly cost (GPT-4o pricing) |
|-------|--------|------------------------|-------------------------------|
| 0 | — | — | $0 (no LLM usage) |
| 1 | 4 | 5M–10M | $150–$300 |
| 2 | 16 | 40M–80M | $1,200–$2,400 |
| 3 | 31 | 100M–200M | $3,000–$6,000 |
| 4 | 37 | 120M–250M | $3,600–$7,500 |

*Notes:*
- Token counts assume 50% cache hit rate by Phase 3
- Embedding usage (ADA-002/3-small) adds ~$50–$200/mo
- OpenRouter routing can cut costs 40–60% by using cheaper models for simple tasks
- Budget for 2x in early weeks of each phase (prompt iteration)

### API calls per day

| API | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|-----|---------|---------|---------|---------|
| CRM (HubSpot/Salesforce) | 5K | 20K | 50K | 60K |
| Enrichment (Clearbit) | 2K | 8K | 15K | 18K |
| Transcription (Deepgram) | 50 calls | 200 calls | 400 calls | 500 calls |
| Embeddings | 10K | 50K | 150K | 200K |
| MCP server requests | 1K | 10K | 30K | 40K |

### Storage

| Type | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| NATS KV (config state) | 100MB | 500MB | 2GB | 3GB |
| NATS Object Store (recording, docs) | 10GB | 100GB | 500GB | 750GB |
| Vector DB (embeddings) | 1GB | 10GB | 50GB | 75GB |
| Time-series (metrics) | 5GB | 20GB | 50GB | 60GB |
| Logs | 10GB | 50GB | 150GB | 200GB |

### Kubernetes resources

| Phase | Pods | CPU (total) | Memory (total) | GPU |
|-------|------|-------------|---------------|-----|
| 0 | 15 | 8 cores | 32GB | 0 |
| 1 | 25 | 16 cores | 64GB | 0 |
| 2 | 55 | 40 cores | 160GB | 1 (T4, for Whisper) |
| 3 | 85 | 64 cores | 256GB | 2 (T4) |
| 4 | 100 | 80 cores | 320GB | 2 (T4) |

---

## Testing Strategy

### Per-phase testing matrix

| Phase | Unit tests | Integration tests | Simulation tests | Load tests |
|-------|-----------|-------------------|-----------------|------------|
| 0 | NATS helper, base agent, CI pipeline | Cluster bootstrap, agent deploy | N/A | NATS pub/sub throughput |
| 1 | Each agent (LLM parsing, CRM formatting) | End-to-end deal flow (mock CRM) | 100 synthetic leads scored hourly | 50 concurrent deals |
| 2 | Value scoring, forecast model, content gen | Cross-agent dependency chains | 500-deal Monte Carlo pipeline | 200 concurrent deals |
| 3 | PII regex, RFP template matching, compliance rules | RFP → procurement pipeline | 1000 sensitive docs for PII audit | NATS partition traffic |
| 4 | Agent training loop, A/B stats engine | Chaos experiment + recovery | 30-day historical replay | Full cluster stress |

### Simulation framework

Each agent exposes a `simulate` NATS subject that accepts synthetic input data:

```yaml
# Example: qualification simulation
input: { company: "Acme Corp", industry: "SaaS", arr: "5M", meeting_transcript: "..." }
expected: { meddpicc: { pain: 8, champion: 6, ... } }
```

- 500+ simulation scenarios per release
- Automated regression check: score must not regress >5% per criterion
- Simulation data generated from real deal anonymization

### Chaos engineering (Phase 4)

| Experiment | Frequency | Expected behavior |
|-----------|-----------|-------------------|
| Kill random agent pod | Weekly | Agent respawns, NATS replays unprocessed messages |
| NATS cluster partition | Bi-weekly | Agents buffer locally; replay on reconnection |
| CRM API throttling | Monthly | Circuit breaker opens; queue fills; replay on throttle lift |
| LLM API timeout | Monthly | Fallback response ("unavailable") published |

---

## Go/No-Go Gates

### Gate 0 → Phase 1

- Cluster healthy with monitoring + alerting
- NATS JetStream streams + KV operational
- CI/CD green on `main` branch
- Base agent template compiles and publishes to NATS
- **Decision:** Team lead + DevOps sign-off

### Gate 1 → Phase 2 (end of Week 6)

- Phase 1 agents have 7+ days of production uptime
- End-to-end deal flow demoed with CRM
- MEDDPICC accuracy baseline established (>70% agreement with human reviewers)
- No P1 bugs open
- LLM cost per deal tracked and within budget (±20%)
- **Decision:** Product owner + lead engineer sign-off. Must demo to 2 sales reps for feedback.

### Gate 2 → Phase 3 (end of Week 12)

- 50+ real deals processed end-to-end
- Forecast accuracy within ±15%
- Agent adoption rate >40% (reps using outputs)
- Per-agent cost modeled and predictable
- PII/security audit passed
- **Decision:** CRO/VP Sales + CTO sign-off. Must present adoption metrics.

### Week 12 Checkpoint: Critical Go/No-Go Decision

**When:** End of Phase 2 (Week 12)
**What:** Comprehensive review of system viability

**GO Criteria (ALL must pass):**
1. Fewer than 16 agents running with real production data → HALT Phase 3
2. MEDDPICC score accuracy >70% vs human qualification → if below, retrain before proceeding
3. End-to-end deal latency (lead→qualified) p95 <60s → if above, investigate bottleneck
4. Cost per qualified deal <$50 → if above, optimize before scaling
5. Human override rate <40% for auto-approved actions → if above, tune agent confidence thresholds
6. Real-time transcription latency <10s/chunk → if above, budget GPU nodes

**Process:**
1. Metrics collected automatically by RCC-003 (Performance Dashboard)
2. Report generated by RCC-005 (Deal Slippage Monitor)
3. Review meeting with: Engineering Lead, Sales Domain Expert, PM
4. Decision recorded in: `revenue.prod.system.checkpoint.week_12`

**If HALT:**
- Freeze new agent development
- Dedicate 4 weeks to: fix accuracy, reduce latency, tune thresholds
- Re-evaluate at Week 16
- If still failing at Week 16 → pivot to simpler architecture

**If GO:**
- Proceed to Phase 3 with confidence
- Double agent development velocity
- Begin planning Phase 4 optimizations

### Gate 3 → Phase 4 (end of Week 18)

- All Phase 1–3 agents stable for 30+ days
- 500+ deals in historical data
- Agent cost per deal < 5% of deal ACV
- No critical security findings
- A/B testing framework validated in staging
- **Decision:** CEO/COO + CTO + CRO. Must present ROI analysis.

### Gate 4 → Production Ready (end of Week 24)

- Full system audit passed
- Documentation complete
- On-call runbooks verified
- 30-day production soak with no P0 incidents
- **Decision:** Final production readiness review.

---

## Team Composition Per Phase

### Phase 0 (Weeks 1–2) — 3 people

| Role | Count | Focus |
|------|-------|-------|
| DevOps/Platform | 1 | Kubernetes, NATS, CI/CD, monitoring |
| Backend (senior) | 1 | Agent template, common libs, MCP registry |
| Backend (junior) | 1 | Developer env, Helm charts, documentation |

### Phase 1 (Weeks 3–6) — 4 people

| Role | Count | Focus |
|------|-------|-------|
| Backend (senior) | 1 | rev-cmd-center, orchestrator, state machine |
| Backend | 1 | meeting-observer, SDR, qualification |
| ML Engineer | 1 | Whisper pipeline, MEDDPICC scoring model |
| DevOps/Platform | 1 | Production deploy, monitoring dashboards, alerts |

### Phase 2 (Weeks 7–12) — 5 people

| Role | Count | Focus |
|------|-------|-------|
| Backend (senior) | 1 | data-services, revenue-ops, architecture oversight |
| Backend | 2 | buyer-psychology, value-engineering, discovery, content, deal-strategy, negotiation |
| ML Engineer | 1 | Forecasting model, NLP for relationship intel |
| Sales domain expert | 1 | Defining agent behavior, validating outputs, training data curation |

*Note: Sales domain expert may be part-time (50%).*

### Phase 3 (Weeks 13–18) — 5 people

| Role | Count | Focus |
|------|-------|-------|
| Backend (senior) | 1 | AI governance, security/privacy, architecture |
| Backend | 1 | ABM, partner-alliance, channel-ops |
| ML Engineer | 1 | Knowledge ingestion, RFP agent, voice analytics |
| Security engineer | 1 | PII redaction, compliance audit, security-privacy agent |
| Sales domain expert | 1 | Executive advisory, territory planning, compensation |

### Phase 4 (Weeks 19–24) — 4 people

| Role | Count | Focus |
|------|-------|-------|
| Backend | 1 | Win/loss analysis, training pipeline |
| ML Engineer | 1 | A/B testing stats, agent fine-tuning |
| DevOps/SRE | 1 | Chaos engineering, performance optimization, hardening |
| Tech writer / all | 1 | Documentation, runbooks, handoff materials |

---

## Appendix: Agent Registry Format

Each agent is configured via a YAML manifest in `agents/<agent-id>/manifest.yaml`:

```yaml
id: qualification
division: Qualification
version: 1.0.0
depends_on:
  - sdr
  - meeting-observer
subscribes:
  - subject: agent.sdr.qualified_lead
  - subject: agent.meeting.observed
publishes:
  - subject: agent.qualification.scored
llm:
  model: gpt-4o-mini  # cheap for structured scoring
  max_tokens: 1024
  temperature: 0.1    # deterministic
rate_limit: 100/min
timeout: 30s
circuit_breaker:
  threshold: 5
  recovery: 60s
cache_ttl: 3600
```

All agent manifests live at `agents/registry.yaml` for the agent registry service.

---

## Appendix: NATS Subject Convention

```
agent.<division>.<agent_id>.<action>
├── agent.sdr.qualified_lead      — events
├── agent.qualification.scored     — events
│
├── agent.rev-cmd-center.command   — commands (orchestrator → agent)
├── agent.rev-cmd-center.status    — status updates
│
├── agent.<agent_id>.simulate      — simulation input
├── agent.<agent_id>.train         — training trigger
│
├── mcp.servers.<agent_id>         — MCP registry KV keys
│
└── system.>                       — health, metrics, alerts
```

Streams are partitioned by priority class:

| Stream | Subjects | Retention | Consumers |
|--------|----------|-----------|-----------|
| `agent-events` | `agent.>` | 7 days | Each agent |
| `agent-commands` | `agent.*.command` | 30 days | rev-cmd-center |
| `agent-simulations` | `agent.*.simulate` | 90 days | CI pipeline |
| `system-metrics` | `system.>` | 30 days | Grafana |

---

*End of roadmap. This document should be reviewed and updated after each phase gate.*
