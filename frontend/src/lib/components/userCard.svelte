<script lang="ts">
	import { images_url, placeholder, trip_purposes_binding } from '$lib/utils';
	import { soulmates } from '$lib/stores';
	import { tripPurposesRu } from '$lib/types';

	export let index: number = 0;
	export let id: string = '';
	export let trip_purposes: number[] = [1, 2, 3];
	export let name: string = 'Никита';
	export let image_name: string;
	export let age: string = '18';
	export let occupation: string = 'Дизайнер';
	export let sex: boolean | null = null;
	export let node;
	$: href = `/user_${id}`;

	export let about: string =
		'\
        Я люблю путешествовать, потому что это позволяет мне познавать другие\
        культуры, открывать новые места и встречать интересных людей. Я уже\
        побывал во многих странах, но всегда готов к новым приключениям и\
        открытиям\
    ';
</script>

<a
	on:touchstart
	on:touchmove
	on:touchend
	on:touchcancel
	class="card"
	bind:this={node}
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
			{#if occupation}
				<span class="subtitle">{occupation}</span>
			{/if}
		</div>
		<div>
			{#if about}
				<p class="text">
					{about}
				</p>
			{/if}
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
