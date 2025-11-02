# OpenBB HKA Frontend

This is a monorepo containing the frontend applications for OpenBB HKA:

1. Web Application (Next.js)
2. WeChat Mini Program (Taro)

## Project Structure

```
frontend/
├── web/                 # Next.js web application
└── miniapp/            # Taro WeChat Mini Program
```

## Features

- User Registration
- Login Methods:
  - Username/Password
  - WeChat Login
- JWT Token Management
- Token Display Page

## Prerequisites

- Node.js 18+
- pnpm (for package management)
- WeChat DevTools (for Mini Program development)

## Development

### Web Application

```bash
# Install dependencies
cd web
npm install

# Start development server
npm run dev
```

### WeChat Mini Program

```bash
# Install dependencies
cd miniapp
pnpm install

# Start development
pnpm dev:weapp
```

## Building for Production

### Web Application

```bash
cd web
npm run build
```

### WeChat Mini Program

```bash
cd miniapp
pnpm build:weapp
```

## Environment Variables

### Web Application (.env.local)

```
NEXT_PUBLIC_API_URL=http://your-api-url
NEXT_PUBLIC_WECHAT_APP_ID=your-wechat-app-id
```

### WeChat Mini Program (project.config.json)

Configure your WeChat Mini Program settings in `miniapp/project.config.json`.