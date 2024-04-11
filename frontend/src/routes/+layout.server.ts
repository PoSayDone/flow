import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import {
	avatarSchema,
	interestsSchema,
	likeSchema,
	profileSchema,
	statusSchema
} from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';
import type { Arrival, Departure, Interest, TripPurpose, UserWStatus } from '$lib/types';

export const load: LayoutServerLoad = async ({ fetch }) => {
	const profile: UserWStatus = await (await fetch('http://nginx/api/user/profile')).json();
	const trip_purposes: TripPurpose[] = await (await fetch('http://nginx/api/trip_purposes')).json();
	const interests: Interest[] = await (await fetch('http://nginx/api/interests')).json();
	const departures: Departure[] = await (await fetch('http://nginx/api/departures')).json();
	const arrivals: Arrival[] = await (await fetch('http://nginx/api/arrivals')).json();

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
	const likeForm = await superValidate(zod(likeSchema));

	const data = {
		user: profile,
		interests: interests,
		trip_purposes: trip_purposes,
		departures: departures,
		arrivals: arrivals,
		statusForm,
		profileForm,
		interestsForm,
		likeForm,
		avatarForm
	};

	return data;
};
