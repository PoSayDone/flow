<script>
	import Button from '$lib/components/button.svelte';
	import { animationDuration } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { slide } from 'svelte/transition';
</script>

<div
	class="auth_buttons"
	in:slide={{ axis: 'y', duration: animationDuration }}
	out:slide={{ axis: 'y', duration: animationDuration, delay: animationDuration }}
>
	<p class="info">
		Переходя дальше, ты соглашаешься на обработку персональных данных в соответсвии
		спользовательским соглашением
	</p>
	<div class="buttons">
		<Button class="white" on:click={() => goto('/auth/signup')}>Создать аккаунт</Button>
		<Button class="border" on:click={() => goto('/auth/signin')}>Войти</Button>
	</div>
</div>

<style>
	.auth_buttons {
		padding: 20px;
	}
	.info {
		color: #fff;
		text-align: center;
		margin-bottom: 20px;
	}

	.buttons {
		gap: 5px;
		display: flex;
		flex-direction: column;
	}
</style>
