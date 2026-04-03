from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.categories import router as categories_router
from routes.accounts import router as accounts_router
from routes.transactions import router as transactions_router 
from routes.summary import router as summary_router
from routes.auth_routes import router as auth_router
from routes.budgets import router as budgets_router

app = FastAPI() 
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(summary_router)
app.include_router(auth_router)
app.include_router(budgets_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


