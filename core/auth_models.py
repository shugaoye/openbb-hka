from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserInDB(UserBase):
    """User model as stored in database."""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class User(UserBase):
    """User model returned to client."""
    id: int
    created_at: datetime


class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    exp: Optional[datetime] = None


class WechatUser(BaseModel):
    """WeChat user information."""
    openid: str
    session_key: str
    unionid: Optional[str] = None


class WechatLoginRequest(BaseModel):
    """WeChat login request data."""
    code: str