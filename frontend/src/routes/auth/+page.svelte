<script>
	import Button from '$lib/components/button.svelte';
	import { goto } from '$app/navigation';
</script>

<div class="auth_buttons">
	<p class="info">
		Переходя дальше, ты соглашаешься на обработку персональных данных в соответсвии
		спользовательским соглашением
	</p>
	<div class="buttons">
		<Button class="white">Создать аккаунт</Button>
		<Button class="border" on:click={() => goto('/auth/login')}>Войти</Button>
	</div>
</div>

<style>
	.info {
		color: #fff;
		text-align: center;
	}

	.buttons {
		gap: 5px;
		display: flex;
		flex-direction: column;
		padding: 20px;
	}
</style>
