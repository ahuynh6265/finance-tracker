from fastapi import HTTPException, status
from models import Category, Account, Transaction, Budget, Goal, Subscription
from datetime import datetime, date
from sqlalchemy import func

def category_lookup(category_id, db, user_id):
  category = db.query(Category).filter(Category.id == category_id).first()

  if not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Category ID not found")
  
  if category.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to user")
  
  return category

def account_lookup(account_id, db, user_id):
  account = db.query(Account).filter(Account.id  == account_id).first() 

  if not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Account ID not found") 

  if account.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to user")
  
  return account

def transaction_lookup(transaction_id, db, user_id):
  transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first() 

  if not transaction:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Transaction ID not found") 
  
  if transaction.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Transaction ID {transaction_id} does not belong to user")
  
  return transaction 

def budget_lookup(budget_id, db, user_id):
  budget = db.query(Budget).filter(Budget.id == budget_id).first()

  if not budget:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget ID not found")
  
  if budget.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Budget ID {budget_id} does not belong to user")
  
  return budget

def goal_lookup(goal_id, db, user_id):
  goal = db.query(Goal).filter(Goal.id == goal_id).first()

  if not goal:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal ID not found")
  
  if goal.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Goal ID {goal_id} does not belong to user")
  
  return goal

def subscription_lookup(subscription_id, db, user_id):
  subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()

  if not subscription: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription ID not found")
  
  if subscription.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Subscription ID {subscription_id} does not belong to user")
  
  return subscription

def adjust_balance(account, transaction, reverse=False):
  #if transaction is being created/updated into current/new account
  if not reverse: 
    if transaction.transaction_type == "income": 
      account.balance += transaction.amount 
    else:
      account.balance -= transaction.amount
  
  #if transaction is being deleted/replaced from current account
  else: 
    if transaction.transaction_type == "income": 
      account.balance -= transaction.amount 
    else:
      account.balance += transaction.amount

#track spending by month
def calculate_category_spending(category, db, user_id):
  this_month = date(datetime.now().year, datetime.now().month, 1)
  if datetime.now().month == 12: 
    next_month = date(datetime.now().year + 1, 1, 1)
  else:
    next_month = date(datetime.now().year, datetime.now().month + 1, 1)

  current_total = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.category_id == category.id, Transaction.date >= this_month, Transaction.date < next_month, Transaction.transaction_type == "expense").scalar() or 0
  
  return current_total 

def calculate_account_monthly_flows(account, db, user_id):
  this_month = date(datetime.now().year, datetime.now().month, 1)
  if datetime.now().month == 12: 
    next_month = date(datetime.now().year + 1, 1, 1)
  else:
    next_month = date(datetime.now().year, datetime.now().month + 1, 1)
  
  income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.account_id == account.id, Transaction.transaction_type == "income", Transaction.date >= this_month, Transaction.date < next_month).scalar() or 0 
  expense = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == user_id, Transaction.account_id == account.id, Transaction.transaction_type == "expense", Transaction.date >= this_month, Transaction.date < next_month).scalar() or 0 

  return income, expense 