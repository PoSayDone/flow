<script>
	import Logo_big from '$lib/assets/images/logo_big.svelte';
	import { page } from '$app/stores';
	import Icon from '$lib/components/icon.svelte';
	import { backIcon } from '$lib/assets/Appicons';
	import { goto } from '$app/navigation';

	function nav_back() {
		goto('/auth');
	}
</script>

<div class="container">
	{#if $page.url.pathname == '/auth/login'}
		<header>
			<button on:click={nav_back}>
				<Icon viewBox={backIcon.viewBox} d={backIcon.d} size={'50'} stroke_width={'2'} />
			</button>
		</header>
	{/if}
	<div class="image">
		<Logo_big />
	</div>
	<div class="bottom">
		<slot />
	</div>
</div>

<style lang="scss">
	header {
		height: 86px;
		padding: 0 20px;
	}

	.container {
		view-transition-name: hero;
		height: 100dvh;
		flex: 1;
		display: flex;
		flex-direction: column;
		background: var(--gradient);
		background-size: var(--gradient-size);
		animation: var(--gradient-animation);
	}

	.image {
		justify-content: center;
		height: max-content;
		display: flex;
		align-items: center;
		flex: 1;
	}

	.image {
		:global(svg) {
			view-transition-name: logo;
			width: 70%;
			height: fit-content;
			z-index: 1;
		}
	}

	button {
		background: none;
	}

	:root::view-transition-group(logo) {
		z-index: 1;
	}
</style>
