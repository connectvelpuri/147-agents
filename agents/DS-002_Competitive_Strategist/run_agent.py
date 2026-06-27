from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.strategist import CompetitiveStrategist


def cmd_assess(args: argparse.Namespace):
    s = CompetitiveStrategist()
    data = {
        "deal_value": float(args.value or 0),
        "buyer_name": args.buyer or "Unknown",
        "industry": args.industry or "Unknown",
        "competitors": args.competitors or "Unknown",
        "our_strengths": args.strengths or "Not specified",
        "buyer_priorities": args.priorities or "Not specified",
        "notes": args.notes or "",
    }
    assessment = asyncio.run(s.analyze_competitive_landscape(args.deal_id, data))
    strategy = asyncio.run(s.develop_positioning_strategy(assessment, data))

    print(f"=== DS-002 COMPETITIVE POSITIONING ===")
    print(f"Deal: {args.deal_id} | Direction: {strategy.direction.value}")
    print()
    print("LANDSCAPE:")
    print(f"  {assessment.summary}")
    print()
    for c in assessment.competitors:
        print(f"  [{c.strength.value.upper():>7}] {c.name}")
        print(f"        Differentiators: {', '.join(c.differentiators[:3])}")
        print(f"        Vulnerabilities: {', '.join(c.vulnerabilities[:3])}")
        print()
    print("NARRATIVE:")
    print(f"  {strategy.primary_narrative}")
    print()
    print("KEY MESSAGES:")
    for m in strategy.key_messages:
        print(f"  - {m}")
    print()
    print("STRENGTH EXPLOITATION:")
    for s in strategy.strength_exploitation:
        print(f"  - {s}")
    print()
    print("WEAKNESS MITIGATION:")
    for w in strategy.weakness_mitigation:
        print(f"  - {w}")
    print()
    print("RISK POINTS:")
    for r in strategy.risk_points:
        print(f"  - {r}")


def main():
    parser = argparse.ArgumentParser(description="DS-002 Competitive Strategist")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("assess")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--buyer")
    p.add_argument("--industry")
    p.add_argument("--competitors")
    p.add_argument("--strengths")
    p.add_argument("--priorities")
    p.add_argument("--notes")
    args = parser.parse_args()
    if args.command == "assess":
        cmd_assess(args)


if __name__ == "__main__":
    main()
