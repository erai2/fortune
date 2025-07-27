
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    proxy: {
      '/extract_rules': 'http://localhost:8000',
      '/rules': 'http://localhost:8000'
    }
  }
})
