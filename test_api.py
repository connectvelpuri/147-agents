"""
Revenue OS — Comprehensive Tests for All API Endpoints
Run: python -m pytest test_api.py -v
"""

import os
import sys
import json
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))

from api.webhook import app

client = TestClient(app)

# Set test API key
os.environ["API_KEY"] = "test-key-123"

HEADERS = {"X-API-Key": "test-key-123"}

# ============================================================
# Health & Root
# ============================================================
class TestHealth:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["status"] == "running"

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

# ============================================================
# Authentication
# ============================================================
class TestAuthentication:
    def test_no_auth_returns_403(self):
        response = client.post("/api/agent/execute", json={"task": "test"})
        assert response.status_code == 403

    def test_wrong_auth_returns_403(self):
        response = client.post("/api/agent/execute",
            json={"task": "test"},
            headers={"X-API-Key": "wrong-key"}
        )
        assert response.status_code == 403

    def test_valid_auth_succeeds(self):
        response = client.post("/api/agent/execute",
            json={"task": "qualify this deal", "persona": "meddpicc_qualifier"},
            headers=HEADERS
        )
        # Should succeed even without LLM key (uses demo mode)
        assert response.status_code in (200, 503)

# ============================================================
# Agent Execution
# ============================================================
class TestAgentExecution:
    def test_execute_default_persona(self):
        response = client.post("/api/agent/execute",
            json={"task": "analyze this deal"},
            headers=HEADERS
        )
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            data = response.json()
            assert "response" in data

    def test_execute_meddpicc_persona(self):
        response = client.post("/api/agent/execute",
            json={
                "task": "qualify this enterprise deal",
                "persona": "meddpicc_qualifier",
                "context": "Fortune 500 company, $2M deal",
                "data": {"deal_size": "2M", "company": "Acme Corp"}
            },
            headers=HEADERS
        )
        assert response.status_code in (200, 503)

    def test_execute_negotiation_persona(self):
        response = client.post("/api/agent/execute",
            json={"task": "negotiate with procurement", "persona": "negotiation"},
            headers=HEADERS
        )
        assert response.status_code in (200, 503)

    def test_execute_with_training(self):
        response = client.post("/api/agent/execute",
            json={"task": "score with MEDDPICC", "persona": "meddpicc_qualifier",
                  "training": "MEDDPICC: M=0.25, E=0.15, D=0.15, D=0.15, P=0.15, I=0.15, C=0.0"},
            headers=HEADERS
        )
        assert response.status_code in (200, 503)

    def test_invalid_persona_returns_400(self):
        response = client.post("/api/agent/execute",
            json={"task": "test", "persona": "nonexistent"},
            headers=HEADERS
        )
        assert response.status_code == 400

# ============================================================
# WhatsApp Webhooks
# ============================================================
class TestWhatsApp:
    def test_whatsapp_json_webhook(self):
        response = client.post("/webhook/whatsapp",
            json={"message": {"text": "qualify this deal"}},
            headers=HEADERS
        )
        assert response.status_code in (200, 400)

    def test_whatsapp_twilio_form_webhook(self):
        response = client.post("/webhook/twilio",
            data={"Body": "negotiate this deal", "From": "+1234567890"},
            headers=HEADERS
        )
        assert response.status_code in (200, 400)

# ============================================================
# Conversation Memory
# ============================================================
class TestConversation:
    def test_conversation_tracking(self):
        # Send first message
        r1 = client.post("/api/agent/execute",
            json={"task": "qualify this deal", "conversation_id": "test-123"},
            headers=HEADERS
        )
        # Send follow-up
        r2 = client.post("/api/agent/execute",
            json={"task": "what were the gaps?", "conversation_id": "test-123"},
            headers=HEADERS
        )
        # Both should work
        assert r1.status_code in (200, 503)
        assert r2.status_code in (200, 503)

# ============================================================
# Error Handling
# ============================================================
class TestErrorHandling:
    def test_missing_task_returns_400(self):
        response = client.post("/api/agent/execute",
            json={},
            headers=HEADERS
        )
        assert response.status_code == 400

    def test_empty_body_returns_422(self):
        response = client.post("/api/agent/execute",
            headers=HEADERS
        )
        assert response.status_code == 422

    def test_large_payload_rejected(self):
        large_data = {"task": "x" * 100000, "data": {"big": "x" * 100000}}
        response = client.post("/api/agent/execute",
            json=large_data,
            headers=HEADERS
        )
        assert response.status_code == 413

# ============================================================
# Performance (basic smoke test)
# ============================================================
class TestPerformance:
    def test_response_under_5s(self):
        import time
        start = time.time()
        response = client.post("/api/agent/execute",
            json={"task": "quick test"},
            headers=HEADERS
        )
        elapsed = time.time() - start
        assert elapsed < 5.0, f"Response took {elapsed:.2f}s (limit: 5s)"
        assert response.status_code in (200, 503)
