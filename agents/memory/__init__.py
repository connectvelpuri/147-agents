"""
Persistent Memory System - SQLite-backed conversation + deal history.
Stores: conversations, agent responses, user feedback, deal data.
"""
import sqlite3
import json
import os
import uuid
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "dealforge.db")

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            persona TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS deals (
            id TEXT PRIMARY KEY,
            name TEXT,
            company TEXT,
            value REAL,
            stage TEXT,
            meddpicc_score REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id TEXT PRIMARY KEY,
            conversation_id TEXT,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS cache (
            query_hash TEXT PRIMARY KEY,
            response TEXT NOT NULL,
            persona TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);
        CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache(expires_at);
    """)
    conn.commit()
    conn.close()

class ConversationMemory:
    def __init__(self, session_id=None):
        self.session_id = session_id or str(uuid.uuid4())
        init_db()

    def add_message(self, role, content, persona=None, confidence=None):
        conn = get_db()
        conn.execute(
            "INSERT INTO conversations (id, session_id, role, content, persona, confidence) VALUES (?, ?, ?, ?, ?, ?)",
            (str(uuid.uuid4()), self.session_id, role, content, persona, confidence)
        )
        conn.commit()
        conn.close()

    def get_history(self, limit=20):
        conn = get_db()
        rows = conn.execute(
            "SELECT role, content, persona, confidence, created_at FROM conversations WHERE session_id=? ORDER BY created_at DESC LIMIT ?",
            (self.session_id, limit)
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]

    def get_context(self, limit=5):
        """Get recent context as formatted string."""
        history = self.get_history(limit)
        lines = []
        for h in history:
            role = "User" if h["role"] == "user" else f"Agent({h['persona'] or 'unknown'})"
            content = h["content"][:200]
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

class DealStore:
    @staticmethod
    def save(name, company, value, stage, meddpicc_score, notes=""):
        conn = get_db()
        deal_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO deals (id, name, company, value, stage, meddpicc_score, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (deal_id, name, company, value, stage, meddpicc_score, notes)
        )
        conn.commit()
        conn.close()
        return deal_id

    @staticmethod
    def list(limit=20):
        conn = get_db()
        rows = conn.execute("SELECT * FROM deals ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

class FeedbackStore:
    @staticmethod
    def save(conversation_id, rating, comment=""):
        conn = get_db()
        conn.execute(
            "INSERT INTO feedback (id, conversation_id, rating, comment) VALUES (?, ?, ?, ?)",
            (str(uuid.uuid4()), conversation_id, rating, comment)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_stats():
        conn = get_db()
        row = conn.execute(
            "SELECT COUNT(*) as count, AVG(rating) as avg_rating FROM feedback"
        ).fetchone()
        conn.close()
        return dict(row) if row else {"count": 0, "avg_rating": 0}

class ResponseCache:
    @staticmethod
    def get(query, persona):
        import hashlib
        q_hash = hashlib.md5(f"{query}:{persona}".encode()).hexdigest()
        conn = get_db()
        row = conn.execute(
            "SELECT response, model FROM cache WHERE query_hash=? AND (expires_at IS NULL OR expires_at > datetime('now'))",
            (q_hash,)
        ).fetchone()
        conn.close()
        return row["response"] if row else None

    @staticmethod
    def set(query, persona, response, model="", ttl_hours=24):
        import hashlib
        q_hash = hashlib.md5(f"{query}:{persona}".encode()).hexdigest()
        expires = (datetime.utcnow() + timedelta(hours=ttl_hours)).isoformat()
        conn = get_db()
        conn.execute(
            "INSERT OR REPLACE INTO cache (query_hash, response, persona, model, expires_at) VALUES (?, ?, ?, ?, ?)",
            (q_hash, response, persona, model, expires)
        )
        conn.commit()
        conn.close()
