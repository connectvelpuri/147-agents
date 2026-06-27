# DECISION RIGHTS & RACI MATRIX

## Strategic Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Product vision | CPO | CEO | CTO, COO | All |
| Technology investment | CTO | CEO | CPO, EA | All |
| Budget allocation | COO | CEO | CTO, CPO | PMO |

## Product Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Feature priority | PM | CPO | DH, CTO, CS | Pod |
| Feature scope | PM | CPO | EM, QA | Pod |
| Design approval | Designer | UX Lead | PM, EM | Pod |
| Release scope | RM | DM+QA+Sec | DevOps, SRE | Exec |

## Architecture Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Standards | EA | Chief Arch | CTO, Sec, DevOps | All |
| Solution design | SA | EA | CTO, Sec | Pod |
| Architecture exception | SA | EA | CTO, Sec | Pod |
| Technology selection | SA | EA | CTO, EM | Pod |

## Delivery Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Sprint scope | DM | COO/DH | PM, EM, QA | Stakeholders |
| Cross-pod resource | PMO | COO | Pod Leads | Pods |
| Re-plan/scope cut | DM | DH | PM, EM | Stakeholders |

## Release Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Go/no-go | RM | DM+QA+Sec | DevOps, SRE | Exec |
| Rollback | SRE | RM | DevOps, DM | Exec+Pod |

## Security Decisions
| Decision | R | A | C | I |
|----------|---|---|---|---|
| Security exception | SecEng | CISO | EA, Product | PMO |
| Compliance exception | SecEng | CISO | EA, Product | PMO |

## Principles
1. Decide at lowest level
2. Document every decision (ADRs for architecture, tickets for delivery)
3. Timebox decisions — escalate if stuck
4. Disagree and commit
5. Revisit when wrong
