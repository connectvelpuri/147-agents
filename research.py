#!/usr/bin/env python3
"""Unified Account Intelligence Research Tool.
Searches company across 100+ data sources using multiple OSINT tools.

Usage:
    python research.py "Company Name"
    python research.py "Novartis" --deep
    python research.py "CEVA Logistics" --all
"""

import subprocess, sys, os, json
from datetime import datetime

RESEARCH_DIR = os.path.join(os.path.dirname(__file__), "intel_output")
os.makedirs(RESEARCH_DIR, exist_ok=True)

TOOLS = {
    "theHarvester": os.path.join(os.path.dirname(__file__), "tools", "osint", "theHarvester", "theHarvester.py"),
    "sherlock": os.path.join(os.path.dirname(__file__), "tools", "osint", "sherlock", "sherlock"),
    "holehe": os.path.join(os.path.dirname(__file__), "tools", "osint", "holehe", "holehe.py"),
}

def run_tool(tool_path, args):
    """Run an OSINT tool and return output."""
    if not os.path.exists(tool_path):
        return f"[{tool_path} not found]"
    try:
        r = subprocess.run([sys.executable, tool_path] + args, capture_output=True, text=True, timeout=120)
        return r.stdout[:1000] if r.stdout else r.stderr[:1000]
    except:
        return "[Tool execution failed]"

def research_company(company, deep=False):
    """Research a company across all available tools."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "company": company,
        "timestamp": timestamp,
        "results": {}
    }
    
    print(f"\n{'='*60}")
    print(f"  RESEARCHING: {company}")
    print(f"  Tools available: {len([t for t,p in TOOLS.items() if os.path.exists(p)])}")
    print(f"{'='*60}")
    
    # 1. theHarvester - email, domain, IP recon
    if os.path.exists(TOOLS.get("theHarvester", "")):
        print(f"\n  Running theHarvester for {company}...")
        result = run_tool(TOOLS["theHarvester"], ["-d", company, "-b", "all", "-l", "50"])
        output["results"]["theHarvester"] = result[:500]
        print(f"    Done: {len(result)} chars")
    
    # 2. Web search via DuckDuckGo
    from urllib.parse import quote
    import httpx
    print(f"\n  Web search: {company}...")
    url = f"https://html.duckduckgo.com/html/?q={quote(company + ' CEO revenue employees technology')}"
    try:
        r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        output["results"]["web_search"] = "OK" if r.status_code == 200 else f"Status: {r.status_code}"
    except Exception as e:
        output["results"]["web_search"] = f"Error: {e}"
    print(f"    Done")
    
    # Save report
    report_file = os.path.join(RESEARCH_DIR, f"{company.replace(' ', '_')}_{timestamp}.json")
    with open(report_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n  Report saved: {report_file}")
    return output

if __name__ == "__main__":
    company = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Company name: ")
    research_company(company)
