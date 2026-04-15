import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:2026',
        changeOrigin: true
      },
      '/static': {
        target: 'http://localhost:2026',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: resolve(__dirname, '../static'),
    emptyOutDir: true,
    assetsDir: 'assets',
    manifest: true
  }
})
