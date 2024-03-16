<script lang="ts">
	import { interests_binding, trip_purposes_binding } from '$lib/utils';
	import { backIcon } from '$lib/assets/Appicons';
	import { getAge } from '$lib/utils';
	import Chip from '$lib/components/chip.svelte';
	import Icon from '$lib/components/icon.svelte';
	import { browser } from '$app/environment';
	import type { PageData } from './$types';

	let popover: HTMLDivElement;
	let startY: number;
	let startTop: string;
	let popoverStart = 330;

	export let data: PageData;

	function nav_back() {
		if (browser) window.history.back();
	}

	function handleTouchStart(event: TouchEvent) {
		startY = event.touches[0].clientY;
		startTop = popover.style.top;
	}
	function handleTouchMove(event: TouchEvent) {
		const deltaY = event.touches[0].clientY - startY;
		if (!startTop || startTop == `${popoverStart}px`) {
			const value = Math.min(Math.max(popoverStart + deltaY, 84), 330);
			popover.style.top = `${value}px`;
		} else {
			const value = Math.min(Math.max(84 + deltaY, 84), 330);
			popover.style.top = `${value}px`;
		}
	}
	function handleTouchEnd(event: TouchEvent) {
		popover.style.transition = 'top 0.3s cubic-bezier(.19,.93,1,1)';
		if (startY - event.changedTouches[0].clientY > 50) {
			popover.style.top = '84px';
			setTimeout(() => {
				popover.style.transition = '';
			}, 300);
		} else if (startY - event.changedTouches[0].clientY < -50) {
			popover.style.top = `${popoverStart}px`;
			setTimeout(() => {
				popover.style.transition = '';
			}, 300);
		} else {
			popover.style.top = startTop;
		}
	}
</script>

<div class="actions">
	<button class="action" on:click={nav_back}>
		<Icon d={backIcon.d} viewBox={backIcon.viewBox} color={'#2461FF'} />
	</button>
</div>
<div class="backdrop" style:view-transition-name={`profile-image`}>
	<div class="profile-picture"></div>
</div>
<div class="tags" style:view-transition-name={`trip-purposes`}>
	{#each data.trip_purposes as id}
		<div class="tag">{trip_purposes_binding[id]}</div>
	{/each}
</div>
<div
	class="popover"
	style="top: {popoverStart}px"
	bind:this={popover}
	on:touchstart={handleTouchStart}
	on:touchmove={handleTouchMove}
	on:touchend={handleTouchEnd}
	on:touchcancel={handleTouchEnd}
>
	<span class="line" />
	<div class="heading">
		<h1>{data.name}, {getAge(data.birthdate)}</h1>
		<h2>{data.occupation}</h2>
	</div>
	<p class="about">{data.about}</p>
	<hr />
	<div class="directions">
		<ul class="from">
			<span class="direction-title">Откуда</span>
			<span class="dot" />
			<li>Пермь</li>
			<li>Москва</li>
		</ul>
		<ul class="to">
			<span class="direction-title">Куда</span>
			<span class="dot" />
			<li>Австрия</li>
			<li>Турция</li>
			<li>Италия</li>
			<li>Германия</li>
			<li>Россия</li>
		</ul>
	</div>
	<hr />
	<div class="interests">
		<h2>Интересы</h2>
		<div class="chips">
			{#each data.interests as id}
				<Chip text={interests_binding[id]} />
			{/each}
		</div>
	</div>
</div>

<style lang="scss">
	.backdrop {
		position: sticky;
		z-index: -10;
		height: 100%;
		background-color: #000;
	}
	.profile-picture {
		z-index: -100;
		position: sticky;
		background: linear-gradient(180deg, rgba(0, 0, 0, 0) 40%, #000 100%),
			url('https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg');
		background-size: cover;
		width: 100%;
		height: 400px;
	}

	.tags {
		position: absolute;
		display: flex;
		gap: 5px;
		left: 50%; /* position the top  edge of the element at the middle of the parent */
		top: 280px;

		transform: translateX(-50%);
	}

	.tag {
		border: 1px solid #fff;
		color: #fff;
		border-radius: 100px;
		padding: 5px 10px;
	}

	.popover {
		z-index: 1000;
		view-transition-name: popover;
		height: 100%;
		width: 100%;
		background-color: #fff;
		position: fixed;
		bottom: var(--bottom);
		padding: 0px 20px 20px 20px;
		border-radius: 40px 40px 0px 0px;
	}

	.line {
		height: 4px;
		width: 80px;
		background-color: #cecece;
		border-radius: 100px;
		display: flex;
		margin: 10px auto 16px auto;
	}

	.heading {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.about {
		margin-top: 15px;
	}

	hr {
		margin: 20px 0;
		border-radius: 40px;
		border: 1px solid var(--light-mode-white-80, #efeff4);
	}

	.directions {
		width: 100%;
		display: flex;
		justify-content: center;
		gap: 80px;
		font-weight: 600;
		li {
			list-style-type: none;
		}
		ul {
			list-style-type: none;
			display: flex;
			flex-direction: column;
			align-items: center;
			gap: 3px;
		}
	}

	.direction-title {
		color: #aaaaaa;
	}

	.dot {
		height: 14px;
		width: 14px;
		border: 2px solid #aaaaaa;
		border-radius: 50%;
		display: inline-block;
	}

	.interests {
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 9px;
	}

	.actions {
		view-transition-name: actions;
		margin: 0 20px;
		margin-top: 10px;
		position: fixed;
		top: 0;
	}

	.action {
		background: #fff;
		display: flex;
		justify-content: center;
		align-items: center;
		width: 55px;
		height: 55px;
		border-radius: 100%;
	}

	@keyframes popover-open {
		from {
			transform: translateY(50%);
			opacity: 0;
		}
	}

	@keyframes popover-close {
		to {
			transform: translateY(50%);
			opacity: 0;
		}
	}

	:root::view-transition-new(popover) {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) popover-open;
	}

	:root::view-transition-old(popover) {
		animation: 300ms cubic-bezier(0.4, 0, 0.2, 1) popover-close;
	}
</style>
