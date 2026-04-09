def test_check_net_balance_after_update_goal(create_account):
  client, token, account_id, category_id = create_account 
  #account balance set at 500
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

  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "15.00"})

  summary_response = client.get("/summary", headers ={"Authorization" : f"Bearer {token}"})
  assert summary_response.json()["net balance"] == "1023.30"
  

  
  