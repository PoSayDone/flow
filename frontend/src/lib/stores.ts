import { writable, type Writable } from 'svelte/store';
import type { User } from './types';

export const status: Writable<boolean> = writable();
export const users: Writable<User[]> = writable();
export const selectedInterests: Writable<number[]> = writable([]);
export const closeCurrentDialog: Writable<() => void> = writable();
export const submitCurrentDialog: Writable<() => void> = writable();
