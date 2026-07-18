import { cpSync, createReadStream, existsSync, mkdirSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { defineConfig, type Plugin, type ViteDevServer } from 'vite'
import vue from '@vitejs/plugin-vue'

const projectRoot = fileURLToPath(new URL('.', import.meta.url))
const localPaperDirs = [
  fileURLToPath(new URL('./content/raw/ai-agent-interview/papers/', import.meta.url)),
  fileURLToPath(new URL('./content/raw/active-learning/papers/', import.meta.url)),
]

function localPaperAssets(): Plugin {
  return {
    name: 'local-paper-assets',
    configureServer(server: ViteDevServer) {
      server.middlewares.use('/papers', (request, response, next) => {
        const fileName = decodeURIComponent(request.url ?? '').replace(/^\/+/, '')
        if (!/^(?:\d+\.\d+|cs\.\d+|settles-2009)\.pdf$/.test(fileName)) {
          next()
          return
        }
        const filePath = localPaperDirs
          .map((directory) => `${directory}/${fileName}`)
          .find((candidate) => existsSync(candidate))
        if (!filePath) {
          next()
          return
        }
        response.setHeader('Content-Type', 'application/pdf')
        createReadStream(filePath).pipe(response)
      })
    },
    closeBundle() {
      const outputDir = `${projectRoot}/dist/papers`
      mkdirSync(outputDir, { recursive: true })
      for (const directory of localPaperDirs) {
        for (const fileName of readdirSync(directory).filter((file) => file.endsWith('.pdf'))) {
          cpSync(`${directory}/${fileName}`, `${outputDir}/${fileName}`)
        }
      }
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), localPaperAssets()],
  server: {
    proxy: {
      '/lm-studio': {
        target: 'http://127.0.0.1:1234',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/lm-studio/, ''),
      },
    },
  },
})
