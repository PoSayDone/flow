<script lang="ts">
	import { interests_binding } from '$lib/utils';
	import Chip from '$lib/components/chip.svelte';
	import InterestsPopup from '$lib/components/interestsPopup.svelte';
	import Modal from '$lib/components/modal.svelte';
	import { page } from '$app/stores';
	import { selectedInterests } from '$lib/stores';
	import { superForm } from 'sveltekit-superforms';
	import { interestsRu } from '$lib/types';

	let showModal = false;

	if ($selectedInterests.length == 0) {
		if ($page.data.user.interests !== undefined) {
			selectedInterests.set($page.data.user.interests);
		}
	}

	const { form, enhance, submit } = superForm($page.data.profileForm, {
		resetForm: false,
		clearOnSubmit: 'none'
	});
</script>

<Modal bind:showModal>
	<InterestsPopup />
</Modal>

<div class="header">
	<div class="profile-picture">
		<img src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg" alt="profile" />
	</div>
</div>

<form class="information" method="POST" action="?/update_profile" use:enhance>
	<div class="info-block">
		<label for="name">Имя</label>
		<input name="name" type="text" bind:value={$form.name} on:blur={() => submit()} />
	</div>
	<div class="info-block">
		<label for="birthdate">День рождения</label>
		<input name="birthdate" type="date" bind:value={$form.birthdate} on:blur={() => submit()} />
	</div>
	<div class="info-block">
		<label for="occupation">Профессия</label>
		<input name="occupation" type="text" bind:value={$form.occupation} on:blur={() => submit()} />
	</div>
	<div class="info-block">
		<label for="about">О себе</label>
		<input name="about" type="text" bind:value={$form.about} on:blur={() => submit()} />
	</div>
	<div class="info-block">
		<label for="interests">Интересы</label>
		<button type="button" class="interests" on:click={() => (showModal = true)}>
			{#if $selectedInterests.length == 0 || $selectedInterests == undefined}
				<Chip text={'Добавить интересы'} />
			{:else}
				{#each $selectedInterests as id}
					<Chip id={`interest_${id}`} text={interestsRu[interests_binding[id]]} />
				{/each}
			{/if}
		</button>
	</div>
</form>

<style lang="scss">
	.header {
		width: 100%;
		margin-top: 10px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 20px;
	}

	.profile-picture {
		width: 130px;
		height: 130px;
		border-radius: 100%;
		overflow: hidden;
		img {
			height: 100%;
		}
	}

	.information {
		margin-top: 20px;
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	.info-block {
		display: flex;
		flex-direction: column;
		input {
			border: none;
			border-bottom: 1px solid var(--fg-gray);
			padding: 10px 0;
			font-family: 'PP Pangram Sans Rounded';
			font-size: 18px;
			font-style: normal;
			font-weight: 600;
			line-height: 100%; /* 18px */
			letter-spacing: -0.27px;
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
</style>
