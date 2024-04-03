<script lang="ts">
	import { page } from '$app/stores';
	import { onDestroy, onMount } from 'svelte';
	import type { PageData } from './$types';
	import { pusherClient } from '$lib/pusher';
	import type { Conversation, Message } from '$lib/types';
	import { invalidateAll } from '$app/navigation';

	export let data: PageData;

	const newHandler = (newConversation: Conversation) => {
		invalidateAll();
	};
	const updateHandler = (newMessage: Message) => {
		invalidateAll();
	};

	onMount(() => {
		pusherClient.subscribe($page.data.mail);
		pusherClient.bind('conversation:new', newHandler);
		pusherClient.bind('message:new', updateHandler);
	});

	onDestroy(() => {
		pusherClient.unsubscribe($page.data.mail);
		pusherClient.unbind('conversation:new', newHandler);
		pusherClient.unbind('message:new', updateHandler);
	});
</script>

<div class="tabs">
	<a href="">
		<h1>Отклики</h1>
	</a>
	<a href="">
		<h1>Общие</h1>
	</a>
</div>
<div class="chats">
	{#each data.chats as chat}
		<a href={`/chat/${chat.id}`} class="chat">
			<div class="avatar">
				<img src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg" alt="avatar" />
			</div>
			<div class="rows">
				<div class="row">
					<h5>{chat.users.filter((user) => user.id !== $page.data.id)[0].name}</h5>
				</div>
				{#if chat.messages.length > 0}
					<div class="row">
						<h6>{chat.messages[chat.messages.length - 1].body || ''}</h6>
					</div>
				{/if}
			</div>
		</a>
	{/each}
</div>

<style lang="scss">
	.tabs {
		display: flex;
		margin-bottom: 20px;
		gap: 12px;
		a {
			text-decoration: none;
			color: #000;
		}
	}

	.chat {
		display: flex;
		gap: 12px;
		align-items: center;
		text-decoration: none;
	}
	.avatar {
		flex-shrink: 0;
		width: 64px;
		height: 64px;
		border-radius: 100%;
		overflow: hidden;
		img {
			height: 100%;
		}
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
