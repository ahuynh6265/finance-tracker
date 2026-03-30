from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Account
from schemas import AccountCreate, AccountResponse
from dependencies import user_lookup, account_lookup

router = APIRouter()

@router.get("/users/{user_id}/accounts", response_model=list[AccountResponse])
def get_user_accounts(user_id: int, db: Session = Depends(get_db)): 
  user = user_lookup(user_id, db)
  return user.accounts 

@router.get("/users/{user_id}/accounts/{account_id}", response_model=AccountResponse)
def get_user_account(user_id: int, account_id: int, db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  account = account_lookup(account_id, db, user_id)
  return account 

@router.post("/users/{user_id}/accounts", response_model=list[AccountResponse], status_code=status.HTTP_201_CREATED)
def create_user_accounts(user_id: int, accounts_data: list[AccountCreate], db: Session = Depends(get_db)): 
  user_lookup(user_id, db)

  new_accounts = [Account (
    user_id = user_id, 
    bank_name = a.bank_name, 
    account_type = a.account_type, 
    balance = a.balance
  ) for a in accounts_data] 
  db.add_all(new_accounts)
  db.commit() 
  for account in new_accounts:
    db.refresh(account)
  return new_accounts 

@router.delete("/users/{user_id}/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(user_id: int, account_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  account = account_lookup(account_id, db, user_id)
  db.delete(account)
  db.commit()
  return

@router.put("/users/{user_id}/accounts/{account_id}", response_model=AccountResponse)
def update_user_account(user_id: int, account_id: int, account_data: AccountCreate, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  account = account_lookup(account_id, db, user_id)
  
  account.bank_name = account_data.bank_name
  account.account_type = account_data.account_type
  account.balance = account_data.balance 
  db.commit() 
  db.refresh(account)
  return account