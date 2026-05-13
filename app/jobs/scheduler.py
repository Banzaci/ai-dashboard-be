from apscheduler.schedulers.background import BackgroundScheduler

from app.services.oil_service import fetch_oil_price

scheduler = BackgroundScheduler()

scheduler.add_job(
    fetch_oil_price,
    "interval",
    hours=1
)

def start_scheduler():
    scheduler.start()