<script lang="ts">
	import Chip from '$lib/components/chip.svelte';
	import type { PageData } from './$types';
	import InterestsPopup from './../../../lib/components/interestsPopup.svelte';
	import Modal from './../../../lib/components/modal.svelte';
	export let interests: string[] = ['IT', 'Спорт', 'Технологии'];

	let showModal = false;
	export let data: PageData;
</script>

<Modal bind:showModal>
	<InterestsPopup />
</Modal>

<div class="header">
	<div class="profile-picture">
		<img src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg" alt="profile" />
	</div>
</div>
<div class="information">
	<div class="info-block">
		<label for="name">Имя</label><input value={data.name} name="name" type="text" />
	</div>
	<div class="info-block">
		<label for="bdate">День рождения</label><input
			value={data.birthdate}
			name="bdate"
			type="date"
		/>
	</div>
	<div class="info-block">
		<label for="occupation">Профессия</label><input
			value={data.occupation}
			name="occupation"
			type="text"
		/>
	</div>
	<div class="info-block">
		<label for="about">О себе</label><input name="about" value={data.about} type="text" />
	</div>
	<div class="info-block">
		<label for="interests">Интересы</label>
		<div class="interests" on:click={() => (showModal = true)}>
			{#each interests as interest}
				<Chip text={interest} />
			{/each}
		</div>
	</div>
</div>

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
		margin-top: 10px;
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
	}
</style>
