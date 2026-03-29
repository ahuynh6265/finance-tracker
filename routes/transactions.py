from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction
from schemas import TransactionCreate, TransactionResponse 
from dependencies import user_lookup, transaction_lookup, category_lookup, account_lookup

router = APIRouter()

@router.get("/users/{user_id}/transactions", response_model=list[TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
  user = user_lookup(user_id, db)
  return user.transaction

#standard single get route
@router.get("/users/{user_id}/transactions/{transaction_id}", response_model=TransactionResponse) 
def get_user_transaction(user_id: int, transaction_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  transaction = transaction_lookup(transaction_id, db, user_id) 
  return transaction 

#get route from user/category 
@router.get("/users/{user_id}/categories/{category_id}/transactions", response_model=list[TransactionResponse])
def get_category_transactions(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  category = category_lookup(category_id, db, user_id)  
  return category.transaction 

#get route from user/account 
@router.get("/users/{user_id}/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_account_transactions(user_id: int, account_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  account = account_lookup(account_id, db, user_id) 
  return account.transaction

@router.post("/users/{user_id}/transactions", response_model=list[TransactionResponse], status_code=status.HTTP_201_CREATED)
def create_user_transactions(user_id: int, transactions_data: list[TransactionCreate], db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
 
  new_transactions = []
  for t in transactions_data:
    new_transaction= Transaction (
    user_id = user_id,
    account_id = t.account_id,
    category_id = t.category_id,
    amount = t.amount,
    transaction_type = t.transaction_type, 
    description = t.description,
    date = t.date
    )
    new_transactions.append(new_transaction)

    account = account_lookup(t.account_id, db, user_id) 
    if account:
      if t.transaction_type == "income":
        account.balance += t.amount
      else:
        account.balance -= t.amount
    
  db.add_all(new_transactions)
  db.commit() 
  for transaction in new_transactions:
    db.refresh(transaction)
  return new_transactions 

@router.delete("/users/{user_id}/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_transaction(user_id: int, transaction_id: int, db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  transaction = transaction_lookup(transaction_id, db, user_id)  
  account = account_lookup(transaction.account_id, db, user_id) 
  if transaction.transaction_type == "income":
    account.balance -= transaction.amount
  else:
    account.balance += transaction.amount
    
  db.delete(transaction)
  db.commit()
  return

@router.put("/users/{user_id}/transactions/{transaction_id}", response_model=TransactionResponse)
def update_user_transaction(user_id: int, transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  transaction = transaction_lookup(transaction_id, db, user_id)  
  transaction.account_id = transaction_data.account_id
  transaction.category_id = transaction_data.category_id
  transaction.amount = transaction_data.amount
  transaction.transaction_type = transaction_data.transaction_type
  transaction.description = transaction_data.description 
  transaction.date = transaction_data.date

  db.commit() 
  db.refresh(transaction)
  return transaction 