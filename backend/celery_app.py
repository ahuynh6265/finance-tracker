from dotenv import load_dotenv
import os 
from celery import Celery 

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(__name__)
celery_app.conf.update(
  broker_url = REDIS_URL, 
  timezone = "UTC",
  broker_connection_retry_on_startup = True
)