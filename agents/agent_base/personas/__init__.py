"""
World-Class Persona Library — Revenue OS Intelligence Layer.
Each persona combines 10 world-class domain experts.
"""

PERSONA_IDS = ['revenue_orchestrator', 'buyer_psychology', 'value_engineer', 'negotiation', 'prospecting_sdr', 'meddpicc_qualifier', 'call_coacher']

def get_persona(persona_id):
    """Get a persona definition by ID."""
    from importlib import import_module
    try:
        mod = import_module("agent_base.personas." + persona_id)
        return mod.PERSONA
    except (ImportError, AttributeError):
        return None

def get_system_prompt(persona_id, agent_name="", context=""):
    """Get a complete system prompt for this persona."""
    from importlib import import_module
    try:
        mod = import_module("agent_base.personas." + persona_id)
        return mod.build_system_prompt(agent_name, context)
    except (ImportError, AttributeError):
        return ""