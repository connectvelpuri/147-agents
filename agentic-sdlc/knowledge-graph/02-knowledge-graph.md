# PART 2 — KNOWLEDGE GRAPH & MEMORY SYSTEM

**Document:** Enterprise Agentic CRM Delivery Operating System  
**Section:** Part 2 — Knowledge Graph & Memory System  
**Classification:** INTERNAL — DO NOT PUSH TO GIT

---

## 2.1 PURPOSE

The Knowledge Graph is the centralized project brain. Every agent must consult
it before making decisions. Every agent must update it after completing work.
No orphaned knowledge, no undocumented decisions, no duplicated efforts.

### Core Principles
1. **Single Source of Truth** — All project knowledge lives here
2. **Always Consulted** — No agent operates without checking the graph
3. **Always Updated** — Every decision and output updates the graph
4. **Relationship-Aware** — Everything connects to everything else
5. **Query-Optimized** — Fast retrieval for agent consumption
6. **Version-Controlled** — Every change is tracked and reversible

---

## 2.2 DATA MODEL

### Entity Types

```
┌─────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE GRAPH ENTITIES                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  REQUIREMENTS          FEATURES           CRM MODULES       │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐     │
│  │ PRD      │────────▶│ Feature  │──────▶│ Module   │     │
│  │ User Story│         │ Epic     │       │ SubMod   │     │
│  │ Acceptance│         │ Story    │       │ Entity   │     │
│  └──────────┘         └──────────┘       └──────────┘     │
│       │                    │                    │            │
│       ▼                    ▼                    ▼            │
│  WORKFLOWS            API ENDPOINTS       DATA MODELS       │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐     │
│  │ Workflow │────────▶│ Endpoint │──────▶│ Table    │     │
│  │ Trigger  │         │ Method   │       │ Column   │     │
│  │ Action   │         │ Schema   │       │ Index    │     │
│  └──────────┘         └──────────┘       └──────────┘     │
│       │                    │                    │            │
│       ▼                    ▼                    ▼            │
│  TESTS               DEPLOYMENTS          INTEGRATIONS      │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐     │
│  │ Unit     │────────▶│ Pipeline │──────▶│ Webhook  │     │
│  │ Integr   │         │ Stage    │       │ API      │     │
│  │ E2E      │         │ Env      │       │ Adapter  │     │
│  └──────────┘         └──────────┘       └──────────┘     │
│                                                             │
│  RISKS               ADRs               PERSONAS            │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐     │
│  │ Risk     │────────▶│ Decision │──────▶│ Persona  │     │
│  │ Impact   │         │ Context  │       │ Journey  │     │
│  │ Mitigate │         │ Tradeoff │       │ Need     │     │
│  └──────────┘         └──────────┘       └──────────┘     │
│                                                             │
│  DECISIONS            COMPONENTS          AGENTS             │
│  ┌──────────┐         ┌──────────┐       ┌──────────┐     │
│  │ Decision │────────▶│ Service  │──────▶│ Agent    │     │
│  │ Rationale│         │ Module   │       │ Role     │     │
│  │ Impact   │         │ Package  │       │ Scope    │     │
│  └──────────┘         └──────────┘       └──────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Entity Definitions

#### REQUIREMENT Entity
```json
{
  "id": "REQ-001",
  "type": "requirement",
  "title": "Contact Management CRUD",
  "description": "Users must be able to create, read, update, and delete contacts",
  "priority": "P0",
  "status": "approved",
  "source": "PRD-001",
  "owner": "Product Management Agent",
  "created_at": "2026-06-07T00:00:00Z",
  "updated_at": "2026-06-07T00:00:00Z",
  "relationships": {
    "implements": ["FEAT-001", "FEAT-002"],
    "depends_on": [],
    "blocked_by": [],
    "verified_by": ["TEST-001", "TEST-002"]
  },
  "metadata": {
    "acceptance_criteria": [
      "User can create contact with first_name, last_name, email",
      "User can list contacts with pagination",
      "User can update any contact field",
      "User can soft-delete contacts"
    ],
    "persona": "PERS-001",
    "journey": "JRNY-001"
  }
}
```

#### FEATURE Entity
```json
{
  "id": "FEAT-001",
  "type": "feature",
  "title": "Contact Creation",
  "description": "API endpoint and UI for creating new contacts",
  "priority": "P0",
  "status": "in_development",
  "module": "MOD-CONTACTS",
  "owner": "Frontend Architect",
  "created_at": "2026-06-07T00:00:00Z",
  "relationships": {
    "satisfies": ["REQ-001"],
    "implemented_by": ["COMP-001", "COMP-002"],
    "depends_on": ["FEAT-010"],  // Authentication
    "blocks": ["FEAT-003"],      // Contact Edit
    "tested_by": ["TEST-001"],
    "deployed_in": ["DEPLOY-001"]
  },
  "metadata": {
    "story_points": 5,
    "sprint": "Sprint-7",
    "design_spec": "DES-001",
    "adr": "ADR-001"
  }
}
```

#### CRM MODULE Entity
```json
{
  "id": "MOD-CONTACTS",
  "type": "crm_module",
  "title": "Contact Management",
  "description": "Core CRM module for managing contacts",
  "status": "implemented",
  "maturity_level": 3,
  "owner": "CRM Architect",
  "created_at": "2026-06-07T00:00:00Z",
  "relationships": {
    "contains": ["FEAT-001", "FEAT-002", "FEAT-003"],
    "depends_on": ["MOD-AUTH", "MOD-TENANTS"],
    "integrates_with": ["MOD-ORGANIZATIONS", "MOD-DEALS"],
    "data_entities": ["ENT-CONTACT", "ENT-ACTIVITY"],
    "api_endpoints": ["API-CONT-001", "API-CONT-002"],
    "ui_components": ["UI-CONT-001", "UI-CONT-002"]
  },
  "metadata": {
    "maturity_scores": {
      "product": 4,
      "architecture": 4,
      "security": 3,
      "data": 4,
      "qa": 3,
      "scalability": 3,
      "operations": 3,
      "ai_readiness": 2
    }
  }
}
```

#### WORKFLOW Entity
```json
{
  "id": "WF-001",
  "type": "workflow",
  "title": "Contact Creation Workflow",
  "description": "Workflow triggered when a new contact is created",
  "trigger_type": "record_created",
  "trigger_entity": "ENT-CONTACT",
  "status": "active",
  "owner": "Workflow Engineer",
  "relationships": {
    "triggered_by": ["FEAT-001"],
    "executes_actions": ["ACT-001", "ACT-002"],
    "modifies_entities": ["ENT-CONTACT", "ENT-ACTIVITY"],
    "tested_by": ["TEST-WF-001"]
  },
  "metadata": {
    "actions": [
      {"type": "create_activity", "config": {"type": "note", "subject": "Contact created"}},
      {"type": "send_notification", "config": {"channel": "email"}}
    ]
  }
}
```

#### API ENDPOINT Entity
```json
{
  "id": "API-CONT-001",
  "type": "api_endpoint",
  "title": "POST /contacts",
  "description": "Create a new contact",
  "method": "POST",
  "path": "/api/contacts",
  "auth_required": true,
  "roles": ["admin", "manager", "rep"],
  "status": "implemented",
  "owner": "API Engineer",
  "relationships": {
    "implements_feature": "FEAT-001",
    "uses_service": "COMP-CONTACT-HANDLER",
    "queries_database": "ENT-CONTACT",
    "validated_by": "TEST-API-001",
    "documented_in": "DOC-API-001"
  },
  "metadata": {
    "request_schema": "ContactCreateRequest",
    "response_schema": "ContactResponse",
    "rate_limit": "100/minute",
    "estimated_latency_ms": 45
  }
}
```

#### DATA MODEL Entity
```json
{
  "id": "ENT-CONTACT",
  "type": "data_entity",
  "title": "contacts table",
  "description": "PostgreSQL table for storing contact data",
  "schema": "public",
  "status": "implemented",
  "owner": "Data Architect",
  "relationships": {
    "implements_entity": "MOD-CONTACTS",
    "referenced_by": ["API-CONT-001", "API-CONT-002"],
    "has_indexes": ["IDX-CONT-001", "IDX-CONT-002"],
    "has_rls_policy": "POL-CONTACTS",
    "referenced_by_foreign_keys": ["ENT-ACTIVITY", "ENT-DEAL"]
  },
  "metadata": {
    "columns": ["id", "tenant_id", "first_name", "last_name", "email", "..."],
    "row_count_estimate": 100000,
    "growth_rate": "10%/month",
    "size_estimate_gb": 2.5
  }
}
```

#### ADR Entity
```json
{
  "id": "ADR-001",
  "type": "adr",
  "title": "Use JWT with Redis for Authentication",
  "status": "accepted",
  "decision_date": "2026-06-07",
  "review_date": "2026-09-07",
  "owner": "Security Architect",
  "relationships": {
    "affects": ["MOD-AUTH", "MOD-SESSION"],
    "supersedes": [],
    "superseded_by": [],
    "related_to": ["ADR-002", "ADR-003"]
  },
  "metadata": {
    "context": "Need secure authentication with token blacklisting",
    "decision": "Use JWT access tokens with Redis session storage",
    "alternatives": ["Supabase Auth", "Auth0", "Self-hosted OAuth2"],
    "tradeoffs": "More implementation work but full control",
    "risks": ["Redis dependency", "Token rotation complexity"],
    "approval_status": "approved",
    "approved_by": "CTO Agent"
  }
}
```

#### TEST Entity
```json
{
  "id": "TEST-001",
  "type": "test",
  "title": "Contact Creation Unit Test",
  "test_type": "unit",
  "status": "passing",
  "coverage_area": "FEAT-001",
  "owner": "Unit Testing Agent",
  "relationships": {
    "tests_feature": "FEAT-001",
    "tests_entity": "ENT-CONTACT",
    "uses_mock": "MOCK-001",
    "part_of_suite": "SUITE-CONTACTS"
  },
  "metadata": {
    "last_run": "2026-06-07T12:00:00Z",
    "pass_rate": 100,
    "execution_time_ms": 45,
    "code_coverage": 85
  }
}
```

#### DEPLOYMENT Entity
```json
{
  "id": "DEPLOY-001",
  "type": "deployment",
  "title": "Production Deployment",
  "environment": "production",
  "status": "active",
  "owner": "DevOps Agent",
  "relationships": {
    "deploys_services": ["SVC-API", "SVC-WEB", "SVC-DB"],
    "uses_pipeline": "PIPE-001",
    "has_rollback": "DEPLOY-000",
    "monitored_by": "MON-001"
  },
  "metadata": {
    "version": "1.0.0",
    "deployed_at": "2026-06-07T00:00:00Z",
    "health_check": "https://api.example.com/health",
    "rollback_procedure": "podman-compose rollback"
  }
}
```

#### RISK Entity
```json
{
  "id": "RISK-001",
  "type": "risk",
  "title": "Redis Single Point of Failure",
  "probability": "medium",
  "impact": "high",
  "severity": "high",
  "status": "mitigated",
  "owner": "CRO Agent",
  "relationships": {
    "affects": ["MOD-AUTH", "MOD-SESSION"],
    "mitigated_by": ["MIT-001"],
    "related_to": ["RISK-002"]
  },
  "metadata": {
    "description": "Redis failure causes authentication system outage",
    "mitigation": "Implement Redis Sentinel for high availability",
    "residual_risk": "medium",
    "review_date": "2026-07-07"
  }
}
```

#### PERSONA Entity
```json
{
  "id": "PERS-001",
  "type": "persona",
  "title": "IT Services Sales Rep",
  "description": "Sales representative at an IT services company",
  "segment": "IT Services",
  "owner": "User Research Agent",
  "relationships": {
    "uses_features": ["FEAT-001", "FEAT-002", "FEAT-005"],
    "journeys": ["JRNY-001", "JRNY-002"],
    "pain_points": ["PP-001", "PP-002"],
    "needs": ["NEED-001", "NEED-002"]
  },
  "metadata": {
    "company_size": "10-50 employees",
    "tech_savviness": "medium",
    "current_crm": "Excel/Sheets",
    "budget": "$500-2000/year"
  }
}
```

---

## 2.3 RELATIONSHIP MODEL

### Relationship Types

| Relationship | Description | Example |
|-------------|-------------|---------|
| `implements` | Feature implements Requirement | FEAT-001 implements REQ-001 |
| `satisfies` | Feature satisfies Requirement | FEAT-001 satisfies REQ-001 |
| `depends_on` | Entity depends on another | FEAT-003 depends_on FEAT-001 |
| `blocks` | Entity blocks another | FEAT-003 blocks FEAT-004 |
| `tested_by` | Feature tested by Test | FEAT-001 tested_by TEST-001 |
| `deployed_in` | Feature deployed in Deployment | FEAT-001 deployed_in DEPLOY-001 |
| `uses_service` | Endpoint uses Service | API-001 uses_service SVC-001 |
| `queries_database` | Endpoint queries Database | API-001 queries_database ENT-001 |
| `affects` | ADR affects Module | ADR-001 affects MOD-001 |
| `supersedes` | ADR supersedes another | ADR-002 supersedes ADR-001 |
| `mitigated_by` | Risk mitigated by Action | RISK-001 mitigated_by MIT-001 |
| `contains` | Module contains Feature | MOD-001 contains FEAT-001 |
| `integrates_with` | Module integrates with Module | MOD-001 integrates_with MOD-002 |
| `triggered_by` | Workflow triggered by Feature | WF-001 triggered_by FEAT-001 |
| `executes_actions` | Workflow executes Actions | WF-001 executes_actions ACT-001 |
| `part_of_suite` | Test part of Test Suite | TEST-001 part_of_suite SUITE-001 |
| `uses_feature` | Persona uses Feature | PERS-001 uses_feature FEAT-001 |
| `reviews` | Agent reviews Entity | QA-Agent reviews FEAT-001 |
| `owns` | Agent owns Entity | PM-Agent owns REQ-001 |
| `escalated_to` | Issue escalated to Agent | ISSUE-001 escalated_to CTO |

### Relationship Rules

1. **No Orphaned Entities** — Every entity must have at least one relationship
2. **No Circular Dependencies** — Dependency chains must be acyclic
3. **Bidirectional Navigation** — If A depends_on B, then B can find A
4. **Cascade Updates** — When entity status changes, related entities notified
5. **Relationship Validation** — New relationships validated against rules

---

## 2.4 RETRIEVAL STRATEGY

### Query Patterns

#### Pattern 1: Impact Analysis
**Question:** "What is affected if I change FEAT-001?"
**Query:** Traverse `blocks`, `depends_on`, `tested_by`, `deployed_in`
**Returns:** All downstream entities, tests, deployments

#### Pattern 2: Traceability
**Question:** "Where does REQ-001 trace to in code?"
**Query:** REQ-001 → implements → FEAT-001 → implemented_by → COMP-001 → queries_database → ENT-001
**Returns:** Full traceability chain from requirement to code to data

#### Pattern 3: Gap Analysis
**Question:** "Which requirements have no tests?"
**Query:** Find REQ where tested_by is empty
**Returns:** List of untested requirements

#### Pattern 4: Dependency Graph
**Question:** "What are all dependencies for MOD-CONTACTS?"
**Query:** Traverse all `depends_on` relationships recursively
**Returns:** Complete dependency tree

#### Pattern 5: Agent Assignment
**Question:** "Which agents are responsible for FEAT-001?"
**Query:** Find all agents with `owns` or `reviews` relationships to FEAT-001
**Returns:** List of responsible agents

### Retrieval Optimization

- **Index Strategy:** Every relationship type indexed
- **Cache Strategy:** Frequently accessed entities cached
- **Batch Queries:** Support bulk retrieval for agent consumption
- **Pagination:** Large result sets paginated
- **Filtering:** Filter by entity type, status, owner, date range

---

## 2.5 UPDATE STRATEGY

### Update Triggers

| Event | Update Action | Agent Responsible |
|-------|--------------|-------------------|
| Requirement created | Create REQ entity, link to PRD | Product Management |
| Feature designed | Create FEAT entity, link to REQ | Solution Architect |
| Code implemented | Update FEAT status, link to COMP | API Engineer |
| Test written | Create TEST entity, link to FEAT | Unit Testing |
| Test passes | Update TEST status | Unit Testing |
| ADR created | Create ADR entity, link to affected entities | Security Architect |
| Deployment done | Create DEPLOY entity, link to services | DevOps |
| Risk identified | Create RISK entity, link to affected entities | CRO |
| Bug found | Create BUG entity, link to FEAT and TEST | QA Architect |

### Update Rules

1. **Atomic Updates** — Multiple related entities updated in transaction
2. **Version Control** — Every update creates new version
3. **Audit Trail** — Every update logged with agent, timestamp, reason
4. **Conflict Detection** — Concurrent updates detected and resolved
5. **Propagation** — Changes propagate to related entities

### Update Validation

```json
{
  "validation_rules": [
    {
      "rule": "ENTITY_EXISTS",
      "description": "Entity must exist before update"
    },
    {
      "rule": "STATUS_TRANSITION_VALID",
      "description": "Status changes must follow allowed transitions"
    },
    {
      "rule": "RELATIONSHIP_VALID",
      "description": "New relationships must not create cycles"
    },
    {
      "rule": "OWNER_AUTHORIZED",
      "description": "Agent must be authorized to update entity"
    },
    {
      "rule": "METADATA_SCHEMA_VALID",
      "description": "Metadata must conform to entity schema"
    }
  ]
}
```

---

## 2.6 AGENT ACCESS CONTROLS

### Access Matrix

| Agent Tier | Read | Write | Approve | Delete |
|-----------|------|-------|---------|--------|
| Tier 1 (Executive) | All | All | All | All |
| Tier 2 (Director) | All | Own Domain | Own Domain | Own Domain |
| Tier 3 (Manager) | Own Domain | Own Team | Own Team | No |
| Tier 4 (Specialist) | Own Scope | Own Work | No | No |
| Tier 5 (Support) | Cross-cutting | Own Work | No | No |

### Domain Boundaries

| Domain | Owner | Access |
|--------|-------|--------|
| Product Requirements | CPO | Product Org, Design Org |
| Architecture | CTO | Architecture Org, Engineering Org |
| Security | CSO | Security Org, DevSecOps |
| Data | CDO | Data Governance Office |
| AI | AI Architect | AI Governance Office |
| Testing | QA Architect | Quality Organization |
| Deployment | DevOps | DevSecOps Organization |

### Access Control Rules

1. **Principle of Least Privilege** — Agents access only what they need
2. **Role-Based Access** — Access determined by agent role and domain
3. **Time-Bounded Access** — Access revoked when role changes
4. **Audit Logging** — All access logged and auditable
5. **Emergency Override** — Tier 1 agents can override for emergencies

---

## 2.7 MEMORY ARCHITECTURE

### Memory Layers

```
┌─────────────────────────────────────────────────────┐
│                  AGENT MEMORY                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  LAYER 1: WORKING MEMORY (Current Session)          │
│  ┌─────────────────────────────────────────────┐   │
│  │ Current task context                        │   │
│  │ Recent decisions                            │   │
│  │ Active conversations                        │   │
│  │ Temporary state                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  LAYER 2: EPISODIC MEMORY (Recent History)          │
│  ┌─────────────────────────────────────────────┐   │
│  │ Last 30 days of decisions                   │   │
│  │ Recent bug fixes                            │   │
│  │ Recent feature completions                  │   │
│  │ Recent review outcomes                      │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  LAYER 3: SEMANTIC MEMORY (Knowledge)               │
│  ┌─────────────────────────────────────────────┐   │
│  │ Architecture patterns                       │   │
│  │ Coding standards                            │   │
│  │ Best practices                              │   │
│  │ Lessons learned                             │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  LAYER 4: PROCEDURAL MEMORY (How-To)                │
│  ┌─────────────────────────────────────────────┐   │
│  │ Build procedures                            │   │
│  │ Deployment procedures                       │   │
│  │ Testing procedures                          │   │
│  │ Incident response procedures                │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  LAYER 5: KNOWLEDGE GRAPH (Shared)                  │
│  ┌─────────────────────────────────────────────┐   │
│  │ All entities and relationships              │   │
│  │ All ADRs                                    │   │
│  │ All decisions                               │   │
│  │ All artifacts                               │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Memory Update Rules

1. **Working Memory** — Cleared at session end, important facts promoted
2. **Episodic Memory** — Retained for 30 days, then archived
3. **Semantic Memory** — Persistent, updated when new patterns emerge
4. **Procedural Memory** — Persistent, updated when procedures change
5. **Knowledge Graph** — Persistent, updated on every significant event

### Memory Retrieval

- **Agents query Knowledge Graph first** before any decision
- **Episodic memory** consulted for recent context
- **Semantic memory** consulted for patterns and standards
- **Procedural memory** consulted for how-to guidance
- **Working memory** used for current task execution

---

*Part 2 complete — Knowledge Graph data model, relationship model, retrieval strategy, update strategy, and access controls defined.*  
*Document maintained by Hermes Agent. Never push to Git.*
