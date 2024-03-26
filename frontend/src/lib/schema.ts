import { z } from 'zod';

export const interestsSchema = z.object({
	user_interests: z.number().array().max(5)
});

export const statusSchema = z.object({
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
