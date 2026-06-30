import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
from agent_base.personas import PERSONA_IDS, get_persona
print(f"Personas: {len(PERSONA_IDS)}")
p = get_persona("account_intelligence")
print(f"Title: {p['title']}")
print(f"Experts: {p['expert_count']}")
print(f"First expert: {p['experts'][0][0]}")
print("OK - Account Intelligence persona loaded!")
