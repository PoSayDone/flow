import type { UserWStatus } from '$lib/types';
import { apiUrl } from '$lib/utils';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const pageUser: UserWStatus = await (await fetch(`${apiUrl}/user/profile/${params.id}`)).json();
	const body = { pageUser };
	return body;
};
