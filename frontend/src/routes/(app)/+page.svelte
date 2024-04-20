<script lang="ts">
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';
	import { getAge } from '$lib/utils';
	import { soulmates, topCard } from '$lib/stores';
	import { fade } from 'svelte/transition';

	export let data;
	if ($soulmates == undefined) {
		soulmates.set(data.soulmates);
	}
</script>

{#if $soulmates.length == 0}
	<div class="placeholder" transition:fade>
		<p class="emoji">🥺</p>
		<p class="placeholder-text">Для вас пока нет сопутешественников</p>
	</div>
{:else}
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
		<ActionButton type="dislike" on:click={() => $topCard.handleDislike()} />
		<ActionButton type="chat" />
		<ActionButton type="like" on:click={() => $topCard.handleLike()} />
	</div>
{/if}

<style lang="scss">
	.placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		flex: 1;
		background: #f2f1f6;
		border-radius: 40px;
		margin-bottom: 20px;
		gap: 12px;
		.emoji {
			font-size: 80px;
		}
	}
	.placeholder-text {
		font-weight: 600;
		text-align: center;
		font-size: 24px;
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
