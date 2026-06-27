"""State persistence — SQLite database for accounts, research cycles, and feedback."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import (
    AccountRequest, ResearchCycleReport, CollectionJob,
    AccountIntelligenceReport, CorrectionEvent, ResearchDepth,
)


class StateDatabase:
    def __init__(self, db_path: str | Path | None = None):
        self._db_path = Path(db_path) if db_path else Path("data/state.db")
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None
        self._init_db()

    def _get_conn(self):
        if self._conn is None:
            import sqlite3
            self._conn = sqlite3.connect(str(self._db_path))
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self):
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                account_name TEXT NOT NULL,
                domain TEXT,
                depth TEXT DEFAULT 'standard',
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now')),
                last_researched_at TEXT,
                intelligence_report TEXT,
                confidence_score REAL DEFAULT 0.0
            );

            CREATE TABLE IF NOT EXISTS research_cycles (
                cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                depth TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                status TEXT DEFAULT 'running',
                jobs_count INTEGER DEFAULT 0,
                errors_count INTEGER DEFAULT 0,
                reports_published TEXT DEFAULT '[]',
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            );

            CREATE TABLE IF NOT EXISTS collection_jobs (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id INTEGER NOT NULL,
                domain TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                started_at TEXT,
                completed_at TEXT,
                results_count INTEGER DEFAULT 0,
                errors TEXT DEFAULT '[]',
                FOREIGN KEY (cycle_id) REFERENCES research_cycles(cycle_id)
            );

            CREATE TABLE IF NOT EXISTS corrections (
                correction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                domain TEXT NOT NULL,
                intelligence_item_id TEXT,
                original_value TEXT,
                corrected_value TEXT,
                corrected_by TEXT,
                corrected_at TEXT DEFAULT (datetime('now')),
                reason TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            );

            CREATE TABLE IF NOT EXISTS consumer_feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                consumer_agent_id TEXT NOT NULL,
                report_type TEXT NOT NULL,
                score INTEGER CHECK(score >= 1 AND score <= 5),
                comment TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)
        conn.commit()

    def upsert_account(self, request: AccountRequest):
        conn = self._get_conn()
        conn.execute(
            """INSERT INTO accounts (account_id, account_name, depth, status)
               VALUES (?, ?, ?, 'pending')
               ON CONFLICT(account_id) DO UPDATE SET
               depth = excluded.depth,
               status = 'pending'""",
            (request.account_id, request.account_name, request.depth.value),
        )
        conn.commit()

    def save_report(self, account_id: str, report: AccountIntelligenceReport):
        conn = self._get_conn()
        conn.execute(
            "UPDATE accounts SET intelligence_report = ?, confidence_score = ?, status = 'researched', last_researched_at = datetime('now') WHERE account_id = ?",
            (json.dumps(report.to_dict(), default=str), report.overall_confidence, account_id),
        )
        conn.commit()

    def start_cycle(self, account_id: str, depth: ResearchDepth) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO research_cycles (account_id, depth, started_at, status) VALUES (?, ?, datetime('now'), 'running')",
            (account_id, depth.value),
        )
        conn.commit()
        return cur.lastrowid

    def complete_cycle(self, cycle_id: int, cycle: ResearchCycleReport):
        conn = self._get_conn()
        conn.execute(
            "UPDATE research_cycles SET completed_at = datetime('now'), status = ?, jobs_count = ?, errors_count = ? WHERE cycle_id = ?",
            ("completed" if not cycle.errors else "completed_with_errors",
             len(cycle.jobs), len(cycle.errors), cycle_id),
        )
        conn.commit()

    def save_job(self, cycle_id: int, job: CollectionJob) -> int:
        conn = self._get_conn()
        cur = conn.execute(
            "INSERT INTO collection_jobs (cycle_id, domain, status, started_at, completed_at, results_count) VALUES (?, ?, ?, ?, ?, ?)",
            (cycle_id, job.domain.value, job.status,
             job.started_at.isoformat() if job.started_at else None,
             job.completed_at.isoformat() if job.completed_at else None,
             len(job.results)),
        )
        conn.commit()
        return cur.lastrowid

    def log_correction(self, event: CorrectionEvent):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO corrections (account_id, domain, original_value, corrected_value, corrected_by, reason) VALUES (?, ?, ?, ?, ?, ?)",
            (event.account_id, event.domain,
             json.dumps(event.original_value, default=str),
             json.dumps(event.corrected_value, default=str),
             event.corrected_by, event.reason),
        )
        conn.commit()

    def log_consumer_feedback(self, account_id: str, consumer_agent_id: str, report_type: str, score: int, comment: str = ""):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO consumer_feedback (account_id, consumer_agent_id, report_type, score, comment) VALUES (?, ?, ?, ?, ?)",
            (account_id, consumer_agent_id, report_type, score, comment),
        )
        conn.commit()

    def get_pending_accounts(self) -> list[AccountRequest]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT account_id, account_name, depth FROM accounts WHERE status = 'pending'"
        ).fetchall()
        return [
            AccountRequest(account_id=r["account_id"], account_name=r["account_name"],
                           depth=ResearchDepth(r["depth"]))
            for r in rows
        ]

    def get_account(self, account_id: str) -> dict | None:
        conn = self._get_conn()
        row = conn.execute(
            "SELECT * FROM accounts WHERE account_id = ?", (account_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_correction_rate(self, account_id: str | None = None) -> float:
        conn = self._get_conn()
        if account_id:
            total = conn.execute(
                "SELECT COUNT(*) as c FROM corrections WHERE account_id = ?", (account_id,)
            ).fetchone()["c"]
        else:
            total = conn.execute("SELECT COUNT(*) as c FROM corrections").fetchone()["c"]
        researched = conn.execute(
            "SELECT COUNT(*) as c FROM accounts WHERE status = 'researched'"
        ).fetchone()["c"]
        if researched == 0:
            return 0.0
        return total / researched

    def close(self):
        if self._conn:
            self._conn.close()
