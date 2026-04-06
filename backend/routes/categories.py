from fastapi import APIRouter, status, Depends 
from sqlalchemy.orm import Session 
from database import get_db 
from models import Category
from schemas import CategoryResponse
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

@router.delete("/categories/{category_id}/transactions",  status_code=status.HTTP_204_NO_CONTENT)
def delete_category_transactions(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  category = category_lookup(category_id, db, current_user["id"])

  for transaction in category.transactions: 
    account = account_lookup(transaction.account_id, db, current_user["id"])
    adjust_balance(account, transaction, True)
    db.delete(transaction)

  db.commit()
  return 