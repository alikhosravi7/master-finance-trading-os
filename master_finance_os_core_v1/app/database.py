import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from app.config import settings

def _connect():
    path = Path(settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize():
    with _connect() as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            details_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS approvals (
            approval_id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            status TEXT NOT NULL,
            request_json TEXT NOT NULL,
            decision_json TEXT,
            created_at TEXT NOT NULL,
            decided_at TEXT
        )''')
        conn.commit()

def audit(event_type: str, actor: str, subject_id: str, details: dict):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO audit_events(event_type, actor, subject_id, details_json, created_at) VALUES(?,?,?,?,?)",
            (event_type, actor, subject_id, json.dumps(details, ensure_ascii=False),
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()

def create_approval(approval_id: str, task_id: str, request: dict):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO approvals(approval_id, task_id, status, request_json, created_at) VALUES(?,?,?,?,?)",
            (approval_id, task_id, "pending", json.dumps(request, ensure_ascii=False),
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()

def list_approvals():
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM approvals ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

def decide_approval(approval_id: str, decision: dict):
    with _connect() as conn:
        row = conn.execute("SELECT status FROM approvals WHERE approval_id=?", (approval_id,)).fetchone()
        if row is None:
            return None
        if row["status"] != "pending":
            return {"error": "approval_already_decided", "status": row["status"]}
        status = "approved" if decision["approved"] else "rejected"
        conn.execute(
            "UPDATE approvals SET status=?, decision_json=?, decided_at=? WHERE approval_id=?",
            (status, json.dumps(decision, ensure_ascii=False),
             datetime.now(timezone.utc).isoformat(), approval_id)
        )
        conn.commit()
        return {"approval_id": approval_id, "status": status}
