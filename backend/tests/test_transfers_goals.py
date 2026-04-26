#check account and goal balance after goal update
def test_check_account(create_account): 
  client, token, account_id, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "155.10"})

  response = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  goal_response = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert response.json()["balance"] == "344.90"
  assert goal_response.status_code == 200
  assert goal_response.json()["current_amount"] == "155.10"

#check transaction created after transfer 
def test_check_transaction(create_account):
  client, token, account_id, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  response = client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "155.10"})
  name = response.json()["name"]


  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert response.json()[0]["user_id"] == 1
  assert response.json()[0]["account_id"] == 1
  assert response.json()[0]["category_id"] == 12
  assert response.json()[0]["destination_account_id"] == None
  assert response.json()[0]["amount"] == "155.10"
  assert response.json()[0]["transaction_type"] == "transfer"
  assert response.json()[0]["description"] == f"Transfer to {name}"

#delete transaction and check if balance is correct before/after
def test_delete_goal_transaction(create_account):
  client, token, account_id, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  name = response.json()["name"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "155.10"})

  #get transaction id through list because goal route doesn't return the id 
  transactions = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  transaction_id = transactions.json()[0]["id"]  

  assert transactions.json()[0]["id"] == 1
  assert transactions.json()[0]["account_id"] == 1
  assert transactions.json()[0]["category_id"] == 12
  assert transactions.json()[0]["destination_goal_id"] == 1
  assert transactions.json()[0]["description"] == f"Transfer to {name}"

  goal_before_delete = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal_before_delete.json()["current_amount"] == "155.10"

  before_delete = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert before_delete.json()["balance"] == "344.90"

  response = client.delete(f"transactions/{transaction_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204

  account = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert account.json()["balance"] == "500.00"

  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.json()["current_amount"] == "0.00"

#same account multiple transfers
def test_multiple_transfers(create_account): 
  #first account balance: 500
  client, token, account_id, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]

  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "55.67"})

  #current amount should be 123.23 + 55.67
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "178.90"

  #check both account balances 
  account = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert account.status_code == 200
  assert account.json()["balance"] == "321.10"
 

def test_different_account_transfers(create_two_accounts): 
  #first account balance: 500, second account balance: 1500
  client, token, first_account_id, second_account_id = create_two_accounts 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]

  #500 - 155.10
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": first_account_id, "amount": "155.10"})
  #1500 - 700.27
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": second_account_id, "amount": "700.27"})

  #current amount should be 155.10 + 700.27 
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "855.37"

  #check both account balances 
  first_account = client.get(f"/accounts/{first_account_id}", headers ={"Authorization" : f"Bearer {token}"})
  second_account = client.get(f"/accounts/{second_account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert first_account.status_code == 200
  assert first_account.json()["balance"] == "344.90"
  assert second_account.status_code == 200
  assert second_account.json()["balance"] == "799.73"

#check total transfer goal transactions 
def test_transaction_count(create_two_accounts):
  #first account balance: 500, second account balance: 1500
  client, token, first_account_id, second_account_id = create_two_accounts 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]

  #500 - 155.10
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": first_account_id, "amount": "155.10"})
  #1500 - 700.27
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": second_account_id, "amount": "700.27"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": second_account_id, "amount": "55.31"})

  transactions = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})

  assert len(transactions.json()) == 3

def test_withdraw(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "55.67"})
  
  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "25.51"})

  #check account and goal balances
  #178.90 - 25.51
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "153.39"

  #321.10 + 25.51
  account = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert account.status_code == 200
  assert account.json()["balance"] == "346.61"

def test_bad_withdraw(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "55.67"})
  
  response = client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "999.99"})

  assert response.status_code == 400
  assert response.json()["detail"] == "Can not withdraw more than you currently have in the fund."

def test_multiple_withdraw(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "55.67"})
  
  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "25.51"})
  #check account and goal balances
  #178.90 - 25.51
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "153.39"

  #321.10 + 25.51
  account = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert account.status_code == 200
  assert account.json()["balance"] == "346.61"

  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "56.17"})
  #check again after second withdrawl
  #153.39 - 56.17
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "97.22"

  #346.61 + 56.17
  account = client.get(f"/accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert account.status_code == 200
  assert account.json()["balance"] == "402.78"

def test_different_account_withdraw(create_two_accounts):
  #first account balance: 500, second account balance: 1500
  client, token, first_account_id, second_account_id = create_two_accounts
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": first_account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": second_account_id, "amount": "555.67"})
  

  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": first_account_id, "amount": "255.67"})
  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": second_account_id, "amount": "25.44"})

  #check account and goal balances
  #123.23 + 555.67 = 678.90 -> 678.90 - 255.67 - 25.44
  goal = client.get(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert goal.status_code == 200
  assert goal.json()["current_amount"] == "397.79"

  #376.77 + 255.67
  first_account = client.get(f"/accounts/{first_account_id}", headers ={"Authorization" : f"Bearer {token}"})
  #944.33 + 25.44
  second_account = client.get(f"/accounts/{second_account_id}", headers ={"Authorization" : f"Bearer {token}"})

  assert first_account.status_code == 200
  assert first_account.json()["balance"] == "632.44"
  assert second_account.status_code == 200
  assert second_account.json()["balance"] == "969.77"

#check goal can be deleted after being funded then withdraw of all money
def test_check_fund_withdraw_delete(create_account):
  client, token, account_id, _ = create_account 
  response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-08-12"}) 
  goal_id = response.json()["id"]
  
  client.put(f"/goals/{goal_id}/current-amount", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  client.put(f"/goals/{goal_id}/withdraw", headers ={"Authorization" : f"Bearer {token}"}, json = {"account_id": account_id, "amount": "123.23"})
  response = client.delete(f"/goals/{goal_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 204 