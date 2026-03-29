from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Category
from schemas import CategoryCreate, CategoryResponse
from dependencies import user_lookup, category_lookup, account_lookup

router = APIRouter()

@router.get("/users/{user_id}/categories", response_model=list[CategoryResponse])
def get_user_categories(user_id: int, db: Session =  Depends(get_db)):
  user = user_lookup(user_id, db)
  return user.category 

@router.get("/users/{user_id}/categories/{category_id}", response_model=CategoryResponse)
def get_user_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  category = category_lookup(category_id, db, user_id)
  return category

@router.post("/users/{user_id}/categories", response_model=list[CategoryResponse], status_code=status.HTTP_201_CREATED)
def create_user_categories(user_id: int, categories_data: list[CategoryCreate], db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  new_categories = [Category (user_id = user_id, name = c.name)for c in categories_data]
  db.add_all(new_categories)
  db.commit() 
  for category in new_categories:
    db.refresh(category)
  return new_categories 

@router.put("/users/{user_id}/categories/{category_id}", response_model=CategoryResponse)
def update_user_category(user_id: int, category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db)): 
  user_lookup(user_id, db)
  category = category_lookup(category_id, db, user_id) 
  
  category.name = category_data.name
  db.commit()
  db.refresh(category)
  return category

@router.delete("/users/{user_id}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user_lookup(user_id, db)
  category = category_lookup(category_id, db, user_id) 
  
  for transaction in category.transaction:
    account = account_lookup(transaction.account_id, db)
    if account:
      if transaction.transaction_type =="income":
        account.balance -= transaction.amount
      else:
        account.balance += transaction.amount
  
  db.delete(category)
  db.commit() 
  return 