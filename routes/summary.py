from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction, Account
from schemas import SummaryResponse
from dependencies import user_lookup

router = APIRouter()

@router.get("/users/{user_id}/summary", response_model=SummaryResponse)
def get_user_summary(user_id: int, db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  
  checking_savings = db.query(Account).filter(Account.user_id == user_id).filter(Account.account_type != "credit").all()
  credit = db.query(Account).filter(Account.user_id == user_id).filter(Account.account_type == "credit").all()

  net_balance = round(sum(a.balance for a in checking_savings) + sum(c.balance for c in credit), 2)

  income = db.query(Transaction).filter(Transaction.transaction_type == "income").filter(Transaction.user_id == user_id).all()
  total_income = sum(t.amount for t in income)
  
  total_income = round(total_income, 2)

  expense = db.query(Transaction).filter(Transaction.transaction_type == "expense").filter(Transaction.user_id == user_id).all()
  total_expense = sum(t.amount for t in expense)
  total_expense = round(total_expense, 2)
  
  return {
    "income": total_income,
    "expenses": total_expense,
    "net balance": net_balance
  }