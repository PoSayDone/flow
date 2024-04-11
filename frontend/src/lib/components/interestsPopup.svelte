<script lang="ts">
	import Chip from './chip.svelte';
	import { page } from '$app/stores';
	import Button from './button.svelte';
	import { superForm } from 'sveltekit-superforms';
	import { closeCurrentDialog, selectedInterests, submitCurrentDialog } from '$lib/stores';
	import { interestsRu } from '$lib/types';

	export let showModal;

	const { form, enhance, submit } = superForm($page.data.interestsForm, {
		dataType: 'json',
		resetForm: false,
		clearOnSubmit: 'none',
		onResult: ({ result }) => {
			if (result.status == 204) {
				selectedInterests.set($form.user_interests);
				$closeCurrentDialog();
			}
		}
	});

	function toggleOption(id: number) {
		if ($form.user_interests.includes(id)) {
			$form.user_interests = $form.user_interests.filter((item: number) => item !== id);
		} else {
			form.set({ user_interests: [...$form.user_interests, id] });
		}
	}
	$: if (showModal) {
		submitCurrentDialog.set(submit);
	}
</script>

<form method="POST" action="?/update_interests" use:enhance>
	<div class="container">
		<h1>Интересы</h1>
		<div class="interests">
			{#each $page.data.interests as interest}
				<Chip
					clickable={true}
					checked={$form.user_interests.includes(interest.id)}
					id={interest.id}
					onClick={() => toggleOption(interest.id)}
					text={interestsRu[interest.interest_name]}
					disabled={$form.user_interests.length >= 5 && !$form.user_interests.includes(interest.id)}
				/>
			{/each}
		</div>
	</div>

	<Button type="submit" class="close-button" autofocus>
		<h2>Готово</h2>
	</Button>
</form>

<style lang="scss">
	h1 {
		margin-bottom: 30px;
	}

	.container {
		border-radius: 40px 40px 0 0;
		background: #fff;
		align-items: center;
		display: flex;
		flex-direction: column;
		margin-bottom: 60px;
	}

	.interests {
		width: 100%;
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
	}
</style>
