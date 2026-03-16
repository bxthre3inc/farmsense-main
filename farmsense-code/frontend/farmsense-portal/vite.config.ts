import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: [
      '.farmsense.io',
      'api.farmsense.io',
      'oracle.farmsense.io',
      'localhost',
      '.zocomputer.io',
      'farmsense-portal-brodiblanco.zocomputer.io',
      'farmsense-frontend-brodiblanco.zocomputer.io'
    ]
  }
})
