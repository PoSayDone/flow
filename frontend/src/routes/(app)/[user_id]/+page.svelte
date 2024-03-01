<script lang="ts">
	import { backIcon } from '$lib/assets/Appicons';
	import Chip from '$lib/components/chip.svelte';
	import Icon from '$lib/components/icon.svelte';
	import { browser } from '$app/environment';

	let overflow: HTMLDivElement;
	let startY: number;
	let startTop: string;
	let overflowStart = 330;

	function nav_back() {
		if (browser) window.history.back();
	}

	function handleTouchStart(event: TouchEvent) {
		startY = event.touches[0].clientY;
		startTop = overflow.style.top;
	}
	function handleTouchMove(event: TouchEvent) {
		const deltaY = event.touches[0].clientY - startY;
		if (!startTop || startTop == `${overflowStart}px`) {
			const value = Math.min(Math.max(overflowStart + deltaY, 84), 330);
			overflow.style.top = `${value}px`;
		} else {
			const value = Math.min(Math.max(84 + deltaY, 84), 330);
			overflow.style.top = `${value}px`;
		}
	}
	function handleTouchEnd(event: TouchEvent) {
		overflow.style.transition = 'top 0.3s cubic-bezier(.19,.93,1,1)';
		if (startY - event.changedTouches[0].clientY > 50) {
			overflow.style.top = '84px';
			setTimeout(() => {
				overflow.style.transition = '';
			}, 300);
		} else if (startY - event.changedTouches[0].clientY < -50) {
			overflow.style.top = `${overflowStart}px`;
			setTimeout(() => {
				overflow.style.transition = '';
			}, 300);
		} else {
			overflow.style.top = startTop;
		}
	}
</script>

<div class="actions">
	<button class="action" on:click={nav_back}>
		<Icon d={backIcon.d} viewBox={backIcon.viewBox} color={'#2461FF'} />
	</button>
</div>
<div class="profile-picture"></div>

<div
	class="overflow"
	style="top: {overflowStart}px"
	bind:this={overflow}
	on:touchstart={handleTouchStart}
	on:touchmove={handleTouchMove}
	on:touchend={handleTouchEnd}
	on:touchcancel={handleTouchEnd}
>
	<span class="line" />
	<div class="heading">
		<h1>Никита,19</h1>
		<h2>Дизайнер</h2>
	</div>
	<p class="about">
		Я люблю путешествовать, потому что это позволяет мне познавать другие культуры, открывать новые
		места и встречать интересных людей. Я уже побывал во многих странах, но всегда готов к новым
		приключениям и открытиям
	</p>
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
			<Chip text="Дизайн" />
			<Chip text="Программирование" />
			<Chip text="Горные лыжи" />
			<Chip text="Бары" />
			<Chip text="Архитектура" />
		</div>
	</div>
</div>

<style lang="scss">
	.profile-picture {
		background: linear-gradient(180deg, rgba(0, 0, 0, 0) 40%, #000 100%),
			url('https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg');
		background-size: cover;
		width: 100%;
		height: 400px;
	}

	.overflow {
		height: 674px;
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
</style>
