<script>
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';

	export let data;
</script>

<div class="cards">
		<UserCard name={data.users[0].name} about={data.users[0].about} occupation={data.users[0].occupation} />
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
		align-items: center;
		flex: 1;
		position: relative;
	}
	.actions {
    view-transition-name: actions;
		display: flex;
		width: 100%;
		justify-content: center;
		align-items: center;
		gap: 15px;
		margin: 10px 0 20px 0;
	}
</style>
