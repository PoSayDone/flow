<script lang="ts">
	import Transition from '$lib/components/transition.svelte';
	import Header from '$lib/components/header.svelte';
	import Navbar from '$lib/components/navbar.svelte';
	import type { LayoutData } from './$types';
	import Modal from '$lib/components/modal.svelte';
	import StatusPopup from '$lib/components/statusPopup.svelte';
	import { showStatusModal, showInterestsModal, showAvatarModal } from '$lib/stores';
	import InterestsPopup from '$lib/components/interestsPopup.svelte';
	import AvatarPopup from '$lib/components/avatarPopup.svelte';

	export let data: LayoutData;

	const showHeader = (pathname: string | undefined) => {
		return !(
			pathname?.startsWith('/chats/') ||
			pathname?.startsWith('/auth') ||
			pathname?.startsWith('/user_') ||
			pathname?.startsWith('/profile')
		);
	};
	const showNavbar = (pathname: string | undefined) => {
		return !(
			pathname?.startsWith('/chats/') ||
			pathname?.startsWith('/auth') ||
			pathname?.startsWith('/user_')
		);
	};
</script>

<Modal bind:showModal={$showInterestsModal}>
	<InterestsPopup bind:showModal={$showInterestsModal} />
</Modal>

<Modal centered={true} bind:showModal={$showAvatarModal}>
	<AvatarPopup bind:showModal={$showAvatarModal} />
</Modal>

<Modal bind:showModal={$showStatusModal}>
	<StatusPopup bind:showModal={$showStatusModal} />
</Modal>

{#if showHeader(data.pathname)}
	<Header bind:showStatusModal={$showStatusModal}></Header>
{/if}
<main>
	<Transition key={data.pathname}>
		<slot />
	</Transition>
</main>
{#if showNavbar(data.pathname)}
	<Navbar />
{/if}
