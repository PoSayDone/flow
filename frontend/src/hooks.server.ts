import { accessTokenMaxAge, api_url, refreshTokenMaxAge } from '$lib/utils';
import { type HandleFetch } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

let refreshingPromise: Promise<void> | undefined = undefined;

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
	if (refreshingPromise) {
		await refreshingPromise;
	}
	const { cookies } = event;
	const accessToken = cookies.get('access_token')?.toString();
	const refreshToken = cookies.get('refresh_token')?.toString();

	if (refreshToken) {
		event.locals.isAuthenticated = true;
	}

	if (!event.url.pathname.includes('/auth')) {
		if (!event.locals.isAuthenticated) {
			throw redirect(303, '/auth');
		}

		const needsRefresh = !accessToken && refreshToken;

		if (needsRefresh) {
			refreshingPromise = new Promise<void>((resolve, reject) => {
				const requestOptions = {
					method: 'POST',
					headers: {
						cookie: `refresh_token=${refreshToken}`
					}
				};

				fetch(`${api_url}/auth/refresh`, requestOptions).then(async (response) => {
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
						resolve();
					} else {
						reject();
					}
				});
			}).then(
				//result
				() => {},
				//error
				() => {
					event.locals.isAuthenticated = false;
					cookies.delete('access_token', { path: '/' });
					cookies.delete('refresh_token', { path: '/' });
					throw redirect(303, '/auth');
				}
			);
			await refreshingPromise;
			refreshingPromise = undefined;
		}
	}
	request.headers.set('cookie', `access_token=${cookies.get('access_token')?.toString()}`);
	const response = await fetch(request);

	if (!event.url.pathname.includes('/auth')) {
		if (response.status == 401) {
			event.locals.isAuthenticated = false;
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
			throw redirect(303, '/auth');
		}
	}

	return response;
};
