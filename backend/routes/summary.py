from fastapi import APIRouter, Depends 
from sqlalchemy import func, extract, case 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction, Account, Goal
from schemas import SummaryResponse, AccountSummaryResponse, SummaryMonthlyResponse
from dependencies import calculate_account_monthly_flows, account_lookup
import auth
from datetime import datetime, date
from decimal import Decimal

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

@router.get("/summary/monthly", response_model=list[SummaryMonthlyResponse])
def get_monthly_summary(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  monthly_flows = db.query(
    extract("month", Transaction.date).label("month"),
    extract("year", Transaction.date).label("year"),
    func.sum(case((Transaction.transaction_type == "income", Transaction.amount),else_=0)).label("monthly_income"),
    func.sum(case((Transaction.transaction_type == "expense", Transaction.amount),else_=0)).label("monthly_expenses")
  ).filter(
    Transaction.user_id == current_user["id"],
    Transaction.transaction_type != "transfer"
  ).group_by("year", "month").order_by("year", "month").all()

  earliest_transaction = db.query(func.min(Transaction.date)).filter(Transaction.user_id == current_user["id"], Transaction.transaction_type != "transfer").scalar()
  if earliest_transaction is None: return [{"year": date.today().year, "month":  date.today().month, "income": Decimal("0.00"), "expenses": Decimal("0.00")}]
  today = date.today()
  earliest_transaction = min(earliest_transaction, today)

  monthly_flows_all = {}
  output_list = []
  for flow in monthly_flows: 
    monthly_flows_all[(flow.year, flow.month)] = (flow.monthly_income, flow.monthly_expenses)

  year, month = earliest_transaction.year, earliest_transaction.month
  while (year, month) <= (today.year, today.month):
    if (year, month) in monthly_flows_all: 
       income, expense = monthly_flows_all[(year, month)]
       output_list.append({"year": year, "month": month, "income": income, "expenses": expense})
    else:
      output_list.append({"year": year, "month": month, "income": Decimal("0.00"), "expenses": Decimal("0.00")})
    
    if month == 12: 
      year += 1
      month = 1
    else: month += 1
  
  return output_list

@router.get("/accounts/{account_id}/summary", response_model=AccountSummaryResponse)
def get_account_summary(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  account = account_lookup(account_id, db, current_user["id"])
  income, expense = calculate_account_monthly_flows(account, db, current_user["id"])

  return {
    "income": income,
    "expenses": expense
  }
