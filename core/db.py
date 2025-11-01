from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import config

engine = create_engine(
    config.database_url,
    connect_args={"check_same_thread": False} if config.database_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
