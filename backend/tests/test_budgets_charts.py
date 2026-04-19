#check total spent for each category per month 
def test_monthly_budgets(create_transactions, create_account):
  client, token, _, _ = create_account

  #One transaction per month
  create_transactions(1, "10.00", "2026-01-23")
  create_transactions(1, "20.00", "2026-02-23")
  create_transactions(1, "30.00", "2026-03-23")
  create_transactions(1, "40.00", "2026-04-23")
  create_transactions(1, "50.00", "2026-05-23")
  create_transactions(1, "60.00", "2026-06-23")
  create_transactions(1, "70.00", "2026-07-23")
  create_transactions(1, "80.00", "2026-08-23")
  create_transactions(1, "90.00", "2026-09-23")
  create_transactions(1, "100.00", "2026-10-23")
  create_transactions(1, "110.00", "2026-11-23")
  create_transactions(1, "120.00", "2026-12-23")
  
  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})

  assert response.status_code == 200 
  
  first_category = response.json()[0]
  assert first_category["category_id"] == 1
  assert first_category["category_name"] == "Automotive"
  #index represents month jan == 0 to dec == 11
  assert first_category["monthly_totals"][0] == "10.00"
  assert first_category["monthly_totals"][1] == "20.00"
  assert first_category["monthly_totals"][2] == "30.00"
  assert first_category["monthly_totals"][3] == "40.00"
  assert first_category["monthly_totals"][4] == "50.00"
  assert first_category["monthly_totals"][5] == "60.00"
  assert first_category["monthly_totals"][6] == "70.00"
  assert first_category["monthly_totals"][7] == "80.00"
  assert first_category["monthly_totals"][8] == "90.00"
  assert first_category["monthly_totals"][9] == "100.00"
  assert first_category["monthly_totals"][10] == "110.00"
  assert first_category["monthly_totals"][11] == "120.00"

#every other month will not have a amount spent
def test_monthly_budgets_zero(create_transactions, create_account):
  client, token, _, _ = create_account

  #One transaction per month
  create_transactions(1, "10.00", "2026-01-23")
  create_transactions(1, "30.00", "2026-03-23")
  create_transactions(1, "50.00", "2026-05-23")
  create_transactions(1, "70.00", "2026-07-23")
  create_transactions(1, "90.00", "2026-09-23")
  create_transactions(1, "110.00", "2026-11-23")
  
  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})

  assert response.status_code == 200 
  
  first_category = response.json()[0]
  assert first_category["category_id"] == 1
  assert first_category["category_name"] == "Automotive"
  #index represents month jan == 0 to dec == 11
  assert first_category["monthly_totals"][0] == "10.00"
  assert first_category["monthly_totals"][1] == "0.00"
  assert first_category["monthly_totals"][2] == "30.00"
  assert first_category["monthly_totals"][3] == "0.00"
  assert first_category["monthly_totals"][4] == "50.00"
  assert first_category["monthly_totals"][5] == "0.00"
  assert first_category["monthly_totals"][6] == "70.00"
  assert first_category["monthly_totals"][7] == "0.00"
  assert first_category["monthly_totals"][8] == "90.00"
  assert first_category["monthly_totals"][9] == "0.00"
  assert first_category["monthly_totals"][10] == "110.00"
  assert first_category["monthly_totals"][11] == "0.00"
  
def test_multiple_monthly_budgets(create_transactions, create_account):
  client, token, _, _ = create_account

  #Automotive
  create_transactions(1, "30.00", "2026-01-23")
  create_transactions(1, "30.00", "2026-02-23")
  create_transactions(1, "30.00", "2026-03-23")
  create_transactions(1, "30.00", "2026-04-23")
  create_transactions(1, "30.00", "2026-05-23")
  create_transactions(1, "30.00", "2026-06-23")
  create_transactions(1, "30.00", "2026-07-23")
  create_transactions(1, "30.00", "2026-08-23")
  create_transactions(1, "30.00", "2026-09-23")
  create_transactions(1, "30.00", "2026-10-23")
  create_transactions(1, "30.00", "2026-11-23")
  create_transactions(1, "30.00", "2026-12-23")

  #food and drink
  create_transactions(6, "30.00", "2026-01-23")
  create_transactions(6, "30.00", "2026-02-23")
  create_transactions(6, "30.00", "2026-03-23")
  create_transactions(6, "30.00", "2026-04-23")
  create_transactions(6, "30.00", "2026-05-23")
  create_transactions(6, "30.00", "2026-06-23")
  create_transactions(6, "30.00", "2026-07-23")
  create_transactions(6, "30.00", "2026-08-23")
  create_transactions(6, "30.00", "2026-09-23")
  create_transactions(6, "30.00", "2026-10-23")
  create_transactions(6, "30.00", "2026-11-23")
  create_transactions(6, "30.00", "2026-12-23")
    
  

  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})

  assert response.status_code == 200 
  first_category = response.json()[0]
  assert first_category["category_id"] == 1
  assert first_category["category_name"] == "Automotive"
  #index represents month jan == 0 to dec == 11
  assert first_category["monthly_totals"][0] == "30.00"
  assert first_category["monthly_totals"][1] == "30.00"
  assert first_category["monthly_totals"][2] == "30.00"
  assert first_category["monthly_totals"][3] == "30.00"
  assert first_category["monthly_totals"][4] == "30.00"
  assert first_category["monthly_totals"][5] == "30.00"
  assert first_category["monthly_totals"][6] == "30.00"
  assert first_category["monthly_totals"][7] == "30.00"
  assert first_category["monthly_totals"][8] == "30.00"
  assert first_category["monthly_totals"][9] == "30.00"
  assert first_category["monthly_totals"][10] == "30.00"
  assert first_category["monthly_totals"][11] == "30.00"

  food_and_drink = response.json()[5]
  assert food_and_drink["category_id"] == 6
  assert food_and_drink["category_name"] == "Food & drink"
  #index represents month jan == 0 to dec == 11
  assert food_and_drink["monthly_totals"][0] == "30.00"
  assert food_and_drink["monthly_totals"][1] == "30.00"
  assert food_and_drink["monthly_totals"][2] == "30.00"
  assert food_and_drink["monthly_totals"][3] == "30.00"
  assert food_and_drink["monthly_totals"][4] == "30.00"
  assert food_and_drink["monthly_totals"][5] == "30.00"
  assert food_and_drink["monthly_totals"][6] == "30.00"
  assert food_and_drink["monthly_totals"][7] == "30.00"
  assert food_and_drink["monthly_totals"][8] == "30.00"
  assert food_and_drink["monthly_totals"][9] == "30.00"
  assert food_and_drink["monthly_totals"][10] == "30.00"
  assert food_and_drink["monthly_totals"][11] == "30.00"

def test_empty_budgets(create_account):
  client, token, _, _ = create_account
  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  
  assert response.status_code == 200 
  food_and_drink = response.json()[5]
  assert food_and_drink["category_id"] == 6
  assert food_and_drink["category_name"] == "Food & drink"
  #index represents month jan == 0 to dec == 11
  assert food_and_drink["monthly_totals"][0] == "0.00"
  assert food_and_drink["monthly_totals"][1] == "0.00"
  assert food_and_drink["monthly_totals"][2] == "0.00"
  assert food_and_drink["monthly_totals"][3] == "0.00"
  assert food_and_drink["monthly_totals"][4] == "0.00"
  assert food_and_drink["monthly_totals"][5] == "0.00"
  assert food_and_drink["monthly_totals"][6] == "0.00"
  assert food_and_drink["monthly_totals"][7] == "0.00"
  assert food_and_drink["monthly_totals"][8] == "0.00"
  assert food_and_drink["monthly_totals"][9] == "0.00"
  assert food_and_drink["monthly_totals"][10] == "0.00"
  assert food_and_drink["monthly_totals"][11] == "0.00"

def test_multiple_transactions_in_same_month(create_transactions, create_account):
  client, token, _, _ = create_account

  create_transactions(1, "30.00", "2026-01-23")
  create_transactions(1, "33.33", "2026-01-17")

  create_transactions(1, "51.10", "2026-02-23")

  create_transactions(1, "91.00", "2026-07-03")
  create_transactions(1, "10.91", "2026-07-13")
  create_transactions(1, "2.03", "2026-07-23")

  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  first_category = response.json()[0]
  assert first_category["category_id"] == 1
  assert first_category["category_name"] == "Automotive"
  #index represents month jan == 0 to dec == 11
  assert first_category["monthly_totals"][0] == "63.33"
  assert first_category["monthly_totals"][1] == "51.10"
  assert first_category["monthly_totals"][2] == "0.00"
  assert first_category["monthly_totals"][3] == "0.00"
  assert first_category["monthly_totals"][4] == "0.00"
  assert first_category["monthly_totals"][5] == "0.00"
  assert first_category["monthly_totals"][6] == "103.94"
  assert first_category["monthly_totals"][7] == "0.00"
  assert first_category["monthly_totals"][8] == "0.00"
  assert first_category["monthly_totals"][9] == "0.00"
  assert first_category["monthly_totals"][10] == "0.00"
  assert first_category["monthly_totals"][11] == "0.00"

#chart for every category but transfer should be made
def test_check_categories(create_account):
  client, token, _, _ = create_account
  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200
  assert len(response.json()) == 12
  assert response.json()[0]["category_name"] == "Automotive"
  assert response.json()[1]["category_name"] == "Bills & utilities"
  assert response.json()[2]["category_name"] == "Cash out"
  assert response.json()[3]["category_name"] == "Education"
  assert response.json()[4]["category_name"] == "Entertainment"
  assert response.json()[5]["category_name"] == "Food & drink"
  assert response.json()[6]["category_name"] == "Gas"
  assert response.json()[7]["category_name"] == "Groceries"
  assert response.json()[8]["category_name"] == "Misc."
  assert response.json()[9]["category_name"] == "Personal"
  assert response.json()[10]["category_name"] == "Shopping"
  assert response.json()[11]["category_name"] == "Travel"

#check first user transactions arent leaking to second user
def test_correct_user(create_two_users, create_transactions, create_two_accounts):
  client, first_token, second_token = create_two_users
  client, _, first, _ = create_two_accounts
  create_transactions(1, "30.00", "2026-01-23", first)
  create_transactions(1, "30.00", "2026-02-23", first)
  create_transactions(1, "30.00", "2026-03-23", first)
  create_transactions(1, "30.00", "2026-04-23", first)
  create_transactions(1, "30.00", "2026-05-23", first)
  create_transactions(1, "30.00", "2026-06-23", first)
  create_transactions(1, "30.00", "2026-07-23", first)
  create_transactions(1, "30.00", "2026-08-23", first)
  create_transactions(1, "30.00", "2026-09-23", first)
  create_transactions(1, "30.00", "2026-10-23", first)
  create_transactions(1, "30.00", "2026-11-23", first)
  create_transactions(1, "30.00", "2026-12-23", first)
  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {second_token}"})

  assert response.status_code == 200  
  automotive = response.json()[0]
  #second user category id index
  category_id = automotive["category_id"]
  category_lookup = client.get(f"/categories/{category_id}", headers ={"Authorization" : f"Bearer {second_token}"})
  assert category_lookup.json()["id"] == 14
  assert category_lookup.json()["name"] == "Automotive"

  #index represents month jan == 0 to dec == 11
  assert automotive["monthly_totals"][0] == "0.00"
  assert automotive["monthly_totals"][1] == "0.00"
  assert automotive["monthly_totals"][2] == "0.00"
  assert automotive["monthly_totals"][3] == "0.00"
  assert automotive["monthly_totals"][4] == "0.00"
  assert automotive["monthly_totals"][5] == "0.00"
  assert automotive["monthly_totals"][6] == "0.00"
  assert automotive["monthly_totals"][7] == "0.00"
  assert automotive["monthly_totals"][8] == "0.00"
  assert automotive["monthly_totals"][9] == "0.00"
  assert automotive["monthly_totals"][10] == "0.00"
  assert automotive["monthly_totals"][11] == "0.00"

  first_response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {first_token}"})

  assert first_response.status_code == 200  
  first_automotive = first_response.json()[0]
  #first user category id index
  assert first_automotive["category_id"] == 1
  assert first_automotive["category_name"] == "Automotive"
  #index represents month jan == 0 to dec == 11
  assert first_automotive["monthly_totals"][0] == "30.00"
  assert first_automotive["monthly_totals"][1] == "30.00"
  assert first_automotive["monthly_totals"][2] == "30.00"
  assert first_automotive["monthly_totals"][3] == "30.00"
  assert first_automotive["monthly_totals"][4] == "30.00"
  assert first_automotive["monthly_totals"][5] == "30.00"
  assert first_automotive["monthly_totals"][6] == "30.00"
  assert first_automotive["monthly_totals"][7] == "30.00"
  assert first_automotive["monthly_totals"][8] == "30.00"
  assert first_automotive["monthly_totals"][9] == "30.00"
  assert first_automotive["monthly_totals"][10] == "30.00"
  assert first_automotive["monthly_totals"][11] == "30.00"

#verify budget chart only counts expenses
def test_expenses_only(create_account, create_transactions):
  client, token, _, _ = create_account

  #Automotive
  create_transactions(1, "30.00", "2026-01-23")
  create_transactions(1, "70.00", "2026-01-20", transaction_type="income")
  create_transactions(1, "200.00", "2026-01-17", transaction_type="income")
  create_transactions(1, "400.00", "2026-01-13")

  response = client.get("/budgets/chart-data", headers ={"Authorization" : f"Bearer {token}"})

  assert response.status_code == 200  
  automotive = response.json()[0]
  assert automotive["category_id"] == 1
  assert automotive["category_name"] == "Automotive"
  assert automotive["monthly_totals"][0] == "430.00"



 


  