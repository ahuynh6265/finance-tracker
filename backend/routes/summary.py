from fastapi import APIRouter, Depends 
from sqlalchemy import func
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction, Account, Goal
from schemas import SummaryResponse
import auth

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
def get_user_summary(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):  
  accounts_balance = db.query(func.sum(Account.balance)).filter(Account.user_id == current_user["id"]).scalar()
  goals_balance = db.query(func.sum(Goal.current_amount)).filter(Goal.user_id == current_user["id"]).scalar()
  total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user["id"], Transaction.transaction_type == "income").scalar()
  total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user["id"], Transaction.transaction_type == "expense").scalar()

  return {
    "income": round(total_income, 2),
    "expenses": round(total_expense, 2), 
    "net balance": round(accounts_balance + goals_balance, 2)
  }