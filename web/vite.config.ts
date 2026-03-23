import path from 'path';
import { fileURLToPath } from 'url';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// ESM-compatible __dirname (Vite config runs as ES module)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '');
    return {
      define: {
        // This is just generic value for the GEMINI API key.
        // This is not used at all, and can be ignored!
        'process.env.API_KEY' : JSON.stringify('api-key-this-is-not-used-can-be-ignored!'),
      },
      server: {
        host: env.HOST || '0.0.0.0',
        port: parseInt(env.VITE_PORT || '44'),
        proxy: {
          '/ws': {
            target: `http://${env.HOST || '0.0.0.0'}:${env.BACKEND_PORT || '444'}`,
            ws: true,
            changeOrigin: true,
          },
          '/api': {
            target: `http://${env.HOST || '0.0.0.0'}:${env.BACKEND_PORT || '444'}`,
            changeOrigin: true,
          },
        },
      },
      plugins: [react()],
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      },
      test: {
        environment: 'jsdom',
        globals: true,
      },
    };
});
