<script>
	import { addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	export let active = false;
	export let clickable = false;
	export let onClick = () => {}

	export let text = 'Активный отдых';

</script>

{#if clickable}
	<button class="chip clickable" class:active on:click={onClick}
		><span>{text}</span><Icon
			stroke_width={'1.5'}
			size={'16'}
			d={addIcon.d}
			viewBox={addIcon.viewBox}
		/></button
	>
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

		&.active {
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
	}
</style>
