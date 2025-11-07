from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from openbb_core.app.utils import get_user_cache_directory
from core.config import config

# 创建数据库引擎
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{get_user_cache_directory()}/{config.data_folder_path}/users.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


# 定义用户表模型
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    wechat_openid = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 初始化数据库
def init_db():
    Base.metadata.create_all(bind=engine)