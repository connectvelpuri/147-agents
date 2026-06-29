#!/usr/bin/env python3
"""SalesHelp CLI v3.0 - McKinsey-Level Revenue Analysis."""
import sys, json, os, argparse, random, subprocess
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

def local_execute(task, pid, system_prompt="", reflect=False, vote=False, cot=False):
    """Execute directly using LLM client - no server needed."""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
        from agent_base.llm_client import LLMClient, DynamicRouter
        from agent_base.agent_wrapper import AgentIntelligence
        
        # Determine tier dynamically
        tier = DynamicRouter.route(task, task)
        
        ai = AgentIntelligence(pid, pid.replace("_"," ").title())
        sp = ai.build_prompt(task) if not system_prompt else system_prompt
        
        client = LLMClient(provider="openrouter", tier=tier)
        result = client.complete(
            system_prompt=sp,
            user_prompt=task,
            reflect=reflect,
            self_consistency=vote,
            chain_of_thought=cot,
        )
        
        if result.success:
            output = result.text
            if result.confidence:
                output += f"\n\n[Confidence: {result.confidence:.0f}% | Model: {result.model}]"
            if result.reasoning and cot:
                output = f"[Reasoning]\n{result.reasoning[:500]}\n\n" + output
            return output
        return f"[Error: {result.error}]"
    except Exception as e:
        return f"[Local execution error: {e}]"
    except Exception as e:
        return f"[API Error: {e}]"



# =============================================================================
# MODULE 1: Web Research Agent (free, no API key needed)
# =============================================================================

class WebResearch:
    """Research accounts, competitors, news using free sources."""
    
    @staticmethod
    def search(query, num_results=5):
        """Search the web using DuckDuckGo (free, no API key)."""
        try:
            import httpx
            encoded = query.replace(" ", "+")
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, follow_redirects=True)
            if r.status_code == 200:
                import re
                # Extract result snippets
                results = re.findall(r'class="result__snippet">(.*?)</a>', r.text, re.DOTALL)
                links = re.findall(r'class="result__url"[^>]*href="(https?://[^"]+)"', r.text)
                titles = re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', r.text, re.DOTALL)
                
                snippets = []
                for i in range(min(num_results, len(results))):
                    title = titles[i].strip() if i < len(titles) else ""
                    snip = results[i].strip() if i < len(results) else ""
                    link = links[i] if i < len(links) else ""
                    snippets.append(f"  {title}\n  {snip}\n  {link}")
                
                return "\n".join(snippets) if snippets else "No results found."
            return f"Search returned {r.status_code}"
        except ImportError:
            return "Install httpx: pip install httpx"
        except Exception as e:
            return f"Search error: {e}"
    
    @staticmethod
    def research_company(company_name):
        """Research a company - news, funding, competitors."""
        queries = [
            f"{company_name} company overview 2026",
            f"{company_name} recent news funding",
            f"{company_name} competitors market position",
            f"{company_name} technology stack partnerships",
        ]
        results = []
        for q in queries:
            result = WebResearch.search(q, 3)
            results.append(f"=== {q} ===\n{result}")
        return "\n\n".join(results)
    
    @staticmethod
    def research_person(person_name, company=""):
        """Research a person - role, background."""
        query = f"{person_name} {company}" if company else person_name
        query += " LinkedIn profile bio"
        return WebResearch.search(query, 5)


# =============================================================================
# MODULE 2: CRM Integration (HubSpot free API)
# =============================================================================

class CRMConnector:
    """Connect to HubSpot or Salesforce CRM."""
    
    @staticmethod
    def format_deal(deal):
        """Format a deal dict for display."""
        if not deal:
            return "No deal data"
        name = deal.get('properties', {}).get('dealname', deal.get('name', 'Unknown'))
        amount = deal.get('properties', {}).get('amount', deal.get('amount', 'N/A'))
        stage = deal.get('properties', {}).get('dealstage', deal.get('stage', 'N/A'))
        return f"  {name} | ${amount} | {stage}"
    
    @staticmethod
    def from_hubspot(api_key=None):
        """Read pipeline from HubSpot API."""
        key = api_key or os.environ.get("HUBSPOT_API_KEY", "")
        if not key:
            return "No HubSpot API key. Set HUBSPOT_API_KEY or use --crm-key"
        try:
            import httpx
            r = httpx.get(
                "https://api.hubapi.com/crm/v3/objects/deals",
                headers={"Authorization": f"Bearer {key}"},
                params={"limit": 20, "properties": "dealname,amount,dealstage,createdate"},
                timeout=30
            )
            if r.status_code == 200:
                deals = r.json().get('results', [])
                if not deals:
                    return "No deals found in HubSpot"
                return "\n".join(CRMConnector.format_deal(d) for d in deals)
            return f"HubSpot error: {r.status_code} {r.text[:200]}"
        except ImportError:
            return "Install httpx: pip install httpx"
        except Exception as e:
            return f"HubSpot error: {e}"
    
    @staticmethod
    def from_salesforce(api_key=None):
        """Read pipeline from Salesforce (basic REST API)."""
        # Placeholder - Salesforce requires OAuth which is complex
        return "Salesforce integration requires OAuth setup. Use HubSpot for simpler API access."


# =============================================================================
# MODULE 3: PDF Report Generator
# =============================================================================

class PDFReport:
    """Generate professional PDF reports from agent analysis."""
    
    @staticmethod
    def generate(text, filename="dealforge_report"):
        """Generate a PDF report from analysis text."""
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 20)
            pdf.cell(0, 15, "DealForge Analysis Report", align="C")
            pdf.ln(20)
            
            # Add timestamp
            from datetime import datetime
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="R")
            pdf.ln(15)
            
            # Add content
            pdf.set_font("Helvetica", "", 11)
            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    pdf.ln(5)
                    continue
                # Detect headers
                if line.startswith("PERSPECTIVE") or line.startswith("=="):
                    pdf.set_font("Helvetica", "B", 13)
                    pdf.cell(0, 10, line[:80])
                    pdf.ln(10)
                    pdf.set_font("Helvetica", "", 11)
                elif line.startswith("  "):
                    pdf.cell(10)
                    pdf.multi_cell(0, 6, line.strip())
                else:
                    pdf.multi_cell(0, 6, line)
            
            filename += ".pdf"
            pdf.output(filename)
            return f"PDF saved: {filename}"
        except ImportError:
            # Fallback: save as markdown
            filename += ".md"
            with open(filename, 'w') as f:
                f.write(f"# DealForge Analysis Report\n\n{text}")
            return f"PDF library not installed. Saved as markdown: {filename}"
        except Exception as e:
            return f"PDF error: {e}"


# =============================================================================
# MODULE 4: LinkedIn Research (via public data)
# =============================================================================

class LinkedInResearch:
    """Research companies and people on LinkedIn via public sources."""
    
    @staticmethod
    def company(company_name):
        """Get LinkedIn company info."""
        return WebResearch.search(f"LinkedIn {company_name} company about", 5)
    
    @staticmethod
    def person(name, company=""):
        """Get LinkedIn person info."""
        query = f"LinkedIn {name}"
        if company:
            query += f" {company}"
        return WebResearch.search(query, 5)
    
    @staticmethod
    def mutual_connections(person1, person2):
        """Find mutual connections (public data only)."""
        return WebResearch.search(f"{person1} {person2} mutual connections LinkedIn", 3)


# =============================================================================
# MODULE 5: Human-in-the-Loop Gates
# =============================================================================

class HITLGates:
    """Human approval gates for critical actions."""
    
    @staticmethod
    def require_approval(action, description, approver="Manager"):
        """Ask for human approval before proceeding."""
        print(f"\n{C.Y}[APPROVAL REQUIRED]{C.R}")
        print(f"  Action: {action}")
        print(f"  Details: {description}")
        print(f"  Approver: {approver}")
        response = input(f"  {C.Y}Approve? (yes/no): {C.R}").strip().lower()
        if response in ('yes', 'y', 'approve'):
            print(f"  {C.G}Approved.{C.R}")
            return True
        else:
            print(f"  {C.R}Rejected.{C.R}")
            return False
    
    @staticmethod
    def review_before_send(content, channel="email"):
        """Review message content before sending."""
        print(f"\n{C.Y}[REVIEW BEFORE SENDING - {channel.upper()}]{C.R}")
        print(f"  Content preview:\n{content[:500]}")
        response = input(f"  {C.Y}Send? (yes/no/edit): {C.R}").strip().lower()
        if response == 'yes' or response == 'y':
            print(f"  {C.G}Sent.{C.R}")
            return True
        elif response == 'edit':
            edited = input(f"  {C.Y}Edit message: {C.R}")
            print(f"  {C.G}Sent (edited).{C.R}")
            return True
        else:
            print(f"  {C.R}Cancelled.{C.R}")
            return False

def main():
    p = argparse.ArgumentParser(description="SalesHelp - McKinsey-Level Analysis CLI")
    p.add_argument("query", nargs="*")
    p.add_argument("--api-key", default=os.environ.get("REVENUE_OS_API_KEY", ""))
    p.add_argument("--url", default=os.environ.get("REVENUE_OS_API_URL", "https://saleshouse-production.up.railway.app"))
    p.add_argument("--persona", default="")
    p.add_argument("--reflect", action="store_true", help="Reflection loop - self-critique")
    p.add_argument("--vote", action="store_true", help="Self-consistency voting (3x runs)")
    p.add_argument("--cot", action="store_true", help="Chain-of-thought reasoning")
    p.add_argument("--web", action="store_true", help="Research accounts/competitors via web")
    p.add_argument("--crm", action="store_true", help="Import pipeline from CRM (HubSpot)")
    p.add_argument("--crm-key", default="", help="CRM API key")
    p.add_argument("--pdf", action="store_true", help="Export analysis as PDF report")
    p.add_argument("--linkedin", action="store_true", help="Research via LinkedIn public data")
    p.add_argument("--approve", action="store_true", help="Human-in-the-loop approval gates")
    p.add_argument("--logo", action="store_true", help="Show logo")
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
        
        # Web research before analysis
        if args.web:
            print(f"\n{C.C}Researching the web...{C.R}")
            if any(term in q.lower() for term in ["company", "competitor", "account", "market"]):
                company = q.replace("research", "").replace("analyze", "").strip()
                research = WebResearch.research_company(company)
                print(f"  {C.D}{research[:500]}...{C.R}")
            else:
                research = WebResearch.search(q)
                print(f"  {C.D}{research[:300]}...{C.R}")
        
        # CRM pipeline import
        if args.crm:
            print(f"\n{C.C}Importing CRM pipeline...{C.R}")
            crm_key = args.crm_key or os.environ.get("HUBSPOT_API_KEY", "")
            deals = CRMConnector.from_hubspot(crm_key)
            print(f"  {C.D}{deals[:500]}{C.R}")
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
