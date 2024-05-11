<script lang="ts">
	import { scale } from 'svelte/transition';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<main>
	<div class="animation-container" transition:scale={{ duration: 1000 }}>
		<slot />
	</div>
</main>

<style>
	.animation-container {
		grid-row: 1;
		grid-column: 1;
	}
</style>
