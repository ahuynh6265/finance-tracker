from celery_app import celery_app 
from database import SessionLocal 
from dateutil.relativedelta import relativedelta
from datetime import date
from models import Subscription, Transaction
from dependencies import adjust_balance, account_lookup
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def _process_due_subscriptions(db):
  subscriptions = db.query(Subscription).filter(Subscription.next_due_date <= date.today()).all()
  logger.info(f"Found {len(subscriptions)} due.")

  for subscription in subscriptions:
    try: 
      logger.info(f"Processing {subscription.id} for User {subscription.user_id}")
      transaction = Transaction(
        user_id = subscription.user_id, 
        account_id = subscription.account_id, 
        category_id = subscription.category_id, 
        amount = subscription.amount,
        transaction_type = "expense", 
        description = f"Subscription to {subscription.name}", 
        date = subscription.next_due_date 
      )
      account = account_lookup(subscription.account_id, db, subscription.user_id)
      adjust_balance(account, transaction)

      #only advances by one month per run, missed-billing backfill not implemented
      subscription.next_due_date += relativedelta(months=1)
      logger.info(f"Updated subscription due date: {subscription.next_due_date}")
      db.add(transaction)
      db.commit()
    except Exception as e:
      db.rollback()
      logger.error(f"Failed to process subscription {subscription.id}: {e}")
    else: logger.info(f"Database commit for subscription {subscription.id} successful.")
  

@celery_app.task
def process_due_subscriptions():
  db = SessionLocal()
  try: _process_due_subscriptions(db)
  finally: db.close()



    
