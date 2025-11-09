from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core import auth as core_auth
from core.user_store import create_user, authenticate_user, init_db, get_user
import asyncio
import os

router = APIRouter()


@router.on_event("startup")
async def startup_init():
    # ensure DB exists
    await init_db()


@router.post("/register")
async def register(payload: dict):
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    created = await create_user(username, password)
    if not created:
        raise HTTPException(status_code=400, detail="user already exists")
    return {"status": "ok", "username": username}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm has .username and .password
    valid = await authenticate_user(form_data.username, form_data.password)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = core_auth.create_jwt_token(sub=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_me(current_user=Depends(core_auth.get_current_user)):
    # current_user is a dict like {"username": ...} or indicates api_key
    return {"current_user": current_user}
