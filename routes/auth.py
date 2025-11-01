from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import requests

from core.db import Base, engine, get_db
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from core.config import config
from pydantic import BaseModel

# Create tables at import (simple bootstrap)
Base.metadata.create_all(bind=engine)

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class WeChatLoginRequest(BaseModel):
    code: str


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=req.username,
        email=req.email,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(str(user.id), extra_claims={"username": user.username})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user.id), extra_claims={"username": user.username})
    return TokenResponse(access_token=token)


@router.post("/wechat/login", response_model=TokenResponse)
def wechat_login(req: WeChatLoginRequest, db: Session = Depends(get_db)):
    if not (config.wechat_appid and config.wechat_secret):
        raise HTTPException(status_code=400, detail="WeChat login not configured")

    # Exchange code for session via WeChat API
    params = {
        "appid": config.wechat_appid,
        "secret": config.wechat_secret,
        "js_code": req.code,
        "grant_type": "authorization_code",
    }
    r = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=params, timeout=10)
    data = r.json()
    if "errcode" in data and data["errcode"] != 0:
        raise HTTPException(status_code=400, detail=f"WeChat error: {data}")
    openid = data.get("openid")
    unionid = data.get("unionid")
    if not openid:
        raise HTTPException(status_code=400, detail="Missing openid from WeChat response")

    user = db.query(User).filter(User.wechat_openid == openid).first()
    if not user:
        # Create a new user bound to this openid
        user = User(
            username=f"wx_{openid[:8]}",
            password_hash=hash_password(openid),
            wechat_openid=openid,
            wechat_unionid=unionid,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(str(user.id), extra_claims={"username": user.username, "wx": True})
    return TokenResponse(access_token=token)


@router.get("/token", response_class=HTMLResponse)
def display_token(request: Request):
    # Expect Authorization: Bearer <token>
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    token = (auth or "").replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    # Simple page to copy token
    html = f"""
    <html>
      <head><title>JWT Token</title></head>
      <body style='font-family: sans-serif; padding: 24px;'>
        <h2>JWT Token</h2>
        <textarea rows='6' cols='80'>{token}</textarea>
        <p>Copy the token above and paste into OpenBB Workspace as APP_API_KEY.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
