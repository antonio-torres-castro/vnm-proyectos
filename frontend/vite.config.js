import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        strictPort: true,
    },
    build: {
        sourcemap: true
    },
    css: {
        devSourcemap: true
    },
    define: {
        __DEV__: true
    },
    esbuild: {
        sourcemap: 'both',
        target: 'es2020'
    }
})