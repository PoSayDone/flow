// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type * as Icons from 'unplugin-icons/types/svelte';
export default Icons;

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			user_token: string | undefined;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
