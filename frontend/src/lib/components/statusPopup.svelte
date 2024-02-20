<script>
	import Chip from './chip.svelte';
  import { status } from "$lib/stores";
  import Icon from "$lib/components/icon.svelte";
  import { backIcon } from "$lib/assets/Appicons";
</script>

<div class="container">
  <h1>Выберите статус</h1>
  <div class="radios" role="radiogroup">
    <label class="radio" class:active={$status == "active"}>
      <div class="rows">
        <label class="radio-title" for="active">Активный</label>
        <label class="radio-subtitle" for="active">
          Готов отправиться в путешествие
        </label>
      </div>
      <input type="radio" id="active" value="active" bind:group={$status} />
    </label>
    {#if $status == "active"}
      <button class="from">Откуда <Icon d={backIcon.d} viewBox={backIcon.viewBox} color="#000000" size="24px"/></button>
      <button class="to">Куда <Icon d={backIcon.d} viewBox={backIcon.viewBox} color="#000000" size="24px"/></button>
      <div class="travel-purposes">
        <Chip clickable={true}></Chip>
      </div>
    {/if}
    <label class="radio" class:active={$status == "inactive"}>
      <div class="rows">
        <label class="radio-title" for="inactive">Перерыв</label>
        <label class="radio-subtitle" for="inactive">Пока не путешествую</label>
      </div>
      <input type="radio" id="inactive" value="inactive" bind:group={$status} />
    </label>
  </div>
</div>

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
  }

  .radios {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
  }

  .from {
    margin-top: 5px;
  }
  .to {
    margin-bottom: 5px;
  }

  .from, .to {
    background-color: #f2f1f6;
    width: 100%;
    border: none;
    border-radius: 20px;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    :global(svg) {
      transform: rotate(180deg);
    }
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 20px;
  }

  .tag {
    border: 1px solid #D6D6D6;
    border-radius: 100px;
    background: none;
    padding: 9px 18px;
  }

  .radio {
    background-color: #f2f1f6;
    width: 100%;
    border: none;
    border-radius: 20px;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition:
      background-color 0.2s ease-in-out,
      color 0.2s ease-in-out;

    &.active {
      background-color: #d3dfff;
      color: var(--primary);
    }
  }

  .radio-title {
    font-family: "PP Pangram Sans Rounded";
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    line-height: 100%; /* 18px */
    letter-spacing: -0.27px;
  }

  .radio-subtitle {
    font-family: "PP Pangram Sans Rounded";
    font-size: 14px;
    font-style: normal;
    font-weight: 500;
    line-height: 120%; /* 16.8px */
    letter-spacing: -0.56px;
  }

  .rows {
    align-items: start;
    display: flex;
    flex-direction: column;
  }

  input[type="radio"] {
    appearance: none;
    background-color: #fff;
    margin: 0;

    font: inherit;
    color: currentColor;
    width: 20px;
    height: 20px;
    border: 1.5px solid #eeedf2;
    border-radius: 50%;
    transform: translateY(-0.075em);

    display: grid;
    place-content: center;
  }

  input[type="radio"]::before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transform: scale(0);
    transition: 120ms transform ease-in-out;
    box-shadow: inset 1em 1em var(--form-control-color);
    /* Windows High Contrast Mode */
    background-color: var(--primary);
  }

  input[type="radio"]:checked::before {
    transform: scale(1);
  }
</style>
