import { writable, type Writable } from 'svelte/store';

export const modalShown = writable(false);
export const status = writable('active');
export const users = writable();
export const selectedInterests: Writable<number[]> = writable([]);
export const statusProperties: Writable<StatusPopupData> = writable({
	tripPurposes: [],
	departures: [],
	arrivals: []
});
