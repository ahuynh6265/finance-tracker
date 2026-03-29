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
  
  user_accounts = db.query(Account).filter(Account.user_id == user_id).all()
  net_balance = round(sum(a.balance for a in user_accounts), 2)
  income = db.query(Transaction).filter(Transaction.transaction_type == "income").filter(Transaction.user_id == user_id).all()

  total_income = round(sum(t.amount for t in income), 2)

  expense = db.query(Transaction).filter(Transaction.transaction_type == "expense").filter(Transaction.user_id == user_id).all()
  total_expense = sum(t.amount for t in expense)
  total_expense = round(total_expense, 2)
  
  return {
    "income": total_income,
    "expenses": total_expense,
    "net balance": net_balance
  }