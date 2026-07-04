# src/integrations/database.py
# ==============================================
# 🥒 Prep Cook: Pantry Keeper (Database)
#
# This module stores every maintenance request in
# a simple SQLite ledger. Each request gets a
# unique tracking number (ID) so the tenant can
# follow up later.
#
# Mental model: A paper notebook where the
# manager writes down every order, one per line,
# with a serial number for easy lookup.
# ==============================================

import sqlite3
from pathlib import Path
from src.agent.classifier import MaintenanceRequest

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "maintenance.db"


def _get_connection():
    """Open the notebook (create the folder and file if needed)."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # return rows as dicts
    return conn


def init_db():
    """Create the ledger table if it doesn't exist (called once at startup)."""
    with _get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_email TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                urgency TEXT NOT NULL,
                unit_number TEXT,
                tenant_phone TEXT,
                access_instructions TEXT,
                summary TEXT,
                status TEXT DEFAULT 'received',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_request(req: MaintenanceRequest, tenant_email: str) -> int:
    """
    Write a new maintenance request into the ledger.
    Returns the tracking number (request ID).
    """
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO requests 
                (tenant_email, issue_type, urgency, unit_number, tenant_phone, access_instructions, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_email,
                req.issue_type,
                req.urgency,
                req.unit_number,
                req.tenant_phone,
                req.access_instructions,
                req.summary,
            ),
        )
        conn.commit()
        return cursor.lastrowid
