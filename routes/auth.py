"""Authentication routes for user registration, login, and JWT token management."""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import authenticate_user
from core.auth_models import Token, UserCreate, UserLogin, WeChatLogin, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.database import db, hash_password, User

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

@auth_router.post("/register", response_model=Token)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    if db.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    if db.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw
    )
    
    db.create_user(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user and return a JWT token."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token endpoint."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/wechat-login", response_model=Token)
async def wechat_login(wechat_data: WeChatLogin):
    """Login or register a user via WeChat."""
    # This is a simplified implementation
    # In a real application, you would verify the WeChat code with WeChat's API
    # and get the user's openid and other information
    
    # For demonstration purposes, we'll simulate getting user info from WeChat
    # In practice, you would make an API call to WeChat to exchange the code for user info
    
    # Check if user with this WeChat openid already exists
    # user = db.get_user_by_wechat_openid(wechat_data.code)
    
    # If not, create a new user or link to existing account
    # This implementation would need to be expanded based on your WeChat integration
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="WeChat login not fully implemented",
    )

@auth_router.get("/token-display")
async def display_token():
    """Display page for JWT token (for copying to OpenBB Workspace)."""
    # This endpoint would typically be protected and return the current user's token info
    return {"message": "JWT token display page - implementation needed"}

@auth_router.get("/me")
async def read_users_me(token: str):
    """Get current user information."""
    from core.auth import get_user_from_token
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": user.username, "email": user.email}