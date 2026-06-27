#!/usr/bin/env python3
"""CLI entry point for MO-002 Sentiment and Emotion Analyst.

Usage:
    python run_agent.py                                                       # Run agent loop
    python run_agent.py --analyze "d_001" --meeting "m_001"                   # Analyze meeting
    python run_agent.py --simulate "d_001" --meeting "m_001" --chunks 3       # Simulate meeting
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope, new_event_id
from agent.analyst import SentimentAnalyst


def main():
    parser = argparse.ArgumentParser(description="MO-002 Sentiment and Emotion Analyst")
    parser.add_argument("--analyze", type=str, help="Deal ID to analyze")
    parser.add_argument("--meeting", type=str, default="m_001", help="Meeting ID")
    parser.add_argument("--simulate", type=str, help="Deal ID for simulation")
    parser.add_argument("--chunks", type=int, default=3, help="Number of chunks to simulate")

    args = parser.parse_args()
    agent = SentimentAnalyst()

    async def run():
        await agent.nats.connect()
        if args.analyze:
            await agent._handle_full(
                f"{args.analyze}:{args.meeting}",
                args.analyze,
                args.meeting,
                {
                    "meeting_id": args.meeting,
                    "full_text": (
                        "Alice: Thanks for joining today. We're excited to show you our platform.\n"
                        "Bob: Great, we've been looking forward to this. Our team has some concerns "
                        "about integration complexity though.\n"
                        "Alice: I understand. Let me walk through our integration architecture. "
                        "It's built to be modular.\n"
                        "Bob: That sounds promising. What about pricing? We have a budget of $50k "
                        "for this quarter.\n"
                        "Alice: Our enterprise plan starts at $45k. Let me share a pricing breakdown.\n"
                        "Bob: That's within range. I'm impressed with the demo. When can we start "
                        "a trial?\n"
                        "Alice: We can set that up this week. I'll send you the onboarding materials.\n"
                        "Bob: Perfect. Let's do it."
                    ),
                    "speakers": ["Alice", "Bob"],
                },
            )
            result = agent._sessions.get(f"{args.analyze}:{args.meeting}")
            if result:
                print(f"=== SENTIMENT ANALYSIS: {args.analyze}/{args.meeting} ===")
                print(f"Overall: {result.overall_meeting_sentiment.value}")
                for t in result.timelines:
                    print(f"\nParticipant: {t.participant_id}")
                    print(f"  Sentiment: {t.overall_sentiment.value}")
                    print(f"  Trend: {t.trend.value}")
                    print(f"  Emotions: {[e.value for e in t.dominant_emotions]}")
                print(f"\nHighlights: {len(result.highlights)}")
                for h in result.highlights[:3]:
                    print(f"  [{h.emotion.value}@{h.timestamp_sec}s] {h.context}")
                print(f"\nFrustration alerts: {len(result.frustration_alerts)}")
                for fa in result.frustration_alerts:
                    print(f"  [{fa.participant_id}] {fa.context}")
                print(f"\nConfusion markers: {len(result.confusion_markers)}")
                await agent._publish_result(result, args.analyze, args.meeting)
        elif args.simulate:
            deal_id = args.simulate
            meeting_id = args.meeting
            speakers = ["Alice", "Bob", "Carol"]
            sentiments = [
                "great platform, exactly what we need",
                "concerned about pricing, seems expensive",
                "can you explain how the integration works",
                "this demo is impressive, our team would love this",
                "not sure about the timeline, we have other priorities",
                "the ROI numbers look compelling",
            ]
            for i in range(args.chunks):
                sp = speakers[i % len(speakers)]
                text = sentiments[i % len(sentiments)]
                chunk = {
                    "meeting_id": meeting_id,
                    "speaker": sp,
                    "text": text,
                    "timestamp_sec": i * 300,
                }
                await agent._handle_chunk(f"{deal_id}:{meeting_id}", deal_id, meeting_id, chunk)
                print(f"[SIM] Chunk {i+1}: {sp} -> {text[:40]}...")
            await agent._handle_full(
                f"{deal_id}:{meeting_id}",
                deal_id,
                meeting_id,
                {"meeting_id": meeting_id, "full_text": "\n".join(
                    f"{speakers[i % len(speakers)]}: {sentiments[i % len(sentiments)]}"
                    for i in range(args.chunks * 2)
                ), "speakers": speakers},
            )
            result = agent._sessions.get(f"{deal_id}:{meeting_id}")
            if result:
                print(f"\n=== SIMULATION COMPLETE ===")
                print(f"Sentiment: {result.overall_meeting_sentiment.value}")
                print(f"Frustration alerts: {len(result.frustration_alerts)}")
                print(f"Confusion markers: {len(result.confusion_markers)}")
        else:
            print("[MO-002] No action specified. Use --analyze <deal_id> or --simulate <deal_id>")

    asyncio.run(run())


if __name__ == "__main__":
    main()
