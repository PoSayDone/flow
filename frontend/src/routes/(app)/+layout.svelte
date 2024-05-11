<script lang="ts">
	import Transition from '$lib/components/transition.svelte';
	import Header from '$lib/components/header.svelte';
	import Navbar from '$lib/components/navbar.svelte';
	import type { LayoutData } from './$types';
	import Modal from '$lib/components/modal.svelte';
	import StatusPopup from '$lib/components/statusPopup.svelte';

	export let data: LayoutData;
	let showStatusModal = false;

	const showHeader = (pathname: string | undefined) => {
		return !(
			pathname?.startsWith('/chats/') ||
			pathname?.startsWith('/auth') ||
			pathname?.startsWith('/user_') ||
			pathname?.startsWith('/profile')
		);
	};
</script>

<Modal bind:showModal={showStatusModal}>
	<StatusPopup bind:showModal={showStatusModal} />
</Modal>

{#if showHeader(data.pathname)}
	<Header bind:showStatusModal></Header>
{/if}
<main>
	<Transition key={data.pathname}>
		<slot />
	</Transition>
</main>
{#if !data.pathname?.startsWith('/chats/')}
	<Navbar />
{/if}
