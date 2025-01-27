from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.db.schemas import User
from src.modules.user import services as user_serivces
from passlib.context import CryptContext
from pydantic import BaseModel

from src.utils.omit import omit

SECRET_KEY="1c-b2-c3-e4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 10

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

def authenticate_user(username: str, password: str):
    user = user_serivces.get_user_by_email(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_request_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = user_serivces.get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception

    return user

def register(user: User):
  payload = user
  payload.password = hash_password(user.password)
  user_serivces.create_user(payload)

def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
