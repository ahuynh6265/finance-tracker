from structlog.contextvars import bind_contextvars, clear_contextvars
from fastapi import Request, Response
import uuid 

async def request_id_middleware(request: Request, call_next):
  #check if request has an id if not generate one
  request_id = request.headers.get("X-Request-ID")
  if not request_id: 
    request_id = str(uuid.uuid4())
  
  #bind the id so downstream code can read it without it being passed as an argument
  bind_contextvars(request_id=request_id)
  try:
    response: Response = await call_next(request)
  finally:
    clear_contextvars()

  response.headers["X-Request-ID"] = request_id
  return response 
