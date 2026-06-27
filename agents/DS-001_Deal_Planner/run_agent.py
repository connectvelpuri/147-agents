from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.planner import DealPlanner


def cmd_plan(args: argparse.Namespace):
    planner = DealPlanner()
    data = {
        "deal_id": args.deal_id,
        "deal_value": float(args.value or 0),
        "buyer_name": args.buyer or "Unknown",
        "industry": args.industry or "Unknown",
        "current_stage": args.stage or "Discovery",
        "competitive_landscape": args.competition or "Unknown",
        "timeline": args.timeline or "No timeline provided",
        "notes": args.notes or "",
    }
    plan = asyncio.run(planner.create_comprehensive_deal_plan(args.deal_id, data))

    print(f"=== DS-001 DEAL PLAN ===")
    print(f"Deal: {plan.deal_id} | Version: {plan.version}")
    print(f"Score: ${plan.situation.deal_value:,.0f}")
    print()
    print("SITUATION:")
    print(f"  {plan.situation.summary}")
    print(f"  Blockers: {', '.join(plan.situation.blockers) if plan.situation.blockers else 'None identified'}")
    print()
    print("MILESTONES:")
    for m in plan.milestones:
        print(f"  [{m.status.value.upper():>11}] {m.title} — due {m.due_date}")
        print(f"        {m.description}")
        print(f"        Criteria: {m.completion_criteria}")
        print()
    print("STAKEHOLDER ENGAGEMENT PLAN:")
    for s in plan.stakeholder_plan:
        print(f"  [{s.influence.value.upper():>6}] {s.stakeholder_name} ({s.title})")
        print(f"        Goal: {s.engagement_goal}")
        print(f"        Action: {s.proposed_action} | Cadence: {s.cadence}")
        print()
    print("RISK REGISTER:")
    for r in plan.risk_register:
        print(f"  [{r.severity.value.upper():>8}] {r.risk} (p={r.probability:.0%})")
        print(f"        Mitigation: {r.mitigation}")
        print()
    print("COMPETITIVE POSITIONING:")
    print(f"  {plan.competitive_positioning}")
    print()
    print("CRITICAL PATH:")
    for cp in plan.critical_path:
        print(f"  - {cp}")
    print()
    print("RECOMMENDATIONS:")
    for rec in plan.recommendations:
        print(f"  - {rec}")


def cmd_situation(args: argparse.Namespace):
    planner = DealPlanner()
    data = {
        "deal_id": args.deal_id,
        "deal_value": float(args.value or 0),
        "buyer_name": args.buyer or "Unknown",
        "industry": args.industry or "Unknown",
        "current_stage": args.stage or "Discovery",
        "competitive_landscape": args.competition or "Unknown",
        "timeline": args.timeline or "No timeline provided",
        "notes": args.notes or "",
    }
    situation = asyncio.run(planner.assess_deal_situation(data))
    print(f"=== DS-001 DEAL SITUATION ASSESSMENT ===")
    print(f"Deal: {situation.deal_id}")
    print(f"Summary: {situation.summary}")
    print(f"Buyer Need: {situation.buyer_need}")
    print(f"Blocker Count: {len(situation.blockers)}")


def main():
    parser = argparse.ArgumentParser(description="DS-001 Deal Planner")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("plan")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--buyer")
    p.add_argument("--industry")
    p.add_argument("--stage")
    p.add_argument("--competition")
    p.add_argument("--timeline")
    p.add_argument("--notes")

    ps = sub.add_parser("situation")
    ps.add_argument("--deal_id", required=True)
    ps.add_argument("--value", default="0")
    ps.add_argument("--buyer")
    ps.add_argument("--industry")
    ps.add_argument("--stage")
    ps.add_argument("--competition")
    ps.add_argument("--timeline")
    ps.add_argument("--notes")

    args = parser.parse_args()
    if args.command == "plan":
        cmd_plan(args)
    elif args.command == "situation":
        cmd_situation(args)


if __name__ == "__main__":
    main()
