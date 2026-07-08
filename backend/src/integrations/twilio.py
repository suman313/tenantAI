# src/integrations/twilio.py
# ==============================================
# 📲 Prep Cook: The WhatsApp Waiter
#
# This module sends WhatsApp messages to contractors.
# It uses Twilio's API, which is like a telephone
# exchange that connects your kitchen to any phone.
#
# Mental model: The chef writes a note, hands it to
# the waiter, and the waiter runs to the contractor's
# phone and delivers the message.
# ==============================================

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio credentials — kept safe in the .env file, never in code
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # sandbox number


def send_whatsapp(to_number: str, message: str) -> str:
    """
    Deliver a WhatsApp message to a phone number.
    Returns the Twilio message SID (delivery receipt ID).
    """
    if not all([TWILIO_SID, TWILIO_AUTH, TWILIO_WHATSAPP_NUMBER]):
        raise EnvironmentError("Twilio credentials missing in .env file")

    client = Client(TWILIO_SID, TWILIO_AUTH)
    msg = client.messages.create(
        body=message,
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
        to=f"whatsapp:{to_number}",
    )
    return msg.sid
