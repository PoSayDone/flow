import { fail, message, superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { zod } from 'sveltekit-superforms/adapters';
import { signinSchema } from '$lib/schema';
import type { Actions } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
	const signinForm = await superValidate(zod(signinSchema));
	return { signinForm };
};

export const actions = {
	default: async ({ fetch, request }) => {
		const signinForm = await superValidate(request, zod(signinSchema));
		if (!signinForm.valid) return fail(400, { signinForm });
		const response = await fetch('http://nginx/api/auth/signin', {
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
		if (response.status == 409) {
			return message(signinForm, 'Пользователь с такой почтой уже зарегистрирован', {
				status: 409
			});
		}
	}
} satisfies Actions;
