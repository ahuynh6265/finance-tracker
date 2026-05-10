import asyncio
from categorizer import transaction_categorizer

inputs = ["Spent $47.32 at Wawa for lunch", "Got paid $2400 today", "Transferred $500 to my savings", "Got gas last week cost 54.23", "Spent 200 at red lobster 12 days ago."]

accounts = ["Chase Checking", "Wells Fargo Savings"]

for input in inputs: 
  result = asyncio.run(transaction_categorizer(input, accounts))
  print(f"\nInput: {input}")
  print(result)
  print("-" * 40)