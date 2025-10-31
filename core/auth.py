from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.config import config, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, WECHAT_APP_ID, WECHAT_APP_SECRET
from core.models import User, TokenData
from core.database import UserDB, get_db
import logging
from mysharelib.tools import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def verify_password(plain_password, hashed_password):
    truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8')
    return pwd_context.verify(truncated_password, hashed_password)

def get_password_hash(password):
    # Truncate password to 72 bytes if necessary
    truncated_password = password.encode('utf-8')[:72].decode('utf-8')    
    return pwd_context.hash(truncated_password)

def get_user(db: Session, username: str):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        # no token was provided by the client
        logger.warning("No token provided by the client")
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def validate_api_key(token: str, api_key: str) -> bool:
    """Validate API key in header against pre-defined list of keys."""
    if not token:
        return False
    if token.replace("Bearer ", "").strip() == api_key:
        return True
    return False

async def get_current_user_or_api_key(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    # First, try to authenticate with JWT token
    try:
        return await get_current_user(token, db)
    except HTTPException:
        # If JWT fails, check if it's a valid API key
        if validate_api_key(token=token, api_key=config.app_api_key):
            # Return a basic user object for API key users
            return User(
                id=0,
                username="api_key_user",
                is_active=True,
                is_superuser=False
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
