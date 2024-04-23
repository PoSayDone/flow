<script lang="ts">
	import { api_url, images_url, placeholder, trip_purposes_binding } from '$lib/utils';
	import { soulmates, topCard } from '$lib/stores';
	import { tripPurposesRu } from '$lib/types';

	export let index: number = 0;
	export let id: string = '';
	export let trip_purposes: number[] = [1, 2, 3];
	export let name: string = 'Никита';
	export let image_name: string;
	export let age: string = '18';
	export let occupation: string = 'Дизайнер';
	export let sex: boolean | null = null;
	$: href = `/user_${id}`;

	export let about: string =
		'\
        Я люблю путешествовать, потому что это позволяет мне познавать другие\
        культуры, открывать новые места и встречать интересных людей. Я уже\
        побывал во многих странах, но всегда готов к новым приключениям и\
        открытиям\
    ';

	let startX: number;
	let currentCard: HTMLAnchorElement;

	function handleTouchStart(event: TouchEvent) {
		startX = event.touches[0].clientX;
	}

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

	$: if (index == 0) {
		topCard.set({ handleLike, handleDislike });
	}

	function handleLike() {
		currentCard.style.transition = 'transform 0.3s ease-out';
		currentCard.style.transform = 'rotate(40deg) translateY(-50%) translateX(120%)';
		setTimeout(() => {
			currentCard.style.transition = '';
			currentCard.style.transform = '';
			soulmates.update((array) => {
				const interested_in_id = array.shift().id;
				fetch(`${api_url}/user/like/${interested_in_id}`, { method: 'POST' });
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
				const not_interested_in_id = array.shift().id;
				fetch(`${api_url}/user/dislike/${not_interested_in_id}`, { method: 'POST' });
				return array;
			});
		}, 300);
	}
</script>

<a
	bind:this={currentCard}
	class="card"
	on:touchstart={handleTouchStart}
	on:touchmove={handleTouchMove}
	on:touchend={handleTouchEnd}
	on:touchcancel={handleTouchEnd}
	{href}
	style:view-transition-name={index == 0 ? 'profile-image' : ''}
	style:z-index={$soulmates.length - index}
	style="--user-image: url({images_url}/{image_name || placeholder(sex)});"
>
	<div class="tags" style:view-transition-name={index == 0 ? `trip-purposes` : ''}>
		{#if trip_purposes}
			{#each trip_purposes as id}
				<div class="tag">{tripPurposesRu[trip_purposes_binding[id]]}</div>
			{/each}
		{/if}
	</div>
	<div class="body">
		<div class="heading">
			<div class="title-container">
				<span class="title">{name}</span>
				<span class="title">{age}</span>
			</div>
			<span class="subtitle">{occupation}</span>
		</div>
		<div>
			<p class="text">
				{about}
			</p>
		</div>
	</div>
</a>

<style lang="scss">
	.card {
		grid-row-start: 1;
		grid-column-start: 1;
		align-items: center;
		z-index: auto;
		width: 100%;
		flex: 1;
		border-radius: 40px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-height: 100%;
		padding: 22px 40px;
		background: radial-gradient(rgba(0, 0, 0, 0) 30%, rgba(0, 0, 0, 0.6) 100%), var(--user-image),
			#d6d6d6;
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;
	}

	.tags {
		width: fit-content;
		display: inline-flex;
		flex-wrap: wrap;
		justify-content: center;
		align-items: center;
		gap: 5px;
	}

	.tag {
		border-radius: 20px;
		border: 1px solid #fff;

		display: flex;
		padding: 5px 10px;
		justify-content: center;
		align-items: center;
		gap: 10px;

		color: #fff;
		font-family: 'PP Pangram Sans Rounded';
		font-size: 14px;
		font-style: normal;
		font-weight: 500;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.56px;
	}

	.body {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 10px;
		flex-shrink: 0;
	}

	.heading {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 5px;
	}

	.title-container {
		display: inline-flex;
		gap: 8px;
	}

	.title {
		color: #fff;
		font-size: 24px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 24px */
		letter-spacing: -0.96px;
	}

	.subtitle {
		color: #dadada;
		font-size: 18px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 18px */
		letter-spacing: -0.27px;
		margin: 0;
	}

	.text {
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 3; /* number of lines to show */
		line-clamp: 3;
		-webkit-box-orient: vertical;
		margin: 0;
		color: #fff;
		font-size: 14px;
		font-style: normal;
		font-weight: 400;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.56px;
		text-wrap: wrap;
	}
</style>
