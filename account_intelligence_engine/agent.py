
#!/usr/bin/env python3
"""
Account Intelligence Engine - Main Agent
Open-source intelligence platform using SQLite + Python
No proprietary APIs required.
"""
import sys, json, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from modules.database import init_db, import_research, query_all_accounts, get_conn
from modules.rag import IntelRAG
from modules.analytics import Analytics

class AccountIntelligenceAgent:
    def __init__(self):
        self.db_initialized = False
        self.rag = IntelRAG()
        self.analytics = None
    
    def initialize(self):
        """Initialize database and load existing data"""
        init_db()
        self.db_initialized = True
        self.analytics = Analytics(str(Path(__file__).parent / "data" / "intel.db"))
        print("✓ Database initialized")
        
        # Load existing accounts
        accounts = query_all_accounts()
        if accounts:
            print(f"✓ Loaded {len(accounts)} existing accounts")
        return self
    
    def load_research(self, json_file):
        """Load research JSON data into database"""
        with open(json_file, "r") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for item in data:
                import_research(item)
            print(f"✓ Imported {len(data)} companies from {json_file}")
        else:
            import_research(data)
            print(f"✓ Imported {data.get('company', 'unknown')}")
        
        # Rebuild RAG
        from modules import database as db_mod
        self.rag.load_from_database(db_mod)
        return self
    
    def search_intel(self, query, top_k=3):
        """Search intelligence via RAG"""
        return self.rag.search(query, top_k)
    
    def analyze_pipeline(self):
        """Analyze opportunity pipeline"""
        accounts = query_all_accounts()
        if not accounts:
            return []
        
        # Get full account data from research_json
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT company, research_json FROM accounts")
        full_data = []
        for row in cur.fetchall():
            try:
                data = json.loads(row[1])
                full_data.append(data)
            except:
                full_data.append({"company": row[0]})
        
        return self.analytics.generate_report(full_data)
    
    def export_report(self, format="md"):
        """Export full intelligence report"""
        accounts = query_all_accounts()
        report = f"# Account Intelligence Engine Report\n"
        report += f"Generated: {__import__('datetime').datetime.now()}\n\n"
        
        pipeline = self.analyze_pipeline()
        
        report += "## Pipeline Priority\n\n"
        report += "| Company | Sector | Score | Priority |\n"
        report += "|---------|--------|-------|----------|\n"
        for item in pipeline:
            report += f"| {item['company']} | {item['sector']} | {item['opportunity_score']}/100 | {item['priority']} |\n"
        
        report += "\n## Account Details\n\n"
        for acct in accounts:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("SELECT research_json FROM accounts WHERE company=?", (acct["company"],))
            row = cur.fetchone()
            if row:
                data = json.loads(row[0])
                report += f"### {data.get('company', acct['company'])}\n"
                report += f"- **Sector:** {data.get('sector', '')}\n"
                report += f"- **HQ:** {data.get('hq', '')}\n"
                report += f"- **Revenue:** {data.get('est_revenue_cr', '')}\n"
                report += f"- **SAP/ERP:** {data.get('sap_erp', '')}\n"
                report += f"- **Leadership:** {len(data.get('leadership', []))} identified\n"
                report += f"- **Pain Points:** {len(data.get('pain_points', []))}\n"
                report += f"- **Digital Signals:** {len(data.get('key_digital_signals', []))}\n\n"
        
        return report

def main():
    agent = AccountIntelligenceAgent().initialize()
    
    # Load existing research if available
    research_dir = Path(__file__).parent.parent / "task_a_account_intelligence"
    json_file = research_dir / "phase1_consolidated_intelligence.json"
    if json_file.exists():
        agent.load_research(str(json_file))
    
    # Generate and print report
    report = agent.export_report()
    print(report)
    
    # Save report
    out_path = Path(__file__).parent / "data" / "latest_report.md"
    out_path.write_text(report)
    print(f"\nReport saved to: {out_path}")
    
    # Demo RAG search
    print("\n=== RAG Search Demo ===")
    for query in ["SAP digital transformation opportunity", "regulatory compliance pain points", "NBFC gold loan technology"]:
        results = agent.search_intel(query, top_k=2)
        if results:
            print(f"\nQuery: '{query}'")
            for r in results:
                print(f"  [{r['similarity']}] {r['source']}: {r['snippet'][:80]}...")

if __name__ == "__main__":
    main()
