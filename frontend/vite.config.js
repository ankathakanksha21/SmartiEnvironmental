import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    // Forward API calls to FastAPI. The browser sees one address,
    // so the backend needs no cross-origin (CORS) setup.
    proxy: { '/api': 'http://127.0.0.1:8000' },
  },
})
