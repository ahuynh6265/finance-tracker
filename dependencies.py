from fastapi import HTTPException, status
from models import User, Category, Account, Transaction

def user_lookup(user_id, db):
  user = db.query(User).filter(User.id == user_id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User ID not found") 
  return user 

def category_lookup(category_id, db, user_id=None):
  category = db.query(Category).filter(Category.id == category_id).first()

  if not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Category ID not found")
  
  if user_id: 
    user = user_lookup(user_id, db)

    if category.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to {user.name}")
    return category

  return category

def account_lookup(account_id, db, user_id=None):
  account = db.query(Account).filter(Account.id  == account_id).first() 

  if not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Account ID not found") 
  
  if user_id: 
    user = user_lookup(user_id, db)

    if account.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to {user.name}")
    return account
  
  return account

def transaction_lookup(transaction_id, db, user_id=None):
  transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first() 

  if not transaction:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Transaction ID not found") 
  
  if user_id:
    user = user_lookup(user_id, db)
    if transaction.user_id != user_id: 
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Transaction ID {transaction_id} does not belong to {user.name}")
    return transaction 
  
  return transaction

