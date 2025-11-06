"""Authentication models and utilities."""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic import BaseModel

from core.config import config


class Token(BaseModel):
    """JWT token model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data stored in JWT token."""
    username: Optional[str] = None


class UserCreate(BaseModel):
    """User registration model."""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str


class WeChatLogin(BaseModel):
    """WeChat login model."""
    code: str


class UserInDB(BaseModel):
    """User model as stored in database."""
    id: int
    username: str
    email: str
    hashed_password: str
    wechat_openid: Optional[str] = None
    is_active: bool


# JWT configuration
SECRET_KEY = config.app_api_key or "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt