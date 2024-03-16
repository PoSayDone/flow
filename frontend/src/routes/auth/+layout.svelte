<script>
	import Logo_big from '$lib/assets/images/logo_big.svelte';
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { backIcon } from '$lib/assets/Appicons';
	import Icon from '$lib/components/icon.svelte';

	function nav_back() {
		if (browser) window.history.back();
	}
</script>

<div class="hero">
	{#if $page.url.pathname == '/auth/login'}
		<div class="header">
			<button on:click={nav_back}>
				<Icon viewBox={backIcon.viewBox} d={backIcon.d} size={'50'} stroke_width={'2'} />
			</button>
		</div>
	{/if}
	<div class="image">
		<Logo_big />
	</div>
	<div class="bottom">
		<slot />
	</div>
</div>

<style>
	.header {
		margin: 10px;
	}

	.hero {
		view-transition-name: hero;
		height: 100%;
		background: linear-gradient(168.51deg, #2461ff 1.38%, rgba(154, 91, 255, 0.87) 53.99%);
		display: flex;
		flex-direction: column;
	}

	.image {
		justify-content: center;
		height: max-content;
		display: flex;
		align-items: center;
		flex: 1;
	}

	.image :global(svg) {
		view-transition-name: logo;
		width: 70%;
		height: fit-content;
	}

	button {
		background: none;
	}
</style>
