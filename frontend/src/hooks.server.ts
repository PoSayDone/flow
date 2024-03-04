import type { Handle } from "@sveltejs/kit";

export function handle({ event, resolve }): Handle {
	const jwt = event.cookies.get('access_token');
	event.locals.user_token = jwt ? jwt : undefined;

	return resolve(event);
}