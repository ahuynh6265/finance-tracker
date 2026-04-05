from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date 
from enum import Enum 
from decimal import Decimal

class AccountType(str, Enum):
  checking = "checking"
  savings = "savings"
  credit = "credit"

class TransactionType(str, Enum):
  income = "income"
  expense = "expense"

class SummaryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True, populate_by_name=True)

  income: Decimal 
  expenses: Decimal 
  net_balance: Decimal = Field(alias="net balance")

#category 
class CategoryCreate(BaseModel): 
  name: str = Field(min_length=1)

class CategoryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int
  name: str 

#account 
class AccountCreate(BaseModel):
  bank_name: str = Field(min_length=1)
  account_type: AccountType
  balance: Decimal = Field(ge=0)

class AccountResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  bank_name: str 
  account_type: AccountType
  balance: Decimal
  created_at: datetime 
  updated_at: datetime

#transaction
class TransactionCreate(BaseModel):
  account_id: int 
  category_id: int
  amount: Decimal = Field(gt=0)
  transaction_type: TransactionType
  description: str = Field(min_length=1)
  date: date

class TransactionResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  account_id: int 
  category_id: int
  amount: Decimal 
  transaction_type: TransactionType
  description: str
  date: date 
  created_at: datetime

#users 
class UserCreate(BaseModel): 
  name: str = Field(min_length=1)
  email: str = Field(min_length=5)
  password: str 

class UserResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  name: str 
  email: str 
  created_at: datetime 
  updated_at: datetime
  
class UserLogin(BaseModel):
  email: str 
  password: str

class BudgetCreate(BaseModel):
  category_id: int 
  budget_limit: Decimal = Field(gt=0)

class BudgetUpdate(BaseModel):
  budget_limit: Decimal = Field(gt=0)
class BudgetResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  user_id: int 
  category_id: int 
  current_total: Decimal
  budget_limit: Decimal 
  created_at: datetime
  updated_at: datetime

class RefreshRequest(BaseModel):
  refresh_token: str 