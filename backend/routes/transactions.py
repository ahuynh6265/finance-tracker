from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction
from schemas import TransactionCreate, TransactionResponse 
from dependencies import transaction_lookup, category_lookup, account_lookup, adjust_balance
import auth

router = APIRouter()

@router.get("/transactions", response_model=list[TransactionResponse])
def get_user_transactions(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  transactions = db.query(Transaction).filter(Transaction.user_id == current_user["id"]).all()
  return transactions

#standard single get route
@router.get("/transactions/{transaction_id}", response_model=TransactionResponse) 
def get_user_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  transaction = transaction_lookup(transaction_id, db, current_user["id"]) 
  return transaction 

#get route from user/category 
@router.get("/categories/{category_id}/transactions", response_model=list[TransactionResponse])
def get_category_transactions(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  category = category_lookup(category_id, db, current_user["id"])  
  return category.transactions 

#get route from user/account 
@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_account_transactions(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  account = account_lookup(account_id, db, current_user["id"]) 
  return account.transactions

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_user_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  new_transaction = Transaction(
    user_id = current_user["id"], 
    account_id = transaction_data.account_id,
    category_id = transaction_data.category_id, 
    amount = transaction_data.amount, 
    transaction_type = transaction_data.transaction_type,
    description = transaction_data.description, 
    date = transaction_data.date
  )
  category_lookup(new_transaction.category_id, db, current_user["id"])
  account = account_lookup(new_transaction.account_id, db, current_user["id"]) 
  adjust_balance(account, new_transaction)
    
  db.add(new_transaction)
  db.commit() 
  db.refresh(new_transaction)
  return new_transaction 

@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  transaction = transaction_lookup(transaction_id, db, current_user["id"])  
  account = account_lookup(transaction.account_id, db, current_user["id"]) 
  adjust_balance(account, transaction, True)
    
  db.delete(transaction)
  db.commit()
  return

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_user_transaction(transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  transaction = transaction_lookup(transaction_id, db, current_user["id"]) 
  account = account_lookup(transaction.account_id, db, current_user["id"])
  #remove current balance before updating
  adjust_balance(account, transaction, True)

  transaction.account_id = transaction_data.account_id
  transaction.category_id = transaction_data.category_id
  transaction.amount = transaction_data.amount
  transaction.transaction_type = transaction_data.transaction_type
  transaction.description = transaction_data.description 
  transaction.date = transaction_data.date

  #check if account being updated is the same account, if it is the same account the new transaction amount will be added back into account if not the new account's balance is updated
  account = account_lookup(transaction.account_id, db, current_user["id"])
  adjust_balance(account, transaction)
  
  db.commit() 
  db.refresh(transaction)
  return transaction 