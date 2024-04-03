import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const users = await fetch('http://nginx/api/user/solemates/10');
	const body = {};
	body['users'] = await users.json();
	return body;
};
