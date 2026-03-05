# Finance Tracker API
A RESTful API for personal finance management. Track income and expenses across multiple bank accounts and custom categories, with a summary endpoint that aggregates your financial data.

## Live Demo
https://finance-tracker-production-fb3d.up.railway.app/docs

## Tech Stack
- **FastAPI** — API framework
- **SQLAlchemy** — ORM and database modeling
- **PostgreSQL** — Database (Neon)
- **Alembic** — Database migrations
- **Pydantic** — Data validation and serialization

> Local development uses SQLite by default. The live deployment uses PostgreSQL.

## Features
- Full CRUD on users, accounts, categories, and transactions
- Nested routes to filter transactions by account or category
- Summary endpoint returning total income, expenses, and net balance
- Enum validation on account type and transaction type
- Cascade deletes — deleting a user removes all associated data
- ISO date formatting and field-level validation via Pydantic

## Getting Started
**1. Clone the repo**
```bash
git clone https://github.com/ahuynh6265/finance-tracker.git
cd finance-tracker
```
**2. Install dependencies**
```bash
pip install -r requirements.txt
```
**3. Run migrations**
```bash
alembic upgrade head
```
**4. Start the server**
```bash
uvicorn main:app --reload
```
**5. Open API docs**
Navigate to `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## API Endpoints
### Users
|Method|Endpoint|Description|
|---|---|---|
|GET|`/users`|Get all users|
|GET|`/users/{user_id}`|Get user by ID|
|POST|`/users`|Create users|
|PUT|`/users/{user_id}`|Update user|
|DELETE|`/users/{user_id}`|Delete user|

### Categories
|Method|Endpoint|Description|
|---|---|---|
|GET|`/users/{user_id}/categories`|Get all categories for user|
|GET|`/users/{user_id}/categories/{category_id}`|Get category by ID|
|POST|`/users/{user_id}/categories`|Create categories|
|PUT|`/users/{user_id}/categories/{category_id}`|Update category|
|DELETE|`/users/{user_id}/categories/{category_id}`|Delete category|

### Accounts
|Method|Endpoint|Description|
|---|---|---|
|GET|`/users/{user_id}/accounts`|Get all accounts for user|
|GET|`/users/{user_id}/accounts/{account_id}`|Get account by ID|
|POST|`/users/{user_id}/accounts`|Create accounts|
|PUT|`/users/{user_id}/accounts/{account_id}`|Update account|
|DELETE|`/users/{user_id}/accounts/{account_id}`|Delete account|

### Transactions
|Method|Endpoint|Description|
|---|---|---|
|GET|`/users/{user_id}/transactions`|Get all transactions for user|
|GET|`/users/{user_id}/transactions/{transaction_id}`|Get transaction by ID|
|GET|`/users/{user_id}/accounts/{account_id}/transactions`|Get transactions by account|
|GET|`/users/{user_id}/categories/{category_id}/transactions`|Get transactions by category|
|POST|`/users/{user_id}/transactions`|Create transactions|
|PUT|`/users/{user_id}/transactions/{transaction_id}`|Update transaction|
|DELETE|`/users/{user_id}/transactions/{transaction_id}`|Delete transaction|

### Summary
|Method|Endpoint|Description|
|---|---|---|
|GET|`/users/{user_id}/summary`|Get total income, expenses, and net balance|

## Data Models
**Account types:** `checking`, `savings`, `credit`  
**Transaction types:** `income`, `expense`  
**Date format:** `YYYY-MM-DD`