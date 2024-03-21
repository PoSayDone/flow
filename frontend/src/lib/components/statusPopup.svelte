<script lang="ts">
	import Chip from './chip.svelte';
	import { status } from '$lib/stores';
	import Icon from '$lib/components/icon.svelte';
	import { backIcon } from '$lib/assets/Appicons';
	import { page } from '$app/stores';

	let fromActive: boolean = false;
	let toActive: boolean = false;

	let selectedOptions: string[] = [];
	try {
		if ($page.data.user_trip_purposes === undefined) {
			throw '';
		}
		if ($page.data.user_trip_purposes.length > 0) {
			selectedOptions = $page.data.user_trip_purposes;
		}
	} catch {
		selectedOptions = [];
	}

	function toggleOption(id: string) {
		if (selectedOptions.includes(id)) {
			selectedOptions = selectedOptions.filter((item) => item !== id);
			fetch(`http://localhost/api/user_trip_purposes/${id}`, {
				method: 'DELETE',
				credentials: 'include'
			});
		} else {
			selectedOptions = [...selectedOptions, id];
			fetch(`http://localhost/api/user_trip_purposes/${id}`, {
				method: 'PUT',
				credentials: 'include'
			});
		}
	}
</script>

<div class="container" class:container-active={$status == 'active'}>
	<h1>Выберите статус</h1>
	<div class="radios" role="radiogroup">
		<label class="radio" class:active={$status == 'active'}>
			<div class="rows">
				<label class="radio-title" for="active">Активный</label>
				<label class="radio-subtitle" for="active"> Готов отправиться в путешествие </label>
			</div>
			<input type="radio" id="active" value="active" bind:group={$status} />
		</label>
		{#if $status == 'active'}
			<button
				type="button"
				class="from"
				class:activebutton={fromActive}
				on:click={() => (fromActive = !fromActive)}
				>Откуда <Icon
					d={backIcon.d}
					viewBox={backIcon.viewBox}
					color="#000000"
					size="24px"
				/></button
			>
			{#if fromActive == true}
				<div class="city-form">
					<input class="search" type="text" />
					{#each $page.data.departures as departure}
						<input
							class="location-checkbox"
							type="checkbox"
							name={`departure_${departure.id}`}
							id={`departure_${departure.id}`}
						/>
						<label for={`departure_${departure.id}`}>
							{departure.location_name}
						</label>
					{/each}
				</div>
			{/if}
			<button class="to" on:click={() => (toActive = !toActive)} type="button"
				>Куда <Icon d={backIcon.d} viewBox={backIcon.viewBox} color="#000000" size="24px" /></button
			>
			{#if toActive == true}
				<div class="city-form">
					<input class="search" type="text" />
					{#each $page.data.arrivals as arrival}
						<input
							class="location-checkbox"
							type="checkbox"
							name={`arrival_${arrival.id}`}
							id={`arrival_${arrival.id}`}
						/>
						<label for={`arrival_${arrival.id}`}>
							{arrival.location_name}
						</label>
					{/each}
				</div>
			{/if}

			{#if fromActive == false && toActive == false}
				<div class="tags">
					{#each $page.data.trip_purposes as trip_purpose}
						<Chip
							clickable={true}
							active={selectedOptions.includes(trip_purpose.id)}
							id={`trip_purpose_${trip_purpose.id}`}
							onClick={() => toggleOption(trip_purpose.id)}
							text={trip_purpose.purpose_name}
						/>
					{/each}
				</div>
			{/if}
		{/if}

		{#if fromActive == false && toActive == false}
			<label class="radio" class:active={$status == 'inactive'}>
				<div class="rows">
					<label class="radio-title" for="inactive">Перерыв</label>
					<label class="radio-subtitle" for="inactive">Пока не путешествую</label>
				</div>
				<input type="radio" id="inactive" value="inactive" bind:group={$status} />
			</label>
		{/if}
	</div>
</div>

<style lang="scss">
	h1 {
		margin-bottom: 30px;
	}

	.container {
		border-radius: 40px 40px 0 0;
		background: #fff;
		align-items: center;
		display: flex;
		flex-direction: column;
		margin-bottom: 60px;
	}

	.container-active {
		margin-bottom: 8px;
		height: 75svh;
	}

	.radios {
		display: flex;
		flex-direction: column;
		gap: 5px;
		width: 100%;
		height: 100%;
	}

	.city-form {
		display: flex;
		overflow-y: scroll;
		flex-direction: column;
		gap: 10px;
		flex: 1;
	}

	.location-checkbox {
		position: absolute;
		z-index: -1;
		opacity: 0;
	}

	.location-checkbox + label {
		margin: 0 17px;
		display: inline-flex;
		align-items: center;
		user-select: none;
		gap: 5px;
		font-size: 16px;
		font-weight: 600;
	}

	.location-checkbox + label::before {
		content: '';
		display: inline-block;
		width: 25px;
		height: 25px;
		flex-shrink: 0;
		flex-grow: 0;
		border: 1px solid #adb5bd;
		border-radius: 5px;
		background-repeat: no-repeat;
		background-position: center center;
		background-size: 50% 50%;
	}

	.location-checkbox:checked + label::before {
		border-color: #0b76ef;
		background-color: #0b76ef;
		background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%23fff' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26 2.974 7.25 8 2.193z'/%3e%3c/svg%3e");
	}

	.search {
		height: 45px;
		display: flex;
		align-items: center;
		border: 1px solid #aaaaaa;
		border-radius: 15px;
	}

	.from {
		margin-top: 5px;
	}
	.to {
		margin-bottom: 5px;
	}

	.from,
	.to {
		background-color: #f2f1f6;
		width: 100%;
		border: none;
		border-radius: 20px;
		padding: 15px 20px;
		display: flex;
		justify-content: space-between;
		align-items: center;

		:global(svg) {
			transform: rotate(180deg);
		}
	}

	.activebutton {
		:global(svg) {
			transform: rotate(270deg);
		}
	}

	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
		margin-bottom: 20px;
	}

	.radio {
		background-color: #f2f1f6;
		width: 100%;
		border: none;
		border-radius: 20px;
		padding: 15px 20px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;

		&.active {
			background-color: #d3dfff;
			color: var(--primary);
		}
	}

	.radio-title {
		font-family: 'PP Pangram Sans Rounded';
		font-size: 18px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 18px */
		letter-spacing: -0.27px;
	}

	.radio-subtitle {
		font-family: 'PP Pangram Sans Rounded';
		font-size: 14px;
		font-style: normal;
		font-weight: 500;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.56px;
	}

	.rows {
		align-items: start;
		display: flex;
		flex-direction: column;
	}

	input[type='radio'] {
		appearance: none;
		background-color: #fff;
		margin: 0;

		font: inherit;
		color: currentColor;
		width: 20px;
		height: 20px;
		border: 1.5px solid #eeedf2;
		border-radius: 50%;
		transform: translateY(-0.075em);

		display: grid;
		place-content: center;
	}

	input[type='radio']::before {
		content: '';
		width: 10px;
		height: 10px;
		border-radius: 50%;
		transform: scale(0);
		transition: 120ms transform ease-in-out;
		box-shadow: inset 1em 1em var(--form-control-color);
		/* Windows High Contrast Mode */
		background-color: var(--primary);
	}

	input[type='radio']:checked::before {
		transform: scale(1);
	}
</style>
