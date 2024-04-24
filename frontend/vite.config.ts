import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';

export default defineConfig({
	server: {
		host: true,
		hmr: {
			port: 3001
		},
		watch: {
			usePolling: true
		}
	},
	plugins: [sveltekit(), SvelteKitPWA()]
});
