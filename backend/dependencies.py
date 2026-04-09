from fastapi import HTTPException, status
from models import Category, Account, Transaction, Budget, Goal
from datetime import datetime, date

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
def calculate_category_spending(category):
  current_total = 0
  this_month = date(datetime.now().year, datetime.now().month, 1)
  if datetime.now().month == 12: 
    next_month = date(datetime.now().year + 1, 1, 1)
  else:
    next_month = date(datetime.now().year, datetime.now().month + 1, 1)

  for transaction in category.transactions: 
    if transaction.transaction_type == "expense" and transaction.date >= this_month and transaction.date < next_month:
      current_total += transaction.amount
  
  return current_total
