import { fail, message, setError, superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { zod } from 'sveltekit-superforms/adapters';
import { signinSchema, signinSchema2 } from '$lib/schema';
import type { Actions } from '@sveltejs/kit';
import { api_url } from '$lib/utils';

export const load: PageServerLoad = async () => {
	const signinForm = await superValidate(zod(signinSchema));
	return { signinForm };
};

export const actions = {
	check_email: async ({ fetch, request }) => {
		const emailForm = await superValidate(request, zod(signinSchema2));
		if (!emailForm.valid) return fail(400, { signinForm: emailForm });
		const response = await fetch(`${api_url}/auth/check_email/${emailForm.data.mail}`, {
			method: 'GET'
		});
		if (response.status == 409) {
			return setError(emailForm, 'mail', 'Пользователь с такой почтой уже зарегистрирован');
		}
		return { emailForm };
	},
	signin: async ({ fetch, request }) => {
		const signinForm = await superValidate(request, zod(signinSchema));
		if (!signinForm.valid) return fail(400, { signinForm });
		const response = await fetch(`${api_url}/auth/signup`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(signinForm.data)
		});
		if (response.status == 201) {
			return message(
				signinForm,
				'Успешная регистрация, через 5 секунд вы будете перенаправлены на страницу входа'
			);
		}
	}
} satisfies Actions;
