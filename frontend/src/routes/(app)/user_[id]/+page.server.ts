import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const users = await fetch(`http://nginx/api/profile/${params.id}`);
	const body = await users.json();
	return body;
};
