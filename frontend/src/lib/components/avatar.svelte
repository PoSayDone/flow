<script lang="ts">
	import type { User } from '$lib/types';
	import { images_url, placeholder } from '$lib/utils';

	export const getInitials = (name: string) => {
		let initials = name.split(' ');

		if (initials.length > 1) {
			initials = initials.shift().charAt(0) + initials.pop().charAt(0);
		} else {
			initials = name.substring(0, 2);
		}

		return initials.toUpperCase();
	};

	export let bgColor = 'lightGrey';
	export let textColor = 'white';
	export let size = '50px';
	export let borderRadius = '50%';
	export let user: User;

	const background = bgColor;
</script>

<div
	aria-label={user.name}
	class="wrapper"
	style="--borderRadius:{borderRadius}; --size:{size}; --bgColor:{background};
   --textColor:{textColor};"
>
	{#if user.user_image}
		<div>
			<img alt="" class={`innerImage`} src={`${images_url}/${user.user_image}`} />
		</div>
	{:else}
		<img alt="" class={`innerImage`} src={`${images_url}/${placeholder(user.sex)}`} />
	{/if}
</div>

<style>
	.wrapper {
		position: relative;
		width: var(--size);
		height: var(--size);
		background: #d6d6d6;
		border-radius: var(--borderRadius);
	}

	.innerImage {
		display: block;
		width: var(--size);
		height: var(--size);
		object-fit: cover;
		border-radius: var(--borderRadius);
	}
</style>
