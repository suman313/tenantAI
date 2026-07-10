# main.py
from backend.src.agent.graph import process_email
from backend.src.gmail.poller import get_unread_maintenance_emails

# Use the default broad query – no custom subject filter
emails = get_unread_maintenance_emails()
print(f"Found {len(emails)} unread maintenance emails.")

if not emails:
    print("No unread maintenance emails found.")
    exit()

for i, email in enumerate(emails, 1):
    print(f"\n--- Email {i}/{len(emails)} ---")
    print(f"Subject: {email['subject']}")
    final_state = process_email(email)
    if final_state.get("error"):
        print(f"❌ Failed: {final_state['error']}")
    else:
        print(
            f"✅ Request #{final_state['request_id']} dispatched to {final_state['contractor_name']}"
        )
