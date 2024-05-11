<script lang="ts">
	import Logo from '$lib/assets/images/logo.svelte';
	import Icon from '$lib/components/icon.svelte';
	import { addIcon, backIcon } from '$lib/assets/Appicons';
	import { beforeNavigate, goto } from '$app/navigation';
	import Button from '$lib/components/button.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { approveIcon } from '$lib/assets/Appicons';
	import type { PageData } from './$types';
	import { toast } from '@zerodevx/svelte-toast';
	import { zod } from 'sveltekit-superforms/adapters';
	import {
		signinSchema1,
		signinSchema2,
		signinSchema3,
		signinSchema4,
		signinSchema
	} from '$lib/schema';
	import { page } from '$app/stores';
	import SignupStep from '$lib/components/signupStep.svelte';

	export let data: PageData;
	let loading = false;

	function nav_back() {
		if (step > 1) {
			step -= 1;
		} else {
			goto('/auth');
		}
	}

	beforeNavigate(({ cancel, to }) => {
		if (step > 1 && to?.route.id !== '/auth/success_[type]') {
			cancel();
			step -= 1;
		}
	});

	function handlePasswordInput(event) {
		form.update(
			($form) => {
				$form.password = event.target?.value;
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
		resetForm: false,

		async onSubmit({ cancel, action }) {
			if (step == 2) {
				loading = true;
				action.search = '?/check_email';
				return;
			}

			if (step == steps.length) {
				loading = true;
				return;
			} else cancel();

			const result = await validateForm({ update: true });
			if (result.valid) step = step + 1;
		},

		onResult: ({ result }) => {
			loading = false;
			if (step == 2) {
				if (result.status == 200) step = step + 1;
			} else {
				if (result.type == 'redirect') {
					console.log(result);
					goto(result.location);
				} else {
					toast.push('Что-то пошло не так');
				}
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
<form method="POST" action="?/signup" use:enhance>
	<div class="steps-container">
		{#if step === 1}
			<SignupStep>
				<label for="name"
					>Введите ваше имя. С этим именем вас будут видеть другие пользователи</label
				>
				<input placeholder="Ваше имя" name="name" type="text" bind:value={$form.name} />
				{#if $errors.name}<span class="invalid">Введите имя</span>{/if}
			</SignupStep>
		{:else if step === 2}
			<SignupStep>
				<label for="email">Введите ваш email</label>
				<input placeholder="Ваш email" name="email" type="email" bind:value={$form.mail} />
				{#if $errors.mail}
					<span class="invalid">
						{$errors.mail || 'Неправильно указана почта'}
					</span>
				{/if}
			</SignupStep>
		{:else if step === 3}
			<SignupStep>
				<label for="birthdate">Введите вашу дату рождения</label>
				<input name="birthdate" type="date" bind:value={$form.birthdate} />
				{#if $errors.birthdate}<span class="invalid">{$errors.birthdate}</span>{/if}
			</SignupStep>
		{:else if step === 4}
			<SignupStep>
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
			</SignupStep>
		{:else}
			<SignupStep>
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
			</SignupStep>
		{/if}
	</div>
	<Button {loading}>{step == 5 ? 'Зарегистрироваться' : 'Далее'}</Button>
</form>

<style lang="scss">
	header {
		display: flex;
		align-items: center;
		padding: 0 20px;
		height: 86px;
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

	.logo {
		:global(svg) {
			color: var(--primary);
			view-transition-name: logo;
			z-index: 1;
		}
	}

	form {
		display: flex;
		justify-content: space-between;
		flex-direction: column;
		align-items: center;
		margin: 0 20px 20px 20px;
	}

	.steps-container {
		display: grid;
		grid-template-columns: 1fr;
		grid-template-rows: 1fr;
	}

	input {
		border: 0;
		font-size: 32px;
		font-weight: 700;
		text-align: center;
		width: 80dvw;
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
		border: 1.5px solid var(--bg-gray);
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
		border: 1.5px solid #d3dfff;
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
