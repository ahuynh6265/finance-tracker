from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Category
from schemas import CategoryCreate, CategoryResponse
from dependencies import category_lookup, account_lookup, adjust_balance
import auth

router = APIRouter()

@router.get("/categories", response_model=list[CategoryResponse])
def get_user_categories(db: Session =  Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  categories = db.query(Category).filter(Category.user_id == current_user["id"]).all()
  return categories

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_user_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  category = category_lookup(category_id, db, current_user["id"])
  return category

@router.post("/categories", response_model=list[CategoryResponse], status_code=status.HTTP_201_CREATED)
def create_user_categories(categories_data: list[CategoryCreate], db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  new_categories = [Category (user_id = current_user["id"], name = c.name)for c in categories_data]
  db.add_all(new_categories)
  db.commit() 
  for category in new_categories:
    db.refresh(category)
  return new_categories 

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_user_category(category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  category = category_lookup(category_id, db, current_user["id"]) 
  
  category.name = category_data.name
  db.commit()
  db.refresh(category)
  return category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  category = category_lookup(category_id, db, current_user["id"]) 
  
  for transaction in category.transactions:
    account = account_lookup(transaction.account_id, db, current_user["id"])
    adjust_balance(account, transaction, True)
  
  db.delete(category)
  db.commit() 
  return 