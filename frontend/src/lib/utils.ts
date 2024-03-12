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
	'2': 'cars',
	'3': 'sport',
	'4': 'fashion',
	'5': 'gastronomy',
	'6': 'alcohol',
	'7': 'art',
	'8': 'technologies',
	'9': 'science',
	'10': 'finance',
	'11': 'motorcycles',
	'12': 'beauty',
	'13': 'business'
};

export const trip_purposes_binding: Binding = {
	'1': 'outdoor_activities',
	'2': 'mountains',
	'3': 'culture',
	'4': 'sea',
	'5': 'parties'
};
