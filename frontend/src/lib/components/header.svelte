<script>
	import Logo from '$lib/assets/images/logo.svelte';
	import Indicator from './indicator.svelte';
</script>

<header>
	<Logo />
	<Indicator />
</header>

<style>
	header {
		view-transition-name: header;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 25px 20px;
	}
</style>
