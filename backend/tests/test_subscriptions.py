def test_get_subscriptions(create_account):
  client, token, account_id, _ = create_account 
  response = client.get("/subscriptions", headers = {"Authorization": f"Bearer {token}"})
  assert response.status_code == 200
  assert len(response.json()) == 0 

def test_get_subscription(create_account, create_subscription):
  client, token, account_id, _ = create_account
  subscription = create_subscription(1, "Netflix", "12.99", "2026-05-27")
  assert subscription.status_code == 201
  response = client.get(f"/subscriptions/{subscription.json()["id"]}", headers = {"Authorization": f"Bearer {token}"})
  assert response.status_code == 200

def test_create_subscription(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/subscriptions", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "name": "Netflix", 
    "amount": "12.99", 
    "next_due_date": "2026-05-27"
  })
  assert response.status_code == 201
  assert response.json()["name"] == "Netflix"
  assert response.json()["amount"] == "12.99"
  assert response.json()["next_due_date"] == "2026-05-27"

def test_bad_name(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/subscriptions", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "name": "", 
    "amount": "12.99", 
    "next_due_date": "2026-05-27"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Subscription name can't be left empty." 

def test_zero_amount(create_account):
  client, token, account_id, _ = create_account
  response = client.post("/subscriptions", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "name": "Netflix", 
    "amount": "0", 
    "next_due_date": "2026-05-27"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be zero."

def test_negative_amount(create_account): 
  client, token, account_id, _ = create_account
  response = client.post("/subscriptions", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "name": "Netflix", 
    "amount": "-0.5", 
    "next_due_date": "2026-05-27"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, Amount can't be negative."

def test_past_date(create_account): 
  client, token, account_id, _ = create_account
  response = client.post("/subscriptions", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": account_id, 
    "category_id": 1, 
    "name": "Netflix", 
    "amount": "100.5", 
    "next_due_date": "2025-01-01"
  })
  assert response.status_code == 422
  assert response.json()["detail"][0]["msg"] == "Value error, This date has already passed."

def test_delete_subscription(create_account, create_subscription):
  client, token, _, _ = create_account
  subscription = create_subscription(1, "Netflix", "12.99", "2026-05-27")
  response = client.delete(f"/subscriptions/{subscription.json()["id"]}", headers = {"Authorization": f"Bearer {token}"})
  assert response.status_code == 204

def test_404_delete(create_account):
  client, token, _, _ = create_account
  response = client.delete(f"/subscriptions/999", headers = {"Authorization": f"Bearer {token}"})
  assert response.status_code == 404
  assert response.json()["detail"] == "Subscription ID not found"

def test_403_delete(create_two_users, create_subscription):
  client, first_token, second_token = create_two_users
  first_token_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"})
  subscription = create_subscription(1, "Netflix", "12.99", "2026-05-27", account_id=first_token_account.json()["id"]) 

  response = client.delete(f"/subscriptions/{subscription.json()["id"]}", headers = {"Authorization": f"Bearer {second_token}"})
  assert response.status_code == 403
  assert response.json()["detail"] == f"Subscription ID {subscription.json()["id"]} does not belong to user"
  
def test_update_subscription(create_two_accounts, create_subscription):
  client, token, first_account_id, second_account_id = create_two_accounts
  subscription = create_subscription(1, "Netflix", "12.99", "2026-05-27", first_account_id)
  assert subscription.status_code == 201
  assert subscription.json()["account_id"] == first_account_id
  assert subscription.json()["category_id"] == 1
  assert subscription.json()["name"] == "Netflix"
  assert subscription.json()["amount"] == "12.99"
  assert subscription.json()["next_due_date"] == "2026-05-27"

  response = client.put(f"/subscriptions/{subscription.json()["id"]}", headers = {"Authorization": f"Bearer {token}"}, json = {
    "account_id": second_account_id, 
    "category_id": 2, 
    "name": "Hulu", 
    "amount": "21.67", 
    "next_due_date": "2026-07-01"
  }) 

  assert response.status_code == 200
  assert response.json()["account_id"] == second_account_id
  assert response.json()["category_id"] == 2
  assert response.json()["name"] == "Hulu"
  assert response.json()["amount"] == "21.67"
  assert response.json()["next_due_date"] == "2026-07-01"

def test_403_update(create_two_users, create_subscription):
  client, first_token, second_token = create_two_users
  first_token_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"})
  subscription = create_subscription(1, "Netflix", "12.99", "2026-05-27", account_id=first_token_account.json()["id"]) 

  response = client.put(f"/subscriptions/{subscription.json()["id"]}", headers = {"Authorization": f"Bearer {second_token}"}, json = {
    "account_id": first_token_account.json()["id"], 
    "category_id": 2, 
    "name": "Hulu", 
    "amount": "21.67", 
    "next_due_date": "2026-07-01"
  })
  assert response.status_code == 403
  assert response.json()["detail"] == f"Subscription ID {subscription.json()["id"]} does not belong to user"
