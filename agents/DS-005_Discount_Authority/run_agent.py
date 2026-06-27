from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.cli_utils import patch_print; patch_print()
from agent.authority import DiscountAuthority, DiscountRequest


def cmd_evaluate(args: argparse.Namespace):
    a = DiscountAuthority()
    request = DiscountRequest(
        deal_id=args.deal_id,
        rep_name=args.rep or "Unknown",
        rep_role=args.role or "ae",
        deal_value=float(args.value or 0),
        requested_discount_pct=float(args.discount or 0),
        current_margin_pct=float(args.margin or 70),
        competitive_pressure=args.pressure or "none",
        buyer_relationship=args.relationship or "new",
        reason=args.reason or "",
    )
    decision = asyncio.run(a.evaluate_discount(request))

    print(f"=== DS-005 DISCOUNT AUTHORITY DECISION ===")
    print(f"Deal: {decision.deal_id}")
    print(f"Decision: {decision.decision.value.upper()}")
    print(f"Approved Discount: {decision.approved_discount_pct:.0f}%")
    print(f"Approval Level: {decision.approval_level.value}")
    print(f"Rationale: {decision.rationale}")
    print()
    if decision.conditions:
        print("CONDITIONS:")
        for c in decision.conditions:
            print(f"  - {c}")
        print()
    if decision.alternative_concessions:
        print("ALTERNATIVE CONCESSIONS:")
        for a in decision.alternative_concessions:
            print(f"  - {a}")


def main():
    parser = argparse.ArgumentParser(description="DS-005 Discount Authority")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("evaluate")
    p.add_argument("--deal_id", required=True)
    p.add_argument("--rep")
    p.add_argument("--role")
    p.add_argument("--value", default="0")
    p.add_argument("--discount", default="0")
    p.add_argument("--margin", default="70")
    p.add_argument("--pressure")
    p.add_argument("--relationship")
    p.add_argument("--reason")
    args = parser.parse_args()
    if args.command == "evaluate":
        cmd_evaluate(args)


if __name__ == "__main__":
    main()
