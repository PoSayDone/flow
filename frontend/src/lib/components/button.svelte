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

<style>
	button {
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

	button[aria-disabled='true'],
	button:disabled {
		opacity: 0.5;
	}

	.sticky {
		bottom: 0;
		position: sticky;
		position: -webkit-sticky;
		-webkit-box-shadow: 0px 0px 43px 23px rgba(255, 255, 255, 1);
		-moz-box-shadow: 0px 0px 43px 23px rgba(255, 255, 255, 1);
		box-shadow: 0px 0px 43px 23px rgba(255, 255, 255, 1);
	}
</style>
