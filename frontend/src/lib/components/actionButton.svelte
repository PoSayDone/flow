<script>
  import { dislikeIcon, likeIcon, writeIcon } from "$lib/assets/Appicons";
  import Icon from "./icon.svelte";

  export let type = "like";
  const types = {
    chat: writeIcon,
    like: likeIcon,
    dislike: dislikeIcon,
  };
  const sizes = {
    chat: "25px",
    like: "22px",
    dislike: "18px",
  };
</script>

<button class={type}>
  <Icon d={types[type].d} viewBox={types[type].viewBox} size={sizes[type]} />
</button>

<style lang="scss">
  button {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 100%;
    border: none;
    background: #f2f1f6;
  }

  .like {
    transition: all 0.1s ease-in-out;
    :global(path) {
      transition: all 0.1s ease-in-out;
      fill: #ff44b4;
      stroke: none;
    }
    &:active {
      background: #ff44b4;
      :global(path) {
        fill: #f2f1f6;
        stroke: none;
      }
    }
  }

  .dislike {
    transition: all 0.1s ease-in-out;
    :global(path) {
      transition: all 0.1s ease-in-out;
      stroke: #F14444;
    }
    &:active {
      background: #F14444;
      :global(path) {
        stroke: #f2f1f6;
      }
    }
  }

  .chat {
    background: var(--primary);
  }
</style>
