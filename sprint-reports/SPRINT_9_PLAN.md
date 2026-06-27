# Sprint 9: AI Copilot Deep Integration — Plan

**Date:** 2026-06-09
**Priority:** P1
**Status:** In Progress

---

## Objective

Transform the basic chat-based AI from Sprint 5 into a context-aware Copilot that's embedded across the entire CRM. Connect the AI assistant to the 19 MCP tools so it can read and write CRM data directly.

---

## 9.1 — AI MCP Bridge

**File:** `api/internal/ai/mcp_bridge.go` (NEW)

Wraps the MCP server's tool registry so the AI agent can call tools in-process without HTTP.

| Method | Description |
|--------|-------------|
| `NewMCPBridge(*mcp.Server)` | Creates bridge from existing MCP server |
| `GetToolDefinitions()` | Returns tools in OpenAI function-calling format |
| `ExecuteTool(name, args, ctx, userID, tenantID)` | Calls tool function directly |

## 9.2 — Enhanced Agent Engine

**File:** `api/internal/ai/agent_engine.go` (MODIFIED)

Add tool-calling loop (ReAct pattern):

```
User message
  -> LLM (with tool definitions)
  -> LLM returns: reply or tool_call
  -> If tool_call: execute via MCP bridge, feed result back to LLM
  -> LLM returns final reply with tool results incorporated
```

Also accepts optional `page_context` so AI knows which entity/record the user is viewing.

## 9.3 — Copilot Handler

**File:** `api/internal/handlers/copilot.go` (NEW)

REST endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/copilot` | Chat with page context + MCP tool access |
| GET | `/api/ai/copilot/tools` | List available MCP tools |

## 9.4 — Copilot Sidebar

**File:** `web/components/CopilotSidebar.tsx` (NEW)

Floating chat panel that:
- Slides in from right side of any page
- Reads page URL + metadata to determine context
- Supports markdown rendering in responses
- Shows typing indicator during AI processing
- Collapsible / expandable

## 9.5 — Layout Integration

**File:** `web/app/layout.tsx` (MODIFIED)

Add `<CopilotSidebar />` to provide a copilot button/panel available from every page.

---

## Tool Inventory (19 MCP tools available to Copilot)

| Category | Tools |
|----------|-------|
| **Contacts** | list_contacts, get_contact, create_contact |
| **Deals** | list_deals, get_deal, update_deal_stage |
| **Leads** | list_leads |
| **Pipeline** | get_pipeline_summary |
| **Forecast** | get_deal_forecast |
| **Dashboard** | get_dashboard_summary |
| **Activities** | list_activities |
| **Organizations** | list_organizations |
| **Search** | search_crm |
| **Dynamic Objects** | list_dynamic_object_types, get_dynamic_object_type, list_dynamic_records, get_dynamic_record, create_dynamic_record, search_dynamic_records |

---

## Compilation Verification

All Go code must pass `go build ./cmd/server/` before delivery.
