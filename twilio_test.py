# test_twilio.py
from src.integrations.twilio import send_whatsapp

sid = send_whatsapp("+91-6289565427", "🧪 Test from your Property AI Agent!")
print(f"✅ WhatsApp sent, SID: {sid}")