import { api_url, isAllowedHost, setCookies, removeAuth } from '$lib/utils';
import {
	redirect,
	type Cookies,
	type Handle,
	type HandleFetch,
	type RequestEvent
} from '@sveltejs/kit';

export const handle = (async ({ event, resolve }) => {
	await isUserAuthenticated(event);
	checkProtectedRoutes(event.url, event.cookies);
	return await resolve(event);
}) satisfies Handle;

async function isUserAuthenticated(event: RequestEvent): Promise<void> {
	try {
		const accessToken = event.cookies.get('access_token') ?? '';
		if (accessToken == '') {
			throw Error('No access token');
		}
	} catch (error) {
		await tryToRefreshToken(event);
	}
}

async function tryToRefreshToken(event: RequestEvent): Promise<void> {
	const refreshToken = event.cookies.get('refresh_token');
	if (refreshToken) {
		const response = await fetch(`${api_url}/auth/refresh`, {
			method: 'POST',
			headers: {
				cookie: `refresh_token=${refreshToken?.toString()}`
			}
		});

		if (!response.ok) {
			removeAuth(event.cookies);
		} else {
			setCookies(response, event);
		}
	}
}

function checkProtectedRoutes(url: URL, cookies: Cookies): void {
	if (!url.pathname.startsWith('/auth')) {
		const accessToken = cookies.get('access_token');
		if (!accessToken) redirect(302, '/auth');
	}
}

export const handleFetch: HandleFetch = async ({ request, event, fetch: nodeFetch }) => {
	const { cookies } = event;
	const requestURL = new URL(request.url);
	if (isAllowedHost(requestURL.host)) {
		request.headers.set('cookie', `access_token=${cookies.get('access_token')?.toString()}`);
	}

	const res = await nodeFetch(request);

	if (event.url.pathname == '/auth/signin') {
		setCookies(res, event);
	}

	return res;
};
