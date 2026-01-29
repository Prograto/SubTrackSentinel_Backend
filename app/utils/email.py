# app/utils/email.py

import requests
from app.config import MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM

def send_email(to: str, subject: str, html: str):
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": MAILGUN_FROM,
            "to": to,
            "subject": subject,
            "html": html
        }
    )

    if response.status_code != 200:
        print("❌ Mailgun error:", response.text)
    else:
        print(f"📧 Email sent to {to}")
