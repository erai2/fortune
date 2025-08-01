import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3000

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: PORT,
    allowedHosts: 'all',
    proxy: {
      '/extract_rules': 'http://localhost:8000',
      '/rules': 'http://localhost:8000'
    }
  }
})
