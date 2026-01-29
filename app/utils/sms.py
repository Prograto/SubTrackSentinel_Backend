from twilio.rest import Client
from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_MESSAGING_SERVICE_SID
)

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to: str, message: str):
    client.messages.create(
        messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,
        to=to,
        body=message
    )
