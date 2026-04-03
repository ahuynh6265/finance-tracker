from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import get_db
from models import Budget
from schemas import BudgetCreate, BudgetResponse, BudgetUpdate
from dependencies import budget_lookup, category_lookup, calculate_category_spending
import auth 

router = APIRouter()

@router.get("/budgets", response_model=list[BudgetResponse])
def get_budgets(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  budgets = db.query(Budget).filter(Budget.user_id == current_user["id"]).all()
  budget_list = []

  for budget in budgets: 
    category = category_lookup(budget.category_id, db, current_user["id"])
    current_total = calculate_category_spending(category)
    budget_list.append({
      "id": budget.id,
      "user_id": budget.user_id,
      "category_id": budget.category_id,
      "current_total": current_total,
      "budget_limit": budget.budget_limit,
      "created_at": budget.created_at,
      "updated_at": budget.updated_at 
    })

  return budget_list

@router.get("/budgets/{budget_id}", response_model=BudgetResponse)
def get_budget(budget_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  budget = budget_lookup(budget_id, db, current_user["id"])
  category = category_lookup(budget.category_id, db, current_user["id"])
  current_total = calculate_category_spending(category)
  return {
    "id": budget.id,
    "user_id": budget.user_id,
    "category_id": budget.category_id,
    "current_total": current_total,
    "budget_limit": budget.budget_limit,
    "created_at": budget.created_at,
    "updated_at": budget.updated_at 
  }

@router.post("/budgets", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget_data: BudgetCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  #if the category has a budget made by a different user, it won't affect this user's ability to make a budget for the same category
  budget = db.query(Budget).filter(Budget.category_id == budget_data.category_id, Budget.user_id == current_user["id"]).first()

  #prevents user from making a budget for category if the budget already exists
  if budget: 
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{budget.category.name} has a budget made already.")
  
  new_budget = Budget(user_id = current_user["id"], category_id = budget_data.category_id, budget_limit = budget_data.budget_limit)

  category = category_lookup(new_budget.category_id, db, current_user["id"])
  current_total = calculate_category_spending(category)

  db.add(new_budget)
  db.commit()
  db.refresh(new_budget)
  return {
    "id": new_budget.id, 
    "user_id": new_budget.user_id, 
    "category_id": new_budget.category_id,
    "current_total": current_total,
    "budget_limit": new_budget.budget_limit,
    "created_at": new_budget.created_at,
    "updated_at": new_budget.updated_at
  } 

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
  current_total = calculate_category_spending(category)

  db.commit()
  db.refresh(budget)
  return {
    "id": budget.id,
    "user_id": budget.user_id,
    "category_id": budget.category_id,
    "current_total": current_total,
    "budget_limit": budget.budget_limit,
    "created_at": budget.created_at,
    "updated_at": budget.updated_at 
  }

