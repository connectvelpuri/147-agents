"""
SDR-002 Intent Signal Monitor -- CLI entry point.

Usage:
  python run_agent.py scan --deal <id> [--account <json>]
  python run_agent.py simulate --deal <id> [--days <N>]
  python run_agent.py aggregate [--period daily|weekly]
  python run_agent.py trend --topic <topic> [--days <N>]
  python run_agent.py enrich --deal <id> [--context <text>]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent.monitor import IntentMonitor


def cmd_scan(args: argparse.Namespace):
    monitor = IntentMonitor()
    account = json.loads(args.account) if args.account else None
    readiness = monitor.scan_all_sources(args.deal, account)

    print(f"=== INTENT SCAN: {args.deal} ===")
    print(f"Readiness: {readiness.readiness_level.upper()} ({readiness.total_score}/100)")
    print(f"Signals: {readiness.signal_count} | Trend: {readiness.trend_direction}")
    print(f"Confidence: {readiness.confidence:.2f}")
    print()
    print("TOP SIGNALS:")
    for s in readiness.top_signals:
        days_ago = int(s.age_days())
        print(f"  [{s.strength.value:>8}] {s.signal_type.value:>15} "
              f"({s.source.value:>12}, {days_ago}d ago) -- {s.raw_text[:70]}")
    print()
    print(f"RECOMMENDATION: {readiness.recommendation}")


def cmd_simulate(args: argparse.Namespace):
    monitor = IntentMonitor()
    now = datetime.now()
    account = {
        "name": f"AcmeCorp-{args.deal}",
        "domain": "acmecorp.io",
        "industry": "enterprise SaaS",
    }
    readiness = monitor.scan_all_sources(args.deal, account, now)

    print(f"=== SIMULATION: {args.deal} ===")
    print(f"Account: {account['name']} ({account['domain']})")
    print(f"Readiness: {readiness.readiness_level.upper()} (score: {readiness.total_score}/100)")
    print(f"Signals Found: {readiness.signal_count}")
    print(f"Trend: {readiness.trend_direction}")
    print(f"Confidence: {readiness.confidence:.2f}")
    print()
    print("ALL SIGNALS (sorted by weight):")
    for i, s in enumerate(readiness.active_signals, 1):
        days_ago = int(s.age_days())
        w = s.effective_weight
        print(f"  {i:2}. [{s.strength.value:>8}] {s.signal_type.value:>15} "
              f"({s.source.value:>12}, {days_ago:2d}d, w={w:.1f})")
        print(f"       {s.raw_text[:80]}")
        if s.topic:
            print(f"       topic={s.topic}")
    print()
    print(f"RECOMMENDATION: {readiness.recommendation}")

    triggers = monitor.evaluate_triggers(readiness)
    if triggers:
        print(f"\nOUTREACH TRIGGERS (sorted by priority):")
        for t in triggers[:5]:
            print(f"  [P{t.priority}] {t.recommended_action} [{t.recommended_channel}]")

    agg = monitor.aggregate("daily", now)
    print(f"\nAGGREGATION ({agg.period}):")
    print(f"  Total signals: {agg.total_signals}")
    if agg.by_type:
        print(f"  By type: {agg.by_type}")
    if agg.by_source:
        print(f"  By source: {agg.by_source}")
    print(f"  Summary: {agg.summary}")


def _seed_for_aggregate(monitor: IntentMonitor):
    for deal_id in ["d_001", "d_002", "d_003", "d_100", "d_101"]:
        monitor.scan_all_sources(deal_id)

def cmd_aggregate(args: argparse.Namespace):
    monitor = IntentMonitor()
    _seed_for_aggregate(monitor)
    agg = monitor.aggregate(args.period)

    print(f"=== SIGNAL AGGREGATION ({agg.period}) ===")
    print(f"Period: {agg.start_date.date()} -> {agg.end_date.date()}")
    print(f"Total signals: {agg.total_signals}")
    print(f"By type: {json.dumps(agg.by_type, indent=2)}")
    print(f"By source: {json.dumps(agg.by_source, indent=2)}")
    print(f"Summary: {agg.summary}")


def cmd_trend(args: argparse.Namespace):
    monitor = IntentMonitor()
    _seed_for_aggregate(monitor)
    trend = monitor.detect_trend(args.topic, args.days)

    print(f"=== TREND: {trend.topic} ({trend.period_days}d) ===")
    print(f"Signals: {trend.signal_count} | Growth: {trend.growth_rate:+.1f}%")
    print(f"Severity: {trend.severity.upper()}")
    print(f"Accounts Affected: {len(trend.accounts_affected)}")
    print(f"Recommendation: {trend.recommendation}")


def cmd_enrich(args: argparse.Namespace):
    monitor = IntentMonitor()
    readiness = monitor.scan_all_sources(args.deal)
    enriched = monitor.enrich_with_llm(readiness, args.context)

    print(f"=== LLM ENRICHMENT: {args.deal} ===")
    print(f"Assessment: {enriched.get('assessment', 'N/A')}")
    print(f"Next Action: {enriched.get('next_action', 'N/A')}")
    print(f"Channel: {enriched.get('channel', 'N/A')}")
    print(f"Talking Points:")
    for tp in enriched.get("talking_points", []):
        print(f"  - {tp}")
    print(f"Risk Factors:")
    for rf in enriched.get("risk_factors", []):
        print(f"  - {rf}")


def main():
    parser = argparse.ArgumentParser(description="SDR-002 Intent Signal Monitor")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--deal", required=True)
    p_scan.add_argument("--account")

    p_sim = sub.add_parser("simulate")
    p_sim.add_argument("--deal", required=True)
    p_sim.add_argument("--days", type=int, default=14)

    p_agg = sub.add_parser("aggregate")
    p_agg.add_argument("--period", choices=["daily", "weekly"], default="weekly")

    p_trend = sub.add_parser("trend")
    p_trend.add_argument("--topic", required=True)
    p_trend.add_argument("--days", type=int, default=30)

    p_enrich = sub.add_parser("enrich")
    p_enrich.add_argument("--deal", required=True)
    p_enrich.add_argument("--context")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "aggregate":
        cmd_aggregate(args)
    elif args.command == "trend":
        cmd_trend(args)
    elif args.command == "enrich":
        cmd_enrich(args)


if __name__ == "__main__":
    main()
