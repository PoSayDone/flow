import type { Conversation } from '$lib/types';
import { api_url } from '$lib/utils';
import type { PageServerLoad } from '../$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const chats_response = await fetch(`${api_url}/chats/`);
	const chats_array: Conversation[] = await chats_response.json();
	const chats = { chats: chats_array };
	return chats;
};
