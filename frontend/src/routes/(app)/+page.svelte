<script>
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';
	import { getAge } from '$lib/utils';
	import { users } from '$lib/stores';

	export let data;
	if ($users == undefined) {
		users.set(data.users);
	}
</script>

<form action="">
	<div class="cards">
		{#each $users as user, i}
			<UserCard
				id={user.id}
				name={user.name}
				about={user.about}
				occupation={user.occupation}
				trip_purposes={user.trip_purposes}
				age={getAge(user.birthdate)}
				index={i}
			/>
		{/each}
	</div>
	<div class="actions">
		<ActionButton type="dislike" />
		<ActionButton type="chat" />
		<ActionButton type="like" />
	</div>
</form>

<style lang="scss">
	.cards {
		view-transition-name: cards;
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 1;
		display: grid;
		grid-template-columns: 1fr;
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

	:root::view-transition-group(cards) {
		display: none;
	}
</style>
