from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_wechat_session,
    get_password_hash,
    fake_users_db,
)
from core.auth_models import Token, User, UserCreate, WechatLoginRequest
from core.config import config

router = APIRouter()


@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if username already exists
    if user_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    user_dict.pop("password")
    user_dict.update({
        "id": len(fake_users_db) + 1,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    
    fake_users_db[user_data.username] = user_dict
    return User(**user_dict)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username and password to get access token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": config.access_token_expire_minutes * 60,
    }


@router.post("/wechat/login", response_model=Token)
async def wechat_login(login_data: WechatLoginRequest):
    """Login with WeChat code to get access token."""
    try:
        wechat_user = await get_wechat_session(login_data.code)
    except HTTPException as e:
        raise e
    
    # Create or get user based on WeChat openid
    username = f"wx_{wechat_user.openid}"
    if username not in fake_users_db:
        user_dict = {
            "id": len(fake_users_db) + 1,
            "username": username,
            "email": f"{username}@wechat.user",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "hashed_password": "",  # WeChat users don't have passwords
        }
        fake_users_db[username] = user_dict
    
    access_token_expires = timedelta(minutes=config.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": config.access_token_expire_minutes * 60,
    }


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user