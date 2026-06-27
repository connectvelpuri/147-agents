#!/usr/bin/env python3
"""
ELO Auto-Onboarding Script
Detects new operational agents and maps them to ELO Tier 2 leads.
Run this periodically or when new agents are created.

Usage: python3 elo-onboard-new-agents.py
"""

import os
import json
import sys
from datetime import datetime

# Paths
V4_ROLES = os.path.expanduser("~/sovereign_crm_vault/agent-org/v4-enterprise/roles")
ELO_BASE = os.path.expanduser("~/sovereign_crm_vault/agent-org/v4-enterprise/elo-system")
MAPPING_FILE = os.path.join(ELO_BASE, "mappings", "agent-to-tier2-mapping.json")
ONBOARDING_LOG = os.path.join(ELO_BASE, "onboarding", "onboarding-log.json")

# Domain to Tier 2 Lead mapping
DOMAIN_TIER2_MAP = {
    "architecture": "ELO-T2-03",
    "engineering": "ELO-T2-02",
    "qa": "ELO-T2-04",
    "platform-ops": "ELO-T2-05",
    "security": "ELO-T2-16",
    "customer-success": "ELO-T2-20",
    "data-ai": "ELO-T2-14",
    "product-design": "ELO-T2-12",
    "executive": "ELO-T2-17",
    "pmo": "ELO-T2-18",
    "product-crm": "ELO-T2-07",
    "product-erp": "ELO-T2-08",
    "product-hr": "ELO-T2-09",
    "product-fin": "ELO-T2-10",
}

def get_tier2_lead(agent_data, domain_dir):
    title = agent_data.get("title", agent_data.get("role", "")).lower()
    
    if domain_dir.startswith("product-"):
        if any(x in title for x in ["frontend", "fe", "ui developer", "mob"]):
            return "ELO-T2-01"
        elif any(x in title for x in ["backend", "be ", "swe", "senior engineer", "software engineer"]):
            return "ELO-T2-02"
        elif any(x in title for x in ["architect", "sa "]):
            return "ELO-T2-03"
        elif any(x in title for x in ["qa", "test", "quality"]):
            return "ELO-T2-04"
        elif any(x in title for x in ["devops", "doe", "dol", "release"]):
            return "ELO-T2-05"
        elif any(x in title for x in ["sre", "re "]):
            return "ELO-T2-06"
        elif any(x in title for x in ["product manager", "pm-", "ba"]):
            return "ELO-T2-12"
        elif any(x in title for x in ["design", "uid", "uxd"]):
            return "ELO-T2-13"
        elif any(x in title for x in ["data", "da-", "dsl"]):
            return "ELO-T2-14"
        elif any(x in title for x in ["ai", "aie", "ml"]):
            return "ELO-T2-15"
        elif any(x in title for x in ["security", "sec"]):
            return "ELO-T2-16"
        elif any(x in title for x in ["engineering manager", "em-"]):
            return "ELO-T2-19"
        else:
            product_map = {"crm": "ELO-T2-07", "erp": "ELO-T2-08", "hr": "ELO-T2-09", "fin": "ELO-T2-10"}
            product = domain_dir.replace("product-", "")
            return product_map.get(product, "ELO-T2-07")
    
    return DOMAIN_TIER2_MAP.get(domain_dir, "ELO-T2-12")

def scan_for_new_agents():
    """Scan all roles/ directories for agents not yet in ELO mapping."""
    # Load existing mapping
    existing_mapped = set()
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        for tier2_id, agents in mapping.items():
            for agent in agents:
                existing_mapped.add(agent["agent_id"])
    
    # Scan all role files
    new_agents = []
    for root, dirs, files in os.walk(V4_ROLES):
        for fname in files:
            if fname.endswith(".json") and not fname.startswith("."):
                path = os.path.join(root, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    agent_id = data.get("id", data.get("agent_id", fname.replace(".json", "")))
                    if agent_id not in existing_mapped:
                        rel_path = os.path.relpath(path, V4_ROLES)
                        domain_dir = rel_path.split(os.sep)[0] if os.sep in rel_path else "unknown"
                        tier2_lead = get_tier2_lead(data, domain_dir)
                        new_agents.append({
                            "agent_id": agent_id,
                            "title": data.get("title", data.get("role", "Unknown")),
                            "domain": domain_dir,
                            "tier2_lead": tier2_lead
                        })
                except Exception as e:
                    pass
    
    return new_agents

def onboard_agents(new_agents):
    """Add new agents to the ELO mapping."""
    if not new_agents:
        print("No new agents to onboard.")
        return
    
    # Load existing mapping
    mapping = {}
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    
    # Add new agents
    onboarded = []
    for agent in new_agents:
        tier2 = agent["tier2_lead"]
        if tier2 not in mapping:
            mapping[tier2] = []
        mapping[tier2].append({
            "agent_id": agent["agent_id"],
            "title": agent["title"],
            "domain": agent["domain"]
        })
        onboarded.append(agent)
        print(f"  ONBOARDED: {agent['agent_id']} -> {tier2} ({agent['title']})")
    
    # Save updated mapping
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    # Log onboarding
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agents_onboarded": len(onboarded),
        "agents": onboarded
    }
    
    log = []
    if os.path.exists(ONBOARDING_LOG):
        with open(ONBOARDING_LOG, "r", encoding="utf-8") as f:
            log = json.load(f)
    log.append(log_entry)
    with open(ONBOARDING_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    
    print(f"\nOnboarded {len(onboarded)} new agents into ELO.")

def main():
    print("=" * 60)
    print("ELO AUTO-ONBOARDING — New Agent Detection")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    new_agents = scan_for_new_agents()
    
    if new_agents:
        print(f"\nFound {len(new_agents)} new agents to onboard:")
        print("-" * 60)
        onboard_agents(new_agents)
    else:
        print("\nAll agents are already mapped in ELO.")
    
    # Print current mapping stats
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        total = sum(len(v) for v in mapping.values())
        print(f"\nCurrent ELO mapping: {total} agents across {len(mapping)} Tier 2 leads")

if __name__ == "__main__":
    main()
