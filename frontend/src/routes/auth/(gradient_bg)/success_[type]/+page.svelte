<script lang="ts">
	import Logo from '$lib/components/logo.svelte';
	import { approveIcon } from '$lib/assets/Appicons';
	import Icon from '$lib/components/icon.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { fade, slide } from 'svelte/transition';
	import { animationDuration } from '$lib/utils';
	import { cubicInOut } from 'svelte/easing';

	onMount(() => {
		setTimeout(() => {
			goto('/');
		}, 3000);
	});

	const text =
		$page.params.type === 'signin'
			? 'Вы успешно вошли в аккаунт Flow'
			: 'Спасибо за регистрацию в flow';
</script>

<div
	class="popover"
	transition:slide={{ easing: cubicInOut, axis: 'y', duration: animationDuration }}
>
	<div class="icon">
		<Icon
			viewBox={approveIcon.viewBox}
			d={approveIcon.d}
			stroke_width={'1.5'}
			size={'28'}
			color={'#54e346'}
		/>
	</div>

	<h1 class="text">
		{text}
	</h1>
</div>

<style lang="scss">
	.popover {
		height: 20dvh;
		z-index: 1;
		position: absolute;
		bottom: 0;
		width: 100%;
		border-radius: 20px 20px 0 0;
		padding: 20px;
		align-items: center;
		display: flex;
		background: #fff;
		box-shadow: var(--toastBoxShadow);
	}

	.text {
		color: var(--fg);
		text-align: center;
	}

	.icon {
		height: 56px;
		width: 56px;
		background: var(--bg);
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 100%;
	}
</style>
