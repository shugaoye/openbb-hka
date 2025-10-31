# OpenBB Authentication System Documentation

## Overview

This document describes the complete authentication system for the OpenBB Workspace backend. The system includes both a React-based web frontend and a WeChat Mini Program frontend, with a Python/FastAPI backend that supports both username/password authentication and WeChat login.

## System Architecture

The authentication system consists of:

1. **Backend**: Python/FastAPI with JWT token authentication
2. **Web Frontend**: React application with Bootstrap UI
3. **Mobile Frontend**: WeChat Mini Program
4. **Database**: SQLAlchemy with SQLite (can be configured for other databases)

## Backend Features

### Endpoints

- `POST /auth/register` - User registration with username, email, and password
- `POST /auth/token` - User login to obtain JWT token
- `POST /auth/wechat/login` - WeChat login using code from WeChat OAuth
- `GET /auth/me` - Get current user information
- `GET /auth/token-display` - Display JWT token for copying (HTML page)

### Authentication Methods

1. **Username/Password Authentication**:
   - Secure password hashing using bcrypt
   - JWT token generation with configurable expiration
   - User session management

2. **WeChat Authentication**:
   - OAuth 2.0 integration with WeChat
   - Automatic user creation for new WeChat users
   - Session key validation

## Frontend Applications

### Web Frontend (React)

#### Features
- User registration form
- Username/password login
- WeChat QR code login for web browsers
- WeChat app login for in-app users
- Token display and copy functionality
- Responsive design with Bootstrap

#### Setup
1. Navigate to the `frontend` directory
2. Install dependencies: `npm install`
3. Create a `.env` file with:
   ```
   REACT_APP_API_URL=https://your-backend-domain.com
   REACT_APP_WECHAT_APP_ID=your_wechat_app_id  # Optional, for web OAuth
   ```
4. Start development server: `npm start`

#### Configuration
- Update `REACT_APP_API_URL` to point to your backend server
- If using WeChat OAuth for web, set `REACT_APP_WECHAT_APP_ID`

### WeChat Mini Program

#### Features
- User registration form optimized for mobile
- Username/password login
- Direct WeChat login using built-in WeChat authentication
- Token display and copy functionality
- Native WeChat UI components

#### Setup
1. Install WeChat Developer Tools
2. Create a new project using the `mini-program` directory
3. Use your test app ID during development
4. Update the backend URLs in `app.js` before production

#### Configuration
- Update the API URLs in `app.js` to your actual backend server
- Register your mini program with WeChat with the correct domain permissions
- Configure your backend to accept requests from your mini program

## Backend Configuration

### Environment Variables

Create a `.env` file in the backend root directory:

```
# JWT Configuration
SECRET_KEY=your-very-secure-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# WeChat Configuration
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# Database Configuration
DATABASE_URL=sqlite:///./users.db
# Or for PostgreSQL: postgresql://user:password@localhost/dbname

# Application Configuration
AGENT_HOST_URL=your-agent-host-url
APP_API_KEY=your-app-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
FMP_API_KEY=your-fmp-api-key
AKSHARE_API_KEY=your-akshare-api-key
```

### Dependencies

The backend requires the following additional dependencies for authentication:
- fastapi
- python-jose[cryptography]
- passlib[bcrypt]
- sqlalchemy
- python-dotenv
- httpx
- wechatpy (for WeChat integration)

## Security Considerations

### JWT Tokens
- Use a strong, unique SECRET_KEY in production
- Set appropriate token expiration time (ACCESS_TOKEN_EXPIRE_MINUTES)
- Tokens are stored securely in the frontend (localStorage for web, storage for mini program)

### Password Security
- Passwords are hashed using bcrypt with salt
- No plain text passwords are stored in the database

### WeChat Integration
- App secret is loaded from environment variables
- OAuth code exchange happens server-side only
- State parameter is used for web OAuth to prevent CSRF

### API Protection
- All protected endpoints require valid JWT token
- Database access is properly scoped per user
- Input validation is implemented for all endpoints

## OpenBB Workspace Integration

### Using the Token
1. User logs in through either web or mini program frontend
2. JWT token is displayed on the dashboard
3. User copies the token
4. In OpenBB Workspace, user adds the token as an API key
5. OpenBB Workspace uses the token to authenticate requests to protected endpoints

### Protecting Endpoints
The backend includes utilities to protect endpoints with JWT authentication:

```python
from core.auth import get_current_active_user

@app.get("/protected-endpoint")
def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.username}"}
```

## Deployment

### Backend Deployment
1. Configure environment variables with production values
2. Set up proper database (not SQLite for production)
3. Use a WSGI server like Gunicorn in production
4. Set up HTTPS with a reverse proxy like Nginx

### Frontend Deployment
1. Build the React app: `npm run build`
2. Serve the build directory with a web server
3. For WeChat Mini Program, upload through WeChat Developer Tools

## Troubleshooting

### Common Issues

1. **WeChat Login Fails**: Check that WECHAT_APP_ID and WECHAT_APP_SECRET are correctly set
2. **Token Not Working**: Verify the token is correctly copied and used in OpenBB Workspace
3. **CORS Issues**: Ensure your backend allows requests from your frontend domains
4. **Database Connection**: Check DATABASE_URL configuration

### Debugging Tips

1. Enable logging in the backend for authentication requests
2. Check browser developer tools for frontend errors
3. Verify all environment variables are loaded correctly

## Development

### Running Locally

Backend:
```bash
uvicorn main:app --reload
```

Frontend (development):
```bash
cd frontend
npm start
```

### Testing

The system includes various authentication flows that should be tested:
- User registration and login
- Password hashing and verification
- JWT token generation and validation
- WeChat OAuth flow (web and mini program)
- Token display and copying

## Future Enhancements

- Two-factor authentication
- Password reset functionality
- Social login with other providers
- Admin panel for user management
- Rate limiting for authentication endpoints
- User profile management
- Refresh token support for longer sessions