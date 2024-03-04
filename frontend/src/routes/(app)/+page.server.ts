import type { PageServerLoad } from './$types';
import * as api from '$lib/api';

export const load: PageServerLoad = async () => {
	const body = { users: await api.get('/users') };
	return body;
};
