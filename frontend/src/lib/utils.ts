interface Binding {
	[key: string]: string;
}

export function getAge(dateString: string) {
	const today = new Date();
	const birthDate = new Date(dateString);
	let age = today.getFullYear() - birthDate.getFullYear();
	const m = today.getMonth() - birthDate.getMonth();
	if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
		age--;
	}
	return age;
}

export const interests_binding: Binding = {
	'1': 'it',
	'2': 'vehicles',
	'3': 'sports',
	'4': 'fashion',
	'5': 'culinary',
	'6': 'alcohol',
	'7': 'art',
	'8': 'technology',
	'9': 'science',
	'10': 'finance',
	'11': 'motorcycless',
	'12': 'beauty',
	'13': 'business'
};

export const trip_purposes_binding: Binding = {
	'1': 'active_recreation',
	'2': 'culture',
	'3': 'sights',
	'4': 'parties',
	'5': 'extreme_and_sports',
	'6': 'to_the_mountains',
	'7': 'gastronomic_tour',
	'8': 'to_the_sea',
	'9': 'shopping'
};
