import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

// ESM-compatible __dirname (Vite config runs as ES module)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '');
  const backendHost = env.BACKEND_HOST || '127.0.0.1';
  const backendPort = env.BACKEND_PORT || env.API_BACKEND_PORT || '444';
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
            target: `http://${backendHost}:${backendPort}`,
            ws: true,
            changeOrigin: true,
          },
          '/api': {
            target: `http://${backendHost}:${backendPort}`,
            changeOrigin: true,
          },
        },
      },
      plugins: [
        react(),
        // ── Serve .github/agents/*.agent.md directly so the Doc tab works
        // ── even when the FastAPI backend (port 444) is not running.
        {
          name: 'vite-agent-docs',
          configureServer(server) {
            const VALID = new Set(['0master','10idea','1project','2think','3design','4plan','5test','6code','7exec','8ql','9git']);
            const agentsDir = path.resolve(__dirname, '../.github/agents');

            server.middlewares.use('/api/agent-doc', (req, res, next) => {
              const agentId = (req.url ?? '').replace(/^\//, '').split('?')[0];
              if (!VALID.has(agentId)) { next(); return; }
              const file = path.join(agentsDir, `${agentId}.agent.md`);

              if (req.method === 'GET') {
                res.setHeader('Content-Type', 'application/json');
                const content = fs.existsSync(file) ? fs.readFileSync(file, 'utf-8') : '';
                res.end(JSON.stringify({ content }));
                return;
              }

              if (req.method === 'PUT') {
                let body = '';
                req.on('data', (chunk: Buffer) => { body += chunk.toString(); });
                req.on('end', () => {
                  try {
                    const { content } = JSON.parse(body) as { content: string };
                    fs.mkdirSync(agentsDir, { recursive: true });
                    fs.writeFileSync(file, content, 'utf-8');
                    res.setHeader('Content-Type', 'application/json');
                    res.end(JSON.stringify({ status: 'ok' }));
                  } catch {
                    res.statusCode = 400;
                    res.end(JSON.stringify({ error: 'Invalid body' }));
                  }
                });
                return;
              }

              next();
            });
          },
        },
      ],
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
