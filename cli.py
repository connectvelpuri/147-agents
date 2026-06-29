#!/usr/bin/env python3
"""SalesHelp CLI v3.0 - McKinsey-Level Revenue Analysis."""
import sys, json, os, argparse, subprocess
from datetime import datetime

LOGO = """
   ╔═══════════════════════════════════════════╗
   ║    ███████  █████  ██      ███████        ║
   ║    ██      ██   ██ ██      ██             ║
   ║    ███████ ███████ ██      ███████        ║
   ║         ██ ██   ██ ██           ██        ║
   ║    ███████ ██   ██ ███████ ███████        ║
   ║                                           ║
   ║    Revenue OS - SalesHelp CLI v3.0        ║
   ║    McKinsey-Level Multi-Agent Analysis    ║
   ╚═══════════════════════════════════════════╝
"""


class C:
    R = chr(27) + "[0m"
    B = chr(27) + "[1m"
    D = chr(27) + "[2m"
    G = chr(27) + "[92m"
    Y = chr(27) + "[93m"
    C = chr(27) + "[96m"
    M = chr(27) + "[95m"
    LINE = "-" * 50

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
    except:
        pass

# === INTAKE QUESTIONS (McKinsey-style discovery) ===

QUESTIONS = {
    "deal": [
        "What is the deal value and current stage?",
        "Who are the decision-makers and what do each care about?",
        "Which competitors are involved and what is their position?",
        "What is the prospect's biggest concern or objection?",
        "What evidence do you have that your champion is real?",
    ],
    "negotiate": [
        "What is your walkaway point (BATNA)?",
        "What does the other side need most from this deal?",
        "What is the confirmed budget range?",
        "Who has signing authority on their side?",
        "What concessions have already been discussed?",
    ],
    "buyer": [
        "What is the buyer's role and seniority level?",
        "What is their personal risk if this fails?",
        "Who else influences their decision (peers, boss, board)?",
        "What would make them look like a hero internally?",
        "What past experience do they have with your company?",
    ],
    "competitor": [
        "Which competitor and why are they leading?",
        "What is their pricing compared to yours?",
        "What is their known weakness in this situation?",
        "What relationships or history do they have?",
        "What unique advantage do you have that they cannot match?",
    ],
    "pipeline": [
        "What is your total pipeline vs quota?",
        "Which stage has the most stuck deals?",
        "What is your win rate by deal size bracket?",
        "What is your average sales cycle length?",
        "Which reps are above vs below quota?",
    ],
}

GENERAL = [
    "What specific outcome do you want?",
    "What is the current situation?",
    "What is blocking progress?",
    "Who is involved in the decision?",
    "What does success look like?",
]

ALL_AGENTS = {
    "meddpicc_qualifier": "MEDDPICC Deal Qualification (+10 experts: Dunkel, Gong, Rackham, Dixon, McMahon)",
    "negotiation": "Strategic Negotiation (+10 experts: Voss, Fisher, Ury, Cohen, Camp)",
    "buyer_psychology": "Buyer Psychology (+10 experts: Cialdini, Kahneman, Ariely, Carnegie, Robbins)",
    "value_engineer": "Value Engineering (+10 experts: Porter, Christensen, Moore, Sinek, Tracy)",
    "prospecting_sdr": "Sales Development (+10 experts: Ross, Konrath, Cardone, Barrows, Bertuzzi)",
    "revenue_orchestrator": "Revenue Strategy (+10 experts: Jobs, Welch, Drucker, Buffett, Dalio)",
    "call_coacher": "Sales Call Coaching (+10 experts: Gong Labs, Ziglar, Blount, Orlob, Barrows)",
}

def detect_intent(q):
    q = q.lower()
    if any(w in q for w in ["deal","win","opportunity","pipeline","forecast","revenue"]):
        return "deal"
    if any(w in q for w in ["negotiate","price","contract","terms","close","procurement"]):
        return "negotiate"
    if any(w in q for w in ["competitor","compete","versus","battle","rival"]):
        return "competitor"
    if any(w in q for w in ["buyer","stakeholder","cio","cfo","executive","influence"]):
        return "buyer"
    if any(w in q for w in ["pipe","stage","forecast","velocity","coverage","sdr"]):
        return "pipeline"
    return None

def ask_intake(intent):
    qs = QUESTIONS.get(intent, GENERAL)
    answers = {}
    print(f"\n{C.C}{C.LINE}{C.R}")
    print(f"{C.B}Let me understand your situation better.{C.R}")
    print(f"{C.D}I will ask a few questions before running analysis.{C.R}")
    print(f"{C.C}{C.LINE}{C.R}\n")
    for q in qs:
        ans = input(f"{C.Y}? {q}{C.R}\n{C.D}> {C.R}").strip()
        answers[q] = ans
    return answers

def get_agents_for(intent):
    if intent == "deal": return ["meddpicc_qualifier", "buyer_psychology", "negotiation", "value_engineer"]
    if intent == "negotiate": return ["negotiation", "meddpicc_qualifier", "buyer_psychology"]
    if intent == "competitor": return ["meddpicc_qualifier", "buyer_psychology", "value_engineer"]
    if intent == "buyer": return ["buyer_psychology", "meddpicc_qualifier", "value_engineer"]
    if intent == "pipeline": return ["revenue_orchestrator", "prospecting_sdr", "meddpicc_qualifier"]
    return ["revenue_orchestrator", "meddpicc_qualifier", "buyer_psychology"]

def print_report(context, intent, agent_id, responses):
    print(f"\n{C.C}{'='*55}{C.R}")
    print(f"{C.B}     McKINSEY-LEVEL ANALYSIS REPORT{C.R}")
    print(f"{C.C}{'='*55}{C.R}")
    print(f"\n{C.Y}EXECUTIVE SUMMARY{C.R}")
    print(f"{C.LINE}")
    print(f"Analysis: {intent.upper()} scenario")
    print(f"Agents consulted: {len(responses)}")
    print(f"Context: {context[:100]}...")
    print(f"\n{C.Y}PERSPECTIVE 1: {ALL_AGENTS.get(agent_id[0], agent_id[0])}{C.R}")
    print(responses[0][:800] if responses else "(no response)")
    print(f"\n{C.Y}PERSPECTIVE 2: {ALL_AGENTS.get(agent_id[1], agent_id[1])}{C.R}")
    print(responses[1][:800] if len(responses) > 1 else "(no response)")
    print(f"\n{C.Y}PERSPECTIVE 3: {ALL_AGENTS.get(agent_id[2], agent_id[2])}{C.R}")
    print(responses[2][:800] if len(responses) > 2 else "(no response)")
    print(f"\n{C.C}{'='*55}{C.R}")
    print(f"\n{C.G}FOLLOW-UP QUESTIONS YOU CAN ASK:{C.R}")
    followups = [
        "Deep dive on competitor weaknesses",
        "Negotiation scenario planning",
        "Stakeholder influence mapping",
        "ROI and business case building",
        "Call coaching for next meeting",
    ]
    for i, f in enumerate(followups, 1):
        print(f"  {i}. {f}")
    print()

def route_single(q):
    for kw, pid in [("qualify","meddpicc_qualifier"),("meddpicc","meddpicc_qualifier"),
                     ("negotiate","negotiation"),("deal","negotiation"),
                     ("psychology","buyer_psychology"),("buyer","buyer_psychology"),
                     ("value","value_engineer"),("roi","value_engineer"),
                     ("prospect","prospecting_sdr"),("lead","prospecting_sdr"),
                     ("strategy","revenue_orchestrator"),("pipeline","revenue_orchestrator"),
                     ("coach","call_coacher"),("call","call_coacher")]:
        if kw in q.lower():
            return pid
    return "revenue_orchestrator"

def api_execute(url, key, task, pid):
    try:
        import urllib.request
        payload = json.dumps({"task": task, "persona": pid}).encode()
        req = urllib.request.Request(url + "/api/agent/execute", data=payload,
            headers={"Content-Type": "application/json", "X-API-Key": key}, method="POST")
        resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
        return resp.get("response", "")
    except Exception as e:
        return f"[API Error: {e}]"

def main():
    p = argparse.ArgumentParser(description="SalesHelp - McKinsey-Level Analysis CLI")
    p.add_argument("query", nargs="*")
    p.add_argument("--api-key", default=os.environ.get("REVENUE_OS_API_KEY", ""))
    p.add_argument("--url", default=os.environ.get("REVENUE_OS_API_URL", "https://saleshouse-production.up.railway.app"))
    p.add_argument("--persona", default="")
    p.add_argument("--logo", action="store_true")
    args = p.parse_args()

    if args.logo:
        print(LOGO)
        return

    api_available = bool(args.api_key)
    url = args.url.rstrip("/")
    key = args.api_key

    # Single query
    if args.query:
        q = " ".join(args.query)
        intent = detect_intent(q)
        if intent and api_available:
            print(f"\n{C.C}Initial assessment: {intent.upper()} opportunity{C.R}")
            answers = ask_intake(intent)
            ctx = "; ".join(f"{k}: {v}" for k, v in answers.items())
            agents = get_agents_for(intent)
            print(f"\n{C.C}Running multi-agent analysis...{C.R}")
            responses = []
            for pid in agents:
                name = ALL_AGENTS.get(pid, pid).split("(")[0].strip()
                print(f"  {C.D}Consulting {name}...{C.R}")
                resp = api_execute(url, key, f"{q} Context: {ctx}", pid)
                responses.append(resp[:500])
                print(f"  {C.G}Done.{C.R}")
            print_report(ctx, intent, agents, responses)
        else:
            pid = args.persona if args.persona else route_single(q)
            name = ALL_AGENTS.get(pid, pid).split("(")[0].strip()
            print(f"{C.C}Routed to: {name}{C.R}")
            if api_available:
                resp = api_execute(url, key, q, pid)
                print(f"{C.G}{resp[:1500]}{C.R}")
            else:
                print(f"{C.Y}Set --api-key for AI responses. Try: --api-key rev-dev-key-2026{C.R}")
        return

    # Interactive
    subprocess.run(["cls" if sys.platform == "win32" else "clear"], shell=True, capture_output=True)
    print(f"{C.C}{LOGO}{C.R}")

    if api_available:
        try:
            h = json.loads(urllib.request.urlopen(urllib.request.Request(url + "/health"), timeout=10).read())
            print(f"  {C.G}Server: {url} | agents={h.get('agents_loaded')} personas={h.get('personas')}{C.R}")
        except:
            print(f"  {C.Y}Server: {url} (unreachable){C.R}")
    else:
        print(f"  {C.Y}Offline. Add --api-key for AI.{C.R}")

    print(f"\n{C.D}Type your question. The system will ask clarifying questions first for deep analysis.{C.R}\n")

    while True:
        try:
            q = input(f"{C.C}> {C.R}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.G}Goodbye!{C.R}")
            break
        if not q: continue

        if q.startswith("/"):
            cmd = q[1:].lower()
            if cmd in ("quit","q","exit"): print(f"{C.G}Goodbye!{C.R}"); break
            elif cmd in ("help","h"):
                print(f"Commands: /help /personas /deepdive /clear /status /quit")
            elif cmd == "personas":
                for pid, desc in ALL_AGENTS.items():
                    print(f"  {C.C}{pid:<25}{C.R} {desc}")
            elif cmd in ("clear","cls"):
                subprocess.run(["cls" if sys.platform == "win32" else "clear"], shell=True)
                print(f"{C.C}{LOGO}{C.R}")
            elif cmd == "deepdive":
                print(f"Ask a question and I will run multi-agent analysis.")
            else:
                print(f"Unknown. Try /help")
            continue

        # Process with intake
        intent = detect_intent(q)
        if intent and api_available:
            print(f"\n{C.C}Detected: {intent.upper()} opportunity{C.R}")
            answers = ask_intake(intent)
            ctx = "; ".join(f"{k}: {v}" for k, v in answers.items())
            agents = get_agents_for(intent)
            print(f"\n{C.C}Running multi-agent deep analysis...{C.R}")
            responses = []
            for pid in agents:
                name = ALL_AGENTS.get(pid, pid).split("(")[0].strip()
                print(f"  {C.D}Consulting {name}...{C.R}", end="", flush=True)
                resp = api_execute(url, key, f"{q} Context: {ctx}", pid)
                responses.append(resp[:500])
                print(f" {C.G}done{C.R}")
            print_report(ctx, intent, agents, responses)
        else:
            pid = args.persona if args.persona else route_single(q)
            name = ALL_AGENTS.get(pid, pid).split("(")[0].strip()
            print(f"{C.C}Routed to: {name}{C.R}")
            if api_available:
                resp = api_execute(url, key, q, pid)
                print(f"{C.G}{resp[:2000]}{C.R}")
            else:
                print(f"{C.Y}[offline - add --api-key]{C.R}")
        print()

if __name__ == "__main__":
    main()
