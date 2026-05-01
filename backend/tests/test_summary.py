from freezegun import freeze_time
from decimal import Decimal

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

  with freeze_time("2026-04-25"):
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

  assert response.status_code == 404
  assert response.json()["detail"] == "Account ID not found"

def test_account_summary_403(create_two_users): 
  client, first_token, second_token = create_two_users 
  #account balance set at 500
  first = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  first_id = first.json()["id"]
  response = client.get(f"/accounts/{first_id}/summary", headers ={"Authorization" : f"Bearer {second_token}"})

  assert response.status_code == 403
  assert response.json()["detail"] == f"Account ID {first_id} does not belong to user"

#check length of list, should have 12 entries one per month, year
def test_monthly_summary(create_account, create_transactions):
  client, token, _, _ = create_account

  create_transactions(1, "10.00", "2025-01-23")
  with freeze_time("2025-12-23"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 12

#start from may 2025 for 12 entries check transactions are in expenses and income are all 0
def test_expense_transaction_every_month(create_account, create_transactions):
  client, token, _, _ = create_account
  #different categories
  create_transactions(2, "10.00", "2025-05-23")
  create_transactions(3, "20.00", "2025-06-23")
  create_transactions(1, "30.00", "2025-07-23")
  create_transactions(4, "40.00", "2025-08-23")
  create_transactions(5, "50.00", "2025-09-23")
  create_transactions(6, "60.00", "2025-10-23")
  create_transactions(7, "70.00", "2025-11-23")
  create_transactions(8, "80.00", "2025-12-23")
  create_transactions(10, "90.00", "2026-01-23")
  create_transactions(3, "100.00", "2026-02-23")
  create_transactions(5, "110.00", "2026-03-23")
  create_transactions(7, "120.00", "2026-04-23")

  with freeze_time("2026-04-25"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 12
  assert response.json()[0]["expenses"] == "10.00"
  assert response.json()[1]["expenses"] == "20.00"
  assert response.json()[2]["expenses"] == "30.00"
  assert response.json()[3]["expenses"] == "40.00"
  assert response.json()[4]["expenses"] == "50.00"
  assert response.json()[5]["expenses"] == "60.00"
  assert response.json()[6]["expenses"] == "70.00"
  assert response.json()[7]["expenses"] == "80.00"
  assert response.json()[8]["expenses"] == "90.00"
  assert response.json()[9]["expenses"] == "100.00"
  assert response.json()[10]["expenses"] == "110.00"
  assert response.json()[11]["expenses"] == "120.00"

  assert response.json()[0]["income"] == "0.00"
  assert response.json()[1]["income"] == "0.00"
  assert response.json()[2]["income"] == "0.00"
  assert response.json()[3]["income"] == "0.00"
  assert response.json()[4]["income"] == "0.00"
  assert response.json()[5]["income"] == "0.00"
  assert response.json()[6]["income"] == "0.00"
  assert response.json()[7]["income"] == "0.00"
  assert response.json()[8]["income"] == "0.00"
  assert response.json()[9]["income"] == "0.00"
  assert response.json()[10]["income"] == "0.00"
  assert response.json()[11]["income"] == "0.00"


def test_both_transaction_types(create_account, create_transactions):
  client, token, _, _ = create_account
  #different categories
  create_transactions(1, "100.00", "2025-05-23", transaction_type="income")
  create_transactions(1, "50.00", "2025-05-23")

  create_transactions(1, "200.00", "2025-12-23", transaction_type="income")
  create_transactions(1, "75.00", "2025-12-23")

  create_transactions(1, "250.00", "2026-04-23", transaction_type="income")
  create_transactions(1, "10.00", "2026-04-23")

  with freeze_time("2026-04-25"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 12
  assert response.json()[0]["expenses"] == "50.00"
  assert response.json()[1]["expenses"] == "0.00"
  assert response.json()[2]["expenses"] == "0.00"
  assert response.json()[3]["expenses"] == "0.00"
  assert response.json()[4]["expenses"] == "0.00"
  assert response.json()[5]["expenses"] == "0.00"
  assert response.json()[6]["expenses"] == "0.00"
  assert response.json()[7]["expenses"] == "75.00"
  assert response.json()[8]["expenses"] == "0.00"
  assert response.json()[9]["expenses"] == "0.00"
  assert response.json()[10]["expenses"] == "0.00"
  assert response.json()[11]["expenses"] == "10.00"

  assert response.json()[0]["income"] == "100.00"
  assert response.json()[1]["income"] == "0.00"
  assert response.json()[2]["income"] == "0.00"
  assert response.json()[3]["income"] == "0.00"
  assert response.json()[4]["income"] == "0.00"
  assert response.json()[5]["income"] == "0.00"
  assert response.json()[6]["income"] == "0.00"
  assert response.json()[7]["income"] == "200.00"
  assert response.json()[8]["income"] == "0.00"
  assert response.json()[9]["income"] == "0.00"
  assert response.json()[10]["income"] == "0.00"
  assert response.json()[11]["income"] == "250.00"

#multiple transactions same month and decimals
def test_multiple_same_month(create_account, create_transactions):
  client, token, _, _ = create_account
  create_transactions(1, "110.343434", "2026-03-23")
  create_transactions(1, "20.999", "2026-03-23", transaction_type="income")
  create_transactions(1, "10.2135", "2026-03-23")
  create_transactions(1, "500.676767", "2026-04-23")
  create_transactions(1, "50.8751", "2026-04-23", transaction_type="income")
  create_transactions(1, "150.94241", "2026-04-23")

  with freeze_time("2026-04-25"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 2
  assert response.json()[0]["expenses"] == "120.56"
  assert response.json()[1]["expenses"] == "651.62"
  assert response.json()[0]["income"] == "21.00"
  assert response.json()[1]["income"] == "50.88"


#test that transfers aren't being added, income and expenses should both be zero, only first expense should be shown
def test_transfer(create_two_accounts, create_transactions):
  client, token, first_account_id, second_account_id = create_two_accounts
  create_transactions(1, "100.00", "2025-05-23", account_id=first_account_id, transaction_type="transfer", destination_account_id=second_account_id)
  create_transactions(1, "50.00", "2025-05-23")
  with freeze_time("2026-04-25"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 12
  assert response.json()[0]["expenses"] == "50.00"
  assert response.json()[1]["expenses"] == "0.00"
  assert response.json()[2]["expenses"] == "0.00"
  assert response.json()[3]["expenses"] == "0.00"
  assert response.json()[4]["expenses"] == "0.00"
  assert response.json()[5]["expenses"] == "0.00"
  assert response.json()[6]["expenses"] == "0.00"
  assert response.json()[7]["expenses"] == "0.00"
  assert response.json()[8]["expenses"] == "0.00"
  assert response.json()[9]["expenses"] == "0.00"
  assert response.json()[10]["expenses"] == "0.00"
  assert response.json()[11]["expenses"] == "0.00"

  assert response.json()[0]["income"] == "0.00"
  assert response.json()[1]["income"] == "0.00"
  assert response.json()[2]["income"] == "0.00"
  assert response.json()[3]["income"] == "0.00"
  assert response.json()[4]["income"] == "0.00"
  assert response.json()[5]["income"] == "0.00"
  assert response.json()[6]["income"] == "0.00"
  assert response.json()[7]["income"] == "0.00"
  assert response.json()[8]["income"] == "0.00"
  assert response.json()[9]["income"] == "0.00"
  assert response.json()[10]["income"] == "0.00"
  assert response.json()[11]["income"] == "0.00"

#test that transfers aren't being added, only one empty list should be made since there are no other transaction other than a transfer
def test_just_transfer(create_two_accounts, create_transactions):
  client, token, first_account_id, second_account_id = create_two_accounts
  create_transactions(1, "100.00", "2025-05-23", account_id=first_account_id, transaction_type="transfer", destination_account_id=second_account_id)
  response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 1

def test_no_transactions(create_account):
  client, token, _, _ = create_account
  response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  assert len(response.json()) == 1

def test_bad_token(create_account, create_transactions):
  client, _, _, _ = create_account
  create_transactions(1, "50.00", "2025-05-23")
  fake_token = 999
  response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {fake_token}"})
  assert response.status_code == 401

#make sure first users transactions dont leak into second users monthly summary
def test_summary_leak(create_two_users, create_transactions):
  client, first_token, second_token = create_two_users 
  first_user_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {first_token}"}, json = {"bank_name": "Chase", "account_type": "checking", "balance": "500"}) 
  second_user_account = client.post("/accounts", headers = {"Authorization" : f"Bearer {second_token}"}, json = {"bank_name": "Wells Fargo", "account_type": "checking", "balance": "500"})
  create_transactions(1, "50.00", "2026-03-23", account_id=first_user_account.json()["id"], token=first_token)
  create_transactions(1, "150.00", "2026-04-23", account_id=first_user_account.json()["id"], token=first_token)
  #second users category id 
  create_transactions(14, "10.00", "2026-03-23", account_id=second_user_account.json()["id"], token=second_token)
  with freeze_time("2026-04-25"):
    response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {second_token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 2
  assert response.json()[0]["expenses"] == "10.00"
  assert response.json()[1]["expenses"] == "0.00"
  assert response.json()[0]["income"] == "0.00"
  assert response.json()[1]["income"] == "0.00"

#check that sum for income and expense equal in both routes
def test_summary_cross_check(create_account, create_transactions):
  client, token, _, _ = create_account
  create_transactions(1, "110.343434", "2026-03-23")
  create_transactions(1, "20.75", "2026-03-23", transaction_type="income")
  create_transactions(1, "10.2135", "2026-03-23")
  create_transactions(1, "500.676767", "2026-04-23")
  create_transactions(1, "50.8751", "2026-04-23", transaction_type="income")
  create_transactions(1, "150.94241", "2026-04-23")

  with freeze_time("2026-04-25"):
    monthly_response = client.get("/summary/monthly", headers = {"Authorization" : f"Bearer {token}"})
    summary_response = client.get("/summary", headers = {"Authorization" : f"Bearer {token}"})
  
  assert monthly_response.status_code == 200 
  assert len(monthly_response.json()) == 2
  assert monthly_response.json()[0]["expenses"] == "120.56"
  assert monthly_response.json()[1]["expenses"] == "651.62"
  assert monthly_response.json()[0]["income"] == "20.75"
  assert monthly_response.json()[1]["income"] == "50.88"

  assert summary_response.status_code == 200
  assert Decimal(summary_response.json()["income"]) == sum(Decimal(income["income"]) for income in monthly_response.json())
  assert Decimal(summary_response.json()["expenses"]) == sum(Decimal(income["expenses"]) for income in monthly_response.json())
  