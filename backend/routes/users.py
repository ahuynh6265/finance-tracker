from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import User 
from schemas import UserCreate, UserResponse
from dependencies import user_lookup

router = APIRouter() 

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  user = user_lookup(user_id, db)
  return user 

@router.post("/users", response_model=list[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(users_data: list[UserCreate], db: Session = Depends(get_db)):
  new_users = [User (name = u.name, email = u.email) for u in users_data]
  db.add_all(new_users)
  db.commit() 
  for user in new_users:
    db.refresh(user)
  return new_users

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
  user = user_lookup(user_id, db)
  user.name = user_data.name
  user.email = user_data.email 
  db.commit() 
  db.refresh(user)
  return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  user = user_lookup(user_id, db)
  db.delete(user)
  db.commit()
  return 