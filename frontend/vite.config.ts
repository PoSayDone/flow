import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';

export default defineConfig({
	server: {
		host: true,
		hmr: {
			port: 5001
		},
		watch: {
			usePolling: true
		}
	},
	plugins: [sveltekit(), SvelteKitPWA()]
});
