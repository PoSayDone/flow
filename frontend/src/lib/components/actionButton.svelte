<script>
	import { dislikeIcon, likeIcon, writeIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';

	export let action = 'like';
	const types = {
		chat: writeIcon,
		like: likeIcon,
		dislike: dislikeIcon
	};
	const sizes = {
		chat: '25px',
		like: '22px',
		dislike: '18px'
	};

	let buttonProps = {
		type: $$restProps.type
	};
	export let disabled;
</script>

<button on:click class={action} {...buttonProps} {disabled} aria-disabled={disabled}>
	<Icon d={types[action].d} viewBox={types[action].viewBox} size={sizes[action]} />
</button>

<style lang="scss">
	button {
		width: 60px;
		height: 60px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 100%;
		border: none;
		background: #f2f1f6;
		transform: 0.3s all ease-in-out;
	}

	.like {
		transition: all 0.1s ease-in-out;
		:global(path) {
			transition: all 0.1s ease-in-out;
			fill: #ff44b4;
			stroke: none;
		}
		&:active {
			background: #ff44b4;
			:global(path) {
				fill: #f2f1f6;
				stroke: none;
			}
		}
	}

	.dislike {
		transition: all 0.1s ease-in-out;
		:global(path) {
			transition: all 0.1s ease-in-out;
			stroke: #f14444;
		}
		&:active {
			background: #f14444;
			:global(path) {
				stroke: #f2f1f6;
			}
		}
	}

	.chat {
		background: var(--primary);
	}

	[aria-disabled='true'] {
		opacity: 0.5;
	}
</style>
