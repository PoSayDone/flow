<script lang="ts">
	import Chip from './chip.svelte';
	import { closeCurrentDialog, status, submitCurrentDialog } from '$lib/stores';
	import Icon from '$lib/components/icon.svelte';
	import { departures, arrivals, tripPurposes } from '$lib/constants';
	import { backIcon } from '$lib/assets/Appicons';
	import { page } from '$app/stores';
	import Button from './button.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { tripPurposesRu } from '$lib/types';

	export let showModal;

	let departureSearch = '';
	let arrivalSearch = '';

	$: filteredDepartures = departures.filter((d) => d.name.includes(departureSearch));
	$: filteredArrivals = arrivals.filter((a) => a.name.includes(arrivalSearch));

	const { form, enhance, submit } = superForm($page.data.statusForm, {
		dataType: 'json',
		resetForm: false,
		clearOnSubmit: 'none',
		onChange: () => {
			if ($form.user_departures.includes(1)) {
				form.update((form) => {
					form.user_departures = [1];
					return form;
				});
			}
			if ($form.user_arrivals.includes(1)) {
				form.update((form) => {
					form.user_arrivals = [1];
					return form;
				});
			}
		},
		onResult: ({ result, cancel }) => {
			if (result.status == 204) {
				$closeCurrentDialog();
				status.set($form.user_status);
			}
			// Фиксит странный баг с рероутингом на профиль, не убирать
			cancel();
		}
	});

	let departuresActive: boolean = false;
	let arrivalsActive: boolean = false;

	function toggleOption(id: number) {
		if ($form.user_trip_purposes.includes(id)) {
			form.update((form) => {
				form.user_trip_purposes = form.user_trip_purposes.filter((item: number) => item !== id);
				return form;
			});
		} else {
			form.update((form) => {
				form.user_trip_purposes = [...form.user_trip_purposes, id];
				return form;
			});
		}
	}
	$: if (showModal) {
		submitCurrentDialog.set(submit);
	}
</script>

<form class:active={$form.user_status} method="POST" action="/profile/?/update_status" use:enhance>
	<div class="container">
		<h1>Выберите статус</h1>
		<div class="radios" role="radiogroup">
			<label class="radio" class:active={$form.user_status}>
				<div class="rows">
					<label class="radio-title" for="active">Активный</label>
					<label class="radio-subtitle" for="active"> Готов отправиться в путешествие </label>
				</div>
				<input type="radio" id="active" value={true} bind:group={$form.user_status} />
			</label>
			<div
				class="active-content"
				class:hidden={!$form.user_status}
				class:expand={departuresActive || arrivalsActive}
			>
				<button
					type="button"
					class="from"
					class:activebutton={departuresActive}
					on:click={() => {
						departuresActive = !departuresActive;
						arrivalsActive = false;
					}}
					>Откуда <Icon
						d={backIcon.d}
						viewBox={backIcon.viewBox}
						color="#000000"
						size="24px"
					/></button
				>
				<div class="location-form" class:shown={departuresActive}>
					<input class="search" type="text" bind:value={departureSearch} />
					<div>
						{#each filteredDepartures as { name, id }}
							<input
								type="checkbox"
								class="location-checkbox"
								bind:group={$form.user_departures}
								id={`departure_${id}`}
								value={id}
								disabled={($form.user_departures.length >= 3 &&
									!$form.user_departures.includes(id)) ||
									($form.user_departures.includes(1) && id != 1)}
							/>
							<label for={`departure_${id}`}>
								{name}
							</label>
						{/each}
					</div>
				</div>
				<button
					class="to"
					class:activebutton={arrivalsActive}
					on:click={() => {
						arrivalsActive = !arrivalsActive;
						departuresActive = false;
					}}
					type="button"
					>Куда <Icon
						d={backIcon.d}
						viewBox={backIcon.viewBox}
						color="#000000"
						size="24px"
					/></button
				>
				<div class="location-form" class:shown={arrivalsActive}>
					<input class="search" type="text" bind:value={arrivalSearch} />
					<div>
						{#each filteredArrivals as { name, id }}
							<input
								type="checkbox"
								class="location-checkbox"
								bind:group={$form.user_arrivals}
								id={`arrival_${id}`}
								value={id}
								disabled={($form.user_arrivals.length >= 3 && !$form.user_arrivals.includes(id)) ||
									($form.user_arrivals.includes(1) && id != 1)}
							/>
							<label for={`arrival_${id}`}>
								{name}
							</label>
						{/each}
					</div>
				</div>

				<div class="tags" class:shown={departuresActive == false && arrivalsActive == false}>
					{#each tripPurposes as trip_purpose}
						<Chip
							clickable={true}
							checked={$form.user_trip_purposes.includes(trip_purpose.id)}
							id={`trip_purpose_${trip_purpose.id}`}
							onClick={() => toggleOption(trip_purpose.id)}
							text={tripPurposesRu[trip_purpose.name]}
							disabled={$form.user_trip_purposes.length >= 3 &&
								!$form.user_trip_purposes.includes(trip_purpose.id)}
						/>
					{/each}
				</div>
			</div>

			<label class="radio" class:active={!$form.user_status}>
				<div class="rows">
					<label class="radio-title" for="inactive">Перерыв</label>
					<label class="radio-subtitle" for="inactive">Пока не путешествую</label>
				</div>
				<input type="radio" id="inactive" value={false} bind:group={$form.user_status} />
			</label>
		</div>
	</div>

	<Button type="submit" class="close-button" autofocus>
		<h2>Готово</h2>
	</Button>
</form>

<style lang="scss">
	h1 {
		margin-bottom: 30px;
	}

	form {
		display: flex;
		flex-direction: column;
		&.active {
			min-height: 75svh;
		}
	}

	input {
		padding: 10px;
	}

	.container {
		flex: 1;
		border-radius: 40px 40px 0 0;
		background: #fff;
		align-items: center;
		display: flex;
		flex-direction: column;
		margin-bottom: 60px;
	}

	.active-content {
		display: flex;
		height: min-content;
		flex-direction: column;
		gap: 5px;

		&.expand {
			height: 100%;
			flex: 1;
		}
	}

	.radios {
		display: flex;
		flex-direction: column;
		gap: 5px;
		width: 100%;
		height: 100%;
	}

	.location-form {
		display: none;
		flex-direction: column;
		gap: 10px;
		height: 250px;

		&.shown {
			display: flex;
			overflow-y: scroll;
			div {
				display: flex;
				gap: 10px;
				flex-direction: column;
			}
		}
		margin-bottom: 12px;
	}

	.location-checkbox {
		display: none;
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
		transition: all 0.1s ease-in-out;
	}

	.location-checkbox:checked + label::before {
		border-color: #0b76ef;
		background-color: #0b76ef;
		background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%23fff' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26 2.974 7.25 8 2.193z'/%3e%3c/svg%3e");
	}

	.location-checkbox:disabled + label {
		color: #999999;
	}
	.location-checkbox:disabled + label::before {
		border-color: #999999;
		background: none;
	}

	.search {
		min-height: 45px;
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
		color: #000;

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
		display: none;
		flex-wrap: wrap;
		gap: 5px;
		margin-bottom: 20px;
		&.shown {
			display: flex;
		}
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
		color: #000;

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

	@keyframes slide {
		from {
			transform: scaleY(1);
		}
		to {
			transform: scaleY(0);
		}
	}

	.hidden {
		display: none;
	}
</style>
