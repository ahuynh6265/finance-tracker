from freezegun import freeze_time
from datetime import date, datetime

#verify that the goal chart is created and is empty with 5 entries for each day 
def test_verify_empty_goal(create_account_goal_chart): 
  client, token, account_id, _ = create_account_goal_chart
  with freeze_time("2026-01-01"):
    response = client.post("/goals", headers ={"Authorization" : f"Bearer {token}"}, json = {"name": "Vacation Fund", "target_amount": "3000.00", "deadline": "2026-01-05",}) 
  goal_id = response.json()["id"]

  assert response.status_code == 201 
  assert response.json()["name"] == "Vacation Fund"
  assert response.json()["target_amount"] == "3000.00"
  assert response.json()["current_amount"] == "0.00"
  assert response.json()["deadline"] == "2026-01-05"

  chart = client.get(f"/goals/{goal_id}/chart-data",  headers ={"Authorization" : f"Bearer {token}"})
  assert chart.status_code == 200
  assert len(chart.json()) == 5


def test_single_fund(create_account_goal_chart, fund_or_withdraw):
  client, token, account_id, _ = create_account_goal_chart
  
  fund_or_withdraw("fund", "100.00", date(2026,4,23))
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  goal = goals.json()[0]
  goals_chart = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert goals_chart.status_code == 200
  assert goals_chart.json()[2]["date"] == "2026-04-23"
  assert goals_chart.json()[2]["cumulative"] == "100.00"


def test_withdraw_later(create_account_goal_chart, fund_or_withdraw):
  client, token, account_id, _ = create_account_goal_chart
  fund_or_withdraw("fund", "100.00", date(2026,4,23))
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  goal = goals.json()[0]

  goals_chart = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert goals_chart.status_code == 200

  #length between date created and deadline
  assert len(goals_chart.json()) == (date.fromisoformat(goal["deadline"]) - datetime.fromisoformat(goal["created_at"]).date()).days + 1

  assert goals_chart.json()[2]["date"] == "2026-04-23"
  assert goals_chart.json()[2]["cumulative"] == "100.00"

  fund_or_withdraw("withdraw", "50.00", date(2026,4,29))
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  goal = goals.json()[0]
  goals_chart = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert goals_chart.status_code == 200
  assert goals_chart.json()[8]["date"] == "2026-04-29"
  assert goals_chart.json()[8]["cumulative"] == "50.00"

  #test days in between 
  assert goals_chart.json()[6]["date"] == "2026-04-27"
  assert goals_chart.json()[2]["cumulative"] == "100.00"

def test_multiple_same_day(create_account_goal_chart, fund_or_withdraw):
  client, token, account_id, _ = create_account_goal_chart
  fund_or_withdraw("fund", "100.00", date(2026,4,23))
  fund_or_withdraw("fund", "100.00", date(2026,4,23))
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  goal = goals.json()[0]

  goals_chart = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert goals_chart.status_code == 200

  #length between date created and deadline
  assert len(goals_chart.json()) == (date.fromisoformat(goal["deadline"]) - datetime.fromisoformat(goal["created_at"]).date()).days + 1

  assert goals_chart.json()[2]["date"] == "2026-04-23"
  assert goals_chart.json()[2]["cumulative"] == "200.00"

def test_multiple_day(create_account_goal_chart, fund_or_withdraw):
  client, token, account_id, _ = create_account_goal_chart
  fund_or_withdraw("fund", "100.00", date(2026,4,21))
  fund_or_withdraw("fund", "100.00", date(2026,4,23))
  fund_or_withdraw("fund", "150.00", date(2026,4,24))
  fund_or_withdraw("withdraw", "50.00", date(2026,4,24))
  fund_or_withdraw("fund", "200.00", date(2026,4,25))
  fund_or_withdraw("fund", "150.00", date(2026,4,25))
  fund_or_withdraw("withdraw", "50.00", date(2026,4,26))
  fund_or_withdraw("withdraw", "100.00", date(2026,4,27))
  fund_or_withdraw("fund", "500.00", date(2026,4,30))
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {token}"})
  goal = goals.json()[0]

  goals_chart = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {token}"})
  assert goals_chart.status_code == 200

  #length between date created and deadline
  assert len(goals_chart.json()) == (date.fromisoformat(goal["deadline"]) - datetime.fromisoformat(goal["created_at"]).date()).days + 1

  #day 1 +100
  assert goals_chart.json()[0]["date"] == "2026-04-21"
  assert goals_chart.json()[0]["cumulative"] == "100.00"
  #day 2 no change
  assert goals_chart.json()[1]["date"] == "2026-04-22"
  assert goals_chart.json()[1]["cumulative"] == "100.00"
  #day 3 +100 
  assert goals_chart.json()[2]["date"] == "2026-04-23"
  assert goals_chart.json()[2]["cumulative"] == "200.00"
  #day 4 +150 -50
  assert goals_chart.json()[3]["date"] == "2026-04-24"
  assert goals_chart.json()[3]["cumulative"] == "300.00"
  #day5 +200 +150
  assert goals_chart.json()[4]["date"] == "2026-04-25"
  assert goals_chart.json()[4]["cumulative"] == "650.00"
  #day6 -50
  assert goals_chart.json()[5]["date"] == "2026-04-26"
  assert goals_chart.json()[5]["cumulative"] == "600.00"
  #day7 -100
  assert goals_chart.json()[6]["date"] == "2026-04-27"
  assert goals_chart.json()[6]["cumulative"] == "500.00"
  #day 8 no change
  assert goals_chart.json()[7]["date"] == "2026-04-28"
  assert goals_chart.json()[7]["cumulative"] == "500.00"
  #day 9 no change
  assert goals_chart.json()[8]["date"] == "2026-04-29"
  assert goals_chart.json()[8]["cumulative"] == "500.00"
  #final day +500
  assert goals_chart.json()[9]["date"] == "2026-04-30"
  assert goals_chart.json()[9]["cumulative"] == "1000.00"

def test_correct_user(create_two_users, fund_or_withdraw, create_two_accounts):
  client, first_token, second_token = create_two_users
  client, _, first, _ = create_two_accounts
  goals = client.get("/goals", headers ={"Authorization" : f"Bearer {first_token}"})
  goal = goals.json()[0]
  fund_or_withdraw("fund", "100.00", date(2026,4,23), first)

  response = client.get(f"/goals/{goal['id']}/chart-data", headers ={"Authorization" : f"Bearer {second_token}"})

  assert response.status_code == 403
  assert response.json()["detail"] == f"Goal ID {goal['id']} does not belong to user" 