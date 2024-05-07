<script>
	import Header from '$lib/components/header.svelte';
	import Navbar from '$lib/components/navbar.svelte';
	import StatusPopup from '$lib/components/statusPopup.svelte';
	import Modal from '$lib/components/modal.svelte';

	let showStatusModal = false;
</script>

<Modal bind:showModal={showStatusModal}>
	<StatusPopup bind:showModal={showStatusModal} />
</Modal>

<Header bind:showStatusModal />
<main>
	<slot />
</main>
<Navbar />
