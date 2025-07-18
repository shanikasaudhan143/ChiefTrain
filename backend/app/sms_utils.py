# app/sms_utils.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

def send_sms(to: str, body: str):
    try:
        message = client.messages.create(
            body=body,
            from_=twilio_number,
            to=to
        )
        print("✅ SMS sent:", message.sid)
    except Exception as e:
        print("❌ SMS error:", e)
