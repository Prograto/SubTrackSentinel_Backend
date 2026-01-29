from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta

from app.database import users_collection
from app.models.user import RegisterUser, LoginUser
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.utils.reset_token import generate_reset_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ✅ REGISTER
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    print("🔥 REGISTER HIT")
    print("USERNAME:", user.username)
    print("EMAIL:", user.email)
    print("PASSWORD LENGTH:", len(user.password))

    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "phone": user.phone,
        "role": "user", 
        "createdAt": datetime.utcnow()
    })

    return {"message": "User registered successfully"}

# ✅ LOGIN
@router.post("/login")
def login(user: LoginUser):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "user_id": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user.get("role", "user")
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": db_user["username"],
            "email": db_user["email"],
            "role": db_user.get("role", "user")
        }
    }

# 🔹 FORGOT PASSWORD
@router.post("/forgot-password")
def forgot_password(data: dict):
    email = data.get("email")

    user = users_collection.find_one({"email": email})
    if not user:
        return {"message": "If email exists, reset link sent"}

    token = generate_reset_token()
    expiry = datetime.utcnow() + timedelta(minutes=15)

    users_collection.update_one(
        {"email": email},
        {"$set": {
            "reset_token": token,
            "reset_token_expiry": expiry
        }}
    )

    # DEV MODE ONLY
    print(f"RESET LINK: http://localhost:5173/reset-password?token={token}")

    return {"message": "Reset link sent"}

# 🔹 RESET PASSWORD
@router.post("/reset-password")
def reset_password(data: dict):
    token = data.get("token")
    new_password = data.get("new_password")

    user = users_collection.find_one({
        "reset_token": token,
        "reset_token_expiry": {"$gt": datetime.utcnow()}
    })

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "password": hash_password(new_password),
            "reset_token": None,
            "reset_token_expiry": None
        }}
    )

    return {"message": "Password reset successful"}

@router.post("/run-alerts")
def trigger_alerts():
    from app.services.alerts import run_alerts
    run_alerts()
    return {"status": "Alerts executed"}


