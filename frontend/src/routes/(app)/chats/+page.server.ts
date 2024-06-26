import type { Conversation } from '$lib/types';
import { apiUrl } from '$lib/utils';
import type { PageServerLoad } from '../$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const chats_response = await fetch(`${apiUrl}/chats/`);
	const chats_array: Conversation[] = await chats_response.json();
	const chats = { chats: chats_array };
	return chats;
};
