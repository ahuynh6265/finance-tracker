from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
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
import os, sentry_sdk, structlog
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded 
from limiter import limiter
from logging_config import configure_logging 
from middleware import request_id_middleware

load_dotenv()
configure_logging()
log = structlog.get_logger()

sentry_sdk.init(
  dsn = os.getenv("SENTRY_DSN"), 
  send_default_pii=True,
  traces_sample_rate=0.1,
  environment=os.getenv("APP_ENV", "development")
)

app = FastAPI() 

app.state.limiter = limiter 
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.middleware("http")(request_id_middleware)

async def unhandled_exception_handler(request: Request, exc: Exception):
  log.exception("unhandled_route_error", path=str(request.url.path), method=request.method)
  return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(users_router)
app.include_router(categories_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(summary_router)
app.include_router(auth_router)
app.include_router(budgets_router)
app.include_router(goals_router)
app.include_router(subscriptions_router)

@app.get("/health")
def check_backend(): 
  return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://finance-tracker-navy-xi.vercel.app", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
