<script>
	import { mainIcon, profileIcon, chatIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	import { page } from '$app/stores';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	export let duration = 300;
</script>

<nav class="navbar" transition:slide={{ easing: cubicInOut, duration, axis: 'y' }}>
	<a href="/chats" class:active={$page.url.pathname == '/chats'}
		><Icon d={chatIcon.d} viewBox={chatIcon.viewBox} /></a
	>
	<a href="/" class:active={$page.url.pathname == '/'}
		><Icon d={mainIcon.d} viewBox={mainIcon.viewBox} /></a
	>
	<a href="/profile" class:active={$page.url.pathname == '/profile'}
		><Icon d={profileIcon.d} viewBox={profileIcon.viewBox} /></a
	>
</nav>

<style lang="scss">
	nav {
		grid-area: nav;
		view-transition-name: nav;
		border-radius: 40px 40px 0px 0px;
		background-color: var(--fg-secondary);
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 67.5px;
		height: 70px;
		:global(path) {
			stroke: #d2d2d2;
		}
	}

	.active {
		:global(path) {
			stroke: #ffffff;
		}
	}
</style>
