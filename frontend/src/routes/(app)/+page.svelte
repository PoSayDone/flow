<script lang="ts">
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';
	import { getAge } from '$lib/utils';
	import { fade } from 'svelte/transition';
	import { superForm } from 'sveltekit-superforms';
	import { invalidateAll } from '$app/navigation';
	import type { PageData } from './$types';
	import { browser } from '$app/environment';
	import Skeleton from '$lib/components/skeleton.svelte';

	export let data: PageData;
	let isLoading = false;

	$: if (data.soulmates.length === 2 && data.shouldRefreshSoulmates) {
		invalidateAll();
	}

	$: currentCard = refs[0];
	let startX: number;
	let refs: HTMLAnchorElement[] = [];

	const { form, enhance, submit } = superForm(data.likeForm, {
		resetForm: false,
		clearOnSubmit: 'none',
		invalidateAll: false,
		onSubmit: ({ formData }) => {
			formData.set('user_id', $form.user_id);
			formData.set('like', String($form.like));
			isLoading = true;
		},
		onResult: () => {
			setTimeout(() => {
				isLoading = false;
			}, 500);
		}
	});

	const handleTouchStart = (event: TouchEvent) => {
		if (isLoading) return;
		startX = event.touches[0].clientX;
	};

	function handleTouchMove(event: TouchEvent) {
		if (isLoading) return;
		const deltaX = event.touches[0].clientX - startX;
		currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX / 10}deg)`;
	}

	function handleTouchEnd(event: TouchEvent) {
		if (isLoading) return;
		if (startX - event.changedTouches[0].clientX > 70) {
			handleDislike();
		} else if (startX - event.changedTouches[0].clientX < -70) {
			handleLike();
		} else {
			currentCard.style.transition = 'transform 0.3s ease-out';
			currentCard.style.transform = 'rotate(0deg) translateY(0%) translateX(0%)';
			setTimeout(() => {
				currentCard.style.transition = '';
				currentCard.style.transform = '';
			}, 300);
		}
	}

	function handleLike() {
		currentCard.style.transition = 'transform 0.3s ease-out';
		currentCard.style.transform = 'rotate(40deg) translateY(-50%) translateX(120%)';
		const interested_in = data.soulmates[0];
		if (interested_in) {
			$form.like = true;
			$form.user_id = interested_in.id;
			submit();
		}
		setTimeout(() => {
			currentCard.style.transition = '';
			currentCard.style.transform = '';
			data.soulmates.shift();
			data.soulmates = data.soulmates;
		}, 300);
	}

	function handleDislike() {
		currentCard.style.transition = 'transform 0.3s ease-out';
		currentCard.style.transform = 'rotate(-40deg) translateY(-50%) translateX(-120%)';
		const not_interested_in = data.soulmates[0];
		if (not_interested_in) {
			$form.like = false;
			$form.user_id = not_interested_in.id;
			submit();
		}
		setTimeout(() => {
			currentCard.style.transition = '';
			currentCard.style.transform = '';
			data.soulmates.shift();
			data.soulmates = data.soulmates;
		}, 300);
	}
</script>

{#if !browser}
	<Skeleton height="100%" width="100%" borderRadius="40px" margin="0 0 20px 0" />
{:else if data.soulmates.length == 0}
	<div class="placeholder" transition:fade>
		<p class="emoji">🥺</p>
		<p class="placeholder-text">Для вас пока нет сопутешественников</p>
	</div>
{:else}
	<form method="POST" use:enhance>
		<div
			class="cards"
			on:touchstart={handleTouchStart}
			on:touchend={handleTouchEnd}
			on:touchmove={handleTouchMove}
		>
			{#each data.soulmates as user, i}
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
					bind:node={refs[i]}
					bind:soulmates={data.soulmates}
				/>
			{/each}
		</div>
		<div class="actions">
			<ActionButton
				disabled={isLoading}
				type="button"
				action="dislike"
				on:click={() => handleDislike()}
			/>
			<ActionButton disabled={isLoading} type="button" action="chat" />
			<ActionButton
				disabled={isLoading}
				type="button"
				action="like"
				on:click={() => handleLike()}
			/>
		</div>
	</form>
{/if}

<style lang="scss">
	form {
		display: flex;
		flex-direction: column;
		height: 100%;
		gap: 15px;
		margin-bottom: 20px;
	}
	.placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		background: #f2f1f6;
		border-radius: 40px;
		gap: 12px;
		margin-bottom: 20px;
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
	}

	:root::view-transition-group(cards) {
		display: none;
	}
</style>
