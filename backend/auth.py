


from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel
from schemas import RegisterRequest, LoginRequest, User, UserInDB
from db import get_db
from config import JWT_SECRET, ALGORITHM,ACCESS_TTL
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

import jwt
import datetime


password_hash = PasswordHash.recommended()

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

def get_user_auth(creds:HTTPBasicCredentials = Depends(HTTPBearer())):
    token = creds.credentials
    payload = jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[ALGORITHM],
    )
    return payload

def get_access_token(user_id:int, username:str):
    access_token = jwt.encode(
        payload={
            "id":user_id,
            "username": username,
            "exp": datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TTL),
        },
        key=JWT_SECRET,
        algorithm=ALGORITHM,
    )
    
    return access_token