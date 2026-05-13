from celery_app import celery_app 
from database import SessionLocal 
from subscription_service import run_due_subscriptions
from demo_data import generate_demo_data

@celery_app.task
def process_due_subscriptions():
  db = SessionLocal()
  try: run_due_subscriptions(db)
  finally: db.close()

@celery_app.task 
def reset_demo_data():
  generate_demo_data()