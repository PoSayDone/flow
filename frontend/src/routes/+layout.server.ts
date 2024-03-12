import type { LayoutServerLoad } from './$types';
import { faker } from '@faker-js/faker';

export const load: LayoutServerLoad = async ({ fetch }) => {
	// const user = {
	// 	id: faker.string.uuid(),
	// 	name: faker.person.firstName(),
	// 	mail: faker.internet.email(),
	// 	password_hash: faker.internet.password(),
	// 	occupation: faker.person.jobTitle(),
	// 	about: faker.person.bio(),
	// 	sex: faker.datatype.boolean(),
	// 	birthdate: faker.date.birthdate().toISOString().split('T')[0]
	// };

	// await fetch('http://nginx/api/users/', {
	// 	method: 'POST',
	// 	headers: {
	// 		'Content-Type': 'application/json'
	// 	},
	// 	body: JSON.stringify(user)
	// });
	//
	// for (let i = 0; i < faker.number.int({ min: 2, max: 5 }); i++) {
	// 	await fetch(
	// 		`http://nginx/api/user_interests/${user.id}/${faker.number.int({ min: 1, max: 13 })}`,
	// 		{ method: 'PUT' }
	// 	);
	// }
	//
	// for (let i = 0; i < faker.number.int({ min: 2, max: 5 }); i++) {
	// 	await fetch(
	// 		`http://nginx/api/user_trip_purposes/${user.id}/${faker.number.int({ min: 1, max: 5 })}`,
	// 		{
	// 			method: 'PUT'
	// 		}
	// 	);
	// }

	const response_user = await fetch('http://nginx/api/profile');
	const body = await response_user.json();
	return body;
};
