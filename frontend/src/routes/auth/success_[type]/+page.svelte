<script lang="ts">
	import Logo from '$lib/assets/images/logo.svelte';
	import { approveIcon } from '$lib/assets/Appicons';
	import Icon from '$lib/components/icon.svelte';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	onMount(() => {
		setTimeout(() => {
			goto('/');
		}, 3000);
	});
</script>

<div class="container">
	<header>
		<div class="logo">
			<Logo />
		</div>
	</header>
	<div class="message">
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
			{#if $page.params.type === 'signin'}
				Вы успешно вошли<br />
				в аккаунт Flow
			{:else if $page.params.type === 'signup'}
				Спасибо за<br />
				регистрацию в flow
			{/if}
		</h1>
	</div>
</div>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: column;
		view-transition-name: hero;
		height: 100dvh;
		background: var(--gradient);
		background-size: var(--gradient-size);
		animation: var(--gradient-animation);
	}

	header {
		height: 86px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.message {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 12px;
	}

	.logo {
		color: var(--bg);
		:global(svg) {
			view-transition-name: logo;
		}
	}

	.text {
		color: var(--bg);
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
