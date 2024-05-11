<script lang="ts">
	import SyncLoader from '$lib/components/syncLoader.svelte';

	export let disabled = false;
	export let loading = false;
</script>

<button {...$$restProps} on:click disabled={loading || disabled} aria-disabled={disabled}>
	{#if loading}
		<SyncLoader size={30} color="#efeff4"></SyncLoader>
	{:else}
		<slot />
	{/if}
</button>

<style lang="scss">
	button {
		flex-shrink: 0;
		height: 56px;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		border-radius: 20px;
		border: none;
		background-color: var(--primary);
		color: #efeff4;
		cursor: pointer;
		font-size: 18px;
		transition: 0.3s all ease-in-out;
		&[aria-disabled='true'] {
			background: var(--disabled-bg);
			color: var(--disabled-fg);
		}
	}

	.white {
		background: #fff;
		color: var(--primary);
	}

	.border {
		background: none;
		border: 1px solid #fff;
		color: #fff;
	}

	.top-auto {
		margin-top: auto;
	}

	.opaque {
		background: none;
		color: #000;
	}

	.sticky {
		bottom: 0;
		position: sticky;
		position: -webkit-sticky;
	}

	.logout {
		font-size: 16px;
		background: none;
		color: var(--red);
		border: 1px solid var(--red);
		text-align: start;
	}
</style>
