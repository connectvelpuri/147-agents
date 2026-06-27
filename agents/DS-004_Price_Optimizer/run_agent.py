from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.optimizer import PriceOptimizer


def cmd_price(args: argparse.Namespace):
    o = PriceOptimizer()
    data = {
        "deal_value": float(args.value or 0),
        "segment": args.segment or "Enterprise",
        "industry": args.industry or "Unknown",
        "competitive_context": args.competition or "Unknown",
        "buyer_budget": args.budget or "Unknown",
        "historical_win_rate": args.win_rate or "Unknown",
        "notes": args.notes or "",
    }
    profile = asyncio.run(o.analyze_price_sensitivity(args.deal_id, data))
    rec = asyncio.run(o.recommend_optimal_price(profile, data))

    print(f"=== DS-004 PRICE OPTIMIZATION ===")
    print(f"Deal: {args.deal_id} | Segment: {profile.segment}")
    print(f"Sensitivity: {profile.sensitivity.value}")
    print()
    print(f"Recommended: ${rec.recommended_price:,.0f}")
    print(f"  Floor: ${rec.floor_price:,.0f} | Ceiling: ${rec.ceiling_price:,.0f}")
    print(f"  Expected Win Rate: {rec.expected_win_rate:.0%}")
    print(f"  Margin Impact: {rec.margin_impact:.0%}")
    print()
    print("RATIONALE:")
    print(f"  {rec.rationale}")
    print()
    print("KEY FACTORS:")
    for f in profile.key_factors:
        print(f"  - {f}")


def cmd_discount(args: argparse.Namespace):
    o = PriceOptimizer()
    data = {
        "deal_value": float(args.value or 0),
        "discount_pct": float(args.discount or 0),
        "margin_pct": float(args.margin or 70),
        "competitive_pressure": args.pressure or "none",
    }
    impact = asyncio.run(o.calculate_discount_impact(data))

    print(f"=== DS-004 DISCOUNT IMPACT ===")
    print(f"Requested Discount: {impact.requested_discount_pct:.0f}%")
    print(f"Revenue Impact: ${impact.revenue_impact:,.0f}")
    print(f"Margin Compression: {impact.margin_impact_pct:.0%}")
    print(f"Break-even Units: {impact.break_even_units}")
    print()
    print("ALTERNATIVES:")
    for a in impact.alternative_suggestions:
        print(f"  - {a}")


def main():
    parser = argparse.ArgumentParser(description="DS-004 Price Optimizer")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("recommend")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--segment")
    p.add_argument("--industry")
    p.add_argument("--competition")
    p.add_argument("--budget")
    p.add_argument("--win_rate")
    p.add_argument("--notes")

    pd = sub.add_parser("discount")
    pd.add_argument("--deal_id", required=True)
    pd.add_argument("--value", default="0")
    pd.add_argument("--discount", default="0")
    pd.add_argument("--margin", default="70")
    pd.add_argument("--pressure")

    args = parser.parse_args()
    if args.command == "recommend":
        cmd_price(args)
    elif args.command == "discount":
        cmd_discount(args)


if __name__ == "__main__":
    main()
