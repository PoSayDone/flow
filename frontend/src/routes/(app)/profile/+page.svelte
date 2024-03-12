<script lang="ts">
	import { interests_binding } from '$lib/utils';
	import Chip from '$lib/components/chip.svelte';
	import InterestsPopup from '$lib/components/interestsPopup.svelte';
	import Modal from '$lib/components/modal.svelte';
	import { enhance, type SubmitFunction } from '$app/forms';
	import { onDestroy } from 'svelte';
	import { page } from '$app/stores';

	let showModal = false;
	let form: HTMLFormElement;

	let selectedInterests: string[] = [];
	try {
		if ($page.data.interests === undefined) {
			throw '';
		}
		if ($page.data.interests.length > 0) {
			selectedInterests = $page.data.interests;
		}
	} catch {
		selectedInterests = [];
	}

	const submitCreateNote: SubmitFunction = () => {
		return async ({ update }) => {
			await update({ reset: false });
		};
	};

	onDestroy(() => {
		if (form) {
			form.requestSubmit();
		}
	});
</script>

<Modal bind:showModal>
	<InterestsPopup bind:selectedInterests />
</Modal>

<div class="header">
	<div class="profile-picture">
		<img src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg" alt="profile" />
	</div>
</div>
<form bind:this={form} class="information" method="POST" use:enhance={submitCreateNote}>
	<div class="info-block">
		<label for="name">Имя</label>
		<input value={$page.data.name} name="name" type="text" on:blur={() => form.requestSubmit()} />
	</div>
	<div class="info-block">
		<label for="birthdate">День рождения</label>
		<input
			name="birthdate"
			type="date"
			value={$page.data.birthdate}
			on:blur={() => form.requestSubmit()}
		/>
	</div>
	<div class="info-block">
		<label for="occupation">Профессия</label>
		<input
			name="occupation"
			type="text"
			value={$page.data.occupation}
			on:blur={() => form.requestSubmit()}
		/>
	</div>
	<div class="info-block">
		<label for="about">О себе</label>
		<input name="about" type="text" value={$page.data.about} on:blur={() => form.requestSubmit()} />
	</div>
	<div class="info-block">
		<label for="interests">Интересы</label>
		<button type="button" class="interests" on:click={() => (showModal = true)}>
			{#if selectedInterests.length == 0 || selectedInterests == undefined}
				<Chip text={'Добавить интересы'} />
			{:else}
				{#each selectedInterests as id}
					<Chip text={interests_binding[id]} />
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

	.status {
		background: #f2f1f6;
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		height: 50px;
		padding: 13px;
		border-radius: 20px;
	}

	.status-title {
		text-align: center;
		font-family: Inter;
		font-size: 16px;
		font-style: normal;
		font-weight: 400;
		line-height: 120%; /* 19.2px */
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
