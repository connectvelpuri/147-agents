# ELO DOCUMENT 14: NEW-AGENT ONBOARDING PROTOCOL
# Enterprise Learning Operations — How New Agents Join ELO

---

## Auto-Onboarding Requirement
Every new operational agent MUST be connected to ELO within 24 hours of creation.
This is automatic. No manual action required by the founder.

---

## Onboarding Trigger
When a new operational agent JSON is created in the v4-enterprise/roles/ directory,
the ELO system detects it and triggers the onboarding protocol.

## Onboarding Steps (Automated)

### Step 1: Detection (Immediate)
- Scan roles/ directories for new agent files
- Extract agent ID, title, domain, role definition
- Compare against existing ELO mapping
- If not mapped: trigger onboarding

### Step 2: Classification (Within 1 hour)
- Analyze agent role definition
- Determine primary domain
- Determine skill requirements
- Identify certification needs
- Assign to appropriate Tier 2 Domain Lead

### Step 3: Profile Creation (Within 2 hours)
- Create agent L&D profile using schema
- Initialize skill map with default levels
- Initialize empty learning history
- Set up self-report schedule
- Connect to relevant Tier 3 feeders

### Step 4: Mapping Update (Within 4 hours)
- Update agent-to-tier2-mapping.json
- Add agent to Tier 2 lead's assigned agents
- Add agent to relevant Tier 3 feeder scan targets
- Update domain agent count

### Step 5: Learning Activation (Within 12 hours)
- Agent receives first learning pack at next cycle
- Agent receives onboarding learning pack with:
  - Domain fundamentals
  - Team context and processes
  - Relevant certifications
  - Key tools and frameworks
  - Initial skill assessment prompt

### Step 6: Integration Confirmation (Within 24 hours)
- Verify agent received learning pack
- Verify agent submitted first self-report
- Verify agent appears in domain dashboard
- Confirm onboarding complete

---

## Onboarding Learning Pack Contents

The onboarding pack includes:
1. **Domain Overview:** What this domain does, key concepts
2. **Team Context:** Who the agent works with, processes
3. **Current Sprint:** What the team is working on now
4. **Key Tools:** Tools this agent needs to know
5. **Certifications:** Recommended certifications for this role
6. **First Week Learning:** Structured learning path for first 7 days
7. **Self-Report Guide:** How to submit self-reports
8. **Quality Standards:** Expected quality for this role
9. **Escalation Guide:** When and how to escalate issues
10. **Contact Points:** Tier 2 lead and relevant Tier 3 feeders

---

## Onboarding Verification Checklist

| Check | Expected | Timeout |
|-------|----------|---------|
| Agent detected in roles/ | Within 1 hour | Automatic |
| L&D profile created | Within 2 hours | Automatic |
| Mapped to Tier 2 lead | Within 4 hours | Automatic |
| Connected to Tier 3 feeders | Within 4 hours | Automatic |
| First learning pack received | Within 12 hours | At next cycle |
| First self-report submitted | Within 24 hours | Agent deadline |
| Dashboard entry created | Within 24 hours | Automatic |
| Onboarding complete | Within 24 hours | Escalate if not |

---

## Re-connection Protocol (For Restructured Agents)

When an agent is moved to a different product or domain:

1. Detect agent ID still exists but domain changed
2. Disconnect from old Tier 2 lead
3. Re-classify for new domain
4. Re-map to new Tier 2 lead
5. Update L&D profile for new domain
6. Connect to new Tier 3 feeders
7. Send transition learning pack
8. Update certification track for new domain
9. Preserve learning history
10. Confirm reconnection within 24 hours

---

## De-connection Protocol (For Removed Agents)

When an agent is deactivated or removed:

1. Detect agent no longer in roles/ directories
2. Set agent status to "inactive" in L&D profile
3. Remove from Tier 2 lead's active agent list
4. Remove from Tier 3 feeder scan targets
5. Preserve L&D profile for historical records
6. Archive agent's learning history
7. Update domain agent count
8. Log deconnection in ELO audit trail

