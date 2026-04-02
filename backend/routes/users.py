from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import User 
from schemas import UserCreate, UserResponse
import auth 

router = APIRouter() 

@router.put("/users/me", response_model=UserResponse)
def update_user(user_data: UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  user = db.query(User).filter(User.id == current_user["id"]).first()
  user.name = user_data.name
  user.email = user_data.email 
  
  db.commit() 
  db.refresh(user)
  return user

@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  user = db.query(User).filter(User.id == current_user["id"]).first()

  db.delete(user)
  db.commit()
  return 