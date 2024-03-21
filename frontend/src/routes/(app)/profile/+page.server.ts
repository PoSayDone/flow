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
	save_interests: async ({ request }) => {
		const data = await request.formData();
		console.log('values:');
		for (const pair of data.entries()) {
			console.log(pair[0] + ', ' + pair[1]);
		}
	},
	save_status: async ({ request }) => {
		const data = await request.formData();
		console.log('values:');
		for (const pair of data.entries()) {
			console.log(pair[0] + ', ' + pair[1]);
		}
	}
} satisfies Actions;
