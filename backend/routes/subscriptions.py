from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 
from database import get_db 
from models import Subscription 
from schemas import SubscriptionCreate, SubscriptionResponse
from dependencies import category_lookup, account_lookup, subscription_lookup
import auth 

router = APIRouter()

@router.get("/subscriptions", response_model=list[SubscriptionResponse])
def get_subscriptions(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  subscriptions = db.query(Subscription).filter(Subscription.user_id == current_user["id"]).all()
  return subscriptions

@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  subscription = subscription_lookup(subscription_id, db, current_user["id"])
  return subscription 

@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription_data: SubscriptionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  account_lookup(subscription_data.account_id, db, current_user["id"])
  category_lookup(subscription_data.category_id, db, current_user["id"])

  new_subscription = Subscription(
    user_id = current_user["id"], 
    account_id = subscription_data.account_id, 
    category_id = subscription_data.category_id, 
    name = subscription_data.name, 
    amount = subscription_data.amount, 
    next_due_date = subscription_data.next_due_date
  )
  db.add(new_subscription)
  db.commit()
  db.refresh(new_subscription)
  return new_subscription

@router.delete("/subscriptions/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(subscription_id: int,  db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  subscription = subscription_lookup(subscription_id, db, current_user["id"])
  db.delete(subscription)
  db.commit()
  return

@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: int, new_subscription_data: SubscriptionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  subscription = subscription_lookup(subscription_id, db, current_user["id"])
  account_lookup(subscription.account_id, db, current_user["id"])
  category_lookup(subscription.category_id, db, current_user["id"])

  subscription.account_id = new_subscription_data.account_id 
  subscription.category_id = new_subscription_data.category_id
  subscription.name = new_subscription_data.name
  subscription.amount = new_subscription_data.amount
  subscription.next_due_date = new_subscription_data.next_due_date 
  db.commit()
  db.refresh(subscription)
  return subscription