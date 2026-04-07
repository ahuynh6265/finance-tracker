def test_get_accounts(register_login_user):
  client, token = register_login_user
  response = client.get("/accounts", headers = {"Authorization" : f"Bearer {token}"}) 
  assert response.status_code == 200

def test_create_account(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 

  assert response.status_code == 201 
  assert response.json()["user_id"] == 1
  assert response.json()["bank_name"] == "Chase"
  assert response.json()["account_type"] == "checking"
  assert response.json()["balance"] == "500.00"

def test_bad_name(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "", "account_type": "checking", "balance": "500"}) 
  assert response.status_code == 422 
  assert response.json()["detail"][0]["msg"] == "Value error, Bank name can't be left empty."

def test_bad_balance(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "-1"}) 
  assert response.status_code == 422 
  assert response.json()["detail"][0]["msg"] == "Value error, Balance can't be a negative number."

def test_delete(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  account_id = response.json()["id"]
  response = client.delete(f"/accounts/{account_id}", headers = {"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204

def test_bad_delete(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  account_id = 2 
  response = client.delete(f"/accounts/{account_id}", headers = {"Authorization" : f"Bearer {token}"})
  assert response.status_code == 404
  assert response.json()["detail"] == "Account ID not found"

def test_wrong_user(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  account_id = response.json()["id"] #should be 1 

  second_response = client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_response  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_response.json()["access_token"]
  second_response = client.post("/accounts", headers = {"Authorization" : f"Bearer {second_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  
  second_id = second_response.json()["id"] #should be 2

  #use first user try to delete second user bank account
  response = client.delete(f"/accounts/{second_id}", headers = {"Authorization" : f"Bearer {token}"})
  assert response.status_code == 403
  assert response.json()["detail"] == f"Account ID {second_id} does not belong to user"

def test_update(register_login_user):
  client, token = register_login_user 
  response = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"})
  account_id = response.json()["id"]

  response = client.put(f"/accounts/{account_id}", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "savings", "balance": "5100"})

  assert response.status_code == 200 
  assert response.json()["user_id"] == 1
  assert response.json()["bank_name"] == "Wells Fargo"
  assert response.json()["account_type"] == "savings"
  assert response.json()["balance"] == "5100.00"

def test_nonexisting_update(register_login_user):
  client, token = register_login_user 
  account_id = 2
  response = client.put(f"/accounts/{account_id}", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "savings", "balance": "5100"})
  assert response.status_code == 404
  assert response.json()["detail"] == "Account ID not found"

def test_wrong_user_update(register_login_user): 
  client, token = register_login_user  
  second_response = client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_response  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_response.json()["access_token"]
  second_response = client.post("/accounts", headers = {"Authorization" : f"Bearer {second_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  
  second_id = second_response.json()["id"] #should be 2

  #use first user try to delete second user bank account
  response = client.put(f"/accounts/{second_id}", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "savings", "balance": "5100"})
  assert response.status_code == 403
  assert response.json()["detail"] == f"Account ID {second_id} does not belong to user"
