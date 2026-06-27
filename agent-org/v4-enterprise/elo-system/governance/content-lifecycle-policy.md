# ELO GOVERNANCE: CONTENT LIFECYCLE MANAGEMENT
# Enterprise Learning Operations — Create → Review → Approve → Publish → Retire V1.0

## Purpose
Define the complete lifecycle for every learning content item in ELO.
No content exists outside this lifecycle.

---

## STAGE 1: CREATE/AUTHOR

**Owner:** T3 Research Feeder
**Duration:** Within each daily cycle (3 hours max)
**Entry Criteria:** Valid intelligence source identified and classified
**Exit Criteria:** Content drafted with source citations, metadata, and domain classification

**Validation Gates:**
- [ ] Content has unique ID (format: LP-[DOMAIN]-[DATE]-[CYCLE])
- [ ] Source URL documented
- [ ] Domain classification assigned
- [ ] Content type tagged (tutorial, news, tool, paper, case study)
- [ ] Minimum quality threshold met (rubric score ≥ 70)

---

## STAGE 2: REVIEW

**Owner:** T2 Domain Lead (primary) / T3 Peer (secondary)
**Duration:** < 2 hours from creation
**Entry Criteria:** Content exits CREATE stage with all validation gates passed
**Exit Criteria:** Content passes review rubric, or returned with revision notes

**Review Checklist:**
- [ ] Factual accuracy verified against source
- [ ] No hallucination/fabrication detected
- [ ] Content is up-to-date (freshness check)
- [ ] Source credibility score ≥ 7/10
- [ ] Cross-source verification completed for high-impact claims
- [ ] No duplicate content (within 30-day window)
- [ ] Appropriate for target agent skill level

**Review Outcomes:**
| Decision | Meaning | Action |
|---|---|---|
| Approve | Ready for next stage | Forward to APPROVE stage |
| Revise | Minor issues | Return to T3 with notes. 2-hour SLA for revision. |
| Reject | Major issues | Discard. Escalate to T1 if pattern. |
| Escalate | Needs T1 input | Forward to T1 Director |

---

## STAGE 3: APPROVE

**Owner:** T2 Domain Lead
**Duration:** < 1 hour from REVIEW approval
**Entry Criteria:** Content passes REVIEW stage
**Exit Criteria:** Content locked for publication

**Approval Gates:**
- [ ] Quality Score ≥ 80 (from rubric)
- [ ] Source Diversity Score verified (domain has > 6 unique sources this cycle)
- [ ] No quality flags from previous cycles
- [ ] Content aligns with current domain priorities

**Approval Outcomes:**
| Decision | Meaning | Action |
|---|---|---|
| Publish | Approved for delivery | Schedule for next cycle delivery |
| Hold | Temporarily paused | Move to holding queue. Auto-escalate after 24 hours. |
| Reject | Not approved | Return to CREATE stage with documentation. |

---

## STAGE 4: PUBLISH/DELIVER

**Owner:** ELO Delivery System (Automated)
**Duration:** Within scheduled cycle window
**Entry Criteria:** Content approved and scheduled
**Exit Criteria:** Delivery confirmed (heartbeat received from receiving agent)

**Delivery Verification:**
- [ ] Delivery heartbeat received from agent
- [ ] Content rendered correctly (no format errors)
- [ ] Delivery timestamp within cycle window
- [ ] Confirm delivery count matches scheduled count

**Failure Handling:**
- Failed delivery: Retry twice, then escalate to T2
- Partial delivery: Check remaining, retry within 30 min
- No heartbeat: Treat as failed, escalate

---

## STAGE 5: RETIRE/ARCHIVE

**Owner:** Automated (T2 audit)
**Trigger Conditions (ANY):**
- Content age > 90 days without review
- Quality Score drops below 60 on periodic reassessment
- Source becomes unavailable or credibility score < 4/10
- Domain priorities change and content no longer relevant
- Superseded by newer content on same topic

**Retirement Actions:**
1. Flag content as RETIRED (not deleted — preserved for audit trail)
2. Notify receiving agents of content retirement with alternative suggestion
3. Store in knowledge-base/archived/ with date stamp
4. Remove from active learning rotation

**Archival Retention:** 12 months minimum (GDPR/SOC2 compliance)
**Permanent Deletion:** Only after 12 months and T1 Director approval

---

## LIFECYCLE SLA SUMMARY

| Stage | Owner | Max Duration | Escalation |
|---|---|---|---|
| CREATE | T3 Feeder | 3 hours | T2 Lead |
| REVIEW | T2 Lead / T3 Peer | 2 hours | T1 Director |
| APPROVE | T2 Lead | 1 hour | T1 Director |
| PUBLISH | Auto | Cycle window | T2 Lead |
| RETIRE | Auto / T2 | 24 hours | T1 Director |

