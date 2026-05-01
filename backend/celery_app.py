from dotenv import load_dotenv
import os 
from celery import Celery 
from celery.schedules import crontab
import sentry_sdk

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

sentry_sdk.init(
  dsn = os.getenv("SENTRY_DSN"), 
  send_default_pii=True,
  traces_sample_rate=1.0,
  environment=os.getenv("ENVIRONMENT", "development")
)

celery_app = Celery(__name__)

celery_app.conf.update(
  broker_url = REDIS_URL, 
  timezone = "UTC",
  broker_connection_retry_on_startup = True,
  imports = ("tasks",),
  beat_schedule = {
  "daily-due-subscriptions" : {
    "task": "tasks.process_due_subscriptions",
    "schedule": crontab(hour=0, minute=0)
    },
  }
)