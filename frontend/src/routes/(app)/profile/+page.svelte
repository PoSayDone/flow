<script lang="ts">
	import { interests_binding } from '$lib/utils';
	import Chip from '$lib/components/chip.svelte';
	import { page } from '$app/stores';
	import { selectedInterests } from '$lib/stores';
	import { superForm } from 'sveltekit-superforms';
	import { interestsRu } from '$lib/types';
	import Indicator from '$lib/components/indicator.svelte';
	import Icon from '$lib/components/icon.svelte';
	import { backIcon, editIcon } from '$lib/assets/Appicons';
	import type { PageData } from './$types';
	import Avatar from '$lib/components/avatar.svelte';
	import Button from '$lib/components/button.svelte';
	import { toast } from '@zerodevx/svelte-toast';
	import { browser } from '$app/environment';
	import Skeleton from '$lib/components/skeleton.svelte';
	import { enhance as svelteEnhance } from '$app/forms';
	import { showStatusModal, showInterestsModal, showAvatarModal } from '$lib/stores';

	let loading = false;

	export let data: PageData;

	if ($selectedInterests.length == 0) {
		if ($page.data.user.interests !== undefined) {
			selectedInterests.set($page.data.user.interests);
		}
	}

	const { form, enhance } = superForm($page.data.profileForm, {
		resetForm: false,
		clearOnSubmit: 'none',
		onSubmit: () => {
			loading = true;
		},
		onResult: ({ result }) => {
			loading = false;
			if (result.status == 204) {
				toast.push('Данные обновлены');
				initialForm = $form;
			} else {
				toast.push('Что-то пошло не так');
				$form = initialForm;
			}
		}
	});

	let initialForm = { ...$form };

	$: isNotEdited =
		initialForm.name == $form.name &&
		initialForm.occupation == $form.occupation &&
		initialForm.about == $form.about &&
		initialForm.birthdate == $form.birthdate;
</script>

<svelte:head>
	<meta
		name="viewport"
		content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no interactive-widget=resizes-visual"
	/>
</svelte:head>

<div class="header">
	<button class="avatar-container" on:click={() => ($showAvatarModal = true)}>
		<Avatar size="128px" user={data.user} />
		<div class="avatar-icon">
			<Icon
				viewBox={editIcon.viewBox}
				d={editIcon.d}
				stroke_width={'1'}
				size={'14'}
				color={'#2461FF'}
			/>
		</div>
	</button>
</div>

<button class="status" on:click={() => ($showStatusModal = true)}>
	Статус
	{#if browser}
		<div class="status-data">
			<Indicator />
			<Icon
				viewBox={backIcon.viewBox}
				d={backIcon.d}
				stroke_width={'2'}
				size={'20'}
				color={'#000'}
			/>
		</div>
	{:else}
		<Skeleton width="120px" height="20px" />
	{/if}
</button>

<form id="logout_form" action="?/logout" method="POST" use:svelteEnhance></form>

<form id="profile_form" class="information" method="POST" action="?/update_profile" use:enhance>
	<div class="info-block">
		<label for="name">Имя</label>
		<input name="name" type="text" bind:value={$form.name} />
	</div>
	<div class="info-block">
		<label for="birthdate">День рождения</label>
		<input class="input-bdate" name="birthdate" type="date" bind:value={$form.birthdate} />
	</div>
	<div class="info-block">
		<label for="occupation">Профессия</label>
		<input name="occupation" type="text" bind:value={$form.occupation} />
	</div>
	<div class="info-block">
		<label for="about">О себе</label>
		<input name="about" type="text" bind:value={$form.about} />
	</div>
	<div class="info-block">
		<label for="interests">Интересы</label>
		<button type="button" class="interests" on:click={() => ($showInterestsModal = true)}>
			{#if browser}
				{#if $selectedInterests.length == 0 || $selectedInterests == undefined}
					<Chip text={'Добавить интересы'} />
				{:else}
					{#each $selectedInterests as id}
						<Chip id={`interest_${id}`} text={interestsRu[interests_binding[id]]} />
					{/each}
				{/if}
			{:else}
				<Skeleton height="36px" width="160px" />
				<Skeleton height="36px" width="80px" />
				<Skeleton height="36px" width="120px" />
			{/if}
		</button>
	</div>
	<Button form="logout_form" class="logout top-auto" type="submit" on:click={() => {}}
		>Выйти из аккаунта</Button
	>
	<Button
		form="profile_form"
		class="sticky"
		style="bottom: 20px;"
		{loading}
		bind:disabled={isNotEdited}>Подтвердить</Button
	>
</form>

<style lang="scss">
	.header {
		margin-top: 20px;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
	}

	.avatar-container {
		position: relative;
		.avatar-icon {
			position: absolute;
			bottom: 0px;
			right: 6px;
			box-shadow: 0px 4px 14px 0px #0000001f;
			background: #fff;
			display: flex;
			align-items: center;
			justify-content: center;
			border-radius: 100%;
			width: 28px;
			height: 28px;
		}
	}

	.status {
		display: flex;
		width: 100%;
		align-items: center;
		justify-content: space-between;
		padding: 16px 13px;
		color: #000;
		background: #f2f1f6;
		border-radius: 20px;
		margin-top: 20px;
	}

	.status-data {
		align-items: center;
		display: flex;
		gap: 6px;
		:global(svg) {
			transform: rotate(180deg);
		}
	}

	.information {
		margin: 20px 0;
		display: flex;
		flex: 1;
		flex-direction: column;
		gap: 15px;
	}

	.info-block {
		display: flex;
		flex-direction: column;
		color: #000;

		input {
			border: none;
			border-radius: 0;
			border-bottom: 1px solid var(--fg-gray);
			padding: 10px 0;
			font-family: 'PP Pangram Sans Rounded';
			font-size: 18px;
			font-style: normal;
			font-weight: 600;
			line-height: 100%; /* 18px */
			letter-spacing: -0.27px;
		}
		input[type='date'] {
			width: 100%;
			text-align: left;
			color: #000;
			background: transparent;
		}
		input::-webkit-date-and-time-value {
			text-align: left;
		}
	}

	label {
		font-family: Inter;
		font-size: 12px;
		font-style: normal;
		font-weight: 400;
		line-height: 100%; /* 12px */
		letter-spacing: -0.48px;
		margin-bottom: 5px;
	}

	.interests {
		background: none;
		margin-top: 10px;
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
	}

	.buttons {
		display: flex;
		flex-direction: column;
		gap: 12px;
		margin-bottom: 20px;
	}
</style>
