import type { PageServerLoad } from './$types';
import * as api from '$lib/api';

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('access_token');
	const body = api.get('/user', token);
	return body;
};
