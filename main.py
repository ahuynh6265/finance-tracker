from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session 
from database import engine, SessionLocal, Base
from models import User, Category, Account, Transaction
from schemas import UserCreate, UserResponse, CategoryCreate, CategoryResponse, AccountCreate, AccountResponse, TransactionCreate, TransactionResponse, SummaryResponse

app = FastAPI() 
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"DB init warning: {e}")

def get_db():
  db = SessionLocal()
  try: yield db
  finally: db.close() 

#user routes 
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
  return db.query(User).all() 

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  return user 

@app.post("/users", response_model=list[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(users_data: list[UserCreate], db: Session = Depends(get_db)):
  new_users = [User (name = u.name, email = u.email) for u in users_data]
  db.add_all(new_users)
  db.commit()
  for user in new_users:
    db.refresh(user)
  return new_users 

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  user.name = user_data.name
  user.email = user_data.email 
  db.commit() 
  db.refresh(user)
  return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  db.delete(user)
  db.commit()
  return 

#category routes
@app.get("/users/{user_id}/categories", response_model=list[CategoryResponse])
def get_user_categories(user_id: int, db: Session =  Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  return user.category 

@app.get("/users/{user_id}/categories/{category_id}", response_model=CategoryResponse)
def get_user_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  category = db.query(Category).filter(category_id == Category.id).first() 

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category ID not found")
  
  if category.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to {user.name}")
  return category

@app.post("/users/{user_id}/categories", response_model=list[CategoryResponse], status_code=status.HTTP_201_CREATED)
def create_user_categories(user_id: int, categories_data: list[CategoryCreate], db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  new_categories = [Category (user_id = user_id, name = c.name)for c in categories_data]
  db.add_all(new_categories)
  db.commit() 
  for category in new_categories:
    db.refresh(category)
  return new_categories 

@app.put("/users/{user_id}/categories/{category_id}", response_model=CategoryResponse)
def update_user_category(user_id: int, category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  category = db.query(Category).filter(category_id == Category.id).first() 

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category ID not found")
  
  if category.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to {user.name}")
  
  category.name = category_data.name
  db.commit()
  db.refresh(category)
  return category

@app.delete("/users/{user_id}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  category = db.query(Category).filter(category_id == Category.id).first() 

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category ID not found")
  
  if category.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to {user.name}")
  
  db.delete(category)
  db.commit() 
  return 

#account routes 
@app.get("/users/{user_id}/accounts", response_model=list[AccountResponse])
def get_user_accounts(user_id: int, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  return user.account 

@app.get("/users/{user_id}/accounts/{account_id}", response_model=AccountResponse)
def get_user_account(user_id: int, account_id: int, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first() 
  account = db.query(Account).filter(account_id ==  Account.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account ID not found")
  
  if account.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to {user.name}")
  
  return account 

@app.post("/users/{user_id}/accounts", response_model=list[AccountResponse], status_code=status.HTTP_201_CREATED)
def create_user_accounts(user_id: int, accounts_data: list[AccountCreate], db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  
  new_accounts = [Account (
    user_id = user_id, 
    bank_name = a.bank_name, 
    account_type = a.account_type, 
    balance = a.balance
  ) for a in accounts_data] 
  db.add_all(new_accounts)
  db.commit() 
  for account in new_accounts:
    db.refresh(account)
  return new_accounts 

@app.delete("/users/{user_id}/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(user_id: int, account_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first() 
  account = db.query(Account).filter(account_id ==  Account.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account ID not found")
  
  if account.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to {user.name}")
  db.delete(account)
  db.commit()
  return

@app.put("/users/{user_id}/accounts/{account_id}", response_model=AccountResponse)
def update_user_account(user_id: int, account_id: int, account_data: AccountCreate, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first() 
  account = db.query(Account).filter(account_id ==  Account.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account ID not found")
  
  if account.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to {user.name}")
  
  account.bank_name = account_data.bank_name
  account.account_type = account_data.account_type
  account.balance = account_data.balance 
  db.commit() 
  db.refresh(account)
  return account

#transaction routes
#get route from users 
@app.get("/users/{user_id}/transactions", response_model=list[TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  return user.transaction

#standard single get route
@app.get("/users/{user_id}/transactions/{transaction_id}", response_model=TransactionResponse) 
def get_user_transaction(user_id: int, transaction_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  transaction = db.query(Transaction).filter(transaction_id == Transaction.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  elif not transaction: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found") 
  
  if transaction.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Transaction ID {transaction_id} does not belong to {user.name}")
  return transaction 

#get route from user/category 
@app.get("/users/{user_id}/categories/{category_id}/transactions", response_model=list[TransactionResponse])
def get_category_transactions(user_id: int, category_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first()
  category = db.query(Category).filter(category_id == Category.id).first() 

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category ID not found")
  
  if category.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Category ID {category_id} does not belong to {user.name}")
  return category.transaction 

#get route from user/account 
@app.get("/users/{user_id}/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_account_transactions(user_id: int, account_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(user_id == User.id).first() 
  account = db.query(Account).filter(account_id ==  Account.id).first() 
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  elif not account: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account ID not found")
  
  if account.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Account ID {account_id} does not belong to {user.name}")
  return account.transaction

@app.post("/users/{user_id}/transactions", response_model=list[TransactionResponse], status_code=status.HTTP_201_CREATED)
def create_user_transactions(user_id: int, transactions_data: list[TransactionCreate], db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
  new_transactions = []
  for t in transactions_data:
    new_transaction= Transaction (
    user_id = user_id,
    account_id = t.account_id,
    category_id = t.category_id,
    amount = t.amount,
    transaction_type = t.transaction_type, 
    description = t.description,
    date = t.date
    )
    new_transactions.append(new_transaction)

    account = db.query(Account).filter(t.account_id == Account.id).first() 
    if account:
      if t.transaction_type == "income":
        account.balance += t.amount
      else:
        account.balance -= t.amount

  db.add_all(new_transactions)
  db.commit() 
  for transaction in new_transactions:
    db.refresh(transaction)
  return new_transactions 

@app.delete("/users/{user_id}/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_transaction(user_id: int, transaction_id: int, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  transaction = db.query(Transaction).filter(transaction_id == Transaction.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  elif not transaction: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found") 
  
  if transaction.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Transaction ID {transaction_id} does not belong to {user.name}")
  
  account = db.query(Account).filter(transaction.account_id == Account.id).first() 
  if transaction.transaction_type == "income":
    account.balance -= transaction.amount
  else:
    account.balance += transaction.amount
    

  db.delete(transaction)
  db.commit()
  return

@app.put("/users/{user_id}/transactions/{transaction_id}", response_model=TransactionResponse)
def update_user_transaction(user_id: int, transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  transaction = db.query(Transaction).filter(transaction_id == Transaction.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  elif not transaction: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found") 
  
  if transaction.user_id != user_id: 
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Transaction ID {transaction_id} does not belong to {user.name}")
  transaction.account_id = transaction_data.account_id
  transaction.category_id = transaction_data.category_id
  transaction.amount = transaction_data.amount
  transaction.transaction_type = transaction_data.transaction_type
  transaction.description = transaction_data.description 
  transaction.date = transaction_data.date
  db.commit() 
  db.refresh(transaction)
  return transaction 

#summary endpoint 
@app.get("/users/{user_id}/summary", response_model=SummaryResponse)
def get_user_summary(user_id: int, db: Session = Depends(get_db)): 
  user = db.query(User).filter(user_id == User.id).first()
  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found") 
  
  checking_savings = db.query(Account).filter(Account.user_id == user_id).filter(Account.account_type != "credit").all()
  credit = db.query(Account).filter(Account.user_id == user_id).filter(Account.account_type == "credit").all()

  net_balance = round(sum(a.balance for a in checking_savings) - sum(c.balance for c in credit), 2)

  income = db.query(Transaction).filter(Transaction.transaction_type == "income").filter(Transaction.user_id == user_id).all()
  total_income = sum(t.amount for t in income)
  
  total_income = round(total_income, 2)

  expense = db.query(Transaction).filter(Transaction.transaction_type == "expense").filter(Transaction.user_id == user_id).all()
  total_expense = sum(t.amount for t in expense)
  total_expense = round(total_expense, 2)
  
  return {
    "income": total_income,
    "expenses": total_expense,
    "net balance": net_balance
  }
  