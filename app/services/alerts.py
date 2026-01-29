# app/services/alerts.py

from datetime import datetime, timedelta
from app.database import subscriptions_collection, users_collection
from app.utils.email import send_email
from app.utils.sms import send_sms

ENABLE_SMS = False  # change to True later if needed

def run_alerts():
    now = datetime.utcnow()      # ✅ datetime for MongoDB
    today = now.date()           # ✅ date for comparison only

    subs = subscriptions_collection.find({
        "status": "active",
        "alerts_enabled": True
    })

    for sub in subs:
        renewal_date = sub["next_renewal_date"].date()
        remind_on = renewal_date - timedelta(days=sub["remind_before_days"])

        # 🔁 Only run on reminder day
        if remind_on != today:
            continue

        # 🔁 Prevent duplicate alerts
        last_sent = sub.get("last_alert_sent_on")
        if last_sent and last_sent.date() == today:
            continue

        user = users_collection.find_one({"_id": sub["user_id"]})
        if not user:
            continue

        # 📧 EMAIL
        if user.get("email"):
            print("📧 Sending email alert...", user["email"])
            send_email(
                to=user["email"],
                subject=f"{sub['name']} renewal reminder",
                html=f"""
                <h3>🔔 Subscription Reminder</h3>
                <p><strong>{sub['name']}</strong> renews on
                <b>{renewal_date.strftime('%d %b %Y')}</b></p>
                <p>Amount: ₹{sub['amount']}</p>
                """
            )

        # 📱 SMS (optional)
        if ENABLE_SMS and user.get("phone"):
            send_sms(
                user["phone"],
                f"{sub['name']} renews on {renewal_date}. Amount ₹{sub['amount']}"
            )

        # ✅ STORE datetime (NOT date)
        subscriptions_collection.update_one(
            {"_id": sub["_id"]},
            {"$set": {"last_alert_sent_on": now}}
        )

        print(f"✅ Alert processed for {sub['name']}")
