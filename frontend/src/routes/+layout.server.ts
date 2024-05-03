import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import { avatarSchema, interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { UserWStatus } from '$lib/types';
import { api_url } from '$lib/utils';

export const load: LayoutServerLoad = async ({ fetch }) => {
	const profile: UserWStatus = await (await fetch(`${api_url}/user/profile`)).json();

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
		statusForm,
		profileForm,
		interestsForm,
		avatarForm
	};

	return data;
};
