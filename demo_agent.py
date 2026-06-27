"""
Revenue OS End-to-End Demo — Run without any API keys or cloud dependencies.
Tests the complete agent pipeline: route -> persona -> LLM -> response.

Usage:
    python demo_agent.py              # Interactive mode
    python demo_agent.py "qualify this deal..."  # Single query
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))

HAS_DEPENDENCIES = True
try:
    from agent_base.agent_wrapper import AgentIntelligence, TRAINING_MODULES
    from agent_base.personas import PERSONA_IDS, get_persona
except ImportError as e:
    HAS_DEPENDENCIES = False
    print(f"Warning: {e}")

ROUTING_RULES = {
    "qualify": ("meddpicc_qualifier", "Deal Qualification Authority"),
    "meddpicc": ("meddpicc_qualifier", "Deal Qualification Authority"),
    "score": ("meddpicc_qualifier", "Deal Qualification Authority"),
    "negotiate": ("negotiation", "Master Negotiator"),
    "deal": ("negotiation", "Master Negotiator"),
    "price": ("negotiation", "Master Negotiator"),
    "prospect": ("prospecting_sdr", "Elite Prospector"),
    "lead": ("prospecting_sdr", "Elite Prospector"),
    "psychology": ("buyer_psychology", "Buyer Behavior Expert"),
    "buyer": ("buyer_psychology", "Buyer Behavior Expert"),
    "value": ("value_engineer", "Value Architect"),
    "roi": ("value_engineer", "Value Architect"),
    "strategy": ("revenue_orchestrator", "Revenue Orchestra Conductor"),
    "pipeline": ("revenue_orchestrator", "Revenue Orchestra Conductor"),
    "coach": ("call_coacher", "Sales Call Coach"),
    "call": ("call_coacher", "Sales Call Coach"),
}

DEFAULT_AGENT = ("revenue_orchestrator", "Revenue Orchestra Conductor")


def route_message(message: str):
    msg_lower = message.lower()
    for keyword, agent_info in ROUTING_RULES.items():
        if keyword in msg_lower:
            return agent_info
    return DEFAULT_AGENT


def list_agents():
    print("\\nAvailable Agents:")
    print("=" * 50)
    for pid in PERSONA_IDS:
        p = get_persona(pid)
        if p:
            print(f"  {p['title']:<45s} ({p['expert_count']} experts)")
    print()
    print("Keywords: qualify, meddpicc, negotiate, deal, prospect, lead, buyer, value, roi, strategy, pipeline, coach, call")


def run_query(query: str):
    persona_id, persona_name = route_message(query)
    print(f"\\n🔍 Routed to: {persona_name}")
    print(f"{'=' * 50}")

    if not HAS_DEPENDENCIES:
        print(f"Agent dependencies not available. Would execute using {persona_id}.")
        return

    # Check for training-specific keywords
    training = ""
    for key in ["meddpicc", "spinning"]:
        if key in query.lower() and key in TRAINING_MODULES:
            training = TRAINING_MODULES[key]
            break

    agent = AgentIntelligence(persona_id, persona_name)
    
    # If no real LLM available, show what would be sent
    if not os.getenv("OPENROUTER_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        prompt = agent.build_prompt(f"User query: {query}")
        print(f"\\n📝 System Prompt ({len(prompt)} chars):")
        print("-" * 50)
        print(prompt[:500])
        print("..." if len(prompt) > 500 else "")
        print(f"\\n⚠️  No LLM API key set. Set OPENROUTER_API_KEY or ANTHROPIC_API_KEY for real execution.")
        print(f"   Demo mode: showing what the agent would receive.")
        return

    # Execute with real LLM
    result = agent.execute(
        task="Analyze the following sales query and provide expert analysis",
        data={"query": query},
        training=training,
        temperature=0.3,
    )

    print(f"\\n📊 Analysis:")
    print("-" * 50)
    if result.get("success"):
        print(result.get("text", "")[:1000])
        if result.get("parsed"):
            print(f"\\n📋 Structured Output:")
            import json
            print(json.dumps(result["parsed"], indent=2)[:500])
    else:
        print(f"  Error: Could not generate analysis.")
        print(f"  Tip: Check LLM API key is set correctly.")


def interactive_mode():
    print("=" * 60)
    print("  REVENUE OS — Agent Demo")
    print("  Type 'agents' to list, 'quit' to exit")
    print("=" * 60)
    list_agents()

    while True:
        try:
            query = input("\\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if query.lower() in ("agents", "list", "help"):
            list_agents()
            continue

        run_query(query)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_query(" ".join(sys.argv[1:]))
    else:
        interactive_mode()
