from database import SessionLocal 
from categorizer import transaction_categorizer
from models import Transaction, Category, Account
import asyncio
from decimal import Decimal
from datetime import date, datetime
import json 
from pathlib import Path

def count_helper(field_counter):
  correct = sum(count["correct"] for count in field_counter.values())
  total = sum(count["total"] for count in field_counter.values())
  return correct, total

db = SessionLocal()
try:
  transactions = db.query(Transaction).filter(Transaction.user_id == 25, Transaction.transaction_type != "transfer").all()
  accounts = db.query(Account).filter(Account.user_id == 25).all()
  accounts_info = [{"id": a.id, "name": a.bank_name, "type": a.account_type} for a in accounts]

  category_counts = {}
  account_counts = {}
  type_counts = {}
  amount_counts = {}
  date_counts = {}

  for transaction in transactions: 
    if transaction.transaction_type == "income": 
      description = f"Got {transaction.amount} from {transaction.description}."
    else:
      description = f"Spent {transaction.amount} on {transaction.description}."

    response = asyncio.run(transaction_categorizer(description, accounts_info))

    category = db.query(Category).filter(Category.id == transaction.category_id, Category.user_id == 25).first()
    if category.name not in category_counts:
      category_counts[category.name] = {"total": 0, "correct": 0} 
    if response["category_name"] == category.name:
      category_counts[category.name]["total"] += 1
      category_counts[category.name]["correct"] += 1
    else:
      category_counts[category.name]["total"] += 1
    
    if transaction.account_id not in account_counts:
      account_counts[transaction.account_id] = {"total": 0, "correct": 0}
    if transaction.account_id == response["account_id"]:
      account_counts[transaction.account_id]["total"] += 1
      account_counts[transaction.account_id]["correct"] += 1
    else:
      account_counts[transaction.account_id]["total"] += 1
    
    if transaction.transaction_type not in type_counts:
      type_counts[transaction.transaction_type] = {"total": 0, "correct": 0}
    if transaction.transaction_type == response["transaction_type"]:
      type_counts[transaction.transaction_type]["total"] += 1
      type_counts[transaction.transaction_type]["correct"] += 1
    else:
      type_counts[transaction.transaction_type]["total"] += 1
    
    if transaction.amount not in amount_counts:
      amount_counts[transaction.amount] = {"total": 0, "correct": 0}
    if transaction.amount == Decimal(str(response["amount"])):
      amount_counts[transaction.amount]["total"] += 1
      amount_counts[transaction.amount]["correct"] += 1
    else:
      amount_counts[transaction.amount]["total"] += 1
    
    if transaction.date not in date_counts:
      date_counts[transaction.date] = {"total": 0, "correct": 0}
    if transaction.date == date.fromisoformat(response["date"]):
      date_counts[transaction.date]["total"] += 1
      date_counts[transaction.date]["correct"] += 1
    else:
      date_counts[transaction.date]["total"] += 1
  
  total_counts = category_counts | account_counts | type_counts | amount_counts | date_counts

  print(f"\nCategory")
  category_correct, category_total = count_helper(category_counts)
  print(f"Correct/Total: {category_correct}/{category_total}")
  print(f"Accuracy: %{round((category_correct/category_total) * 100)}")
  print("-" * 40)

  print(f"\nAccounts")
  account_correct, account_total = count_helper(account_counts)
  print(f"Correct/Total: {account_correct}/{account_total}")
  print(f"Accuracy: %{round((account_correct/account_total) * 100)}")
  print("-" * 40)

  print(f"\nTransaction Type")
  type_correct, type_total = count_helper(type_counts)
  print(f"Correct/Total: {type_correct}/{type_total}")
  print(f"Accuracy: %{round((type_correct/type_total) * 100)}")
  print("-" * 40)

  print(f"\nAmount")
  amount_correct, amount_total = count_helper(amount_counts)
  print(f"Correct/Total: {amount_correct}/{amount_total}")
  print(f"Accuracy: %{round((amount_correct/amount_total) * 100)}")
  print("-" * 40)

  print(f"\nDate")
  date_correct, date_total = count_helper(date_counts)
  print(f"Correct/Total: {date_correct}/{date_total}")
  print(f"Accuracy: %{round((date_correct/date_total) * 100)}")
  print("-" * 40)

  print(f"\nTotal Count")
  total_correct, total_total = count_helper(total_counts)
  print(f"Correct/Total: {total_correct}/{total_total}")
  print(f"Accuracy: %{round((total_correct/total_total) * 100)}")
  print("-" * 40)

  bare = {
    "timestamp": datetime.now().isoformat(), 
    "model": "claude-haiku-4-5-20251001", 
    "sample_size": len(transactions), 
    "mode": "bare", 
    "category": {
      "correct": category_correct, 
      "total": category_total, 
      "accuracy": f"%{round((category_correct/category_total * 100))}"
    },
    "account": {
      "correct": account_correct, 
      "total": account_total, 
      "accuracy": f"%{round((account_correct/account_total * 100))}"
    },
    "type": {
      "correct": type_correct, 
      "total": type_total, 
      "accuracy": f"%{round((type_correct/type_total * 100))}"
    },
    "amount": {
      "correct": amount_correct, 
      "total": amount_total, 
      "accuracy": f"%{round((amount_correct/amount_total * 100))}"
    },
    "date": {
      "correct": date_correct, 
      "total": date_total, 
      "accuracy": f"%{round((date_correct/date_total * 100))}"
    }
  }
  
  results_dir = Path(__file__).parent / "results"
  results_dir.mkdir(exist_ok=True)
  filename =  results_dir / f"eval_bare_{datetime.now().strftime('%Y-%m-%d')}.json"
  with open(filename, 'w') as f:
    json.dump(bare, f, indent=2)

finally: db.close()