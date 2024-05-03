<script lang="ts">
	export let disabled = false;
	let buttonProps = {
		class: [$$restProps.class],
		type: [$$restProps.type]
	};
</script>

<button
	on:click
	on:mouseover
	on:mouseenter
	on:mouseleave
	{...buttonProps}
	{disabled}
	aria-disabled={disabled}
>
	<slot />
</button>

<style>
	button {
		padding: 17px 0;
		width: 100%;
		border-radius: 20px;
		border: none;
		background-color: var(--primary);
		color: #efeff4;
		cursor: pointer;
		font-size: 18px;
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

	[aria-disabled='true'] {
		opacity: 0.5;
	}
</style>
