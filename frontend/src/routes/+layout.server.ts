import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import { avatarSchema, interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { UserWStatus } from '$lib/types';
import { apiUrl } from '$lib/utils';
import { pusherClient } from '$lib/pusher';

export const load: LayoutServerLoad = async ({ fetch, url }) => {
	const pathname = url.pathname;

	if (pathname.startsWith('/auth')) {
		const data = { pathname };
		return data;
	}

	const profile: UserWStatus = await (await fetch(`${apiUrl}/user/profile`)).json();

	const statusForm = await superValidate(
		{
			user_status: profile.status,
			user_trip_purposes: profile.trip_purposes,
			user_departures: profile.departures,
			user_arrivals: profile.arrivals
		},
		zod(statusSchema)
	);
	const profileForm = await superValidate(profile, zod(profileSchema));
	const avatarForm = await superValidate(zod(avatarSchema));
	const interestsForm = await superValidate(
		{ user_interests: profile.interests },
		zod(interestsSchema)
	);

	const data = {
		user: profile,
		pathname,
		statusForm,
		profileForm,
		interestsForm,
		avatarForm
	};

	return data;
};
