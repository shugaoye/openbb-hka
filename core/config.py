import os

from dotenv import load_dotenv

from .models import AppConfig

load_dotenv()

config = AppConfig(
    agent_host_url=os.getenv("AGENT_HOST_URL", ""),
    app_api_key=os.getenv("APP_API_KEY", ""),
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
    fmp_api_key=os.getenv("FMP_API_KEY", None),
    akshare_api_key=os.getenv("AKSHARE_API_KEY", None),
    jwt_secret=os.getenv("JWT_SECRET", ""),
    jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")),
    database_url=os.getenv("DATABASE_URL", "sqlite:///./auth.db"),
    wechat_appid=os.getenv("WECHAT_APPID", None),
    wechat_secret=os.getenv("WECHAT_SECRET", None),
)
