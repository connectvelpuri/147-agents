#!/usr/bin/env python3
"""CLI entry point for MO-003 Objection Detector and Classifier.

Usage:
    python run_agent.py --analyze "d_001" --meeting "m_001"
    python run_agent.py --simulate "d_001" --meeting "m_001"
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope, new_event_id
from agent.detector import ObjectionDetector


def main():
    parser = argparse.ArgumentParser(description="MO-003 Objection Detector")
    parser.add_argument("--analyze", type=str, help="Deal ID")
    parser.add_argument("--meeting", type=str, default="m_001", help="Meeting ID")
    parser.add_argument("--simulate", type=str, help="Deal ID for simulation")

    args = parser.parse_args()
    agent = ObjectionDetector()

    async def run():
        await agent.nats.connect()
        if args.analyze:
            transcript = (
                "Buyer: This looks interesting but it seems really expensive for what we need.\n"
                "Seller: I understand the concern. Let me share some ROI data.\n"
                "Buyer: We're also evaluating another vendor right now.\n"
                "Seller: We're confident in our differentiation. Can we discuss specifics?\n"
                "Buyer: I'm not sure the timing is right. We have other priorities this quarter.\n"
                "Seller: What if we phased the implementation?\n"
                "Buyer: I'll need to check with our security team before moving forward.\n"
            )
            result = await agent._analyze(
                f"{args.analyze}:{args.meeting}",
                args.analyze, args.meeting,
                {"meeting_id": args.meeting, "full_text": transcript},
            )
            if result:
                print(f"=== OBJECTION ANALYSIS: {args.analyze}/{args.meeting} ===")
                print(f"Total objections: {result.objection_count}")
                print(f"Blocking: {result.blocking_count}")
                print(f"Addressed: {result.addressed_count}")
                print(f"\nObjections:")
                for o in result.log.objections:
                    status = "ADDRESSED" if o.addressed else "UNANSWERED"
                    print(f"  [{o.severity.value}] {o.category.value} | {o.utterance[:60]} | {status}")
                if result.alerts:
                    print(f"\nUnaddressed alerts ({len(result.alerts)}):")
                    for a in result.alerts:
                        print(f"  {a.category.value}: {a.context[:60]}")
                if result.log.response_map:
                    print(f"\nRecommended responses:")
                    for cat, r in result.log.response_map.items():
                        print(f"  {cat}: {r.strategy}")
                await agent._publish_result(result, args.analyze, args.meeting)
        elif args.simulate:
            transcript = (
                f"Buyer: We're happy with our current solution. Not sure we need this.\n"
                f"Seller: I see. Can I ask what your current setup lacks?\n"
                f"Buyer: Budget is tight this quarter. We can't afford another tool.\n"
                f"Seller: Many customers find the ROI justifies the investment within 3 months.\n"
                f"Buyer: I'd also need to get legal and security to sign off.\n"
            )
            result = await agent._analyze(
                f"{args.simulate}:{args.meeting}",
                args.simulate, args.meeting,
                {"meeting_id": args.meeting, "full_text": transcript},
            )
            if result:
                print(f"=== SIMULATION: {args.simulate}/{args.meeting} ===")
                print(f"Objections: {result.objection_count}, Blocking: {result.blocking_count}, "
                      f"Alerts: {len(result.alerts)}")
        else:
            print("[MO-003] Use --analyze <deal_id> or --simulate <deal_id>")

    asyncio.run(run())


if __name__ == "__main__":
    main()
