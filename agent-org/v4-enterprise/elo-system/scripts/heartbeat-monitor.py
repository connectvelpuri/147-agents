#!/usr/bin/env python3
"""
ELO Heartbeat Monitor
Checks agent health, triggers alerts on missed heartbeats, manages failover.

Run: Every 5 minutes (cron)
"""
import json
import os
from datetime import datetime, timedelta

ELO_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HB_LOG = os.path.join(ELO_HOME, "logs", "heartbeats")
ALERT_LOG = os.path.join(ELO_HOME, "logs", "alerts")

HEARTBEAT_SLA = {
    "T1": {"expected_interval_min": 15, "missed_threshold": 2},
    "T2": {"expected_interval_min": 10, "missed_threshold": 3},
    "T3": {"expected_interval_min": 5,  "missed_threshold": 5},
}

def check_heartbeats():
    """Check all agents' heartbeats against SLA."""
    now = datetime.now()
    alerts = []
    healthy = 0
    warning = 0
    critical = 0
    
    hb_dir = os.path.join(ELO_HOME, "logs", "heartbeats")
    if not os.path.exists(hb_dir):
        return {"healthy": 0, "warning": 0, "critical": 0, "alerts": ["No heartbeat log directory"]}
    
    for fname in os.listdir(hb_dir):
        if not fname.endswith(".json"):
            continue
        agent_id = fname.replace(".json", "")
        tier = agent_id.split("-")[1] if "-" in agent_id else "T3"
        
        try:
            with open(os.path.join(hb_dir, fname)) as f:
                hb = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            continue
        
        last_seen = datetime.fromisoformat(hb.get("timestamp", now.isoformat()))
        elapsed = (now - last_seen).total_seconds() / 60
        
        sla = HEARTBEAT_SLA.get(tier, {"expected_interval_min": 5, "missed_threshold": 5})
        expected_min = sla["expected_interval_min"]
        missed = int(elapsed / expected_min)
        
        if missed >= sla["missed_threshold"]:
            critical += 1
            alerts.append({
                "severity": "CRITICAL",
                "agent": agent_id,
                "tier": tier,
                "message": f"Agent {agent_id} missed {missed} heartbeats ({elapsed:.0f}min since last)"
            })
        elif missed >= 2:
            warning += 1
            alerts.append({
                "severity": "WARNING",
                "agent": agent_id,
                "message": f"Agent {agent_id} missed {missed} heartbeats"
            })
        else:
            healthy += 1
    
    # Log alerts
    if alerts:
        os.makedirs(ALERT_LOG, exist_ok=True)
        alert_file = os.path.join(ALERT_LOG, f"heartbeat-alerts-{now.strftime('%Y-%m-%d-%H')}.json")
        with open(alert_file, "a") as f:
            for a in alerts:
                f.write(json.dumps(a) + "\n")
    
    return {"healthy": healthy, "warning": warning, "critical": critical, "alerts": alerts}

def simulate_heartbeat(agent_id, tier, status="operational"):
    """Register a heartbeat from an agent."""
    hb = {
        "agent_id": agent_id,
        "tier": tier,
        "status": status,
        "timestamp": datetime.now().isoformat(),
    }
    os.makedirs(HB_LOG, exist_ok=True)
    with open(os.path.join(HB_LOG, f"{agent_id}.json"), "w") as f:
        json.dump(hb, f)
    return hb

if __name__ == "__main__":
    # Simulate some heartbeats then check
    for i in range(5):
        simulate_heartbeat(f"ELO-T3-AGENT-{i:02d}", "T3", "operational")
    
    status = check_heartbeats()
    print(f"Heartbeat Status: {status['healthy']} healthy, {status['warning']} warning, {status['critical']} critical")
    for a in status["alerts"][:3]:
        print(f"  [{a['severity']}] {a['message']}")
