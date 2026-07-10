# src/gmail/sender.py
# ==============================================
# ✉️ Prep Cook: The Thank‑You Note (Email Reply)
#
# Sends a confirmation email back to the tenant
# in the SAME email thread they originally wrote.
# Includes their tracking number and contractor name.
#
# Mental model: The waiter takes the order, then
# hands the customer a receipt with a number so
# they can check on it later.
# ==============================================

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from .auth import get_creds

def reply_to_tenant(thread_id: str, tenant_email: str, request_id: int, issue_type: str, contractor_name: str):
    """
    Send a reply in the same email thread.
    The tenant will see:
    "We've received your maintenance request #123.
    A contractor (Raju's Plumbing) will contact you."
    """
    creds = get_creds()
    service = build('gmail', 'v1', credentials=creds)

    # Build the email
    message = MIMEText(
        f"Hi,\n\n"
        f"We've received your {issue_type} maintenance request (tracking #{request_id}).\n"
        f"{contractor_name} has been assigned and will contact you shortly.\n\n"
        f"If this is an emergency, please call us directly.\n\n"
        f"Thank you,\nProperty Management"
    )
    message['to'] = tenant_email
    message['subject'] = f"Maintenance Request #{request_id} Received"
    message['In-Reply-To'] = thread_id
    message['References'] = thread_id

    # Encode and send
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId='me',
        body={
            'raw': raw,
            'threadId': thread_id,
        }
    ).execute()