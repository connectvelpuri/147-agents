#!/usr/bin/env python3
"""CLI entry point for MO-001 Meeting Observer.

Usage:
    python run_agent.py                                # Run agent loop
    python run_agent.py --simulate-start "mid_001"     # Simulate meeting start
    python run_agent.py --simulate-chunk "mid_001"     # Simulate audio chunk
    python run_agent.py --simulate-end "mid_001"       # Simulate meeting end
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent_base.event_envelope import EventEnvelope
from agent.observer import MeetingObserver


def main():
    parser = argparse.ArgumentParser(description="MO-001 Meeting Observer")
    parser.add_argument("--simulate-start", type=str, help="Simulate meeting start")
    parser.add_argument("--simulate-chunk", type=str, help="Simulate audio chunk for meeting")
    parser.add_argument("--simulate-end", type=str, help="Simulate meeting end")
    parser.add_argument("--chunks", type=int, default=3, help="Number of chunks for simulation")
    parser.add_argument("--simulate-full", type=str, help="Simulate full meeting cycle: start -> N chunks -> end")

    args = parser.parse_args()
    agent = MeetingObserver()

    async def run():
        await agent.nats.connect()

        if args.simulate_full:
            meeting_id = args.simulate_full
            # Start
            env = EventEnvelope(event_type="meeting.started", source_agent="cli",
                                deal_id=meeting_id,
                                data={"meeting_id": meeting_id, "platform": "zoom"})
            await agent.handle_event(env)
            # Chunks
            for i in range(args.chunks):
                env = EventEnvelope(event_type="meeting.audio.chunk", source_agent="cli",
                                    deal_id=meeting_id,
                                    data={"meeting_id": meeting_id, "chunk_index": i,
                                          "platform": "zoom", "duration_seconds": 5.0})
                await agent.handle_event(env)
            # End
            env = EventEnvelope(event_type="meeting.ended", source_agent="cli",
                                deal_id=meeting_id,
                                data={"meeting_id": meeting_id})
            await agent.handle_event(env)
            print(f"[MO-001] Full meeting cycle complete for {meeting_id}")
            return

        if args.simulate_start:
            env = EventEnvelope(event_type="meeting.started", source_agent="cli",
                                deal_id=args.simulate_start,
                                data={"meeting_id": args.simulate_start, "platform": "zoom"})
            await agent.handle_event(env)
        if args.simulate_chunk:
            for i in range(args.chunks):
                env = EventEnvelope(event_type="meeting.audio.chunk", source_agent="cli",
                                    deal_id=args.simulate_chunk,
                                    data={"meeting_id": args.simulate_chunk, "chunk_index": i,
                                          "platform": "zoom", "duration_seconds": 5.0})
                await agent.handle_event(env)
        if args.simulate_end:
            env = EventEnvelope(event_type="meeting.ended", source_agent="cli",
                                deal_id=args.simulate_end,
                                data={"meeting_id": args.simulate_end})
            await agent.handle_event(env)
        print("[MO-001] Simulation complete")

    asyncio.run(run())


if __name__ == "__main__":
    main()
