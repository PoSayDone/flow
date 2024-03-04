<script lang="ts">
	import Chip from './chip.svelte';
	
	async function getInterests() {
		const res = await fetch('http://localhost/api/interests');
		const values = await res.json();
		return values;
	}

	export let selectedOptions: string[];

	function toggleOption(id: string) {
    if (selectedOptions.includes(id)) {
      selectedOptions = selectedOptions.filter((item) => item !== id);
    } else {
      selectedOptions = [...selectedOptions, id];
			fetch('http://localhost/api/user_interests/id', {method:'PUT'});
    }
  }

	let interestsPromise = getInterests();

</script>

<div class="container">
	<h1>Интересы</h1>
	<div class="interests">
		{#await interestsPromise then fetched_data }
			{#each fetched_data as interest}
				<Chip
					clickable={true}
					active={selectedOptions.includes(interest.id)} 
					onClick={() => toggleOption(interest.id)}
					text = {interest.interest_name}
				/>
			{/each}
		{:catch error}
			<p style="color: red">{error.message}</p>
		{/await}
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
	}

	.interests {
		width: 100%;
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
	}
</style>
