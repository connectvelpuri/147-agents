# ELO DOCUMENT 6: LEARNING PACKET SCHEMA
# Enterprise Learning Operations — Daily Learning Pack Format

---

## Learning Pack Structure

Every learning pack delivered to an operational agent contains exactly 10 sections:

```json
{
  "pack_id": "LP-[DOMAIN]-[AGENT_ID]-[DATE]-[CYCLE]",
  "agent_id": "string",
  "domain": "string",
  "tier2_lead": "string",
  "cycle": "morning|midday|evening",
  "date": "YYYY-MM-DD",
  "generated_at": "ISO-8601 timestamp",
  "sections": {
    "top_trends": {
      "description": "Top 3-5 trends relevant to this agent's role today",
      "items": [
        {
          "trend": "string — what is trending",
          "source": "string — where this was found",
          "relevance": "string — why this matters for this agent",
          "action": "string — what the agent should do about it"
        }
      ]
    },
    "best_frameworks": {
      "description": "Best frameworks and patterns relevant to current work",
      "items": [
        {
          "framework": "string — framework name",
          "use_case": "string — when to use it",
          "source": "string — where to learn more",
          "applicability": "string — how it applies to current sprint tasks"
        }
      ]
    },
    "new_tools_releases": {
      "description": "New tools, versions, and releases relevant to this agent",
      "items": [
        {
          "tool": "string — tool name and version",
          "change": "string — what changed",
          "impact": "string — how it affects the agent's work",
          "action": "string — what to do about it"
        }
      ]
    },
    "github_implementation": {
      "description": "Real GitHub implementation example for learning",
      "items": [
        {
          "repo": "string — repository name and URL",
          "pattern": "string — what pattern it demonstrates",
          "relevance": "string — how it applies to this agent's work",
          "key_files": "array — specific files to study"
        }
      ]
    },
    "practitioner_case": {
      "description": "Real-world practitioner case study",
      "items": [
        {
          "case": "string — what happened",
          "context": "string — the situation",
          "solution": "string — what they did",
          "result": "string — what happened",
          "lesson": "string — what to learn from it"
        }
      ]
    },
    "expert_insight": {
      "description": "Expert insight from practitioner community",
      "items": [
        {
          "insight": "string — the expert insight",
          "expert": "string — who said it (if named)",
          "source": "string — where to find more",
          "application": "string — how to apply this"
        }
      ]
    },
    "mistake_to_avoid": {
      "description": "Common production mistake to avoid",
      "items": [
        {
          "mistake": "string — what the mistake is",
          "consequence": "string — what happens when you make it",
          "prevention": "string — how to avoid it",
          "example": "string — real-world example"
        }
      ]
    },
    "certification_recommendation": {
      "description": "Certification or learning path recommendation",
      "items": [
        {
          "certification": "string — certification name",
          "provider": "string — certification provider",
          "relevance": "string — why this is relevant now",
          "next_step": "string — what to do next",
          "roi": "string — expected return on investment"
        }
      ]
    },
    "applied_exercise": {
      "description": "Practical exercise to apply learning",
      "items": [
        {
          "exercise": "string — what to do",
          "time_estimate": "string — how long it takes",
          "expected_outcome": "string — what you'll learn",
          "resources_needed": "array — tools/references needed"
        }
      ]
    },
    "improvement_suggestion": {
      "description": "Suggested improvement to current work",
      "items": [
        {
          "current": "string — how things are done now",
          "suggested": "string — how they could be done better",
          "rationale": "string — why this is better",
          "effort": "string — how much effort to implement",
          "impact": "string — expected impact"
        }
      ]
    }
  },
  "quality_score": "number — quality score of this pack (0-100)",
  "source_diversity": "number — unique sources used in this pack",
  "applicability_score": "number — how applicable to current work (0-100)"
}
```

---

## Pack Quality Standards

| Section | Minimum Items | Maximum Items | Quality Requirement |
|---------|--------------|---------------|-------------------|
| top_trends | 3 | 5 | Each must be <7 days old |
| best_frameworks | 2 | 4 | Each must have source URL |
| new_tools_releases | 1 | 3 | Must be within 30 days |
| github_implementation | 1 | 2 | Must have working code example |
| practitioner_case | 1 | 2 | Must be real-world, not hypothetical |
| expert_insight | 1 | 3 | Must be attributed |
| mistake_to_avoid | 1 | 2 | Must have real consequence |
| certification_recommendation | 1 | 1 | Must be role-specific |
| applied_exercise | 1 | 2 | Must be completable in <2 hours |
| improvement_suggestion | 1 | 2 | Must be specific to current work |

---

## Pack Delivery Rules

1. Every pack must be delivered within the assigned cycle window
2. Every pack must contain all 10 sections
3. Every item must have a source attribution
4. Every pack must be role-specific (not generic)
5. Every pack must be actionable within the same work cycle
6. No pack may contain motivational filler
7. No pack may contain stale content (>7 days for trends, >30 days for tools)
8. No pack may contain repeated recommendations from previous packs
9. Every pack must include at least 6 unique sources
10. Every pack must be quality-scored above 60/100

