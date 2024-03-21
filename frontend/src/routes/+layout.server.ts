import type { LayoutServerLoad } from './$types';
import { faker } from '@faker-js/faker';

export const load: LayoutServerLoad = async ({ fetch }) => {
	const response_user = await fetch('http://nginx/api/profile');
	const body = await response_user.json();
	return body;
};
