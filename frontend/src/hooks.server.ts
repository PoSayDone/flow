import { accessTokenMaxAge, api_url, refreshTokenMaxAge } from '$lib/utils';
import { type HandleFetch } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
	const { cookies } = event;
	const accessToken = cookies.get('access_token')?.toString();
	const refreshToken = cookies.get('refresh_token')?.toString();

	const needsRefresh = !accessToken && refreshToken;

	if (needsRefresh) {
		const requestOptions = {
			method: 'POST',
			headers: {
				cookie: `refresh_token=${refreshToken}`
			}
		};

		const response = await fetch(`${api_url}/auth/refresh`, requestOptions);

		if (response.status == 200) {
			const data = await response.json();
			cookies.set('access_token', decodeURIComponent(`Bearer ${data.access_token}`), {
				path: '/',
				maxAge: accessTokenMaxAge
			});
			cookies.set('refresh_token', decodeURIComponent(`Bearer ${data.refresh_token}`), {
				path: '/',
				maxAge: refreshTokenMaxAge
			});
			event.locals.isAuthenticated = true;
		} else {
			throw redirect(302, '/auth/');
		}
	}

	request.headers.set('cookie', `access_token=${cookies.get('access_token')?.toString()}`);
	const response = await fetch(request);
	return response;
};
