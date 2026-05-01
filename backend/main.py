from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.categories import router as categories_router
from routes.accounts import router as accounts_router
from routes.transactions import router as transactions_router 
from routes.summary import router as summary_router
from routes.auth_routes import router as auth_router
from routes.budgets import router as budgets_router
from routes.goals import router as goals_router
from routes.subscriptions import router as subscriptions_router
import os 
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

sentry_sdk.init(
  dsn = os.getenv("SENTRY_DSN"), 
  send_default_pii=True,
  traces_sample_rate=0.1,
  environment=os.getenv("ENVIRONMENT", "development")
)

app = FastAPI() 
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(summary_router)
app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(goals_router)
app.include_router(subscriptions_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


