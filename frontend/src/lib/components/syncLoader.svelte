<script lang="ts">
	const durationUnitRegex = /[a-zA-Z]/;
	const range = (size: number, startAt = 0) => [...Array(size).keys()].map((i) => i + startAt);

	export let color = '#FF3E00';
	export let unit = 'px';
	export let duration = '0.6s';
	export let size: number = 60;
	let durationUnit: string = duration.match(durationUnitRegex)?.[0] ?? 's';
	let durationNum: string = duration.replace(durationUnitRegex, '');
</script>

<div class="wrapper" style="--size:{size}{unit}; --duration: {duration};">
	{#each range(3, 1) as i}
		<div
			class="dot"
			style="--dotSize:{+size * 0.25}{unit}; --color:{color}; animation-delay:  {i *
				(+durationNum / 10)}{durationUnit};"
		/>
	{/each}
</div>

<style>
	.wrapper {
		height: var(--size);
		width: var(--size);
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4px;
	}

	.dot {
		height: var(--dotSize);
		width: var(--dotSize);
		background-color: var(--color);
		display: inline-block;
		border-radius: 100%;
		animation: sync var(--duration) ease-in-out infinite alternate both running;
	}

	@-webkit-keyframes sync {
		33% {
			-webkit-transform: translateY(3px);
			transform: translateY(3px);
		}
		66% {
			-webkit-transform: translateY(-3px);
			transform: translateY(-3px);
		}
		100% {
			-webkit-transform: translateY(0);
			transform: translateY(0);
		}
	}
	@keyframes sync {
		33% {
			-webkit-transform: translateY(3px);
			transform: translateY(3px);
		}
		66% {
			-webkit-transform: translateY(-3px);
			transform: translateY(-3px);
		}
		100% {
			-webkit-transform: translateY(0);
			transform: translateY(0);
		}
	}
</style>
