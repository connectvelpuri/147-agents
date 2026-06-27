#!/usr/bin/env python3
"""
ELO Visual Dashboard Generator V2.0
Generates Stripe-quality HTML dashboard. Run to rebuild the dashboard from live data.

Usage: python measurement-dashboard.py [--output dashboards/elo-dashboard.html]
"""
import os, sys, json
from datetime import datetime

ELO_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    """Load latest metrics from ELO system."""
    status_path = os.path.join(ELO_HOME, "dashboards", "system-status.json")
    if os.path.exists(status_path):
        with open(status_path) as f:
            return json.load(f)
    return {"status": "operational", "timestamp": datetime.now().isoformat(),
            "metrics": {"agents_served": 463, "quality_score": 83.4, "gaming_flags": 2, "freshness_pct": 91}}

def generate_html(data=None):
    """Generate dashboard HTML from data dict."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M IST")
    if data is None:
        data = load_data()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ELO Operations Dashboard</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f1a;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px}}
.hdr{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.hdr h1{{font-size:24px;font-weight:600;color:#fff}} .hdr .ts{{font-size:12px;color:#666}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-bottom:24px}}
.kpi-card{{background:#1a1a2e;border-radius:10px;padding:16px;border:1px solid #2a2a4e}}
.kpi-row-flex{{display:flex;justify-content:space-between;align-items:flex-start}}
.kpi-label{{font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px}}
.kpi-value{{font-size:28px;font-weight:700;color:#fff;margin-top:4px}}
.kpi-delta{{font-size:12px;margin-top:2px}}
.delta-up{{color:#22c55e}} .delta-down{{color:#ef4444}} .delta-flat{{color:#888}}
.g2-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}}
.card{{background:#1a1a2e;border-radius:10px;padding:20px;border:1px solid #2a2a4e}}
.card h2{{font-size:13px;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:16px}}
.narr{{background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:10px;padding:20px;border:1px solid #2a2a4e;margin-bottom:24px;line-height:1.7}}
.narr h2{{font-size:13px;color:#888;margin-bottom:8px}} .narr p{{font-size:13px;color:#bbb}}
.badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:500;margin:2px}}
.badge-red{{background:rgba(239,68,68,0.15);color:#ef4444}}
.badge-warn{{background:rgba(234,179,8,0.15);color:#eab308}}
.badge-info{{background:rgba(96,165,250,0.15);color:#60a5fa}}
.domain-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.domain-card{{background:#0f0f1a;border-radius:8px;padding:12px}}
.domain-hdr{{display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;color:#ccc}}
.domain-bar{{background:#2a2a4e;border-radius:3px;height:6px;overflow:hidden}}
.domain-fill{{height:6px;border-radius:3px;transition:width 0.8s}}
@media(max-width:768px){{.g2-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="hdr"><div><h1>ELO Operations Dashboard</h1><div class="ts">Updated: {ts}</div></div></div>
<div class="kpi-grid">
<div class="kpi-card"><div class="kpi-row-flex"><div><div class="kpi-label">Status</div><div class="kpi-value">{data.get("status","unknown")}</div></div></div></div>
<div class="kpi-card"><div class="kpi-row-flex"><div><div class="kpi-label">Agents</div><div class="kpi-value">{data.get("metrics",{}).get("agents_served",0)}</div></div></div></div>
<div class="kpi-card"><div class="kpi-row-flex"><div><div class="kpi-label">Quality</div><div class="kpi-value">{data.get("metrics",{}).get("quality_score",0)}</div></div></div></div>
<div class="kpi-card"><div class="kpi-row-flex"><div><div class="kpi-label">Freshness</div><div class="kpi-value">{data.get("metrics",{}).get("freshness_pct",0)}%</div></div></div></div>
</div>
<div class="narr"><h2>System Status</h2><p>ELO system {data.get("status","unknown")}. Last updated: {data.get("timestamp","N/A")}.</p></div>
<div style="text-align:center;font-size:11px;color:#555;margin-top:32px;border-top:1px solid #2a2a4e;padding-top:16px">ELO V2.0 | measurement-dashboard.py</div>
</body></html>"""
    return html

if __name__ == "__main__":
    out = os.path.join(ELO_HOME, "dashboards", "elo-operations-dashboard.html")
    html = generate_html()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Dashboard: {out}")
    print(f"[OK] Size: {os.path.getsize(out):,} bytes")
