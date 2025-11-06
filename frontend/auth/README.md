# OpenBB Authentication Frontend

This is a React/TypeScript frontend application for user authentication with the OpenBB Workspace backend.

## Features

- User registration
- Username/password login
- JWT token generation and display
- Copy token to clipboard for use with OpenBB Workspace
- Dark/light mode support

## Development

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000.

### Building for Production

```bash
npm run build
```

## Usage

1. Register a new account or login with existing credentials
2. After successful authentication, your JWT token will be displayed
3. Copy the token and use it with your OpenBB Workspace backend

## API Integration

The frontend communicates with the backend API at `/api` (proxied to `http://localhost:8000` during development).

Authentication endpoints:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/token` - OAuth2 token endpoint
- `GET /api/auth/me` - Get current user information

## Technologies Used

- React 18 with TypeScript
- Vite build tool
- Tailwind CSS for styling
- Radix UI components