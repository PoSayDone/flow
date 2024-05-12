<script lang="ts">
	import Logo from '$lib/components/logo.svelte';
	import Indicator from './indicator.svelte';
	import { addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	import { browser } from '$app/environment';
	import { animationDuration } from '$lib/utils';
	import Skeleton from './skeleton.svelte';

	export let showStatusModal = false;

	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';
</script>

<header transition:slide={{ easing: cubicInOut, duration: animationDuration, axis: 'y' }}>
	<div class="logo">
		<Logo />
	</div>
	{#if browser}
		<button class="indicator-container" on:click={() => (showStatusModal = true)}>
			<Indicator />
			<Icon
				viewBox={addIcon.viewBox}
				d={addIcon.d}
				stroke_width={'1.5'}
				size={'18'}
				color={'#000'}
			/>
		</button>
	{:else}
		<Skeleton width="140px" height="38px" borderRadius={'100px'} />
	{/if}
</header>

<style lang="scss">
	.logo {
		:global(svg) {
			view-transition-name: logo;
			color: var(--primary);
		}
	}

	.indicator-container {
		background: #f2f1f6;
		border-radius: 100px;
		border: none;
		padding: 0px 14px;
		height: 38px;
		cursor: pointer;
		display: flex;
		align-items: center;
	}

	header {
		grid-area: header;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0px 20px;
		margin: 20px 0;
	}
</style>
