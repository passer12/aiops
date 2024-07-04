import { fileURLToPath, URL } from 'node:url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig(() => {
    return {
        plugins: [vue()],
        resolve: {
            alias: {
                '@': fileURLToPath(new URL('./src', import.meta.url))
            }
        },
        server: {
            port: 5173,
            proxy: {
                '/api': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true
                },
                '/media': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true
                }
            }
        }

        // server: {
        //     port: 5173,
        //     proxy: {
        //         '/api': {
        //             target: 'http://127.0.0.1:8000',
        //             changeOrigin: true
        //         }
        //     }
        // }
    };
});
