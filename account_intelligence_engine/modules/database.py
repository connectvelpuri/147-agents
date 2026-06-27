"""
Account Intelligence Engine - Database Layer
Open-source SQLite backend replacing Airtable/Notion
"""
import sqlite3, json, os
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "intel.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(str(DB_PATH))

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    
    # Accounts table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT UNIQUE NOT NULL,
            hq TEXT, sector TEXT, founded INTEGER,
            est_revenue_cr TEXT, is_unlisted INTEGER DEFAULT 1,
            employees TEXT, sap_erp TEXT, group_name TEXT,
            research_json TEXT, last_updated TIMESTAMP
        )
    """)
    
    # Contacts (leadership)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            name TEXT NOT NULL, role TEXT,
            linkedin_url TEXT, email TEXT, phone TEXT,
            priority INTEGER DEFAULT 3,
            last_contacted TIMESTAMP, notes TEXT
        )
    """)
    
    # Tech Stack
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tech_stack (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            category TEXT, product TEXT, vendor TEXT,
            maturity TEXT, notes TEXT
        )
    """)
    
    # Pain Points
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pain_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            pain TEXT NOT NULL, severity INTEGER DEFAULT 3,
            category TEXT, our_solution TEXT
        )
    """)
    
    # News / Events
    cur.execute("""
        CREATE TABLE IF NOT EXISTS intelligence_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            event_type TEXT, title TEXT, url TEXT,
            source TEXT, date TIMESTAMP,
            summary TEXT, sentiment TEXT
        )
    """)
    
    # Digital Transformation Signals
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transformation_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            signal_text TEXT NOT NULL, category TEXT,
            opportunity_score INTEGER DEFAULT 5,
            status TEXT DEFAULT 'identified'
        )
    """)
    
    conn.commit()
    return conn

def import_research(company_data):
    """Import structured research into SQLite"""
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT OR REPLACE INTO accounts 
        (company, hq, sector, founded, est_revenue_cr, is_unlisted, employees, sap_erp, group_name, research_json, last_updated)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        company_data["company"],
        company_data.get("hq", ""),
        company_data.get("sector", ""),
        company_data.get("founded"),
        company_data.get("est_revenue_cr", ""),
        1,
        company_data.get("employees", ""),
        company_data.get("sap_erp", ""),
        company_data.get("group", ""),
        json.dumps(company_data),
        datetime.now()
    ))
    
    conn.commit()
    account_id = cur.lastrowid
    
    # Insert leadership as contacts
    for leader in company_data.get("leadership", []):
        cur.execute("""
            INSERT INTO contacts (account_id, name, role, priority)
            VALUES (?,?,?,1)
        """, (account_id, leader["name"], leader.get("role", "")))
    
    # Insert pain points
    for pain in company_data.get("pain_points", []):
        cur.execute("""
            INSERT INTO pain_points (account_id, pain, severity, category)
            VALUES (?,?,3,'identified')
        """, (account_id, pain))
    
    # Insert digital signals
    for signal in company_data.get("key_digital_signals", []):
        cur.execute("""
            INSERT INTO transformation_signals (account_id, signal_text, category, opportunity_score)
            VALUES (?,?,'digital_transformation',8)
        """, (account_id, signal))
    
    # Insert news
    for news in company_data.get("key_news", []):
        cur.execute("""
            INSERT INTO intelligence_feed (account_id, event_type, title, source, date)
            VALUES (?,'news',?,'web_research',datetime('now'))
        """, (account_id, news))
    
    conn.commit()
    return account_id

def query_all_accounts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, company, sector, est_revenue_cr, sap_erp, last_updated FROM accounts")
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

def query_contacts(account_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, role, priority FROM contacts WHERE account_id=?", (account_id,))
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

def query_pain_points(account_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT pain, severity, category FROM pain_points WHERE account_id=?", (account_id,))
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

def query_signals(account_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT signal_text, category, opportunity_score FROM transformation_signals WHERE account_id=?", (account_id,))
    return [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)
