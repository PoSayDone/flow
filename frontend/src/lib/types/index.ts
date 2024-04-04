export type Soulmate = {
	id: string;
	name: string;
	occupation: string;
	about: string;
	birthdate: Date;
	trip_purposes: number[];
};

export type User = {
	id: string;
	status: boolean;
	name: string;
	occupation: string;
	about: string;
	mail: string;
	sex: boolean;
	birthdate: Date;
	registration_date: Date;
};

export type UserWMessages = {
	conversations: Conversation[];
	messages: Message[];
} & User;

export type UserWStatus = {
	interests: number[];
	trip_purposes: number[];
	departures: number[];
	arrivals: number[];
} & User;

export type UserFullType = UserWMessages & UserWStatus;

export type Interest = {
	id: number;
	interest_name: string;
};

export type TripPurpose = {
	id: number;
	purpose_name: string;
};

export type Departure = {
	id: number;
	departure_name: string;
};

export type Arrival = {
	id: number;
	arrival_name: string;
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
