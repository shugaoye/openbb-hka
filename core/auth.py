from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.config import config
from core.database import db, verify_password
from core.auth_models import TokenData
import jwt
from jwt import PyJWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_api_key(token: str, api_key: str) -> bool:
    """Validate API key in header against pre-defined list of keys."""
    if not token:
        return False
    if token.replace("Bearer ", "").strip() == api_key:
        return True
    return False

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not validate_api_key(token=token, api_key=config.app_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

# New authentication functions
def authenticate_user(username: str, password: str):
    """Authenticate a user with username and password."""
    user = db.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user_from_token(token: str):
    """Get user from JWT token."""
    try:
        payload = jwt.decode(token, config.app_api_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except PyJWTError:
        return None
    user = db.get_user_by_username(username=token_data.username or "")
    return user