<script lang="ts">
	import Chip from './chip.svelte';
	import { page } from '$app/stores';
	export let selectedInterests: number[] = [];

	function toggleOption(id: number) {
		if (selectedInterests.includes(id)) {
			selectedInterests = selectedInterests.filter((item) => item !== id);
			fetch(`http://localhost/api/user_interests/${id}`, {
				method: 'DELETE',
				credentials: 'include'
			});
		} else {
			selectedInterests = [...selectedInterests, id];
			fetch(`http://localhost/api/user_interests/${id}`, {
				method: 'PUT',
				credentials: 'include'
			});
		}
	}
</script>

<div class="container">
	<h1>Интересы</h1>
	<div class="interests">
		{#each $page.data.interests as interest}
			<Chip
				clickable={true}
				active={selectedInterests.includes(interest.id)}
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
