from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.config import config
from core.auth_utils import verify_token
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth_utils import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def validate_api_key(token: str, api_key: str) -> bool:
    """Validate API key in header against pre-defined list of keys."""
    if not token:
        return False
    # 移除Bearer前缀并去除空白字符
    clean_token = token.replace("Bearer ", "").strip()
    # 检查是否是API密钥
    if clean_token == api_key:
        return True
    return False

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 首先尝试使用API密钥验证
    if validate_api_key(token=token, api_key=config.app_api_key):
        return {"type": "api_key", "value": token}
    
    # 然后尝试使用JWT令牌验证
    token_data = verify_token(token.replace("Bearer ", "").strip())
    if token_data and token_data.username:
        user = get_user_by_username(db, token_data.username)
        if user:
            return {"type": "jwt", "user": user}
    
    # 如果都验证失败，抛出异常
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
