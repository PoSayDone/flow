<script lang="ts">
	import Button from '$lib/components/button.svelte';
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';

	export let data: PageData;

	const { form, enhance, constraints, errors } = superForm(data.loginForm, {
		clearOnSubmit: 'errors'
	});
</script>

<div class="popover">
	<h1>Вход</h1>
	<form method="POST" use:enhance>
		<div class="inputs">
			<input
				aria-invalid={$errors._errors ? 'true' : undefined}
				name="mail"
				type="email"
				placeholder="Email"
				value={$form.mail}
				{...$constraints.mail}
			/>
			<input
				aria-invalid={$errors._errors ? 'true' : undefined}
				name="password"
				required
				type="password"
				placeholder="Пароль"
				value={$form.password}
				{...$constraints.password}
			/>
		</div>
		<div class="errors">
			{#if $errors._errors}<p>{$errors._errors}</p>{/if}
		</div>
		<div class="buttons">
			<Button type="submit">Войти</Button>
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
		input[aria-invalid='true'] {
			border: 1px solid #e63d43;
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

	input.error {
		border: red thin solid;
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
