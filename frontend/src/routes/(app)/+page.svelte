<script>
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';
	import { getAge } from '$lib/utils';
	import { soulmates } from '$lib/stores';

	export let data;
	if ($soulmates == undefined) {
		soulmates.set(data.soulmates);
	}
</script>

<form action="">
	<div class="cards">
		{#each $soulmates as user, i}
			<UserCard
				id={user.id}
				name={user.name}
				about={user.about}
				occupation={user.occupation}
				trip_purposes={user.trip_purposes}
				sex={user.sex}
				image_name={user.user_image}
				age={getAge(user.birthdate.toString()).toString()}
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
	form {
		height: 100%;
		display: flex;
		flex-direction: column;
		flex: 1;
	}
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
