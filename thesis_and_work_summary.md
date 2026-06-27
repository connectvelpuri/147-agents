# Sovereign CRM: Thesis Thinking and Work Summary

## Core Thesis
The Sovereign CRM project is founded on the belief that enterprises need a truly open-source, privacy-first CRM alternative that avoids vendor lock-in while providing enterprise-grade functionality. Current market leaders (Salesforce, HubSpot) create dependency through proprietary ecosystems, high costs, and data sovereignty concerns. Sovereign CRM addresses this by:

1. **Technical Sovereignty**: Built on open-source stack (Go, Next.js, Supabase) with self-hostable architecture
2. **Data Sovereignty**: Customer data remains under user control via Supabase PostgreSQL
3. **Operational Sovereignty**: Minimal dependencies, avoidant of surveillance capitalism models
4. **Strategic Sovereignty**: Executive agent methodology ensures rigorous, Big 4-level strategic oversight

The thesis posits that open-source CRMs can compete with proprietary solutions not through feature parity alone, but through superior architecture, community-driven innovation, and alignment with user sovereignty values.

## Current Project Status
- **Sprint**: 5 (in progress)
- **Previous Sprint (4) Complete**: Email, sequences, workflows, reports modules
- **Stack**: Go (backend) + Next.js (frontend) + Supabase (backend services)
- **Database**: `sovereign/sovereign` (PostgreSQL via Supabase)
- **Go API**: chi router + pgxpool.Pool
- **Vault**: `sovereign_crm_vault/` (for research/docs - NEVER committed to Git)
- **DB Password**: 'sovereign' (SCRAM-SHA-256)

## Key Technical Decisions & Learnings
1. **Go Backend**:
   - Using chi router for middleware composition
   - pgxpool.Pool for efficient database connections
   - **Critical**: pgx NULL handling - MUST use COALESCE for nullable columns or *string pointers in structs
   - Avoid @ts-nocheck in Next.js 14+ (use ignoreBuildErrors in next.config.js instead)

2. **Architecture Principles**:
   - Strict separation: research/vault vs. source code (Git)
   - Multi-session workflow: named sessions for continuity
   - Prefer Reddit/forum/Grok validation over customer discovery calls
   - Open-source infrastructure preference (Podman, Supabase, Ollama)

3. **Current Focus (Sprint 5)**:
   - Fixing runtime bugs from Sprint 4 delivery
   - Refining email, sequences, workflows, and reports modules
   - Addressing pgx NULL handling edge cases
   - Ensuring Next.js 14+ compatibility

## User Preferences & Workflow
- **Executive Agent Behavior**: Expects high-agency, autonomous decisions with Big 4-level strategic audits
- **Methodology**: Strict plan → audit → approve → execute sequence (must be followed)
- **Communication**: Values honest critical feedback over politeness
- **Work Style**: Multi-session worker; batch execution mode for "complete all remaining" directives
- **Validation**: Prefers market feedback via Reddit/forums/Grok instead of discovery calls
- **Infrastructure**: Strong preference for open-source tools

## Research Constraints & Adaptations
- **Bot Detection**: Major research platforms (G2, Capterra, Trustpilot, Brave, Google, Reddit) block automated access
- **Adaptation**: Use old.reddit.com, hn.algolia.com, GitHub API for research
- **Delegation Limitation**: delegate_task subagents return thin results for web research - critical research must be done directly
- **Vault Discipline**: All strategic research/blueprints stored in sovereign_crm_vault - NEVER in Git repository

## Open Questions for Future Work
1. How to balance open-source development with enterprise sales motion?
2. Optimal community governance model for CRM project sustainability?
3. Integration pathways with existing open-source business tools (accounting, marketing, etc.)
4. Measurement framework for sovereignty-focused value proposition vs. feature-checklist competition

---
*Document created: $(date)*
*Stored in Sovereign CRM Vault per user requirements*
