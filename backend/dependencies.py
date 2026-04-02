from fastapi import HTTPException, status
from models import Category, Account, Transaction


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
  

