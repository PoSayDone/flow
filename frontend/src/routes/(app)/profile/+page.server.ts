import { avatarSchema, interestsSchema, profileSchema, statusSchema } from '$lib/schema';
import { apiUrl } from '$lib/utils';
import { redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { fail, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const actions = {
	update_interests: async ({ request, fetch }) => {
		const interestsForm = await superValidate(request, zod(interestsSchema));
		if (!interestsForm.valid) return fail(400, { interestsForm });
		await fetch(`${apiUrl}/user/interests/edit`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				tags: interestsForm.data.user_interests
			})
		});
	},
	update_status: async ({ request, fetch }) => {
		const statusForm = await superValidate(request, zod(statusSchema));
		if (!statusForm.valid) return fail(400, { statusForm });
		await fetch(`${apiUrl}/user/status_data/edit`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(statusForm.data)
		});
	},
	update_profile: async ({ request, fetch }) => {
		const profileForm = await superValidate(request, zod(profileSchema));
		if (!profileForm.valid) return fail(400, { profileForm });
		await fetch(`${apiUrl}/user/`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(profileForm.data)
		});
	},
	update_avatar: async ({ request, fetch }) => {
		const formData = await request.formData();
		const avatarForm = await superValidate(
			{ image: formData.get('image') as File },
			zod(avatarSchema)
		);
		if (!avatarForm.valid) {
			return setError(avatarForm, 'C этим изображением что-то не так, попробуйте другое');
		}
		const response = await fetch(`${apiUrl}/user/image`, {
			method: 'PATCH',
			body: formData
		});
		if (response.status == 413) {
			return setError(avatarForm, 'Файл должен быть меньше 5 мб');
		}
	},
	logout: async ({ cookies }) => {
		cookies.delete('access_token', { path: '/' });
		cookies.delete('refresh_token', { path: '/' });
		return redirect(302, '/auth');
	}
} satisfies Actions;
