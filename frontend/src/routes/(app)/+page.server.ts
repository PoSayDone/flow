import type { Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Soulmate } from '$lib/types';
import { api_url } from '$lib/utils';

export const load: PageServerLoad = async ({ fetch }) => {
	const { soulmates }: { soulmates: Soulmate[] } = await (
		await fetch(`${api_url}/user/soulmates/10`)
	).json();
	const body = { soulmates };
	return body;
};

export const actions = {
	like_user: async () => {}
} satisfies Actions;
