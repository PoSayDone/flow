import { writable, type Writable } from 'svelte/store';

export const status = writable();
export const users = writable();
export const selectedInterests: Writable<number[]> = writable([]);
export const closeCurrentDialog: Writable<() => void> = writable();
export const submitCurrentDialog: Writable<() => void> = writable();
