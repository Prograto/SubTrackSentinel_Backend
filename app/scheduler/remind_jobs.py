# app/scheduler/remind_jobs.py

from app.services.alerts import run_alerts

def run_daily_alerts():
    print("⏰ Running daily subscription alerts...")
    run_alerts()
    print("✅ Alert job finished")


if __name__ == "__main__":
    run_daily_alerts()
