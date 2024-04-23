<script>
  export let d = [""];
  export let viewBox = "0 0 24 24";
  export let color = "#fff";
  export let stroke = color;
  export let stroke_width = "3";
  export let size = "36px"; // default 1em match the parent element
</script>

<svg
  class="icon"
  {viewBox}
  style:width={size}
  style:height={size}
  xmlns="http://www.w3.org/2000/svg"
>
  {#each d as path}
    <path {stroke} fill="none" stroke-width={stroke_width} d={path} stroke-linejoin="round" stroke-linecap="round" />
  {/each}
</svg>

<style>
  .icon {
    position: relative;
    display: inline-block;
  }
</style>
