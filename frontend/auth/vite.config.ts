import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 1422,
    proxy: {
      // proxy /auth requests to backend
      '/auth': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
        secure: false,
      },
      // add other endpoints as needed, e.g. /api, /udf, etc.
    },
  },
})
