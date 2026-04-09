def test_get_goals(create_account):
  client, token, _, _ = create_account 
  response = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 

def test_get_goal(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200

def test_bad_get(create_account): 
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = 999
  response = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 404
  assert response.json()["detail"] == "Goal ID not found"

def test_create_goal(create_account):
  client, token, _, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 

  assert response.status_code == 201 
  assert response.json()["name"] == "Vacation Fund"
  assert response.json()["target_amount"] == "3000.00"
  assert response.json()["current_amount"] == "0.00"
  assert response.json()["deadline"] == "2026-08-12"

def test_bad_name(create_account):
  client, token, _, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "", "target_amount": "3000.00", "deadline": "2026-08-12"}) 

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Goal name can't be left empty."

def test_zero_amount(create_account):
  client, token, _, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "0.00", "deadline": "2026-08-12"}) 

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Target amount can't be zero."

def test_negative_amount(create_account):
  client, token, _, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": -1, "deadline": "2026-08-12"}) 

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Target amount can't be negative."

def test_delete(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.delete(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204 

def test_update_goal(create_account): 
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Emergency Fund", "target_amount": "5000.00", "deadline": "2030-12-30"})
  
  assert response.status_code == 200 
  assert response.json()["name"] == "Emergency Fund"
  assert response.json()["target_amount"] == "5000.00"
  assert response.json()["current_amount"] == "0.00"
  assert response.json()["deadline"] == "2030-12-30"

def test_update_current_amount(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "15.00"})

  assert response.status_code == 200
  assert response.json()["current_amount"] == "15.00"

#higher value than account balance (500.00)
def test_bad_update_current_amount(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "1500.00"})

  assert response.status_code == 400
  assert response.json()["detail"] == "Account does not have enough money for this transfer."

#zero amount value 
def test_zero_update_current_amount(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "0"})

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be zero."

#negative amount value 
def test_negative_update_current_amount(create_account):
  client, token, _, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "-0.2"})

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be negative."

def test_check_account_after_update(register_login_user):
  client, token = register_login_user 
  account_response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500.00"}) 
  account_id = account_response.json()["id"]
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": 1, "amount": "15.00"})
  account_response = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert account_response.status_code == 200 
  assert account_response.json()["balance"] == "485.00"



