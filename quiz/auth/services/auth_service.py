import os
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt

from auth.models.token import TokenData
from models import UserRequest
from auth.utils.auth_utils import verify_password
from mongodb import users_collection

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def authenticate_user(email: str, password: str):
    user = users_collection.find_one({ "email": email })
    if not user:
        return False
    if not verify_password(password, user['password_hash']):
        return False

    return user

def create_acces_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception

    user = users_collection.find_one({ "email": token_data.email })
    if not user:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: UserRequest = Depends(get_current_user)):
    return current_user