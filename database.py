from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv 
import os 

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

connect_args = {"sslmode": "require"} if DATABASE_URL and DATABASE_URL.startswith("postgresql") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

class Base(DeclarativeBase):
  pass