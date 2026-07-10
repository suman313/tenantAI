# test_gmail_sender.py
from backend.src.gmail.sender import reply_to_tenant

# Use YOUR own email and a fake thread ID from a test email you already received
# You can get a threadId from test_gmail.py output
reply_to_tenant(
    thread_id="19f1f414e436493c",
    tenant_email="sumanmodak616@gmail.com",
    request_id=42,
    issue_type="Plumbing",
    contractor_name="Raju's Plumbing",
)
print("✅ Reply sent (check your inbox)")
