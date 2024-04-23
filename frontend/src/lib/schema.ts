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
	name: z.string().optional(),
	birthdate: z.string().optional(),
	occupation: z.string().optional(),
	about: z.string().optional()
});

export const likeSchema = z.object({
	user_id: z.string().uuid(),
	like: z.boolean()
});

export const avatarSchema = z.object({
	file: z
		.instanceof(File)
		.refine((f) => f.size < 1_000_000, 'Max 1 Mb upload size.')
		.optional()
});
