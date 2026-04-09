#testing transfer with transaction routes
def test_transfer_create(create_account):
  client, token, account_id, category_id = create_account
  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "destination_account_id": second_account_id, 
    "amount": "200.00",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 201 
  assert response.json()["user_id"] == 1
  assert response.json()["account_id"] == 1
  assert response.json()["category_id"] == 12
  assert response.json()["amount"] == "200.00"
  assert response.json()["transaction_type"] == "transfer"
  assert response.json()["description"] == f"Transfer to {second_account_name}"
  assert response.json()["date"] == "2026-04-06"

#higher amount than balance
def test_bad_transfer_create(create_account):
  client, token, account_id, category_id = create_account
  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "destination_account_id": second_account_id, 
    "amount": "1000.00",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 400
  assert response.json()["detail"] == "Account does not have enough money for this transfer."

#transfer with bad account id destination
def test_bad_destination_id(create_account):
  client, token, account_id, category_id = create_account
  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = 999
  second_account_name = second_account.json()["bank_name"]

  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "destination_account_id": second_account_id, 
    "amount": "1000.00",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 404
  assert response.json()["detail"] == "Account ID not found"

#transfer with account id not belonging to user 
def test_forbidden_destination_id(create_account):
  client, token, account_id, category_id = create_account

  #second user
  client.post("/auth/register", json = {"name": "Test", "email": "test2@test.com", "password": "password123"})
  second_response  = client.post("/auth/login", json = {"email": "test2@test.com", "password": "password123"})
  second_token = second_response.json()["access_token"]
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {second_token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  #user one transfers to user 2 account 
  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "destination_account_id": second_account_id, 
    "amount": "1000.00",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 403
  assert response.json()["detail"] == f"Account ID {second_account_id} does not belong to user"

#transfer with no account id destination
def test_no_destination_id(create_account):
  client, token, account_id, category_id = create_account
  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  
  second_account_name = second_account.json()["bank_name"]

  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "amount": "1000.00",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Please provide a valid destination to transfer to."

#using account id destination without transfer transaction type
def test_no_transfer_type(create_account):
  client, token, account_id, category_id = create_account
  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  response = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": category_id, 
    "destination_account_id": second_account_id, 
    "amount": "1000.00",
    "transaction_type": "expense", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Can not add a destination."

#check balance of accounts 
def test_check_balance(register_login_user):
  client, token =  register_login_user
  first_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"})
  first_account_id = first_account.json()["id"]

  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": first_account_id, 
    "category_id": 1, #dummy id, category id gets overwritten when using transfer transaction type 
    "destination_account_id": second_account_id, 
    "amount": "257.67",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })

  first_response = client.get(f"/accounts/{first_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 
  second_response = client.get(f"/accounts/{second_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 
  assert first_response.status_code == 200 
  assert first_response.json()["balance"] == "242.33"
  assert second_response.status_code == 200 
  assert second_response.json()["balance"] == "1457.67"
  
def test_transfer_delete(register_login_user):
  client, token =  register_login_user
  first_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"})
  first_account_id = first_account.json()["id"]

  #second account 
  second_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "1200"}) 
  second_account_id = second_account.json()["id"]
  second_account_name = second_account.json()["bank_name"]

  transaction = client.post("/transactions", headers ={"Authorization" : f"Bearer {token}"}, json = {
    "account_id": first_account_id, 
    "category_id": 1,
    "destination_account_id": second_account_id, 
    "amount": "351.23",
    "transaction_type": "transfer", 
    "description": f"Transfer to {second_account_name}", 
    "date": "2026-04-06"
  })
  transaction_id = transaction.json()["id"]

  first_before_delete = client.get(f"/accounts/{first_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 
  second_before_delete = client.get(f"/accounts/{second_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 

  response = client.delete(f"/transactions/{transaction_id}", headers = {"Authorization" : f"Bearer {token}"})

  first_response = client.get(f"/accounts/{first_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 
  second_response = client.get(f"/accounts/{second_account_id}", headers = {"Authorization" : f"Bearer {token}"}) 

  assert first_before_delete.json()["balance"] == "148.77"
  assert second_before_delete.json()["balance"] == "1551.23" 
  assert response.status_code == 204
  assert first_response.json()["balance"] == "500.00"
  assert second_response.json()["balance"] == "1200.00" 


