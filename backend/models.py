from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class User(Base): 
  __tablename__ = "user"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False, unique=True)
  hashed_password = Column(String, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  categories = relationship("Category", back_populates="user", cascade="all, delete")
  accounts = relationship("Account", back_populates="user", cascade="all, delete")
  transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
  budgets = relationship("Budget", back_populates="user", cascade="all, delete")
  goals = relationship("Goal", back_populates="user", cascade="all, delete")

class Category(Base): 
  __tablename__ ="category"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  name = Column(String, nullable=False)

  user = relationship("User", back_populates="categories")
  transactions = relationship("Transaction", back_populates="category")
  budget = relationship("Budget", back_populates="category", uselist=False)
  
class Account(Base): 
  __tablename__="account"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  bank_name = Column(String, nullable=False)
  account_type = Column(String, nullable=False)
  balance = Column(Numeric(10,2), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="accounts")
  transactions = relationship("Transaction", back_populates="account", cascade="all, delete", foreign_keys="[Transaction.account_id]")

class Transaction(Base): 
  __tablename__="transaction"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  account_id = Column(Integer, ForeignKey("account.id", ondelete="CASCADE"), nullable=False)
  category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
  destination_account_id = Column(Integer, ForeignKey("account.id", ondelete="SET NULL"), nullable=True)
  source_goal_id = Column(Integer, ForeignKey("goal.id", ondelete="SET NULL"), nullable=True)
  destination_goal_id = Column(Integer, ForeignKey("goal.id", ondelete="SET NULL"), nullable=True)
  amount = Column(Numeric(10,2), nullable=False)
  transaction_type = Column(String, nullable=False)
  description = Column(String, nullable=False)
  date = Column(Date, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="transactions")
  category = relationship("Category", back_populates="transactions")
  account = relationship("Account", back_populates="transactions", foreign_keys=[account_id]) #specify which id since both account and destination pull foreign key from same table

class Budget(Base): 
  __tablename__="budget"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  category_id = Column(Integer, ForeignKey("category.id"), nullable=False, unique=True)
  budget_limit = Column(Numeric(10,2), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="budgets")
  category = relationship("Category", back_populates="budget")

class Goal(Base):
  __tablename__ = "goal"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  name = Column(String, nullable=False)
  target_amount = Column(Numeric(10, 2), nullable=False)
  current_amount = Column(Numeric(10,2), default=0, nullable=False)
  deadline = Column(Date, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="goals")

