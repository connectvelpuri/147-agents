#!/usr/bin/env python3
"""
revenue-os — Command-line interface for Revenue OS agents.

Usage:
  revenue-os "qualify this $500K deal"                    # Single query
  revenue-os --persona negotiation "negotiate procurement"  # Specific persona
  revenue-os --interactive                                 # Interactive mode
  revenue-os --train "MEDDPICC scoring guide"              # Train with knowledge
  revenue-os --learn                                       # Show learning loop stats
  revenue-os --whatsapp                                    # Start WhatsApp bridge
"""

import os, sys, json, argparse
from datetime import datetime

# Add agents to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.join(script_dir, "agents"))

VERSION = "2.0.0"
API_URL = os.environ.get("REVENUE_OS_API_URL", "https://saleshouse-production.up.railway.app")
API_KEY = os.environ.get("REVENUE_OS_API_KEY", "rev-dev-key-2026")

PERSONAS = {
    "qualify": ("meddpicc_qualifier", "Deal Qualification Authority — 10 experts"),
    "negotiate": ("negotiation", "Master Negotiator — Voss, Fisher, Ury, Cohen..."),
    "psychology": ("buyer_psychology", "Buyer Behavior — Cialdini, Kahneman, Ariely..."),
    "value": ("value_engineer", "Value Architect — Porter, Christensen, Moore..."),
    "prospect": ("prospecting_sdr", "Elite Prospector — Ross, Konrath, Barrows..."),
    "strategy": ("revenue_orchestrator", "Revenue Conductor — Jobs, Welch, Buffett..."),
    "coach": ("call_coacher", "Sales Coach — Gong Labs, McMahon, Orlob..."),
}

def detect_persona(task):
    """Auto-detect persona from task text."""
    task_lower = task.lower()
    for keyword, (pid, title) in sorted(PERSONAS.items(), key=lambda x: -len(x[0])):
        if keyword in task_lower:
            return pid, title
    return "revenue_orchestrator", "Revenue Orchestra Conductor"

def call_api(task, persona=None, context="", training=""):
    """Call the Revenue OS API."""
    if not persona:
        persona, _ = detect_persona(task)
    
    payload = {"task": task, "persona": persona}
    if context:
        payload["context"] = context
    if training:
        payload["training"] = training
    
    try:
        import httpx
        r = httpx.post(f"{API_URL}/api/agent/execute",
            json=payload,
            headers={"Content-Type": "application/json", "X-API-Key": API_KEY},
            timeout=120)
        return r.json()
    except ImportError:
        # Fallback: run locally
        return call_local(task, persona, context, training)
    except Exception as e:
        return {"success": False, "response": f"Error: {e}", "persona": persona}

def call_local(task, persona, context, training):
    """Run agent locally (no API needed)."""
    try:
        from agent_base.agent_wrapper import AgentIntelligence, TRAINING_MODULES
        from agent_base.personas import PERSONA_IDS
        
        ai = AgentIntelligence(persona if persona in PERSONA_IDS else "revenue_orchestrator", 
                              persona.replace("_", " ").title() if persona else "Revenue OS")
        
        training_text = ""
        if training:
            training_text = training
        elif context:
            training_text = context
        
        result = ai.execute(task=task, data={"context": context} if context else None, 
                          training=training_text, temperature=0.3)
        return result
    except ImportError as e:
        return {"success": False, "response": f"Local mode unavailable: {e}", "persona": persona}

def interactive_mode():
    """Interactive CLI mode."""
    print(f"\n{'='*60}")
    print(f"  Revenue OS v{VERSION} — AI Sales Agent Platform")
    print(f"{'='*60}")
    print(f"  Connected to: {API_URL}")
    print(f"  Type 'help' for personas, 'learn' for learning stats, 'quit' to exit")
    print()
    
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not line:
            continue
        if line.lower() in ("quit", "exit", "q"):
            break
        if line.lower() in ("help", "h", "?"):
            print("\nPersonas (auto-detected from keywords):")
            for kw, (pid, title) in sorted(PERSONAS.items()):
                print(f"  [{kw:12s}] → {title}")
            print("\nCommands:")
            print("  learn           Show learning loop stats")
            print("  --persona X     Force a specific persona")
            continue
        
        if line.lower() == "learn":
            show_learning_stats()
            continue
        
        # Parse special commands
        task = line
        persona = None
        if " --persona " in line:
            parts = line.split(" --persona ")
            task = parts[0]
            persona = parts[1].strip().split()[0] if parts[1].strip() else None
        
        # Call API or local
        result = call_api(task, persona)
        display_result(result, task)

def display_result(result, task):
    """Display agent result."""
    persona = result.get("persona", "unknown")
    response = result.get("response", "No response")
    success = result.get("success", False)
    
    print(f"\n  🤖 [{persona}]")
    print(f"  {'─'*55}")
    if success and response:
        print(f"  {response[:1500]}")
        if len(response) > 1500:
            print(f"  ... (truncated, {len(response)} total chars)")
    else:
        print(f"  {response}")
    print()

def show_learning_stats():
    """Show learning loop statistics."""
    try:
        from agent_base.learning_loop import LearningLoop
        loop = LearningLoop()
        summary = loop.summary()
        print(f"\n📊 Learning Loop Statistics:")
        print(f"  Lessons stored: {summary.get('total_lessons', 0)}")
        print(f"  Agents learning: {summary.get('agents', 0)}")
        print(f"  Last reflection: {summary.get('last_reflection', 'never')}")
        print()
    except ImportError:
        print("\nLearning loop not available. Install dependencies first.")
        print()

def main():
    parser = argparse.ArgumentParser(description="Revenue OS CLI — AI Sales Agent Platform")
    parser.add_argument("query", nargs="?", help="Sales query to analyze")
    parser.add_argument("--persona", "-p", help="Force specific persona")
    parser.add_argument("--context", "-c", help="Add context to the query")
    parser.add_argument("--train", "-t", help="Training knowledge to inject")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--learn", "-l", action="store_true", help="Show learning stats")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument("--local", action="store_true", help="Run locally (no API)")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Revenue OS v{VERSION}")
        return
    
    if args.learn:
        show_learning_stats()
        return
    
    if args.interactive or not args.query:
        interactive_mode()
        return
    
    # Single query mode
    result = call_api(args.query, args.persona, args.context or "", args.train or "")
    display_result(result, args.query)

if __name__ == "__main__":
    main()
