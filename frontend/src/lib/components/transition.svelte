<script lang="ts">
	import { cubicOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';

	export let key: string | undefined;
	export let duration = 400;
</script>

{#key key}
	<div
		class:chats={key?.startsWith('/chats/')}
		in:fly={{ easing: cubicOut, duration: duration, x: -400 }}
		out:fly={{ easing: cubicOut, duration, x: 400 }}
	>
		<slot />
	</div>
{/key}

<style>
	div {
		padding: 0 20px;
		grid-row: 1;
		grid-column: 1;
		overflow-y: scroll;
		display: flex;
		flex-direction: column;
	}
	.chats {
		padding: 0;
	}
</style>
