# src/agent/nodes.py
# ==============================================
# 👨‍🍳 Sous Chefs (Node Implementations)
#
# Each function in this file is one station in the
# kitchen. It takes the order ticket (state), does
# its job using the prep cooks (integrations), and
# returns any updates to the ticket.
#
# Mental model: The Head Chef yells "Classify!"
# and the classify_node chef grabs the email,
# reads it, and writes the structured order on
# the ticket before passing it along.
# ==============================================

from googleapiclient.discovery import build

from src.agent.state import AgentState
from src.agent.classifier import classify_email
from src.integrations.database import save_request
from src.integrations.contractors import find_contractor
from src.integrations.twilio import send_whatsapp
from src.gmail.sender import reply_to_tenant
from src.gmail.auth import get_creds
from src.gmail.poller import mark_as_read as _mark_as_read


def classify_node(state: AgentState) -> dict:
    """
    Read the email body and extract structured maintenance info.
    Updates state with the MaintenanceRequest object.
    """
    result = classify_email(state["email_body"])
    return {"maintenance_request": result}


def save_node(state: AgentState) -> dict:
    request_id = save_request(
        state["maintenance_request"],
        state["tenant_email"],
        email_id=state["email_id"],
        thread_id=state["thread_id"],
        contractor_name=state["contractor_name"],
        contractor_phone=state["contractor_phone"],
    )
    return {"request_id": request_id}


def dispatch_node(state: AgentState) -> dict:
    """
    Look up the right contractor for the issue type.
    Returns the contractor's name and phone number.
    """
    name, phone = find_contractor(state["maintenance_request"].issue_type)
    return {"contractor_name": name, "contractor_phone": phone}


def notify_node(state: AgentState) -> dict:
    """
    Send a WhatsApp message to the contractor with the job details.
    """
    request = state["maintenance_request"]
    message = (
        f"🔧 New Maintenance Request #{state['request_id']}\n"
        f"Issue: {request.issue_type} ({request.urgency})\n"
        f"Unit: {request.unit_number}\n"
        f"Access: {request.access_instructions}\n"
        f"Tenant: {state['tenant_email']}\n"
        f"Summary: {request.summary}"
    )
    send_whatsapp(state["contractor_phone"], message)
    return {}


def reply_node(state: AgentState) -> dict:
    """
    Send a confirmation reply to the tenant in the same email thread.
    """
    reply_to_tenant(
        thread_id=state["thread_id"],
        tenant_email=state["tenant_email"],
        request_id=state["request_id"],
        issue_type=state["maintenance_request"].issue_type,
        contractor_name=state["contractor_name"],
    )
    return {}


def mark_read_node(state: AgentState) -> dict:
    """
    Mark the email as read so it's not processed again.
    """
    creds = get_creds()
    service = build("gmail", "v1", credentials=creds)
    _mark_as_read(service, state["email_id"])
    return {}
