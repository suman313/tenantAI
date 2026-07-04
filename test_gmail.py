# test_gmail.py
from src.gmail.poller import get_unread_maintenance_emails

# emails = get_unread_maintenance_emails()
# for em in emails:
#     print(f"From: {em['from']}, Subject: {em['subject']}")
#     print(em["body"][:100])
#     print("---")
# # test_gmail.py
# from src.gmail.poller import get_unread_maintenance_emails

# Only fetch this specific test email
emails = get_unread_maintenance_emails(query='subject:"Water leaking from ceiling in 4B"')
for em in emails:
    print(f"ID: {em['id']}")
    print(f"ThreadID: {em['threadId']}")
    print(f"From: {em['from']}")
    print(f"Subject: {em['subject']}")
    print(em['body'][:200])
    print("---")