# PART 4 — MEMORY IMPLEMENTATION ARCHITECTURE

**Document:** Enterprise Agentic CRM Delivery Operating System  
**Section:** Part 4 — Memory Implementation Architecture  
**Classification:** INTERNAL — DO NOT PUSH TO GIT

---

## 1. MEMORY LAYER ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                     MEMORY LAYER ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    AGENT LAYER                           │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Working  │ │ Episodic │ │ Semantic │ │Procedural│  │   │
│  │  │ Memory   │ │ Memory   │ │ Memory   │ │ Memory   │  │   │
│  │  │(current  │ │(past     │ │(general  │ │(learned  │  │   │
│  │  │ task)    │ │ events)  │ │ facts)   │ │ workflows)│  │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │   │
│  └───────┼────────────┼────────────┼────────────┼─────────┘   │
│          │            │            │            │              │
│  ┌───────▼────────────▼────────────▼────────────▼─────────┐   │
│  │                  MEMORY SERVICES                        │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────────┐     │   │
│  │  │  Mem0      │ │  Zep/      │ │  LangMem       │     │   │
│  │  │ (universal │ │  Graphiti  │ │  (LangGraph    │     │   │
│  │  │  memory)   │ │  (temporal │ │   memory)      │     │   │
│  │  │            │ │   graph)   │ │                │     │   │
│  │  └─────┬──────┘ └─────┬──────┘ └───────┬────────┘     │   │
│  └────────┼──────────────┼────────────────┼───────────────┘   │
│           │              │                │                   │
│  ┌────────▼──────────────▼────────────────▼───────────────┐   │
│  │                  STORAGE LAYER                          │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────────┐     │   │
│  │  │  PostgreSQL │ │   Redis    │ │  Neo4j          │     │   │
│  │  │  (structured│ │  (session  │ │  (knowledge     │     │   │
│  │  │   data)     │ │   cache)   │ │   graph)        │     │   │
│  │  └────────────┘ └────────────┘ └────────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. MEMORY TYPES DEFINITION

### 2.1 Working Memory

```yaml
working_memory:
  purpose: "Current task context — ephemeral, high-frequency access"
  scope: "Single agent, single task"
  lifetime: "Task duration (minutes to hours)"
  storage: "In-process memory (agent context window)"
  
  contents:
    - "Current task description"
    - "Acceptance criteria"
    - "Relevant code snippets"
    - "Recent tool outputs"
    - "Intermediate results"
  
  size_limit: "100KB (context window budget)"
  
  access_pattern:
    read: "continuous"
    write: "continuous"
    evict: "task_completion"
  
  implementation:
    type: "in_memory_map"
    structure:
      task_id: "string"
      task_description: "string"
      acceptance_criteria: "list[string]"
      code_context: "string"
      tool_outputs: "list[dict]"
      intermediate_results: "dict"
      metadata: "dict"
```

### 2.2 Episodic Memory

```yaml
episodic_memory:
  purpose: "Past experiences — what happened, when, and why"
  scope: "Per-agent, cross-task"
  lifetime: "Indefinite (with retention policy)"
  storage: "PostgreSQL + Redis cache"
  
  contents:
    - "Task completion records"
    - "Decision records"
    - "Error records"
    - "Lesson learned records"
    - "Performance records"
  
  retention_policy:
    keep_forever:
      - "Critical decisions (Tier 1 ADRs)"
      - "Security incidents"
      - "Architecture decisions"
    
    keep_1_year:
      - "Task completions"
      - "Performance metrics"
      - "Lesson learned"
    
    keep_90_days:
      - "Routine task records"
      - "Debugging sessions"
      - "Meeting notes"
    
    evict_after_30_days:
      - "Intermediate results"
      - "Working memory snapshots"
  
  access_pattern:
    read: "on_demand"
    write: "task_completion"
    evict: "retention_policy"
  
  implementation:
    table: "episodic_memory"
    columns:
      id: "UUID PRIMARY KEY"
      agent_id: "VARCHAR(50)"
      episode_type: "VARCHAR(50)"
      title: "VARCHAR(255)"
      description: "TEXT"
      context: "JSONB"
      outcome: "VARCHAR(50)"
      lessons_learned: "TEXT"
      created_at: "TIMESTAMP"
      expires_at: "TIMESTAMP"
      metadata: "JSONB"
    
    indexes:
      - "agent_id + created_at"
      - "episode_type + created_at"
      - "expires_at"
```

### 2.3 Semantic Memory

```yaml
semantic_memory:
  purpose: "General knowledge — facts, patterns, conventions"
  scope: "Shared across all agents"
  lifetime: "Indefinite"
  storage: "Knowledge Graph (Neo4j) + Vector DB (Qdrant)"
  
  contents:
    - "CRM domain knowledge"
    - "Technical conventions"
    - "Architecture patterns"
    - "Best practices"
    - "Industry knowledge"
  
  categories:
    domain_knowledge:
      description: "CRM-specific knowledge"
      examples: ["Contact management patterns", "Deal pipeline stages"]
      source: "Manual curation + agent updates"
    
    technical_knowledge:
      description: "Technical patterns and conventions"
      examples: ["Go patterns", "Next.js patterns", "PostgreSQL patterns"]
      source: "Code analysis + manual curation"
    
    business_knowledge:
      description: "Business rules and processes"
      examples: ["Pricing rules", "Workflow triggers"]
      source: "Product team + manual curation"
    
    market_knowledge:
      description: "Market and competitive intelligence"
      examples: ["Competitor features", "Industry trends"]
      source: "Market Intelligence Agent"
  
  access_pattern:
    read: "frequent (every agent turn)"
    write: "daily (Knowledge Graph updates)"
    evict: "never (append-only)"
  
  implementation:
    graph_store: "Neo4j"
    vector_store: "Qdrant"
    sync: "bidirectional"
```

### 2.4 Procedural Memory

```yaml
procedural_memory:
  purpose: "Learned workflows — how to do things"
  scope: "Per-agent, cross-task"
  lifetime: "Indefinite (evolves)"
  storage: "Knowledge Graph + Mem0"
  
  contents:
    - "Successful workflows"
    - "Best practices"
    - "Tool usage patterns"
    - "Error recovery patterns"
    - "Optimization patterns"
  
  structure:
    workflow_pattern:
      name: "string"
      description: "string"
      steps: "list[WorkflowStep]"
      success_rate: "float"
      average_duration: "duration"
      last_used: "timestamp"
      context: "dict"
    
    workflow_step:
      action: "string"
      tool: "string"
      inputs: "dict"
      outputs: "dict"
      conditions: "list[Condition]"
      fallback: "WorkflowStep"
  
  learning_process:
    trigger: "task_completion"
    steps:
      - "Extract workflow from task execution"
      - "Compare with existing patterns"
      - "Update success rates"
      - "Merge similar patterns"
      - "Archive unused patterns"
  
  access_pattern:
    read: "on_task_start"
    write: "on_task_completion"
    evict: "success_rate < 0.3 after 10 uses"
```

---

## 3. MEMORY STORAGE ARCHITECTURE

### 3.1 PostgreSQL Schema

```sql
-- Episodic Memory
CREATE TABLE episodic_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(50) NOT NULL,
    episode_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    context JSONB,
    outcome VARCHAR(50),
    lessons_learned TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_episodic_agent ON episodic_memory(agent_id, created_at);
CREATE INDEX idx_episodic_type ON episodic_memory(episode_type, created_at);
CREATE INDEX idx_episodic_expires ON episodic_memory(expires_at);

-- Decision Memory
CREATE TABLE decision_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    context JSONB,
    decision JSONB,
    rationale TEXT,
    alternatives JSONB,
    outcome VARCHAR(50),
    impact_assessment JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    reviewed_at TIMESTAMP,
    reviewed_by VARCHAR(50),
    metadata JSONB
);

CREATE INDEX idx_decision_type ON decision_memory(decision_type, created_at);
CREATE INDEX idx_decision_outcome ON decision_memory(outcome, created_at);

-- Learning Memory
CREATE TABLE learning_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    learning_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    context JSONB,
    pattern JSONB,
    success_rate FLOAT DEFAULT 0.5,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_learning_type ON learning_memory(learning_type, success_rate);
CREATE INDEX idx_learning_usage ON learning_memory(usage_count DESC);

-- Sprint Memory
CREATE TABLE sprint_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sprint_id VARCHAR(50) NOT NULL,
    sprint_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    goals JSONB,
    metrics JSONB,
    retrospective JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_sprint_id ON sprint_memory(sprint_id);
```

### 3.2 Redis Cache Structure

```yaml
redis_cache:
  session_cache:
    pattern: "session:{agent_id}:{session_id}"
    ttl: "1_hour"
    purpose: "Agent session state"
  
  working_memory:
    pattern: "working:{agent_id}:{task_id}"
    ttl: "task_duration"
    purpose: "Current task context"
  
  recent_decisions:
    pattern: "decisions:recent:{agent_id}"
    ttl: "24_hours"
    purpose: "Recent decisions for quick lookup"
  
  knowledge_cache:
    pattern: "knowledge:{entity_type}:{entity_id}"
    ttl: "1_hour"
    purpose: "Cached Knowledge Graph queries"
  
  performance_cache:
    pattern: "perf:{agent_id}:{metric}"
    ttl: "5_minutes"
    purpose: "Agent performance metrics"
```

---

## 4. RETRIEVAL STRATEGY

### 4.1 Retrieval by Context

```yaml
retrieval_strategies:
  on_task_start:
    priority_order:
      - "working_memory (current task)"
      - "episodic_memory (similar past tasks)"
      - "procedural_memory (relevant workflows)"
      - "semantic_memory (domain knowledge)"
    max_items: 20
    relevance_threshold: 0.7
  
  on_decision:
    priority_order:
      - "decision_memory (similar decisions)"
      - "semantic_memory (related knowledge)"
      - "episodic_memory (past outcomes)"
    max_items: 15
    relevance_threshold: 0.8
  
  on_error:
    priority_order:
      - "episodic_memory (similar errors)"
      - "learning_memory (error recovery patterns)"
      - "procedural_memory (fallback workflows)"
    max_items: 10
    relevance_threshold: 0.6
  
  on_review:
    priority_order:
      - "decision_memory (review criteria)"
      - "semantic_memory (quality standards)"
      - "procedural_memory (review workflows)"
    max_items: 10
    relevance_threshold: 0.8
```

### 4.2 Retrieval Algorithm

```yaml
retrieval_algorithm:
  steps:
    - "Parse context for keywords and entities"
    - "Query Knowledge Graph for related entities"
    - "Query vector store for semantic matches"
    - "Query episodic memory for temporal matches"
    - "Score and rank results"
    - "Filter by relevance threshold"
    - "Apply diversity filter (avoid redundancy)"
    - "Assemble context with token budget"
  
  scoring:
    relevance: "0.4 * semantic_similarity"
    recency: "0.2 * time_decay_factor"
    frequency: "0.15 * usage_count"
    authority: "0.15 * agent_tier_score"
    diversity: "0.1 * category_diversity"
  
  token_budget:
    working_memory: "50% of context window"
    episodic_memory: "20% of context window"
    semantic_memory: "20% of context window"
    procedural_memory: "10% of context window"
```

---

## 5. INDEXING STRATEGY

### 5.1 Knowledge Graph Indexing

```yaml
kg_indexing:
  entities:
    - "Contact"
    - "Organization"
    - "Deal"
    - "Activity"
    - "Workflow"
    - "Agent"
    - "ADR"
    - "Sprint"
    - "Module"
    - "API"
    - "Test"
    - "SecurityControl"
  
  relationships:
    - "WORKS_ON"
    - "OWNS"
    - "DEPENDS_ON"
    - "REVIEWED_BY"
    - "APPROVED_BY"
    - "CREATED_BY"
    - "IMPLEMENTS"
    - "TESTS"
    - "SECURES"
  
  indexes:
    - "Entity type + name"
    - "Relationship type + source"
    - "Created timestamp"
    - "Updated timestamp"
    - "Full-text search on descriptions"
```

### 5.2 Vector Store Indexing

```yaml
vector_indexing:
  embedding_model: "text-embedding-3-small"
  dimensions: 1536
  
  collections:
    code_embeddings:
      description: "Code snippets and documentation"
      metadata_fields: ["file_path", "language", "agent_id"]
    
    decision_embeddings:
      description: "Decision descriptions and rationale"
      metadata_fields: ["decision_type", "agent_id", "outcome"]
    
    knowledge_embeddings:
      description: "Domain knowledge and best practices"
      metadata_fields: ["category", "source", "confidence"]
    
    conversation_embeddings:
      description: "Agent conversation summaries"
      metadata_fields: ["agent_id", "topic", "timestamp"]
```

---

## 6. CONTEXT ASSEMBLY RULES

### 6.1 Assembly Process

```yaml
context_assembly:
  steps:
    - "Determine agent tier and role"
    - "Calculate token budget per memory type"
    - "Retrieve from each memory type"
    - "Score and rank retrieved items"
    - "Apply token budget constraints"
    - "Assemble final context"
    - "Validate context coherence"
    - "Inject into agent prompt`
  
  token_budget_allocation:
    system_prompt: "20%"
    working_memory: "30%"
    episodic_memory: "15%"
    semantic_memory: "25%"
    procedural_memory: "10%"
  
  context_coherence:
    rules:
      - "No contradictory information"
      - "No stale information (unless explicitly needed)"
      - "No irrelevant information"
      - "No duplicate information"
      - "Prioritize recent information"
      - "Prioritize high-confidence information"
```

### 6.2 Context Injection

```yaml
context_injection:
  format: |
    ## MEMORY CONTEXT
    
    ### Working Memory (Current Task)
    {working_memory_summary}
    
    ### Relevant Past Experiences
    {episodic_memory_summary}
    
    ### Domain Knowledge
    {semantic_memory_summary}
    
    ### Learned Workflows
    {procedural_memory_summary}
    
    ### Recent Decisions
    {decision_memory_summary}
  
  rules:
    - "Inject at the beginning of the prompt"
    - "Mark each section clearly"
    - "Include confidence scores"
    - "Include source references"
    - "Keep summaries concise"
```

---

## 7. RETENTION RULES

### 7.1 Retention Policy

```yaml
retention_policy:
  working_memory:
    retention: "task_duration"
    cleanup: "immediate"
  
  episodic_memory:
    critical_decisions: "forever"
    security_incidents: "forever"
    task_completions: "1_year"
    lessons_learned: "1_year"
    routine_records: "90_days"
    intermediate_results: "30_days"
  
  semantic_memory:
    retention: "forever"
    cleanup: "never"
    versioning: "append_only"
  
  procedural_memory:
    retention: "indefinite"
    cleanup: "success_rate < 0.3 after 10 uses"
    versioning: "evolutionary"
  
  decision_memory:
    tier1_adrs: "forever"
    tier2_adrs: "5_years"
    tier3_adrs: "2_years"
    routine_decisions: "1_year"
```

### 7.2 Cleanup Process

```yaml
cleanup_process:
  schedule: "daily at 02:00 UTC"
  
  steps:
    - "Identify expired episodic memory"
    - "Archive before deletion"
    - "Delete expired records"
    - "Optimize indexes"
    - "Update statistics"
    - "Report cleanup metrics"
  
  archive:
    location: "cold_storage"
    format: "compressed JSON"
    retention: "2_years"
```

---

## 8. MEMORY CONSISTENCY

### 8.1 Consistency Rules

```yaml
consistency_rules:
  cross_agent:
    - "Semantic memory is globally consistent"
    - "Episodic memory is per-agent (no conflicts)"
    - "Working memory is per-task (no conflicts)"
    - "Decision memory is globally consistent"
    - "Procedural memory is per-agent (no conflicts)"
  
  temporal:
    - "Recent information takes precedence"
    - "Conflicting information flagged for resolution"
    - "Stale information marked as potentially outdated"
  
  authoritative:
    - "Knowledge Graph is source of truth"
    - "Vector store is derived from Knowledge Graph"
    - "Episodic memory is append-only"
    - "Decision memory is immutable after approval"
```

### 8.2 Conflict Resolution

```yaml
conflict_resolution:
  semantic_memory:
    strategy: "append_only"
    conflict: "flag_for_review"
    resolution: "Context Steward Agent"
  
  decision_memory:
    strategy: "immutable_after_approval"
    conflict: "new_decision_required"
    resolution: "Architecture Review Board"
  
  procedural_memory:
    strategy: "success_rate_wins"
    conflict: "merge_similar_patterns"
    resolution: "Learning process"
```

---

*Part 4 complete — Full memory implementation architecture with 5 memory types, storage schema, retrieval strategy, indexing, context assembly, retention rules, and consistency management.*  
*Document maintained by Hermes Agent. Never push to Git.*
