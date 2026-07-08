# backend/api/main.py
# ==============================================
# 🌐 API Server for Maintenance Dashboard
# Provides endpoints for the React frontend to
# read and update maintenance requests.
# ==============================================
import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from src.integrations.database import _get_connection, init_db
from .auth import verify_password

app = FastAPI(title="Property AI Agent")


@app.on_event("startup")
def startup_event():
    try:
        init_db()
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Database init failed: {e}")


# Allow React dev server to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---
class RequestOut(BaseModel):
    id: int
    email_id: Optional[str]
    tenant_email: str
    issue_type: str
    urgency: str
    unit_number: Optional[str]
    summary: Optional[str]
    contractor_name: Optional[str]
    contractor_phone: Optional[str]
    status: str
    created_at: str


class StatusUpdate(BaseModel):
    status: str


# --- Endpoints ---
@app.get("/api/requests", response_model=List[RequestOut])
def get_requests():
    conn = _get_connection()
    rows = conn.execute("""
        SELECT id, email_id, tenant_email, issue_type, urgency,
               unit_number, summary, contractor_name, contractor_phone,
               status, created_at
        FROM requests
        ORDER BY created_at DESC
        LIMIT 50
    """).fetchall()
    return [dict(r) for r in rows]


@app.get("/api/requests/{request_id}", response_model=RequestOut)
def get_request(request_id: int):
    conn = _get_connection()
    row = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Request not found")
    return dict(row)


@app.patch("/api/requests/{request_id}/status")
def update_status(request_id: int, update: StatusUpdate):
    valid_statuses = ["received", "in_progress", "completed", "cancelled"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    conn = _get_connection()
    conn.execute(
        "UPDATE requests SET status = ? WHERE id = ?", (update.status, request_id)
    )
    conn.commit()
    return {"ok": True}


@app.get("/api/health")
def health():
    return {"status": "ok"}
