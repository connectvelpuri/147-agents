#!/usr/bin/env python3
"""Start script for Railway deployment.
Reads PORT from environment and passes to uvicorn.
Railway sets PORT automatically.
"""
import os
import sys

# Ensure agents directory is on Python path
_agent_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")
if os.path.isdir(_agent_path):
    sys.path.insert(0, _agent_path)
_docker_path = "/app/agents"
if os.path.isdir(_docker_path) and _docker_path not in sys.path:
    sys.path.insert(0, _docker_path)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting Revenue OS on {host}:{port}")
    sys.stdout.flush()
    uvicorn.run(
        "api.webhook:app",
        host=host,
        port=port,
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
    )
