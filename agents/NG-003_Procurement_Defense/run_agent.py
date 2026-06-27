from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.defense import ProcurementDefense


def cmd_classify(args: argparse.Namespace):
    d = ProcurementDefense()
    data = {
        "communication": args.communication or "Not specified",
        "buyer_action": args.action or "Not specified",
        "context": args.context or "Not specified",
        "stage": args.stage or "Unknown",
        "previous_tactics": args.previous or "None",
    }
    alert = asyncio.run(d.classify_tactic(data))
    strategy = d._lookup_counter(alert)

    print(f"=== NG-003 PROCUREMENT DEFENSE ===")
    print(f"Tactic: {alert.tactic.value.upper()} (confidence: {alert.confidence:.0%})")
    print(f"Severity: {alert.severity.value}")
    print(f"Evidence: {alert.evidence}")
    print()
    print("IMMEDIATE RESPONSE:")
    print(f"  {strategy.immediate_response}")
    print()
    print("FALLBACK POSITION:")
    print(f"  {strategy.fallback_position}")
    print()
    print("ESCALATION TRIGGER:")
    print(f"  {strategy.escalation_trigger}")


def cmd_list(args: argparse.Namespace):
    d = ProcurementDefense()
    print(f"=== NG-003 TACTIC LIBRARY ({len(d._counter_library)} tactics) ===")
    for key, cs in d._counter_library.items():
        print(f"\n  [{key.upper()}]")
        print(f"    {cs['alert']}")
        print(f"    Response: {cs['immediate_response'][:80]}...")


def main():
    parser = argparse.ArgumentParser(description="NG-003 Procurement Defense")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("classify")
    p.add_argument("--communication")
    p.add_argument("--action")
    p.add_argument("--context")
    p.add_argument("--stage")
    p.add_argument("--previous")

    sub.add_parser("list")

    args = parser.parse_args()
    if args.command == "classify":
        cmd_classify(args)
    elif args.command == "list":
        cmd_list(args)


if __name__ == "__main__":
    main()
