<script lang="ts">
	import { page } from '$app/stores';
	import { onDestroy, onMount } from 'svelte';
	import type { PageData } from './$types';
	import { pusherClient } from '$lib/pusher';
	import { invalidateAll } from '$app/navigation';
	import Avatar from '$lib/components/avatar.svelte';
	import { browser } from '$app/environment';
	import Skeleton from '$lib/components/skeleton.svelte';

	export let data: PageData;

	const newHandler = () => {
		invalidateAll();
	};
	const updateHandler = () => {
		invalidateAll();
	};

	onMount(() => {
		pusherClient.subscribe($page.data.user.mail);
		pusherClient.bind('conversation:new', newHandler);
		pusherClient.bind('message:new', updateHandler);
	});

	onDestroy(() => {
		pusherClient.unsubscribe($page.data.user.mail);
		pusherClient.unbind('conversation:new', newHandler);
		pusherClient.unbind('message:new', updateHandler);
	});
</script>

<svelte:head>
	<meta
		name="viewport"
		content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no interactive-widget=resizes-content"
	/>
</svelte:head>

<div class="chats">
	{#if !browser}
		<div class="chat">
			<Skeleton height="64px" width="64px" borderRadius="100%" />
			<div class="rows" style="flex: 1;">
				<Skeleton height="18px" width="10rem" />
				<Skeleton height="14px" width="15rem" />
			</div>
		</div>
		<div class="chat">
			<Skeleton height="64px" width="64px" borderRadius="100%" />
			<div class="rows" style="flex: 1;">
				<Skeleton height="18px" width="10rem" />
				<Skeleton height="14px" width="15rem" />
			</div>
		</div>
		<div class="chat">
			<Skeleton height="64px" width="64px" borderRadius="100%" />
			<div class="rows" style="flex: 1;">
				<Skeleton height="18px" width="10rem" />
				<Skeleton height="14px" width="15rem" />
			</div>
		</div>
	{:else if data.chats.length == 0}
		<div class="placeholder">
			<p class="emoji">😉</p>
			<p class="placeholder-text">Здесь пока ничего нет.<br /> Самое время исправить это!</p>
		</div>
	{:else}
		{#each data.chats as chat}
			{@const otherUser = chat.users.filter((user) => user.id !== $page.data.user.id)[0]}
			<a href={`/chats/${chat.id}`} class="chat">
				<Avatar user={otherUser} size="64px" />
				<div class="rows">
					<div class="row">
						<h5>{chat.users.filter((user) => user.id !== $page.data.user.id)[0].name}</h5>
					</div>
					{#if chat.messages.length > 0}
						<div class="row">
							<h6>{chat.messages[chat.messages.length - 1].body || ''}</h6>
						</div>
					{/if}
				</div>
			</a>
		{/each}
	{/if}
</div>

<style lang="scss">
	.chats {
		display: flex;
		flex: 1;
		flex-direction: column;
		gap: 12px;
	}

	.placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		background: #f2f1f6;
		border-radius: 40px;
		gap: 12px;
		margin-bottom: 20px;
		.emoji {
			font-size: 80px;
		}
	}
	.placeholder-text {
		font-weight: 600;
		text-align: center;
		font-size: 24px;
	}
	.chat {
		display: flex;
		gap: 12px;
		align-items: center;
		text-decoration: none;
	}
	.rows {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	h5 {
		color: #000;
		font-family: 'PP Pangram Sans Rounded';
		font-size: 18px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 18px */
		letter-spacing: -0.27px;
	}
	h6 {
		text-wrap: wrap;
		/* Наборный текст */
		font-family: 'PP Pangram Sans Rounded';
		font-size: 14px;
		font-style: normal;
		font-weight: 400;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.56px;
		color: var(--fg-gray);
	}
</style>
