import os
import hashlib
import secrets
import aiosqlite
from typing import Optional


DB_PATH = os.getenv("OPENBB_USERS_DB", "./users.db")


async def init_db(db_path: str | None = None):
    path = db_path or DB_PATH
    async with aiosqlite.connect(path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
            """
        )
        await db.commit()


def _hash_password(password: str, salt: str) -> str:
    # PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return dk.hex()


async def create_user(username: str, password: str, db_path: str | None = None) -> bool:
    path = db_path or DB_PATH
    salt = secrets.token_hex(16)
    password_hash = _hash_password(password, salt)
    try:
        async with aiosqlite.connect(path) as db:
            await db.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )
            await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False


async def get_user(username: str, db_path: str | None = None) -> Optional[dict]:
    path = db_path or DB_PATH
    async with aiosqlite.connect(path) as db:
        cur = await db.execute("SELECT id, username, password_hash, salt FROM users WHERE username = ?", (username,))
        row = await cur.fetchone()
        await cur.close()
    if not row:
        return None
    return {"id": row[0], "username": row[1], "password_hash": row[2], "salt": row[3]}


async def authenticate_user(username: str, password: str, db_path: str | None = None) -> bool:
    user = await get_user(username, db_path=db_path)
    if not user:
        return False
    expected = _hash_password(password, user["salt"]) if isinstance(user, dict) else _hash_password(password, user[3])
    return expected == user["password_hash"]
