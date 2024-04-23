import { api_url } from '$lib/utils';
import { redirect, type HandleFetch } from '@sveltejs/kit';

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
	const { cookies } = event;
	const accessToken = event.cookies.get('access_token')?.toString();
	const refreshToken = event.cookies.get('refresh_token')?.toString();

	if (accessToken && refreshToken) {
		event.locals.isAuthenticated = true;
	} else {
		event.locals.isAuthenticated = false;
	}

	if (!event.url.pathname.startsWith('/auth')) {
		if (!event.locals.isAuthenticated) {
			throw redirect(303, '/auth');
		}
	}

	request.headers.set('cookie', `access_token=${accessToken}`);
	let response = await fetch(request);

	if (response.status == 401 && refreshToken) {
		const refresh_response = await fetch(`${api_url}/auth/refresh/`, {
			method: 'POST',
			headers: {
				cookie: `refresh_token=${refreshToken}`
			}
		});

		const data = await refresh_response.json();
		if (data.access_token && data.refresh_token) {
			cookies.set('access_token', `Bearer ${data.access_token}`, { path: '/', httpOnly: true });
			cookies.set('refresh_token', `Bearer ${data.refresh_token}`, { path: '/', httpOnly: true });
		}

		const accessToken = event.cookies.get('access_token');
		request.headers.set('cookie', `access_token=${accessToken}`);
		response = await fetch(request);

		if (response.status === 401 && refreshToken && accessToken) {
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			event.locals.isAuthenticated = false;
		}
	}

	return response;
};
