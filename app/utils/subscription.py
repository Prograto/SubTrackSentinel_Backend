from datetime import datetime, timedelta

def calculate_next_renewal(start_date, billing_cycle):
    if billing_cycle == "weekly":
        return start_date + timedelta(days=7)

    if billing_cycle == "monthly":
        return start_date + timedelta(days=30)

    if billing_cycle == "quarterly":
        return start_date + timedelta(days=90)

    if billing_cycle == "half_yearly":
        return start_date + timedelta(days=180)

    if billing_cycle == "yearly":
        return start_date + timedelta(days=365)

    raise ValueError("Invalid billing cycle")
