<script lang="ts">
	import Chip from './chip.svelte';
	import { page } from '$app/stores';
	import { selectedInterests } from '$lib/stores';

	let localSelectedInterests: number[] = $selectedInterests;

	function toggleOption(id: number) {
		if (localSelectedInterests.includes(id)) {
			localSelectedInterests = localSelectedInterests.filter((item) => item !== id);
		} else {
			localSelectedInterests = [...localSelectedInterests, id];
		}
	}
</script>

<div class="container">
	<h1>Интересы</h1>
	<div class="interests">
		{#each $page.data.interests as interest}
			<Chip
				clickable={true}
				active={localSelectedInterests.includes(interest.id)}
				id={interest.id}
				onClick={() => toggleOption(interest.id)}
				text={interest.interest_name}
			/>
		{/each}
	</div>
</div>

<style lang="scss">
	h1 {
		margin-bottom: 30px;
	}

	.container {
		border-radius: 40px 40px 0 0;
		background: #fff;
		align-items: center;
		display: flex;
		flex-direction: column;
		margin-bottom: 60px;
	}

	.interests {
		width: 100%;
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
	}
</style>
