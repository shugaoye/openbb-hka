from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import config
from core.auth_models import UserInDB, TokenData, User, WechatUser
import httpx

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock database - Replace with actual database in production
fake_users_db = {}


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def validate_api_key(token: str, api_key: str) -> bool:
    """Validate API key in header against pre-defined list of keys."""
    if not token:
        return False
    if token.replace("Bearer ", "").strip() == api_key:
        return True
    return False


def get_user(username: str) -> Optional[UserInDB]:
    """Get user from database."""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with username and password."""
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.jwt_secret_key, algorithm=config.jwt_algorithm
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.jwt_secret_key, algorithms=[config.jwt_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(
        id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
    )


async def get_wechat_session(code: str) -> WechatUser:
    """Get WeChat session information using code."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": config.wechat_app_id,
                "secret": config.wechat_app_secret,
                "js_code": code,
                "grant_type": "authorization_code",
            },
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get WeChat session",
            )
        data = response.json()
        if "errcode" in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"WeChat error: {data['errmsg']}",
            )
        return WechatUser(**data)
