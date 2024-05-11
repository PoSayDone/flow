<script lang="ts">
	import { animationDuration } from '$lib/utils';
	import { circInOut } from 'svelte/easing';

	import { type EasingFunction, type TransitionConfig } from 'svelte/transition';

	export let key: string | undefined;
	type Params = {
		delay?: number;
		duration?: number;
		easing?: EasingFunction;
	};

	function slideFade(
		_node: Element,
		{ delay = 0, duration = animationDuration, easing = circInOut }: Params = {}
	): TransitionConfig {
		return {
			delay,
			duration,
			easing,
			css: (t, u) => `
                transform: translateX(${300 * u}px);
                opacity: ${t};
            `
		};
	}
</script>

{#key key}
	<div
		transition:slideFade
		class:no-padding={key?.startsWith('/chats/') || key?.startsWith('/user_')}
	>
		<slot />
	</div>
{/key}

<style>
	div {
		padding: 0 20px;
		grid-row: 1;
		grid-column: 1;
		overflow-y: scroll;
		display: flex;
		flex-direction: column;
	}
	.no-padding {
		padding: 0;
	}
</style>
