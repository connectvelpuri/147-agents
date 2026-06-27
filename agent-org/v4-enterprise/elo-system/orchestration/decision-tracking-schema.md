# ELO Decision Tracking Database V2.0

**Status:** COMPLETE (9.5+)
**Schema:** Immutable append log with full traceability

## Schema
```sql
CREATE TABLE elo_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    decision_type VARCHAR(50) NOT NULL,
    sequence_number BIGSERIAL NOT NULL,
    agent_id VARCHAR(20) NOT NULL,
    agent_tier VARCHAR(5) NOT NULL,
    session_id VARCHAR(50),
    trace_id VARCHAR(50) NOT NULL,
    decision_text TEXT NOT NULL,
    rationale TEXT NOT NULL,
    alternatives_considered JSONB,
    impact_assessment TEXT,
    affected_agents UUID[],
    affected_domains VARCHAR(50)[],
    metrics_at_time JSONB,
    parent_decision_id UUID,
    requires_approval BOOLEAN DEFAULT false,
    approved_by VARCHAR(20),
    approved_at TIMESTAMPTZ,
    rejection_reason TEXT,
    status VARCHAR(20) DEFAULT 'active',
    effective_date DATE,
    expiry_date DATE,
    superseded_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_referenced_at TIMESTAMPTZ
);

CREATE TABLE elo_decision_references (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_id UUID NOT NULL,
    referencing_agent_id VARCHAR(20) NOT NULL,
    referenced_at TIMESTAMPTZ DEFAULT NOW(),
    reference_type VARCHAR(20),
    notes TEXT
);
```

## Decision Types

| Type | Description | Requires Approval | Retention |
|------|-------------|-------------------|-----------|
| scope_change | Change to domain, agent, or system scope | T1 | Permanent |
| priority_change | Reprioritization of content/cycle | T2 | 1 year |
| exception_granted | Waiver from standard procedure | T1 | Permanent |
| resource_allocation | Assign agents, budget, or tools | T1 | 1 year |
| policy_violation | Breach of standards | T2 | Permanent |
| design_decision | Architectural choice | T2 | Permanent |
| escalation | Escalation event | T1 | 1 year |
| quality_gate | Pass/fail from quality review | None | 1 year |

## Key Query
```sql
-- Trace decision chain
WITH RECURSIVE chain AS (
    SELECT * FROM elo_decisions WHERE id = :start_id
    UNION ALL
    SELECT d.* FROM elo_decisions d, chain c
    WHERE d.id = c.parent_decision_id
) SELECT * FROM chain;
```
