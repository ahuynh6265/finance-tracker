def test_get_budgets(create_account):
  client, token, _ , _ = create_account
  response = client.get("/budgets", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200

def test_create_budgets(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  assert response.status_code == 201
  assert response.json()["category_id"] == 1
  assert response.json()["budget_limit"] == "500.00"

def test_bad_zero_limit(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "0"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Budget limit can't be zero."

def test_bad_negative_limit(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "-1"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Budget limit can't be negative."

def test_duplicate_budget(create_account):
  client, token, _ , category_id = create_account
  client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  category = client.get(f"/categories/{category_id}", headers ={"Authorization" : f"Bearer {token}"})
  name = category.json()["name"]

  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "750.00"
  })

  assert response.status_code == 409
  assert response.json()["detail"] == f"{name} has a budget made already."

def test_delete(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  response = client.delete(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204 

def test_bad_delete(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = 999

  response = client.delete(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 404
  assert response.json()["detail"] == "Budget ID not found"

def test_wrong_user_delete(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  second_client = client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_client  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_client.json()["access_token"]

  response = client.delete(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {second_token}"})
  assert response.status_code == 403
  assert response.json()["detail"] == f"Budget ID {budget_id} does not belong to user" 

def test_patch(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  response = client.patch(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {"budget_limit": "575.75"})
  assert response.status_code == 200
  assert response.json()["budget_limit"] == "575.75"

def test_zero_budget_patch(create_account): 
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  response = client.patch(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {"budget_limit": "0"})

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Budget limit can't be zero."

def test_negative_budget_patch(create_account): 
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  response = client.patch(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {"budget_limit": "-0.5"})

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Budget limit can't be negative."

def test_nonexisting_patch(create_account):
  client, token, _ , category_id = create_account
  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = 999 
  response = client.patch(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {"budget_limit": "100"})

  assert response.status_code == 404 
  assert response.json()["detail"] == "Budget ID not found"

def test_calculate_category_spending(create_account):
  client, token, account_id, category_id = create_account
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "20.00",
    "transaction_type": "expense", 
    "description": "Bolay", 
    "date": "2026-04-07"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "122.22",
    "transaction_type": "expense", 
    "description": "Chick fil a", 
    "date": "2026-03-12"
  })

  response = client.post("/budgets", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "category_id": category_id, 
    "budget_limit": "500.00"
  })
  budget_id = response.json()["id"]

  response = client.get(f"/budgets/{budget_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert response.status_code == 200 
  #should only total this month's(april) spend on this catergory
  assert response.json()["current_total"] == "32.57"
