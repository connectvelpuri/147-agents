"""
DS-001 Deal Dashboard — CLI entry point.

Usage:
  python run_agent.py health --deal_id <id> [--sentiment positive|negative|neutral]
  python run_agent.py produce --deal_id <id> [--objections 2] [--blocking 1]
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent.dashboard import DealDashboard
from agent.models import DealHealthCard


def cmd_health(args: argparse.Namespace):
    dash = DealDashboard()
    card = DealHealthCard(deal_id=args.deal_id, overall_score=0.0)

    if args.sentiment:
        dash._apply_sentiment(card, {
            "overall_sentiment": args.sentiment,
            "timelines": [{"participant_id": "Buyer", "overall_sentiment": args.sentiment}],
        })
    if args.objections:
        dash._apply_objections(card, {
            "objection_count": int(args.objections),
            "blocking_count": int(args.blocking or 0),
            "addressed_count": int(args.addressed or 0),
        })
    if args.commitments:
        dash._apply_commitments(card, {
            "buyer_commitments": int(int(args.commitments) > 0),
            "seller_commitments": 1,
            "no_commitments": int(args.commitments) == 0,
        })

    dash._recalculate(card)

    print(f"=== DS-001 DEAL HEALTH CARD ===")
    print(f"Deal: {card.deal_id} | Score: {card.overall_score}/100")
    print(f"Forecast: {card.forecast_category.value}")
    print()
    for d in card.dimensions:
        label = DIMENSION_LABELS.get(d.name, d.name)
        print(f"  [{d.rating.value.upper():>6}] {label} ({d.score:.1f})")
        print(f"        {d.evidence}")
        print()
    print("MEDDIC:")
    m = card.meddic
    print(f"  EB Engaged: {m.economic_buyer_engaged}")
    print(f"  Decision Criteria Clear: {m.decision_criteria_clear}")
    print(f"  Decision Process Mapped: {m.decision_process_mapped}")
    print(f"  Champion Confirmed: {m.champion_confirmed}")
    print()
    if card.risk_factors:
        print("RISK FACTORS:")
        for r in card.risk_factors:
            print(f"  - {r}")
        print()
    print("RECOMMENDATIONS:")
    for r in card.recommendations:
        print(f"  - {r}")


DIMENSION_LABELS = {
    "economic_buyer": "Economic Buyer",
    "negative_consequences": "Negative Consequences",
    "pbo_clarity": "PBO Clarity",
    "required_capabilities": "Required Capabilities",
    "decision_process": "Decision Process",
    "stakeholder_consensus": "Stakeholder Consensus",
    "timeline_urgency": "Timeline Urgency",
    "competitive_position": "Competitive Position",
}


def main():
    parser = argparse.ArgumentParser(description="DS-001 Deal Dashboard")
    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser("health")
    p_health.add_argument("--deal_id", required=True)
    p_health.add_argument("--sentiment", default="neutral")
    p_health.add_argument("--objections")
    p_health.add_argument("--blocking")
    p_health.add_argument("--addressed")
    p_health.add_argument("--commitments")

    args = parser.parse_args()
    if args.command == "health":
        cmd_health(args)


if __name__ == "__main__":
    main()
