from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date 
from enum import Enum 

class AccountType(str, Enum):
  checking = "checking"
  savings = "savings"
  credit = "credit"

class TransactionType(str, Enum):
  income = "income"
  expense = "expense"

class SummaryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True, populate_by_name=True)

  income: float 
  expenses: float 
  net_balance: float = Field(alias="net balance")

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
  balance: float = Field(ge=0)

class AccountResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  bank_name: str 
  account_type: AccountType
  balance: float
  created_at: datetime 
  updated_at: datetime

#transaction
class TransactionCreate(BaseModel):
  account_id: int 
  category_id: int
  amount: float = Field(gt=0)
  transaction_type: TransactionType
  description: str = Field(min_length=1)
  date: date

class TransactionResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  account_id: int 
  category_id: int
  amount: float 
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