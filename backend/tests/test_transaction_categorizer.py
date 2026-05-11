from unittest.mock import patch, AsyncMock 

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_transaction_categorizer_happy_path(mock_categorizer, create_account):
  client, token, account_id, _ = create_account 
  mock_categorizer.return_value = {
    "account_id": account_id, 
    "amount": 43.67, 
    "category_name": "Food & drink", 
    "transaction_type": "expense", 
    "description": "...", "date": 
    "2026-05-10", 
    "confidence": 0.95
    }
  
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {token}"}, json = {"description": "Spent 43.67 at Chipotle", "accounts_info": accounts_info})
    
  assert response.status_code == 200
  assert response.json()["amount"] == "43.67"
  assert response.json()["account_id"] == 1 

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_bad_account_id(mock_categorizer, create_account):
  client, token, _, _ = create_account 
  mock_categorizer.return_value = {
    "account_id": 999, 
    "amount": 43.67, 
    "category_name": "Food & drink", 
    "transaction_type": "expense", 
    "description": "...", "date": 
    "2026-05-10", 
    "confidence": 0.95
    }
  
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {token}"}, json = {"description": "Spent 43.67 at Chipotle", "accounts_info": accounts_info})
    
  assert response.status_code == 422 
  assert response.json()["detail"] == "Account does not exist."

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_bad_category_name(mock_categorizer, create_account):
  client, token, account_id, _ = create_account 
  mock_categorizer.return_value = {
    "account_id": account_id, 
    "amount": 43.67, 
    "category_name": "blah blah blah blah", 
    "transaction_type": "expense", 
    "description": "...", "date": 
    "2026-05-10", 
    "confidence": 0.95
    }
  
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {token}"}, json = {"description": "Spent 43.67 at Chipotle", "accounts_info": accounts_info})
    
  assert response.status_code == 422 
  assert response.json()["detail"] == "Category does not exist."

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_transaction_categorizer_503(mock_categorizer, create_two_accounts):
  client, token, first_account_id, second_account_id= create_two_accounts 
  mock_categorizer.side_effect = Exception("Anthropic API down")
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {token}"}, json = {"description": "Spent 43.67 on Chiptole", "accounts_info": accounts_info})
    
  assert response.status_code == 503 
  assert response.json()["detail"] == "Categorization service unavailable."

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_bad_token(mock_categorizer, create_account):
  client, token, account_id, _ = create_account 
  mock_categorizer.return_value = {
    "account_id": account_id, 
    "amount": 43.67, 
    "category_name": "Food & drink", 
    "transaction_type": "expense", 
    "description": "...", "date": 
    "2026-05-10", 
    "confidence": 0.95
    }
  
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {999}"}, json = {"description": "Spent 43.67 at Chipotle", "accounts_info": accounts_info})
    
  assert response.status_code == 401

@patch("routes.transactions.transaction_categorizer", new_callable=AsyncMock)
def test_wrong_user(mock_categorizer, create_two_users):
  client, first_token, second_token = create_two_users 
  #first user account
  account = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  mock_categorizer.return_value = {
    "account_id": account.json()["id"], 
    "amount": 43.67, 
    "category_name": "Food & drink", 
    "transaction_type": "expense", 
    "description": "...", "date": 
    "2026-05-10", 
    "confidence": 0.95
    }
  
  accounts = client.get("/accounts", headers = {"Authorization" : f"Bearer {first_token}"})
  accounts_info = [{"id": a["id"], "name": a["bank_name"], "type": a["account_type"]} for a in accounts.json()]
  response = client.post("/transactions/categorize", headers = {"Authorization" : f"Bearer {second_token}"}, json = {"description": "Spent 43.67 at Chipotle", "accounts_info": accounts_info})
    
  assert response.status_code == 422 
  assert response.json()["detail"] == "Account does not exist."