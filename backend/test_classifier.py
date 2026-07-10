# test_classifier.py
from backend.src.agent.classifier import classify_email

test_email = """
Subject: Water leaking from ceiling in Apt 4B

Hi, this is Priya in unit 4B. There's water dripping from the ceiling in the living room.
It started last night and it's getting worse. My phone is 9876543210.
Please send someone urgently. I have a spare key under the mat.
"""

result = classify_email(test_email)
print("Issue Type:", result.issue_type)
print("Urgency:", result.urgency)
print("Unit:", result.unit_number)
print("Phone:", result.tenant_phone)
print("Access:", result.access_instructions)
print("Summary:", result.summary)
