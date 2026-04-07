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