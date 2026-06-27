"""
NG-001 BATNA Analyst — CLI entry point.

Usage:
  python run_agent.py profile --deal_id <id> --value 100000 [--competitive true] [--stakeholders 3]
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.negotiator import BATNAAnalyst


def cmd_profile(args: argparse.Namespace):
    analyst = BATNAAnalyst()
    data = {
        "deal_value": float(args.value or 0),
        "competitive": args.competitive == "true",
        "competitor": args.competitor or "",
        "stakeholder_count": int(args.stakeholders or 0),
        "timeline_days": int(args.timeline or 90),
        "urgency": args.urgency or "medium",
        "notes": args.notes or "",
    }

    profile = asyncio.run(analyst._build_profile(args.deal_id, data))

    if not profile:
        print("Profile generation failed")
        return

    print(f"=== NG-001 NEGOTIATION POWER PROFILE ===")
    print(f"Deal: {args.deal_id} | Value: ${float(args.value or 0):,.0f}")
    print()

    print("BATNA (Fisher & Ury):")
    print(f"  Description: {profile.batna.description}")
    print(f"  Walkaway: ${profile.batna.walkaway_value:,.0f}")
    print(f"  Confidence: {profile.batna.confidence:.0%}")
    if profile.batna.alternative_details:
        print(f"  Alternatives: {', '.join(profile.batna.alternative_details)}")
    print()

    print("THEIR BATNA:")
    print(f"  Description: {profile.their_batna.description}")
    print(f"  Est. Walkaway: ${profile.their_batna.estimated_walkaway_value:,.0f}")
    print(f"  Confidence: {profile.their_batna.confidence:.0%}")
    if profile.their_batna.weakness_signals:
        print(f"  Weakness Signals: {', '.join(profile.their_batna.weakness_signals)}")
    print()

    print("ZOPA (Zone of Possible Agreement):")
    print(f"  Overlap: {'YES' if profile.zopa.overlap_exists else 'NO'}")
    if profile.zopa.overlap_exists:
        print(f"  Range: ${profile.zopa.overlap_range[0]:,.0f} - ${profile.zopa.overlap_range[1]:,.0f}")
        print(f"  Midpoint: ${profile.zopa.midpoint:,.0f}")
    else:
        print(f"  Our minimum (${profile.zopa.our_minimum:,.0f}) exceeds their estimated maximum (${profile.zopa.their_maximum:,.0f})")
    print()

    print("LEVERAGE FACTORS:")
    for f in profile.leverage:
        icon = "[+]" if f.direction.value == "toward_us" else "[-]" if f.direction.value == "toward_them" else "[~]"
        print(f"  {icon} {f.name} (w={f.weight:.1f}): {f.description}")
    print()

    if profile.power_timeline:
        pt = profile.power_timeline
        print(f"POWER TIMELINE: {pt.current_leverage}")
        print(f"  Trend: {pt.trend.value}")
        print(f"  Recommendation: {pt.recommendation}")
        print()

    print("OVERALL ASSESSMENT:")
    print(f"  {profile.overall_assessment}")
    print()
    print("WALKAWAY GUIDANCE:")
    print(f"  {profile.walkaway_guidance}")


def main():
    parser = argparse.ArgumentParser(description="NG-001 BATNA Analyst")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("profile")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--competitive", default="false")
    p.add_argument("--competitor")
    p.add_argument("--stakeholders", default="0")
    p.add_argument("--timeline", default="90")
    p.add_argument("--urgency", default="medium")
    p.add_argument("--notes")

    args = parser.parse_args()
    if args.command == "profile":
        cmd_profile(args)


if __name__ == "__main__":
    main()
