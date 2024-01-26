<script>
  import { addIcon } from "$lib/assets/Appicons";
  import Icon from "./icon.svelte";
  let active = false;

  export let text = "Активный отдых";
  const handleClick = () => {
    active = !active;
  };
</script>

<button class:active on:click={handleClick}
  ><span>{text}</span><Icon
    stroke_width={"1.5"}
    size={"16"}
    d={addIcon.d}
    viewBox={addIcon.viewBox}
  /></button
>

<style lang="scss">
  button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: min-content;
    height: 36px;
    padding: 0 18px;
    border-radius: 100px;
    background: none;
    outline: 1.5px solid var(--bg-gray);
    border: none;
    cursor: pointer;
    transition: all 0.1s ease-in-out;

    span {
      text-wrap: nowrap;
      margin-right: 10px;
    }

    :global(path) {
      transition: all 0.1s ease-in-out;
      stroke: #000;
    }

    :global(svg) {
      transition: all 0.1s ease-in-out;
    }

    &.active {
      background: #d3dfff;
      color: #2461ff;
      outline: none;
      :global(path) {
        stroke: #2461ff;
      }
      :global(svg) {
        transform: rotate(45deg);
      }
    }
  }
</style>
