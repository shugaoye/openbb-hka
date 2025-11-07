from pydantic import BaseModel, Field, field_validator


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
    data_folder_path: str | None = Field(
        description="The path to the folder that will store the transaction data."
    )
    data_file: str = Field(
        default="yourdata.xlsx", description="Path to your data file."
    )
    fmp_api_key: str | None = Field(
        default=None, description="Financial Modeling Prep API key for data retrieval."
    )
    akshare_api_key: str | None = Field(
        default=None, description="AKShare API key for data retrieval."
    )
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production", description="Secret key for JWT token generation."
    )
    jwt_algorithm: str = Field(
        default="HS256", description="Algorithm used for JWT token generation."
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30, description="Expiration time for access tokens in minutes."
    )
    wechat_app_id: str = Field(
        default="", description="WeChat App ID for WeChat login."
    )
    wechat_app_secret: str = Field(
        default="", description="WeChat App Secret for WeChat login."
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
