from fastapi import APIRouter, Depends
from app.database import users_collection, subscriptions_collection
from app.utils.admin import admin_only

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def admin_stats(admin=Depends(admin_only)):
    return {
        "total_users": users_collection.count_documents({}),
        "total_subscriptions": subscriptions_collection.count_documents({}),
        "active_subscriptions": subscriptions_collection.count_documents({"status": "active"})
    }

@router.post("/send-alerts")
def admin_send_alerts(admin=Depends(admin_only)):
    from app.services.alerts import run_alerts
    run_alerts()
    return {"status": "Alerts sent to all eligible users"}
