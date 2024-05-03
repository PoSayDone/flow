import { redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { loginSchema } from '$lib/schema';
import { fail, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { accessTokenMaxAge, api_url, refreshTokenMaxAge } from '$lib/utils';

export const load: PageServerLoad = async () => {
	const loginForm = await superValidate(zod(loginSchema));
	return { loginForm };
};

export const actions = {
	default: async ({ request, cookies, fetch }) => {
		const loginForm = await superValidate(request, zod(loginSchema));
		if (!loginForm.valid) return fail(400, { loginForm });

		const urlParams = new URLSearchParams();
		urlParams.append('username', loginForm.data.mail);
		urlParams.append('password', loginForm.data.password);

		const requestOptions = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: urlParams
		};

		const response = await fetch(`${api_url}/auth/signin`, requestOptions);

		if (response.status == 200) {
			throw redirect(302, '/');
		} else {
			return setError(loginForm, 'Invalid email or password');
		}
	}
} satisfies Actions;