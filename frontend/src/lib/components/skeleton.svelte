<script lang="ts">
	export let borderRadius = '20px';
	export let width = '20px';
	export let height = '20px';
	export let margin = '0px';
</script>

<div class="skeleton" style:border-radius={borderRadius} style:width style:height style:margin>
	<slot />
</div>

<style lang="scss">
	.skeleton {
		background: var(--bg-gray);
		position: relative;
	}

	.skeleton::before {
		content: '';
		display: block;
		height: 100%;
		width: 100%;
		background: linear-gradient(90deg, transparent, #ffffff38, transparent);
		position: absolute;
		top: 0;
		left: 0;
		animation: skeleton-animation 1.2s linear infinite;
	}

	@keyframes skeleton-animation {
		0% {
			transform: translateX(-100%);
		}
		100% {
			transform: translateX(100%);
		}
	}
</style>
