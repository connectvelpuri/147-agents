#!/usr/bin/env python3
"""CLI entry point for QL-001 BANT/MEDDPICC Scorer.

Usage:
    python run_agent.py                                    # Run agent loop
    python run_agent.py --score "d_001"                    # Score a deal
    python run_agent.py --score "d_001" --transcript "..." # Score with transcript
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope
from agent.scorer import QualificationScorer


def main():
    parser = argparse.ArgumentParser(description="QL-001 BANT/MEDDPICC Scorer")
    parser.add_argument("--score", type=str, help="Deal ID to score")
    parser.add_argument("--transcript", type=str, default="", help="Meeting transcript text")

    args = parser.parse_args()
    agent = QualificationScorer()

    async def run():
        await agent.nats.connect()
        if args.score:
            result = await agent.score_deal(args.score, transcript=args.transcript)
            print(f"=== QUALIFICATION RESULT: {args.score} ===")
            if result.bant:
                b = result.bant
                print(f"BANT Composite: {b.composite:.2f}")
                print(f"  Budget:    {b.budget.score:.2f} ({b.budget.confidence.value})")
                print(f"  Authority: {b.authority.score:.2f} ({b.authority.confidence.value})")
                print(f"  Need:      {b.need.score:.2f} ({b.need.confidence.value})")
                print(f"  Timeline:  {b.timeline.score:.2f} ({b.timeline.confidence.value})")
            if result.meddpicc:
                m = result.meddpicc
                print(f"MEDDPICC Composite: {m.composite:.2f}")
            print(f"DQI: {result.deal_quality_index:.2f}")
            print(f"Disqualify: {result.disqualify} {'- ' + result.disqualify_reason if result.disqualify else ''}")
            if result.gaps:
                print(f"Gaps ({len(result.gaps)}):")
                for g in result.gaps:
                    print(f"  - {g}")
            if result.next_questions:
                print(f"Next questions ({len(result.next_questions)}):")
                for q in result.next_questions:
                    print(f"  - {q}")
            await agent._publish_result(result, args.score)
        else:
            print("[QL-001] No action specified. Use --score <deal_id>")

    asyncio.run(run())


if __name__ == "__main__":
    main()
