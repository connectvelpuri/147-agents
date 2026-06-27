
"""
Account Intelligence Engine - Analytics Module
Win-rate analysis, opportunity scoring, pipeline modeling
"""
import json, sqlite3, csv
from datetime import datetime
from pathlib import Path

class Analytics:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def opportunity_score(self, account):
        """Calculate opportunity score (1-100) based on intelligence signals"""
        score = 50  # baseline
        
        # SAP maturity signals
        if "S/4HANA" in account.get("sap_erp", ""):
            score += 15  # Already on SAP - upsell opportunity
        if "RISE" in account.get("sap_erp", ""):
            score += 10  # Managed service - deepen relationship
        if "migration" in account.get("sap_erp", "").lower():
            score += 20  # Migration in progress - consulting need
        
        # Revenue size
        rev_str = account.get("est_revenue_cr", "0")
        rev_num = 0
        import re as _re
        nums = _re.findall(r'[\d,]+', rev_str.replace("₹", ""))
        if nums:
            rev_num = float(nums[0].replace(",", ""))
        
        if rev_num > 10000:
            score += 15
        elif rev_num > 1000:
            score += 10
        elif rev_num > 500:
            score += 5
        
        # Pain points
        pain_count = len(account.get("pain_points", []))
        score += min(pain_count * 2, 10)
        
        # Digital transformation signals
        signal_count = len(account.get("key_digital_signals", []))
        score += min(signal_count * 3, 15)
        
        return min(score, 100)
    
    def generate_report(self, accounts_data):
        """Generate analytics report"""
        rows = []
        for acct in accounts_data:
            score = self.opportunity_score(acct)
            rows.append({
                "company": acct["company"],
                "sector": acct.get("sector", ""),
                "revenue": acct.get("est_revenue_cr", ""),
                "sap_erp": acct.get("sap_erp", ""),
                "opportunity_score": score,
                "priority": "HIGH" if score > 70 else "MEDIUM" if score > 50 else "LOW"
            })
        
        rows.sort(key=lambda r: r["opportunity_score"], reverse=True)
        return rows

if __name__ == "__main__":
    print("Analytics module ready")
