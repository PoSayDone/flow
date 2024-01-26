import { writable } from 'svelte/store';

export const modalShown = writable(false);
export const status = writable('active');