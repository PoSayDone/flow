export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();

		const formData = new URLSearchParams();
		formData.append('username', data.get('mail'));
		formData.append('password', data.get('password'));

		const requestOptions = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: formData
		};

		const response = await fetch(`http://nginx/api/auth/token`, requestOptions);
		const body = await response.json();

		const value = body.access_token;
		cookies.set('access_token', value, { path: '/' });
	}
};

