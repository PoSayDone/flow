<script>
  import Logo from "$lib/assets/images/logo.svelte";
  import Indicator from "./indicator.svelte";
</script>

<header>
  <Logo />
  <Indicator />
</header>

<style>
  header {
    display: flex;
    justify-content: space-between;
    margin: 25px 20px;
  }
</style>
