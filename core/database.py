"""Database models and utilities for user management."""

import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import os
from openbb_core.app.utils import get_user_cache_directory
from core.config import config
from pydantic import BaseModel


class User(BaseModel):
    """User model for authentication."""
    id: Optional[int] = None
    username: str
    email: str
    hashed_password: str
    wechat_openid: Optional[str] = None
    is_active: bool = True
    created_at: datetime = datetime.utcnow()


class Database:
    """Simple SQLite database wrapper for user management."""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = f"{get_user_cache_directory()}/{config.data_folder_path}/{db_path}"
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                wechat_openid TEXT UNIQUE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if wechat_openid column exists, add it if not
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'wechat_openid' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN wechat_openid TEXT UNIQUE")
        
        conn.commit()
        conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, email, hashed_password, wechat_openid, is_active, created_at FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                hashed_password=row[3],
                wechat_openid=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if isinstance(row[6], str) else row[6]
            )
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, email, hashed_password, wechat_openid, is_active, created_at FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                hashed_password=row[3],
                wechat_openid=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if isinstance(row[6], str) else row[6]
            )
        return None
    
    def get_user_by_wechat_openid(self, openid: str) -> Optional[User]:
        """Retrieve a user by WeChat OpenID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, email, hashed_password, wechat_openid, is_active, created_at FROM users WHERE wechat_openid = ?",
            (openid,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                hashed_password=row[3],
                wechat_openid=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if isinstance(row[6], str) else row[6]
            )
        return None
    
    def create_user(self, user: User) -> User:
        """Create a new user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, wechat_openid, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user.username, user.email, user.hashed_password, user.wechat_openid, user.is_active, user.created_at)
        )
        
        user.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user
    
    def update_user_wechat_openid(self, user_id: int, openid: str) -> bool:
        """Update a user's WeChat OpenID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE users SET wechat_openid = ? WHERE id = ?",
            (openid, user_id)
        )
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success


# Utility functions
def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return hash_password(plain_password) == hashed_password


# Global database instance
db = Database()