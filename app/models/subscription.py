from pydantic import BaseModel
from typing import Optional
from datetime import date

class SubscriptionCreate(BaseModel):
    name: str
    category: Optional[str] = None
    amount: float
    billing_cycle: str  # weekly | monthly | quarterly | half_yearly | yearly
    start_date: date
    alerts_enabled: bool = True
    remind_before_days: int = 3

class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    billing_cycle: Optional[str] = None
    start_date: Optional[date] = None
    alerts_enabled: Optional[bool] = None
    remind_before_days: Optional[int] = None
    status: Optional[str] = None

    class Config:
        extra = "ignore"  # ✅ IGNORE extra fields instead of 422

