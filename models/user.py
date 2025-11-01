from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(128), unique=False, index=True, nullable=True)
    phone = Column(String(32), unique=False, nullable=True)
    password_hash = Column(String(255), nullable=False)
    wechat_openid = Column(String(128), unique=True, nullable=True)
    wechat_unionid = Column(String(128), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
