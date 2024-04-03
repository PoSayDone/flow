<script lang="ts">
	import { trip_purposes_binding } from '$lib/utils';
	import { users } from '$lib/stores';

	export let index: number = 0;
	export let id: string = '';
	export let trip_purposes: string[] = ['Горы', 'Море', 'Тусовки'];
	export let name: string = 'Никита';
	export let age: string = '18';
	export let occupation: string = 'Дизайнер';
	let href: string = `/user_${id}`;

	export let about: string =
		'\
        Я люблю путешествовать, потому что это позволяет мне познавать другие\
        культуры, открывать новые места и встречать интересных людей. Я уже\
        побывал во многих странах, но всегда готов к новым приключениям и\
        открытиям\
    ';

	let startX: number;
	let currentCard: HTMLDivElement;

	function handleTouchStart(event: TouchEvent) {
		startX = event.touches[0].clientX;
	}

	function handleTouchMove(event: TouchEvent) {
		const deltaX = event.touches[0].clientX - startX;
		currentCard.style.transform = `translateX(${deltaX}px) rotate(${deltaX / 10}deg)`;
	}
	function handleTouchEnd(event: TouchEvent) {
		currentCard.style.transition = 'transform 0.3s ease-out';

		if (startX - event.changedTouches[0].clientX > 70) {
			// Swipe left
			currentCard.style.transform = 'rotate(-40deg) translateY(-50%) translateX(-120%)';
			setTimeout(() => {
				currentCard.style.transition = '';
				currentCard.style.transform = '';
				users.update((array) => {
					array.shift();
					return array;
				});
			}, 300);
		} else if (startX - event.changedTouches[0].clientX < -70) {
			// Swipe right
			currentCard.style.transform = 'rotate(40deg) translateY(-50%) translateX(120%)';
			setTimeout(() => {
				currentCard.style.transition = '';
				currentCard.style.transform = '';
				users.update((array) => {
					const interested_in = array.shift().id;
					fetch(`http://localhost/api/match/${interested_in}`, { method: 'PUT' });
					return array;
				});
			}, 300);
		} else {
			currentCard.style.transform = 'rotate(0deg) translateY(0%) translateX(0%)';
			setTimeout(() => {
				currentCard.style.transition = '';
				currentCard.style.transform = '';
			}, 300);
		}
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
	style:z-index={$users.length - index}
>
	<div class="tags" style:view-transition-name={index == 0 ? `trip-purposes` : ''}>
		{#each trip_purposes as id}
			<div class="tag">{trip_purposes_binding[id]}</div>
		{/each}
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
		max-width: 380px;
		flex: 1;
		border-radius: 40px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		min-height: 100%;
		padding: 22px 40px;
		background: linear-gradient(0deg, rgba(0, 0, 0, 0) 70%, #000 100%),
			url(https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg);
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
		text-align: center;
		font-family: Inter;
		font-size: 24px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 24px */
		letter-spacing: -0.96px;
	}

	.subtitle {
		color: #dadada;
		text-align: center;
		font-family: 'PP Pangram Sans Rounded';
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
		font-family: Inter;
		font-size: 14px;
		font-style: normal;
		font-weight: 400;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.56px;
		text-wrap: wrap;
	}
</style>
