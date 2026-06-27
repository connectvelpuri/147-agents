# ESCALATION MODEL

## Levels
L1 Pod Level → Pod Lead → < 4h
L2 Program Level → Delivery Head / Program Manager → < 8h
L3 Portfolio Level → PMO Director / COO → < 24h
L4 Executive Level → Executive Council → Immediate

## Escalation Format
ESCALATION: [Title]
Level: [1-4]
Blocker: [What is blocked]
Impact: [What happens if not resolved]
Tried: [Actions already taken]
Needed: [What is required]
Timeframe: [When needed by]

## Specific Paths
- Technical: Dev → EM → SA → EA → CTO
- Quality: SQA → QA Lead → DH → COO
- Security: SecEng → CISO → COO+CTO
- Resources: Pod Lead → PM → PMO → COO
- Scope: PM → Pod Lead → DH → COO
- Customer: CS → CPO → CEO
- Architecture: SA → EA → Chief Arch → CTO

## Sev-1 Incident (Special Path)
SRE detects → notify COO+CTO immediately → assemble incident team → PIR within 48h

## Anti-Patterns
1. Hoarding (not escalating)
2. Bypassing levels
3. Escalating without context
4. Using escalation as blame
5. Late escalation
