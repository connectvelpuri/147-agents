# Revenue OS Agent Skills Directory

> **Purpose:** Methodological foundation for all 27 divisions / 108 agents
> **Last Updated:** 2026-06-25
> **Applied To:** SDR-001, SDR-002, SDR-003, SDR-004, MO-001, MO-002, MO-003, MO-004, QL-001, RCC-001, AI-001, DS-001, DS-002, DS-003, DS-004, DS-005, NG-001, NG-002, NG-003, NG-004

---

## How to Use This File

Every agent loads the skill files relevant to its role. The skills below encode
specific sales methodologies, psychological frameworks, and neuroscience
principles. Agents reference them directly in their LLM system prompts.

**For new agents:** Reference the relevant skill(s) in the system prompt.
**For existing agents:** This file documents what has already been applied.

---

## Table of Contents

1. [Skip Miller (M3 Learning) — ATL/BTL, L1-L2-L3, Give-Get, Kid Table/Adult Table](#1-skip-miller)
2. [Gal Borenstein — Psychological Objection Mitigation](#2-gal-borenstein)
3. [Paul Butterfield — Customer Journey Enablement](#3-paul-butterfield)
4. [Jeff Shore — Cognitive Behavioral Sales Coaching](#4-jeff-shore)
5. [Andy Paul — Selling In Framework](#5-andy-paul)
6. [Dale Merrill — Sales Movie Trailer / Co-Creation](#6-dale-merrill)
7. [Ashley Welch — Anti-Pitch / 6/60 Rule](#7-ashley-welch)
8. [Brian Burns — The Brutal Truth / Curiosity Framework](#8-brian-burns)
9. [David Weiss — Hard Truths / Respect-Based Selling](#9-david-weiss)
10. [50 Cognitive & Persuasion Principles](#10-cognitive--persuasion-principles)
11. [Reverse Funnel Math / Intent Stack](#11-reverse-funnel-math--intent-stack)
12. [Multi-Channel Sequence Architecture](#12-multi-channel-sequence-architecture)

---

## 1. Skip Miller (M3 Learning)

### Core Model: ATL vs BTL

**ATL (Above the Line)** — Conscious, rational, overt.
- Buyer is thinking: "I need to solve this problem"
- They know they have a problem
- They're actively evaluating solutions
- They can articulate their needs
- Communication: direct, logical, feature-benefit

**BTL (Below the Line)** — Subconscious, emotional, hidden.
- Buyer feels: "Something isn't right but I can't name it"
- They sense pain but won't admit vulnerability
- They fear making the wrong decision
- They have hidden political/ego drivers
- Communication: indirect, story-based, trust-building

**Agent Application:**
| Agent Type | When to Use ATL | When to Use BTL |
|---|---|---|
| SDR-003 (Outreach) | Prospect has explicit intent signals | Prospect is cold/ unaware of problem |
| MO-003 (Objection Detection) | Objection is stated | Objection is masked as question |
| QL-001 (Scoring) | Dimension has clear evidence | Dimension is speculative/low confidence |

### L1-L2-L3 Quantification

- **L1:** Activity metrics (emails sent, calls made, meetings booked)
- **L2:** Pipeline metrics (deals created, pipeline value, stage velocity)
- **L3:** Financial outcomes (revenue generated, margin, customer LTV)

**Scoring Framework:**
| Dimension | Weight |
|---|---|
| Response/Reply Rate | L1 (0.1x) |
| Meeting Booked | L1→L2 (0.3x) |
| Pipeline Created ($) | L2 (0.5x) |
| Revenue Closed ($) | L3 (1.0x) |

**Agent Application:**
- SDR-001/SDR-003 should optimize for L2 outcomes, not L1 activity
- QL-001 should weight L3 signals highest in composite score
- RCC-001 should measure DAG success by L2/L3 metrics

### Give-Get Homework

Before every interaction, prepare:
- **Give:** What value do I bring to this specific interaction?
  - Industry insight, relevant case study, trend data, warm introduction
- **Get:** What do I need to walk away with?
  - Specific commitment, next meeting, introduced to champion, budget validation

**Application in SDR-003:**
Each email template must pass the Give-Get test:
1. Every email GIVES something (insight, data, perspective, value)
2. Every email GETS something (reply, meeting, referral, specific answer)

### Kid Table vs Adult Table

- **Kid Table:** Talking to non-decision-makers who can't buy
- **Adult Table:** Talking to economic buyers who can write checks

**Agent heuristics:**
- QL-001: Score down deals without economic buyer access
- SDR-001: Prioritize accounts where adult table access is confirmed
- MO-004: Track whether commitments come from kid table or adult table

---

## 2. Gal Borenstein — Psychological Objection Mitigation

### The Three-Bucket Matrix

Every objection falls into one of three psychological buckets:

| Bucket | Fear | Agent Response |
|---|---|---|
| **SAFE** | "Will this get me fired?" | Risk reversal, guarantees, case studies from similar companies |
| **BEST** | "Is this the right choice vs alternatives?" | Comparative evidence, category design, clear decision criteria |
| **INNOVATIVE** | "Am I early enough / too early?" | Peer adoption proof, market timing data, FOMO via competitors adopting |

### Pattern-Matching Objection Resolution

```json
{
  "objection": "This seems expensive",
  "psychological_bucket": "SAFE",
  "root_fear": "Fear of wasting budget / getting questioned",
  "mitigation_strategy": "ROI calculator + money-back guarantee + peer proof",
  "forbidden_response": "Discounting without addressing the root fear"
}
```

### Reverse-Engineered Objections

Before any meeting, pre-identify likely objections per bucket:
1. Review prospect's industry, role, company stage
2. Generate 2 SAFE, 1 BEST, 1 INNOVATIVE predicted objection
3. Prepare mitigation for each before going in

**Agent Application (MO-003):**
- Add `psychological_bucket` field to every detected objection
- Suggested response varies by bucket, not just category
- Score meetings by how well each bucket was addressed (0-100%)

---

## 3. Paul Butterfield — Customer Journey Enablement

### The Discovery Gap

```
Current State ──── Gap ──── Desired Future State
                     │
                     └── This is where you sell
```

The gap is not what they tell you — it's what they can't articulate.

### Vision Architecture

Help the buyer build a vision of their future state that:
1. **Is vivid enough to feel real** — specific outcomes, timelines, metrics
2. **Is valuable enough to justify change** — quantified ROI vs status quo
3. **Is verifiable** — they can point to it and say "that's what I want"

### Customer Input Gating

Before presenting any solution, verify the buyer has:
1. Named the gap in their own words
2. Quantified the cost of not closing it
3. Described what success looks like (not you describing it)

**Gate check for QL-001:**
If all three are confirmed → high confidence scoring
If 0-1 confirmed → score down, flag gap in assessment

### Selling to Status Quo

The real competitor is not Vendor X. It's:
- Doing nothing
- The buyer's own inertia
- The fear of making things worse

**Agent response:** Always quantify the cost of inaction vs cost of change.

---

## 4. Jeff Shore — Cognitive Behavioral Sales Coaching

### Foundational Principle: Behavior Drives Outcome

Sales success is not about personality — it's about repeatable behaviors.
Coaching should focus on what the rep DOES, not who the rep IS.

### The Three-Legged Stool

| Leg | Description | Agent Application |
|---|---|---|
| **Skill** | Can the rep DO it? | SDR-003 template quality assessment |
| **Will** | Does the rep WANT to do it? | Emotional energy detection (MO-002) |
| **Joy** | Does the rep ENJOY doing it? | Sentiment pattern over time (MO-002) |

### Easy Equals Right

Buyers choose the path of least psychological resistance.
Every friction point reduces close probability by ~15%.

**Application in SDR-003:**
- Every CTA must be the absolute easiest possible next step
- Remove: form fills, demo requests longer than 30s, multi-step processes
- Prefer: calendar link (1 click), reply with "yes" (2 words), referral ask (warm)

### Cognitive Behavioral Objections

Objections are not logical — they're emotional with post-hoc rationalization.

```
Trigger → Thought → Emotion → Behavior
```

To change the behavior (buying), you must first identify the trigger thought.

**MO-003 enhancement:**
For each objection, trace back to the trigger thought:
- "This is expensive" → "I'll look bad if I overspend on something that fails"
- "Not right now" → "I'm overwhelmed and this is one more thing to manage"
- "Need to check with team" → "I don't have the authority/confidence to decide"

### Goal Gradient Effect

People work harder toward a goal as they get closer to it.
Show progress: "You're 80% of the way there. The last 20% is worth it."

---

## 5. Andy Paul — Selling In Framework

### Value = Progress

Buyers don't buy products — they buy progress toward a desired outcome.
Every interaction must answer: "How does this move me forward?"

### The 5 Fears Framework

Buyer resistance traces to five primal fears:
1. **Fear of loss** — "What if I lose what I already have?"
2. **Fear of failure** — "What if this doesn't work?"
3. **Fear of looking bad** — "What will others think of this decision?"
4. **Fear of the unknown** — "What if there are hidden consequences?"
5. **Fear of being sold to** — "What if I'm being manipulated?"

**MO-003 enhancement:** Map each objection to one or more of the 5 Fears.

### Dual WIIFM (What's In It For Me)

Every interaction needs TWO value propositions:
1. **Organizational WIIFM** — What the company gains
2. **Personal WIIFM** — What the INDIVIDUAL gains (promotion, recognition, less stress)

**SDR-003 enhancement:** Every email must include both.

### Selling In vs Selling To

- **Selling TO:** Presenting your solution to a passive buyer
- **Selling IN:** Helping the buyer sell YOUR solution to THEIR stakeholders

When you sell IN, your buyer becomes your champion internally.
Every SDR-003 sequence should arm the buyer to sell internally.

### Calibrated Absence

After delivering value, step back and let silence create tension.
The person who speaks first after a value moment loses negotiating power.

**Application:**
- SDR-003 follow-ups: After sending a case study, don't chase for 3 days
- MO-004: After a commitment is made, calibrate silence before following up

---

## 6. Dale Merrill — Sales Movie Trailer / Co-Creation

### The Movie Trailer

Don't tell the whole story. Show the best 2 minutes.
A sales conversation should be a trailer, not the feature film.

**Structure:**
1. **Hook (30s):** The problem they feel but haven't named
2. **Stakes (30s):** The cost of NOT solving this
3. **Tease (30s):** A glimpse of what's possible (not the full solution)
4. **Call to action (30s):** "Want to see the full movie?"

### Co-Creation

Don't pitch solutions — build them WITH the buyer.
When the buyer contributes ideas, they own the outcome.

**Agent application:**
- SDR-003 discovery questions should invite co-creation:
  "If you could wave a magic wand, what would your ideal outcome look like?"
- QL-001: Score up deals where buyer has co-created the vision
- MO-004: Track co-creation moments as commitment signals

### Value Tension

Create productive tension between:
- **Current reality** (painful but familiar)
- **Future possibility** (better but uncertain)

The tension between these two states drives action.

---

## 7. Ashley Welch — Anti-Pitch / 6/60 Rule

### The 6/60 Rule

You have 6 seconds to earn their attention and 60 seconds to earn their time.

**6 Seconds:** Subject line or opening hook
- Must be specific to THEM
- Must create curiosity gap
- Must NOT sound like marketing

**60 Seconds:** Value proposition
- State the problem (their words)
- Imply the solution (don't explain it fully)
- Ask for permission to continue

### The Anti-Pitch

Don't present. Ask permission, then diagnose before prescribing.

**Structure:**
1. "I have an observation about [their specific situation]"
2. "Would you be open to 90 seconds on how we've helped similar companies?"
3. After permission: "Here's what we did for [similar company]..."
4. "Does that resonate with what you're seeing?"

### Objection Integration

If you know they'll object, address it BEFORE they raise it.
"Some leaders in your position worry about [objection]. Here's what we've found..."

**This converts SAFE fear into BEST consideration.**

---

## 8. Brian Burns — The Brutal Truth / Curiosity Framework

### The Brutal Truth

The best sales questions are uncomfortable — for the RIGHT person.
Ask the question the buyer is afraid to ask themselves.

**Examples:**
- "What's the real cost of NOT fixing this?"
- "How long has this been a problem?"
- "What happens if nothing changes in 12 months?"

### Curiosity as a Sales Tool

Curiosity > Pitch. An open question creates more value than a polished demo.

**SDR-003 discovery question bank:**
1. "What's changed that brought this to the top of your priority list?"
2. "What have you tried so far, and why didn't it work?"
3. "If you could wave a magic wand, what would change by next quarter?"
4. "Who else in the organization is invested in solving this?"
5. "What would make this a 'must do' vs 'nice to do'?"

---

## 9. David Weiss — Hard Truths / Respect-Based Selling

### The 4 Hard Truths

1. **The buyer doesn't care about you.** They care about their problem.
2. **Your product is not special.** Differentiation is earned, not assumed.
3. **No one is waiting for your call.** You are an interruption.
4. **The buyer will lie to you.** Not maliciously — to protect themselves.

### Respect-Based Selling Protocol

**Before every interaction, ask:**
- Am I bringing value or just taking time?
- Have I earned the right to ask for their attention?
- Do I understand their world well enough to be useful?

**If the answer to any is "no" — do more research first.**

---

## 10. Cognitive & Persuasion Principles

### Mindset & Identity (10 Principles)

| # | Principle | Description | Agent Application |
|---|---|---|---|
| 1 | **Growth Mindset** | Failures are learning data, not verdicts | MO-004: Track "failure → learning" cycles |
| 2 | **Locus of Control** | Internal = agency, external = victim | MO-002: Detect internal vs external framing |
| 3 | **Self-Efficacy** | "I can do this" belief drives action | SDR-003: Use "you have what it takes" framing |
| 4 | **Identity-Based Change** | "I am the kind of person who X" | QL-001: Score self-identity alignment |
| 5 | **Cognitive Dissonance** | Inconsistency causes discomfort → change | SDR-003: Highlight gap between values and actions |
| 6 | **Confirmation Bias** | People seek evidence for what they believe | MO-002: Detect selective listening |
| 7 | **Fundamental Attribution Error** | Others' failures = character, ours = circumstances | QL-001: Flag attribution patterns in transcripts |
| 8 | **Growth vs Fixed Mindset** | Which mode is the buyer in? | MO-002: Classify buyer mindset per interaction |
| 9 | **Dunning-Kruger Effect** | Incompetence masks self-awareness | MO-002: Flag overconfidence vs underconfidence |
| 10 | **Sunk Cost Fallacy** | Continuing because already invested | QL-001: Flag sunk cost reasoning in deal scoring |

### Emotional Intelligence (10 Principles)

| # | Principle | Description | Agent Application |
|---|---|---|---|
| 11 | **Emotional Contagion** | Emotions spread between people | MO-002: Track emotional mirroring in calls |
| 12 | **Amygdala Hijack** | Stress shuts down rational thinking | MO-002: Flag stress spikes as deal risk |
| 13 | **Neuroplasticity** | The brain can rewire with practice | SDR-003: Use "we can teach your team" framing |
| 14 | **Dopamine Loops** | Anticipation of reward drives behavior | SDR-003: Create "next step" anticipation |
| 15 | **Cortisol Response** | Chronic stress degrades decision quality | MO-003: Flag cortisol triggers in objections |
| 16 | **Oxytocin Bonding** | Trust is chemical, built through shared experience | MO-004: Track rapport-building moments |
| 17 | **Mirror Neurons** | People mimic what they observe | SDR-003: Use language the buyer uses |
| 18 | **Default Mode Network** | Brain wanders when not engaged | SDR-003: Keep messages short, high-signal |
| 19 | **State-Dependent Memory** | Recall is tied to emotional state | MO-002: Align messaging with buyer state |
| 20 | **Window of Tolerance** | Optimal performance zone between boredom and panic | MO-002: Detect when buyer leaves this zone |

### Influence & Persuasion (10 Principles)

| # | Principle | Description | Agent Application |
|---|---|---|---|
| 21 | **Reciprocity** | Give first to receive | SDR-003: Always give value before asking |
| 22 | **Scarcity** | Limited availability increases desire | SDR-003: Use time/availability constraints |
| 23 | **Social Proof** | People follow peers | SDR-003: Include peer case studies |
| 24 | **Commitment & Consistency** | Small yes → bigger yes | SDR-003: Start with micro-commitments |
| 25 | **Liking** | People buy from people they like | SDR-003: Use mirroring, similarity, compliments |
| 26 | **Authority** | Credentials build trust | SDR-003: Cite relevant expertise/certifications |
| 27 | **Framing Effect** | How you frame changes the decision | SDR-003: Frame choices, don't just state facts |
| 28 | **Anchoring** | First number sets the reference | QL-001: Score anchoring effectiveness |
| 29 | **Loss Aversion** | Losing hurts 2x more than winning feels good | SDR-003: "What do you lose by waiting?" vs "What do you gain?" |
| 30 | **Paradox of Choice** | Too many options = paralysis | SDR-003: Limit choices to 2-3 max |

### Habits & Systems (10 Principles)

| # | Principle | Description | Agent Application |
|---|---|---|---|
| 31 | **Habit Loop** | Cue → Routine → Reward → Craving | MO-004: Track buyer's decision habits |
| 32 | **Implementation Intentions** | "When X happens, I will do Y" | MO-004: Score specificity of commitments |
| 33 | **Temptation Bundling** | Pair want with should | SDR-003: Frame meetings as "while you're already reviewing X..." |
| 34 | **Habit Stacking** | New habit after existing one | SDR-003: "After your weekly team meeting, let's..."" |
| 35 | **Environment Design** | Make good habits easy, bad ones hard | SDR-003: Make the CTA path frictionless |
| 36 | **Kaizen** | Continuous small improvements | RCC-001: Measure incremental agent improvement |
| 37 | **Parkinson's Law** | Work expands to fill time | SDR-003: Set specific, short meeting times |
| 38 | **Pareto Principle** | 80% of results from 20% of effort | SDR-003: Focus on the 20% of accounts that matter |
| 39 | **Zeigarnik Effect** | Unfinished tasks stick in memory | SDR-003: Create curiosity gaps that demand closure |
| 40 | **Einstellung Effect** | Existing solutions block new ones | MO-003: Flag when buyer is stuck on old solutions |

### Decision Science (10 Principles)

| # | Principle | Description | Agent Application |
|---|---|---|---|
| 41 | **System 1 vs System 2** | Fast/intuitive vs slow/analytical | SDR-003: Match decision mode to situation |
| 42 | **Peak-End Rule** | People judge experiences by peak and end | MO-004: Engineer peak moments + strong closes |
| 43 | **Serial Position Effect** | Primacy/recency bias | SDR-003: Put key info first and last |
| 44 | **Halo Effect** | One positive trait colors everything | QL-001: Guard against halo bias in scoring |
| 45 | **Affect Heuristic** | Emotion overrides analysis | MO-002: Track when emotion dominates |
| 46 | **Availability Heuristic** | Recent examples feel more likely | SDR-003: Use vivid, recent case studies |
| 47 | **Plan Continuation Bias** | Sticking with a failing plan | QL-001: Flag when deal should be disqualified |
| 48 | **Overconfidence Effect** | 93% of people think they're above average | MO-002: Detect overconfidence in buyer statements |
| 49 | **Hyperbolic Discounting** | Present rewards > future rewards | SDR-003: Show immediate value, not distant ROI |
| 50 | **Optimism Bias** | "It won't happen to me" | SDR-003: Make risks feel real and present |

---

## 11. Reverse Funnel Math / Intent Stack

### Reverse Funnel Math

Instead of "how many leads do I need to hit quota":
**"Given quota, work backward to required meetings → opportunities → pipeline → outreach"**

```
Quota: $500K
Average deal size: $50K → 10 closed deals needed
Win rate: 25% → 40 qualified opportunities needed
Qualification rate: 30% → 133 meetings needed
Meeting rate: 15% → 887 outreach sequences needed
```

### Intent Stack Framework

Layer signals by buying intent weight:

| Layer | Signal Type | Weight | Decay |
|---|---|---|---|
| 1 | Direct demo request | 10x | None — immediate outreach |
| 2 | Pricing page visit | 7x | 24hr window |
| 3 | Case study / content consumption | 5x | 72hr window |
| 4 | Job change / new role | 4x | 7 day window |
| 5 | Tech stack change | 3x | 14 day window |
| 6 | Funding / acquisition | 2x | 30 day window |
| 7 | Social media mention | 1x | 7 day window |
| 8 | General industry content | 0.5x | Low signal |

---

## 12. Multi-Channel Sequence Architecture

### Sequence Design Principles

1. **Every touch gives value before asking for it**
2. **Channel diversification increases reach 3x**
   - Email + LinkedIn + Call = 68% contact rate
   - Email only = 23% contact rate
3. **Gap between touches increases over time**
   - Touch 1→2: 2 days
   - Touch 2→3: 4 days
   - Touch 3→4: 7 days
   - Touch 4→5: 10 days
4. **Every touch must have a different angle**
   - Rotate: value insight → social proof → urgency → direct ask → breakup
5. **Breakup email triggers 30%+ response rate**
   - Closing the loop creates psychological permission to reply

### Channel-Specific Psychology

| Channel | Strength | Psychology |
|---|---|---|
| Email | Long-form value | Attention, Curiosity Gap, Social Proof |
| LinkedIn | Social credibility | Liking, Authority, Social Proof |
| Phone | Real-time conversation | Emotional Contagion, Mirroring, Rapport |
| Video | Visual trust-building | Oxytocin Bonding, Mirror Neurons |
| Direct Mail | Physical surprise | Reciprocity, Scarcity, Novelty |
