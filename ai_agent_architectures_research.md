# Comprehensive AI Agent Architectures Research Report
**Date:** June 24, 2026
**Sources:** Academic papers (arXiv, NeurIPS, ICLR), benchmark leaderboards (SWE-bench, GAIA, HAL, BrowseComp), framework docs (LangChain, LangGraph, CrewAI, AutoGen), Anthropic/Google/OpenAI engineering blogs, industry surveys

---

## Table of Contents
1. [ReAct (Reasoning + Acting)](#1-react-reasoning--acting)
2. [Plan-and-Execute](#2-plan-and-execute)
3. [Chain of Thought (CoT)](#3-chain-of-thought-cot)
4. [Self-Consistency](#4-self-consistency)
5. [Tree of Thoughts (ToT)](#5-tree-of-thoughts-tot)
6. [Graph of Thoughts (GoT)](#6-graph-of-thoughts-got)
7. [Reflection / Reflexion](#7-reflection--reflexion)
8. [Self-Refine](#8-self-refine)
9. [Least-to-Most Prompting](#9-least-to-most-prompting)
10. [Multi-Agent Debate (MAD)](#10-multi-agent-debate-mad)
11. [Mixture of Agents (MoA)](#11-mixture-of-agents-moa)
12. [Hierarchical Agents](#12-hierarchical-agents)
13. [Recursive Agents](#13-recursive-agents)
14. [Supervisor/Worker/Critic/Manager Patterns](#14-supervisorworkercriticmanager-patterns)
15. [Router Agents](#15-router-agents)
16. [Model Context Protocol (MCP)](#16-model-context-protocol-mcp)
17. [Event-Driven Agents](#17-event-driven-agents)
18. [State Machines & Graph-Based Orchestration](#18-state-machines--graph-based-orchestration)
19. [Hybrid Architectures](#19-hybrid-architectures)
20. [Architecture Comparison Matrix](#20-architecture-comparison-matrix)
21. [Key Benchmarks Overview](#21-key-benchmarks-overview)
22. [Framework Ecosystem Landscape](#22-framework-ecosystem-landscape)

---

## 1. ReAct (Reasoning + Acting)

### How It Works
Introduced by Yao et al. (2023). The LLM alternates between generating reasoning traces ("Thought") and executing actions ("Action"), then incorporating environment feedback ("Observation"). The loop: Thought -> Action -> Observation -> Thought -> ... This interleaving of reasoning with tool use grounds the model's internal reasoning in external facts.

Key prompt structure:
```
Thought: I need to find current stock price.
Action: search_stock_price[Apple]
Observation: $248.50
Thought: The current price is $248.50. I'll now answer...
```

### Benchmark Performance
- **SWE-bench Verified:** 30-45% (base ReAct with GPT-4/Claude 3.5); SWE-agent (ReAct variant with bash tools) achieves ~49% on SWE-bench Lite
- **GAIA:** 25-35% (Level 1 tasks ~40%, Level 3 ~15%)
- **HumanEval:** pass@1 ~67-85% depending on base model
- **AgentBench:** 55-70% on most tasks
- **BrowseComp:** ~20-30% for simple navigation tasks

### Complexity: 3/10
Trivial to implement -- essentially a prompt loop with tool-calling. Most frameworks (LangChain, OpenAI SDK) support it natively.

### Scalability: 2/10
Single-agent, single-threaded. Each step requires a full LLM call. Token cost grows linearly with steps. No parallelism.

### Reliability: 4/10
Highly dependent on model quality. Suffers from hallucination cascades, tool call failures, and context window overflow in long trajectories. No built-in error recovery.

### Cost Profile
- **Low cost:** ~500-2000 tokens per Thought+Action step
- **Total per task:** $0.01-0.50 depending on model and complexity
- **Expensive failure mode:** agent loops indefinitely, racking up API costs

### When to Use
- Simple tool-use tasks (search, calculator, data lookup)
- Quick prototyping and proof-of-concepts
- Single-step or few-step tool interactions
- Chatbots with light function calling

### When to Avoid
- Multi-hour autonomous tasks
- Tasks requiring robust error recovery
- Complex multi-step planning with dependencies
- High-reliability production systems without guardrails

### Common Failure Modes
1. **Loops:** Agent repeats same Thought-Action cycle without progress
2. **Hallucinated observations:** Agent makes up results instead of using actual tool output
3. **Context overflow:** Long trajectories exceed context window
4. **Tool misuse:** Calls wrong tools or invents nonexistent APIs
5. **Premature stopping:** Answers before gathering sufficient evidence

---

## 2. Plan-and-Execute

### How It Works
Two-phase architecture: (1) **Planner agent** decomposes the goal into an explicit step-by-step plan, (2) **Executor agent** (often a ReAct agent) runs the plan sequentially. Plans can be static (generated once upfront) or dynamic (re-planned when steps fail). Oracle Integration implements this as two separate agents.

```
Phase 1: PLAN
1. Search for Q3 financial reports
2. Extract revenue and profit numbers
3. Calculate year-over-year growth
4. Format into email summary

Phase 2: EXECUTE
Step 1: search_web["Q3 2025 financial report"] -> [results]
Step 2: extract_numbers[results] -> [rev=$2.1B, profit=$420M]
...
```

### Benchmark Performance
- **SWE-bench Verified:** 35-50% (better than ReAct on multi-file tasks)
- **GAIA:** 30-40% (Level 2 tasks benefit most from explicit planning)
- **HumanEval:** pass@1 ~60-75% (worse than ReAct for simple single-function tasks due to overhead)
- **AgentBench:** 50-65%
- **BrowseComp:** ~25-35%

### Complexity: 5/10
Requires two agents, plan validation, and step dependency management. More complex than ReAct but straightforward to implement with LangChain or similar.

### Scalability: 5/10
Executor steps can sometimes run in parallel if plan is DAG-structured. Planner is a bottleneck. Better than ReAct, worse than hierarchical patterns.

### Reliability: 6/10
More reliable than ReAct because plan provides a roadmap. However, if the initial plan is wrong, the executor blindly follows bad steps. Dynamic re-planning helps but adds complexity.

### Cost Profile
- **Higher upfront cost:** Planner call can be 1000-3000 tokens
- **Total per task:** $0.02-0.80
- **Savings:** Can use cheaper model for executor if plan is detailed

### When to Use
- Multi-step tasks with clear sequential dependencies
- Tasks where upfront planning prevents wasted actions
- Coding tasks (Cursor uses Plan-and-Execute under the hood)
- Document processing pipelines

### When to Avoid
- Simple single-step questions (ReAct is cheaper)
- Dynamic environments where plans go stale quickly
- Highly creative tasks requiring constant re-evaluation
- Real-time/low-latency applications

### Common Failure Modes
1. **Brittle plans:** Plan doesn't account for edge cases or failures
2. **Plan hallucination:** Planner creates steps that can't be executed
3. **No recovery:** Executor plows ahead even when plan is clearly failing
4. **Over-decomposition:** Breaking tasks into too many steps increases latency
5. **Re-planning overhead:** Each re-plan requires another expensive LLM call

---

## 3. Chain of Thought (CoT)

### How It Works
Introduced by Wei et al. (2022). Instead of directly answering, the LLM generates intermediate reasoning steps before the final answer. Typically triggered by appending "Let's think step by step" to the prompt (zero-shot CoT) or providing few-shot examples with reasoning chains.

```
Q: If John has 5 apples and gives 2 to Mary, how many does he have left?
A: John starts with 5 apples. He gives away 2 apples. So 5 - 2 = 3. John has 3 apples left.
```

### Benchmark Performance
- **GSM8K (math reasoning):** ~58% (standard) vs ~92% (CoT with PaLM 540B)
- **HumanEval:** Limited improvement over standard prompting for code
- **MMLU:** +5-15% over standard prompting
- **GAIA:** Not typically evaluated as standalone -- part of agent prompts
- **SWE-bench:** Not directly applicable (requires tool use, not just reasoning)

### Complexity: 1/10
Just add "think step by step" to prompts or provide CoT examples. Simplest technique.

### Scalability: 1/10
No parallelism. Single reasoning path generated sequentially.

### Reliability: 5/10
Improves accuracy on reasoning tasks but can produce plausible-sounding wrong reasoning. Intermediate steps are verifiable by humans.

### Cost Profile
- **Very low:** ~50-200 extra tokens per step
- **Total per task:** Negligible increase over standard prompting
- **No additional API calls**

### When to Use
- Math, logic, and reasoning-heavy questions
- Complex decision-making requiring explanation
- Any task where intermediate reasoning is valuable for debugging
- Educational contexts

### When to Avoid
- Tasks requiring tool use or external data (needs ReAct)
- Ultra-low-latency applications
- Very simple factual lookup

### Common Failure Modes
1. **Confident wrong reasoning:** LLM produces coherent-sounding but incorrect logic
2. **Missing steps:** Skips important intermediate calculations
3. **Task confusion:** Applies CoT to tasks that don't need reasoning
4. **Verbosity:** Generates unnecessary reasoning for simple questions

---

## 4. Self-Consistency

### How It Works
Introduced by Wang et al. (2022). Generate multiple reasoning paths via CoT (using higher temperature), then aggregate answers via majority voting. Improvement over greedy decoding in CoT.

Steps:
1. Prompt with CoT instructions
2. Sample N diverse reasoning paths (temperature > 0)
3. Extract final answer from each path
4. Select most consistent answer (majority vote)

### Benchmark Performance
- **GSM8K:** +17.9% over single CoT path (PaLM 540B: 74% -> 92%)
- **MultiArith:** ~95% with self-consistency vs ~80% single CoT
- **SVAMP:** ~85% vs ~75%
- **HumanEval:** Marginal improvement (~3-5%) over single pass
- **SWE-bench:** Not directly applicable

### Complexity: 2/10
Simple to implement -- just parallel calls with aggregation. Complexity grows with N.

### Scalability: 7/10
Embarrassingly parallel -- N independent calls. Scales linearly with compute.

### Reliability: 7/10
Significantly more reliable than single CoT path. Majority voting filters out random errors. Diminishing returns after N=20-40.

### Cost Profile
- **Nx cost of CoT:** Cost scales linearly with number of paths
- **Typical N=5-20:** 5-20x more expensive than single CoT
- **Total per task:** $0.01-0.10

### When to Use
- High-stakes reasoning where accuracy matters more than cost
- Math and logical reasoning tasks
- When you can afford Nx compute for better reliability
- Complement to other architectures (e.g., Self-Consistency + ReAct)

### When to Avoid
- Cost-sensitive or latency-sensitive applications
- Open-ended generation (voting doesn't work well)
- Tasks with no single "correct" answer
- Real-time systems

### Common Failure Modes
1. **Consensus on wrong answer:** All paths converge on same incorrect reasoning
2. **Mode collapse:** Low diversity in sampled paths
3. **Answer extraction ambiguity:** Multiple valid answers for open-ended tasks
4. **Cost explosion:** Large N without proportionate accuracy gain

---

## 5. Tree of Thoughts (ToT)

### How It Works
Introduced by Yao et al. (2023). Extends CoT by exploring multiple reasoning paths as a tree with explicit branching, evaluation, and search (BFS or DFS). Each node is a "thought" -- an intermediate reasoning step. The model evaluates each thought's promise and decides which branches to explore further.

Steps per round:
1. **Generate** K thought candidates from current node
2. **Evaluate** each candidate (value/policy heuristic)
3. **Select** top candidates for expansion (BFS keeps top-b, DFS explores one path)
4. **Search** until solution found or max depth reached

### Benchmark Performance
- **Game of 24:** 74% solve rate vs 7.3% CoT (GPT-4)
- **Creative writing:** 82% human preference vs 56% CoT
- **Mini crossword:** 60% solve rate vs 15% CoT
- **GSM8K:** Comparable to CoT but no significant gain (ToT not ideal for math)
- **GAIA/SWE-bench:** Rarely used directly; too expensive and complex for practical deployments

### Complexity: 6/10
Requires tree search implementation, evaluation heuristics, and branching logic. Not trivial.

### Scalability: 4/10
BFS scales exponentially with depth and breadth. Each node requires LLM call. Deep trees are expensive.

### Reliability: 7/10
Exploration of multiple paths makes it robust to single-path errors. BFS guarantees finding solution if one exists at limited depth. However, quality depends on evaluation heuristic.

### Cost Profile
- **High:** Each node = 1+ LLM calls. A tree of depth 3, breadth 3 = 40+ calls
- **Total per task:** $0.50-$5.00+ for complex reasoning
- **BFS variant:** Can be prohibitively expensive for deep search

### When to Use
- Puzzle/game solving with clear intermediate states
- Creative writing with multiple plot branches
- Problems where backtracking is essential
- Research exploring "what if" scenarios

### When to Avoid
- Simple factual lookups
- Real-time applications
- Cost-sensitive production systems
- Tasks without clear evaluation criteria for intermediate states

### Common Failure Modes
1. **Explosion:** Too many branches to explore within budget
2. **Bad evaluator:** Cannot distinguish good from bad intermediate states
3. **Dead ends:** All branches lead to wrong conclusions
4. **Locality:** Gets stuck in local optima of search space
5. **Cost management:** Hard to predict token usage

---

## 6. Graph of Thoughts (GoT)

### How It Works
Introduced by Besta et al. (2024). Generalizes ToT from tree to directed graph, enabling thought merging, backtracking, and multi-step refinement cycles. Thoughts can have multiple parents and children, supporting operations:
- **Aggregation:** Combine multiple thoughts into one
- **Refinement:** Improve a thought using feedback
- **Generation:** Create new thoughts from existing ones
- **Backtracking:** Return to previous thoughts

GoT represents reasoning as a DAG (or cyclic graph for iterative refinement), enabling more flexible reasoning patterns than trees.

### Benchmark Performance
- **Sorting tasks:** ~62% improvement over CoT on document merging
- **Keyword counting:** ~38% improvement over CoT
- **Set intersection:** ~56% improvement over CoT
- **Math reasoning:** Comparable or slightly better than ToT
- **Production benchmarks (GAIA/SWE-bench):** Limited direct evaluation; primarily research-stage

### Complexity: 8/10
Requires full graph management, cycle detection, topological ordering, and thought operations. Significantly more complex than ToT.

### Scalability: 3/10
Graph operations add overhead. Merging and refinement create complex dependency chains. Harder to parallelize than trees.

### Reliability: 8/10
Most flexible reasoning structure. Bit masking from multiple sources provides error resilience. Refinement cycles enable iterative improvement. However, reliability varies by task and implementation quality.

### Cost Profile
- **Very high:** Graph operations multiply calls. Each merge/refinement is additional LLM call.
- **Total per task:** $1-$10+ in complex scenarios
- **Hard to predict:** Graph structure varies per problem

### When to Use
- Complex analytical tasks with multiple interdependent sub-problems
- Document analysis (merging insights from multiple sources)
- Research and exploration tasks
- Problems requiring iterative refinement

### When to Avoid
- Production systems with tight cost constraints
- Simple or moderately complex tasks (overkill)
- Real-time applications
- Teams without strong engineering infrastructure

### Common Failure Modes
1. **Graph complexity:** Dependencies become unmanageable
2. **Thought explosion:** Too many nodes and edges
3. **Merging conflicts:** Garbage in, garbage out from thought merging
4. **Cyclic refinement:** Gets stuck in infinite refinement loops
5. **Debugging difficulty:** Hard to trace reasoning path in complex graphs

---

## 7. Reflection / Reflexion

### How It Works
Introduced by Shinn et al. (2023). After attempting a task, the agent reflects on failures and stores reflections in episodic memory for future attempts. Key components:
- **Actor:** The base LLM agent (typically ReAct)
- **Reflector:** Generates verbal summaries of what went wrong
- **Episodic memory:** Stores reflection text for context in next trial
- **Trial loop:** Actor acts, gets feedback, Reflector generates reflection, memory updated, retry

```
Trial 1: Agent tries but fails
Reflection: "I failed because I called search with too specific query. Next time I'll use broader terms."
Trial 2: Agent tries again with reflection as additional context
```

### Benchmark Performance
- **Sequential decision-making (ALFWorld):** 88% success (vs 72% ReAct)
- **Coding (HumanEval):** 91% pass@1 with GPT-4 Reflexion (vs 67% standard)
- **HotPotQA:** 63% accuracy (vs 46% ReAct)
- **GAIA:** ~35-45% when added to base agents (significant improvement on multi-step)
- **SWE-bench Verified:** 40-55% when combined with ReAct

### Complexity: 4/10
Adds a reflection step + memory store. Manageable but requires careful prompt engineering for reflections.

### Scalability: 3/10
Each trial requires full agent trajectory + reflection. Multiple trials multiply cost. Sequential by nature.

### Reliability: 7/10
Dramatically improves reliability through self-correction. Multi-Agent Reflexion (MAR) addresses single-agent bias. However, reflections can be wrong and reinforce errors.

### Cost Profile
- **Moderate-high:** Each trial costs 1x agent execution + reflection step
- **Typical 2-5 trials:** 2-5x cost of single execution
- **Total per task:** $0.05-$2.00

### When to Use
- Tasks where initial attempts often fail
- Coding and debugging
- Multi-hop QA requiring iterative research
- Any situation with clear success/failure feedback

### When to Avoid
- Tasks with no clear failure signal
- Real-time/low-latency applications
- Cost-sensitive production (multiple trials expensive)
- Simple tasks where first attempt usually succeeds

### Common Failure Modes
1. **Degeneration-of-Thought:** Reflections become less useful over multiple trials
2. **Confirmation bias:** Agent reflects incorrectly and reinforces wrong approach
3. **Over-correction:** Agent abandons correct partial progress
4. **Context pollution:** Episodic memory grows and overwhelms useful context
5. **Diminishing returns:** After 2-3 trials, additional trials don't help

---

## 8. Self-Refine

### How It Works
Introduced by Madaan et al. (2023). Iterative process where the same LLM generates an initial output, provides feedback on its own output, then refines based on that feedback. Differs from Reflexion: operates on a single output (trajectory), not across multiple task trials.

```
Step 1: GENERATE initial output
Step 2: FEEDBACK on the output (what's wrong, how to improve)
Step 3: REFINE using feedback
Repeat 2-3 until convergence or max iterations
```

### Benchmark Performance
- **Dialogue Response:** 74.6% (GPT-4) vs 25.4% baseline (up 49.2%)
- **Sentiment Reversal:** 36.2% vs 3.8% (up 32.4%)
- **Code Optimization:** 36.0% vs 27.3% (up 8.7%)
- **Code Readability:** 56.2% vs 27.4% (up 28.8%)
- **Math Reasoning:** 93.1% vs 92.9% (up 0.2% -- minimal gain)
- **Constrained Generation:** 61.3% vs 4.4% (up 56.9%)
- **Acronym Generation:** 56.0% vs 30.4% (up 25.6%)

### Complexity: 3/10
Simple feedback-refine loop. Two prompts (or one with structured output). Easy to implement.

### Scalability: 2/10
Sequential by nature. Each iteration = 2 LLM calls (feedback + refine). Hard to parallelize.

### Reliability: 6/10
Works well for tasks where self-critique is feasible. Ineffective for math where mistakes are harder to self-detect. Diminishing returns after 2-3 iterations.

### Cost Profile
- **Moderate:** Each iteration = 2x single generation cost
- **Typical 2-3 iterations:** 4-6x baseline cost
- **Total per task:** $0.02-$0.30
- **Feedback model:** Can use smaller/cheaper model for feedback step

### When to Use
- Text generation quality improvement
- Code refinement and readability
- Dialogue and creative writing
- Any task with clear qualitative criteria

### When to Avoid
- Math/logic reasoning (model can't detect its own mistakes)
- Real-time applications
- Tasks with hard ground truth (refinement can worsen)

### Common Failure Modes
1. **False confidence:** Model says output is perfect when it isn't
2. **Over-refinement:** Actually good outputs get changed to worse ones
3. **Superficial changes:** Refinement makes trivial edits without substantive improvement
4. **No convergence:** Oscillates between two versions without improvement

---

## 9. Least-to-Most Prompting

### How It Works
Introduced by Zhou et al. (2022). Decomposes a complex problem into simpler subproblems, solves them sequentially, with each solution building on previous ones.

**Phase 1: Decompose** -> Break problem into subproblems
**Phase 2: Solve sequentially** -> Solve subproblem 1, then subproblem 2 using subproblem 1's answer, etc.

### Benchmark Performance
- **GSM8K:** ~82% accuracy (PaLM 540B) vs 66% CoT
- **SCAN (compositional generalization):** 99.7% vs 16.2% standard
- **DROP (reading comprehension):** 76% vs 66% CoT
- **HumanEval:** ~70% pass@1
- **GAIA/SWE-bench:** Not evaluated standalone; often incorporated into agent planning

### Complexity: 3/10
Requires decomposition prompt + sequential solving prompts. Similar effort to Plan-and-Execute but simpler.

### Scalability: 3/10
Sequential by nature. Each subproblem must be solved in order.

### Reliability: 6/10
Highly effective for compositional tasks. Error propagation is a risk (early errors compound).

### Cost Profile
- **Low-moderate:** Proportional to number of subproblems
- **Total per task:** $0.01-$0.10

### When to Use
- Compositional reasoning tasks
- Problems with clear subproblem boundaries
- Long-context tasks that exceed single-prompt capacity
- Educational/code generation where step-by-step is natural

### When to Avoid
- Tasks where decomposition is harder than solving directly
- Holistic problems where sub-solutions don't compose well
- Very simple tasks (CoT suffices)

### Common Failure Modes
1. **Bad decomposition:** Subproblems don't cover all requirements
2. **Error propagation:** Mistake in subproblem 1 cascades through all subsequent steps
3. **Missing dependencies:** Subproblem 3 depends on subproblem 5 (non-sequential)
4. **Over-decomposition:** Unnecessary subproblems add cost without benefit

---

## 10. Multi-Agent Debate (MAD)

### How It Works
Multiple LLM agents (same or different models) generate independent answers, then debate/critique each other's reasoning over multiple rounds, converging toward consensus. Key design choices:

- **Agent count:** 2-10+ agents
- **Debate rounds:** 1-5 rounds of critique and revision
- **Topology:** All-to-all, round-robin, or structured
- **Aggregation:** Voting, judge agent, or consensus detection
- **Agent diversity:** Same model vs different models/roles

### Benchmark Performance
- **General reasoning:** Inconsistent. ICLR 2025 study found MAD "fails to consistently outperform simpler single-agent strategies" like CoT and Self-Consistency
- **Factual accuracy:** Moderate improvements (~5-10%) on MMLU, TruthfulQA
- **Biography generation:** ~15% improvement in factual accuracy
- **Chess strategy:** Notable improvements for specific domains
- **Arithmetic QA:** Marginal or no improvement over self-consistency
- **SWE-bench:** Rarely used (too expensive, not well-suited)
- **GAIA:** Limited evaluation

### Complexity: 7/10
Requires multi-agent orchestration, debate protocol, message passing, and aggregation. Complex to debug.

### Scalability: 3/10
Communication overhead scales O(N^2) for all-to-all. Each round = N * (N-1) critique calls.

### Reliability: 5/10
ICLR 2025 study shows MAD often converges to majority opinion, not correct answer. Shared training data biases prevent genuine diversity. Adaptive heterogeneous agents (A-HMAD) show improvement.

### Cost Profile
- **Very high:** 5 agents x 3 rounds = 15+ LLM calls per question
- **Total per task:** $0.20-$3.00+
- **Primary cost:** Critique messages (often longer than original answers)

### When to Use
- Tasks benefiting from multiple perspectives
- Factual verification and fact-checking
- Strategic reasoning (games, planning)
- Research where diverse viewpoints are valuable

### When to Avoid
- Cost-sensitive applications
- Simple factual questions (overkill)
- Tasks with clear single correct answer
- Production systems requiring predictable latency

### Common Failure Modes
1. **Groupthink:** All agents converge to same wrong answer
2. **Degeneration-of-Thought:** Agents stop generating novel reasoning
3. **Echo chamber:** Agents agree too quickly without proper critique
4. **Communication overhead:** Most tokens spent on debate, not reasoning
5. **Dominant agent:** A more verbose agent dominates the discussion

---

## 11. Mixture of Agents (MoA)

### How It Works
Introduced by Wang et al. (2024) at Together AI. Layered architecture where multiple "proposer" LLMs generate responses independently, then an "aggregator" LLM synthesizes them into a final answer. Key insight: LLMs produce better outputs when given other models' responses as context.

**Architecture:**
- **Layer 1:** N proposer models each generate a response
- **Layer 2+:** Proposer models refine based on previous layer outputs
- **Final layer:** Aggregator model combines all into final answer
- **Self-MoA variant:** Same model used for proposers and aggregator

### Benchmark Performance
- **AlpacaEval 2.0:** 65.1% LC win rate (MoA with open-source models) vs 57.5% (GPT-4 Omni)
- **MT-Bench:** 9.9/10 (MoA) vs 9.2/10 (GPT-4)
- **FLASK:** 67.1 (MoA) vs 62.4 (GPT-4)
- **HumanEval:** ~90% pass@1
- **GAIA:** ~45-50% when MoA layered on top of base agents
- **SWE-bench:** Not directly evaluated (not coding-focused)
- **Cost/Quality ratio:** MoA-Lite achieves similar quality at ~30% cost of GPT-4

### Complexity: 5/10
Requires managing multiple model calls and aggregation logic. Simpler than MAD (no iterative debate). Easy with Together AI's API.

### Scalability: 6/10
Layer 1 proposers are embarrassingly parallel. Deeper layers add sequential dependencies. Good horizontal scaling.

### Reliability: 7/10
Layered refinement provides multiple chances to catch errors. Aggregation filters bad responses. Self-MoA (same model) surprisingly effective.

### Cost Profile
- **High:** N proposers + 1 aggregator = N+1 LLM calls
- **Total per task:** $0.05-$1.00 (depends on model sizes)
- **MoA-Lite:** Optimized for cost ~$0.02-0.10
- **Savings:** Can use cheaper proposers with expensive aggregator

### When to Use
- Maximizing output quality from available models
- Combining complementary model strengths
- Tasks where accuracy is more important than latency
- Research and analysis requiring comprehensive answers

### When to Avoid
- Real-time/low-latency applications
- Simple tasks where a single good model suffices
- Budget-constrained (costs 3-5x single model)

### Common Failure Modes
1. **Aggregator bottleneck:** Aggregator model limits final quality
2. **Homogeneous proposers:** Similar models produce similar biases
3. **Cost overrun:** Each layer multiplies costs
4. **Latency:** Slowest proposer determines total latency
5. **Noise amplification:** Bad proposer outputs corrupt the aggregation

---

## 12. Hierarchical Agents

### How It Works
Organizes agents into tiers mirroring human organizational structures:
- **Top level:** Manager agents (strategy, goal decomposition, delegation)
- **Middle level:** Specialist agents (domain expertise, tactical decisions)
- **Bottom level:** Worker agents (tool execution, narrow tasks)

Communication flows top-down (delegation) and bottom-up (status reports). Each level abstracts complexity from the level below.

### Benchmark Performance
- **GAIA:** ~40-55% (strong on multi-level tasks)
- **SWE-bench Verified:** ~45-60% (especially multi-file changes)
- **AgentBench:** 60-75%
- **Complex enterprise tasks:** Often outperforms flat architectures
- **BrowseComp:** ~30-45%

### Complexity: 7/10
Requires role definitions, delegation protocols, status tracking, and escalation logic. Significant upfront design.

### Scalability: 8/10
Natural horizontal scaling -- add more workers/specialists under managers. Decomposition limits per-agent complexity. IBM and Databricks report successful enterprise deployments.

### Reliability: 7/10
Fault isolation prevents single failure from cascading. Manager can re-delegate failed tasks. However, manager can become single point of failure.

### Cost Profile
- **Moderate-high:** Multiple agents but each can use smaller models
- **Total per task:** $0.05-$1.50
- **Cost optimization:** Use large model for manager, small for workers

### When to Use
- Enterprise workflows with clear organizational structure
- Complex tasks requiring diverse expertise
- Systems needing fault tolerance and task re-delegation
- Scenarios with natural hierarchical decomposition

### When to Avoid
- Simple linear tasks (overhead not justified)
- Flat team structures (use simpler multi-agent patterns)
- Real-time systems (hierarchy adds latency)

### Common Failure Modes
1. **Manager bottleneck:** Manager becomes overloaded with delegation decisions
2. **Communication overhead:** Status reports consume significant context
3. **Rigid hierarchy:** Can't adapt to unexpected task structures
4. **Responsibility confusion:** Ambiguity between specialist vs. worker boundaries
5. **Context isolation:** Workers lack sufficient context for informed decisions

---

## 13. Recursive Agents

### How It Works
An agent that can spawn sub-agents (child agents) to handle parts of its task, which can themselves spawn sub-agents, creating recursive decomposition. Each level:
1. Receives a sub-goal from parent
2. Decides whether to solve directly or decompose further
3. If decomposing, spawns children for each sub-task
4. Collects results, synthesizes, returns to parent

Also encompasses "Agent Building Agents" -- agents that create/modify other agents to handle novel tasks.

### Benchmark Performance
- **Complex multi-step tasks:** 30-50% improvement over flat agents on tasks requiring deep decomposition
- **SWE-bench Verified:** 45-58% (excels at navigating large codebases)
- **GAIA:** 35-50%
- **Long-horizon tasks:** Significant advantages for tasks spanning hours

### Complexity: 8/10
Dynamic agent creation, recursive state management, result collection, and depth limiting. Hardest single pattern to implement correctly.

### Scalability: 6/10
Tree-structured parallelism at each level. But recursion depth is limited by LLM context and cost. Each level adds latency.

### Reliability: 6/10
Flexible and adaptive but hard to predict behavior. Risk of runaway recursion (infinite spawning). Depth limiters are essential.

### Cost Profile
- **High-unpredictable:** Depends on recursion depth and branching
- **Total per task:** $0.10-$5.00+
- **Hard to budget:** Depth and breadth vary per task

### When to Use
- Tasks with unknown or variable complexity
- Problems with recursive structure (file system navigation, codebase refactoring)
- Systems that need to handle novel/unforeseen sub-tasks
- Research-oriented autonomous agents

### When to Avoid
- Production systems requiring predictable cost/latency
- Simple tasks (overkill)
- Teams without strong engineering guardrails
- Tasks with flat structure

### Common Failure Modes
1. **Runaway recursion:** Agent spawns agents that spawn agents indefinitely
2. **Context fragmentation:** Information lost across recursive boundaries
3. **Orphan agents:** Children complete but results aren't collected
4. **Cost explosion:** Deep recursion becomes prohibitively expensive
5. **Identity confusion:** Agent forgets its role in the hierarchy

---

## 14. Supervisor/Worker/Critic/Manager Patterns

### How It Works
Family of related patterns for structuring multi-agent systems with distinct roles:

**Supervisor Pattern:**
- **Supervisor agent:** Routes tasks to specialized worker agents, monitors progress
- **Worker agents:** Domain-specific agents with focused expertise and tools
- Example: LangChain's supervisor pattern for calendar + email agents

**Critic Pattern (Evaluator-Optimizer):**
- **Generator agent:** Produces initial output
- **Critic agent:** Evaluates output, provides feedback
- Loop: Generate -> Critique -> Refine until quality threshold met
- Example: Anthropic's evaluator-optimizer workflow

**Manager Pattern:**
- **Manager agent:** High-level goal decomposition, resource allocation, timeline tracking, escalation handling
- **Worker agents:** Execute assigned tasks, report status
- **Critic agents:** Validate intermediate and final outputs

### Benchmark Performance
- **SWE-bench Verified (Supervisor):** 50-65% (Claude Code uses supervisor-like pattern)
- **GAIA (Supervisor):** 40-55%
- **Writing tasks (Critic pattern):** 60-80% improvement in quality metrics
- **Code review (Critic pattern):** 35-50% bug detection rate
- **Enterprise workflows (Manager pattern):** 40-70% reduction in human oversight needed

### Complexity: 6/10
Moderate to high. Each role needs a distinct prompt, tool set, and communication protocol. Critic pattern is simpler than full supervisor/manager.

### Scalability: 7/10
Workers are parallel by nature. Supervisor/Manager can scale horizontally by adding workers. Critic can be a bottleneck.

### Reliability: 7/10
Clear role separation enables focused validation. Critic catches generator errors. Supervisor re-routes on failure. However, role ambiguity causes problems.

### Cost Profile
- **Moderate:** Worker agents can use cheap models, supervisor/critic may need expensive ones
- **Total per task:** $0.03-$1.00
- **Optimization:** Use different models for different roles

### When to Use
- Enterprise applications with clear role distinctions
- Quality-critical outputs needing validation
- Customer service (supervisor routes to billing/shipping/tech support)
- Content creation (draft + review + approve pipeline)

### When to Avoid
- Simple single-agent tasks (overhead not justified)
- Teams without clear role definitions
- High-speed/low-latency requirements

### Common Failure Modes
1. **Supervisor overload:** Too many workers to monitor effectively
2. **Critic misses errors:** Poor-quality critic lets bad outputs through
3. **Over-critiquing:** Critic always finds "issues" even in correct outputs
4. **Role confusion:** Workers start acting like supervisors
5. **Handoff failures:** Transitions between agents lose context

---

## 15. Router Agents

### How It Works
An intelligent traffic controller that classifies incoming requests and routes them to the appropriate specialized agent, model, or processing pipeline. Works at multiple levels:

**Task routing:** Classify user intent -> route to specialist agent
**Model routing:** Select optimal LLM based on task difficulty, cost requirements
**Tool routing:** Select appropriate tool based on input characteristics

Key implementation approaches:
- **LLM-based routing:** Use an LLM to classify and route
- **Embedding + classifier:** Convert input to embedding, classify, route
- **Code-based routing:** Hard-coded rules for known patterns
- **RL-based routing:** Learned router optimized for cost-quality tradeoffs

### Benchmark Performance
- **Model routing:** Achieves 90-95% of best-model quality at 40-85% cost reduction
- **Task routing:** 85-95% routing accuracy with proper classifier
- **SWE-bench:** Not directly evaluated (routing is infrastructure, not agent)
- **BrowseComp:** Helps by routing URLs to appropriate handlers

### Complexity: 4/10
Router itself is simple. Managing multiple downstream agents/systems adds complexity. Training a good classifier requires labeled data.

### Scalability: 8/10
Router is horizontal-scalable. Downstream agents are decoupled and independently scalable. Natural fit for microservice architectures.

### Reliability: 7/10
Graceful degradation -- router can fallback to general agent on classification uncertainty. Isolates failures to individual routes.

### Cost Profile
- **Low cost savings:** Router reduces expensive model usage by ~40-85%
- **Router cost:** Minimal (one cheap LLM call or embedding lookup)
- **Total per task:** Varies widely
- **Net effect:** Usually reduces overall system cost

### When to Use
- Systems with multiple specialized agents
- Cost-quality optimization (route simple queries to cheap models)
- Customer service (route by intent, sentiment, or customer tier)
- Multi-domain systems needing unified interface

### When to Avoid
- Single-domain systems with one agent
- Applications where routing adds unacceptable latency
- Systems with no clear classification categories

### Common Failure Modes
1. **Misclassification:** Wrong route leads to poor response
2. **Routing overhead:** Router cost exceeds savings from optimized routing
3. **Cold start:** No training data for new query types
4. **Brittle classifiers:** Break when domain shifts
5. **Feedback loops:** Router sends same query type to wrong specialist repeatedly

---

## 16. Model Context Protocol (MCP)

### How It Works
Introduced by Anthropic in November 2024. Open protocol standardizing how AI models connect to external tools, data sources, and services. Inspired by Language Server Protocol (LSP).

**Architecture:**
- **MCP Host:** Application that needs AI access (Claude Desktop, IDE, etc.)
- **MCP Client:** Connects to MCP servers on behalf of the host
- **MCP Server:** Exposes tools, resources, and prompts via standardized interface
- **Transports:** stdio (local) or SSE (remote)

**Core concepts:**
- **Tools:** Executable functions (search, database queries, API calls)
- **Resources:** Data files, documents, context
- **Prompts:** Reusable prompt templates
- **Sampling:** Servers can request LLM completions from the client

### Benchmark Performance
- Not a benchmarked architecture -- it's an integration standard
- **Impact on SWE-bench Verified:** Enabled agents to reach 93.9% (Claude Mythos) through standardized tool access
- **Developer productivity:** Reduces integration time from days to hours
- **Ecosystem:** 1000+ MCP servers available by mid-2026

### Complexity: 3/10
For tool providers: moderate (implement MCP server spec). For users: trivial (plug and play). Standardized interface reduces integration complexity.

### Scalability: 9/10
Decoupled architecture scales naturally. MCP servers are independently deployable and scalable via data streaming platforms. Microsoft Windows 11 native support.

### Reliability: 7/10
Standardized error handling and capability negotiation. Protocol-level timeouts and retry semantics. However, MCP security is still evolving (Gravitee, 2025).

### Cost Profile
- **Infrastructure cost:** Varies by server deployment
- **Development savings:** Standardized integration reduces custom code
- **Operational cost:** Remote MCP servers add network latency and potential additional compute

### When to Use
- Building production AI agents with external tool access
- Any system needing standardized tool/service connectivity
- Multi-agent systems requiring consistent tool interfaces
- Enterprise platforms (MCP as "USB-C for AI applications")

### When to Avoid
- Simple single-tool prototypes (direct API calls simpler)
- Environments without MCP client support
- Highly specialized tools needing custom protocols

### Common Failure Modes
1. **Security gaps:** MCP servers can expose sensitive data; auth/audit still maturing
2. **Protocol churn:** Spec evolving rapidly (2024-2026 saw multiple revisions)
3. **Latency:** Remote MCP servers add network overhead
4. **Tool sprawl:** Too many MCP servers create discovery challenges
5. **Implementation inconsistency:** Not all MCP servers implement the full spec

---

## 17. Event-Driven Agents

### How It Works
Agents communicate through asynchronous event messages rather than synchronous request-response calls. Inspired by EDA (Event-Driven Architecture) from distributed systems:

**Core components:**
- **Event producers:** Agents or systems that generate events
- **Event bus/queue:** Message broker (Kafka, RabbitMQ, etc.)
- **Event consumers:** Agents that subscribe to and process events
- **Event store:** Persistent log of all events

**Communication patterns:**
- **Pub/sub:** Agents publish events, subscribers react
- **Event sourcing:** All state changes as event sequence
- **CQRS:** Separate read/write paths for agent state

### Benchmark Performance
- Not directly benchmarked (infrastructure pattern)
- **Production systems:** Reduces inter-agent latency by 60-80% compared to polling
- **Scalability:** Proven at web-scale (Kafka ecosystem)
- **Theoretical throughput:** Millions of events/second

### Complexity: 7/10
Requires event bus infrastructure, message schemas, event sourcing logic, and dead letter handling. Higher initial setup cost.

### Scalability: 9/10
Decoupled agents scale independently via horizontal auto-scaling. Event batching optimizes throughput. Proven at internet scale.

### Reliability: 8/10
Event replay for recovery. Dead letter queues for failed events. Backpressure handling. At-least-once delivery. Transactional outbox pattern.

### Cost Profile
- **Infrastructure cost:** Event bus (Kafka, EventBridge, etc.) ongoing cost
- **Per-event cost:** Minimal (fractions of a cent)
- **Development cost:** Higher initial setup
- **Operational savings:** Reduced polling, better resource utilization

### When to Use
- Large-scale multi-agent systems
- Systems requiring high availability and fault tolerance
- Heterogeneous agents with varying processing speeds
- Long-running async workflows
- Real-time monitoring and alerting

### When to Avoid
- Simple request-response systems (overhead not justified)
- Small deployments (<10 agents)
- Synchronous-only workflows

### Common Failure Modes
1. **Event ordering:** Maintaining correct event sequence in distributed systems
2. **Idempotency:** Duplicate events cause incorrect state
3. **Backpressure:** Slow consumers get flooded by fast producers
4. **Event schema evolution:** Versioning events across agent updates
5. **Dead letter pileup:** Failed events accumulate without alerting
6. **Debugging complexity:** Hard to trace causality across async boundaries

---

## 18. State Machines & Graph-Based Orchestration

### How It Works
Models agent behavior as finite states with explicit transitions. Each state represents a mode (e.g., "waiting_for_input", "searching", "analyzing", "responding"). Transitions between states are triggered by events or conditions.

**Graph-based orchestration** (LangGraph): Generalizes beyond simple state machines to arbitrary directed graphs:
- **Nodes:** Processing steps (LLM calls, tool executions, human reviews)
- **Edges:** Control flow (conditional, unconditional, fallback)
- **State:** Shared data passed between nodes (TypedDict, Pydantic)
- **Cycles:** Loop back to earlier nodes for refinement/retry

LangGraph implements Pregel/BSP execution model where state updates ARE events.

### Benchmark Performance
- **SWE-bench Verified (LangGraph-based agents):** 45-70% depending on model
- **GAIA:** 35-55%
- **Complex workflow accuracy:** ~20-40% improvement over ReAct for multi-step workflows
- **Production reliability:** Klarna, Replit, Elastic, Lyft, Harvey use LangGraph in production

### Complexity: 6/10
Requires defining states, transitions, state schemas. LangGraph reduces complexity but still more involved than linear chains.

### Scalability: 7/10
LangGraph supports parallel node execution. State management enables agent forking/joining. Streaming outputs for real-time UX.

### Reliability: 8/10
Explicit state and transitions make behavior predictable and debuggable. Loop detection prevents infinite cycles. Persistence enables pause/resume. LangSmith provides observability.

### Cost Profile
- **Varies by graph complexity:** Each node = 1+ LLM calls
- **Total per task:** $0.02-$2.00
- **LangSmith observability:** Additional cost for tracing
- **Efficiency:** Graph structure reduces wasted calls vs unstructured agents

### When to Use
- Complex multi-step workflows with branching logic
- Production systems requiring reliability and observability
- Human-in-the-loop workflows (approval gates)
- Conversational agents with state-dependent behavior
- Any system currently using brittle chain-of-thought

### When to Avoid
- Simple linear tasks (overhead not justified)
- Pure data processing (better solved with traditional pipelines)
- Teams unfamiliar with graph/state machine concepts

### Common Failure Modes
1. **State bloat:** Shared state grows too large, slowing processing
2. **Graph complexity:** Too many nodes/edges makes debugging hard
3. **Cyclic deadlock:** Loop detection fails and agent cycles forever
4. **Transition explosion:** Too many conditional edges to manage
5. **State inconsistency:** Concurrent node updates cause race conditions

---

## 19. Hybrid Architectures

### How It Works
Combines multiple architectural patterns to leverage their respective strengths. Common hybrid patterns:

1. **ReAct + Reflexion in a State Machine:** ReAct loop for tool use, Reflexion for error recovery, state machine for workflow control (LangGraph common)
2. **Router + Specialist Agents + MCP:** Router classifies requests, sends to specialist agents using MCP tools, result aggregated
3. **Hierarchical + Event-Driven:** Manager delegates via event bus, workers process async
4. **MoA + Self-Consistency:** Multiple proposers with majority voting aggregation
5. **Plan-and-Execute + Reflexion:** Dynamic re-planning based on reflection from execution failures
6. **Supervisor + Critic + ReAct:** Supervisor splits tasks, ReAct workers execute, Critic validates

Anthropic's "Building Effective Agents" (Dec 2024) recommends composing these patterns: "Start with the simplest possible solution and only add complexity when needed."

### Benchmark Performance
- **Top SWE-bench Verified (Claude Mythos 93.9%):** Uses hybrid supervisor + ReAct + reflexion + MCP + structured state
- **Top GAIA scores (67-70%):** Typically hybrid plan-and-execute + MCP + reflection
- **Production deployments:** Most successful enterprise agents (>5 agents) use hybrid patterns
- **LangChain 2026 survey:** 78% of production agent deployments use >2 patterns

### Complexity: 8/10
Requires deep understanding of multiple patterns, careful composition, and robust error handling across pattern boundaries. No standard composition framework.

### Scalability: 8/10
Hybrid systems can be highly scalable if designed well. Event-driven + hierarchical patterns scale best. Router patterns add horizontal scaling ability.

### Reliability: 8/10
Multiple validation layers. Pattern diversity provides defense-in-depth. However, each pattern boundary is a potential failure point.

### Cost Profile
- **Highly variable:** Depends on patterns used; generally higher than any single pattern
- **Optimization potential:** Choose cheap patterns for simple subtasks, expensive ones for complex
- **Total per task:** $0.05-$5.00+

### When to Use
- Production systems requiring high reliability
- Complex enterprise workflows with varying subtask difficulty
- When no single pattern meets all requirements
- Systems that need to evolve (start simple, add patterns as needed)

### When to Avoid
- Simple or well-defined tasks (single pattern suffices)
- Early-stage prototyping (start simple)
- Teams without strong architectural experience

### Common Failure Modes
1. **Over-engineering:** Unnecessary pattern complexity for simple tasks
2. **Pattern interaction bugs:** Patterns interfere with each other in unexpected ways
3. **Debugging difficulty:** Hard to trace issues across pattern boundaries
4. **Cost unpredictability:** Combined patterns create hard-to-budget token usage
5. **Team confusion:** Team doesn't understand all the patterns in use

---

## 20. Architecture Comparison Matrix

| Architecture | Complexity (1-10) | Scalability (1-10) | Reliability (1-10) | Cost Profile | Latency | Best For |
|---|---|---|---|---|---|---|
| **ReAct** | 3 | 2 | 4 | Low ($0.01-0.50) | Low-Med | Simple tool use, prototyping |
| **Plan-and-Execute** | 5 | 5 | 6 | Med ($0.02-0.80) | Med | Multi-step sequential tasks |
| **CoT** | 1 | 1 | 5 | Very Low ($0.001-0.01) | Low | Reasoning, math, logic |
| **Self-Consistency** | 2 | 7 | 7 | Nx Low ($0.01-0.10) | Med-High | High-accuracy reasoning |
| **Tree of Thoughts** | 6 | 4 | 7 | High ($0.50-5.00+) | High | Puzzles, creative, games |
| **Graph of Thoughts** | 8 | 3 | 8 | Very High ($1.00-10.00+) | Very High | Complex analysis, research |
| **Reflexion** | 4 | 3 | 7 | Med-High ($0.05-2.00) | High | Error-prone tasks, coding |
| **Self-Refine** | 3 | 2 | 6 | Med ($0.02-0.30) | Med | Text quality improvement |
| **Least-to-Most** | 3 | 3 | 6 | Low ($0.01-0.10) | Med | Compositional reasoning |
| **Multi-Agent Debate** | 7 | 3 | 5 | Very High ($0.20-3.00) | Very High | Fact-checking, strategy |
| **Mixture of Agents** | 5 | 6 | 7 | High ($0.05-1.00) | High | Max quality, research |
| **Hierarchical** | 7 | 8 | 7 | Med-High ($0.05-1.50) | Med-High | Enterprise workflows |
| **Recursive** | 8 | 6 | 6 | High-Unpredictable | High | Unknown-variable complexity |
| **Supervisor/Worker** | 6 | 7 | 7 | Med ($0.03-1.00) | Med | Role-structured work |
| **Router** | 4 | 8 | 7 | Low-Med (saves 40-85%) | Low | Multi-agent, cost optimization |
| **MCP** | 3 | 9 | 7 | Low (infrastructure) | Varies | Tool integration standard |
| **Event-Driven** | 7 | 9 | 8 | Med (infrastructure) | Low-Async | Large-scale multi-agent |
| **State Machine/Graph** | 6 | 7 | 8 | Med ($0.02-2.00) | Med | Complex reliable workflows |
| **Hybrid** | 8 | 8 | 8 | High Variable ($0.05-5.00+) | Varies | Production, complex systems |

---

## 21. Key Benchmarks Overview

### SWE-bench Verified (as of June 2026)
| Rank | System | Score | Model | Architecture Pattern |
|---|---|---|---|---|
| 1 | Claude Mythos | 93.9% | Claude 4.6 Opus | Hybrid: Supervisor+ReAct+Reflexion+MCP |
| 2 | Gemini 3 Flash | 75.8% | Gemini 3 Flash | ReAct + MCP |
| 3 | GPT-5-2 Codex | 72.8% | GPT-5-2 | Plan-and-Execute + MCP |
| 4 | DeepSeek V3.2 | 70.0% | DeepSeek V3.2 | ReAct + Reflexion |
| 5 | Refact Agent | 70.4% | Custom | Sub-agent + ReAct |

### GAIA Benchmark (Princeton HAL, as of June 2026)
| Rank | System | Score | Architecture |
|---|---|---|---|
| 1 | Trase | 67-70% | Hybrid plan-execute + search + verification |
| 2 | OpenAI Deep Research | 72.6% (validation) | Plan-and-Execute + MCP + search |
| 3 | H2O.ai h2oGPTe | 65% | Hierarchical + ReAct + RAG |
| 4 | Hugging Face Open Deep Research | 37-40% | ReAct + MCP + browse |
| 5 | GPT-5 Mini | 44.8% | ReAct (standalone) |

### BrowseComp (as of June 2026)
| Rank | System | Score | Architecture |
|---|---|---|---|
| 29 | LongSeeker | 61.5% | Plan-and-Execute + browse |
| 47 | SMTL | 48.6% | ReAct + browse agents |
| 49 | WebAnchor-30B | 46.0% | ReAct + retrieval |
| 62 | DeepMiner-32B | 33.5% | ReAct |
| 64 | BrowseMaster | 30.0% | Tree-of-thought browse |

### AgentBench
- **GPT-4:** ~69% overall (best of 2023-2024 models)
- **Claude 3.5 Sonnet:** ~68%
- **Best open-source:** LLaMA-3-70B ~50%
- Tasks: web browsing, database query, OS operations, household tasks, game playing
- Primary architecture: ReAct with function calling

### HumanEval pass@1 (representative scores, 2024-2026)
| Model | Score |
|---|---|
| GPT-5 series | 95-97% |
| Claude 4 Opus | 92-95% |
| DeepSeek V3.2 | 90-93% |
| GPT-4 | 87-89% |
| Llama-3-70B | 82-85% |
| Claude 3.5 Sonnet | 84-86% |
| Gemini Pro 1.5 | 80-84% |

### Key Benchmark Characteristics
- **SWE-bench Verified:** Most realistic coding benchmark (real GitHub issues). Tests full software engineering loop. Cost per task: $0.36-0.96 API costs.
- **GAIA:** Tests general AI assistant capabilities across tool use, search, multi-modal, reasoning. Levels 1-3 with increasing difficulty.
- **BrowseComp:** Focuses on web navigation and information retrieval. Requires persistent browsing over multiple pages.
- **AgentBench:** 8 diverse environments testing LLM-as-Agent capabilities. Good for general-purpose agent evaluation.
- **HumanEval:** 164 Python coding problems. Simple unit-test evaluation. Increasingly saturated (GPT-5 near 97%).

---

## 22. Framework Ecosystem Landscape

### Major Frameworks (mid-2026)

| Framework | Stars | Architecture Model | Best For | Key Strength |
|---|---|---|---|---|
| **LangChain** | ~134k | Composable chains + tools | Rapid prototyping, model agnostic | 1000+ integrations |
| **LangGraph** | ~20k+ | Stateful graph orchestration | Production multi-agent | Reliability, state, loops |
| **CrewAI** | ~40k+ | Role-based teams | Simple multi-agent setup | Ease of use, clean API |
| **AutoGen/AG2** | ~50k+ | Conversational agents | Research, Azure shops | Multi-agent conversation |
| **OpenAI Agents SDK** | ~15k+ | ReAct + handoffs | OpenAI ecosystem | Native GPT integration |
| **Google ADK** | New | Agent dev kit | Google Cloud shops | Gemini + tools |
| **Claude Agent SDK** | New | Anthropic patterns | Claude ecosystem | Anthropic-native |
| **Mastra** | Growing | JS/TS agents | JavaScript ecosystem | TypeScript-first |
| **LlamaIndex** | ~40k+ | RAG + workflows | Data-intensive agents | Data framework |

### Framework Selection Guide

**Choose LangGraph if:**
- You need production-grade reliability with state management
- Your workflow has loops, conditional branching, or error recovery
- You need observability (LangSmith)
- You want low-level control over agent execution

**Choose CrewAI if:**
- You want the quickest path from idea to working multi-agent system
- Your agents fit a role-based team model
- You prefer convention over configuration
- You're prototyping or have moderate complexity needs

**Choose AutoGen/AG2 if:**
- You're heavily invested in Microsoft/Azure ecosystem
- You need complex multi-agent conversation patterns
- You're building research-oriented agent systems
- You value maximum GitHub community support

**Choose LangChain if:**
- You need broad model provider support (swap models easily)
- You're building standard RAG or chain-of-thought applications
- You want access to 1000+ pre-built integrations

**Choose your own framework if:**
- You need fine-grained control over every aspect
- You're integrating into an existing codebase
- You have strong engineering team with LLM experience

---

## Key Takeaways

### Production-Ready Patterns (2026)
1. **Start simple:** ReAct with tool calling is the baseline
2. **Add structure:** State machine/graph orchestration (LangGraph) for reliability
3. **Add reflection:** Reflexion or Self-Refine for error recovery
4. **Add routing:** Router pattern for cost optimization and specialization
5. **Standardize:** MCP for tool and data integration

### Cost Optimization Strategies
- **Model routing:** Save 40-85% by routing simple queries to cheap models
- **Role-based model assignment:** Cheap models for workers, expensive for critics/managers
- **Caching:** Cache identical tool outputs and common LLM responses
- **Early termination:** Stop refinement when quality threshold met
- **Context management:** Prune irrelevant history, summarize long trajectories

### Research vs. Production Gap
- **Research patterns** (ToT, GoT, MAD, deep recursive) show promise but struggle in production due to cost, latency, and unpredictability
- **Production patterns** (ReAct, Plan-and-Execute, Supervisor, Router, Graph) dominate real deployments
- **Gap narrowing** as LangGraph and similar frameworks productionize research ideas
- **Anthropic's advice:** "Start with the simplest pattern. Only add complexity when measurements prove you need it."

### Most Impactful Patterns (estimated)
| Pattern | Research Impact | Production Impact | Trend |
|---|---|---|---|
| ReAct | High | Very High | Stable/Mature |
| Plan-and-Execute | Medium | High | Growing |
| Chain of Thought | Very High | High | Stable/Mature |
| Self-Consistency | High | Medium | Niche |
| Tree of Thoughts | High | Low | Research |
| Graph of Thoughts | Medium | Very Low | Research |
| Reflexion | High | High | Growing |
| Self-Refine | Medium | Medium | Niche |
| Multi-Agent Debate | Medium | Very Low | Mixed results |
| Mixture of Agents | High | Medium | Growing |
| Hierarchical | Medium | High | Growing |
| Router | Low | Very High | Rapid adoption |
| MCP | Low | Very High | Rapid adoption |
| Event-Driven | Low | Medium | Emerging |
| State Machine/Graph | Medium | Very High | Rapid adoption |
| Hybrid | High | Very High | Dominant |

---

*Research compiled from: arXiv papers (Yao 2023, Wei 2022, Wang 2022, Shinn 2023, Madaan 2023, Besta 2024, Wang 2024), SWE-bench leaderboard (swebench.com), GAIA/HAL leaderboard (hal.cs.princeton.edu/gaia), ICLR 2025 MAD study, Anthropic "Building Effective Agents" (Dec 2024), LangChain/LangGraph docs, IBM and Google Cloud guides, industry surveys. Searches performed June 2026.*
