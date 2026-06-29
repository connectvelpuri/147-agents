"""
DealForge SaaS Platform - FastAPI backend with auth, accounts, API keys, dashboard.
"""
import os
import sys
import uuid
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import logging

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "agents"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("dealforge-saas")

# Database
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "saas.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, api_key TEXT UNIQUE, tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            api_calls_today INTEGER DEFAULT 0, last_api_call_date TEXT
        );
        CREATE TABLE IF NOT EXISTS api_calls (
            id TEXT PRIMARY KEY, user_id TEXT, endpoint TEXT, persona TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()

# FastAPI imports
try:
    from fastapi import FastAPI, Request, HTTPException, Depends
    from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    FastAPI = object

app = None

if HAS_FASTAPI:
    _app = FastAPI(title="DealForge SaaS", version="1.0.0")
    app = _app

    # Helpers
    def hash_password(password):
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{pwd_hash}"

    def verify_password(password, stored):
        salt, pwd_hash = stored.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == pwd_hash

    def generate_api_key():
        return "df-" + secrets.token_hex(24)

    def get_user_by_session(session_id):
        if not session_id: return None
        conn = get_db()
        row = conn.execute(
            "SELECT u.* FROM users u JOIN sessions s ON u.id = s.user_id WHERE s.id = ? AND (s.expires_at IS NULL OR s.expires_at > datetime('now'))",
            (session_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_api_key(api_key):
        if not api_key: return None
        conn = get_db()
        row = conn.execute("SELECT * FROM users WHERE api_key = ?", (api_key,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def require_user(session: str = Cookie(None) if 'Cookie' in dir() else None):
        # Simplified - requires sessions cookie
        return {}

    TEMPLATES = Path(os.path.join(os.path.dirname(__file__), "templates"))

    def render_template(name, **kwargs):
        path = TEMPLATES / name
        if not path.exists():
            return HTMLResponse(f"Template not found", status_code=404)
        content = path.read_text()
        for k, v in kwargs.items():
            content = content.replace("{" + k + "}", str(v))
        return HTMLResponse(content)

    # Routes
    @_app.get("/")
    async def landing():
        return HTMLResponse(Path(TEMPLATES / "landing.html").read_text())

    @_app.get("/login")
    async def login_page():
        return HTMLResponse(Path(TEMPLATES / "login.html").read_text())

    @_app.get("/signup")
    async def signup_page():
        return HTMLResponse(Path(TEMPLATES / "signup.html").read_text())

    @_app.get("/dashboard")
    async def dashboard():
        return HTMLResponse(Path(TEMPLATES / "dashboard.html").read_text())

    @_app.post("/api/auth/signup")
    async def signup(request: Request):
        body = await request.json()
        name = body.get("name", "").strip()
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        if not name or not email or not password:
            raise HTTPException(400, "All fields required")
        if len(password) < 8:
            raise HTTPException(400, "Password must be 8+ characters")
        conn = get_db()
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            raise HTTPException(409, "Email already registered")
        uid = str(uuid.uuid4())
        api_key = generate_api_key()
        conn.execute("INSERT INTO users (id, name, email, password_hash, api_key, tier) VALUES (?,?,?,?,?,'free')",
                     (uid, name, email, hash_password(password), api_key))
        conn.commit()
        conn.close()
        logger.info(f"New user: {email}")
        return {"success": True}

    @_app.post("/api/auth/login")
    async def login(request: Request):
        body = await request.json()
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if not user or not verify_password(password, user["password_hash"]):
            raise HTTPException(401, "Invalid email or password")
        session_id = str(uuid.uuid4())
        expires = (datetime.utcnow() + timedelta(days=30)).isoformat()
        conn = get_db()
        conn.execute("INSERT INTO sessions (id, user_id, expires_at) VALUES (?,?,?)",
                     (session_id, user["id"], expires))
        conn.commit()
        conn.close()
        resp = JSONResponse({"success": True})
        resp.set_cookie(key="session", value=session_id, httponly=True, max_age=2592000, samesite="lax")
        return resp

    @_app.get("/api/user/profile")
    async def profile(session: str = Cookie(None)):
        user = get_user_by_session(session)
        if not user:
            raise HTTPException(401, "Not authenticated")
        return {"name": user["name"], "email": user["email"], "tier": user["tier"],
                "api_key": user["api_key"], "created_at": user["created_at"]}

    @_app.post("/api/user/regenerate-key")
    async def regenerate_key(session: str = Cookie(None)):
        user = get_user_by_session(session)
        if not user:
            raise HTTPException(401, "Not authenticated")
        new_key = generate_api_key()
        conn = get_db()
        conn.execute("UPDATE users SET api_key = ? WHERE id = ?", (new_key, user["id"]))
        conn.commit()
        conn.close()
        return {"api_key": new_key}

    @_app.post("/api/agent/execute")
    async def execute_agent(request: Request):
        api_key = request.headers.get("X-API-Key", "")
        user = get_user_by_api_key(api_key)
        if not user:
            raise HTTPException(401, "Invalid API key")
        body = await request.json()
        task = body.get("task", "")
        persona = body.get("persona", "revenue_orchestrator")
        if not task:
            raise HTTPException(400, "Task required")
        conn = get_db()
        conn.execute("INSERT INTO api_calls (id, user_id, endpoint, persona) VALUES (?,?,?,?)",
                     (str(uuid.uuid4()), user["id"], "execute", persona))
        conn.execute("UPDATE users SET api_calls_today = api_calls_today + 1 WHERE id = ?", (user["id"],))
        conn.commit()
        conn.close()
        try:
            from agent_base.llm_client import LLMClient, DynamicRouter
            from agent_base.agent_wrapper import AgentIntelligence
            tier = DynamicRouter.route(task, task)
            ai = AgentIntelligence(persona, persona.replace("_", " ").title())
            sp = ai.build_prompt(task)
            client = LLMClient(provider="openrouter", tier=tier)
            result = client.complete(system_prompt=sp, user_prompt=task)
            text = result.text if result.success else f"Error: {result.error}"
        except ImportError:
            text = f"[Demo] Would execute {persona}"
        except Exception as e:
            text = f"[Error] {e}"
        return {"success": True, "persona": persona, "response": text}

    @_app.get("/health")
    async def health():
        return {"status": "healthy", "version": "1.0.0"}
