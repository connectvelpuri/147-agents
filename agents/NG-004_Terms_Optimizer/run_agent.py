from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.optimizer import TermsOptimizer


def cmd_analyze(args: argparse.Namespace):
    o = TermsOptimizer()
    data = {
        "deal_value": float(args.value or 0),
        "contract_type": args.contract_type or "SaaS",
        "key_terms": args.terms or "Not provided",
        "buyer_changes": args.changes or "None",
        "payment_structure": args.payment or "Annual upfront",
        "industry": args.industry or "Technology",
        "legal_notes": args.legal_notes or "None",
    }
    report = asyncio.run(o.analyze_terms(args.deal_id, data))

    print(f"=== NG-004 TERMS OPTIMIZATION ===")
    print(f"Deal: {report.deal_id}")
    print()
    print("TERM ANALYSES:")
    for a in report.analyses:
        print(f"  [{a.impact.value.upper():>6}] [{a.category.value.upper():>12}] {a.clause}")
        print(f"        Risk: {a.risk}")
        print(f"        Recommendation: {a.recommendation}")
        print(f"        Market Standard: {a.market_standard}")
        print()

    if report.payment_optimization:
        po = report.payment_optimization
        print("PAYMENT OPTIMIZATION:")
        print(f"  Current: {po.current_terms}")
        print(f"  Recommended: {po.recommended_terms}")
        print(f"  Cash Flow Impact: ${po.cash_flow_impact:,.0f}")
        print(f"  Rationale: {po.rationale}")
        print()

    if report.liability_exposures:
        print("LIABILITY EXPOSURES:")
        for l in report.liability_exposures:
            print(f"  [{l.severity.value.upper():>6}] {l.clause}")
            print(f"        Exposure: {l.exposure}")
            print(f"        Mitigation: {l.mitigation}")
            print()

    print("PRIORITY ACTIONS:")
    for a in report.priority_actions:
        print(f"  - {a}")


def main():
    parser = argparse.ArgumentParser(description="NG-004 Terms Optimizer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--value", default="0")
    p.add_argument("--contract_type")
    p.add_argument("--terms")
    p.add_argument("--changes")
    p.add_argument("--payment")
    p.add_argument("--industry")
    p.add_argument("--legal_notes")
    args = parser.parse_args()
    if args.command == "analyze":
        cmd_analyze(args)


if __name__ == "__main__":
    main()
