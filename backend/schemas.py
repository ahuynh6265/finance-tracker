from pydantic import BaseModel, ConfigDict,Field, field_validator, model_validator, computed_field
from datetime import datetime, date 
from enum import Enum 
from decimal import Decimal
import validators
from typing_extensions import Self

class AccountType(str, Enum):
  checking = "checking"
  savings = "savings"
  credit = "credit"

class TransactionType(str, Enum):
  income = "income"
  expense = "expense"
  transfer = "transfer"

class SummaryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True, populate_by_name=True)

  income: Decimal 
  expenses: Decimal 
  net_balance: Decimal = Field(alias="net balance")
  accounts_only: Decimal
  goals_only: Decimal

#category 
class CategoryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int
  name: str 

#account 
class AccountCreate(BaseModel):
  bank_name: str 
  account_type: AccountType
  balance: Decimal 

  @field_validator("bank_name")
  @classmethod
  def check_bank_name(cls, value: str) -> str: 
    if len(value) < 1: 
      raise ValueError("Bank name can't be left empty.")
    return value 
  
  @field_validator("balance")
  @classmethod
  def check_name(cls, value: Decimal) -> Decimal:
    if value < 0:
      raise ValueError("Balance can't be a negative number.")
    return value
class AccountResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  bank_name: str 
  account_type: AccountType
  balance: Decimal
  created_at: datetime 
  updated_at: datetime

#summary per account
class AccountSummaryResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  income: Decimal
  expenses: Decimal

  @computed_field
  @property
  def net_balance(self) -> Decimal: 
    return self.income - self.expenses

#transaction
class TransactionCreate(BaseModel):
  account_id: int 
  category_id: int
  destination_account_id: int | None = None
  amount: Decimal 
  transaction_type: TransactionType
  description: str 
  date: date

  @field_validator("amount")
  @classmethod 
  def check_amount(cls, value: Decimal) -> Decimal:
    if value == 0:
      raise ValueError("Amount can't be zero.")
    elif value < 0: 
      raise ValueError("Amount can't be negative.")
    return value
  
  @field_validator("description")
  @classmethod
  def check_description(cls, value: str) -> str:
    if len(value) < 1:
      raise ValueError("Description can't be empty.")
    return value
  
  @model_validator(mode="after")
  def check_transfer_id(self) -> Self:
    if self.transaction_type == "transfer" and not self.destination_account_id:
      raise ValueError("Please provide a valid destination to transfer to.")
    elif not self.transaction_type == "transfer" and self.destination_account_id: 
      raise ValueError("Can not add a destination.")
    return self
  
class TransactionResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int 
  user_id: int 
  account_id: int 
  category_id: int
  destination_account_id: int | None
  destination_goal_id: int | None 
  amount: Decimal 
  transaction_type: TransactionType
  description: str
  date: date 
  created_at: datetime

#users 
class UserCreate(BaseModel): 
  name: str 
  email: str 
  password: str 

  @field_validator("name")
  @classmethod
  def check_name(cls, value: str) -> str:
    name = value.replace("-", "").replace(" ", "").replace("'", "")
    if len(value) < 1: 
      raise ValueError("Name can't be left empty.")
    elif not name.isalpha():
      raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes.")
    return value

  @field_validator("email")
  @classmethod
  def check_email(cls, value: str) -> str:
    if len(value) < 1:
      raise ValueError("Email can't be left empty.")
    elif not validators.email(value):
      raise ValueError("Not a valid email.")
    return value
  
  @field_validator("password")
  @classmethod
  def check_password(cls, value: str) -> str:
    if len(value) < 1: 
      raise ValueError("Password can't be left empty.")
    return value

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
  budget_limit: Decimal

  @field_validator("budget_limit")
  @classmethod
  def check_budget_limit(cls, value: Decimal) -> Decimal:
    if value == 0:
      raise ValueError("Budget limit can't be zero.")
    elif value < 0: 
      raise ValueError("Budget limit can't be negative.")
    return value

class BudgetUpdate(BaseModel):
  budget_limit: Decimal 

  @field_validator("budget_limit")
  @classmethod
  def check_budget_limit(cls, value: Decimal) -> Decimal:
    if value == 0:
      raise ValueError("Budget limit can't be zero.")
    elif value < 0: 
      raise ValueError("Budget limit can't be negative.")
    return value
  
class BudgetResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  user_id: int 
  category_id: int 
  current_total: Decimal
  budget_limit: Decimal 
  created_at: datetime
  updated_at: datetime
  @computed_field
  @property
  def remaining_balance(self) -> Decimal: 
    return self.budget_limit - self.current_total

class BudgetChartResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  category_id: int 
  category_name: str 
  monthly_totals: list[Decimal]

class RefreshRequest(BaseModel):
  refresh_token: str 

class GoalCreate(BaseModel): 
  name: str
  target_amount: Decimal 
  deadline: date 

  @field_validator("name")
  @classmethod
  def check_name(cls, value: str) -> str:
    if len(value) < 1: 
      raise ValueError("Goal name can't be left empty.")
    return value

  @field_validator("target_amount")
  @classmethod
  def check_target_amount(cls, value: Decimal) -> Decimal:
    if value == 0:
      raise ValueError("Target amount can't be zero.")
    elif value < 0: 
      raise ValueError("Target amount can't be negative.")
    return value
  
class GoalResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  user_id: int 
  name: str
  target_amount: Decimal 
  current_amount: Decimal 
  deadline: date 
  created_at: datetime
  updated_at: datetime

class GoalUpdate(BaseModel):
  account_id: int
  amount: Decimal 

  @field_validator("amount")
  @classmethod
  def check_target_amount(cls, value: Decimal) -> Decimal:
    if value == 0:
      raise ValueError("Amount can't be zero.")
    elif value < 0: 
      raise ValueError("Amount can't be negative.")
    return value

