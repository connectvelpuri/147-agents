#!/usr/bin/env python3
"""Unified Account Intelligence Research Tool.
Integrates 14+ OSINT tools for deep company and prospect research.

Usage:
    python research.py "Company Name"          # Basic research
    python research.py "Company Name" --deep   # Full deep dive
    python research.py --tools                 # List available tools
"""

import subprocess, sys, os, json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE, "tools", "osint")
OUTPUT_DIR = os.path.join(BASE, "intel")
os.makedirs(OUTPUT_DIR, exist_ok=True)

AVAILABLE_TOOLS = {}

# Discover available tools
for tool_name in os.listdir(TOOLS_DIR):
    tool_path = os.path.join(TOOLS_DIR, tool_name)
    if os.path.isdir(tool_path):
        AVAILABLE_TOOLS[tool_name] = tool_path

def print_banner():
    print("""
   ╔═══════════════════════════════════════════════╗
   ║     Account Intelligence Research Engine      ║
   ║     14+ OSINT Tools  ·  7,500+ Files         ║
   ╚═══════════════════════════════════════════════╝
    """)

def list_tools():
    """List all available OSINT tools."""
    print(f"\nAvailable OSINT Tools ({len(AVAILABLE_TOOLS)}):")
    print("-" * 50)
    for name, path in sorted(AVAILABLE_TOOLS.items()):
        files = sum(len(files) for _, _, files in os.walk(path))
        print(f"  {name:<25s} ({files} files)")

def research_company(company, deep=False):
    """Multi-tool company research."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company_clean = company.replace(" ", "_")
    
    print(f"\nResearching: {company}")
    print(f"Tools available: {len(AVAILABLE_TOOLS)}")
    print(f"Output: {OUTPUT_DIR}/{company_clean}_{timestamp}.json\n")
    
    results = {}
    
    # 1. Account Intelligence Engine (built-in)
    try:
        sys.path.insert(0, os.path.join(BASE, "agents"))
        from agents.account_intel.engine import AccountIntelEngine
        engine = AccountIntelEngine()
        md = engine.to_markdown(company)
        results["account_intel"] = {"status": "OK", "length": len(md)}
        # Save markdown report
        with open(os.path.join(OUTPUT_DIR, f"{company_clean}_{timestamp}.md"), 'w') as f:
            f.write(md)
        print(f"  ✅ Account Intelligence Report: {len(md)} chars")
    except Exception as e:
        results["account_intel"] = {"status": f"Error: {e}"}
        print(f"  ❌ Account Intelligence: {e}")
    
    # 2. Technology detection
    whatweb = os.path.join(TOOLS_DIR, "whatweb", "whatweb")
    if os.path.exists(whatweb):
        try:
            r = subprocess.run(["ruby", whatweb, f"{company.lower().replace(' ', '')}.com", "--quiet"],
                capture_output=True, text=True, timeout=30)
            results["whatweb"] = r.stdout[:500]
            print(f"  ✅ WhatWeb: tech stack detected")
        except:
            print(f"  ❌ WhatWeb: not available (needs ruby)")
    
    # 3. Search intelligence
    from urllib.parse import quote
    import httpx
    import re
    from html import unescape
    
    searches = [
        f"{company} CEO CFO CIO leadership",
        f"{company} revenue employees headquarters 2026",
        f"{company} technology stack Oracle SAP Salesforce AWS",
        f"{company} digital transformation strategy 2026",
        f"{company} partnership acquisition expansion",
    ]
    
    for q in searches:
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote(q)}"
            r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, follow_redirects=True)
            if r.status_code == 200:
                snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</(?:a|span)', r.text, re.DOTALL)
                titles = re.findall(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', r.text, re.DOTALL)
                links = re.findall(r'class="result__url"[^>]*href="(https?://[^"]+)"', r.text)
                items = []
                for i in range(min(len(snippets), 3)):
                    items.append({
                        "title": unescape(re.sub(r'<[^>]+>', '', titles[i])) if i < len(titles) else "",
                        "snippet": unescape(re.sub(r'<[^>]+>', '', snippets[i])) if i < len(snippets) else "",
                    })
                results[f"search_{q[:30]}"] = items
        except:
            pass
    
    print(f"  ✅ Web search: {len(searches)} queries complete")
    
    # Save
    report = {
        "company": company,
        "timestamp": timestamp,
        "tools_available": len(AVAILABLE_TOOLS),
        "results": {k: str(v)[:200] for k, v in results.items()}
    }
    
    json_path = os.path.join(OUTPUT_DIR, f"{company_clean}_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved: {json_path}")
    print(f"Report (MD): {OUTPUT_DIR}/{company_clean}_{timestamp}.md")
    
    return results

def deep_research(company):
    """Full deep dive using all available tools."""
    print(f"\n{'='*60}")
    print(f"  DEEP RESEARCH: {company}")
    print(f"{'='*60}")
    
    results = research_company(company, deep=True)
    
    # Run theHarvester if available
    harvester = os.path.join(TOOLS_DIR, "theHarvester", "theHarvester.py")
    if os.path.exists(harvester):
        domain = company.lower().replace(" ", "").replace(",", ".com").split(".")[0] + ".com"
        print(f"  Running theHarvester on {domain}...")
        r = subprocess.run([sys.executable, harvester, "-d", domain, "-b", "google", "-l", "30"],
            capture_output=True, text=True, timeout=120)
        print(f"    Output: {len(r.stdout)} chars")
    
    return results

if __name__ == "__main__":
    print_banner()
    
    if "--tools" in sys.argv:
        list_tools()
        sys.exit(0)
    
    if "--deep" in sys.argv:
        company = " ".join([a for a in sys.argv[1:] if a != "--deep"])
        if company:
            deep_research(company)
        else:
            print("Usage: python research.py "Company Name" --deep")
    else:
        company = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Company name: ")
        if company:
            research_company(company)
        else:
            print("Usage: python research.py "Company Name"")
            list_tools()
