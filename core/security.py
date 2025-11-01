from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from passlib.context import CryptContext

from .config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: Optional[int] = None, extra_claims: Optional[dict] = None) -> str:
    to_encode = {"sub": subject, "iat": int(datetime.now(timezone.utc).timestamp())}
    if extra_claims:
        to_encode.update(extra_claims)
    expire_delta = expires_minutes if expires_minutes is not None else config.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.jwt_secret, algorithm=config.jwt_algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
