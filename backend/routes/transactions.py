from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session 
from database import get_db 
from models import Transaction, Category, Account
from schemas import TransactionCreate, TransactionResponse, TransactionParseRequest, TransactionParseResponse
from dependencies import transaction_lookup, category_lookup, account_lookup, adjust_balance
import auth
from limiter import limiter
from categorizer import transaction_categorizer
import structlog

router = APIRouter()
log = structlog.get_logger()

@router.get("/transactions", response_model=list[TransactionResponse])
def get_user_transactions(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  transactions = db.query(Transaction).filter(Transaction.user_id == current_user["id"]).all()
  return transactions

#standard single get route
@router.get("/transactions/{transaction_id}", response_model=TransactionResponse) 
def get_user_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  transaction = transaction_lookup(transaction_id, db, current_user["id"]) 
  return transaction 

#get route from user/category 
@router.get("/categories/{category_id}/transactions", response_model=list[TransactionResponse])
def get_category_transactions(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  category = category_lookup(category_id, db, current_user["id"])  
  return category.transactions 

#get route from user/account 
@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_account_transactions(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  account = account_lookup(account_id, db, current_user["id"]) 
  return account.transactions

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_user_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  new_transaction = Transaction(
    user_id = current_user["id"], 
    account_id = transaction_data.account_id,
    category_id = transaction_data.category_id, 
    destination_account_id = transaction_data.destination_account_id, 
    amount = transaction_data.amount, 
    transaction_type = transaction_data.transaction_type,
    description = transaction_data.description, 
    date = transaction_data.date
  )

  account = account_lookup(new_transaction.account_id, db, current_user["id"])

  if new_transaction.transaction_type == "transfer": 
    category = db.query(Category).filter(Category.user_id == current_user["id"], Category.name == "Transfer").first()

    destination_account = account_lookup(new_transaction.destination_account_id, db, current_user["id"]) 
    if new_transaction.amount > account.balance:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account does not have enough money for this transfer.")
    new_transaction.description = f"Transfer to {destination_account.bank_name}"
    new_transaction.category_id = category.id
    account.balance -= new_transaction.amount
    destination_account.balance += new_transaction.amount 
  
  else: 
    category_lookup(new_transaction.category_id, db, current_user["id"])
    adjust_balance(account, new_transaction)
    
  db.add(new_transaction)
  db.commit() 
  db.refresh(new_transaction)
  return new_transaction 

@router.post("/transactions/categorize", response_model=TransactionParseResponse)
@limiter.limit("30/minute")
async def categorize_transaction(request: Request, body: TransactionParseRequest, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  accounts = db.query(Account).filter(Account.user_id == current_user["id"]).all()
  accounts_info = [{"id": a.id, "name": a.bank_name, "type": a.account_type} for a in accounts]
  try:
    response = await transaction_categorizer(body.description, accounts_info)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Categorization service unavailable.")

  category = db.query(Category).filter(Category.name == response["category_name"], Category.user_id == current_user["id"]).first()
  if not category:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Category does not exist.")

  account = db.query(Account).filter(Account.id == response["account_id"], Account.user_id == current_user["id"]).first()
  if not account:
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Account does not exist.")
  
  destination_account_id = None
  if response["transaction_type"] == "transfer":
    destination_account = db.query(Account).filter(Account.id == response["destination_account_id"], Account.user_id == current_user["id"]).first()
    if not destination_account:
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Destination account name does not exist.")
    destination_account_id = destination_account.id

  return {
    "account_id": account.id, 
    "category_id": category.id, 
    "destination_account_id": destination_account_id, 
    "amount": response["amount"], 
    "transaction_type": response["transaction_type"], 
    "description": response["description"], 
    "date": response["date"],
    "confidence": response["confidence"]
  }

@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  transaction = transaction_lookup(transaction_id, db, current_user["id"])  
  if transaction.transaction_type == "transfer":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Transfer transactions cannot be deleted.")
   
  account = account_lookup(transaction.account_id, db, current_user["id"]) 
  adjust_balance(account, transaction, True)
    
  db.delete(transaction)
  db.commit()
  return

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_user_transaction(transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)): 
  transaction = transaction_lookup(transaction_id, db, current_user["id"]) 
  if transaction.transaction_type == "transfer":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Transfer transactions cannot be edited.")

  account = account_lookup(transaction.account_id, db, current_user["id"])
  #remove current balance before updating
  adjust_balance(account, transaction, True)

  transaction.account_id = transaction_data.account_id
  transaction.category_id = transaction_data.category_id
  transaction.amount = transaction_data.amount
  transaction.transaction_type = transaction_data.transaction_type
  transaction.description = transaction_data.description 
  transaction.date = transaction_data.date

  #check if account being updated is the same account, if it is the same account the new transaction amount will be added back into account if not the new account's balance is updated
  account = account_lookup(transaction.account_id, db, current_user["id"])
  adjust_balance(account, transaction)
  
  db.commit() 
  db.refresh(transaction)
  return transaction 