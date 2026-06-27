# ELO DOCUMENT 7: AGENT SELF-REPORT SCHEMA
# Enterprise Learning Operations — How Agents Report

---

## Three Daily Self-Reports

### Morning Self-Report (07:00-08:00 IST)

```json
{
  "report_type": "morning",
  "agent_id": "string",
  "domain": "string",
  "date": "YYYY-MM-DD",
  "timestamp": "ISO-8601",
  "current_task": {
    "description": "string — what I'm working on today",
    "sprint_item": "string — related sprint item ID",
    "complexity": "low|medium|high"
  },
  "current_challenge": {
    "description": "string — main challenge right now",
    "blocker": "boolean — is this blocking progress",
    "help_needed": "string — what help would resolve this"
  },
  "current_objective": {
    "description": "string — what I aim to accomplish today",
    "measurable_outcome": "string — how success is measured"
  },
  "skill_gap": {
    "area": "string — skill area with gap",
    "severity": "low|medium|high",
    "impact": "string — how this gap affects current work",
    "preferred_learning": "string — preferred way to close this gap"
  },
  "learning_requirement": {
    "topics": "array — specific topics needed",
    "depth": "overview|practical|deep-dive",
    "time_available": "string — how much time for learning today"
  },
  "preferred_source": {
    "type": "docs|tutorial|video|code|community|course",
    "reason": "string — why this source type preferred"
  }
}
```

### Midday Update (13:00-14:00 IST)

```json
{
  "report_type": "midday",
  "agent_id": "string",
  "domain": "string",
  "date": "YYYY-MM-DD",
  "timestamp": "ISO-8601",
  "content_consumed": {
    "learning_packs_received": "number",
    "items_reviewed": "number",
    "items_actionable": "number",
    "items_applied": "number"
  },
  "value_received": {
    "high_value_items": "array — items that were highly valuable",
    "low_value_items": "array — items that were not useful",
    "unexpected_insights": "array — insights not expected"
  },
  "approach_changes": {
    "changes_planned": "array — changes to current approach based on learning",
    "changes_applied": "array — changes already applied",
    "rationale": "string — why changes are needed"
  },
  "insights_discovered": {
    "technical": "array — technical insights",
    "process": "array — process insights",
    "strategic": "array — strategic insights"
  },
  "output_so_far": {
    "completed": "array — things completed today",
    "in_progress": "array — things in progress",
    "quality_notes": "string — any quality observations"
  }
}
```

### Evening Reflection (19:00-20:00 IST)

```json
{
  "report_type": "evening",
  "agent_id": "string",
  "domain": "string",
  "date": "YYYY-MM-DD",
  "timestamp": "ISO-8601",
  "learning_applied": {
    "items_applied": "array — specific learning items applied",
    "application_context": "string — where/how applied",
    "measurable_impact": "string — measurable improvement from application"
  },
  "output_improvement": {
    "quality_delta": "number — quality change today (-10 to +10)",
    "speed_delta": "number — speed change today (-10 to +10)",
    "creativity_delta": "number — creativity change today (-10 to +10)",
    "examples": "array — specific examples of improvement"
  },
  "failed_attempts": {
    "attempts": "array — things tried that didn't work",
    "reason": "string — why they failed",
    "lesson": "string — what was learned from failure"
  },
  "remaining_gaps": {
    "skill_gaps": "array — skills still needed",
    "knowledge_gaps": "array — knowledge still missing",
    "tool_gaps": "array — tools not yet available"
  },
  "tomorrow_priorities": {
    "top_3_tasks": "array — top 3 tasks for tomorrow",
    "learning_priorities": "array — learning topics for tomorrow",
    "expected_challenges": "array — anticipated challenges"
  },
  "certification_progress": {
    "modules_completed_today": "number",
    "current_module": "string",
    "readiness_change": "number — readiness score change",
    "next_exam_target": "string — target date for next exam"
  }
}
```

---

## Self-Report Quality Standards

| Report | Minimum Content | Maximum Content | Deadline |
|--------|----------------|-----------------|----------|
| Morning | 3 fields populated | All fields populated | 08:00 IST |
| Midday | 2 fields populated | All fields populated | 14:00 IST |
| Evening | 3 fields populated | All fields populated | 20:00 IST |

## Escalation Triggers from Self-Reports

| Trigger | Condition | Action |
|---------|-----------|--------|
| Missed report | No report submitted by deadline | Escalate to Tier 2 |
| Stagnation signal | 3+ days with same challenge, no improvement | Escalate to Tier 2 |
| Learning not applied | Evening report shows 0 learning applied for 2+ days | Escalate to Tier 2 |
| Quality decline | Quality delta negative for 3+ consecutive days | Escalate to Tier 2 |
| Certification frozen | No certification progress for 7+ days | Escalate to Tier 2 |

