# OpenBB WeChat Mini Program

This is the WeChat Mini Program frontend for the OpenBB authentication system. It provides user registration, login (including WeChat login), and token management functionality.

## Features

- User registration with username/email and password
- Standard username/password login
- WeChat login (using WeChat's built-in authentication)
- JWT token display and copy functionality
- Secure token storage and management

## Setup

1. Install the WeChat Developer Tools from the official WeChat website
2. Open the WeChat Developer Tools
3. Create a new mini program project
4. Set the project directory to this folder (`mini-program`)
5. Use a test app ID during development

## Configuration

Before deploying to production, update the API endpoints in `app.js` to point to your backend server:

```javascript
const API_BASE_URL = 'https://your-backend-domain.com'; // Update this
```

For WeChat login to work properly, make sure your mini program is registered with the correct app ID in the WeChat platform, and your backend has the corresponding app secret configured.

## Structure

- `app.js` - Main application logic and global functions
- `app.json` - Global configuration
- `pages/` - Contains all pages
  - `index/` - Main landing page
  - `login/` - Login page
  - `register/` - Registration page
  - `dashboard/` - Token display page after login

## Deployment

To deploy this mini program:

1. Update the API endpoints in `app.js` to your production backend URL
2. Make sure your backend server allows requests from your mini program
3. Upload the code through the WeChat Developer Tools
4. Submit for review in the WeChat Mini Program platform