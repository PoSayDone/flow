<script lang="ts">
	import ActionButton from '$lib/components/actionButton.svelte';
	import UserCard from '$lib/components/userCard.svelte';
	import { getAge } from '$lib/utils';
	import { soulmates } from '$lib/stores';
	import { fade } from 'svelte/transition';
	import { superForm } from 'sveltekit-superforms';

	export let data;
	if ($soulmates == undefined) {
		soulmates.set(data.soulmates);
	}

	let startX: number;
	let refs: HTMLAnchorElement[] = [];

	const { form, enhance, submit } = superForm(data.likeForm, {
		resetForm: false,
		clearOnSubmit: 'none',
		onSubmit: ({ formData }) => {
			formData.set('user_id', $form.user_id);
			formData.set('like', String($form.like));
		},
		onResult: ({ result, cancel }) => {
			// Фиксит странный баг с рероутингом на профиль, не убирать
			cancel();
		}
	});
	$: currentCard = refs[0];

	const handleTouchStart = (event: TouchEvent) => {
		startX = event.touches[0].clientX;
	};

	function handleTouchMove(event: TouchEvent) {
		const deltaX = event.touches[0].clientX - startX;
		currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX / 10}deg)`;
	}

	function handleTouchEnd(event: TouchEvent) {
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
		setTimeout(() => {
			currentCard.style.transition = '';
			currentCard.style.transform = '';
			soulmates.update((array) => {
				const interested_in_id = array.shift()?.id;
				if (interested_in_id) {
					$form.like = true;
					$form.user_id = interested_in_id;
					submit();
				}
				return array;
			});
		}, 300);
	}

	function handleDislike() {
		currentCard.style.transition = 'transform 0.3s ease-out';
		currentCard.style.transform = 'rotate(-40deg) translateY(-50%) translateX(-120%)';
		setTimeout(() => {
			currentCard.style.transition = '';
			currentCard.style.transform = '';
			soulmates.update((array) => {
				const not_interested_in_id = array.shift()?.id;
				if (not_interested_in_id) {
					$form.user_id = not_interested_in_id;
					$form.like = false;
					submit();
				}
				return array;
			});
		}, 300);
	}
</script>

{#if $soulmates.length == 0}
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
					bind:node={refs[i]}
				/>
			{/each}
		</div>
		<div class="actions">
			<ActionButton type="button" action="dislike" on:click={() => handleDislike()} />
			<ActionButton type="button" action="chat" />
			<ActionButton type="button" action="like" on:click={() => handleLike()} />
		</div>
	</form>
{/if}

<style lang="scss">
	form {
		display: flex;
		flex-direction: column;
		flex: 1;
	}
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
