<script lang="ts">
	import { page } from '$app/stores';
	import { closeCurrentDialog, submitCurrentDialog } from '$lib/stores';
	import { images_url, placeholder } from '$lib/utils';
	import { trashIcon, editIcon, approveIcon, addIcon } from '$lib/assets/Appicons';
	import Icon from './icon.svelte';
	import { fileProxy, superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import { avatarSchema } from '$lib/schema';
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let showModal;

	let newImage: string | ArrayBuffer | null;
	let tempImage: string | ArrayBuffer | null;
	let fileInput: HTMLInputElement;
	let previewShown = false;
	let loading = false;
	const user = $page.data.user;

	const closeAvatarDialog = () => {
		$closeCurrentDialog();
		resetForm();
	};

	const { form, errors, enhance, submit, reset } = superForm($page.data.avatarForm, {
		dataType: 'json',
		resetForm: true,
		clearOnSubmit: 'errors-and-message',
		invalidateAll: true,
		validators: zodClient(avatarSchema),
		validationMethod: 'auto',

		onSubmit: () => {
			loading = true;
		},

		onResult: ({ result }) => {
			loading = false;
			if (result.status == 204) {
				newImage = tempImage;
				closeAvatarDialog();
			}
		}
	});

	const file = fileProxy(form, 'image');

	const onFileSelected = (event: Event) => {
		const target = event.target as HTMLInputElement;
		if (target.files && target.files.length) {
			let imageFile = target.files[0];
			let reader = new FileReader();
			reader.readAsDataURL(imageFile);
			reader.onload = (event: ProgressEvent<FileReader>) => {
				if (event.target) {
					tempImage = event.target.result;
					previewShown = true;
				}
			};
		}
	};

	const resetForm = () => {
		tempImage = null;
		fileInput.value = '';
		previewShown = false;
		reset();
	};

	$: if (showModal) {
		submitCurrentDialog.set(closeAvatarDialog);
	}
</script>

<form method="POST" action="?/update_avatar" enctype="multipart/form-data" use:enhance>
	{#if $errors.image}
		<div
			transition:slide={{ delay: 250, duration: 300, easing: quintOut, axis: 'y' }}
			class="errors"
		>
			{$errors.image}
		</div>
	{/if}
	<button type="button" class="avatar-container" on:click={() => fileInput.click()}>
		{#if tempImage}
			<img alt="Preview" src={tempImage.toString()} class={`avatar`} />
		{:else if newImage}
			<img alt="Preview" src={newImage.toString()} class={`avatar`} />
		{:else if user.user_image}
			<img alt="Avatar" class={`avatar`} src={`${images_url}/${user.user_image}`} />
		{:else}
			<img alt="Avatar" class={`avatar`} src={`${images_url}/${placeholder(user.sex)}`} />
		{/if}
	</button>

	<input
		name="image"
		type="file"
		accept="image/png, image/jpeg, image/webp"
		bind:this={fileInput}
		bind:files={$file}
		on:change={onFileSelected}
	/>
	{#if !previewShown}
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
				on:click={resetForm}
				disabled={loading}
				aria-disabled={loading}
			>
				<Icon
					viewBox={addIcon.viewBox}
					d={addIcon.d}
					stroke_width={'1.3'}
					size={'32'}
					color={'#F14444'}
				/>
			</button>
			<button
				disabled={$errors.image != undefined || loading}
				aria-disabled={$errors.image != undefined || loading}
				on:click={submit}
				type="button"
			>
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
	.errors {
		height: 60px;
		display: flex;
		align-items: center;
		padding: 0 20px;
		margin-bottom: 10px;
		border-radius: 20px;

		color: #f14444;
		background: #ffffff;
		font-weight: 600;
	}

	.avatar-container {
		display: flex;
		height: 50svh;
		width: 100%;
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

	button[aria-disabled='true'] {
		opacity: 50%;
	}
</style>
