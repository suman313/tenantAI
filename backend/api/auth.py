# backend/api/auth.py
from fastapi import Header, HTTPException

ADMIN_PASSWORD = "admin123"  # change in production


def verify_password(x_password: str = Header(None)):
    if x_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return True
