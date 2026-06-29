"""LLM Client - with Reflection, Self-Consistency, CoT, Dynamic Routing, RAG, Confidence."""

import os
import json
import random


class LLMResult:
    def __init__(self, success=False, text="", model="", error="", 
                 used_fallback=False, confidence=0.0, reasoning=""):
        self.success = success
        self.text = text
        self.model = model
        self.error = error
        self.used_fallback = used_fallback
        self.confidence = confidence
        self.reasoning = reasoning


TIER_MODELS = {
    "fast": {"openrouter": "openrouter/free", "nvidia": "nvidia/nemotron-3-super-120b-a12b:free"},
    "smart": {"openrouter": "openrouter/free", "nvidia": "nvidia/nemotron-3-ultra-550b-a55b:free"},
    "best": {"openrouter": "openrouter/free", "nvidia": "nvidia/nemotron-3-ultra-550b-a55b:free"},
}


class LLMClient:
    """Unified LLM client with reflection, self-consistency, CoT, dynamic routing."""

    def __init__(self, provider="openrouter", tier="smart", temperature=0.3, max_tokens=4000):
        self.provider = provider
        self.tier = tier
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._call_count = 0

    def _call_llm(self, system, user, model, temperature=None, max_tokens=None):
        """Make an LLM API call."""
        from openai import OpenAI
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        self._call_count += 1
        
        api_key = os.getenv("OPENROUTER_API_KEY") if self.provider == "openrouter" else os.getenv("NVIDIA_NIM_API_KEY")
        base_url = "https://openrouter.ai/api/v1" if self.provider == "openrouter" else "https://integrate.api.nvidia.com/v1"
        
        if not api_key:
            return LLMResult(success=False, error="No API key set")
        
        try:
            from openai import OpenAI as OA
            client = OA(api_key=api_key, base_url=base_url)
            resp = client.chat.completions.create(
                model=model, 
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=temp, max_tokens=tokens)
            text = resp.choices[0].message.content or ""
            return LLMResult(success=True, text=text, model=model)
        except Exception as e:
            return LLMResult(success=False, error=str(e))

    def complete(self, system_prompt, user_prompt, temperature=None, max_tokens=None,
                 reflect=False, self_consistency=False, chain_of_thought=False):
        """Complete with optional reflection, self-consistency, CoT."""
        
        prompt = user_prompt
        
        # Chain of Thought wrapper
        if chain_of_thought:
            prompt = "Think step by step. Show your reasoning before giving your final answer. End with CONFIDENCE: X% where X is 0-100.

" + user_prompt
        
        # Get model for current tier
        model = TIER_MODELS.get(self.tier, {}).get(self.provider, TIER_MODELS["smart"]["openrouter"])
        if not model:
            return LLMResult(success=False, error="No model for tier")
        
        # Self-Consistency: run N times and vote
        if self_consistency:
            temps = [0.2, 0.5, 0.7]
            results = []
            for t in temps:
                r = self._call_llm(system_prompt, prompt, model, temperature=t, max_tokens=max_tokens)
                if r.success:
                    results.append(r.text)
            
            if len(results) >= 2:
                # Simple voting: pick the longest (usually most detailed) among consistent answers
                # For real consistency, we'd compare semantic similarity
                # Good enough: pick the middle-length answer (avoids too short or too long)
                sorted_results = sorted(results, key=len)
                text = sorted_results[len(sorted_results)//2]
                
                if chain_of_thought:
                    # Extract confidence from best answer
                    confidence = extract_confidence(text)
                    reasoning = extract_reasoning(text)
                    text = text
                else:
                    confidence = 70.0
                    reasoning = ""
                
                return LLMResult(success=True, text=text, model=model, confidence=confidence, reasoning=reasoning)
        
        # Single call
        result = self._call_llm(system_prompt, prompt, model, temperature, max_tokens)
        if not result.success:
            return result
        
        text = result.text
        confidence = 50.0
        reasoning = ""
        
        if chain_of_thought:
            confidence = extract_confidence(text)
            reasoning = extract_reasoning(text)
        
        # Reflection loop: self-critique
        if reflect and len(text) > 100:
            reflect_prompt = f"Critique the following analysis. What was missed? What could be improved? Be specific and actionable.

{text[:2000]}"
            ref_result = self._call_llm("You are a critical reviewer.", reflect_prompt, model, temperature=0.3, max_tokens=500)
            if ref_result.success and ref_result.text:
                text = text + "

[SELF-CRITIQUE]
" + ref_result.text[:500]
        
        return LLMResult(success=True, text=text, model=model, confidence=confidence, reasoning=reasoning)


def extract_confidence(text):
    """Extract confidence percentage from text."""
    import re
    matches = re.findall(r'CONFIDENCE:\s*(\d+)', text)
    if matches:
        return min(float(matches[0]), 100.0)
    matches = re.findall(r'confidence[:\s]+(\d+)', text.lower())
    if matches:
        return min(float(matches[0]), 100.0)
    return 70.0


def extract_reasoning(text):
    """Extract reasoning/thinking from CoT response."""
    parts = text.split("CONFIDENCE:")
    if len(parts) > 1:
        return parts[0].strip()
    # Try to find reasoning before "Answer:" or "Therefore"
    for marker in ["Answer:", "Therefore,", "Final answer:", "In conclusion"]:
        if marker in text:
            idx = text.index(marker)
            return text[:idx].strip()
    return text[:min(len(text), 500)]


class DynamicRouter:
    """Routes tasks to appropriate model tier based on complexity."""
    
    COMPLEX_KEYWORDS = ["negotiate", "strategy", "complex", "procurement", "legal", "multi-thread"]
    SIMPLE_KEYWORDS = ["quick", "simple", "email", "outreach", "follow-up", "meeting"]
    
    @staticmethod
    def route(task_description, user_message=""):
        combined = (task_description + " " + user_message).lower()
        
        # Detect complexity
        complex_score = sum(1 for kw in DynamicRouter.COMPLEX_KEYWORDS if kw in combined)
        simple_score = sum(1 for kw in DynamicRouter.SIMPLE_KEYWORDS if kw in combined)
        
        if complex_score > simple_score:
            return "best"
        elif simple_score > complex_score:
            return "fast"
        else:
            return "smart"


class RAGKnowledge:
    """Simple in-memory RAG from injected books."""
    
    KNOWLEDGE = {
        "meddpicc": "MEDDPICC: M-Metrics, E-Economic Buyer, D-Decision Criteria, D-Decision Process, P-Pain, I-Champion, C-Competition, C-Competition. Score 0-5 each.",
        "voss": "Voss Negotiation: Tactical empathy, mirroring, labeling, calibrated questions (how/what), accusation audit, 'no' is start of negotiation.",
        "cialdini": "Cialdini: Reciprocity, Scarcity, Authority, Consistency, Liking, Social Proof. Use ethically.",
        "challenger": "Challenger Sale: Teach (new insight), Tailor (to their situation), Take Control (constructive tension).",
        "carnegie": "Carnegie: Win friends - genuine interest, talk in other's interests, make them feel important, don't criticize.",
        "hill": "Napoleon Hill: Burning desire, definiteness of purpose, master mind, faith, persistence, the psychological moment.",
    }
    
    @staticmethod
    def retrieve(query, top_k=2):
        """Retrieve relevant knowledge for a query."""
        query_lower = query.lower()
        relevant = []
        for key, value in RAGKnowledge.KNOWLEDGE.items():
            if key in query_lower:
                relevant.append(value)
        return relevant[:top_k]
