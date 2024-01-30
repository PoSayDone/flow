<script lang="ts">
  import { backIcon } from "$lib/assets/Appicons";
  import Chip from "$lib/components/chip.svelte";
  import Icon from "$lib/components/icon.svelte";
  import { browser } from "$app/environment";


  let overflow: HTMLDivElement;
  let startY: number;
  let startBottom: string;
  let overflowStart = -230;

  function nav_back() {
    if (browser) window.history.back();
  }

  function handleTouchStart(event: TouchEvent) {
    startY = event.touches[0].clientY;
    startBottom = overflow.style.bottom;
  }
  function handleTouchMove(event: TouchEvent) {
    const deltaY = event.touches[0].clientY - startY;
    if (!startBottom || startBottom == `${overflowStart}px`) {
      overflow.style.bottom = `${overflowStart + -deltaY}px`;
    } else {
      overflow.style.bottom = `${-deltaY}px`;
    }
  }
  function handleTouchEnd(event: TouchEvent) {
    overflow.style.transition = "bottom 0.3s cubic-bezier(.19,.93,1,1)";
    if (startY - event.changedTouches[0].clientY > 50) {
      overflow.style.bottom = "0";
      setTimeout(() => {
        overflow.style.transition = "";
      }, 300);
    } else if (startY - event.changedTouches[0].clientY < -50) {
      overflow.style.bottom = `${overflowStart}px`;
      setTimeout(() => {
        overflow.style.transition = "";
      }, 300);
    } else {
      overflow.style.bottom = startBottom;
    }
  }
</script>

<div class="actions">
  <button class="action" on:click={nav_back}>
    <Icon d={backIcon.d} viewBox={backIcon.viewBox} color={"#2461FF"}/>
  </button>
</div>
<div>
  <img
    src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg"
    alt=""
  />
</div>
<div
  class="overflow"
  style="--bottom: {overflowStart}px"
  bind:this={overflow}
  on:touchstart={handleTouchStart}
  on:touchmove={handleTouchMove}
  on:touchend={handleTouchEnd}
  on:touchcancel={handleTouchEnd}
>
  <div class="heading">
    <h1>Никита,19</h1>
    <h2>Дизайнер</h2>
  </div>
  <p class="about">
    Я люблю путешествовать, потому что это позволяет мне познавать другие
    культуры, открывать новые места и встречать интересных людей. Я уже побывал
    во многих странах, но всегда готов к новым приключениям и открытиям
  </p>
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

<style>
  img {
    width: 100%;
  }
  .overflow {
    height: 674px;
    background-color: #fff;
    position: fixed;
    bottom: var(--bottom);
    padding: 20px;
    border-radius: 40px 40px 0px 0px;
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
