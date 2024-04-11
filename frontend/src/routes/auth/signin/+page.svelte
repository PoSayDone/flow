<script lang="ts">
	import Logo from '$lib/assets/images/logo.svelte';
	import Icon from '$lib/components/icon.svelte';
	import { addIcon, backIcon } from '$lib/assets/Appicons';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/button.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { approveIcon } from '$lib/assets/Appicons';
	import type { PageData } from './$types';
	import { zod } from 'sveltekit-superforms/adapters';
	import {
		signinSchema1,
		signinSchema2,
		signinSchema3,
		signinSchema4,
		signinSchema
	} from '$lib/schema';
	import { page } from '$app/stores';

	export let data: PageData;

	function nav_back() {
		if (step > 1) {
			step -= 1;
		} else {
			goto('/auth');
		}
	}

	function handlePasswordInput(event) {
		form.update(
			($form) => {
				$form.password = event.target.value;
				return $form;
			},
			{ taint: false }
		);
	}

	$: options.validators = steps[step - 1];

	let step = 1;
	const steps = [
		zod(signinSchema1),
		zod(signinSchema2),
		zod(signinSchema3),
		zod(signinSchema4),
		zod(signinSchema)
	];
	let showPassword = false;
	$: passwordInputType = showPassword ? 'text' : 'password';

	const { form, enhance, validateForm, options, errors, message } = superForm(data.signinForm, {
		dataType: 'json',
		async onSubmit({ cancel }) {
			if (step == steps.length) return;
			else cancel();

			const result = await validateForm({ update: true });
			if (result.valid) step = step + 1;
		},

		async onUpdated({ form }) {
			if (form.valid) step = 1;
		},

		onResult: ({ result }) => {
			console.log(result.status);
			if (result.status == 200) {
				setTimeout(() => {
					goto('/auth/login');
				}, 5000);
			} else {
				setTimeout(() => {
					goto('/auth/');
				}, 4000);
			}
		}
	});
</script>

{#if $message}
	<!-- eslint-disable-next-line svelte/valid-compile -->
	<div class="status" class:success={$page.status == 200} class:error={$page.status == 409}>
		{$message}
		{#if $page.status == 200}
			<Icon
				viewBox={approveIcon.viewBox}
				d={approveIcon.d}
				stroke_width={'1.3'}
				size={'40'}
				color={'#2461FF'}
			/>
		{:else}
			<Icon
				viewBox={addIcon.viewBox}
				d={addIcon.d}
				stroke_width={'1.3'}
				size={'46'}
				color={'#F14444'}
			/>
		{/if}
	</div>
{/if}
<header>
	<div class="nav-back">
		<button on:click={nav_back}>
			<Icon
				viewBox={backIcon.viewBox}
				d={backIcon.d}
				size={'40'}
				stroke_width={'2'}
				color={'#2461FF'}
			/>
		</button>
	</div>
	<div class="logo">
		<Logo />
	</div>
</header>
<form method="POST" action="/auth/signin" use:enhance class="content">
	{#if step === 1}
		<div class="input-block">
			<label for="name">Введите ваше имя. С этим именем вас будут видеть другие пользователи</label>
			<input placeholder="Ваше имя" name="name" type="text" bind:value={$form.name} />
			{#if $errors.name}<span class="invalid">Введите имя</span>{/if}
		</div>
	{:else if step === 2}
		<div class="input-block">
			<label for="email">Введите ваш email</label>
			<input placeholder="Ваш email" name="email" type="email" bind:value={$form.mail} />
			{#if $errors.mail}<span class="invalid">Неправильно указана почта</span>{/if}
		</div>
	{:else if step === 3}
		<div class="input-block">
			<label for="birthdate">Введите вашу дату рождения</label>
			<input name="birthdate" type="date" bind:value={$form.birthdate} />
		</div>
	{:else if step === 4}
		<div class="input-block">
			<label for="sex">Вы</label>
			<fieldset class="radios">
				<div>
					<input
						class="chip"
						id="men"
						type="radio"
						name="sex"
						value={true}
						bind:group={$form.sex}
					/>
					<label for="men">Мужчина</label>
				</div>
				<div>
					<input
						class="chip"
						id="women"
						type="radio"
						name="sex"
						value={false}
						bind:group={$form.sex}
					/>
					<label for="women">Женщина</label>
				</div>
				<div>
					<input
						class="chip"
						id="unknown"
						type="radio"
						name="sex"
						value={undefined}
						bind:group={$form.sex}
					/>
					<label for="unknown">Не указывать</label>
				</div>
			</fieldset>
			<!-- <input name="birthdate" type="text" /> -->
		</div>
	{:else}
		<div class="input-block">
			<label for="password">Придумайте пароль</label>
			<input
				placeholder="Пароль"
				name="password"
				type={passwordInputType}
				on:input={handlePasswordInput}
			/>
			<div class="show-password">
				<label for="show-password">Показать пароль</label>
				<input name="show-password" type="checkbox" bind:checked={showPassword} />
			</div>
			{#if $errors.password}<span class="invalid">{$errors.password}</span>{/if}
		</div>
	{/if}
	<Button>{step == 5 ? 'Зарегистрироваться' : 'Далее'}</Button>
</form>

<style lang="scss">
	header {
		display: flex;
		align-items: center;
		padding: 20px;
	}

	.nav-back {
		display: flex;
		flex: 1;
		align-items: center;
		justify-content: flex-start;
	}

	header:after {
		content: '';
		flex: 1;
	}

	.logo :global(svg) {
		view-transition-name: logo;
		z-index: 1;
	}

	.content {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		margin: 0 20px 20px 20px;
	}

	input {
		border: 0;
		font-size: 32px;
		font-weight: 700;
		text-align: center;
		width: 80%;
		&:focus {
			outline: none;
			border-bottom: 2px solid #000;
			margin-bottom: -1px;
		}
	}

	.show-password {
		display: flex;
		gap: 10px;
		align-items: center;
		align-self: flex-end;
		input {
			height: 24px;
			width: 24px;
		}
	}

	.input-block {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: center;
		text-align: center;
		font-size: 14px;
		font-weight: 600;
	}

	fieldset {
		display: flex;
		flex-direction: column;
		border: none;
		gap: 10px;
		justify-content: center;
		width: 60svw;
		max-width: 300px;
	}

	.chip {
		display: none;
	}

	.chip + label {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 46px;
		padding: 0 18px;
		border-radius: 100px;
		background: none;
		outline: 1.5px solid var(--bg-gray);
		border: none;
		cursor: pointer;
		transition: all 0.1s ease-in-out;

		:global(path) {
			transition: all 0.1s ease-in-out;
			stroke: #000;
		}

		:global(svg) {
			transition: all 0.1s ease-in-out;
		}
	}

	input[type='radio']:checked + label {
		background: #d3dfff;
		color: #2461ff;
		outline: none;
	}

	input[type='radio']:disabled + label {
		opacity: 0.4;
	}

	.invalid {
		color: #f14444;
	}

	.status {
		position: absolute;
		display: flex;
		gap: 20px;
		align-items: center;
		padding: 20px;
		border-radius: 20px;
		background: #fff;
		top: 20px;
		left: 50%;
		transform: translateX(-50%);
		width: 80%;
		box-shadow: 0px 4px 14px 0px #0000001f;
		z-index: 10;
	}

	.status.error {
		:global(svg) {
			transform: rotate(45deg);
		}
	}
</style>
