<script>
  import Header from "$lib/components/header.svelte";
  import { fly } from "svelte/transition";
  import Navbar from "$lib/components/navbar.svelte";
</script>

<main>
  <slot />
</main>
<Navbar />