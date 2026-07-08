# main.py
from src.agent.graph import process_email
from src.gmail.poller import get_unread_maintenance_emails

# Fetch one real maintenance email (use your test email)
emails = get_unread_maintenance_emails(
    query='subject:"Water leaking from ceiling in 4B"'
)
if not emails:
    print("No emails found.")
    exit()

email = emails[0]
print(f"Processing: {email['subject']}")

final_state = process_email(email)

if final_state.get("error"):
    print(f"❌ Failed: {final_state['error']}")
else:
    print(
        f"✅ Request #{final_state['request_id']} dispatched to {final_state['contractor_name']}"
    )
