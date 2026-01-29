from fastapi import Depends, HTTPException
from app.utils.jwt import get_current_user

def admin_only(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
