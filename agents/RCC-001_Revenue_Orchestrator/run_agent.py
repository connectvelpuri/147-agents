#!/usr/bin/env python3
"""CLI entry point for RCC-001 Revenue Orchestrator.

Usage:
    python run_agent.py                          # Run agent loop
    python run_agent.py --simulate "DealCreated" # Simulate an event
    python run_agent.py --status                 # Show state summary
    python run_agent.py --list-dags              # List registered DAGs
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope
from agent_base.config import load_config, get_nats_servers
from agent.orchestrator import RevenueOrchestrator


def main():
    parser = argparse.ArgumentParser(description="RCC-001 Revenue Orchestrator")
    parser.add_argument("--simulate", type=str, choices=["DealCreated", "MeetingCompleted", "ContractSent", "DealClosedLost"],
                        help="Simulate an event")
    parser.add_argument("--deal-id", type=str, default="d_sim_001", help="Deal ID for simulation")
    parser.add_argument("--status", action="store_true", help="Show agent status summary")
    parser.add_argument("--list-dags", action="store_true", help="List registered workflow DAGs")
    parser.add_argument("--dev", action="store_true", default=True, help="Run in dev mode (no NATS)")

    args = parser.parse_args()
    config = load_config(Path(__file__).parent / "config.yaml", "rcc-001")
    nats_servers = [] if args.dev else get_nats_servers(config)

    orchestrator = RevenueOrchestrator(nats_servers=nats_servers)

    async def run():
        await orchestrator.nats.connect()

        if args.list_dags:
            from agent.models import WORKFLOW_DAGS
            print("=== REGISTERED WORKFLOW DAGS ===")
            for dag_id, dag in WORKFLOW_DAGS.items():
                steps = " -> ".join(f"{s.agent_id}" for s in dag.steps)
                gates = f" [gates: {', '.join(dag.human_gate_at)}]" if dag.human_gate_at else ""
                print(f"  {dag_id:25s} | {dag.trigger_event_type:25s} | {steps}{gates}")
            return

        if args.status:
            summary = orchestrator.state.get_summary()
            print("=== ORCHESTRATOR STATUS ===")
            print(f"  Active chains: {summary['active_chains']}")
            print(f"  History: {summary['chain_history']}")
            for aid, info in summary['agents'].items():
                circuit = " ⚠️ CIRCUIT OPEN" if info["circuit_open"] else ""
                print(f"  Agent {aid}: {info['status']}{circuit}")
            return

        if args.simulate:
            envelope = EventEnvelope(
                event_type=args.simulate,
                source_agent="cli",
                deal_id=args.deal_id,
                data={"source": "cli_simulation"},
            )
            await orchestrator.handle_event(envelope)
            return

        # Run agent loop
        await orchestrator.run()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[RCC-001] Shutdown by user")


if __name__ == "__main__":
    main()
