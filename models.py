from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class User(Base): 
  __tablename__ = "user"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  category = relationship("Category", back_populates="user", cascade="all, delete")
  account = relationship("Account", back_populates="user", cascade="all, delete")
  transaction = relationship("Transaction", back_populates="user", cascade="all, delete")

class Category(Base): 
  __tablename__ ="category"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
  name = Column(String, nullable=False)

  user = relationship("User", back_populates="category")
  transaction = relationship("Transaction", back_populates="category", cascade="all, delete")
  
class Account(Base): 
  __tablename__="account"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
  bank_name = Column(String, nullable=False)
  account_type = Column(String, nullable=False)
  balance = Column(Float, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="account")
  transaction = relationship("Transaction", back_populates="account", cascade="all, delete")

class Transaction(Base): 
  __tablename__="transaction"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
  account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
  category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
  amount = Column(Float, nullable=False)
  transaction_type = Column(String, nullable=False)
  description = Column(String, nullable=False)
  date = Column(Date, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

  user = relationship("User", back_populates="transaction")
  category = relationship("Category", back_populates="transaction")
  account = relationship("Account", back_populates="transaction")