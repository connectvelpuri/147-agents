# ELO GOVERNANCE: CONTENT QUALITY RUBRIC
# Enterprise Learning Operations — Automated Quality Standards V1.0

## Purpose
Define minimum quality thresholds for all learning content processed by ELO.
Every learning pack must score ≥ 80/100 to be delivered to operational agents.

---

## QUALITY DIMENSIONS (Weighted Scoring)

### Dimension 1: Learning Objectives Clarity (Weight: 15)
**Assessment Questions:**
- Are learning objectives clearly stated at the pack header? (0-10)
- Are objectives measurable/assessable? (0-10)  
- Are objectives aligned with the agent's domain? (0-10)
- Can a reader explain what they'll learn after reading? (0-10)

**Scoring:**
- 0-3: No objectives OR objectives are vague/non-measurable
- 4-6: Objectives stated but not assessable
- 7-9: Clear, measurable, assessable objectives
- 10: Objectives exceed expectations with real-world application context

**Weighted Max:** 15 points (max 10 × weight 1.5)

### Dimension 2: Content Accuracy & Verifiability (Weight: 25) ★ HIGHEST WEIGHT
**Assessment Questions:**
- Are sources cited for factual claims? (0-10)
- Are citations traceable back to original source? (0-10)
- Is the information consistent with current domain knowledge? (0-10)
- Are there unambiguous factual errors? (-10 penalty per error)

**Scoring:**
- 0-3: No citations, claims unverifiable
- 4-6: Some citations but not all claims supported
- 7-9: Every claim has a verifiable source
- 10: Sources are primary/original (not derivative)

**Weighted Max:** 25 points

### Dimension 3: Recency & Freshness (Weight: 15)
**Assessment Questions:**
- Is the content < 90 days from publication? (0-10)
- Has the content been reviewed within its lifecycle? (0-10)
- Does the content reference current tools/methods/versions? (0-10)

**Scoring:**
- 0-3: > 180 days old, outdated references
- 4-6: 90-180 days, partially outdated
- 7-9: < 90 days, current references
- 10: < 30 days, cutting-edge content

**Weighted Max:** 15 points

### Dimension 4: Domain Relevance (Weight: 15)
**Assessment Questions:**
- Is the content directly applicable to the target domain? (0-10)
- Does the content address current problems/challenges? (0-10)
- Is the depth appropriate for the target agent's level? (0-10)

**Scoring:**
- 0-3: Tangential or generic content
- 4-6: Partially relevant but not specific to domain
- 7-9: Directly applicable to domain
- 10: Solves a known problem in the domain

**Weighted Max:** 15 points

### Dimension 5: Actionability (Weight: 20)
**Assessment Questions:**
- Does the content provide actionable insights? (0-10)
- Can the agent apply this knowledge immediately? (0-10)
- Are next steps or implementation guidance included? (0-10)

**Scoring:**
- 0-3: Purely theoretical or informational
- 4-6: Some actionable elements but unclear
- 7-9: Clear action items with implementation guidance
- 10: Ready-to-use code, configs, or procedures

**Weighted Max:** 20 points

### Dimension 6: Readability & Structure (Weight: 10)
**Assessment Questions:**
- Is the content well-structured (headings, paragraphs, lists)? (0-10)
- Is the language clear and free of jargon without explanation? (0-10)
- Is the length appropriate (not overwhelming, not too brief)? (0-10)

**Scoring:**
- 0-3: Wall of text, poor structure
- 4-6: Some structure but hard to scan
- 7-9: Well-structured, easy to read
- 10: Excellent structure, ideal format for agent consumption

**Weighted Max:** 10 points

---

## TOTAL SCORE CALCULATION
```
Quality_Score = (L0_Clarity × 1.5) + (Accuracy × 2.5) + (Recency × 1.5) + (Relevance × 1.5) + (Actionability × 2.0) + (Readability × 1.0)
```

## QUALITY GATES
| Score Range | Classification | Action Required |
|---|---|---|
| 90-100 | Excellent | Deliver immediately. Audit quarterly. |
| 80-89 | Good | Deliver. Review monthly. |
| 70-79 | Marginal | T2 Lead review required before delivery. |
| 50-69 | Poor | Return to T3 for revision. No delivery. |
| 0-49 | Unacceptable | Discard. Escalate to T1. |

## QUALITY FAILURE ACTIONS
- **Score < 80:** Learning pack NOT delivered. T3 feeder alerted.
- **Score < 70 for 3 consecutive packs:** T3 feeder quality audit triggered.
- **Score < 50:** T1 director notified. Source credibility review initiated.

## AUDIT REQUIREMENTS
- Automated scoring on every pack (100% sampling)
- Manual scoring audit on 5% random sample weekly
- Inter-rater reliability check monthly (> 0.80 Cohen's Kappa)

