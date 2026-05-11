import asyncio
from categorizer import transaction_categorizer

inputs = ["Spent $47.32 at Wawa for lunch", "Got paid $2400 today", "Transferred $500 to my savings", "Got gas last week cost 54.23", "Spent 200 at red lobster 12 days ago.", "Repaired tires at Auto Service shop, cost 450"]

accounts = [{"id": 2, "name": "Chase", "type": "checking"}, {"id": 1, "name": "Wells Fargo", "type": "savings"}]

for input in inputs: 
  result = asyncio.run(transaction_categorizer(input, accounts))
  print(f"\nInput: {input}")
  print(result)
  print("-" * 40)