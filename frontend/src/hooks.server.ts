import { api_url } from '$lib/utils';
import { redirect, type Handle, type HandleFetch, type RequestEvent } from '@sveltejs/kit';
import * as scp from 'set-cookie-parser';

const isAllowedHost = (host: string) => {
	return host === 'localhost' || host === 'nginx';
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

let needsRefresh = false;

function checkTokenRequest(): Promise<void> {
	return new Promise(function (resolve) {
		(function waitForTokenRequest() {
			if (!needsRefresh) return resolve();
			setTimeout(waitForTokenRequest, 30);
		})();
	});
}

export const handle: Handle = async ({ event, resolve }) => {
	if (needsRefresh) {
		await checkTokenRequest();
	}
	console.log(event.cookies.get('access_token'));

	const { cookies } = event;
	const accessToken = cookies.get('access_token');
	const refreshToken = cookies.get('refresh_token');

	if (refreshToken) {
		event.locals.isAuthenticated = true;
		if (!accessToken) {
			needsRefresh = true;
		}
	} else if (!accessToken && !refreshToken) {
		event.locals.isAuthenticated = false;
	}

	if (!event.url.pathname.includes('/auth')) {
		if (!event.locals.isAuthenticated) {
			throw redirect(303, '/auth/signin');
		}
	}

	if (needsRefresh && !event.url.pathname.includes('/auth')) {
		const refresh_res = await fetch(`${api_url}/auth/refresh`, {
			method: 'POST',
			headers: {
				cookie: `refresh_token=${refreshToken?.toString()}`
			}
		});
		if (!refresh_res.ok) {
			cookies.delete('access_token', { path: '/' });
			cookies.delete('refresh_token', { path: '/' });
		} else {
			setCookies(refresh_res, event);
		}
	}

	const result = await resolve(event);
	if (needsRefresh) {
		needsRefresh = false;
	}
	return result;
};

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
