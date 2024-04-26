import { messageSchema } from '$lib/schema';
import type { Actions } from '@sveltejs/kit';
import { fail, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { PageServerLoad } from './$types';
import type { Message, User } from '$lib/types';
import { api_url } from '$lib/utils';

export const load: PageServerLoad = async ({ params, fetch, parent }) => {
	const messageForm = await superValidate(zod(messageSchema));
	const conversation_id = params.conversation_id;
	const { messages, users }: { messages: Message[]; users: User[] } = await (
		await fetch(`${api_url}/chats/${conversation_id}`, {
			method: 'GET'
		})
	).json();

	const parentData = await parent();
	return { messageForm, conversation_id, messages, users, parentData };
};

export const actions = {
	send_message: async ({ request, fetch, params }) => {
		const messageForm = await superValidate(request, zod(messageSchema));
		if (!messageForm.valid) return fail(400, { messageForm });
		await fetch(`${api_url}/chats/${params.conversation_id}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				content: messageForm.data.message
			})
		});
	}
} satisfies Actions;
