#!/usr/bin/env python3
"""
Revenue OS CLI - A production command-line chat interface for Revenue OS.
Works standalone (direct agent execution) or connected to the Railway API.

Usage:
    python cli.py                         # Interactive chat mode
    python cli.py --persona sales         # Force a specific persona
    python cli.py --api-key <key>         # Set API key
    python cli.py --url <url>             # Custom server URL
    python cli.py "query text"            # Single-shot query
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────
# Color & styling helpers - zero external deps
# ──────────────────────────────────────────────────────────────────────


class Style:
    """ANSI color/style helpers. Auto-detects terminal support."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @classmethod
    def supports_color(cls):
        if not sys.stdout.isatty():
            return False
        if os.name == 'nt':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except Exception:
                return False
        return True

    @classmethod
    def strip(cls, text):
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)


_USE_COLOR = Style.supports_color()


def c(text, *styles):
    """Colorize text if terminal supports it."""
    if not _USE_COLOR or not styles:
        return text
    return "".join(styles) + text + Style.RESET


def section_header(title, char="="):
    """Render a prominent section header."""
    width = min(72, max(48, len(title) + 12))
    line = char * width
    padded = f" {title} ".center(width, char)
    return (f"\n{c(line, Style.DIM, Style.GRAY)}\n"
            f"{c(padded, Style.BOLD, Style.BRIGHT_CYAN)}\n"
            f"{c(line, Style.DIM, Style.GRAY)}\n")


# ──────────────────────────────────────────────────────────────────────
# Persona definitions
# ──────────────────────────────────────────────────────────────────────


class Persona:
    """An agent persona with keyword-based routing rules."""

    def __init__(self, name, display_name, description, keywords, system_prompt):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.keywords = keywords
        self.system_prompt = system_prompt

    def matches(self, query):
        q = query.lower()
        return any(kw.lower() in q for kw in self.keywords)


PERSONAS = [
    Persona(
        "sales", "Sales Strategist",
        "Handles sales strategy, pipeline management, prospecting, and closing techniques.",
        ["sales", "pipeline", "deal", "prospect", "close", "revenue",
         "quota", "lead", "opportunity", "upsell", "cross-sell",
         "cold email", "outreach", "demo", "negotiation", "objection"],
        "You are a Sales Strategist for Revenue OS. You help with sales strategy, "
        "pipeline management, prospecting, closing techniques, and revenue growth. "
        "Provide actionable, data-driven advice. Be direct and professional.",
    ),
    Persona(
        "marketing", "Marketing Analyst",
        "Handles marketing campaigns, analytics, content strategy, and brand positioning.",
        ["marketing", "campaign", "content", "brand", "analytics",
         "seo", "social media", "email marketing", "lead gen",
         "conversion", "a/b test", "landing page", "funnel",
         "demand generation", "ppc", "ads"],
        "You are a Marketing Analyst for Revenue OS. You help with marketing campaigns, "
        "analytics, content strategy, brand positioning, and demand generation. "
        "Provide insights backed by best practices. Be creative and strategic.",
    ),
    Persona(
        "support", "Customer Success",
        "Handles customer support, onboarding, retention, and success workflows.",
        ["support", "help", "issue", "bug", "problem", "error",
         "customer", "onboarding", "retention", "churn", "ticket",
         "faq", "troubleshoot", "complaint", "feedback",
         "how do i", "how to", "not working"],
        "You are a Customer Success specialist for Revenue OS. You help with customer "
        "support, onboarding, retention, and success workflows. Be empathetic, thorough, "
        "and solution-oriented.",
    ),
    Persona(
        "product", "Product Manager",
        "Handles product roadmap, feature requests, prioritization, and strategy.",
        ["product", "feature", "roadmap", "backlog", "sprint",
         "user story", "requirement", "priority", "release",
         "product strategy", "pm", "spec", "mvp"],
        "You are a Product Manager for Revenue OS. You help with product roadmap, "
        "feature prioritization, user stories, and product strategy. "
        "Be strategic, user-focused, and data-informed.",
    ),
    Persona(
        "analytics", "Data Analyst",
        "Handles data analysis, reporting, metrics, and business intelligence.",
        ["analytics", "data", "report", "metric", "kpi", "dashboard",
         "analysis", "statistics", "forecast", "trend", "insight",
         "sql", "query", "chart", "visualization", "performance"],
        "You are a Data Analyst for Revenue OS. You help with data analysis, reporting, "
        "metrics, dashboards, and business intelligence. Be precise, analytical, and data-driven.",
    ),
    Persona(
        "general", "Revenue OS Assistant",
        "General assistant for all other queries about Revenue OS.",
        [],
        "You are a helpful AI assistant for Revenue OS. Answer questions about the platform, "
        "provide guidance, and help users achieve their revenue goals. "
        "Be friendly, knowledgeable, and concise.",
    ),
]

DEFAULT_PERSONA = PERSONAS[-1]


# ──────────────────────────────────────────────────────────────────────
# Conversation History
# ──────────────────────────────────────────────────────────────────────


class Conversation:
    """In-memory conversation history with optional JSON persistence."""

    def __init__(self, history_file=None, max_turns=50):
        self.history = []
        self.max_turns = max_turns
        self.history_file = history_file
        self._load()

    def _load(self):
        if self.history_file and os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.history = data.get('history', [])
            except (json.JSONDecodeError, IOError):
                self.history = []

    def save(self):
        if not self.history_file:
            return
        try:
            os.makedirs(os.path.dirname(self.history_file) or '.', exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump({'history': self.history[-self.max_turns:]}, f, indent=2)
        except IOError:
            pass

    def add_entry(self, role, content, persona=None):
        entry = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
        }
        if persona:
            entry['persona'] = persona
        self.history.append(entry)
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns:]

    def get_messages(self):
        return [{'role': e['role'], 'content': e['content']} for e in self.history]

    def get_context(self, max_exchanges=10):
        lines = []
        recent = self.history[-(max_exchanges * 2):]
        for entry in recent:
            label = "User" if entry['role'] == 'user' else "Assistant"
            if entry.get('persona'):
                label += f" ({entry['persona']})"
            lines.append(f"{label}: {entry['content']}")
        return "\n".join(lines)

    def clear(self):
        self.history = []
        self.save()

    def count_turns(self):
        return sum(1 for e in self.history if e['role'] == 'user')


# ──────────────────────────────────────────────────────────────────────
# Persona Router
# ──────────────────────────────────────────────────────────────────────


class PersonaRouter:
    """Routes messages to the correct agent persona."""

    def __init__(self, personas=None):
        self.personas = personas or PERSONAS

    def route(self, query, forced_persona=None):
        if forced_persona:
            for p in self.personas:
                if p.name == forced_persona.lower():
                    return p
            return DEFAULT_PERSONA
        for p in self.personas:
            if p.name == "general":
                continue
            if p.matches(query):
                return p
        return DEFAULT_PERSONA

    def list_personas(self):
        return [(p.name, p.display_name, p.description) for p in self.personas]


# ──────────────────────────────────────────────────────────────────────
# Standalone Agent (local fallback)
# ──────────────────────────────────────────────────────────────────────


class StandaloneAgent:
    """Local agent that generates contextual responses without an API."""

    RESPONSES = {
        "sales": {
            "pipeline|deal|opportunity": [
                "Let me analyze your sales pipeline. Key metrics to track:",
                "  \u2022 Deal velocity (avg time from creation to close)",
                "  \u2022 Win rate by stage",
                "  \u2022 Pipeline coverage ratio (weighted pipeline / quota)",
                "",
                "Would you like a deep-dive into any of these?",
            ],
            "email|outreach|prospect": [
                "Here's a proven outreach framework:",
                "  1. Personalize the first line",
                "  2. State the value in <10 words",
                "  3. Include a low-friction CTA",
                "",
                "Tip: A/B test subject lines \u2014 35-50% of opens depend on them.",
            ],
            "__default__": [
                "I can help with: sales strategy, pipeline management, prospecting,",
                "closing techniques, objection handling, and revenue forecasting.",
                "",
                "What aspect of sales would you like to explore?",
            ],
        },
        "marketing": {
            "campaign|funnel": [
                "Let's optimize your campaign funnel:",
                "  Top-of-funnel: awareness & reach metrics",
                "  Middle-of-funnel: engagement & consideration",
                "  Bottom-of-funnel: conversion & ROI",
                "",
                "Where is your biggest drop-off happening?",
            ],
            "__default__": [
                "I can help with: campaign strategy, content marketing, SEO,",
                "social media, email marketing, and analytics.",
                "",
                "What marketing challenge are you facing?",
            ],
        },
        "support": {
            "bug|error|not working|issue": [
                "Let's troubleshoot together. Please provide:",
                "  1. What were you trying to do?",
                "  2. What actually happened?",
                "  3. Any error messages?",
                "  4. What steps you've tried so far",
            ],
            "__default__": [
                "I'm here to help! I can assist with:",
                "  \u2022 Product setup and onboarding",
                "  \u2022 Feature questions and how-tos",
                "  \u2022 Troubleshooting and bug reporting",
                "  \u2022 Account and billing questions",
            ],
        },
        "product": {
            "feature|roadmap": [
                "Great idea! Here's how we evaluate feature requests:",
                "  \u2022 Strategic alignment (does it fit our vision?)",
                "  \u2022 User impact (how many users benefit?)",
                "  \u2022 Development effort (cost vs value)",
                "  \u2022 Revenue/retention impact",
                "",
                "Can you share more about the use case?",
            ],
            "__default__": [
                "I can help with: product strategy, roadmap planning,",
                "feature prioritization, user stories, and sprint planning.",
                "",
                "What product area are you thinking about?",
            ],
        },
        "analytics": {
            "report|dashboard|kpi|metric": [
                "Let's build a clear reporting structure:",
                "  \u2022 Leading indicators (predictive metrics)",
                "  \u2022 Lagging indicators (outcome metrics)",
                "  \u2022 Diagnostic metrics (why things happen)",
                "",
                "What business question are you trying to answer?",
            ],
            "__default__": [
                "I can help with: data analysis, reporting, KPI tracking,",
                "dashboard design, SQL queries, and business intelligence.",
                "",
                "What data would you like to explore?",
            ],
        },
        "general": {
            "__default__": [
                "I'm your Revenue OS assistant. I can help with:",
                "  \u2022 Sales strategy and pipeline management",
                "  \u2022 Marketing campaigns and analytics",
                "  \u2022 Customer support and success",
                "  \u2022 Product management and roadmap",
                "  \u2022 Data analysis and reporting",
                "",
                "How can I help you grow your revenue today?",
            ],
        },
    }

    def __init__(self, persona, conversation=None):
        self.persona = persona
        self.conversation = conversation

    def respond(self, query):
        pn = self.persona.name
        ql = query.lower()
        lines = [f"Thank you for reaching out to the {self.persona.display_name} team."]

        persona_map = self.RESPONSES.get(pn, self.RESPONSES["general"])
        matched = False
        for pattern, response_lines in persona_map.items():
            if pattern == "__default__":
                continue
            if any(kw in ql for kw in pattern.split("|")):
                lines.extend([""] + list(response_lines))
                matched = True
                break

        if not matched:
            lines.extend([""] + list(persona_map.get("__default__", [])))

        return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────
# API Client (Railway connection)
# ──────────────────────────────────────────────────────────────────────


class APIClient:
    """HTTP client for the Revenue OS Railway API. Falls back gracefully."""

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.environ.get("REVENUE_OS_API_KEY", "")
        self.base_url = (base_url or os.environ.get("REVENUE_OS_API_URL", "")).rstrip("/")
        self.available = False
        self._conv_id = None
        self._check_connection()

    def _check_connection(self):
        if not self.base_url:
            return
        try:
            import urllib.request
            import urllib.error
            req = urllib.request.Request(f"{self.base_url}/health", method="GET")
            if self.api_key:
                req.add_header("Authorization", f"Bearer {self.api_key}")
            try:
                with urllib.request.urlopen(req, timeout=5) as resp:
                    self.available = resp.status == 200
            except urllib.error.HTTPError:
                self.available = True  # 404 means server is alive
            except urllib.error.URLError:
                self.available = False
        except Exception:
            self.available = False

    def chat(self, query, persona_name, history=None):
        if not self.available or not self.base_url:
            return None, False
        try:
            import urllib.request
            payload = {"message": query, "persona": persona_name}
            if history:
                payload["history"] = history
            if not self._conv_id:
                self._conv_id = str(uuid.uuid4())
            payload["conversation_id"] = self._conv_id

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=data,
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            if self.api_key:
                req.add_header("Authorization", f"Bearer {self.api_key}")

            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = (result.get("response") or
                        result.get("message") or
                        result.get("text", ""))
                return text, True
        except Exception as e:
            return f"[API Error: {e}]", False

    def status_string(self):
        if not self.base_url:
            return c("Standalone Mode", Style.ITALIC, Style.GRAY)
        if self.available:
            return c(f"Connected to {self.base_url}", Style.GREEN)
        return c(f"API Unreachable ({self.base_url}) \u2014 using fallback", Style.YELLOW)


# ──────────────────────────────────────────────────────────────────────
# Main CLI Application
# ──────────────────────────────────────────────────────────────────────


class RevenueOSCLI:
    """Interactive chat CLI with persona routing, history, and color output."""

    def __init__(self, api_key=None, base_url=None, forced_persona=None):
        self.forced_persona = forced_persona
        self.router = PersonaRouter()
        self.api_client = APIClient(api_key=api_key, base_url=base_url)
        script_dir = (os.path.dirname(os.path.abspath(__file__))
                      if '__file__' in dir() else os.getcwd())
        self.conversation = Conversation(
            history_file=os.path.join(script_dir, ".revenue_os_history.json")
        )
        self.current_persona = None
        self.running = True

    def _resolve_persona(self, query):
        if self.forced_persona:
            return self.router.route(query, forced_persona=self.forced_persona)
        return self.router.route(query)

    def _get_response(self, query, persona):
        history = self.conversation.get_messages()
        if self.api_client.available and self.api_client.base_url:
            text, ok = self.api_client.chat(query, persona.name, history)
            if ok and text:
                return text
        return StandaloneAgent(persona, self.conversation).respond(query)

    def process_query(self, query):
        query = query.strip()
        if not query:
            return
        persona = self._resolve_persona(query)
        self.current_persona = persona
        self.conversation.add_entry("user", query, persona.name)

        # Show routing info
        print(c(
            f"  \u26a1 Routed to: {persona.display_name} ({persona.name})",
            Style.BOLD, Style.BRIGHT_MAGENTA,
        ))
        print(c(f"     {persona.description}", Style.ITALIC, Style.GRAY))
        print()

        # Get and display response
        response = self._get_response(query, persona)
        self.conversation.add_entry("assistant", response, persona.name)

        print(section_header(f"Response from {persona.display_name}"))
        print(response)
        print(c(
            f"\n\u2500\u2500 Revenue OS \u2022 {persona.display_name}",
            Style.DIM, Style.GRAY,
        ))
        print()

        self.conversation.save()

    def show_welcome(self):
        banner = (
            f"\n"
            f"{c('=' * 60, Style.DIM, Style.GRAY)}\n"
            f"{c('  R E V E N U E   O S   -   I N T E L L I G E N T   C L I', Style.BOLD, Style.BRIGHT_CYAN)}\n"
            f"{c('  Revenue Operations Command Center', Style.ITALIC, Style.GRAY)}\n"
            f"{c('=' * 60, Style.DIM, Style.GRAY)}\n"
            f"  {c('Type any query \u2014 I\'ll route it to the right agent!', Style.GRAY)}\n"
            f"  {c('Commands:  /quit  /clear  /personas  /history  /help  /status', Style.GRAY)}\n"
        )
        print(banner)
        print(f"  {self.api_client.status_string()}")
        if self.forced_persona:
            p = self.router.route("", forced_persona=self.forced_persona)
            print(c(f"  \ud83d\udd12 Persona locked: {p.display_name}", Style.YELLOW))
        print()

    def _handle_command(self, cmd):
        cmd = cmd.strip().lower()

        if cmd == "/quit":
            print(c("\nThank you for using Revenue OS. Goodbye! \ud83d\udc4b",
                    Style.BRIGHT_CYAN, Style.BOLD))
            self.conversation.save()
            self.running = False
            return True

        if cmd == "/clear":
            self.conversation.clear()
            print(c("\n\u2705 Conversation history cleared.", Style.GREEN))
            return True

        if cmd == "/personas":
            print(section_header("Available Agent Personas"))
            for i, (name, dn, desc) in enumerate(self.router.list_personas(), 1):
                active = ""
                if self.current_persona and self.current_persona.name == name:
                    active = c(" \u25c4 ACTIVE", Style.BRIGHT_GREEN, Style.BOLD)
                print(f"  {c(f'{i}.', Style.BRIGHT_YELLOW)} "
                      f"{c(dn, Style.BOLD, Style.BRIGHT_WHITE)} "
                      f"({c(name, Style.CYAN)}){active}")
                print(f"     {c(desc, Style.GRAY, Style.ITALIC)}")
                print()
            return True

        if cmd == "/history":
            if not self.conversation.history:
                print(c("\n  No conversation history yet.", Style.ITALIC, Style.GRAY))
                return True
            print(section_header(
                f"Conversation History ({self.conversation.count_turns()} turns)"
            ))
            for i, entry in enumerate(self.conversation.history):
                role = entry['role']
                content = entry['content']
                persona = entry.get('persona', '')
                if role == 'user':
                    label = c(f"  [{i+1}] You", Style.BOLD, Style.BRIGHT_GREEN)
                    if persona:
                        label += c(f" (\u2192 {persona})", Style.ITALIC, Style.GRAY)
                    print(label)
                    dc = content[:200] + "..." if len(content) > 200 else content
                    print(f"       {c(dc, Style.GRAY)}")
                else:
                    label = c(f"       {persona or 'Assistant'}", Style.DIM, Style.BLUE)
                    print(label)
                    dc = content[:200] + "..." if len(content) > 200 else content
                    print(f"       {c(dc, Style.GRAY)}")
                print()
            return True

        if cmd == "/status":
            print(section_header("Session Status"))
            print(f"  {c('Connection:', Style.BOLD)} {self.api_client.status_string()}")
            print(f"  {c('Persona mode:', Style.BOLD)} ", end="")
            if self.forced_persona:
                p = self.router.route("", forced_persona=self.forced_persona)
                print(c(f"Locked to {p.display_name}", Style.YELLOW))
            else:
                print(c("Auto-route (based on query)", Style.GREEN))
            print(f"  {c('Current persona:', Style.BOLD)} ", end="")
            if self.current_persona:
                print(c(self.current_persona.display_name, Style.BRIGHT_CYAN))
            else:
                print(c("None (send a query first)", Style.GRAY))
            print(f"  {c('History turns:', Style.BOLD)} {self.conversation.count_turns()}")
            print(f"  {c('API key set:', Style.BOLD)} "
                  f"{c('Yes' if self.api_client.api_key else 'No',
                       Style.GREEN if self.api_client.api_key else Style.YELLOW)}")
            print()
            return True

        if cmd == "/help":
            print(f"""
{c('Available Commands:', Style.BOLD, Style.BRIGHT_CYAN)}
  {c('/quit', Style.BRIGHT_YELLOW)}          Exit the CLI
  {c('/clear', Style.BRIGHT_YELLOW)}         Clear conversation history
  {c('/personas', Style.BRIGHT_YELLOW)}      List available agent personas
  {c('/history', Style.BRIGHT_YELLOW)}       Show conversation history
  {c('/help', Style.BRIGHT_YELLOW)}          Show this help message
  {c('/status', Style.BRIGHT_YELLOW)}        Show connection & session status

{c('Flags:', Style.BOLD, Style.BRIGHT_CYAN)}
  --persona <name>    Force persona: sales, marketing, support, product, analytics
  --api-key <key>     API key for Railway API connection
  --url <url>         Custom Railway API server URL

{c('Examples:', Style.BOLD, Style.BRIGHT_CYAN)}
  python cli.py                           Interactive session
  python cli.py "What's in my pipeline?"  Single query
  python cli.py --persona sales           Start with sales persona locked
  python cli.py --api-key sk-xxx --url https://api.example.com
""")
            return True

        if cmd.startswith("/"):
            print(c(f"\n\u274c Unknown command: {cmd}", Style.BRIGHT_RED))
            print(c("  Type /help for available commands.", Style.GRAY))
            return True

        return False

    def interactive_loop(self):
        self.show_welcome()
        while self.running:
            try:
                query = input(
                    f" {c('RevOS', Style.BRIGHT_CYAN, Style.BOLD)} "
                    f"{c('\u276f', Style.BRIGHT_MAGENTA)} "
                )
                if not query:
                    continue
                if query.startswith("/"):
                    self._handle_command(query)
                    continue
                print()
                self.process_query(query)
            except KeyboardInterrupt:
                print(c("\n\n  Use /quit to exit.", Style.YELLOW))
                try:
                    input(c("  Press Enter to continue...", Style.DIM, Style.GRAY))
                except (KeyboardInterrupt, EOFError):
                    print()
                    self._handle_command("/quit")
            except EOFError:
                print()
                self._handle_command("/quit")

        self.conversation.save()

    def single_query(self, query):
        self.show_welcome()
        print(c(f"  Query: {query}", Style.BOLD, Style.BRIGHT_GREEN))
        print()
        self.process_query(query)


# ──────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Revenue OS CLI \u2014 Intelligent chat for Revenue Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py                          Interactive session\n"
            "  python cli.py --persona sales          Force sales persona\n"
            "  python cli.py --api-key sk-abc123      API key auth\n"
            "  python cli.py --url https://api.example.com  Custom URL\n"
            "  python cli.py \"What's in my pipeline?\"  Single query\n"
        ),
    )
    parser.add_argument("query", nargs="?", default=None,
                        help="Single query (omit for interactive mode)")
    parser.add_argument("--persona", type=str, default=None,
                        help="Force persona: sales, marketing, support, product, analytics")
    parser.add_argument("--api-key", type=str, default=None,
                        help="API key for Railway API")
    parser.add_argument("--url", type=str, default=None,
                        help="Custom Railway API URL")
    parser.add_argument("--version", action="store_true",
                        help="Show version information")

    args = parser.parse_args()

    if args.version:
        print("Revenue OS CLI v1.0.0")
        print(f"Python {sys.version}")
        return

    if args.persona:
        valid = [p.name for p in PERSONAS]
        if args.persona.lower() not in valid:
            print(c(f"\u274c Invalid persona: '{args.persona}'", Style.BRIGHT_RED))
            print(f"   Valid personas: {', '.join(valid)}")
            sys.exit(1)

    cli = RevenueOSCLI(
        api_key=args.api_key,
        base_url=args.url,
        forced_persona=args.persona,
    )

    try:
        if args.query:
            cli.single_query(args.query)
        else:
            cli.interactive_loop()
    except Exception as e:
        print(c(f"\n\u274c Unexpected error: {e}", Style.BRIGHT_RED))
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
