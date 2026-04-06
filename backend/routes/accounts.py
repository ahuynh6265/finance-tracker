from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Account
from schemas import AccountCreate, AccountResponse
from dependencies import account_lookup
import auth 

router = APIRouter()

@router.get("/accounts", response_model=list[AccountResponse])
def get_user_accounts(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  accounts = db.query(Account).filter(Account.user_id == current_user["id"]).all()
  return accounts 

@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_user_account(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  account = account_lookup(account_id, db, current_user["id"])
  return account 

@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_user_accounts(account_data: AccountCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  new_account = Account(
    user_id = current_user["id"], 
    bank_name = account_data.bank_name, 
    account_type = account_data.account_type, 
    balance = account_data.balance)
  db.add(new_account)
  db.commit() 
  db.refresh(new_account)
  return new_account 

@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  account = account_lookup(account_id, db, current_user["id"])
  db.delete(account)
  db.commit()
  return

@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_user_account(account_id: int, account_data: AccountCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  account = account_lookup(account_id, db, current_user["id"])
  
  account.bank_name = account_data.bank_name
  account.account_type = account_data.account_type
  account.balance = account_data.balance 
  db.commit() 
  db.refresh(account)
  return account