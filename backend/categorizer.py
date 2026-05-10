from anthropic import AsyncAnthropic
from routes import categories
from datetime import date 

client = AsyncAnthropic()

async def transaction_categorizer(description: str, account_names: list[str]):
  response = await client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    tools=[
      {
        "name": "categorize_transaction", 
        "description": "assign correct category to transaction", 
        "input_schema": {
          "type": "object", 
          "properties": {
            "account_name": {"type": "string", "enum": account_names, "description": "the account the transaction is from (expense/transfer source) or to (income)."},

            "destination_account_name": {"type": "string", "enum": account_names, "description": "the destination account when transaction_type is 'transfer'; omit otherwise."}, 

            "amount": {"type": "number", "description": "cost of the transaction"},

            "category_name": {"type": "string", "enum": categories.DEFAULT_CATEGORIES, "description": "name of the category"},

            "transaction_type": {"type": "string", "enum": ["income", "expense", "transfer"], "description": "the type of transaction"}, 

            "description": {"type": "string", "description": "description of the transaction being made"}, 

            "date": {"type": "string", "description": "date of the transaction in YYYY-MM-DD format e.g. 2026-01-01"},

            "confidence": {"type": "number", "minimum": 0, "maximum": 1, "description": "how confident the model is in its accuracy e.g. 0.76"}
          },
          "required": ["account_name", "amount", "category_name", "transaction_type", "description", "date", "confidence"]
        },
      }
    ],
    messages=[{"role": "user", "content": f"{description}"}],
    system=f"Today's date is {date.today()}. The user's accounts are: {account_names}. For transfers, set both account_name (source) and destination_account_name (target). For income or expense, set only account_name.",
    tool_choice={"type": "tool", "name": "categorize_transaction"}
  )

  for block in response.content: 
    if block.type == "tool_use": return block.input
  
  raise Exception("Model returned text instead of using the tool")
