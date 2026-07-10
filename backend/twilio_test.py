# test_twilio.py
from backend.src.integrations.twilio import send_whatsapp

sid = send_whatsapp("+91-6289565427", "🧪 Test from your Property AI Agent! - Suman Here")
print(f"✅ WhatsApp sent, SID: {sid}")