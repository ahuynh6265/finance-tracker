# Finance Tracker

![CI](https://github.com/ahuynh6265/finance-tracker/actions/workflows/ci.yml/badge.svg)

A full-stack personal finance application for tracking income, expenses, budgets, savings goals, and recurring subscriptions across multiple bank accounts. Built with FastAPI, React, and PostgreSQL, with an async task queue powered by Celery and Redis for scheduled background work.

## Live Demo

https://finance-tracker-navy-xi.vercel.app/

## Architecture

Five coordinated services in production:

- **Frontend** (Vercel) — React SPA with preview deployments per branch
- **Backend Web** (Render Web Service) — FastAPI HTTP API for all CRUD requests
- **Celery Worker** (Render Background Worker) — executes background tasks pulled from Redis
- **Celery Beat** (Render Background Worker) — scheduler that fires periodic tasks
- **Redis** (Render Key Value) — message broker between FastAPI/Beat and the worker
- **PostgreSQL** (Neon) — primary data store with branch-based dev/prod isolation

The web service handles synchronous user-facing requests. Long-running and scheduled work — currently a daily job that processes due subscriptions — is offloaded to the worker via Redis, keeping API responses fast and decoupling user actions from periodic system jobs.

```
Frontend (Vercel)
     │  HTTPS
     ▼
FastAPI Web (Render) ────────────►  PostgreSQL (Neon)
                                          ▲
                                          │
Celery Beat ─────► Redis ─────► Celery Worker
(scheduler)      (broker)       (executor)
```

## Tech Stack

### Backend

- **FastAPI** — API framework with dependency injection
- **SQLAlchemy 2.0** — ORM and database modeling, with explicit `ondelete` behavior on every FK
- **PostgreSQL** (Neon) — primary database with separate dev and prod branches
- **Alembic** — schema migrations
- **Pydantic** — request/response validation, computed fields for derived data, field validators for input sanitization
- **Celery** — distributed task queue
- **Redis** — Celery broker
- **python-dateutil** — calendar-aware date arithmetic for monthly cycle advancement
- **python-jose** — JWT signing and validation
- **passlib (bcrypt)** — password hashing
- **pytest** — backend test suite
- **freezegun** — time-frozen tests for date-sensitive logic

### Frontend

- **React** — SPA with React Router
- **Axios** — HTTP client with refresh-token interceptor for silent auth retry
- **Tailwind CSS** — utility-first styling with a glassmorphism design system
- **MUI (Material UI)** — Buttons, Icons, Tooltips, Modals, LinearProgress
- **Recharts** — chart library for dashboard visualizations

### Deployment

- **Vercel** — frontend hosting + per-branch preview deployments
- **Render** — backend web service, two background workers, managed Redis instance
- **Neon** — managed PostgreSQL with database branching for dev/prod isolation

## Features

### Core

- JWT authentication with refresh-token rotation; frontend interceptor handles silent token refresh on 401
- Multi-account support with per-account transaction history and live balance tracking
- Custom categories — default set seeded on user registration
- Income / expense / transfer transactions with cross-account transfers
- Pagination, filtering by month, and filtering by category on the transactions table

### Budgets

- Per-category monthly budget limits with current spend, remaining balance, and over-budget warnings
- Monthly spending bar chart per category
- Status indicators: green (good), yellow (close to limit), red (over budget)

### Goals

- Savings goals with target amount, deadline, and current funded amount
- Fund / withdraw flow that creates transfer transactions between an account and the goal
- Cumulative progress chart per goal
- Funding pace calculator: weekly, biweekly, or monthly contribution recommendation to hit deadline
- Status: on-track, funded, or overdue (deadline passed without hitting target)

### Subscriptions (background-task feature)

- Recurring monthly bills (Netflix, Spotify, gym, etc.)
- A daily Celery beat schedule fires `process_due_subscriptions` at midnight UTC
- The Celery worker queries due subscriptions, creates expense transactions, advances each subscription's `next_due_date` by one month using `dateutil.relativedelta` (handles end-of-month edge cases like Jan 31 → Feb 28)
- Per-subscription failure isolation so one corrupted record doesn't block the rest of the batch
- Total monthly cost, active subscription count, and annual projection on the Subscriptions page

### Dashboard

- Net worth hero card (accounts + savings goals)
- This-month income, expenses, and net balance stat cards
- Income vs. expenses line chart over the last 6 months
- Budgets at risk with progress bars and color-coded status
- Goals snapshot with funded / on-track / overdue status

## Architecture Highlights

### Async task pipeline

The `process_due_subscriptions` task is split into a pure-logic helper (`_process_due_subscriptions(db)`) and a Celery-decorated wrapper (`process_due_subscriptions()`):

- The helper takes a SQLAlchemy session as a parameter and contains all the per-subscription logic. It's unit-tested with the SQLite test session, no Redis or Celery worker required.
- The wrapper opens a real `SessionLocal()`, calls the helper, and closes the session in a `finally` block. This is what beat actually invokes in production.

This separation keeps the Celery infrastructure out of the business-logic tests and lets the same logic run in either environment.

### Deployment workflow

- `main` branch → production. Pushing to main triggers Render's web service redeploy + Vercel's production deploy.
- Feature branches → Vercel preview deployment with a unique URL per branch. Render's other services don't redeploy on non-main pushes.
- Schema migrations are applied to the Neon dev database branch first, verified locally, then applied to the prod branch before code is merged. This avoids the "code expects table that doesn't exist yet" deploy ordering bug.
- Local dev points at the Neon dev branch via `.env`; prod credentials live only in Render's environment variables.

### Foreign-key behavior

Every foreign key on the schema declares explicit `ondelete` behavior:

- `CASCADE` on user-owned tables (deleting a user removes their categories, accounts, transactions, budgets, goals, subscriptions)
- `CASCADE` on `Transaction.account_id` (deleting an account removes its transactions)
- `SET NULL` on `Transaction.destination_account_id`, `Transaction.source_goal_id`, `Transaction.destination_goal_id` (transactions persist as historical records when the related entity is deleted)
- Default `RESTRICT` on `category_id` references (deletion blocked if any transactions/budgets reference the category)

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (locally on macOS via Homebrew: `brew install redis && brew services start redis`)
- A PostgreSQL connection string (Neon, or local Postgres)

### 1. Clone the repo

```bash
git clone https://github.com/ahuynh6265/finance-tracker.git
cd finance-tracker
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
```

Create `backend/.env`:

```
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=<random-string-for-jwt-signing>
REDIS_URL=redis://localhost:6379/0
```

Apply migrations:

```bash
alembic upgrade head
```

### 3. Run the backend services

Each in its own terminal, all from `backend/`:

```bash
# FastAPI web
uvicorn main:app --reload

# Celery worker
celery -A celery_app worker --loglevel=info --concurrency=1

# Celery beat scheduler
celery -A celery_app beat --loglevel=info
```

### 4. Frontend setup

```bash
cd ../frontend
npm install
```

Create `frontend/.env`:

```
REACT_APP_API_URL=http://localhost:8000
```

Start the dev server:

```bash
npm start
```

App will be available at `http://localhost:3000`.

### 5. Run tests

```bash
cd backend
pytest
```

## API Endpoints

All authenticated routes require a `Authorization: Bearer <jwt>` header. User context is resolved from the token; user IDs are not in the URL.

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user (auto-seeds default categories) |
| POST | `/auth/login` | Log in, returns access + refresh tokens |
| POST | `/auth/refresh` | Refresh an expired access token |
| GET | `/auth/me` | Return the current user's email |

### Accounts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/accounts` | List user's accounts |
| GET | `/accounts/{id}` | Get account by ID |
| GET | `/accounts/{id}/summary` | Get account's monthly income / expenses / net |
| GET | `/accounts/{id}/transactions` | Get transactions for an account |
| POST | `/accounts` | Create an account |
| PUT | `/accounts/{id}` | Update an account |
| DELETE | `/accounts/{id}` | Delete an account (cascades transactions) |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| GET | `/categories` | List user's categories |
| GET | `/categories/{id}` | Get category by ID |
| GET | `/categories/{id}/transactions` | Get transactions in a category |
| DELETE | `/categories/{id}/transactions` | Bulk-delete all transactions in a category |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/transactions` | List all transactions |
| GET | `/transactions/{id}` | Get transaction by ID |
| POST | `/transactions` | Create a transaction (income, expense, or transfer) |
| PUT | `/transactions/{id}` | Update a transaction (reverses old balance, applies new) |
| DELETE | `/transactions/{id}` | Delete a transaction (reverses balance) |

### Budgets

| Method | Endpoint | Description |
|---|---|---|
| GET | `/budgets` | List budgets with current monthly spend |
| GET | `/budgets/{id}` | Get budget by ID |
| GET | `/budgets/chart-data` | Monthly spending data per category for the year |
| POST | `/budgets` | Create a budget for a category |
| PATCH | `/budgets/{id}` | Update a budget limit |
| DELETE | `/budgets/{id}` | Delete a budget |

### Goals

| Method | Endpoint | Description |
|---|---|---|
| GET | `/goals` | List goals |
| GET | `/goals/{id}` | Get goal by ID |
| GET | `/goals/{id}/chart-data` | Cumulative progress over time |
| POST | `/goals` | Create a goal |
| PUT | `/goals/{id}` | Update a goal |
| PUT | `/goals/{id}/current-amount` | Fund a goal (creates transfer transaction) |
| PUT | `/goals/{id}/withdraw` | Withdraw from a goal (creates transfer transaction) |
| DELETE | `/goals/{id}` | Delete a goal (only if `current_amount` is 0) |

### Subscriptions

| Method | Endpoint | Description |
|---|---|---|
| GET | `/subscriptions` | List user's subscriptions |
| GET | `/subscriptions/{id}` | Get subscription by ID |
| POST | `/subscriptions` | Create a subscription |
| PUT | `/subscriptions/{id}` | Update a subscription |
| DELETE | `/subscriptions/{id}` | Delete a subscription |

### Summary

| Method | Endpoint | Description |
|---|---|---|
| GET | `/summary` | Net worth + all-time totals (income, expenses, accounts, goals) |
| GET | `/summary/monthly` | Per-month income and expenses time series for charts |

## Data Models

- **Account types:** `checking`, `savings`, `credit`
- **Transaction types:** `income`, `expense`, `transfer`
- **Date format:** `YYYY-MM-DD` (ISO 8601)
- **Money:** stored as `Numeric(10, 2)` (Python `Decimal`, never `float`)
