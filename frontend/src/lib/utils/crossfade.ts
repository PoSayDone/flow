import { animationDuration } from '$lib/utils';
import { crossfade } from 'svelte/transition';

export const [send, receive] = crossfade({ duration: animationDuration });
