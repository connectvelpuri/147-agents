"""Tests for 147 Agents - all personas, routing, memory, LLM client."""
import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agents"))

os.environ["OPENROUTER_API_KEY"] = "test-key"

class TestPersonas:
    def test_all_personas_load(self):
        from agent_base.personas import PERSONA_IDS, get_persona
        assert len(PERSONA_IDS) == 7
        for pid in PERSONA_IDS:
            p = get_persona(pid)
            assert p is not None
            assert p["expert_count"] == 10

    def test_all_personas_build_prompt(self):
        from agent_base.personas import get_system_prompt, PERSONA_IDS
        for pid in PERSONA_IDS:
            sp = get_system_prompt(pid, "Test Agent", "test context")
            assert len(sp) > 100

class TestRouting:
    def test_intent_detection(self):
        from cli import detect_intent
        assert detect_intent("qualify this deal") is not None
        assert detect_intent("negotiate the price") is not None
        assert detect_intent("analyze buyer psychology") is not None
        assert detect_intent("random unrelated") is None

class TestMemory:
    def test_conversation_memory(self):
        from agents.memory import ConversationMemory
        mem = ConversationMemory()
        mem.add_message("user", "Hello")
        mem.add_message("assistant", "Hi there", persona="test")
        history = mem.get_history()
        assert len(history) >= 2
        assert history[-1]["role"] == "user"

    def test_response_cache(self):
        from agents.memory import ResponseCache
        ResponseCache.set("test query", "test", "cached response", "test-model")
        cached = ResponseCache.get("test query", "test")
        assert cached == "cached response"

class TestLLMClient:
    def test_tier_routing(self):
        from agent_base.llm_client import DynamicRouter
        assert DynamicRouter.route("negotiate complex deal") == "best"
        assert DynamicRouter.route("quick email follow-up") == "fast"

    def test_rag_knowledge(self):
        from agent_base.llm_client import RAGKnowledge
        results = RAGKnowledge.retrieve("meddpicc scoring")
        assert len(results) > 0

class TestCLI:
    def test_cli_imports(self):
        import cli
        assert hasattr(cli, "WebResearch")
        assert hasattr(cli, "CRMConnector")
        assert hasattr(cli, "PDFReport")
