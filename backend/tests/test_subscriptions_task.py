from tasks import _process_due_subscriptions
from models import Subscription
from datetime import date
from freezegun import freeze_time

@freeze_time("2026-04-28")
def test_due_today(create_account, create_subscription, db_session):
  client, token, _, _ = create_account 
  subscription = create_subscription(1, "Netflix", "12.99", "2026-04-28")
  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 1
  assert response.json()[0]["amount"] == "12.99"
  assert response.json()[0]["description"] == "Subscription to Netflix"
  assert response.json()[0]["transaction_type"] == "expense"
  assert response.json()[0]["date"] == "2026-04-28"

  subscription_response = client.get(f"/subscriptions/{subscription.json()["id"]}", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert subscription_response.json()["next_due_date"] == "2026-05-28"

@freeze_time("2026-04-28")
def test_due_future(create_account, create_subscription, db_session):
  client, token, _, _ = create_account 
  subscription = create_subscription(1, "Netflix", "12.99", "2026-04-30")
  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 0

  subscription_response = client.get(f"/subscriptions/{subscription.json()["id"]}", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert subscription_response.json()["next_due_date"] == "2026-04-30"

@freeze_time("2026-04-28")
#check that the sub doesn't move again after being processed 
def test_sub_already_advanced(create_account, create_subscription, db_session):
  client, token, _, _ = create_account 
  subscription = create_subscription(1, "Netflix", "12.99", "2026-04-28")
  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 1
  assert response.json()[0]["amount"] == "12.99"
  assert response.json()[0]["description"] == "Subscription to Netflix"
  assert response.json()[0]["transaction_type"] == "expense"
  assert response.json()[0]["date"] == "2026-04-28"

  subscription_response = client.get(f"/subscriptions/{subscription.json()["id"]}", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert subscription_response.json()["next_due_date"] == "2026-05-28"

  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 1
  assert response.json()[0]["amount"] == "12.99"
  assert response.json()[0]["description"] == "Subscription to Netflix"
  assert response.json()[0]["transaction_type"] == "expense"
  assert response.json()[0]["date"] == "2026-04-28"

  subscription_response = client.get(f"/subscriptions/{subscription.json()["id"]}", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert subscription_response.json()["next_due_date"] == "2026-05-28"

#manually create subscription because of field validator on date
def test_multiple_due(create_account, db_session):
  client, token, account_id, _ = create_account 
  account = client.get(f"accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert account.status_code == 200
  user_id = account.json()["user_id"]

  db_session.add(Subscription(
    user_id = user_id, 
    account_id = account_id, 
    category_id = 1, 
    name = "Netflix", 
    amount = "12.99", 
    next_due_date = date.fromisoformat("2026-04-28")
  ))
  db_session.add(Subscription(
    user_id = user_id, 
    account_id = account_id, 
    category_id = 1, 
    name = "Hulu", 
    amount = "15.67", 
    next_due_date = date.fromisoformat("2026-04-24")
  ))
  db_session.add(Subscription(
    user_id = user_id, 
    account_id = account_id, 
    category_id = 1, 
    name = "Paramount+", 
    amount = "7.99", 
    next_due_date = date.fromisoformat("2026-04-26")
  ))
  db_session.commit()

  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 3
  assert response.json()[0]["amount"] == "12.99"
  assert response.json()[0]["description"] == "Subscription to Netflix"
  assert response.json()[0]["transaction_type"] == "expense"
  assert response.json()[0]["date"] == "2026-04-28"

  assert response.json()[1]["amount"] == "15.67"
  assert response.json()[1]["description"] == "Subscription to Hulu"
  assert response.json()[1]["transaction_type"] == "expense"
  assert response.json()[1]["date"] == "2026-04-24"

  assert response.json()[2]["amount"] == "7.99"
  assert response.json()[2]["description"] == "Subscription to Paramount+"
  assert response.json()[2]["transaction_type"] == "expense"
  assert response.json()[2]["date"] == "2026-04-26"

  subscription_response = client.get(f"/subscriptions", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert len(subscription_response.json()) == 3
  assert subscription_response.json()[0]["next_due_date"] == "2026-05-28"
  assert subscription_response.json()[1]["next_due_date"] == "2026-05-24"
  assert subscription_response.json()[2]["next_due_date"] == "2026-05-26"

def test_due_last_day_of_month(create_account, db_session):
  client, token, account_id, _ = create_account 
  account = client.get(f"accounts/{account_id}", headers ={"Authorization" : f"Bearer {token}"})
  assert account.status_code == 200
  user_id = account.json()["user_id"]
  db_session.add(Subscription(
    user_id = user_id, 
    account_id = account_id, 
    category_id = 1, 
    name = "Netflix", 
    amount = "12.99", 
    next_due_date = date.fromisoformat("2026-01-31")
  ))
  db_session.commit()
  _process_due_subscriptions(db_session)
  response = client.get("/transactions", headers ={"Authorization" : f"Bearer {token}"})
  assert response.status_code == 200 
  assert len(response.json()) == 1
  assert response.json()[0]["amount"] == "12.99"
  assert response.json()[0]["description"] == "Subscription to Netflix"
  assert response.json()[0]["transaction_type"] == "expense"
  assert response.json()[0]["date"] == "2026-01-31"

  subscription_response = client.get(f"/subscriptions", headers ={"Authorization" : f"Bearer {token}"})
  assert subscription_response.status_code == 200
  assert subscription_response.json()[0]["next_due_date"] == "2026-02-28"