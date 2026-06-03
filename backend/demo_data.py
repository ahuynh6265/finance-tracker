from models import User, Account, Category, Transaction, Goal, Budget, Subscription
from database import SessionLocal 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from random import uniform, randint, choice
from subscription_service import run_due_subscriptions
from decimal import Decimal

"""
Category Names: 
"Automotive", "Bills & utilities", "Cash out", "Education", "Entertainment", "Food & drink", "Gas", "Groceries", "Income", "Misc.", "Personal", "Shopping", "Transfer", "Travel"
"""

#generate random dates per month:
def random_date_in_month(month): 
  start_date = date(datetime.now().year, month, 1)
  end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
  days_in_month = end_date.day

  #generate random day, minus by 1 because starting day starts at 1 
  random_day = randint(0, days_in_month - 1)

  return start_date + relativedelta(days=random_day)

def generate_demo_data():
  db = SessionLocal()

  try: 
    demo_user = db.query(User).filter(User.email == "demo@example.com").first()
    if demo_user is None: 
      raise RuntimeError("Demo user not found — register demo@example.com first")

    categories = db.query(Category).filter(Category.user_id == demo_user.id).all()

    db.query(Account).filter(Account.user_id == demo_user.id).delete()
    db.query(Budget).filter(Budget.user_id == demo_user.id).delete()
    db.query(Goal).filter(Goal.user_id == demo_user.id).delete()

    categories_by_name = {}
    for category in categories: 
      categories_by_name[category.name] = category.id 

    checking_account = Account(
      user_id = demo_user.id, 
      bank_name = "Chase", 
      account_type = "checking", 
      balance = Decimal("25000")
    )

    savings_account = Account(
      user_id = demo_user.id,
      bank_name = "Wells Fargo", 
      account_type = "savings", 
      balance = Decimal("50000")
    )
    db.add_all([checking_account, savings_account])
    db.flush()
    
    #income transactions, adjust balance after all income transactions finish, income goes only to savings
    starting_date = date(datetime.now().year, 1, 1)
    current_month = datetime.now().month 
    total_income = 0
    for _ in range(current_month): 
      num = round(uniform(1500, 2500), 2)
      total_income += num
      db.add(
        Transaction(
          user_id = demo_user.id, 
          account_id = savings_account.id, 
          category_id = categories_by_name["Income"], 
          amount = num,
          transaction_type = "income", 
          description = "Paycheck", 
          date = starting_date
        )
      )
      starting_date += relativedelta(months=1)
    total_income = round(total_income, 2)
    savings_account.balance += Decimal(str(total_income))
    
    #expense transactions, adjust balance after all expense transactions finish, expense only uses checkings account
    total_expense = 0
    common_categories = {
      "Food & drink": ["Taco Bell", "Chipotle", "Moe's Southwest Grill", "Chick-fil-A", "Culver's", "Starbucks"], 
      "Shopping": ["Clothing", "Electronics", "Books", "Furniture", "Sports Equipment"], 
      "Entertainment": ["Movie", "Concert", "Theater", "Streaming", "Gaming"],
      "Gas": ["Wawa", "7-Eleven", "RaceTrac", "Chevron", "Shell"]
    }
    for i in range(1, current_month):
      #generate three transactions for common categories
      for _ in range(3):  
        batch1 = [
          Transaction(
            user_id = demo_user.id, 
            account_id = checking_account.id, 
            category_id = categories_by_name["Food & drink"], 
            amount = round(uniform(7, 22), 2),
            transaction_type = "expense", 
            description = choice(common_categories["Food & drink"]), 
            date = random_date_in_month(i)
          ),
          Transaction(
            user_id = demo_user.id, 
            account_id = checking_account.id, 
            category_id = categories_by_name["Shopping"], 
            amount = round(uniform(15, 150), 2),
            transaction_type = "expense", 
            description = choice(common_categories["Shopping"]), 
            date = random_date_in_month(i)
          ),
          Transaction(
            user_id = demo_user.id, 
            account_id = checking_account.id, 
            category_id = categories_by_name["Entertainment"], 
            amount = round(uniform(10, 70), 2),
            transaction_type = "expense", 
            description = choice(common_categories["Entertainment"]), 
            date = random_date_in_month(i)
          ),
        ]
        total_expense += sum(t.amount for t in batch1)
        db.add_all(batch1)
        
      batch2 = [
        Transaction(
          user_id = demo_user.id, 
          account_id = checking_account.id, 
          category_id = categories_by_name["Bills & utilities"], 
          amount = round(uniform(150, 155), 2),
          transaction_type = "expense", 
          description = "Water and Electric", 
          date = random_date_in_month(i)
        ),
        Transaction(
          user_id = demo_user.id, 
          account_id = checking_account.id, 
          category_id = categories_by_name["Groceries"], 
          amount = round(uniform(300, 400), 2),
          transaction_type = "expense", 
          description = "Publix", 
          date = random_date_in_month(i)
        ),
        Transaction(
          user_id = demo_user.id, 
          account_id = checking_account.id, 
          category_id = categories_by_name["Gas"], 
          amount = round(uniform(40, 60), 2),
          transaction_type = "expense", 
          description = f"Gas at {choice(common_categories["Gas"])}", 
          date = random_date_in_month(i)
        ),
      ]
      total_expense += sum(t.amount for t in batch2)
      db.add_all(batch2)
      
    #one transactions on random days that are not as common
    batch3 = [
      Transaction(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Automotive"], 
        amount = round(uniform(35, 50), 2),
        transaction_type = "expense", 
        description = "Oil Change", 
        date = random_date_in_month(1)
      ), 
      Transaction(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Personal"], 
        amount = round(uniform(15, 25), 2),
        transaction_type = "expense", 
        description = "Shipped package with Fedex", 
        date = random_date_in_month(3)
      ), 
      Transaction(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Travel"], 
        amount = round(uniform(150, 300), 2),
        transaction_type = "expense", 
        description = "Flight to Boston using Delta Airlines", 
        date = random_date_in_month(4)
      ),
      Transaction(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Cash out"], 
        amount = round(uniform(20, 100)),
        transaction_type = "expense", 
        description = "ATM Withdrawal", 
        date = random_date_in_month(2)
      ),
      Transaction(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Education"], 
        amount = round(uniform(400, 700), 2),
        transaction_type = "expense", 
        description = "UCF Tuition", 
        date = random_date_in_month(1)
      ), 
    ]
    total_expense += sum(t.amount for t in batch3)
    total_expense = round(total_expense, 2)
    db.add_all(batch3)
    checking_account.balance -= Decimal(str(total_expense))

    #transfer transactions, only transfers from savings to checking
    transfer_total = 0
    for i in range(1, current_month):
      transfer = Transaction(
        user_id = demo_user.id, 
        account_id = savings_account.id, 
        category_id = categories_by_name["Transfer"], 
        destination_account_id = checking_account.id,
        amount = round(uniform(200, 1000), 2),
        transaction_type = "transfer", 
        description = f"Transfer to {checking_account.bank_name}", 
        date = random_date_in_month(i)
      )
      transfer_total += transfer.amount
      db.add(transfer)
    db.flush()
    transfer_total = round(transfer_total, 2)
    savings_account.balance -= Decimal(str(transfer_total))
    checking_account.balance += Decimal(str(transfer_total ))
    
    #budgets - creating budgets for common categories
    common_budget_categories = ["Entertainment", "Food & drink", "Shopping"]
    for category_name in common_budget_categories: 
      db.add(
        Budget(
          user_id = demo_user.id,
          category_id = categories_by_name[category_name], 
          budget_limit = round(uniform(150, 200))
        )
      )
    
    #goals - two goals
    goals = ["Vacation Fund", "Emergency Fund"]
    for goal_name in goals:
      db.add(
        Goal(
          user_id = demo_user.id, 
          name = goal_name, 
          target_amount = round(uniform(3000, 5000)),
          deadline = random_date_in_month(randint(10,12)) #random month oct-dec
        )
      )
    
    #subscriptions - three subscriptions, start from first month, 5 transactions per subscription
    subscriptions = ["Netflix", "Hulu", "HBO Max"]
    for subscription_name in subscriptions: 
      subscription = Subscription(
        user_id = demo_user.id, 
        account_id = checking_account.id, 
        category_id = categories_by_name["Entertainment"], 
        name = subscription_name, 
        amount = round(uniform(10, 20), 2), 
        next_due_date = random_date_in_month(1)
      )
      db.add(subscription)
    db.flush()
    
    run_due_subscriptions(db)

    db.commit()

  finally: 
    db.close()
