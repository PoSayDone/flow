import { z } from 'zod';

export const messageSchema = z.object({
	message: z.string()
});

export const loginSchema = z.object({
	mail: z.string().email(),
	password: z.string()
});

export const signinSchema1 = z.object({
	name: z.string().min(1)
});
export const signinSchema2 = signinSchema1.extend({
	mail: z.string().email()
});
export const signinSchema3 = signinSchema2.extend({
	birthdate: z.string().refine(
		(dateStr) => {
			const userDate = Date.parse(dateStr);
			const result = userDate < Date.now() && userDate > Date.parse('1900-01-01');
			return result;
		},
		{
			message: 'Введите правильную дату рождения'
		}
	)
});
export const signinSchema4 = signinSchema3.extend({
	sex: z.boolean().optional()
});
export const signinSchema = signinSchema4.extend({
	password: z.string()
});

export const interestsSchema = z.object({
	user_interests: z.number().array().max(5)
});

export const statusSchema = z.object({
	user_status: z.boolean(),
	user_trip_purposes: z.number().array(),
	user_departures: z.number().array(),
	user_arrivals: z.number().array()
});

export const profileSchema = z.object({
	name: z.string(),
	birthdate: z.string(),
	occupation: z.string(),
	about: z.string()
});

export const likeSchema = z.object({
	user_id: z.string(),
	like: z.boolean()
});

export const avatarSchema = z.object({
	image: z
		.instanceof(File, { message: 'Пожалуйста загрузите файл' })
		.refine((f) => f.size < 5_000_000, 'Файл должен быть меньше 5 мб')
});
