import {
    defineConfig
} from 'vite'

export default defineConfig({
    root: '.',
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
        sourcemap: true,
        rollupOptions: {
            input: {
                main: 'index.html'
            }
        }
    },
    server: {
        port: 3000,
        open: true,
        host: true,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            },
            '/health': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                secure: false
            }
        }
    },
    optimizeDeps: {
        include: ['chess.js']
    },
    define: {
        global: 'globalThis'
    }
})