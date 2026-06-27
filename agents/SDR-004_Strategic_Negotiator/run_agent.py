"""
SDR-004 Strategic Negotiator — CLI entry point.

Usage:
  python run_agent.py plan --name <name> --title <title> --company <company> [--value <val>] [--stage <stage>] [--obj <objections>]
  python run_agent.py objection --name <name> --obj <objection_text>
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent.negotiator import StrategicNegotiator
from agent.models import DealContext


def cmd_plan(args: argparse.Namespace):
    neg = StrategicNegotiator()
    ctx = DealContext(
        deal_id=args.deal_id or "d_new",
        prospect_name=args.name,
        prospect_title=args.title,
        company=args.company,
        deal_value=float(args.value or 0),
        current_stage=args.stage or "discovery",
        objections=[s.strip() for s in args.obj.split("|") if s.strip()] if args.obj else [],
        stakeholders=[s.strip() for s in args.stakeholders.split("|") if s.strip()] if args.stakeholders else [],
        timeline=args.timeline or "",
        competitor=args.competitor or "",
        notes=args.notes or "",
    )

    plan = asyncio.run(neg._build_plan(args.deal_id or "d_new", {
        "prospect_name": ctx.prospect_name,
        "prospect_title": ctx.prospect_title,
        "company": ctx.company,
        "deal_value": ctx.deal_value,
        "stage": ctx.current_stage,
        "objections": ctx.objections,
        "stakeholders": ctx.stakeholders,
        "timeline": ctx.timeline,
        "competitor": ctx.competitor,
        "notes": ctx.notes,
    }))

    print(f"=== SDR-004 NEGOTIATION PLAN ===")
    print(f"Deal: {plan.deal_id} | Prospect: {plan.context.prospect_name} ({plan.context.prospect_title} @ {plan.context.company})")
    print(f"Phase: {plan.phase.value} | Value: ${plan.context.deal_value:,.0f}")
    print(f"Approach: {plan.recommended_approach}")
    print()
    print("GIVE-GET PAIRS (Bob Burg):")
    for gg in plan.give_gets:
        print(f"  GIVE: {gg.give}")
        print(f"  GET:  {gg.get}")
        print(f"  WHY:  {gg.rationale}")
        print()
    print("VALUE=PROGRESS FRAMES (Jeff Shore):")
    for vf in plan.value_frames:
        print(f"  Metric: {vf.metric}")
        print(f"  Current: {vf.current_state}")
        print(f"  Desired: {vf.desired_state}")
        print(f"  Gap: {vf.progress_gap}")
        print(f"  Prop: {vf.value_proposition}")
        print()
    print("MIRROR ATTACKS (Oren Klaff):")
    for ma in plan.mirror_attacks:
        print(f"  Their Frame: {ma.their_frame}")
        print(f"  Mirror: {ma.mirrored_response}")
        print(f"  Reframe: {ma.reframe}")
        print(f"  Evidence: {ma.evidence}")
        print()
    print("CALIBRATED ABSENCES (Stuart Diamond):")
    for ca in plan.calibrated_absences:
        print(f"  Trigger: {ca.trigger}")
        print(f"  Silence: {ca.silence_duration_seconds}s")
        print(f"  Expected: {ca.expected_effect}")
        print(f"  Fallback: {ca.fallback}")
        print()
    print("FULL SCRIPT:")
    print(plan.script)


def cmd_objection(args: argparse.Namespace):
    neg = StrategicNegotiator()
    move = asyncio.run(neg._respond_to_objection("d_response", {
        "prospect_name": args.name,
        "company": args.company or "their company",
        "objection": args.obj,
    }))
    print(f"=== OBJECTION RESPONSE ===")
    print(f"Objection: {move['objection']}")
    print()
    print("MIRROR:")
    print(f"  {move['mirror_attack']['mirrored_response']}")
    print()
    print("REFRAME:")
    print(f"  {move['mirror_attack']['reframe']}")
    print()
    print("VALUE FRAME:")
    print(f"  Metric: {move['value_frame']['metric']}")
    print(f"  Gap: {move['value_frame']['gap']}")


def main():
    parser = argparse.ArgumentParser(description="SDR-004 Strategic Negotiator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("--deal_id", default="d_new")
    p_plan.add_argument("--name", required=True)
    p_plan.add_argument("--title", required=True)
    p_plan.add_argument("--company", required=True)
    p_plan.add_argument("--value", default="0")
    p_plan.add_argument("--stage", default="discovery")
    p_plan.add_argument("--obj", help="Pipe-separated objections: price|timeline|competitor")
    p_plan.add_argument("--stakeholders")
    p_plan.add_argument("--timeline")
    p_plan.add_argument("--competitor")
    p_plan.add_argument("--notes")

    p_obj = sub.add_parser("objection")
    p_obj.add_argument("--name", required=True)
    p_obj.add_argument("--company")
    p_obj.add_argument("--obj", required=True, help="The objection text")

    args = parser.parse_args()

    if args.command == "plan":
        cmd_plan(args)
    elif args.command == "objection":
        cmd_objection(args)


if __name__ == "__main__":
    main()
