from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import get_db
from models import Budget, Transaction, Category
from schemas import BudgetCreate, BudgetResponse, BudgetUpdate, BudgetChartResponse
from dependencies import budget_lookup, category_lookup, calculate_category_spending
import auth 
from sqlalchemy import func, extract
from datetime import datetime
from decimal import Decimal

router = APIRouter()

@router.get("/budgets", response_model=list[BudgetResponse])
def get_budgets(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  budgets = db.query(Budget).filter(Budget.user_id == current_user["id"]).all()

  for budget in budgets: 
    category = category_lookup(budget.category_id, db, current_user["id"])
    current_total = calculate_category_spending(category, db, current_user["id"])
    budget.current_total = current_total

  return budgets

@router.get("/budgets/chart-data", response_model=list[BudgetChartResponse])
def get_budgets_charts(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  categories = db.query(Category).filter(Category.user_id == current_user["id"], Category.name != "Transfer").all()
  current_year = datetime.now().year

  totals_per_category = []
  for category in categories:
    monthly_total = db.query(
      extract("month", Transaction.date).label("month"), 
      func.sum(Transaction.amount)
      ).filter(
        Transaction.user_id == current_user["id"], 
        Transaction.category_id == category.id, 
        Transaction.transaction_type == "expense", 
        extract("year", Transaction.date) == current_year
        ).group_by(Transaction.category_id, "month").all()
    
    monthly_total_dict = dict(monthly_total)
    totals_per_category.append({
      "category_id": category.id,
      "category_name": category.name, 
      "monthly_totals": [monthly_total_dict.get(m, Decimal("0.00")) for m in range (1, 13)]
    })

  return totals_per_category

@router.get("/budgets/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  budget = budget_lookup(budget_id, db, current_user["id"])
  category = category_lookup(budget.category_id, db, current_user["id"])
  current_total = calculate_category_spending(category, db, current_user["id"])
  budget.current_total = current_total 
  return budget

@router.post("/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget_data: BudgetCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  #if the category has a budget made by a different user, it won't affect this user's ability to make a budget for the same category
  budget = db.query(Budget).filter(Budget.category_id == budget_data.category_id, Budget.user_id == current_user["id"]).first()

  #prevents user from making a budget for category if the budget already exists
  if budget: 
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{budget.category.name} has a budget made already.")
  
  new_budget = Budget(user_id = current_user["id"], category_id = budget_data.category_id, budget_limit = budget_data.budget_limit)

  category = category_lookup(new_budget.category_id, db, current_user["id"])
  current_total = calculate_category_spending(category, db, current_user["id"])

  db.add(new_budget)
  db.commit()
  db.refresh(new_budget)
  new_budget.current_total = current_total #move after refresh - prevents the current total from being wiped since the current total is not apart of the budget model 
  return new_budget

@router.delete("/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  budget = budget_lookup(budget_id, db, current_user["id"])
  db.delete(budget)
  db.commit()
  return 

@router.patch("/budgets/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, budget_data: BudgetUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  budget = budget_lookup(budget_id, db, current_user["id"])

  #don't set a new category id because the category can only have one budget
  budget.budget_limit = budget_data.budget_limit

  category = category_lookup(budget.category_id, db, current_user["id"])
  current_total = calculate_category_spending(category, db, current_user["id"])

  db.commit()
  db.refresh(budget)
  budget.current_total = current_total
  return budget
  