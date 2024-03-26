import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();

		const formData = new URLSearchParams();
		formData.append('username', data.get('mail'));
		formData.append('password', data.get('password'));

		const requestOptions = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: formData
		};

		const response = await fetch(`http://nginx/api/auth/token`, requestOptions);

		if (response.status == 200) {
			const data = await response.json();
			cookies.set('access_token', decodeURIComponent(`Bearer ${data.access_token}`), { path: '/' });
			cookies.set('refresh_token', decodeURIComponent(`Bearer ${data.refresh_token}`), {
				path: '/'
			});
			throw redirect(302, '/');
		} else {
			return {
				message: 'invalid email or password'
			};
		}
	}
} satisfies Actions;
