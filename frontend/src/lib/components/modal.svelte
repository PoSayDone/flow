<script lang="ts">
	import Button from './button.svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';

	export let showModal: boolean; // boolean
	export let action: string;
	let form: HTMLFormElement;
	let dialog: HTMLDialogElement; // HTMLDialogElement

	$: if (dialog && showModal) dialog.showModal();

	const closeAnimation = () => {
		dialog.addEventListener('animationend', closeDialog);
		dialog.classList.add('close');
	};

	function closeDialog() {
		form.requestSubmit();
		dialog.close();
		dialog.classList.remove('close');
		dialog.removeEventListener('animationend', closeDialog);
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog bind:this={dialog} on:close={() => (showModal = false)} on:click|self={closeAnimation}>
	<form
		bind:this={form}
		method="POST"
		action={`/profile?/${action}`}
		use:enhance={() => {
			return async ({ result }) => {
				await applyAction(result);
			};
		}}
	>
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div on:click|stopPropagation>
			<slot />
			<Button type="subimt" class="close-button" autofocus on:click={closeAnimation}>
				<h2>Готово</h2>
			</Button>
		</div>
	</form>
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

	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}

	dialog[open] {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) modal-open;
	}

	dialog[open]::backdrop {
		animation: fade 0.3s ease-out;
	}

	:global(dialog.close[open]) {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) modal-close;
	}
	:global(dialog.close::backdrop) {
		animation: fade-out 0.2s ease-out;
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
</style>
