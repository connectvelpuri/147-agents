"""
SDR-003 Personalized Outreach Generator -- CLI entry point.

Usage:
  python run_agent.py email --name <name> --title <title> --company <company> [--industry <ind>] [--signals <json>] [--llm]
  python run_agent.py linkedin --name <name> --title <title> --company <company> [--llm]
  python run_agent.py call --name <name> --title <title> --company <company> [--llm]
  python run_agent.py sequence --name <name> --title <title> --company <company> [--design standard_14day|intensive_7day|li_first_10day]
  python run_agent.py enrich --name <name> --title <title> --company <company>
  python run_agent.py simulate --deal <id> [--prospects <N>]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from agent.generator import OutreachGenerator
from agent.models import (
    Prospect, Channel, OutreachStage, estimate_personalization_depth,
    SEQUENCE_DESIGNS,
)


def _make_prospect(args: argparse.Namespace) -> Prospect:
    def _split(val):
        return [s.strip() for s in val.split("|") if s.strip()] if val else []

    signals = _split(getattr(args, "signals", None))
    activity = _split(getattr(args, "activity", None))
    news = _split(getattr(args, "news", None))
    notes = _split(getattr(args, "notes", None))

    return Prospect(
        contact_id=args.contact_id if getattr(args, "contact_id", None) else f"prospect_{args.name.lower().replace(' ', '_')}",
        name=args.name,
        title=args.title,
        company=args.company,
        industry=args.industry if getattr(args, "industry", None) else "SaaS",
        company_size=args.size if getattr(args, "size", None) else "51-200",
        intent_signals=signals,
        recent_activity=activity,
        company_news=news,
        personal_notes=notes,
    )


def cmd_email(args: argparse.Namespace):
    gen = OutreachGenerator()
    prospect = _make_prospect(args)
    stage = OutreachStage(args.stage) if getattr(args, "stage", None) else OutreachStage.INITIAL

    email = gen.generate_email(prospect, stage=stage, force_llm=args.llm if getattr(args, "llm", None) else False)

    depth = estimate_personalization_depth(prospect)
    print(f"=== EMAIL DRAFT ===")
    print(f"To: {prospect.name} <{prospect.title} @ {prospect.company}>")
    print(f"Depth: {depth.value.upper()} | Template: {email.template_id}")
    print(f"Est. Reply Rate: {email.estimated_reply_rate:.0%}")
    print()
    print(f"Subject: {email.subject}")
    print(f"Preview: {email.preview_text}")
    print()
    print("---")
    print(email.body)
    print("---")
    print(f"CTA: {email.cta}")
    print(f"Chars: {email.character_count}")


def cmd_linkedin(args: argparse.Namespace):
    gen = OutreachGenerator()
    prospect = _make_prospect(args)
    msg_type = args.msg_type if getattr(args, "msg_type", None) else "connection_request"

    msg = gen.generate_linkedin_message(prospect, message_type=msg_type, force_llm=args.llm if getattr(args, "llm", None) else False)

    depth = estimate_personalization_depth(prospect)
    print(f"=== LINKEDIN MESSAGE ===")
    print(f"To: {prospect.name} ({prospect.title} @ {prospect.company})")
    print(f"Type: {msg.message_type} | Depth: {depth.value.upper()}")
    print(f"Chars: {msg.character_count} | Est. Response Rate: {msg.estimated_response_rate:.0%}")
    print()
    if msg.subject:
        print(f"Subject: {msg.subject}")
    print("---")
    print(msg.body)
    print("---")


def cmd_call(args: argparse.Namespace):
    gen = OutreachGenerator()
    prospect = _make_prospect(args)

    script = gen.generate_call_script(prospect, force_llm=args.llm if getattr(args, "llm", None) else False)

    depth = estimate_personalization_depth(prospect)
    print(f"=== CALL SCRIPT ===")
    print(f"Prospect: {prospect.name} ({prospect.title} @ {prospect.company})")
    print(f"Depth: {depth.value.upper()}")
    print(f"Est. Duration: {script.estimated_duration_seconds}s")
    print()
    print(f"OPENING ({30}s):")
    print(f"  {script.opening}")
    print()
    print(f"VALUE PROP:")
    print(f"  {script.value_proposition}")
    print()
    print("DISCOVERY QUESTIONS:")
    for i, q in enumerate(script.discovery_questions, 1):
        print(f"  {i}. {q}")
    print()
    print("OBJECTION HANDLERS:")
    for obj, resp in script.objection_handlers:
        print(f"  O: {obj}")
        print(f"  R: {resp}")
        print()
    print(f"CLOSING:")
    print(f"  {script.closing}")


def cmd_sequence(args: argparse.Namespace):
    gen = OutreachGenerator()
    prospect = _make_prospect(args)
    design = args.design if getattr(args, "design", None) else "standard_14day"

    seq = gen.design_sequence(prospect, design)
    depth = estimate_personalization_depth(prospect)

    print(f"=== MULTI-CHANNEL SEQUENCE: {seq.sequence_id} ===")
    print(f"Prospect: {prospect.name} ({prospect.title} @ {prospect.company})")
    print(f"Depth: {depth.value.upper()} | Design: {design}")
    print(f"Duration: {seq.duration_days} days | Touches: {seq.total_touches}")
    print(f"Channels: {', '.join(c.value for c in seq.channels_used)}")
    print()
    print(f"{'DAY':>4} {'CHANNEL':>12} {'STAGE':>16} {'CONTENT':<60}")
    print("-" * 100)
    for step in seq.steps:
        if isinstance(step.content, object) and hasattr(step.content, "__class__"):
            content_type = step.content.__class__.__name__
        else:
            content_type = str(type(step.content).__name__)
        preview = ""
        if hasattr(step.content, "subject") and step.content.subject:
            preview = step.content.subject[:55]
        elif hasattr(step.content, "body"):
            preview = step.content.body[:55].replace("\n", " ")
        condition = f" [{step.condition}]" if step.condition else ""
        print(f"{step.day:>4} {step.channel.value:>12} {step.stage.value:>16} {preview:<60}{condition[:30]}")
    print()


def cmd_enrich(args: argparse.Namespace):
    gen = OutreachGenerator()
    prospect = _make_prospect(args)
    context = args.context if getattr(args, "context", None) else None

    enriched = gen.enrich_with_llm(prospect, context=context)

    print(f"=== LLM ENRICHMENT ===")
    print(f"Subject: {enriched.get('subject_line', 'N/A')}")
    print(f"Body: {enriched.get('body', 'N/A')[:200]}...")
    print(f"CTA: {enriched.get('cta', 'N/A')}")
    print(f"Channel: {enriched.get('channel_recommendation', 'N/A')}")


def cmd_simulate(args: argparse.Namespace):
    gen = OutreachGenerator()
    n = args.prospects if getattr(args, "prospects", None) else 3

    profiles = [
        ("Sarah Chen", "VP of Sales", "DataStream Analytics", "SaaS", "201-1000",
         ["looking for CRM recommendations", "visited pricing page"],
         ["raised $30M Series B"],
         ["Mentioned at SaaStr annual"]),
        ("Mike O'Brien", "CTO", "NexGen Health", "Healthcare", "51-200",
         ["evaluating sales engagement platforms"],
         ["HIPAA compliance initiative", "hiring sales team"],
         ["Spoke at HIMSS conference"]),
        ("Priya Patel", "Head of Marketing", "FinFlow", "Fintech", "201-1000",
         ["reading case studies on category page"],
         ["launched new product line", "expanding to EU"],
         []),
    ]

    designs = list(SEQUENCE_DESIGNS.keys())

    for i in range(min(n, len(profiles))):
        name, title, company, industry, size, activity, news, notes = profiles[i]
        prospect = Prospect(
            contact_id=f"p_{i+1:03d}",
            name=name, title=title, company=company,
            industry=industry, company_size=size,
            recent_activity=activity, company_news=news,
            personal_notes=notes,
        )

        design = designs[i % len(designs)]
        seq = gen.design_sequence(prospect, design)
        depth = estimate_personalization_depth(prospect)

        email = gen.generate_email(prospect)
        linkedin = gen.generate_linkedin_message(prospect)
        call_scr = gen.generate_call_script(prospect)

        print(f"=== SIMULATION: Prospect {i+1} ===")
        print(f"Name: {name} | Title: {title} | Company: {company}")
        print(f"Depth: {depth.value.upper()} | Design: {design}")
        print(f"Sequence: {seq.total_touches} touches over {seq.duration_days} days")
        print()
        print(f"EMAIL: \"{email.subject}\" ({email.estimated_reply_rate:.0%} est.)")
        print(f"  {email.body[:100].replace(chr(10), ' ')}...")
        print(f"LINKEDIN: {linkedin.message_type} ({linkedin.character_count} chars, {linkedin.estimated_response_rate:.0%} est.)")
        print(f"  {linkedin.body[:80].replace(chr(10), ' ')}...")
        print(f"CALL: {call_scr.estimated_duration_seconds}s script | {len(call_scr.discovery_questions)} questions")
        print(f"  OPEN: {call_scr.opening[:80].replace(chr(10), ' ')}...")
        print()

        var = gen.create_variant(seq, "B", ["different subject line", "shortened intro"])
        print(f"  Variant {var.variant_label}: {', '.join(var.changes)} (expected lift: {var.expected_lift:.0%})")
        print()

    stats = gen.get_template_stats()
    if stats:
        print("TEMPLATE STATS:")
        for tid, st in stats.items():
            print(f"  {tid}: {st['uses']} uses, {st['successes']} success ({st['success_rate']:.0%})")


def main():
    parser = argparse.ArgumentParser(description="SDR-003 Personalized Outreach Generator")
    sub = parser.add_subparsers(dest="command", required=True)

    shared_args = argparse.ArgumentParser(add_help=False)
    shared_args.add_argument("--name", required=True)
    shared_args.add_argument("--title", required=True)
    shared_args.add_argument("--company", required=True)
    shared_args.add_argument("--industry", default="SaaS")
    shared_args.add_argument("--size", default="51-200")
    shared_args.add_argument("--signals")
    shared_args.add_argument("--activity")
    shared_args.add_argument("--news")
    shared_args.add_argument("--notes")
    shared_args.add_argument("--contact_id")

    p_email = sub.add_parser("email", parents=[shared_args])
    p_email.add_argument("--stage", choices=[s.value for s in OutreachStage], default="initial")
    p_email.add_argument("--llm", action="store_true")

    p_li = sub.add_parser("linkedin", parents=[shared_args])
    p_li.add_argument("--msg_type", default="connection_request")
    p_li.add_argument("--llm", action="store_true")

    p_call = sub.add_parser("call", parents=[shared_args])
    p_call.add_argument("--llm", action="store_true")

    p_seq = sub.add_parser("sequence", parents=[shared_args])
    p_seq.add_argument("--design", choices=list(SEQUENCE_DESIGNS.keys()), default="standard_14day")

    p_enrich = sub.add_parser("enrich", parents=[shared_args])
    p_enrich.add_argument("--context")

    p_sim = sub.add_parser("simulate")
    p_sim.add_argument("--deal", default="d_001")
    p_sim.add_argument("--prospects", type=int, default=3)

    args = parser.parse_args()

    if args.command == "email":
        cmd_email(args)
    elif args.command == "linkedin":
        cmd_linkedin(args)
    elif args.command == "call":
        cmd_call(args)
    elif args.command == "sequence":
        cmd_sequence(args)
    elif args.command == "enrich":
        cmd_enrich(args)
    elif args.command == "simulate":
        cmd_simulate(args)


if __name__ == "__main__":
    main()
