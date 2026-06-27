# Phase 11: AI & Agent Architecture

**Created:** 2026-06-06
**Purpose:** Complete AI integration strategy — MCP server, agents, RAG, model management, permissions. The AI layer that makes Sovereign CRM intelligent.

---

## 0. DESIGN PRINCIPLES

| Principle | Rationale |
|-----------|-----------|
| **Local-first AI** | Self-hosted customers use Ollama. No data leaves their network. |
| **MCP-native** | Every CRM operation is an MCP tool. Any MCP client can control the CRM. |
| **Human-in-the-loop** for destructive actions | AI reads freely. AI writes with approval for delete/merge/bulk. |
| **Permission-gated** | AI tools respect RBAC. AI cannot do what the user cannot do. |
| **BYO Model** | Bring your own LLM (Ollama, OpenAI, Anthropic, etc.). No vendor lock. |
| **Auditable** | Every AI action logged. Every AI suggestion tracked. |

---

## 1. MCP (Model Context Protocol) SERVER

Sovereign CRM implements an MCP server that exposes every CRM operation as a tool.

### MCP Tool Catalog

| Tool Name | Description | Permission Required | Destructive? |
|-----------|-------------|-------------------|:-----------:|
| crm_search | Search across all entities | View access on entity | NO |
| crm_get_record | Get single record by ID | View access on entity | NO |
| crm_query | Query records with filters | View access on entity | NO |
| crm_create_record | Create a record | Create permission | NO |
| crm_update_record | Update a record | Edit permission | NO |
| crm_delete_record | Soft-delete a record | Delete permission | YES |
| crm_merge_records | Merge two records | Edit permission on both | YES |
| crm_bulk_update | Bulk update (up to 50) | Bulk edit permission | NO |
| crm_create_report | Generate report from NL | Create report permission | NO |
| crm_get_insight | AI analysis of data | View + AI permission | NO |
| crm_execute_workflow | Trigger a workflow | Admin permission | NO |
| crm_get_forecast | Current forecast data | View forecast permission | NO |
| crm_list_activities | Activity timeline | View activity permission | NO |
| crm_send_email | Send email via CRM | Send email permission | NO |
| crm_schedule_meeting | Create calendar event | Calendar permission | NO |
| crm_export_data | Export to CSV | Export permission | NO |

### Tool Definition Example (MCP format)
```json
{
  "name": "crm_create_record",
  "description": "Create a new record in any entity type",
  "input_schema": {
    "type": "object",
    "properties": {
      "entity_type": {
        "type": "string",
        "description": "Entity API name (e.g., Contact, Deal, Engagement__c)"
      },
      "data": {
        "type": "object",
        "description": "Field name → value pairs"
      }
    },
    "required": ["entity_type", "data"]
  }
}
```

---

## 2. AI ASSISTANT (Chat Interface)

### Capabilities

| Capability | Example |
|------------|---------|
| **Natural Language Query** | "Show me all deals over $100k that haven't had activity in 2 weeks" |
| **Natural Language Action** | "Create a follow-up task for John to call Acme Corp tomorrow at 10am" |
| **Report Generation** | "Show me win rate by rep this quarter as a bar chart" |
| **Context-Aware** | (On deal page) "What's the risk on this deal?" → AI inspects current deal |
| **Multi-turn** | Follow-up: "Which of those have the highest probability?" |
| **Entity Creation** | "Create a new Engagement for Acme Corp with a $200k budget" |

### Query Parsing Pipeline

```
User: "Show me deals over 50k that are stale"

1. NLU: Intent = query, Entity = deal, Filters = {amount > 50000, stale = true}
2. Context: What does "stale" mean? → no activity in 7+ days
3. Query Builder: SELECT * FROM deals WHERE amount > 50000 AND last_activity_date < NOW() - 7
4. Permission Check: Does user have view access on deals?
5. Execute → Return formatted results
6. Follow-up: "Which of those are close to closing?" → same session context
```

### AI Assistant Prompt Template
```
You are the Sovereign CRM AI Assistant. You help users manage their CRM data.

RULES:
- You can READ any data the user has permission to view
- You can WRITE (create/update) with the user's permission level
- You CANNOT delete or merge records without explicit user confirmation
- Always cite the record ID when referencing specific records
- When unsure, ask the user for clarification
- Never guess field names — use the entity metadata

Current context:
  Tenant: {tenant_name}
  User: {user_name}
  Role: {user_role}
  Current page: {entity_type}:{entity_id} (if on record page)

Available entities: {entity_list}
```

---

## 3. AI INSIGHTS ENGINE

### Insight Types

| Insight | Trigger | Output | Persona |
|---------|---------|--------|---------|
| Deal Risk | Deal stale > 7 days | "Acme Corp deal hasn't had activity in 12 days. The contact Jane hasn't been reached. Risk: HIGH" | AE, Manager |
| Pipeline Health | Weekly scan | "3 deals in Negotiation stage have been there > 30 days. 2 of them are over $100k." | Manager, VP |
| Rep Activity | Daily scan | "Sarah made 8 calls yesterday vs her average of 15. She's behind this week." | Manager |
| Data Quality | Weekly scan | "42 contacts missing email. 15 deals missing close date. 8 leads from last week unconverted." | Admin, RevOps |
| Forecast Bias | Pre-forecast | "Rep A's commit deals historically close at 72%. His commit is $500k → expected $360k." | VP, CRO |
| Win/Loss Trends | Monthly | "Deals over $100k are 2x more likely to win with a technical champion present." | CRO, Manager |
| Expansion Signal | Real-time | "Acme Corp usage up 40% this month. Their subscription renews in 90 days. Expansion opportunity." | CSM |

### AI Insight Engine Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    SCHEDULER (cron)                          │
│  Daily at 6am │ Weekly Monday │ Monthly 1st │ Real-time      │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    INSIGHT GENERATOR                          │
│                                                              │
│  Rule Engine: "Deal stale > 7d AND stage != Closed Lost"      │
│  ML Model: Churn prediction from historical patterns          │
│  Anomaly Detection: Statistical deviation from baseline       │
│  NLG: Template-based insight narrative                        │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    DELIVERY                                   │
│                                                              │
│  In-app notification │ Email digest │ Dashboard widget        │
│  Push mobile │ Slack bot │ Webhook to external               │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. AI CRM ADMINISTRATOR (Autonomous Agent)

### Capabilities (Phase 2 of AI — Sprint 6+)

| Capability | Prompt | Tech |
|------------|--------|------|
| Data Cleanup | "Find and merge contacts with duplicate emails" | MCP tools + fuzzy matching |
| Workflow Creation | "Create a workflow: when deal stage = Closed Won, set Won Date = today" | NL → workflow builder API |
| Report Building | "Build a dashboard showing pipeline, forecast, and team activity" | NL → report builder API |
| Import Management | "Import this CSV and map the columns" | NL → import wizard API |
| Permission Audit | "Find users with admin access who haven't logged in for 90 days" | Query tools |
| Data Enrichment | "Auto-fill company info for all organizations missing website" | API enrichment tools |

### Agent Architecture (ReAct pattern)

```
User: "Merge duplicate contacts for John Smith"
  ↓
Agent: Thought → I need to find contacts named John Smith
  ↓
Tool: crm_search(query="John Smith", entity="Contact")
  ↓
Result: 3 contacts found
  ↓
Agent: Thought → These look like duplicates. Same email domain, similar names.
  ↓
Tool: crm_get_record(123), crm_get_record(456), crm_get_record(789)
  ↓
Result: 3 records with same email domain, 2 with exact same company
  ↓
Agent: Asking user → "I found 3 similar contacts. Should I merge them?"
  ↓
User: "Yes, merge them, keep the one with the most complete data"
  ↓
Tool: crm_merge_records(primary=456, secondary=[123, 789])
  ↓
Result: Merge successful. Audit logged.
  ↓
Agent: "Done. Merged 3 contacts into 1. Kept record #456 as primary."
```

---

## 5. RAG (Retrieval Augmented Generation)

### Use Cases
- **Knowledge Base Q&A**: "How do I create a custom field?" → Search KB → Answer
- **Deal Similarity Search**: "Find deals like this one" → Vector search → Similar deals
- **Email Drafting**: "Draft an email to Jane about the proposal" → Search deal context → Draft

### RAG Pipeline
```
User Query
    │
    ▼
┌──────────────┐
│ Query        │
│ Embedding    │  (Ollama embedding model or OpenAI ADA)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Vector DB    │
│ (pgvector)   │  Cosine similarity search
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Context      │  Top-K results → context window
│ Assembly     │  Max tokens: 8000
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ LLM          │  Generate answer with context
│ Response     │
└──────────────┘
```

### Embedding Strategy
- **Entity records**: Encode as text blobs: `"Contact: John Doe, Acme Corp, VP Engineering, j@acme.com..."`
- **Knowledge base articles**: Full text embedding
- **Activity/notes**: Per-entry embedding
- **Update frequency**: On create/update → re-embed. Batch re-index nightly.

---

## 6. MODEL MANAGEMENT

### Supported Providers

| Provider | Models | Use Case | Self-Hosted? |
|----------|--------|----------|:------------:|
| Ollama | Llama 3, Mistral, Qwen, DeepSeek, etc. | General AI, chat, insights | ✅ YES |
| OpenAI | GPT-4o, GPT-4o-mini | High-quality chat, complex reasoning | ❌ Cloud |
| Anthropic | Claude Sonnet 4, Haiku | Code, analysis | ❌ Cloud |
| Custom | Any OpenAI-compatible API | BYO model | ✅ Configurable |

### Model Selection Strategy

| Task | Recommended Model | Fallback |
|------|-------------------|----------|
| Quick queries (NL→SQL) | Llama 3.1 8B (Ollama) | GPT-4o-mini |
| Complex analysis | Llama 3.3 70B / DeepSeek | Claude Sonnet |
| Insight generation | DeepSeek / Qwen 32B | GPT-4o |
| Email drafting | Llama 3.1 8B | Claude Haiku |
| Embeddings | nomic-embed-text / bge | OpenAI ADA |
| Autonomous agent | GPT-4o / Claude Sonnet | DeepSeek |
| Code/workflow gen | Claude Sonnet | GPT-4o |

### Configuration Example (tenant settings)
```yaml
ai:
  assistant_model:
    provider: ollama
    model: llama3.1:70b
    endpoint: http://localhost:11434
    context_window: 8192
  embeddings_model:
    provider: ollama
    model: nomic-embed-text
  insight_model:
    provider: ollama
    model: deepseek-r1:32b
  agent_model:
    provider: openai
    model: gpt-4o
    api_key: ${OPENAI_API_KEY}
```

---

## 7. AI PERMISSION MODEL

| Permission | Default | Description |
|------------|:-------:|-------------|
| AI Chat Access | All users | Can use AI assistant |
| AI Insights View | All users | Can see AI-generated insights |
| AI Action Execute | Manager+ | Can execute AI actions (create/update) |
| AI Destructive Action | Admin only | Can execute merge/delete via AI |
| AI Configure | Admin only | Can change AI model settings |
| AI Audit View | Admin only | Can see AI action logs |

---

## 8. AI GOVERNANCE

| Concern | Control |
|---------|---------|
| Hallucination | All AI responses include "AI-generated" disclaimer. Factual claims cite record IDs. |
| Destructive actions | Confirmation dialog for delete/merge. Rollback available for 24h. |
| Data leakage | With self-hosted Ollama, data never leaves. Cloud models: data anonymization option. |
| Token cost | Usage dashboard per user. Optional monthly cap. |
| Audit trail | Every AI action logged: prompt, response, tool calls, duration. |
| Model freshness | Supported models list updated with security patches. Old models deprecated. |
| Prompt injection | Input sanitization. System prompt hardening. Tool call validation. |

---

*Phase 11 complete. AI architecture covers MCP tools, chat assistant, insights engine, autonomous agent, RAG, model management, and governance. Next: Phase 12 — Security & Permissions Architecture.*
