// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import ViteFonts from 'unplugin-fonts/vite'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/styles/settings.scss',
      },
    }),
    ViteFonts({
      google: {
        families: [{
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    watch: {
      usePolling: true,
    },
    port: 3000,
  },
  build: {
    rollupOptions: {
      output: {
        // TODO: We would usually like to use assets/ here, but we first have to fix this disraptor problem: https://github.com/disraptor/disraptor/issues/33
        assetFileNames: 'assets-public/[name].[ext]',
        chunkFileNames: 'chunks/[name].js',
        entryFileNames: 'entries/[name].js',
      },
    },
    outDir: '/dist',
  },
  experimental: {
    renderBuiltUrl(filename: string, { hostType }: { hostType: 'js' | 'css' | 'html' }) {
      // TIRA expects resourecs/assets at this location
      return '/static/' + filename
    }
  }
})
