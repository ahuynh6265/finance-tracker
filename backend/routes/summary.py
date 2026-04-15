from fastapi import APIRouter, Depends 
from sqlalchemy import func
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction, Account, Goal
from schemas import SummaryResponse, AccountSummaryResponse
from dependencies import calculate_account_monthly_flows, account_lookup
import auth

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
def get_user_summary(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):  
  accounts_balance = db.query(func.sum(Account.balance)).filter(Account.user_id == current_user["id"]).scalar() or 0
  goals_balance = db.query(func.sum(Goal.current_amount)).filter(Goal.user_id == current_user["id"]).scalar() or 0
  total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user["id"], Transaction.transaction_type == "income").scalar() or 0
  total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user["id"], Transaction.transaction_type == "expense").scalar() or 0

  return {
    "income": total_income,
    "expenses": total_expense,
    "net balance": accounts_balance + goals_balance, 
    "accounts_only": accounts_balance,
    "goals_only": goals_balance
  }

@router.get("/accounts/{account_id}/summary", response_model=AccountSummaryResponse)
def get_account_summary(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  account = account_lookup(account_id, db, current_user["id"])
  income, expense = calculate_account_monthly_flows(account, db, current_user["id"])

  return {
    "income": income,
    "expenses": expense
  }
