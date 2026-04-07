from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session 
from database import get_db
from models import User, Category 
from schemas import UserCreate, UserLogin, UserResponse, RefreshRequest 
import auth 

router = APIRouter()
categories = ["Automotive", "Bills & utilities", "Cash out", "Education", "Entertainment", "Food & drink", "Gas", "Groceries", "Misc.", "Personal", "Shopping", "Travel"]

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == user_data.email).first()
  if user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email has already been registered.")
  user = User(name = user_data.name, email= user_data.email, hashed_password = auth.hash_password(user_data.password))
  db.add(user)
  db.commit()
  db.refresh(user)

  set_categories = []
  for category in categories:
    set_category = Category(user_id = user.id, name = category)
    set_categories.append(set_category)
  db.add_all(set_categories)
  db.commit()

  return user 

@router.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == user_data.email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password incorrect.")
  
  if not auth.verify_password(user_data.password, user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password incorrect.")
  
  access_token, refresh_token = auth.create_token(user.name, user_data.email, user.id)
  return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "name": user.name} 
  
  
@router.get("/auth/me")
def get_email(token: dict = Depends(auth.get_current_user)):
  return token["email"]

@router.post("/auth/refresh")
def refresh(refresh_token: RefreshRequest):
  new_access_token = auth.refresh_access_token(refresh_token.refresh_token)
  return {"access_token": new_access_token, "token_type": "bearer"}