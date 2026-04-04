from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer 
from dotenv import load_dotenv 
from datetime import datetime, timezone, timedelta
import os 

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password):
  hash = pbkdf2_sha256.hash(password)
  return hash 

def verify_password(password, hash_password):
  return pbkdf2_sha256.verify(password, hash_password)

def create_token(name, email, id):
  access_token = jwt.encode({"name": name, "email": email, "id": id, "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15), "type": "access"}, SECRET_KEY, algorithm="HS256")

  refresh_token = jwt.encode({"name": name, "email": email, "id": id, "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1), "type": "refresh"}, SECRET_KEY, algorithm="HS256")

  return access_token, refresh_token

def get_current_user(token: str = Depends(oauth2_scheme)):
  try:
    current_user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if current_user["type"] != "access":
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
  return current_user
