<script>
	import { status } from '$lib/stores';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		status.set($page.data.user.status);
	});
</script>

<div class="indicator-container">
	<span class="indicator" class:active={$status}></span>
	<span class="status">
		{$status ? 'Активный' : 'Перерыв'}
	</span>
</div>

<style lang="scss">
	.indicator-container {
		background: none;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.indicator {
		margin-right: 6px;
		background: #ff3b3b;
		width: 10px;
		height: 10px;
		border-radius: 100%;
		&.active {
			background: #72cd2a;
		}
	}

	.status {
		color: #000;
		margin-right: 14px;
	}
</style>
