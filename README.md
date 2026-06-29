# DealForge

> **147 AI Agents . 70 World-Class Experts . One CLI**
> Forge smarter deals. Close faster.

---

## The Pain

**Sales teams use 8+ disconnected tools.** Gong records calls but can't prospect. Outreach sequences emails but can't analyze buyer psychology. Salesforce qualifies deals but can't run negotiation strategy. Every tool solves ONE piece. Nothing connects them.

**Your best reps have 15+ years of instincts.** MEDDPICC. Challenger. SPIN. Gap Selling. Cialdini. When they leave, that knowledge walks out. New reps take 12+ months to ramp.

**Deals die silently.** Stalled at legal because nobody prepped procurement defense. Champions go unsupported. Competitive threats go unnoticed until the loss review.

---

## What Makes This Different

| Traditional Tools | DealForge |
|:-----------------|:----------|
| One function per tool | **Full revenue lifecycle**: prospect > qualify > negotiate > close > coach |
| Generic AI prompts | **70 world-class experts** as agent personas (Voss, Cialdini, Jobs, Buffett...) |
| Single-agent response | **Multi-agent orchestration**: 3-4 agents analyze in parallel |
| Monthly SaaS fees | **$0 open source** - bring your own LLM key |

---

## How It Works

```
                         YOU
                          |
                    ------v------
                    |  Ask your  |
                    |  question  |
                    ------+------
                          |
              ------------+-----------
              |   Intent Detector    |
              |  (deal? negotiate?   |
              |   pipeline? buyer?)  |
              ------------+-----------
                          |
              ------------+-----------
              |  5 Clarifying        |
              |  Questions           |
              |  (consultant-style)  |
              ------------+-----------
                          |
         ----------------+----------------
         v               v                v
  +-----------+   +-----------+   +-----------+
  |  MEDDPICC |   |   Buyer   |   |  Master   |
  | Qualifier |   | Psychology|   | Negotiator|
  | 10 experts|   | 10 experts|   | 10 experts|
  +-----------+   +-----------+   +-----------+
         |               |                |
         +---------------+----------------+
                          |
              ------------+-----------
              |  McKinsey-Level      |
              |  Analysis Report     |
              |  + Follow-up Qs      |
              ------------------------
```

---

## 7 Agent Personas (70 Combined Experts)

| Agent | 10 Experts Behind It |
|-------|---------------------|
| **MEDDPICC Qualifier** | Dunkel, Gong Labs, Rackham, Dixon, McMahon, Antonio, Whyte, Weisberg, Sandler, Blount |
| **Master Negotiator** | Voss, Fisher, Ury, Cohen, Camp, Karrass, Cialdini, Kupfer, Shell, Malhotra |
| **Buyer Behavior** | Cialdini, Kahneman, Ariely, Carnegie, Munger, Greene, Thaler, Ogilvy, Godin, Robbins |
| **Value Architect** | Porter, Christensen, Moore, Sinek, Thiel, Ferriss, Rose, Tracy, Balfour, Peters |
| **Elite Prospector** | Ross, Konrath, Barrows, Bertuzzi, Efti, Tyler, Schultz, Coggins, Iannarino, Cardone |
| **Revenue Conductor** | Jobs, Welch, Grove, Drucker, Bezos, Sandberg, Nadella, Powell, Buffett, Dalio |
| **Sales Call Coach** | Gong Labs, McMahon, Chorus, Weinberg, Priemer, Dixon, Orlob, Blount, Ziglar, Barrows |

---

## Quick Start

```bash
git clone https://github.com/connectvelpuri/147-agents.git
cd 147-agents
pip install -r requirements.txt
python cli.py --logo
```

### Interactive Mode

```bash
python cli.py
```

Type naturally:

| You type | What happens |
|----------|-------------|
| `qualify this $500K deal` | MEDDPICC Qualifier |
| `negotiate with procurement` | Master Negotiator |
| `analyze buyer psychology` | Buyer Behavior Expert |
| `build an ROI case` | Value Architect |
| `/help` | Show commands |
| `/quit` | Exit |

### Multi-Agent Deep Dive (Best Feature)

Asks 5 clarifying questions first, then runs 3-4 agents:

```bash
python cli.py "I need to win a $2M deal against Oracle" --api-key your-key
```

### Single Query

```bash
python cli.py "qualify this $500K enterprise deal" --api-key your-key
```

---

## Example

```
$ python cli.py --api-key sk-or-...n

> I need to win a $2M enterprise deal

? Deal value and stage?  $2M, stuck at legal review
? Decision-makers?  CIO + Procurement Director
? Competitors?  Oracle
? Biggest concern?  Implementation risk
? Your champion?  VP of Engineering

PERSPECTIVE 1: MEDDPICC QUALIFIER (Score: 32/40)
Gap: Economic buyer not engaged
Action: Schedule CIO briefing

PERSPECTIVE 2: BUYER PSYCHOLOGY
Procurement is risk-averse. Champion needs ammunition.
Action: Build TCO comparison for VP Eng

PERSPECTIVE 3: MASTER NEGOTIATOR
Oracle competes on price. Your speed is the advantage.
Action: Build switching cost narrative
```

---

## Bring Your Own AI

```bash
export OPENROUTER_API_KEY=*** cli.py --api-key $OPENROUTER_API_KEY
```

Free models: `openrouter/free`, `nvidia/nemotron-3-ultra-550b-a55b:free`

---

## Project Structure (22 files)

```
dealforge/
  cli.py                       # Main CLI (the only file you need)
  agents/agent_base/
    llm_client.py              # Routes to OpenRouter / Anthropic / NVIDIA
    agent_wrapper.py           # Wires persona to LLM
    personas/                  # 7 expert persona definitions
  api/webhook.py               # WhatsApp + API server (optional)
  requirements.txt             # 4 dependencies
  LICENSE                      # MIT
  README.md                    # This file
```

---

## License

MIT - free to use, modify, sell, deploy.
