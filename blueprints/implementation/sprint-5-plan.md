# Sprint 5 Execution Plan

**Date:** 2026-06-07
**Theme:** "AI Co-pilot + Insights + Advanced Reports"
**Duration:** 3 weeks
**Prerequisites:** Sprint 4 COMPLETE ✅

---

## Sprint 4 Delivery Audit

### What Was Built (Sprint 4)

| Area | Backend | Frontend | Status |
|------|---------|----------|--------|
| Email Accounts | CRUD handler, routes | Account management page | ✅ Done |
| Email Messages | Send, list, get, star, delete | Inbox page | ✅ Done |
| Email Templates | CRUD handler, routes | (no page yet) | ✅ Backend done |
| IMAP Sync | Background worker (imap_sync.go) | — | ✅ Done |
| SMTP Send | Email sender (smtp_sender.go) | — | ✅ Done |
| Sequences | CRUD handler, routes | Sequences page | ✅ Done |
| Workflows | CRUD handler, routes | (no page yet) | ✅ Backend done |
| Reports | Pipeline/Activity/Email handlers | Reports dashboard | ✅ Done |
| Migration 007 | email_accounts, messages, templates | — | ✅ Applied |
| Migration 008 | sequences, steps, enrollments, workflows, triggers, actions | — | ✅ Applied |

### What's Missing from Sprint 4 (deferred to Sprint 5)

| Gap | Impact | Sprint 5 Task |
|-----|--------|---------------|
| No sequence execution engine | Sequences can be created but don't send emails | Task 1.5 |
| No workflow execution engine | Workflows can be created but don't trigger actions | Task 1.6 |
| No email open/click tracking | Can't measure email engagement | Deferred to Sprint 6 |
| No workflow frontend page | Can't create/edit workflows in UI | Task 3.4 |
| No template frontend page | Can't create/edit templates in UI | Task 3.5 |

### What Sprint 5 Should Cover (from Strategic Plan)

The strategic plan says Sprint 5 = "AI Co-pilot + Email Sequences + Reports".
Since email/sequences/reports were built in Sprint 4, Sprint 5 focuses on:

1. **AI Foundation** (the main differentiator — not yet started)
2. **Sequence + Workflow Execution** (the engines that make them work)
3. **Insights** (deal risk, pipeline health — not yet started)
4. **Advanced Reports** (dashboard builder — basic reports exist)

---

## Sprint 5 Plan

### Week 1: AI Foundation (Days 1-6)

| Day | Task | Deliverable | Est. Hours |
|:---:|------|-------------|:----------:|
| 1 | **Ollama client** | `ai/ollama_client.go` — connect to Ollama API, configurable model/endpoint/provider | 2h |
| 2 | **AI config model** | Migration + Go model for ai_settings (provider, model, api_key, endpoint) | 1.5h |
| 3 | **AI Chat backend** | `ai/chat.go` — NL→Query: user asks question → Ollama generates SQL → execute → return results | 4h |
| 4 | **AI Chat UI** | Chat sidebar component; message history; streaming response display | 3h |
| 5 | **AI Actions backend** | NL→Action: "Create a lead for Acme" → parse intent → validate → execute with confirmation | 4h |
| 6 | **Provider config UI** | Settings page: select Ollama/OpenAI/Anthropic, set model, endpoint, API key | 2h |

**Week 1 Total: ~16.5h**

### Week 2: Sequence/Workflow Execution + Insights (Days 7-12)

| Day | Task | Deliverable | Est. Hours |
|:---:|------|-------------|:----------:|
| 7 | **Sequence executor** | Background worker: pick enrolled contacts, send emails per step schedule, wait logic | 4h |
| 8 | **Sequence enrollment UI** | Enroll contacts from contact list or deal; view enrollment status | 2h |
| 9 | **Workflow executor** | Background worker: evaluate triggers, run conditions, execute actions | 4h |
| 10 | **Deal risk detection** | Engine: stale deals (>14d), stuck stages (>2x avg), amount drops | 3h |
| 11 | **Pipeline health engine** | Bottleneck detection, velocity analysis, stage conversion rates | 3h |
| 12 | **Insight cards UI** | Dashboard widgets: at-risk deals, stale leads, pipeline alerts | 2h |

**Week 2 Total: ~18h**

### Week 3: Advanced Reports + Frontend Polish (Days 13-18)

| Day | Task | Deliverable | Est. Hours |
|:---:|------|-------------|:----------:|
| 13 | **Dashboard builder API** | Widget system: metric card, chart, table, activity feed; save/load layouts | 4h |
| 14 | **Dashboard builder UI** | Drag-drop widget placement; add/remove; resize; save multiple dashboards | 4h |
| 15 | **Workflow frontend** | CRUD page for workflows with trigger/condition/action editor | 3h |
| 16 | **Template frontend** | CRUD page for email templates with merge field preview | 2h |
| 17 | **AI enrichment (basic)** | Auto-fill company/industry from email domain via Ollama | 2h |
| 18 | **Sprint review** | Test all features, document issues, plan Sprint 6 | 2h |

**Week 3 Total: ~17h**

---

## Sprint 5 Acceptance Criteria

### AI
- [ ] Ollama connects and responds to chat
- [ ] AI Chat answers "How many deals are in pipeline?" correctly
- [ ] AI Chat can create a contact via natural language
- [ ] Provider config allows switching Ollama/OpenAI/Anthropic
- [ ] AI enrichment fills company info from email domain

### Sequences + Workflows
- [ ] Sequence sends multi-step email campaign on schedule
- [ ] Workflow triggers on deal stage change and logs action
- [ ] Sequence enrollment UI works from contact list
- [ ] Workflow CRUD page is functional

### Insights
- [ ] Deal risk flags stale deals (>14 days, no activity)
- [ ] Pipeline health shows bottleneck stages
- [ ] Dashboard shows insight cards with actionable items

### Reports
- [ ] Dashboard builder creates layout with 2+ widget types
- [ ] Saved dashboards persist and load on page visit
- [ ] Reports page shows drill-down from summary to list view

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Ollama not installed / model too large | Medium | High | Test with smallest model first; graceful fallback message |
| AI generates bad SQL | Medium | Medium | Sandboxed query execution; read-only queries by default |
| Sequence timing unreliable | Low | Medium | Use cron-based scheduler; test with short delays |
| Too many tasks for 3 weeks | Medium | High | Priority: AI > Sequences > Workflows > Reports. Cut if needed |

---

## Files to Create/Modify

### New Backend Files
- `api/internal/ai/ollama_client.go` — Ollama HTTP client
- `api/internal/ai/chat.go` — AI chat orchestrator (NL→Query, NL→Action)
- `api/internal/ai/enrichment.go` — Email domain enrichment
- `api/internal/handlers/ai_chat.go` — Chat API handler
- `api/internal/handlers/ai_config.go` — Provider config handler
- `api/internal/handlers/dashboards.go` — Dashboard builder handler
- `api/internal/handlers/insights.go` — Deal risk + pipeline health handler
- `api/internal/sequences/executor.go` — Background sequence worker
- `api/internal/workflows/executor.go` — Background workflow worker
- `api/internal/database/migrations/009_ai_and_dashboards.sql`

### New Frontend Files
- `web/app/ai/chat/page.tsx` — AI chat page
- `web/app/workflows/page.tsx` — Workflow management page
- `web/app/email/templates/page.tsx` — Template management page
- `web/app/settings/ai/page.tsx` — AI provider config page
- `web/components/ai/chat-sidebar.tsx` — Chat widget component
- `web/components/dashboard/widget-grid.tsx` — Dashboard builder widget

### Modified Files
- `api/cmd/server/main.go` — Register new routes
- `web/components/layout/sidebar.tsx` — Add new nav items
