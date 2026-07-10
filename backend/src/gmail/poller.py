# src/gmail/poller.py
import base64
from googleapiclient.discovery import build
from .auth import get_creds


def get_unread_maintenance_emails(query=None):
    if query is None:
        keywords = (
            'leaking OR leak OR repair OR broken OR "not working" '
            "OR sparking OR crack OR infestation OR clogged OR mold OR pest OR HVAC OR plumbing OR electrical"
        )
        # Only emails from the last 2 days
        query = f"is:unread newer_than:2d ({keywords})"
    else:
        # If a custom query is provided, still ensure it's unread
        if "is:unread" not in query:
            query = f"is:unread {query}"
        # Optionally add date filter to custom queries too
        if "newer_than" not in query and "after" not in query:
            query += " newer_than:2d"

    creds = get_creds()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"], format="full")
            .execute()
        )
        headers = msg_data["payload"]["headers"]
        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
        )
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")

        body = ""
        if "parts" in msg_data["payload"]:
            for part in msg_data["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode()
                    break
        else:
            if msg_data["payload"]["body"].get("data"):
                body = base64.urlsafe_b64decode(
                    msg_data["payload"]["body"]["data"]
                ).decode()

        emails.append(
            {
                "id": msg["id"],
                "threadId": msg["threadId"],
                "subject": subject,
                "from": sender,
                "body": body,
            }
        )

    return emails


def mark_as_read(service, msg_id):
    """Remove UNREAD label from a message."""
    service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()
