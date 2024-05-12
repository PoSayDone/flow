<script>
	import { animationDuration } from '$lib/utils';
	import { cubicIn, cubicInOut, cubicOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';
</script>

<div class="container" transition:fly={{ x: 100, duration: animationDuration, easing: cubicOut }}>
	<slot />
</div>

<style>
	.container {
		z-index: 10;
		background: var(--bg);
		grid-row: 1;
		grid-column: 1;
		overflow-x: hidden;
		overflow-y: scroll;
		display: flex;
		flex-direction: column;
	}
</style>
