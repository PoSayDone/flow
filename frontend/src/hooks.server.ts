import type { HandleFetch } from '@sveltejs/kit';

export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
	request.headers.set('cookie', `access_token=${event.cookies.get('access_token')}`);
	return fetch(request);
};
