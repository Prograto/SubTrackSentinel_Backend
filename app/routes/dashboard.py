from fastapi import APIRouter, Depends
from datetime import datetime
from bson import ObjectId

from app.database import subscriptions_collection
from app.utils.jwt import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def dashboard_summary(user=Depends(get_current_user)):
    subs = list(
        subscriptions_collection.find(
            {"user_id": ObjectId(user["user_id"]), "status": "active"}
        )
    )

    total_subs = len(subs)
    monthly_spend = sum(s["amount"] for s in subs)

    upcoming = 0
    for s in subs:
        # ✅ FIX: datetime - datetime
        days_left = (s["next_renewal_date"] - datetime.utcnow()).days
        if days_left <= 7:
            upcoming += 1

    return {
        "total_subscriptions": total_subs,
        "monthly_spend": monthly_spend,
        "upcoming_renewals": upcoming,
        "alerts_enabled": sum(
            1 for s in subs if s.get("alerts_enabled")
        )
    }
