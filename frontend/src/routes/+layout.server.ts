import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import { avatarSchema, interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { Arrival, Departure, Interest, TripPurpose, UserWStatus } from '$lib/types';
import { api_url } from '$lib/utils';

export const load: LayoutServerLoad = async ({ fetch }) => {
	const profile: UserWStatus = await (await fetch(`${api_url}/user/profile`)).json();
	const trip_purposes: TripPurpose[] = await (await fetch(`${api_url}/trip_purposes`)).json();
	const interests: Interest[] = await (await fetch(`${api_url}/interests`)).json();
	const departures: Departure[] = await (await fetch(`${api_url}/departures`)).json();
	const arrivals: Arrival[] = await (await fetch(`${api_url}/arrivals`)).json();

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
		interests: interests,
		trip_purposes: trip_purposes,
		departures: departures,
		arrivals: arrivals,
		statusForm,
		profileForm,
		interestsForm,
		avatarForm
	};

	return data;
};
