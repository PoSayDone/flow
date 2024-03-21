import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';
import Icons from 'unplugin-icons/vite';
import IconsResolver from 'unplugin-icons/resolver';
import AutoImport from 'unplugin-auto-import/vite';
import { FileSystemIconLoader } from 'unplugin-icons/loaders';

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
	plugins: [
		sveltekit(),
		SvelteKitPWA(),
		Icons({
			compiler: 'solid',
			customCollections: {
				flow: FileSystemIconLoader('./static/icons')
			}
		}),
		AutoImport({
			dts: true,
			resolvers: [
				IconsResolver({
					prefix: 'icon',
					extension: 'solid',
					customCollections: ['flow'],
					enabledCollections: ['flow']
				})
			]
		})
	]
});
