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
	type Options = {
		direction?: 'in' | 'out' | 'both';
	};
	function slideFade(
		_node: Element,
		{ delay = 0, duration = animationDuration, easing = circInOut }: Params = {},
		{ direction = 'both' }: Options = {}
	): TransitionConfig {
		let multiplier = 1;
		let translateValue = 100;

		if (direction === 'out') {
			multiplier = -1;
			translateValue = translateValue * 0.25;
		}

		return {
			delay,
			duration,
			easing,
			css: (t, u) => `
			background: var(--bg);
				transform-origin: "right";
                transform: translateX(${multiplier * translateValue * u}%);
                opacity: ${direction === 'out' ? t : '1'}
            `
		};
	}
</script>

{#key key}
	<div
		class="container"
		in:slideFade={{}}
		out:slideFade={{}}
		class:no-padding={key?.startsWith('/chats/') || key?.startsWith('/user_')}
		class:non-scrollable={key == '/'}
	>
		<slot />
	</div>
{/key}

<style>
	.container {
		padding: 0 20px;
		grid-row: 1;
		grid-column: 1;
		overflow-x: hidden;
		overflow-y: scroll;
		display: flex;
		flex-direction: column;
	}
	.non-scrollable {
		overflow: visible !important;
	}
	.no-padding {
		padding: 0;
	}
</style>
