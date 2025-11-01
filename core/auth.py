from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.config import config
from core.security import decode_token

# OAuth2PasswordBearer expects a token URL; for our API-key/JWT mixed usage, we keep it simple
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def validate_api_key(token: str, api_key: str) -> bool:
    """Validate API key in header against configured APP_API_KEY."""
    if not token:
        return False
    if token.replace("Bearer ", "").strip() == api_key:
        return True
    return False

async def get_current_user_api_key(token: str = Depends(oauth2_scheme)):
    if not validate_api_key(token=token, api_key=config.app_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

async def get_current_user_jwt(token: str = Depends(oauth2_scheme)):
    raw = token.replace("Bearer ", "").strip()
    try:
        payload = decode_token(raw)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired JWT",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency that accepts either API key or valid JWT."""
    if validate_api_key(token=token, api_key=config.app_api_key):
        return {"type": "api_key"}
    raw = token.replace("Bearer ", "").strip()
    try:
        payload = decode_token(raw)
        return {"type": "jwt", "claims": payload}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
