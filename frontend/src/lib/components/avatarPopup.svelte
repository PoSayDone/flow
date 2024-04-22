<script lang="ts">
	import { page } from '$app/stores';
	import { closeCurrentDialog, submitCurrentDialog } from '$lib/stores';
	import { placeholder } from '$lib/utils';
	import { trashIcon, editIcon, approveIcon, addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	import { fileProxy, superForm } from 'sveltekit-superforms';

	export let showModal;
	let image: HTMLImageElement;
	let fileInput: HTMLInputElement;
	let showPreview = false;
	const user = $page.data.user;
	const url = import.meta.env.VITE_SITE_URL;

	const { form, enhance, submit, errors } = superForm($page.data.avatarForm, {
		dataType: 'json',
		resetForm: false,
		clearOnSubmit: 'none',
		invalidateAll: true,

		onSubmit: ({ cancel }) => {
			if (showPreview == false) cancel();
		},

		onResult: ({ result }) => {
			if (result.status == 204) {
				$closeCurrentDialog();
			}
		}
	});

	const file = fileProxy(form, 'image');

	function onChange() {
		if ($file[0]) {
			showPreview = true;
			const reader = new FileReader();
			reader.addEventListener('load', function () {
				image.setAttribute('src', reader.result);
			});
			reader.readAsDataURL($file[0]);

			return;
		}
		showPreview = false;
	}

	$: if (showModal) {
		submitCurrentDialog.set(submit);
	}
</script>

<form method="POST" action="?/update_avatar" enctype="multipart/form-data" use:enhance>
	<div class="container">
		<div class="avatar-container">
			{#if showPreview}
				<img alt="Preview" bind:this={image} class={`avatar`} />
			{:else if user}
				<img alt="Avatar" class={`avatar`} src={`${url}/images/${user.user_image}`} />
			{:else}
				<img alt="Avatar" class={`avatar`} src={`${url}/images/${placeholder(user.sex)}`} />
			{/if}
		</div>
	</div>

	<input
		name="file"
		type="file"
		accept=".jpg, .jpeg, .png, .webp"
		bind:this={fileInput}
		bind:files={$file}
		on:change={onChange}
	/>
	{#if !showPreview}
		<div class="buttons">
			<button type="button">
				<Icon
					viewBox={trashIcon.viewBox}
					d={trashIcon.d}
					stroke_width={'2'}
					size={'25'}
					color={'#F14444'}
				/>
			</button>
			<button on:click={() => fileInput.click()} type="button">
				<Icon
					viewBox={editIcon.viewBox}
					d={editIcon.d}
					stroke_width={'1.2'}
					size={'23'}
					color={'#2461FF'}
				/>
			</button>
		</div>
	{:else}
		<div class="buttons">
			<button
				type="button"
				class="cancel"
				on:click={() => {
					showPreview = false;
				}}
			>
				<Icon
					viewBox={addIcon.viewBox}
					d={addIcon.d}
					stroke_width={'1.3'}
					size={'32'}
					color={'#F14444'}
				/>
			</button>
			<button on:click={submit} type="button">
				<Icon
					viewBox={approveIcon.viewBox}
					d={approveIcon.d}
					stroke_width={'1.3'}
					size={'23'}
					color={'#2461FF'}
				/>
			</button>
		</div>
	{/if}
</form>

<style lang="scss">
	.avatar-container {
		display: flex;
		border-radius: 40px;
		background: #d6d6d6;
	}

	.avatar {
		height: 50svh;
		width: 100%;
		border-radius: 40px;
		object-fit: cover;
	}

	.buttons {
		margin-top: 10px;
		display: flex;
		justify-content: center;
		gap: 20px;
		width: 100%;
	}

	.cancel {
		:global(svg) {
			transform: rotate(45deg);
		}
	}

	input {
		display: none;
	}

	button {
		background: #fff;
		border-radius: 100%;
		min-width: 60px;
		min-height: 60px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
