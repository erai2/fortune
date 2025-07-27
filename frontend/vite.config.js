import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 5000; // Use environment port or fallback to 5000

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Set host for external access
    port: PORT,
    allowedHosts: 'all',
    proxy: {
      '/extract_rules': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/rules': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
});