from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from auth.models.token import Token
from auth.services.auth_service import authenticate_user, create_acces_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    #  -> Token
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if user['role'] == "admin":
        access_token_expires = timedelta(minutes=1440)
        access_token = create_acces_token(
            data={'sub': user['email'], 'admin': True},
            expires_delta=access_token_expires
        )
    elif user['role'] == "user":
        access_token_expires = timedelta(minutes=1440)
        access_token = create_acces_token(
            data={'sub': user['email'], 'admin': False},
            expires_delta=access_token_expires
        )
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="invalid role")

    return { "token": Token(access_token=access_token, token_type="bearer"), "id": str(user['_id']) }