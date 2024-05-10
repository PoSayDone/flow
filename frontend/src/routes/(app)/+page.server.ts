import type { Soulmate } from '$lib/types';
import { api_url } from '$lib/utils';
import { fail, superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { likeSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { Actions } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ fetch }) => {
	const { soulmates }: { soulmates: Soulmate[] } =
		(await (await fetch(`${api_url}/user/soulmates/3`)).json()) || [];
	const likeForm = await superValidate(zod(likeSchema));
	const shouldRefreshSoulmates = soulmates.length > 2;
	const result = { soulmates, shouldRefreshSoulmates, likeForm };
	return result;
};

export const actions = {
	default: async ({ request, fetch }) => {
		const likeForm = await superValidate(request, zod(likeSchema));
		if (!likeForm.valid) return fail(400, { likeForm });
		console.log(likeForm.data.like);
		if (likeForm.data.like) {
			await fetch(`${api_url}/user/like/${likeForm.data.user_id}`, {
				method: 'POST'
			});
		} else {
			await fetch(`${api_url}/user/dislike/${likeForm.data.user_id}`, {
				method: 'POST'
			});
		}
	}
} satisfies Actions;
