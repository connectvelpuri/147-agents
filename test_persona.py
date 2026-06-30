import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))
from agent_base.personas import PERSONA_IDS, get_persona

print(f"Personas loaded: {len(PERSONA_IDS)}")
p = get_persona("account_intelligence")
print(f"Title: {p['title']}")
print(f"Experts: {p['expert_count']}")
for e in p['experts']:
    print(f"  - {e[0]}: {e[1][:60]}")
print("\nAccount Intelligence persona loaded successfully!")
