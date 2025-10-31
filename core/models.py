from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class AppConfig(BaseModel):
    """Application configuration loaded from environment variables."""

    title: str = Field(default="FinApp", description="The title of the app.")
    description: str = Field(
        default="FinApp API for OpenBB Workspace", description="The description of the app."
    )
    agent_host_url: str = Field(
        description="The host URL and port number where the app is running."
    )
    app_api_key: str = Field(description="The API key to access the bot.")
    openrouter_api_key: str = Field(
        description="OpenRouter API key for AI functionality."
    )
    fmp_api_key: str | None = Field(
        default=None, description="Financial Modeling Prep API key for data retrieval."
    )
    akshare_api_key: str | None = Field(
        default=None, description="AKShare API key for data retrieval."
    )

    @field_validator(
        "agent_host_url", "app_api_key", "openrouter_api_key", mode="before"
    )
    def validate_required_env_vars(cls, value: str | None, info) -> str | None:
        """Validate required environment variables.

        Raises ValueError if any required variable is not set.
        """
        if not value:
            raise ValueError(f"{info.field_name} environment variable is required.")
        return value

    @field_validator("fmp_api_key")
    def validate_fmp_api_key(cls, value: str | None) -> str | None:
        """Validate the Financial Modeling Prep API key.

        Must be set if FMP data retrieval is required.
        Raises ValueError if the key is not valid.
        """
        if value is None:
            raise ValueError("FMP API key must be set for data retrieval.")
        return value

    @field_validator("akshare_api_key")
    def validate_akshare_api_key(cls, value: str | None) -> str | None:
        """Validate the AKShare API key.

        Must be set if AKShare data retrieval is required.
        Raises ValueError if the key is not valid.
        """
        if value is None:
            raise ValueError("AKShare API key must be set for data retrieval.")
        return value


class User(BaseModel):
    """User model for authentication"""
    id: Optional[int] = None
    username: str
    email: Optional[str] = None
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = datetime.utcnow()


class UserCreate(BaseModel):
    """Model for user registration"""
    username: str
    password: str
    email: Optional[str] = None


class UserLogin(BaseModel):
    """Model for user login"""
    username: str
    password: str


class Token(BaseModel):
    """JWT Token model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: Optional[str] = None


class WeChatLogin(BaseModel):
    """Model for WeChat login"""
    code: str  # WeChat authorization code
