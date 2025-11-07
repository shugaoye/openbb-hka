from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
import requests
from sqlalchemy.orm import Session
from .config import config
from .database import UserDB
from .user_models import TokenData

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配。"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码的哈希值。"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌。"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.jwt_secret_key, algorithm=config.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """验证令牌并返回令牌数据。"""
    try:
        payload = jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return TokenData(username=username)
    except JWTError:
        return None


def get_user_by_username(db: Session, username: str) -> Optional[UserDB]:
    """通过用户名获取用户。"""
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    """通过邮箱获取用户。"""
    return db.query(UserDB).filter(UserDB.email == email).first()


def get_user_by_wechat_openid(db: Session, openid: str) -> Optional[UserDB]:
    """通过微信openid获取用户。"""
    return db.query(UserDB).filter(UserDB.wechat_openid == openid).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserDB]:
    """验证用户凭据。"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def handle_wechat_login(db: Session, code: str) -> Union[UserDB, None]:
    """处理微信登录。"""
    # 如果没有配置微信App ID和App Secret，则返回None
    if not config.wechat_app_id or not config.wechat_app_secret:
        return None
    
    # 构建请求URL
    url = f"https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": config.wechat_app_id,
        "secret": config.wechat_app_secret,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    
    # 发送请求
    response = requests.get(url, params=params)
    data = response.json()
    
    # 检查是否成功获取openid
    if "openid" not in data:
        return None
    
    openid = data["openid"]
    
    # 查找用户是否已存在
    user = get_user_by_wechat_openid(db, openid)
    
    # 如果用户不存在，则创建新用户
    if not user:
        # 使用openid的前8位作为用户名
        username = f"wechat_{openid[:8]}"
        
        # 生成一个随机密码
        import secrets
        random_password = secrets.token_urlsafe(16)
        
        # 创建新用户
        user = UserDB(
            username=username,
            hashed_password=get_password_hash(random_password),
            wechat_openid=openid
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user