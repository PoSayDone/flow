import { writable, type Writable } from 'svelte/store';
import type { Soulmate } from './types';

export const status: Writable<boolean> = writable();
export const soulmates: Writable<Soulmate[]> = writable();
export const selectedInterests: Writable<number[]> = writable([]);
export const closeCurrentDialog: Writable<() => void> = writable();
export const submitCurrentDialog: Writable<() => void> = writable();
export const showStatusModal: Writable<boolean> = writable(false);
export const showAvatarModal: Writable<boolean> = writable(false);
export const showInterestsModal: Writable<boolean> = writable(false);
