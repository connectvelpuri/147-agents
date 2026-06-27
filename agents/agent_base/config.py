"""Configuration loader for RevenueOS agents.

Loads from YAML file with env var overrides.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_config(path: str | Path, agent_id: str | None = None) -> dict[str, Any]:
    """Load agent configuration from YAML file.

    Args:
        path: Path to config file (e.g., 'config.yaml' next to agent).
        agent_id: Optional — if provided, reads `agents.{agent_id}` section.

    Returns:
        Config dictionary with env var overrides applied.
    """
    path = Path(path)
    config: dict[str, Any] = {}

    if path.exists():
        try:
            import yaml
            with open(path) as f:
                raw = yaml.safe_load(f) or {}
            if agent_id:
                config = raw.get("agents", {}).get(agent_id, raw)
            else:
                config = raw
        except Exception as e:
            print(f"[CONFIG:WARN] Could not load {path}: {e}")

    # Env var overrides (NATS_SERVERS, LLM_PROVIDER, etc.)
    env_overrides = {
        "nats_servers": os.getenv("NATS_SERVERS"),
        "llm_provider": os.getenv("LLM_PROVIDER"),
        "llm_tier": os.getenv("LLM_TIER"),
        "log_level": os.getenv("LOG_LEVEL"),
    }
    for key, value in env_overrides.items():
        if value is not None:
            _set_nested(config, key, value)

    return config


def _set_nested(d: dict, key: str, value: Any):
    parts = key.split(".")
    for part in parts[:-1]:
        d = d.setdefault(part, {})
    d[parts[-1]] = value


def get_nats_servers(config: dict) -> list[str]:
    servers = config.get("nats", {}).get("servers", [])
    if not servers:
        env_str = os.getenv("NATS_SERVERS")
        if env_str:
            servers = [s.strip() for s in env_str.split(",")]
    return servers
