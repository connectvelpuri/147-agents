
"""Agent Intelligence Wrapper — wires personas to LLM execution."""

import os
from agent_base.personas import get_system_prompt
from agent_base.llm_client import LLMClient

DEFAULT_LLM_CONFIG = {
    "provider": os.getenv("LLM_PROVIDER", "openrouter"),
    "tier": os.getenv("LLM_TIER", "complex"),
}

class AgentIntelligence:
    def __init__(self, persona_id, agent_name="", llm_config=None):
        self.persona_id = persona_id
        self.agent_name = agent_name or persona_id.replace("_", " ").title()
        llm_config = llm_config or DEFAULT_LLM_CONFIG
        self.llm = LLMClient(provider=llm_config.get("provider", "openrouter"),
                             tier=llm_config.get("tier", "auto"))

    def build_prompt(self, context=""):
        return get_system_prompt(self.persona_id, self.agent_name, context)

    def add_training(self, training_text):
        base = self.build_prompt()
        return base + "\n\nTRAINING:\n" + training_text

    def execute(self, task, data=None, training="", temperature=0.3):
        system_prompt = self.add_training(training) if training else self.build_prompt()
        user_prompt = "TASK: " + task + "\n\n"
        if data:
            user_prompt += "INPUT DATA:\n"
            for k, v in data.items():
                user_prompt += "  " + k + ": " + str(v) + "\n"
        user_prompt += "\nApply your expert framework and produce your analysis."
        result = self.llm.complete(system_prompt=system_prompt, user_prompt=user_prompt, temperature=temperature)
        out = {"success": result.success, "text": result.text}
        if result.success:
            parsed = self.llm.format_json(result.text)
            if parsed:
                out["parsed"] = parsed
        return out

TRAINING_MODULES = {
    "meddpicc": "MEDDPICC: M-Metrics, E-Economic Buyer, D-Decision Criteria, D-Decision Process, P-Pain, I-Champion, C-Competition, C-Competition. Score 0-5 each. >25=good, 15-25=gaps, <15=disqualify",
    "spinning": "SPIN: Situation, Problem, Implication, Need-Payoff. For every 3 questions, 1 statement. Top reps ask 57% more questions.",
    "challenger": "Challenger: TEACH new insight, TAILOR to their situation, TAKE CONTROL with constructive tension. Challenger reps outperform 2x.",
    "gap_selling": "Gap Selling: Current State -> Future State -> The Gap (cost of inaction) -> The Bridge (your solution). No product mention until gap sized.",
    "cialdini": "Cialdini: Reciprocity, Scarcity, Authority, Consistency, Liking, Social Proof. Use ethically to identify patterns, not manipulate.",
}
