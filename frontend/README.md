# OpenBB Authentication Frontend

This is the React-based frontend for the OpenBB authentication system. It provides user registration, login (including WeChat login), and token management functionality.

## Features

- User registration with username/email and password
- Standard username/password login
- WeChat login (both in WeChat browser and via OAuth QR code)
- JWT token display and copy functionality
- Secure token storage and management

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file in the frontend directory with the following:
```
REACT_APP_API_URL=http://localhost:8000
```

3. Start the development server:
```bash
npm start
```

## Configuration

The frontend needs to be configured to connect to your backend API. Update the `REACT_APP_API_URL` environment variable to point to your backend server.

For WeChat login to work properly, make sure your backend has the correct WeChat app ID and secret configured in the environment variables.

## Building for Production

To create a production build:
```bash
npm run build
```

The build artifacts will be placed in the `build/` directory and can be served by any static file server.