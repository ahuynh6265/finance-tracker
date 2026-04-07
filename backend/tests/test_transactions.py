def test_get_transactions(create_account):
  client, token, account_id, category_id = create_account
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 

def test_create_transaction(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  assert response.status_code == 201 
  assert response.json()["user_id"] == 1
  assert response.json()["account_id"] == 1
  assert response.json()["category_id"] == 1
  assert response.json()["amount"] == "12.57"
  assert response.json()["transaction_type"] == "expense"
  assert response.json()["description"] == "Chipotle"
  assert response.json()["date"] == "2026-04-06"

def test_zero_amount(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "0",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be zero."

def test_bad_amount(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "-1",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be negative."

def test_bad_description(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "", 
    "date": "2026-04-06"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Description can't be empty."

def test_delete(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = response.json()["id"]
  response  = client.delete(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204

def test_bad_delete(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = 999
  response = client.delete(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 404 
  assert response.json()["detail"] == "Transaction ID not found"

def test_wrong_user(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = response.json()["id"]
  second_client = client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_client  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_client.json()["access_token"]
  
  response = client.delete(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {second_token}"})

  assert response.status_code == 403
  assert response.json()["detail"] == f"Transaction ID {transaction_id} does not belong to user"

def test_update_transaction(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = response.json()["id"]

  response = client.put(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "14.99",
    "transaction_type": "income", 
    "description": "Payment", 
    "date": "2026-03-12"
  })

  assert response.status_code == 200 
  assert response.json()["user_id"] == 1
  assert response.json()["account_id"] == 1
  assert response.json()["category_id"] == 1
  assert response.json()["amount"] == "14.99"
  assert response.json()["transaction_type"] == "income"
  assert response.json()["description"] == "Payment"
  assert response.json()["date"] == "2026-03-12"

def test_nonexisting_update(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = 999

  response = client.put(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "14.99",
    "transaction_type": "income", 
    "description": "Payment", 
    "date": "2026-03-12"
  })
  
  assert response.status_code == 404
  assert response.json()["detail"] == "Transaction ID not found"

def test_wrong_user_update(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = response.json()["id"]
  second_client = client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_client  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_client.json()["access_token"]
  
  response = client.put(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {second_token}"}, json = {
  "account_id": account_id, 
  "category_id": category_id, 
  "amount": "14.99",
  "transaction_type": "income", 
  "description": "Payment", 
  "date": "2026-03-12"
  })

  assert response.status_code == 403
  assert response.json()["detail"] == f"Transaction ID {transaction_id} does not belong to user"

def test_adjust_balance(create_account):
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
    "amount": "555.87",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  response = client.get("/accounts", headers ={"Authorization" : f"Bearer {token}"})
  #balance should be 500 - 12.57 - 20 + 555.87
  assert response.json()[0]["balance"] == "1023.30"

def test_adjust_balance_delete(create_account):
  client, token, account_id, category_id = create_account
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  transaction_id = response.json()["id"]
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
    "amount": "555.87",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  client.delete(f"/transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"}) 

  response = client.get("/accounts", headers ={"Authorization" : f"Bearer {token}"})
  #balance should be 500 + 12.57 - 20 + 555.87
  assert response.json()[0]["balance"] == "1035.87"