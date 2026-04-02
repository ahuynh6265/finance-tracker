from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session 
from database import get_db
from models import User 
from schemas import UserCreate, UserLogin, UserResponse 
import auth 

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == user_data.email).first()
  if user:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email has already been registered.")
  user = User(name = user_data.name, email= user_data.email, hashed_password = auth.hash_password(user_data.password))
  db.add(user)
  db.commit()
  db.refresh(user)
  return user 

@router.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == user_data.email).first()
  if user: 
    if auth.verify_password(user_data.password, user.hashed_password):
      token = auth.create_token(user_data.email, user.id)
      return {"access_token": token, "token_type": "bearer"} 
    else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password incorrect.")
  
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password incorrect")
  
@router.get("/auth/me")
def get_email(token: dict = Depends(auth.get_current_user)):
  return token["email"]
