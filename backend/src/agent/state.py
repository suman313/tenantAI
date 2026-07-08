# src/agent/state.py
# ==============================================
# 🎫 The Order Ticket
# This is the data that flows through every step
# of the agent. Think of it as the piece of paper
# that follows a dish from the waiter to the table.
# ==============================================

from typing import TypedDict, Optional
from src.agent.classifier import MaintenanceRequest

class AgentState(TypedDict):
    email_id: str
    thread_id: str
    tenant_email: str
    email_body: str
    maintenance_request: Optional[MaintenanceRequest]  # filled after classification
    contractor_name: Optional[str]
    contractor_phone: Optional[str]
    request_id: Optional[int]
    error: Optional[str]