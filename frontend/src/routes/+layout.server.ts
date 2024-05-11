import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import { avatarSchema, interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { UserWStatus } from '$lib/types';
import { apiUrl } from '$lib/utils';

export const load: LayoutServerLoad = async ({ fetch, url }) => {
	if (url.pathname.startsWith('/auth')) {
		const data = { pathname: url.pathname };
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
		pathname: url.pathname,
		user: profile,
		statusForm,
		profileForm,
		interestsForm,
		avatarForm
	};

	return data;
};
