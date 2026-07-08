# test_database.py
from src.integrations.database import init_db, save_request
from src.agent.classifier import MaintenanceRequest

init_db()
print("✅ Database ready")

# Create a fake classified request (like the one your classifier returns)
fake_request = MaintenanceRequest(
    issue_type="Plumbing",
    urgency="high",
    unit_number="4B",
    tenant_phone="9876543210",
    access_instructions="key under mat",
    summary="Leak in ceiling"
)

req_id = save_request(fake_request, "priya@example.com")
print(f"✅ Request saved with ID: {req_id}")