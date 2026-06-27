#!/usr/bin/env python3
"""CLI entry point for MO-004 Commitment Tracker.

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
from agent.tracker import CommitmentTracker


def main():
    parser = argparse.ArgumentParser(description="MO-004 Commitment Tracker")
    parser.add_argument("--analyze", type=str, help="Deal ID")
    parser.add_argument("--meeting", type=str, default="m_001", help="Meeting ID")
    parser.add_argument("--simulate", type=str, help="Deal ID for simulation")

    args = parser.parse_args()
    agent = CommitmentTracker()

    async def run():
        await agent.nats.connect()
        if args.analyze:
            transcript = (
                "Seller: Great meeting today. Let me send you the pricing proposal by EOD.\n"
                "Buyer: Thanks. I'll review it internally with my team this week.\n"
                "Seller: Also, I'll schedule a technical demo for next Tuesday.\n"
                "Buyer: Perfect. I'll introduce you to our CTO, she'll want to be involved.\n"
                "Seller: Looking forward to it. Should I also prepare the security docs?\n"
                "Buyer: Yes, please send those over too. Our security team will need to review.\n"
            )
            result = await agent._analyze(
                f"{args.analyze}:{args.meeting}",
                args.analyze, args.meeting,
                {"meeting_id": args.meeting, "full_text": transcript},
            )
            if result:
                print(f"=== COMMITMENT TRACKING: {args.analyze}/{args.meeting} ===")
                print(f"Total: {len(result.log.commitments)} | "
                      f"Buyer: {result.log.buyer_count} | Seller: {result.log.seller_count} | "
                      f"None: {result.no_commitments}")
                print()
                for c in result.log.commitments:
                    print(f"  [{c.party.value}] {c.type.value}")
                    print(f"    {c.description[:80]}")
                    print(f"    By: {c.participant_id} | Deadline: {c.deadline or 'not stated'}")
                await agent._publish_result(result, args.analyze, args.meeting)
        elif args.simulate:
            transcript = (
                "Buyer: Interesting demo. We'll think about it.\n"
                "Seller: Great, let me know if you have any questions.\n"
            )
            result = await agent._analyze(
                f"{args.simulate}:{args.meeting}",
                args.simulate, args.meeting,
                {"meeting_id": args.meeting, "full_text": transcript},
            )
            if result:
                print(f"=== SIMULATION: {args.simulate}/{args.meeting} ===")
                print(f"Commitments: {len(result.log.commitments)}, "
                      f"No commitments detected: {result.no_commitments}")
        else:
            print("[MO-004] Use --analyze <deal_id> or --simulate <deal_id>")

    asyncio.run(run())


if __name__ == "__main__":
    main()
