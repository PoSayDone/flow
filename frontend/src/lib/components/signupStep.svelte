<script>
	import { cubicOut } from 'svelte/easing';
	import { animationDuration } from '$lib/utils';
	import { fly } from 'svelte/transition';
</script>

<div
	class="step"
	in:fly={{ easing: cubicOut, duration: animationDuration, x: 400 }}
	out:fly={{ easing: cubicOut, duration: animationDuration, x: -400 }}
>
	<slot />
</div>

<style>
	.step {
		grid-row: 1;
		grid-column: 1;
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: center;
		text-align: center;
		font-size: 14px;
		font-weight: 600;
	}
</style>
