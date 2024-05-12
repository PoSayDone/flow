<script>
	import Logo from '$lib/components/logo.svelte';
	import { page } from '$app/stores';
	import Icon from '$lib/components/icon.svelte';
	import { backIcon } from '$lib/assets/Appicons';
	import { goto } from '$app/navigation';
	import { fade, slide } from 'svelte/transition';
	import { animationDuration, fasterAnimationDuration } from '$lib/utils';
	import { cubicInOut } from 'svelte/easing';

	function nav_back() {
		goto('/auth');
	}
</script>

<svelte:head>
	<meta name="theme-color" content="#2461ff" />
</svelte:head>

<div class="container" transition:fade={{ duration: animationDuration }}>
	{#if $page.url.pathname == '/auth/signin'}
		<header transition:slide={{ easing: cubicInOut, duration: fasterAnimationDuration, axis: 'y' }}>
			<button on:click={nav_back}>
				<Icon viewBox={backIcon.viewBox} d={backIcon.d} size={'50'} stroke_width={'2'} />
			</button>
		</header>
	{/if}
	<div class="logo">
		<Logo />
	</div>

	<div class="bottom">
		<slot />
	</div>
</div>

<style lang="scss">
	header {
		display: flex;
		align-items: center;
		height: 86px;
		padding: 0 20px;
	}

	.bottom {
		position: fixed;
		bottom: 0;
		width: 100%;
	}

	.container {
		grid-area: main;
		height: 100dvh;
		flex: 1;
		display: flex;
		flex-direction: column;
		background: var(--gradient);
		background-size: var(--gradient-size);
		animation: var(--gradient-animation);
		background-position: 25% 25%;
	}

	.logo {
		top: 25dvh;
		position: absolute;
		justify-content: center;
		display: flex;
		align-items: center;
		flex: 1;
		width: 100%;
		z-index: 0;
		color: var(--bg);
		:global(svg) {
			width: 70%;
			height: fit-content;
		}
	}

	button {
		background: none;
	}

	:root::view-transition-group(logo) {
		z-index: 1;
	}
</style>
