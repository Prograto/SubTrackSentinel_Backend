from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes import auth, subscriptions, dashboard
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.alerts import run_alerts
from app.routes import admin


scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(run_alerts, "cron", hour=10, minute=0)
scheduler.start()


app = FastAPI(title="SubTrack Sentinel API")

# (CORS FIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sub-track-sentinel.vercel.app/"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(dashboard.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

