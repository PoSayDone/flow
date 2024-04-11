<script lang="ts">
	import { backIcon, sendIcon } from '$lib/assets/Appicons';
	import Icon from '$lib/components/icon.svelte';
	import { browser } from '$app/environment';
	import { onDestroy, onMount } from 'svelte';
	import { pusherClient } from '$lib/pusher';
	import { page } from '$app/stores';
	import { superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import type { Message, User } from '$lib/types';
	import { getAge } from '$lib/utils';
	import Avatar from '$lib/components/avatar.svelte';

	export let data: PageData;
	let messages: Message[] = data.messages || [];

	let otherUser: User = data.users.filter((u) => u.id != $page.data.user.id)[0];

	function nav_back() {
		if (browser) window.history.back();
	}

	let messagesContainer: HTMLDivElement;

	const scrollToBottom = (node: HTMLDivElement) => {
		const scroll = () =>
			node.scroll({
				top: node.scrollHeight,
				behavior: 'smooth'
			});
		scroll();

		return { update: scroll };
	};

	const newHandler = (data: Message) => {
		messages = [...messages, data];
		setTimeout(() => {
			scrollToBottom(messagesContainer);
		}, 100);
	};

	onMount(() => {
		pusherClient.subscribe($page.data.user.mail);
		pusherClient.bind('message:new', newHandler);

		scrollToBottom(messagesContainer);
	});

	onDestroy(() => {
		pusherClient.unsubscribe($page.data.mail);
		pusherClient.unbind('message:new', newHandler);
	});

	const { form, enhance } = superForm(data.messageForm, {
		dataType: 'json',
		resetForm: false
	});
</script>

<div class="container">
	<div class="header">
		<div class="left-block">
			<button on:click={nav_back} class="back">
				<Icon viewBox={backIcon.viewBox} d={backIcon.d} size={'30'} stroke_width={'2'} />
			</button>
		</div>
		<div class="center-block">
			<span class="name">{otherUser.name}, {getAge(otherUser.birthdate.toString())}</span>
		</div>
		<div class="right-block">
			<a href={`/user_${otherUser.id}`}>
				<Avatar user={otherUser} />
			</a>
		</div>
	</div>
	<div bind:this={messagesContainer} class="messages">
		{#each messages as message}
			<div class={`message ${message.sender_id === otherUser.id ? 'to' : 'from'}`}>
				{message.body}
			</div>
		{/each}
	</div>

	<form class="message-input" method="POST" action="?/send_message" use:enhance>
		<textarea placeholder="Напишите сообщение..." bind:value={$form.message} rows="1" />
		<button class="send" type="submit">
			<Icon viewBox={sendIcon.viewBox} d={sendIcon.d} size={'27'} stroke_width={'2'} />
		</button>
	</form>
</div>

<style lang="scss">
	.container {
		max-height: 100svh;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.left-block,
	.right-block {
		flex: 1;
	}

	.header {
		display: flex;
		align-items: center;
		padding: 8px 20px;
		border-bottom: 1px solid #efeff4;
	}

	.left-block {
		display: flex;
		justify-content: start;
	}

	.back {
		background: none;
		border: none;
		padding: 0;
		margin: 0;
		height: 30px;
		:global(path) {
			stroke: var(--primary);
		}
	}

	.center-block {
		margin: 0 auto;
	}

	.name {
		color: #000;
		text-align: center;
		leading-trim: both;
		text-edge: cap;
		font-family: 'PP Pangram Sans Rounded';
		font-size: 18px;
		font-style: normal;
		font-weight: 600;
		line-height: 100%; /* 18px */
		letter-spacing: -0.27px;
	}

	.right-block {
		display: flex;
		justify-content: end;
	}

	.messages {
		display: flex;
		flex-direction: column;
		flex: 1;
		overflow-y: scroll;
		padding: 30px 20px;
		gap: 10px;
	}

	.message {
		display: flex;
		max-width: 245px;
		padding: 10px 15px;
		flex-direction: column;
		align-items: flex-start;

		font-family: 'PP Pangram Sans Rounded';
		font-size: 14px;
		font-style: normal;
		font-weight: 600;
		line-height: 120%; /* 16.8px */
		letter-spacing: -0.21px;
	}

	.message.from {
		align-self: end;
		background: var(--Secondary-blue, #2461ff);
		border-radius: 15px 15px 0px 15px;
		color: #fff;
	}

	.message.to {
		align-self: start;
		border-radius: 15px 15px 15px 0px;
		background: var(--light-mode-white-80, #efeff4);
		color: #000;
	}

	.message-input {
		display: flex;
		border-radius: 55px;
		border: 1px solid var(--light-mode-black-60, #cecece);
		min-height: 55px;
		align-items: center;
		margin: 10px 20px;
		textarea {
			color: #000;
			font-family: 'PP Pangram Sans Rounded';
			font-size: 14px;
			font-style: normal;
			font-weight: 500;
			line-height: 120%; /* 16.8px */
			letter-spacing: -0.56px;
			min-height: 20px;
			margin: 0 19px;
			border: none;
			flex: 1;
			padding: 14px 0;
			outline: none;
		}
		textarea::placeholder {
			color: var(--Gray-Text, #aaa);
		}
	}

	.send {
		width: 45px;
		height: 45px;
		border-radius: 100%;
		background-color: #2461ff;
		margin-right: 5px;
		border: none;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
