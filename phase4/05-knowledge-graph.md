# PART 5 — KNOWLEDGE GRAPH IMPLEMENTATION

**Document:** Enterprise Agentic CRM Delivery Operating System  
**Section:** Part 5 — Knowledge Graph Implementation  
**Classification:** INTERNAL — DO NOT PUSH TO GIT

---

## 1. GRAPH TECHNOLOGY STACK

```yaml
tech_stack:
  primary_store:
    engine: "Neo4j Community Edition"
    version: "5.x"
    deployment: "Docker (Podman)"
    purpose: "Primary knowledge graph store"
    features:
      - "ACID transactions"
      - "Cypher query language"
      - "Native graph storage"
      - "Full-text indexing"
      - "Vector search (built-in)"
  
  vector_store:
    engine: "Qdrant"
    version: "1.x"
    deployment: "Docker (Podman)"
    purpose: "Semantic search and embeddings"
    features:
      - "Vector similarity search"
      - "Payload filtering"
      - "Multi-tenancy"
      - "Snapshot backup"
  
  embedding_model:
    provider: "OpenAI"
    model: "text-embedding-3-small"
    dimensions: 1536
    purpose: "Generate embeddings for semantic search"
  
  cache:
    engine: "Redis"
    purpose: "Cache frequent graph queries"
    ttl: "1_hour"
    max_size: "1GB"
```

---

## 2. ENTITY SCHEMA (12 ENTITY TYPES)

### 2.1 CRM Entities

```cypher
// CONTACT
CREATE (c:Contact {
    id: UUID,
    email: String,
    firstName: String,
    lastName: String,
    phone: String,
    company: String,
    position: String,
    source: String,
    leadScore: Float,
    tags: [String],
    customFields: Map,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime,
    deletedAt: DateTime
})

// ORGANIZATION
CREATE (o:Organization {
    id: UUID,
    name: String,
    domain: String,
    industry: String,
    size: String,
    revenue: String,
    location: String,
    website: String,
    notes: String,
    customFields: Map,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime,
    deletedAt: DateTime
})

// DEAL
CREATE (d:Deal {
    id: UUID,
    title: String,
    value: Float,
    currency: String,
    stage: String,
    probability: Float,
    expectedCloseDate: Date,
    actualCloseDate: Date,
    outcome: String,
    notes: String,
    customFields: Map,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime,
    deletedAt: DateTime
})

// ACTIVITY
CREATE (a:Activity {
    id: UUID,
    type: String,
    subject: String,
    description: String,
    dueDate: DateTime,
    completedAt: DateTime,
    priority: String,
    status: String,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})

// WORKFLOW
CREATE (w:Workflow {
    id: UUID,
    name: String,
    description: String,
    status: String,
    triggerType: String,
    triggerConfig: Map,
    actions: [Map],
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})

// EMAIL_TEMPLATE
CREATE (e:EmailTemplate {
    id: UUID,
    name: String,
    subject: String,
    body: String,
    category: String,
    variables: [String],
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})

// SEQUENCE
CREATE (s:Sequence {
    id: UUID,
    name: String,
    description: String,
    status: String,
    steps: [Map],
    enrolledCount: Int,
    completedCount: Int,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})

// CAMPAIGN
CREATE (c:Campaign {
    id: UUID,
    name: String,
    type: String,
    status: String,
    startDate: Date,
    endDate: Date,
    budget: Float,
    spent: Float,
    metrics: Map,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})
```

### 2.2 Platform Entities

```cypher
// USER
CREATE (u:User {
    id: UUID,
    email: String,
    name: String,
    role: String,
    tenantId: UUID,
    lastLoginAt: DateTime,
    createdAt: DateTime,
    updatedAt: DateTime
})

// TENANT
CREATE (t:Tenant {
    id: UUID,
    name: String,
    plan: String,
    status: String,
    settings: Map,
    createdAt: DateTime,
    updatedAt: DateTime
})

// IMPORT_JOB
CREATE (i:ImportJob {
    id: UUID,
    entityType: String,
    status: String,
    totalRows: Int,
    processedRows: Int,
    errorRows: Int,
    errors: [Map],
    tenantId: UUID,
    createdAt: DateTime,
    completedAt: DateTime
})

// REPORT
CREATE (r:Report {
    id: UUID,
    name: String,
    type: String,
    config: Map,
    lastRunAt: DateTime,
    tenantId: UUID,
    createdAt: DateTime,
    updatedAt: DateTime
})
```

---

## 3. RELATIONSHIP SCHEMA (20 RELATIONSHIP TYPES)

```cypher
// CRM Relationships
CREATE (c:Contact)-[:WORKS_FOR]->(o:Organization)
CREATE (c:Contact)-[:OWNS]->(d:Deal)
CREATE (c:Contact)-[:PARTICIPATES_IN]->(d:Deal)
CREATE (c:Contact)-[:HAS_ACTIVITY]->(a:Activity)
CREATE (c:Contact)-[:IN_SEQUENCE]->(s:Sequence)
CREATE (c:Contact)-[:IN_CAMPAIGN]->(c:Campaign)

CREATE (o:Organization)-[:HAS_DEAL]->(d:Deal)
CREATE (o:Organization)-[:HAS_CONTACT]->(c:Contact)
CREATE (o:Organization)-[:HAS_ACTIVITY]->(a:Activity)
CREATE (o:Organization)-[:IN_CAMPAIGN]->(c:Campaign)

CREATE (d:Deal)-[:HAS_ACTIVITY]->(a:Activity)
CREATE (d:Deal)-[:USES_TEMPLATE]->(e:EmailTemplate)
CREATE (d:Deal)-[:IN_CAMPAIGN]->(c:Campaign)

CREATE (w:Workflow)-[:TRIGGERS]->(a:Activity)
CREATE (w:Workflow)-[:USES_TEMPLATE]->(e:EmailTemplate)
CREATE (w:Workflow)-[:ENROLLS]->(s:Sequence)

CREATE (s:Sequence)-[:ENROLLS]->(c:Contact)
CREATE (s:Sequence)-[:USES_TEMPLATE]->(e:EmailTemplate)

CREATE (e:EmailTemplate)-[:USED_IN]->(s:Sequence)
CREATE (e:EmailTemplate)-[:USED_IN]->(w:Workflow)

// Platform Relationships
CREATE (u:User)-[:BELONGS_TO]->(t:Tenant)
CREATE (u:User)-[:OWNS]->(c:Contact)
CREATE (u:User)-[:OWNS]->(d:Deal)
CREATE (u:User)-[:CREATED]->(w:Workflow)
CREATE (u:User)-[:CREATED]->(r:Report)
CREATE (u:User)-[:RAN]->(i:ImportJob)

CREATE (t:Tenant)-[:HAS_USER]->(u:User)
CREATE (t:Tenant)-[:HAS_CONTACT]->(c:Contact)
CREATE (t:Tenant)-[:HAS_DEAL]->(d:Deal)
CREATE (t:Tenant)-[:HAS_WORKFLOW]->(w:Workflow)
CREATE (t:Tenant)-[:HAS_REPORT]->(r:Report)
```

---

## 4. QUERY PATTERNS

### 4.1 Entity Lookup

```cypher
// Find contact by email
MATCH (c:Contact {email: $email})
WHERE c.tenantId = $tenantId
RETURN c

// Find organization by name
MATCH (o:Organization)
WHERE o.name CONTAINS $search
AND o.tenantId = $tenantId
RETURN o

// Find deals by stage
MATCH (d:Deal {stage: $stage})
WHERE d.tenantId = $tenantId
RETURN d ORDER BY d.value DESC
```

### 4.2 Relationship Traversal

```cypher
// Find all contacts for an organization
MATCH (c:Contact)-[:WORKS_FOR]->(o:Organization {id: $orgId})
RETURN c

// Find all deals for a contact
MATCH (c:Contact {id: $contactId})-[:OWNS]->(d:Deal)
RETURN d

// Find contact's activity history
MATCH (c:Contact {id: $contactId})-[:HAS_ACTIVITY]->(a:Activity)
RETURN a ORDER BY a.createdAt DESC

// Find deal's full context
MATCH (d:Deal {id: $dealId})
OPTIONAL MATCH (d)<-[:OWNS]-(c:Contact)
OPTIONAL MATCH (d)-[:HAS_ACTIVITY]->(a:Activity)
OPTIONAL MATCH (d)-[:IN_CAMPAIGN]->(camp:Campaign)
RETURN d, c, a, camp
```

### 4.3 Aggregate Queries

```cypher
// Pipeline summary
MATCH (d:Deal {tenantId: $tenantId})
WHERE d.stage IN ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost']
RETURN d.stage, COUNT(d) as count, SUM(d.value) as totalValue
ORDER BY totalValue DESC

// Contact engagement score
MATCH (c:Contact {id: $contactId})
OPTIONAL MATCH (c)-[:HAS_ACTIVITY]->(a:Activity)
WHERE a.createdAt > datetime() - duration('P30D')
RETURN c, COUNT(a) as recentActivities

// Organization deal history
MATCH (o:Organization {id: $orgId})<-[:WORKS_FOR]-(c:Contact)-[:OWNS]->(d:Deal)
RETURN d, c
ORDER BY d.createdAt DESC
```

### 4.4 Semantic Search (via Qdrant)

```yaml
semantic_search:
  code_search:
    description: "Search code by natural language"
    collection: "code_embeddings"
    query: "How to implement rate limiting in Go"
    top_k: 10
    filter: "language:go"
  
  decision_search:
    description: "Search past decisions"
    collection: "decision_embeddings"
    query: "Database migration strategy for contacts table"
    top_k: 5
    filter: "decision_type:architecture"
  
  knowledge_search:
    description: "Search domain knowledge"
    collection: "knowledge_embeddings"
    query: "Best practices for contact management"
    top_k: 10
    filter: "category:crm"
```

---

## 5. UPDATE PATTERNS

### 5.1 Entity Updates

```yaml
entity_updates:
  create:
    pattern: "Create node + index + vector embedding"
    transaction: "ACID"
    notification: "knowledge_graph.updates"
  
  update:
    pattern: "Update properties + re-index + re-embed"
    transaction: "ACID"
    notification: "knowledge_graph.updates"
  
  delete:
    pattern: "Soft delete (set deletedAt)"
    transaction: "ACID"
    notification: "knowledge_graph.updates"
    hard_delete: "Never (retain for audit)"
```

### 5.2 Relationship Updates

```yaml
relationship_updates:
  create:
    pattern: "Create relationship + update index"
    transaction: "ACID"
    validation: "Both nodes must exist"
  
  delete:
    pattern: "Delete relationship"
    transaction: "ACID"
    validation: "Relationship must exist"
  
  update:
    pattern: "Delete + Create (relationships are immutable)"
    transaction: "ACID"
```

### 5.3 Batch Updates

```yaml
batch_updates:
  import_job:
    pattern: "Bulk create entities from CSV"
    batch_size: 1000
    transaction: "Per batch"
    error_handling: "Continue on error, log failures"
    progress_tracking: "Update ImportJob progress"
  
  data_sync:
    pattern: "Sync from external source"
    batch_size: 500
    transaction: "Per batch"
    conflict_resolution: "Last-write-wins"
    audit_trail: "Log all changes"
```

---

## 6. VALIDATION RULES

```yaml
validation_rules:
  entity_creation:
    - "ID must be UUID v4"
    - "Required fields must be present"
    - "Email must be valid format"
    - "Dates must be valid ISO 8601"
    - "tenantId must match current tenant"
  
  relationship_creation:
    - "Source node must exist"
    - "Target node must exist"
    - "Relationship type must be valid"
    - "No duplicate relationships"
    - "Both nodes must belong to same tenant"
  
  entity_update:
    - "Entity must exist"
    - "Only allowed fields can be updated"
    - "updated_at must be set"
    - "Audit trail must be maintained"
  
  tenant_isolation:
    - "All queries must filter by tenantId"
    - "Cross-tenant queries are forbidden"
    - "Global entities (ADR) use special access"
```

---

## 7. AGENT INTERACTION PATTERNS

```yaml
agent_kg_interactions:
  read_patterns:
    on_task_start:
      - "Query related entities"
      - "Query past decisions"
      - "Query relevant knowledge"
    during_task:
      - "Query entity details"
      - "Query relationship context"
    on_completion:
      - "Query for review context"
  
  write_patterns:
    on_task_completion:
      - "Update entity status"
      - "Create new relationships"
      - "Log decision"
    on_decision:
      - "Create ADR entity"
      - "Link to related entities"
    on_learning:
      - "Update procedural memory"
      - "Log lesson learned"
  
  search_patterns:
    semantic_search:
      - "Find similar past tasks"
      - "Find relevant code"
      - "Find relevant decisions"
    graph_traversal:
      - "Find related entities"
      - "Find dependency chains"
      - "Find impact analysis"
```

---

## 8. BACKUP & RECOVERY

```yaml
backup_strategy:
  neo4j:
    schedule: "daily at 01:00 UTC"
    method: "neo4j-admin database dump"
    retention: "30 days"
    location: "cold_storage"
    verification: "weekly restore test"
  
  qdrant:
    schedule: "daily at 01:30 UTC"
    method: "qdrant snapshot"
    retention: "30 days"
    location: "cold_storage"
    verification: "weekly restore test"
  
  redis:
    schedule: "every 6 hours"
    method: "RDB snapshot"
    retention: "7 days"
    location: "local"
    verification: "none (cache only)"
  
  recovery:
    rpo: "24 hours"
    rto: "4 hours"
    procedure: "Restore from latest backup, replay WAL"
```

---

*Part 5 complete — Full Knowledge Graph implementation with Neo4j/Qdrant schema, 12 entity types, 20 relationship types, query patterns, update patterns, validation rules, and agent interaction patterns.*  
*Document maintained by Hermes Agent. Never push to Git.*
