import os

from dotenv import load_dotenv

from .models import AppConfig

load_dotenv()

config = AppConfig(
    agent_host_url=os.getenv("AGENT_HOST_URL", ""),
    app_api_key=os.getenv("APP_API_KEY", ""),
    data_folder_path=os.getenv("DATA_FOLDER_PATH", None),
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
    fmp_api_key=os.getenv("FMP_API_KEY", None),
    data_file=os.getenv("DATA_FILE_NAME", "yourdata.xlsx"),
    akshare_api_key=os.getenv("AKSHARE_API_KEY", None),
    jwt_secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production"),
    jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    jwt_access_token_expire_minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    wechat_app_id=os.getenv("WECHAT_APP_ID", ""),
    wechat_app_secret=os.getenv("WECHAT_APP_SECRET", ""),
)
