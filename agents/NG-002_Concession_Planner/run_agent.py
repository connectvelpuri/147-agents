from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.planner import ConcessionPlanner


def cmd_plan(args: argparse.Namespace):
    p = ConcessionPlanner()
    data = {
        "deal_value": float(args.value or 0),
        "buyer_type": args.buyer_type or "Enterprise",
        "stage": args.stage or "Discovery",
        "known_demands": args.demands or "None yet",
        "margin_available": args.margin or "Unknown",
        "urgency": args.urgency or "medium",
        "batna_strength": args.batna or "moderate",
        "notes": args.notes or "",
    }
    plan = asyncio.run(p.design_concession_sequence(args.deal_id, data))

    print(f"=== NG-002 CONCESSION PLAN ===")
    print(f"Deal: {plan.deal_id}")
    print(f"Max Concession Depth: {plan.max_concession_depth_pct:.0f}%")
    print()
    print("CONCESSION SEQUENCE:")
    for c in plan.sequence:
        print(f"  [{c.type.value.upper():>8}] {c.description}")
        print(f"        Cost: ${c.actual_cost:,.0f} | Perceived: ${c.perceived_value:,.0f}")
        print(f"        Trigger: {c.trigger_condition}")
        print(f"        Frame: \"{c.framing_language}\"")
        print()
    print("WALK-AWAY TRIGGERS:")
    for t in plan.walk_away_triggers:
        print(f"  - {t}")
    print()
    print("PACING GUIDANCE:")
    print(f"  {plan.pacing_guidance}")


def main():
    parser = argparse.ArgumentParser(description="NG-002 Concession Planner")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--buyer_type")
    p.add_argument("--stage")
    p.add_argument("--demands")
    p.add_argument("--margin")
    p.add_argument("--urgency")
    p.add_argument("--batna")
    p.add_argument("--notes")
    args = parser.parse_args()
    if args.command == "plan":
        cmd_plan(args)


if __name__ == "__main__":
    main()
