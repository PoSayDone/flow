<script lang="ts">
	import { scale } from 'svelte/transition';
	import type { PageData } from './$types';
	import { cubicInOut } from 'svelte/easing';

	export let data: PageData;
</script>

<div
	class="animation-container"
	transition:scale={{ duration: 300, easing: cubicInOut, start: 0.6 }}
>
	<slot />
</div>

<style>
	.animation-container {
		display: flex;
		flex-direction: column;
		background: transparent;
		z-index: 1;
		grid-area: main;
	}
</style>
