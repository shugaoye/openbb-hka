from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from core.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user
)
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, WECHAT_APP_ID
from core.models import UserCreate, UserLogin, Token, User, WeChatLogin
from core.database import UserDB, get_db
import httpx

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_superuser=db_user.is_superuser
    )

@auth_router.post("/token", response_model=Token)
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/wechat/login", response_model=Token)
async def wechat_login(wechat_data: WeChatLogin, db: Session = Depends(get_db)):
    """
    WeChat login endpoint.
    Requires exchanging the code for an access token with WeChat's servers.
    """
    # Check if WeChat configuration is available
    if not WECHAT_APP_ID or not WECHAT_APP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="WeChat configuration not available. Please contact administrator."
        )
    
    async with httpx.AsyncClient() as client:
        # Exchange code for access token and openid
        wechat_response = await client.get(
            f"https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": WECHAT_APP_ID,
                "secret": WECHAT_APP_SECRET,
                "js_code": wechat_data.code,
                "grant_type": "authorization_code"
            }
        )
        
    wechat_user_data = wechat_response.json()
    
    if "errcode" in wechat_user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"WeChat login error: {wechat_user_data.get('errmsg')}"
        )
    
    openid = wechat_user_data.get("openid")
    session_key = wechat_user_data.get("session_key")
    
    if not openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get openid from WeChat"
        )
    
    # Check if user exists, if not, create a new user
    db_user = db.query(UserDB).filter(UserDB.username == f"wechat_{openid}").first()
    if not db_user:
        # Create a new user for WeChat login
        # Using session_key for password hashing if available, otherwise using openid
        password_base = session_key if session_key else openid
        db_user = UserDB(
            username=f"wechat_{openid}",
            email=None,
            hashed_password=get_password_hash(password_base)  # Using session_key or openid as base for password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    # Generate JWT token for our application
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return User(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser
    )

@auth_router.get("/token-display", response_class=HTMLResponse)
def display_token(current_user: User = Depends(get_current_active_user)):
    """
    Display JWT token in a simple HTML page that users can copy
    """
    from core.auth import create_access_token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your Access Token</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }}
            .token-container {{
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 20px;
                margin: 20px 0;
                word-break: break-all;
                font-family: monospace;
            }}
            .copy-button {{
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }}
            .copy-button:hover {{
                background-color: #0056b3;
            }}
            .instructions {{
                text-align: left;
                margin: 20px 0;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <h1>Your Access Token</h1>
        <p>Copy this token and use it with OpenBB Workspace:</p>
        
        <div class="token-container">
            {access_token}
        </div>
        
        <button class="copy-button" onclick="copyToken()">Copy Token</button>
        
        <div class="instructions">
            <h2>How to use this token with OpenBB Workspace:</h2>
            <ol>
                <li>Copy the token above</li>
                <li>In OpenBB Workspace, go to Settings > API Keys</li>
                <li>Add a new API key with the following details:
                    <ul>
                        <li>Name: FinApp Auth Token</li>
                        <li>Key: {access_token}</li>
                        <li>Provider: Custom</li>
                    </ul>
                </li>
                <li>Save and use this key to access protected endpoints</li>
            </ol>
        </div>
        
        <script>
            function copyToken() {{
                const token = "{access_token}";
                navigator.clipboard.writeText(token).then(() => {{
                    alert('Token copied to clipboard!');
                }}).catch(err => {{
                    console.error('Failed to copy token: ', err);
                }});
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
