import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        host: '0.0.0.0',
        port: 3000,
        strictPort: true, // Fuerza el puerto 3000
    },
    build: {
        sourcemap: true
    },
    css: {
        devSourcemap: true
    },
    // Optimización para debugging
    esbuild: {
        sourcemap: 'both' // Generar source maps inline y externos
    }
})