#!/usr/bin/env python3
"""CLI entry point for SDR-001 Multi-Channel Prospector.

Usage:
    python run_agent.py                        # Run agent loop
    python run_agent.py --scan                 # Run one discovery cycle
    python run_agent.py --queue                # Show priority queue
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope, new_event_id
from agent.prospector import MultiChannelProspector


def main():
    parser = argparse.ArgumentParser(description="SDR-001 Multi-Channel Prospector")
    parser.add_argument("--scan", action="store_true", help="Run one discovery cycle")
    parser.add_argument("--queue", action="store_true", help="Show current priority queue")

    args = parser.parse_args()
    agent = MultiChannelProspector()

    async def run():
        await agent.nats.connect()
        if args.scan:
            await agent._run_discovery_cycle()
            print("[SDR-001] Scan complete")
        elif args.queue:
            await agent._run_discovery_cycle()
            summary = {
                "total": len(agent._discovered_accounts),
                "accounts": list(agent._discovered_accounts.keys()),
            }
            print(f"[SDR-001] Queue: {summary}")
        else:
            print("[SDR-001] No action specified. Use --scan or --queue")

    asyncio.run(run())


if __name__ == "__main__":
    main()
