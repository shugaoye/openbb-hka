from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user model with common fields."""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: Optional[EmailStr] = Field(None, description="Email address")
    

class UserCreate(UserBase):
    """Model for user creation."""
    password: str = Field(..., min_length=6, description="Password")
    

class UserLogin(BaseModel):
    """Model for user login."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    

class User(UserBase):
    """Model for user response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        

class Token(BaseModel):
    """Model for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    

class TokenData(BaseModel):
    """Model for JWT token data."""
    username: Optional[str] = None
    

class WeChatLogin(BaseModel):
    """Model for WeChat login request."""
    code: str = Field(..., description="WeChat authorization code")