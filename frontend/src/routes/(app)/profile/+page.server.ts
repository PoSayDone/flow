import type { Actions } from './$types';

export const actions = {
	default: async ({ request, fetch }) => {
		const data = await request.formData();

		const name = data.get('name');
		const birthdate = data.get('birthdate');
		const occupation = data.get('occupation');
		const about = data.get('about');

		console.log(name, birthdate, occupation, about);

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
	}
} satisfies Actions;
