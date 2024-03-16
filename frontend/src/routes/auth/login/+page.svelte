<script>
	import Button from '$lib/components/button.svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	export let form;
</script>

<div class="popover">
	<h1>Вход</h1>
	<form
		method="POST"
		use:enhance={() => {
			return async ({ result }) => {
				await invalidateAll();
				await applyAction(result);
			};
		}}
	>
		<div class="inputs">
			<input name="mail" required type="email" placeholder="Email" />
			<input name="password" required type="password" placeholder="Пароль" />
		</div>
		<div class="errors">
			{#if form?.message}
				<p>{form.message}</p>
			{/if}
		</div>
		<div class="buttons">
			<Button>Войти</Button>
			<Button class="opaque">Не помню пароль</Button>
		</div>
	</form>
</div>

<style lang="scss">
	h1 {
		margin-bottom: 20px;
	}

	.popover {
		view-transition-name: popover;
		border-radius: 20px 20px 0 0;
		padding: 20px;
		display: flex;
		flex-direction: column;
		background: #fff;

		input {
			border-radius: 16px;
			border: 1px solid #cecece;
			padding: 19px;
			font-family: PP Pangram Sans Rounded;
			font-size: 14px;
			font-weight: 500;
			letter-spacing: -0.04em;
		}
	}

	.errors {
		font-family: Inter;
		font-size: 12px;
		font-weight: 400;
		letter-spacing: 0em;
		text-align: left;
		color: #e63d43;
		display: flex;
		align-items: center;
		height: 48px;
	}

	.inputs {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.buttons {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	@keyframes slide-from-bottom {
		from {
			transform: translateY(100%);
		}
	}

	@keyframes slide-to-bottom {
		to {
			transform: translateY(100%);
		}
	}

	:root::view-transition-old(popover) {
		animation:
			90ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
			300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-bottom;
	}
	:root::view-transition-new(popover) {
		animation:
			300ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-bottom,
			90ms cubic-bezier(0.4, 0, 1, 1) both fade-out;
	}
</style>
