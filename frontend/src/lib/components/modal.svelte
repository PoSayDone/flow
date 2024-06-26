<script lang="ts">
	import { closeCurrentDialog, submitCurrentDialog } from '$lib/stores';
	import { beforeNavigate } from '$app/navigation';

	export let showModal: boolean; // boolean
	export let centered: boolean = false;
	let dialog: HTMLDialogElement; // HTMLDialogElement

	$: if (dialog && showModal) {
		dialog.showModal();
		closeCurrentDialog.set(closeAnimation);
	}

	const closeAnimation = () => {
		dialog.addEventListener('animationend', closeDialog);
		dialog.classList.add('close');
	};

	function closeDialog() {
		dialog.close();
		dialog.classList.remove('close');
		dialog.removeEventListener('animationend', closeDialog);
	}

	beforeNavigate(({ cancel, type }) => {
		if (showModal && type != 'leave') {
			cancel();
			$submitCurrentDialog();
		}
	});
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	class:centered
	bind:this={dialog}
	on:close={() => {
		showModal = false;
	}}
	on:click|self={$submitCurrentDialog}
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div on:click|stopPropagation>
		<slot />
	</div>
</dialog>

<style>
	dialog {
		margin-top: auto;
		min-width: 100%;
		border-radius: 40px 40px 0 0;
		border: none;
		padding: 0;
		bottom: 0;
		padding: 30px 20px;
	}

	dialog.centered {
		padding: 0;
		border-radius: 0;
		margin: auto;
		min-width: 80%;
		background: none;
	}

	dialog::backdrop {
		background: rgba(0, 0, 0, 0.5);
	}

	dialog.centered::backdrop {
		background: rgba(0, 0, 0, 0.7);
	}

	dialog[open] {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) modal-open;
	}

	dialog[open]::backdrop {
		animation: fade-in 0.3s ease-out;
	}

	:global(dialog.close[open]) {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) modal-close;
	}

	:global(dialog.close[open]::backdrop) {
		animation: fade-out 0.3s ease-out;
	}

	@keyframes modal-open {
		from {
			transform: translateY(50%);
			opacity: 0;
		}
	}

	@keyframes modal-close {
		to {
			transform: translateY(50%);
			opacity: 0;
		}
	}

	@keyframes fade-in {
		from {
			opacity: 0;
		}
	}

	@keyframes fade-out {
		to {
			opacity: 0;
		}
	}
</style>
