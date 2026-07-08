import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': 'https://didactic-potato-ppwpjx99x6x297xv-8000.app.github.dev/'   // forward API calls to FastAPI
    }
  }
})