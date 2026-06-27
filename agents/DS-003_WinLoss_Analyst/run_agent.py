"""
DS-003 Win/Loss Analyst — CLI entry point.

Usage:
  python run_agent.py analyze --deal_id <id> --outcome lost --value 50000 --cycle_days 90
  python run_agent.py stats
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.analyst import WinLossAnalyst
from agent.models import LossReason, WinReason


def cmd_analyze(args: argparse.Namespace):
    analyst = WinLossAnalyst()
    outcome = args.outcome

    data = {
        "deal_value": float(args.value or 0),
        "sales_cycle_days": int(args.cycle_days or 0),
        "stages_passed": [s.strip() for s in (args.stages or "").split(",") if s.strip()],
        "stakeholder_count": int(args.stakeholders or 0),
        "competitive": args.competitive == "true",
        "notes": args.notes or "",
    }

    if outcome == "lost":
        result = asyncio.run(analyst._analyze_loss(args.deal_id, data))
    else:
        data["win_reason"] = args.win_reason or "other"
        result = asyncio.run(analyst._analyze_win(args.deal_id, data))

    if not result:
        print("Analysis failed")
        return

    r = result.record
    print(f"=== DS-003 WIN/LOSS ANALYSIS ===")
    print(f"Deal: {r.deal_id} | Outcome: {r.outcome}")
    if r.value:
        print(f"Value: ${r.value:,.0f} | Cycle: {r.sales_cycle_days}d | Stakeholders: {r.stakeholder_count}")
    print()

    if r.loss_details:
        d = r.loss_details
        print(f"Primary Reason: {d.primary.value.upper()}")
        print(f"Description: {d.description}")
        print(f"Evidence: {d.evidence}")
        print(f"Preventability: {d.preventability:.0%}")
        if d.contributing:
            print(f"Contributing: {', '.join(c.value for c in d.contributing)}")
        print()

    if result.recommendations:
        print("RECOMMENDATIONS:")
        for rec in result.recommendations:
            print(f"  - {rec}")
        print()

    if result.patterns:
        print("DETECTED PATTERNS:")
        for p in result.patterns:
            print(f"  [{p.pattern_type.value}] {p.description} (x{p.frequency})")
            print(f"     {p.recommendation}")
        print()

    print(f"Data Completeness: {result.data_completeness:.0%}")


def cmd_stats(args: argparse.Namespace):
    analyst = WinLossAnalyst()
    stats = asyncio.run(analyst.get_aggregate_stats())
    print(f"=== DS-003 AGGREGATE STATS ===")
    print(f"Total Analyzed: {stats['total_analyzed']}")
    print(f"Wins: {stats['total_wins']} | Losses: {stats['total_losses']}")
    if stats['total_analyzed']:
        print(f"Win Rate: {stats['win_rate']:.1f}%")
        print(f"Avg Preventability: {stats['avg_preventability']:.0%}")
        print()
        print("Loss Reason Distribution:")
        for reason, count in stats['loss_reason_distribution'].items():
            bar = "█" * count
            print(f"  {reason:20s}: {bar} ({count})")


def main():
    parser = argparse.ArgumentParser(description="DS-003 Win/Loss Analyst")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze")
    p_analyze.add_argument("--deal_id", required=True)
    p_analyze.add_argument("--outcome", choices=["lost", "won"], default="lost")
    p_analyze.add_argument("--value")
    p_analyze.add_argument("--cycle_days")
    p_analyze.add_argument("--stages")
    p_analyze.add_argument("--stakeholders")
    p_analyze.add_argument("--competitive", default="false")
    p_analyze.add_argument("--notes")
    p_analyze.add_argument("--win_reason")

    p_stats = sub.add_parser("stats")

    args = parser.parse_args()
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "stats":
        cmd_stats(args)


if __name__ == "__main__":
    main()
