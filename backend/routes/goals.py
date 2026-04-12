from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session 
from database import get_db 
from models import Goal, Transaction, Category
from schemas import GoalCreate, GoalResponse, GoalUpdate
from dependencies import goal_lookup, account_lookup
import auth 
from datetime import date

router =  APIRouter()

@router.get("/goals", response_model=list[GoalResponse]) 
def get_user_goals(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  goals = db.query(Goal).filter(Goal.user_id == current_user["id"]).all()
  return goals 

@router.get("/goals/{goal_id}", response_model=GoalResponse)
def get_user_goal(goal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  goal = goal_lookup(goal_id, db, current_user["id"])
  return goal 

@router.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal_data: GoalCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  new_goal = Goal(
    user_id = current_user["id"], 
    name = goal_data.name,
    target_amount = goal_data.target_amount, 
    deadline = goal_data.deadline
  )
  db.add(new_goal)
  db.commit()
  db.refresh(new_goal)
  return new_goal 

@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  goal = goal_lookup(goal_id, db, current_user["id"])  
  #placeholder for transfer transaction type 
  if goal.current_amount > 0: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There is money currently stored in this fund, can not be deleted.")
  db.delete(goal)
  db.commit()
  return 

@router.put("/goals/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, goal_data: GoalCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  goal = goal_lookup(goal_id, db, current_user["id"])
  goal.name = goal_data.name
  goal.target_amount = goal_data.target_amount
  goal.deadline = goal_data.deadline 
  db.commit()
  db.refresh(goal)
  return goal 

@router.put("/goals/{goal_id}/current-amount", response_model=GoalResponse)
def update_current_amount(goal_id, update_data: GoalUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  goal = goal_lookup(goal_id, db, current_user["id"])
  account = account_lookup(update_data.account_id, db, current_user["id"])
  category = db.query(Category).filter(Category.user_id == current_user["id"], Category.name == "Transfer").first()

  if update_data.amount > account.balance:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account does not have enough money for this transfer.")
  
  create_transaction = Transaction(
    user_id = current_user["id"], 
    account_id = update_data.account_id, 
    category_id = category.id, 
    destination_goal_id = goal.id, 
    amount = update_data.amount, 
    transaction_type = "transfer", 
    description  = f"Transfer to {goal.name}",
    date = date.today()
  )

  account.balance -= update_data.amount  
  goal.current_amount += update_data.amount
  db.add(create_transaction)
  db.commit()
  db.refresh(create_transaction)
  db.refresh(account)
  db.refresh(goal)
  return goal

@router.put("/goals/{goal_id}/withdraw", response_model=GoalResponse)
def withdraw_from_goal(goal_id: int, update_data: GoalUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  goal = goal_lookup(goal_id, db, current_user["id"])
  account = account_lookup(update_data.account_id, db, current_user["id"])
  category = db.query(Category).filter(Category.user_id == current_user["id"], Category.name == "Transfer").first()

  if update_data.amount > goal.current_amount:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Can not withdraw more than you currently have in the fund.")
  
  #SOURCE AND DESTINATION SWITCHED BECAUSE USER IS WITHDRAWING FROM GOAL FUND MEANING GOAL ID IS NOW THE SOURCE AND THE ACCOUNT THE MONEY IS BEING RETURNED TO IS THE SOURCE
  #note that for withdrawals account id does not have to be the same account id used to fund goal, can be withdrawn into another of the user's account
  create_transaction = Transaction(
    user_id = current_user["id"], 
    account_id = update_data.account_id, #DESTINATION
    category_id = category.id, 
    destination_goal_id = goal.id, #SOURCE
    amount = update_data.amount, 
    transaction_type = "transfer", 
    description  = f"Withdrawal from {goal.name}",
    date = date.today()
  )
  #logic is flipped as well
  goal.current_amount -= update_data.amount 
  account.balance += update_data.amount 
  db.add(create_transaction)
  db.commit()
  db.refresh(create_transaction)
  db.refresh(account)
  db.refresh(goal)
  return goal
