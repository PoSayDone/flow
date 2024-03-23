import type { Actions } from './$types';

export const actions = {
	save_profile: async ({ request, fetch }) => {
		const data = await request.formData();

		const name = data.get('name');
		const birthdate = data.get('birthdate');
		const occupation = data.get('occupation');
		const about = data.get('about');

		await fetch('http://nginx/api/user/', {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				name: name,
				birthdate: birthdate,
				occupation: occupation,
				about: about
			})
		});
	},
	save_interests: async ({ request, fetch }) => {
		const data = await request.formData();
		const interests: number[] = [...data.keys()].map((str) => parseInt(str));

		await fetch('http://nginx/api/user_interests/edit', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				tags: interests
			})
		});
	},
	save_status: async ({ request, fetch }) => {
		const data = await request.formData();

		const tripPurposes: number[] = [];
		const departures: number[] = [];
		const arrivals: number[] = [];

		for (const item of data.entries()) {
			console.log(item[0], ' ', item[1]);
		}

		for (const item of data.keys()) {
			if (item.includes('trip_purpose')) {
				tripPurposes.push(parseInt(item.replace('trip_purpose_', '')));
			} else if (item.includes('departure')) {
				departures.push(parseInt(item.replace('departure_', '')));
			} else if (item.includes('arrival')) {
				arrivals.push(parseInt(item.replace('arrival_', '')));
			}
		}

		await fetch('http://nginx/api/user_trip_purposes/edit', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				tags: tripPurposes
			})
		});

		await fetch('http://nginx/api/user_departures/edit', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				locations: departures
			})
		});

		await fetch('http://nginx/api/user_arrivals/edit', {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				locations: arrivals
			})
		});
	}
} satisfies Actions;
