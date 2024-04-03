import { superValidate } from 'sveltekit-superforms';
import type { LayoutServerLoad } from './$types';
import { interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { zod } from 'sveltekit-superforms/adapters';

export const load: LayoutServerLoad = async ({ fetch }) => {
	const profile = (await fetch('http://nginx/api/user/profile')).json();
	const trip_purposes = (await fetch('http://nginx/api/trip_purposes')).json();
	const interests = (await fetch('http://nginx/api/interests')).json();
	const departures = (await fetch('http://nginx/api/departures')).json();
	const arrivals = (await fetch('http://nginx/api/arrivals')).json();

	const statusForm = await superValidate(await profile, zod(statusSchema));
	const profileForm = await superValidate(await profile, zod(profileSchema));
	const interestsForm = await superValidate(await profile, zod(interestsSchema));
	const likeForm = await superValidate(zod(statusSchema));

	const data = {
		...(await profile),
		interests: await interests,
		trip_purposes: await trip_purposes,
		departures: await departures,
		arrivals: await arrivals,
		statusForm,
		profileForm,
		interestsForm,
		likeForm
	};

	return data;
};
