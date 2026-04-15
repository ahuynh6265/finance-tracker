def test_check_net_balance_after_update_goal(create_account):
  client, token, account_id, category_id = create_account 
  #account balance set at 500
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.568924",
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
    "amount": "555.86723232",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "15.00"})

  summary_response = client.get("/summary", headers ={"Authorization" : f"Bearer {token}"})
  assert summary_response.status_code == 200
  assert summary_response.json()["income"] == "555.87"
  assert summary_response.json()["expenses"] == "32.57"
  assert summary_response.json()["net balance"] == "1023.30"
  assert summary_response.json()["accounts_only"] == "1008.30"

#check account income, expense, net balance per month is correct  
def test_account_summary(create_account):
  client, token, account_id, category_id = create_account 
  #account balance set at 500
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "12.568924",
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
    "amount": "555.86723232",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-04-12"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "555.86723232",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-11"
  })
  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "500",
    "transaction_type": "income", 
    "description": "Wage", 
    "date": "2026-03-12"
  })

  response = client.get(f"/accounts/{account_id}/summary", headers ={"Authorization" : f"Bearer {token}"})
  #this month
  assert response.status_code == 200
  assert response.json()["income"] == "555.87"
  assert response.json()["expenses"] == "32.57"
  assert response.json()["net_balance"] == "523.30"

  #total 
  account_response = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert account_response.status_code == 200
  assert account_response.json()["balance"] == "2079.17"
  
def test_account_summary_404(create_account): 
  client, token, _, _ = create_account 
  #account balance set at 500
  response = client.get(f"/accounts/{999}/summary", headers ={"Authorization" : f"Bearer {token}"})
  #this month
  assert response.status_code == 404
  assert response.json()["detail"] == "Account ID not found"

def test_account_summary_403(create_two_users): 
  client, first_token, second_token = create_two_users 
  #account balance set at 500
  first = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  first_id = first.json()["id"]
  response = client.get(f"/accounts/{first_id}/summary", headers ={"Authorization" : f"Bearer {second_token}"})

  #this month
  assert response.status_code == 403
  assert response.json()["detail"] == f"Account ID {first_id} does not belong to user"