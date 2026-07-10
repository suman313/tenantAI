# view_requests.py
import sys
from pathlib import Path

if str(Path(__file__).resolve().parents[1]) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.src.integrations.database import _get_connection

conn = _get_connection()
rows = conn.execute("""
    SELECT id, email_id, tenant_email, issue_type, unit_number, contractor_name, status, created_at
    FROM requests ORDER BY created_at DESC LIMIT 10
""").fetchall()

for r in rows:
    print(
        f"#{r['id']} | Email: {r['email_id']} | {r['issue_type']} in {r['unit_number']} | "
        f"Contractor: {r['contractor_name']} | Status: {r['status']} | {r['created_at']}"
    )
