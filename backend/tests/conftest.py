import pytest
from starlette.testclient import TestClient 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app 
import models

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal =  sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

def override_get_db():
  db = TestingSessionLocal()
  try: yield db
  finally: db.close()

app.dependency_overrides[get_db] = override_get_db 

@pytest.fixture
def test_app():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  client = TestClient(app)
  yield client 
  Base.metadata.drop_all(bind=engine)

@pytest.fixture 
def register_login_user(test_app):
  response = test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  response = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})

  return test_app, response.json()["access_token"]

@pytest.fixture
def create_account(register_login_user):
  client, token = register_login_user
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  account_id, category_id = response.json()["id"], 1

  return client, token, account_id, category_id 

@pytest.fixture
def create_two_accounts(register_login_user): 
  client, token = register_login_user
  first_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "savings", "balance": "1500"})
  first_account_id = first_account.json()["id"]
  second_account_id = second_account.json()["id"]

  return client, token, first_account_id, second_account_id

@pytest.fixture 
def create_two_users(test_app):
  test_app.post("/auth/register", json = {"name": "Test", "email": "test@test.com", "password": "password123"})
  first = test_app.post("/auth/login", json = {"email": "test@test.com", "password": "password123"})
  test_app.post("/auth/register", json = {"name": "Alex", "email": "alex@test.com", "password": "alex"})
  second = test_app.post("/auth/login", json = {"email": "alex@test.com", "password": "alex"})

  return test_app, first.json()["access_token"], second.json()["access_token"]

@pytest.fixture 
def create_transactions(create_account):
  client, token, account_id, _ = create_account
  def _transaction(category_id, amount, date, account_id=account_id, transaction_type="expense"):
    response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": amount,
    "transaction_type": transaction_type, 
    "description": "Description", 
    "date": date
    })
    return response
  return _transaction


