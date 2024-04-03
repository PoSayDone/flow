export type User = {
	id: string;
	name: string;
	occupation: string;
	about: string;
	mail: string;
	password_hash: string;
	sex: boolean;
	birthdate: Date;
	registration_date: Date;
	conversations: Conversation[];
	messages: Message[];
};

export type Message = {
	id: number;
	body: string;
	image: string;
	created_at: Date;
	conversation_id: number;
	conversation: Conversation;
	sender_id: string;
	sender: User;
};

export type Conversation = {
	id: number;
	created_at: Date;
	updated_at: Date;
	messages: Message[];
	users: User[];
	is_deleted: boolean;
};

interface Binding {
	[key: string]: string;
}

export const interestsRu: Binding = {
	it: 'IT',
	vehicles: 'Автомобили',
	sports: 'Спорт',
	fashion: 'Мода',
	culinary: 'Кулинария',
	alcohol: 'Алкоголь',
	art: 'Искусство',
	technology: 'Технологии',
	science: 'Наука',
	finance: 'Финансы',
	motorcycles: 'Мототехника',
	beauty: 'Красота',
	business: 'Бизнес'
};

export const tripPurposesRu: Binding = {
	active_recreation: 'Aктивный отдых',
	culture: 'Культура',
	sights: 'Достопримечательности',
	parties: 'Тусовки',
	extreme_and_sports: 'Экстрим и спорт',
	to_the_mountains: 'В горы',
	gastronomic_tour: 'Гастротур',
	to_the_sea: 'На море',
	shopping: 'Шоппинг'
};
