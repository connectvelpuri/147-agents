# 03 — Agent Memory Architecture

## Where Knowledge Lives in a 548-Agent System

---

## Executive Summary

Without explicit memory architecture, agents relearn the same things repeatedly.
Agent A discovers that a specific database query is slow. Agent B discovers the
same thing next week. Agent C doesn't discover it at all and causes a production
outage. This is the fundamental failure mode of memoryless agent systems.

The Sovereign Enterprise memory architecture defines FIVE memory layers, each with
specific content, access patterns, ownership, and lifecycle rules. Together they
ensure that knowledge is discovered once, validated, stored, retrieved when needed,
and eventually retired when obsolete.

The architecture integrates concepts from:
  - Semantic Kernel: Semantic memory + chat history
  - LangChain: Vector stores + document retrieval
  - Phidata: Knowledge bases + retrieval-augmented generation
  - CrewAI: Shared crew context + task memory
  - LangGraph: Checkpointed state + short-term memory

---

## 1. Memory Philosophy

### 1.1 Why Memory Matters

Memory is the difference between a collection of agents and an intelligent
organization. Without memory:

  - Agents waste time rediscovering known facts
  - Decisions are made without historical context
  - Patterns are never recognized because no one remembers them
  - Mistakes are repeated because no one records them
  - Best practices remain tribal knowledge instead of system knowledge

With memory:

  - Agents start every task with relevant context pre-loaded
  - Decisions reference historical outcomes and precedent
  - Patterns are detected, validated, and operationalized
  - Mistakes trigger prevention mechanisms that prevent recurrence
  - Best practices are codified, versioned, and enforced

### 1.2 Memory Principles

  PRINCIPLE 1: Memory is not optional
    Every agent MUST read relevant memory before starting work.
    "I didn't know" is never an acceptable excuse.

  PRINCIPLE 2: Memory is validated, not trusted
    Memory entries have credibility scores. Agents should prefer
    high-credibility entries over low-credibility ones.

  PRINCIPLE 3: Memory is owned
    Every memory entry has an owner responsible for its accuracy.
    Unowned memory decays and is eventually deleted.

  PRINCIPLE 4: Memory is time-bound
    Memory entries have expiration dates. Stale memory is automatically
    flagged for review or deletion.

  PRINCIPLE 5: Memory is structured
    Unstructured memory dumps are useless. Every memory entry follows
    a schema and belongs to a category.

---

## 2. Memory Layers

### 2.1 Layer 1: Working Memory (Agent-Local)

  SCOPE: Single agent
  LIFETIME: Current task/session
  SIZE: Limited (fits in agent context window)
  ACCESS: Agent-only (no other agent can read)

  CONTENT:
    - Current task description and acceptance criteria
    - Recent messages related to current task
    - Intermediate calculations and reasoning
    - Scratchpad for in-progress work
    - Temporary variable storage

  STRUCTURE:
    {
      "agent_id": "crm-backend-eng-01",
      "task_id": "crdt-sync-contacts",
      "working_memory": {
        "task_description": "Implement CRDT sync for contacts module",
        "acceptance_criteria": [...],
        "recent_messages": [...],
        "scratchpad": {
          "approach": "LWW-Register with vector clocks",
          "files_modified": ["contacts/models.py", "contacts/sync.py"],
          "tests_written": 12,
          "tests_passing": 10,
          "remaining": "Edge case: concurrent delete + update"
        }
      },
      "expires_at": "2026-06-09T18:00:00Z"
    }

  ACCESS PATTERN:
    Read/write: Agent itself only
    On task completion: Key learnings extracted to Team Memory
    On task failure: Failure context extracted to Domain Memory

  STORAGE: In-process (agent's own context/state)
  RETENTION: Duration of task only

### 2.2 Layer 2: Team Memory (Pod-Shared)

  SCOPE: Single pod (5-15 agents)
  LIFETIME: Sprint duration (2 weeks) + 30 days archive
  SIZE: Moderate (100KB-1MB per pod)
  ACCESS: All pod members

  CONTENT:
    - Sprint goals and current progress
    - Pod-specific conventions and shortcuts
    - Shared technical decisions for this sprint
    - Dependency status with other pods
    - Known issues and workarounds
    - Pod retrospective learnings

  STRUCTURE:
    {
      "pod_id": "crm-core-pod",
      "sprint": "sprint-12",
      "team_memory": {
        "sprint_goal": "Complete CRDT sync + dashboard v2",
        "conventions": {
          "branch_naming": "feature/{ticket}-{short-desc}",
          "pr_template": "Standard CRM pod template"
        },
        "decisions": [
          {
            "decision": "Use LWW-Register for CRDT",
            "rationale": "Simpler than OT for our use case",
            "decided_by": "crm-arch-01",
            "date": "2026-06-05"
          }
        ],
        "dependencies": [
          {
            "dependent_on": "platform-pod",
            "item": "Database index creation",
            "status": "completed"
          }
        ],
        "known_issues": [
          {
            "issue": "Slow query on contacts with 100K+ records",
            "workaround": "Add LIMIT clause, paginate results",
            "ticket": "CRM-456"
          }
        ],
        "retrospective_notes": [
          "We need better test data generation for performance testing"
        ]
      }
    }

  ACCESS PATTERN:
    Read: All pod members
    Write: All pod members (with attribution)
    Archive: At sprint end, key learnings extracted to Domain Memory

  STORAGE: Shared pod workspace (Redis/disk-backed)
  RETENTION: Sprint + 30 days, then archived

### 2.3 Layer 3: Domain Memory (Cross-Pod)

  SCOPE: Entire domain (e.g., all CRM agents, all backend engineers)
  LIFETIME: Persistent (reviewed quarterly)
  SIZE: Large (10MB-100MB per domain)
  ACCESS: All agents in the domain

  CONTENT:
    - Domain-specific best practices
    - Architecture decision records (ADRs)
    - Technical patterns and anti-patterns
    - Known failure modes and mitigations
    - Performance benchmarks and baselines
    - API contracts and schema definitions
    - Domain glossary and terminology
    - Regulatory/compliance requirements

  STRUCTURE:
    {
      "domain": "crm-backend",
      "domain_memory": {
        "best_practices": [
          {
            "id": "bp-001",
            "title": "Always index foreign keys in CRM database",
            "description": "Unindexed FK joins cause N+1 queries...",
            "evidence": "CRM-234 incident, CRM-456 slow query",
            "credibility": 0.95,
            "last_validated": "2026-06-01",
            "owner": "crm-arch-01"
          }
        ],
        "adrs": [...],
        "patterns": [...],
        "failure_modes": [...],
        "benchmarks": {...},
        "api_contracts": [...],
        "glossary": {...},
        "compliance": [...]
      }
    }

  ACCESS PATTERN:
    Read: All domain agents (recommended before starting any task)
    Write: Domain leads and authorized contributors
    Validation: Quarterly review by domain lead
    Credibility: Scored by evidence count and recency

  STORAGE: Domain knowledge base (vector store + relational DB)
  RETENTION: Persistent, reviewed quarterly

### 2.4 Layer 4: Enterprise Memory (Organization-Wide)

  SCOPE: All agents across all products and domains
  LIFETIME: Permanent (with versioning)
  SIZE: Very large (500MB-5GB)
  ACCESS: All agents (read), authorized roles (write)

  CONTENT:
    - Enterprise standards and conventions
    - Cross-domain architectural decisions
    - Product roadmap and strategic context
    - Customer research insights
    - Market and competitive intelligence
    - Financial metrics and budgets
    - Organizational structure and roles
    - Governance policies and compliance requirements
    - Incident post-mortems (enterprise-level)
    - Learning patterns from ELO system

  STRUCTURE:
    {
      "enterprise_memory": {
        "standards": {
          "coding": "TypeScript, React, Python, Go",
          "architecture": "Microservices, event-driven, CQRS",
          "security": "Zero-trust, mTLS, RBAC",
          "testing": "80% coverage minimum, no sev-1/2 in production"
        },
        "strategic_context": {
          "mission": "AI-native enterprise operating system",
          "products": ["CRM", "ERP", "HR", "Finance"],
          "competitive_advantage": "Agent-native architecture, real-time sync"
        },
        "customer_insights": {...},
        "market_intelligence": {...},
        "governance_policies": {...},
        "learning_patterns": {...}
      }
    }

  ACCESS PATTERN:
    Read: All agents (injected into context at task start)
    Write: L1-L2 agents, Enterprise Architect, designated knowledge owners
    Version: Every update creates a new version with change log
    Credibility: Enterprise-level entries are highest credibility

  STORAGE: Enterprise knowledge graph + vector store
  RETENTION: Permanent with versioning

### 2.5 Layer 5: Knowledge Graph (Semantic Relationships)

  SCOPE: Cross-cutting (connects all memory layers)
  LIFETIME: Permanent (continuously updated)
  SIZE: Variable (grows with the organization)
  ACCESS: All agents (query), knowledge engineers (maintain)

  CONTENT:
    - Entity relationships (agent → domain → product → customer)
    - Causal chains (incident → root cause → fix → prevention)
    - Pattern detection (recurring issues → systemic problem)
    - Expertise mapping (who knows what)
    - Dependency graphs (service A depends on service B)
    - Concept hierarchies (CRM → contacts → fields → validation rules)

  STRUCTURE:
    Nodes:
      - Agent (id, role, domain, capabilities)
      - Document (id, type, domain, version, credibility)
      - Decision (id, rationale, outcome, precedents)
      - Incident (id, severity, root_cause, resolution)
      - Pattern (id, evidence_count, confidence, domain)
      - Customer (id, segment, feedback_count, satisfaction)
      - Service (id, domain, dependencies, SLOs)
      - Standard (id, scope, enforcement_level, version)

    Edges:
      - OWNS (agent → document)
      - DEPENDS_ON (service → service)
      - CAUSED_BY (incident → root_cause)
      - RESOLVED_BY (incident → fix)
      - FOLLOWS_PATTERN (incident → pattern)
      - DECIDED_BY (decision → agent)
      - AFFECTS (change → service)
      - KNOWS_ABOUT (agent → knowledge)

  ACCESS PATTERN:
    Query: Any agent can query the graph
    Traverse: Follow relationships to find relevant context
    Update: Automated (from events) + manual (knowledge engineers)
    Validate: Automated consistency checks + quarterly review

  STORAGE: Graph database (Neo4j or equivalent) + vector embeddings
  RETENTION: Permanent, continuously pruned

---

## 3. Memory Operations

### 3.1 Memory Write

  WHEN: After completing any task, making any decision, resolving any incident
  WHAT: Extract key learnings, decisions, and patterns
  HOW: Structured extraction with schema validation
  VALIDATE: Credibility scoring based on evidence and source

  WRITE FLOW:
    1. Agent completes task
    2. Extraction prompt identifies key learnings
    3. Learnings are classified by layer (working → team → domain → enterprise)
    4. Schema validation ensures format compliance
    5. Credibility score assigned based on:
       - Source authority (L1 > L2 > L3 > L4 > L5 > L6)
       - Evidence count (more evidence = higher credibility)
       - Recency (newer = higher, unless historical)
       - Validation status (peer-reviewed = higher)
    6. Memory entry stored in appropriate layer
    7. Knowledge graph updated with new nodes and edges

### 3.2 Memory Read

  WHEN: Before starting any task, making any decision, responding to any incident
  WHAT: Retrieve relevant context from all memory layers
  HOW: Semantic search + graph traversal + direct lookup
  FILTER: By relevance, credibility, recency, and domain

  READ FLOW:
    1. Agent receives task
    2. Task context is parsed for key concepts
    3. Memory query is constructed:
       - Working memory: Already loaded (agent-local)
       - Team memory: Query pod-specific knowledge
       - Domain memory: Semantic search for relevant patterns
       - Enterprise memory: Direct lookup for standards/policies
       - Knowledge graph: Traverse relationships for context
    4. Results are ranked by:
       - Relevance (semantic similarity)
       - Credibility (confidence score)
       - Recency (time since last validation)
       - Authority (source layer)
    5. Top results are injected into agent context
    6. Agent begins work with full context

### 3.3 Memory Update

  WHEN: When new evidence contradicts existing memory
  WHAT: Update credibility scores, add new evidence, mark conflicts
  HOW: Conflict detection → Evidence comparison → Resolution → Update

  UPDATE FLOW:
    1. New evidence arrives (incident, experiment, decision)
    2. Conflict detection: Does this contradict existing memory?
    3. If conflict:
       a. Compare evidence quality and quantity
       b. If clear winner: Update memory, mark old as superseded
       c. If ambiguous: Flag for human review
    4. If no conflict: Add as supporting evidence
    5. Recalculate credibility scores
    6. Update knowledge graph edges

### 3.4 Memory Delete

  WHEN: Memory is confirmed obsolete, incorrect, or expired
  WHAT: Archive (never truly delete) the memory entry
  HOW: Expiration check → Obsolescence detection → Archive → Cleanup

  DELETE FLOW:
    1. Scheduled job checks memory entries against expiration dates
    2. Entries past expiration are flagged for review
    3. Obsolescence detection:
       - No references in 90 days
       - Superseded by newer entry
       - Domain lead marks as obsolete
    4. Archived (moved to cold storage, not deleted)
    5. Knowledge graph edges pruned
    6. Index updated

---

## 4. Memory Search Architecture

### 4.1 Search Types

  SEMANTIC SEARCH
    Technology: Vector embeddings + cosine similarity
    Use: Finding conceptually related knowledge
    Example: "How do we handle concurrent updates to shared data?"
    Results: CRDT patterns, OT patterns, conflict resolution docs

  KEYWORD SEARCH
    Technology: Full-text search (Elasticsearch/Meilisearch)
    Use: Finding specific terms, APIs, error messages
    Example: "contacts API timeout 504"
    Results: Specific incident reports, known issues, fixes

  GRAPH TRAVERSAL
    Technology: Graph database queries
    Use: Finding related entities and relationships
    Example: "What services depend on the contacts API?"
    Results: Service dependency graph, affected teams, risk areas

  DIRECT LOOKUP
    Technology: Key-value store
    Use: Finding specific known items
    Example: "What is the SLO for the contacts API?"
    Results: Specific SLO definition, owner, current compliance

### 4.2 Search Ranking

Results are ranked by a composite score:
  SCORE = (0.4 × relevance) + (0.3 × credibility) + (0.2 × recency) + (0.1 × authority)

  relevance: Semantic similarity to query (0-1)
  credibility: Confidence score of the memory entry (0-1)
  recency: Time decay function (1.0 = today, 0.5 = 90 days ago, 0.1 = 1 year ago)
  authority: Source layer bonus (L1=1.0, L2=0.9, L3=0.8, L4=0.7, L5=0.6, L6=0.5)

---

## 5. Memory Governance

### 5.1 Memory Ownership

  | Memory Layer | Owner | Responsibility |
  |-------------|-------|----------------|
  | Working Memory | Individual Agent | Accuracy during task |
  | Team Memory | Pod Lead | Accuracy within sprint |
  | Domain Memory | Domain Lead | Accuracy within domain |
  | Enterprise Memory | Knowledge/Docs Lead | Accuracy across enterprise |
  | Knowledge Graph | Knowledge Engineer | Structural integrity |

### 5.2 Memory Quality Gates

  GATE 1: Schema Compliance
    Every memory entry must conform to its layer's schema.
    Non-compliant entries are rejected with specific error message.

  GATE 2: Credibility Threshold
    Memory entries below 0.3 credibility are flagged as "unverified."
    Entries below 0.1 are archived automatically.

  GATE 3: Conflict Resolution
    Conflicting entries must be resolved within 48 hours.
    Unresolved conflicts are escalated to the domain lead.

  GATE 4: Freshness Check
    Memory entries older than their validity period are flagged.
    Validity periods by type:
      - Technical patterns: 6 months
      - Business decisions: 12 months
      - Architecture decisions: Until superseded
      - Incident learnings: 3 years
      - Standards/policies: Until superseded

### 5.3 Memory Anti-Patterns

  ANTI-PATTERN: MEMORY OVERFLOW
    Description: Too much memory loaded into agent context
    Impact: Increased latency, reduced accuracy, token waste
    Prevention: Relevance filtering, pagination, summary compression
    Detection: Context window >80% full before task start

  ANTI-PATTERN: MEMORY HOARDING
    Description: Agents never delete or archive memory
    Impact: Stale decisions, contradictory guidance
    Prevention: Automatic expiration, quarterly review
    Detection: Memory entries without access in >90 days

  ANTI-PATTERN: MEMORY SILOS
    Description: Each pod maintains its own memory without sharing
    Impact: Duplicated knowledge, missed cross-domain insights
    Prevention: Mandatory cross-domain memory sync, shared search
    Detection: High duplication rate across pods

  ANTI-PATTERN: TRUSTING BAD MEMORY
    Description: Agent follows outdated or incorrect memory
    Impact: Wrong decisions, repeated mistakes
    Prevention: Credibility scoring, freshness checks, validation
    Detection: Decisions contradicted by newer evidence

---

## 6. Memory Integration with ELO

The ELO system is the primary consumer and producer of enterprise memory:

  ELO AS CONSUMER:
    - Reads domain memory to understand current state
    - Reads enterprise memory for strategic context
    - Reads knowledge graph for relationship context
    - Uses memory to inform scoring and recommendations

  ELO AS PRODUCER:
    - Produces learning patterns from cross-domain analysis
    - Validates memory entries through automated testing
    - Updates credibility scores based on outcomes
    - Identifies memory gaps and triggers discovery

  MEMORY-ELO FEEDBACK LOOP:
    1. Agent completes task → writes memory
    2. ELO reads memory → detects pattern
    3. ELO validates pattern → updates credibility
    4. Other agents read validated pattern → improve decisions
    5. Outcomes feed back into ELO → refine scoring

---

## 7. Memory Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Memory hit rate | >80% of queries return relevant results | Search analytics |
  | Memory freshness | >90% of entries within validity period | Scheduled audit |
  | Memory accuracy | >95% of entries validated as correct | Periodic review |
  | Cross-domain sharing | >60% of relevant cross-domain memory accessed | Access logs |
  | Conflict resolution time | <48 hours | Conflict tracking |
  | Memory write rate | >10 entries/agent/day | Write tracking |
  | Memory size growth | <20% per quarter | Storage monitoring |
  | Stale memory rate | <5% of total entries | Freshness audit |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
