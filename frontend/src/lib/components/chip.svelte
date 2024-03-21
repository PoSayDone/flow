<script lang="ts">
	import { addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	export let clickable = false;
	export let onClick = () => {};

	export let active: boolean = false;
	export let id: string = 'undefined';
	export let text = 'Активный отдых';
</script>

{#if clickable}
	<input class="chip" class:clickable type="checkbox" {id} name={id} bind:checked={active} />
	<label for={id}>
		<span>{text}</span>
		<Icon stroke_width={'1.5'} size={'16'} d={addIcon.d} viewBox={addIcon.viewBox} />
	</label>
{:else}
	<div class="chip">
		<span>{text}</span>
	</div>
{/if}

<style lang="scss">
	.chip {
		display: flex;
		align-items: center;
		justify-content: center;
		width: min-content;
		height: 36px;
		padding: 0 18px;
		border-radius: 100px;
		background: none;
		outline: 1.5px solid var(--bg-gray);
		border: none;
		cursor: pointer;
		transition: all 0.1s ease-in-out;

		span {
			text-wrap: nowrap;
		}
	}

	.chip.clickable {
		display: none;
	}

	.chip.clickable + label {
		display: flex;
		align-items: center;
		justify-content: center;
		width: min-content;
		height: 36px;
		padding: 0 18px;
		border-radius: 100px;
		background: none;
		outline: 1.5px solid var(--bg-gray);
		border: none;
		cursor: pointer;
		transition: all 0.1s ease-in-out;
		span {
			text-wrap: nowrap;
			margin-right: 10px;
		}

		:global(path) {
			transition: all 0.1s ease-in-out;
			stroke: #000;
		}

		:global(svg) {
			transition: all 0.1s ease-in-out;
		}
	}

	.chip.clickable:checkd + label {
		background: #d3dfff;
		color: #2461ff;
		outline: none;
		:global(path) {
			stroke: #2461ff;
		}
		:global(svg) {
			transform: rotate(45deg);
		}
	}

	input[type='checkbox']:checked + label {
		background: #d3dfff;
		color: #2461ff;
		outline: none;
		:global(path) {
			stroke: #2461ff;
		}
		:global(svg) {
			transform: rotate(45deg);
		}
	}
</style>
