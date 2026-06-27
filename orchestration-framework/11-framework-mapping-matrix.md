# 11 — Framework Mapping Matrix

## How Every Framework Maps to the Sovereign Enterprise Architecture

---

## Executive Summary

The Sovereign Enterprise does not use a single framework. It integrates the best
concepts from 8 major agent frameworks into a unified architecture. This document
maps each framework's strengths to specific Sovereign Enterprise layers, explains
what is borrowed from each, and defines how they work together without conflict.

The frameworks are NOT adopted wholesale. Each is evaluated, its best concepts
are extracted, and those concepts are woven into the enterprise architecture.
The result is a hybrid system that is more capable than any single framework.

---

## 1. Framework Overview

### 1.1 Frameworks Integrated

  1. CrewAI — Role-based team collaboration
  2. LangGraph — Stateful workflow orchestration
  3. LangChain — Tool integration and chaining
  4. Semantic Kernel — Planning, memory, and tool orchestration
  5. AgentScope — Multi-agent simulation and coordination
  6. MetaGPT — Structured artifact generation and delivery
  7. AutoGPT — Autonomous task decomposition (historical concepts)
  8. Phidata — Knowledge retrieval and agent tooling
  9. SuperAGI — Agent lifecycle and marketplace concepts
  10. Team Topologies — Organizational design patterns
  11. Product Operating Model — Product management practices
  12. OODA Loop — Rapid decision-making cycle
  13. Double-Loop Learning — Organizational learning
  14. Wardley Mapping — Strategic evolution analysis
  15. Domain-Driven Design — Architecture patterns

---

## 2. CrewAI Mapping

### 2.1 What CrewAI Provides

  CrewAI is a framework for orchestrating role-based AI agent teams.
  Core concepts:
    - CREW: A team of agents working toward a goal
    - AGENT: Individual team member with a role, goal, and backstory
    - TASK: Specific assignment with expected output
    - TOOL: Capability an agent can use (search, code, API)
    - PROCESS: Sequential, hierarchical, or parallel execution

### 2.2 What We Borrow

  | CrewAI Concept | Sovereign Enterprise Usage | Layer |
  |---------------|---------------------------|-------|
  | Crew (team) | Pod structure (CRM Core Pod, Platform Pod, etc.) | L3-L5 |
  | Agent (role) | Agent catalog roles (PM, Eng, QA, DevOps) | All layers |
  | Task (assignment) | Sprint backlog items, ad-hoc tasks | L3-L5 |
  | Tool (capability) | Agent tool configurations | L4-L5 |
  | Hierarchical process | Layer-to-layer command chain | L1-L6 |
  | Sequential process | SDLC workflow pipeline | L3-L5 |
  | Delegation | Cross-pod task delegation via Delivery Manager | L2-L5 |

### 2.3 How We Extend CrewAI

  CrewAI lacks:
    - Enterprise governance (we add: Document 07)
    - Memory architecture (we add: Document 03)
    - Conflict resolution (we add: Document 06)
    - Human oversight gates (we add: Document 17)
    - Lifecycle management (we add: Document 09)

  Our extension: CrewAI pods operate within the governance framework.
  Pods have autonomy, but cross-pod and cross-layer interactions follow
  the enterprise coordination protocols.

---

## 3. LangGraph Mapping

### 3.1 What LangGraph Provides

  LangGraph is a framework for building stateful, multi-actor applications
  with LLMs. Core concepts:
    - GRAPH: Directed graph of nodes (agents/actions)
    - STATE: Shared state between nodes
    - EDGES: Transitions between nodes (conditional and static)
    - CHECKPOINTING: Save and resume graph execution
    - HUMAN-IN-THE-LOOP: Pause for human input

### 3.2 What We Borrow

  | LangGraph Concept | Sovereign Enterprise Usage | Layer |
  |------------------|---------------------------|-------|
  | State graph | SDLC workflow pipeline (Document 01) | L3-L5 |
  | Shared state | Shared context framework (Document 08) | All layers |
  | Conditional edges | Decision framework routing (Document 04) | L2-L5 |
  | Checkpointing | Incident response blackboard (Document 01) | L5-L6 |
  | Human-in-the-loop | Mandatory human gates (Document 17) | All layers |
  | Sub-graphs | Pod-level workflows within enterprise workflows | L3-L5 |

### 3.3 How We Extend LangGraph

  LangGraph lacks:
    - Multi-product scaling (we add: Document 10)
    - Role-based organization (we add: from CrewAI)
    - Knowledge management (we add: Document 15)
    - Continuous improvement (we add: Document 16)

  Our extension: LangGraph powers the workflow execution engine.
  The coordination layer (Document 12) manages which graphs run,
  how they interact, and how state is shared across graphs.

---

## 4. Semantic Kernel Mapping

### 4.1 What Semantic Kernel Provides

  Semantic Kernel is Microsoft's AI orchestration framework.
  Core concepts:
    - PLANNER: Automatically determines steps to achieve a goal
    - MEMORY: Semantic and chat history memory
    - PLUGINS: Modular capabilities (tools, services, data)
    - CHAINING: Sequential and parallel function composition

### 4.2 What We Borrow

  | Semantic Kernel Concept | Sovereign Enterprise Usage | Layer |
  |------------------------|---------------------------|-------|
  | Planner | Agent task planning and decomposition | L4-L5 |
  | Semantic memory | Enterprise knowledge base (Document 15) | All layers |
  | Chat history memory | Agent working memory (Document 03) | L4-L5 |
  | Plugins | Agent tool configuration | L4-L5 |
  | Function chaining | Workflow step composition | L3-L5 |

### 4.3 How We Extend Semantic Kernel

  Semantic Kernel lacks:
    - Multi-agent coordination (we add: CrewAI concepts)
    - Enterprise governance (we add: Document 07)
    - Conflict resolution (we add: Document 06)
    - Scaling architecture (we add: Document 10)

  Our extension: Semantic Kernel powers individual agent intelligence.
  The enterprise coordination layer manages how agents interact.

---

## 5. AgentScope Mapping

### 5.1 What AgentScope Provides

  AgentScope is a multi-agent simulation platform.
  Core concepts:
    - AGENT: Autonomous entity with message handling
    - MESSAGE: Structured communication between agents
    - PIPELINE: Sequential message processing
    - SERVICE: Shared infrastructure for agents
    - DISTRIBUTED: Multi-machine agent deployment

### 5.2 What We Borrow

  | AgentScope Concept | Sovereign Enterprise Usage | Layer |
  |-------------------|---------------------------|-------|
  | Message passing | Communication protocols (Document 02) | All layers |
  | Pipeline | Workflow execution (Document 01) | L3-L5 |
  | Service sharing | Shared infrastructure and tools | L4-L5 |
  | Distributed deployment | Multi-region scaling (Document 10) | L2-L6 |
  | Multi-agent simulation | Organizational design testing | L1-L2 |

### 5.3 How We Extend AgentScope

  AgentScope lacks:
    - Enterprise-scale governance (we add: Document 07)
    - Human oversight (we add: Document 17)
    - Knowledge management (we add: Document 15)
    - Lifecycle management (we add: Document 09)

  Our extension: AgentScope concepts inform the communication layer.
  The coordination layer (Document 12) provides the enterprise context.

---

## 6. MetaGPT Mapping

### 6.1 What MetaGPT Provides

  MetaGPT simulates a software company with multiple roles.
  Core concepts:
    - ROLE: Specialized agent (Product Manager, Architect, Engineer, QA)
    - ARTIFACT: Structured output (PRD, design doc, code, test report)
    - STANDARDIZED OUTPUT: Each role produces specific document types
    - WATERFALL-LIKE: Sequential role execution with artifact handoff

### 6.2 What We Borrow

  | MetaGPT Concept | Sovereign Enterprise Usage | Layer |
  |----------------|---------------------------|-------|
  | Role specialization | Agent catalog roles (25 roles + 15 skills) | All layers |
  | Structured artifacts | SDLC deliverables (PRD, HLD, LLD, test report) | L3-L5 |
  | Standardized output | Quality gates require specific artifacts | L3-L5 |
  | Role sequencing | SDLC phase transitions | L3-L5 |
  | Artifact handoff | Cross-role workflow transitions | L3-L5 |

### 6.3 How We Extend MetaGPT

  MetaGPT lacks:
    - Concurrent execution (we add: from CrewAI parallel processing)
    - Enterprise governance (we add: Document 07)
    - Feedback loops (we add: Double-Loop Learning from Document 16)
    - Human oversight (we add: Document 17)

  Our extension: MetaGPT concepts define what each role produces.
  The governance framework ensures quality and oversight.

---

## 7. AutoGPT Mapping

### 7.1 What AutoGPT Provides (Historical)

  AutoGPT pioneered autonomous task decomposition.
  Core concepts (historical, not primary):
    - GOAL: User-defined objective
    - PLAN: Decomposed task list
    - EXECUTE: Autonomous task execution
    - EVALUATE: Check if goal is achieved
    - ITERATE: Refine approach based on results

### 7.2 What We Borrow

  | AutoGPT Concept | Sovereign Enterprise Usage | Layer |
  |----------------|---------------------------|-------|
  | Goal decomposition | Sprint goal → task breakdown | L3-L4 |
  | Self-evaluation | Agent quality self-checks | L4-L5 |
  | Iteration | Continuous improvement loops (Document 16) | All layers |
  | Memory management | Local agent memory (Document 03) | L4-L5 |

### 7.3 What We Do NOT Borrow

  - Fully autonomous goal pursuit without human oversight
  - Self-modifying prompts or tools
  - Unbounded task execution
  Reason: These patterns are dangerous at enterprise scale.

---

## 8. Phidata Mapping

### 8.1 What Phidata Provides

  Phidata is a framework for building AI assistants with knowledge.
  Core concepts:
    - ASSISTANT: AI agent with tools and knowledge
    - KNOWLEDGE: Structured data sources for retrieval
    - TOOL: Function calling capabilities
    - MEMORY: Conversation and user memory

### 8.2 What We Borrow

  | Phidata Concept | Sovereign Enterprise Usage | Layer |
  |----------------|---------------------------|-------|
  | Knowledge bases | Enterprise knowledge management (Document 15) | All layers |
  | Retrieval | Context retrieval for agents (Document 08) | All layers |
  | Tool definitions | Agent tool configuration | L4-L5 |
  | Memory | Agent working + team memory (Document 03) | L4-L6 |

### 8.3 How We Extend Phidata

  Phidata lacks:
    - Multi-agent coordination (we add: CrewAI + LangGraph)
    - Enterprise governance (we add: Document 07)
    - Scaling architecture (we add: Document 10)
    - Conflict resolution (we add: Document 06)

  Our extension: Phidata powers the knowledge retrieval layer.
  The coordination layer manages how knowledge is shared.

---

## 9. Team Topologies Mapping

### 9.1 What Team Topologies Provides

  Team Topologies defines four team types:
    - STREAM-ALIGNED TEAM: Aligned to a business flow
    - PLATFORM TEAM: Provides internal services
    - ENABLING TEAM: Helps others adopt new practices
    - COMPLICATED-SUBSYSTEM TEAM: Manages complex components

### 9.2 What We Borrow

  | Team Topologies Concept | Sovereign Enterprise Usage | Layer |
  |------------------------|---------------------------|-------|
  | Stream-aligned team | Product pods (CRM Core, CRM Intelligence) | L3-L5 |
  | Platform team | Platform Pod (CI/CD, infra, monitoring) | L4-L5 |
  | Enabling team | Knowledge/Docs Lead + Continuous Improvement | L6 |
  | Complicated-subsystem team | Data/AI specialists within pods | L4 |
  | Team API | Pod interaction protocols (Document 02) | L3-L5 |
  | Cognitive load limits | Pod size limits (5-8 agents) | L3-L5 |

---

## 10. OODA Loop Mapping

### 10.1 What OODA Provides

  OODA (Observe-Orient-Decide-Act) is a decision-making framework:
    - OBSERVE: Gather information about the situation
    - ORIENT: Analyze information in context
    - DECIDE: Choose a course of action
    - ACT: Execute the decision

### 10.2 What We Borrow

  | OODA Concept | Sovereign Enterprise Usage | Layer |
  |-------------|---------------------------|-------|
  | Observe | Monitoring and alerting (operational context) | L5-L6 |
  | Orient | Shared context framework (Document 08) | All layers |
  | Decide | Decision framework (Document 04) | L2-L5 |
  | Act | Task execution and workflow (Document 01) | L3-L5 |
  | Loop speed | Incident response SLA targets | L5-L6 |

---

## 11. Double-Loop Learning Mapping

### 11.1 What Double-Loop Learning Provides

  Single-loop learning: "Did we execute correctly?"
  Double-loop learning: "Should we be doing this at all?"

  Double-loop learning challenges underlying assumptions, not just
  execution quality.

### 11.2 What We Borrow

  | Double-Loop Concept | Sovereign Enterprise Usage | Layer |
  |--------------------|---------------------------|-------|
  | Single-loop | Sprint retrospectives, RCA | L3-L6 |
  | Double-loop | Quarterly strategy reviews, architecture reassessment | L1-L3 |
  | Reflective inquiry | Blameless post-mortems | All layers |
  | Theory-in-use vs espoused | Agent behavior auditing | All layers |

---

## 12. Domain-Driven Design Mapping

### 12.1 What DDD Provides

  DDD defines bounded contexts and domain modeling:
    - BOUNDED CONTEXT: Distinct business domain with its own model
    - AGGREGATE: Cluster of entities with transactional consistency
    - DOMAIN EVENT: Something that happened in the domain
    - DOMAIN SERVICE: Operation that doesn't belong to an entity

### 12.2 What We Borrow

  | DDD Concept | Sovereign Enterprise Usage | Layer |
  |------------|---------------------------|-------|
  | Bounded context | Domain boundaries (CRM, ERP, HR, Finance) | All layers |
  | Aggregate | Pod-level data ownership | L3-L5 |
  | Domain event | Event bus event types (Document 01) | All layers |
  | Domain service | Cross-pod services | L4-L5 |
  | Ubiquitous language | Domain glossary in knowledge base | All layers |

---

## 13. Integration Architecture

### 13.1 How Frameworks Work Together

  LAYER 1 (Organizational Governance):
    Frameworks: Team Topologies, Product Operating Model
    Purpose: Define team structure, roles, and interaction modes

  LAYER 2 (Agent Orchestration):
    Frameworks: LangGraph (workflows), Semantic Kernel (planning)
    Purpose: Execute workflows, plan tasks, manage state

  LAYER 3 (Team Collaboration):
    Frameworks: CrewAI (role-based teams)
    Purpose: Multi-agent teamwork within pods

  LAYER 4 (Enterprise Memory):
    Frameworks: Phidata (knowledge), Semantic Kernel (memory)
    Purpose: Shared intelligence and context

  LAYER 5 (Learning):
    Frameworks: ELO system, OODA Loop, Double-Loop Learning
    Purpose: Capability growth and organizational learning

  LAYER 6 (Continuous Improvement):
    Frameworks: PDCA, Systems Thinking, Wardley Mapping
    Purpose: Self-improvement and strategic evolution

### 13.2 Framework Conflict Resolution

  When frameworks suggest different approaches:
    1. Enterprise architecture standards take precedence
    2. If no standard exists: Enterprise Architect decides
    3. If frameworks conflict: Choose the one that fits the context
    4. Document the choice as an ADR
    5. Review the choice quarterly

---

## 14. Framework Metrics

  | Metric | Target | Measured By |
  |--------|--------|-------------|
  | Framework utilization | >80% of concepts actively used | Usage audit |
  | Framework conflict rate | <5% of decisions | Decision log |
  | Framework evolution | Quarterly review of framework fit | Review meeting |
  | New framework adoption | <2 per year (avoid framework fatigue) | Adoption tracking |
  | Developer satisfaction with frameworks | >4.0/5.0 | Survey |

---

*Document version: 2.0 | Created: 2026-06-09 | Last Updated: 2026-06-09*
*Part of the Enterprise Coordination & Intelligence Layer (ECIL)*
