from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from bson import ObjectId

from app.database import subscriptions_collection
from app.models.subscription import SubscriptionCreate, SubscriptionUpdate
from app.utils.jwt import get_current_user
from app.utils.subscription import calculate_next_renewal

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

# 🔹 CREATE
@router.post("/")
def create_subscription(
    data: SubscriptionCreate,
    user=Depends(get_current_user)
):
    next_renewal_date = calculate_next_renewal(
        data.start_date, data.billing_cycle
    )

    subscription = {
        "user_id": ObjectId(user["user_id"]),
        "name": data.name,
        "category": data.category,
        "amount": data.amount,
        "billing_cycle": data.billing_cycle,

        # ✅ FIX: convert date → datetime
        "start_date": datetime.combine(
            data.start_date, datetime.min.time()
        ),
        "next_renewal_date": datetime.combine(
            next_renewal_date, datetime.min.time()
        ),

        "alerts_enabled": data.alerts_enabled,
        "remind_before_days": data.remind_before_days,
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    subscriptions_collection.insert_one(subscription)
    return {"message": "Subscription added successfully"}

# 🔹 LIST
@router.get("/")
def get_subscriptions(user=Depends(get_current_user)):
    subs = subscriptions_collection.find(
        {"user_id": ObjectId(user["user_id"]), "status": "active"}
    )

    results = []
    for s in subs:
        results.append({
            "id": str(s["_id"]),
            "name": s["name"],
            "amount": s["amount"],
            "billing_cycle": s["billing_cycle"],
            "start_date": s["start_date"],
            "next_renewal_date": s["next_renewal_date"],
            "alerts_enabled": s["alerts_enabled"],
            "remind_before_days": s["remind_before_days"]
        })

    return results

# 🔹 UPDATE
@router.put("/{sub_id}")
def update_subscription(
    sub_id: str,
    data: SubscriptionUpdate,
    user=Depends(get_current_user)
):
    update_data = {
        k: v for k, v in data.dict().items() if v is not None
    }

    # 🔥 If start_date OR billing_cycle changes → recalc renewal
    if "start_date" in update_data or "billing_cycle" in update_data:
        sub = subscriptions_collection.find_one({
            "_id": ObjectId(sub_id),
            "user_id": ObjectId(user["user_id"])
        })

        if not sub:
            raise HTTPException(status_code=404, detail="Subscription not found")

        start_date = update_data.get(
            "start_date",
            sub["start_date"].date()
        )

        billing_cycle = update_data.get(
            "billing_cycle",
            sub["billing_cycle"]
        )

        next_renewal = calculate_next_renewal(
            start_date, billing_cycle
        )

        update_data["start_date"] = datetime.combine(
            start_date, datetime.min.time()
        )

        update_data["next_renewal_date"] = datetime.combine(
            next_renewal, datetime.min.time()
        )

    update_data["updated_at"] = datetime.utcnow()

    subscriptions_collection.update_one(
        {"_id": ObjectId(sub_id), "user_id": ObjectId(user["user_id"])},
        {"$set": update_data}
    )

    return {"message": "Subscription updated"}


# 🔹 DELETE (Soft delete)
@router.delete("/{sub_id}")
def delete_subscription(sub_id: str, user=Depends(get_current_user)):
    subscriptions_collection.update_one(
        {"_id": ObjectId(sub_id), "user_id": ObjectId(user["user_id"])},
        {"$set": {
            "status": "cancelled",
            "updated_at": datetime.utcnow()
        }}
    )
    return {"message": "Subscription removed"}
