<script>
  import Icon from "./icon.svelte";
  import { addIcon } from "$lib/assets/Appicons";
  import { status } from "$lib/stores";
  import StatusPopup from "./statusPopup.svelte";
  import Modal from "./modal.svelte";

  let showModal = false;
</script>

<button on:click={() => (showModal = true)}>
  <span class="indicator" class:active={$status === "active"}></span>
  <span class="status">
    {$status === "active" ? "Активный" : "Перерыв"}
  </span>
  <Icon
    viewBox={addIcon.viewBox}
    d={addIcon.d}
    stroke_width={"1.5"}
    size={"18"}
    color={"#000"}
  />
</button>

<Modal bind:showModal>
  <StatusPopup />
</Modal>

<style lang="scss">
  button {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 100px;
    border: none;
    padding: 10px 14px;
    cursor: pointer;
  }

  .indicator {
    margin-right: 6px;
    background: #ff3b3b;
    width: 10px;
    height: 10px;
    border-radius: 100%;
    &.active {
      background: #72cd2a;
    }
  }

  .status {
    margin-right: 14px;
  }
</style>
