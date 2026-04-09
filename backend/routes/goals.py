from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session 
from database import get_db 
from models import User, Goal 
from schemas import GoalCreate, GoalResponse, GoalUpdate
from dependencies import goal_lookup, account_lookup
import auth 

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

  if update_data.amount > account.balance:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account does not have enough money for this transfer.")

  account.balance -= update_data.amount  
  goal.current_amount += update_data.amount
  db.commit()
  db.refresh(account)
  db.refresh(goal)
  return goal
