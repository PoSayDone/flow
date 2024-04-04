import type { UserWStatus } from '$lib/types';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const pageUser: UserWStatus = await (
		await fetch(`http://nginx/api/user/profile/${params.id}`)
	).json();
	const body = { pageUser };
	return body;
};
