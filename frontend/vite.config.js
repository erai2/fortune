import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 5173
const BACKEND_URL = process.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: PORT,
    allowedHosts: 'all',
    proxy: {
      '/extract_rules': BACKEND_URL,
      '/rules': BACKEND_URL
    }
  }
})
