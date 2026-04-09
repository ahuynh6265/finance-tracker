def test_get_categories(create_account):
  client, token, _, _ = create_account
  response = client.get("/categories", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200
  assert response.json()[0]["name"] == "Automotive"
  assert response.json()[1]["name"] == "Bills & utilities"
  assert response.json()[2]["name"] == "Cash out"
  assert response.json()[3]["name"] == "Education"
  assert response.json()[4]["name"] == "Entertainment"
  assert response.json()[5]["name"] == "Food & drink"
  assert response.json()[6]["name"] == "Gas"
  assert response.json()[7]["name"] == "Groceries"
  assert response.json()[8]["name"] == "Misc."
  assert response.json()[9]["name"] == "Personal"
  assert response.json()[10]["name"] == "Shopping"
  assert response.json()[11]["name"] == "Transfer"
  assert response.json()[12]["name"] == "Travel"

def test_clearall_transaction_by_category(create_account):
  client, token, account_id, _ = create_account

  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "20.00",
    "transaction_type": "expense", 
    "description": "Bolay", 
    "date": "2026-04-07"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "555.87",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "amount": "1000.00",
    "transaction_type": "income", 
    "description": "payment", 
    "date": "2026-04-06"
  })

  response = client.delete("/categories/2/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204 

def test_check_balance_after_clear(create_account):
  client, token, account_id, _ = create_account

  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "12.57",
    "transaction_type": "expense", 
    "description": "Chipotle", 
    "date": "2026-04-06"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "20.00",
    "transaction_type": "expense", 
    "description": "Bolay", 
    "date": "2026-04-07"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 2, 
    "amount": "555.87",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "amount": "1000.00",
    "transaction_type": "income", 
    "description": "payment", 
    "date": "2026-04-06"
  })

  client.delete("/categories/2/transactions", headers ={"Authorization" : f"Bearer {token}"})

  response = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  #balance should be 1500 because we deleted all transactions linked to category 2 but kept category 1
  assert response.json()["balance"] == "1500.00"