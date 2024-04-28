import { api_url } from '$lib/utils';
import { redirect, type HandleFetch, type RequestEvent } from '@sveltejs/kit';
import * as scp from 'set-cookie-parser';

let isRefreshing = false;
let requestsWhileRefreshing: Request[] = [];

const isAllowedHost = (host: string) => {
	return (
		host === 'localhost' || host === 'nginx' || host === 'flowtrip.ru' || host === '192.168.1.137'
	);
};

function setCookies(
	res: Response,
	event: RequestEvent<Partial<Record<string, string>>, string | null>
) {
	const setCookie = res.headers.getSetCookie();

	if (setCookie && isAllowedHost(event.url.hostname)) {
		const parsed = scp.parse(res);

		parsed.forEach((cookie) => {
			event.cookies.set(cookie.name, cookie.value, {
				...cookie
			});
		});

		if (res.status == 200) {
			if (event.url.pathname == '/api/auth/signin' || event.url.pathname == '/api/auth/refresh') {
				event.locals.isAuthenticated = true;
			}
		}
	}
}

export const handleFetch: HandleFetch = async ({ request, fetch: nodeFetch, event }) => {
	const { cookies } = event;
	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');

	if (refreshToken) {
		event.locals.isAuthenticated = true;
	} else if (!accessToken && !refreshToken) {
		event.locals.isAuthenticated = false;
	}

	if (!event.url.pathname.includes('/auth')) {
		if (!event.locals.isAuthenticated) {
			throw redirect(303, '/auth/signin');
		}
	}

	const requestURL = new URL(request.url);
	if (isAllowedHost(requestURL.host)) {
		request.headers.set('cookie', `access_token=${cookies.get('access_token')?.toString()}`);
	}

	const res = await nodeFetch(request);

	if (res.status === 401 && !event.url.pathname.includes('/auth')) {
		if (!isRefreshing) {
			isRefreshing = true;
			const refresh_res = await nodeFetch(`${api_url}/auth/refresh`, {
				method: 'POST',
				headers: {
					cookie: `refresh_token=${refreshToken?.toString()}`
				}
			});
			if (refresh_res.status !== 200) {
				cookies.delete('access_token', { path: '/' });
				cookies.delete('refresh_token', { path: '/' });
			} else {
				setCookies(refresh_res, event);
			}
			isRefreshing = false;
			requestsWhileRefreshing.unshift(request);
			requestsWhileRefreshing.forEach((request) => {
				request.headers.set('cookie', `access_token=${cookies.get('access_token')?.toString()}`);
				nodeFetch(request);
			});
			requestsWhileRefreshing = [];
		} else {
			requestsWhileRefreshing.push(request);
		}
	}

	setCookies(res, event);
	return res;
};
