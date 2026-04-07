def test_get_transactions(create_account):
  client, token, account_id, category_id = create_account
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  response.status_code == 200 

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
  response.status_code == 201 
  response.json()["user_id"] == 1
  response.json()["account_id"] == 1
  response.json()["category_id"] == 1
  response.json()["amount"] == "12.57"
  response.json()["transaction_type"] == "expense"
  response.json()["description"] == "Chipotle"
  response.json()["date"] == "2026-04-06"
  
