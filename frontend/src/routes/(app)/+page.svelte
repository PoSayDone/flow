<script>
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';

	export let data;
</script>

<div class="cards">
	{#each data.body as user}
		<UserCard name={user.name} about={user.about} occupation={user.occupation} />
	{/each}
</div>
<div class="actions">
	<ActionButton type="dislike" />
	<ActionButton type="chat" />
	<ActionButton type="like" />
</div>

<style>
	.cards {
		display: flex;
		flex-direction: column;
		flex: 1;
		position: relative;
	}
	.actions {
		display: flex;
		width: 100%;
		justify-content: center;
		align-items: center;
		gap: 15px;
		margin: 10px 0 20px 0;
	}
</style>
