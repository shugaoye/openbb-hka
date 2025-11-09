# OpenBB Auth Frontend

This is a minimal React + Vite frontend for authentication (register + token issuance) intended to work with the OpenBB Workspace backend.

Quick start

1. cd frontend/auth
2. npm install
3. npm run dev

The app will run on the Vite server (default port 1422 as configured) and calls the backend endpoints under `/auth` (register and token).

Notes

- This is intentionally minimal. For production you should set a secure `JWT_SECRET` on the backend and run the frontend build.
- The UI uses Tailwind for styling. Run `npm run build` to produce a production bundle.
