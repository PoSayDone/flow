<script>
	let buttonProps = {
		class: [$$restProps.class]
	};
</script>

<button on:click on:mouseover on:mouseenter on:mouseleave {...buttonProps}>
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

	.close-button {
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
	.opaque {
		background: none;
		color: #000;
	}
</style>
