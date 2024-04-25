<script lang="ts">
	import Logo from '$lib/assets/images/logo.svelte';
	import Indicator from './indicator.svelte';
	import { addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';

	let showStatusModal = false;
</script>

<header>
	<Logo />
	<div class="indicator-container" on:click={() => (showStatusModal = true)}>
		<Indicator bind:showModal={showStatusModal} />
		<Icon viewBox={addIcon.viewBox} d={addIcon.d} stroke_width={'1.5'} size={'18'} color={'#000'} />
	</div>
</header>

<style>
	.indicator-container {
		background: #f2f1f6;
		border-radius: 100px;
		border: none;
		padding: 10px 14px;
		cursor: pointer;
		display: flex;
		align-items: center;
	}

	header {
		view-transition-name: header;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 25px 20px;
	}
</style>
