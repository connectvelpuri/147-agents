#!/usr/bin/env python3
"""CLI entry point for AI-001 Account Research Agent.

Usage:
    python run_agent.py --account "Example Corp"
    python run_agent.py --account "Example Corp" --depth deep
    python run_agent.py --monitor
    python run_agent.py --report                    # Show last research cycle
    python run_agent.py --feedback                   # Show correction/feedback stats
    python run_agent.py --list                       # List all researched accounts
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from agent.models import AccountRequest, ResearchDepth, CorrectionEvent
from agent.orchestrator import AccountResearchOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="AI-001 Account Research Agent — RevenueOS Intelligence Foundation"
    )
    parser.add_argument("--account", "-a", type=str, help="Account name to research")
    parser.add_argument("--domain", type=str, default="", help="Account website domain")
    parser.add_argument("--depth", type=str, default="standard",
                        choices=["quick", "standard", "deep"],
                        help="Research depth (default: standard)")
    parser.add_argument("--monitor", action="store_true",
                        help="Run monitoring cycle for all active accounts")
    parser.add_argument("--report", action="store_true",
                        help="Show last research cycle report")
    parser.add_argument("--feedback", action="store_true",
                        help="Show feedback and correction statistics")
    parser.add_argument("--list", action="store_true",
                        help="List all researched accounts")
    parser.add_argument("--init-db", action="store_true",
                        help="Initialize database and exit")

    args = parser.parse_args()
    orchestrator = AccountResearchOrchestrator()

    try:
        if args.init_db:
            print("[OK] Database initialized at data/state.db")
            return

        if args.account:
            request = AccountRequest(
                account_name=args.account,
                account_id=_make_id(args.account),
                depth=ResearchDepth(args.depth),
            )
            report = orchestrator.research_account(request)
            print(f"\n=== INTELLIGENCE SUMMARY ===")
            print(f"Account: {report.account_name}")
            print(f"Depth: {report.research_depth.value}")
            print(f"Confidence: {report.overall_confidence:.0%}")
            print(f"Strategic initiatives identified: {len(report.strategic_initiatives)}")
            print(f"Buying signals: {len(report.buying_signals)}")
            print(f"Risk factors: {len(report.risk_factors)}")
            print(f"Competitors: {len(report.competitors_present)}")
            print(f"=============================")

        elif args.monitor:
            print("[MONITOR] Checking active accounts for new signals...")
            orchestrator.monitor_accounts()
            print("[MONITOR] Cycle complete")

        elif args.report:
            print("[REPORT] See data/state.db for latest research state")

        elif args.feedback:
            rates = orchestrator.feedback.get_correction_rate_by_domain()
            print("=== CORRECTION RATES BY DOMAIN ===")
            for domain, rate in rates.items():
                print(f"  {domain}: {rate:.1%}")
            print(f"  Should trigger retrain: {orchestrator.feedback.should_trigger_retrain()}")

        elif args.list:
            conn = orchestrator.db._get_conn()
            rows = conn.execute(
                "SELECT account_id, account_name, depth, status, confidence_score, last_researched_at FROM accounts ORDER BY last_researched_at DESC"
            ).fetchall()
            print("=== RESEARCHED ACCOUNTS ===")
            for r in rows:
                print(f"  {r['account_id']:20s} | {r['account_name']:25s} | {r['depth']:10s} | "
                      f"{r['status']:15s} | confidence: {r['confidence_score']:.0%} | "
                      f"{r['last_researched_at'] or 'never'}")
            if not rows:
                print("  No accounts researched yet.")

        else:
            parser.print_help()

    finally:
        orchestrator.close()


def _make_id(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")[:30]


if __name__ == "__main__":
    main()
