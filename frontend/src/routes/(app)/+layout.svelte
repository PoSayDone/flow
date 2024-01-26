<script>
  import Header from "$lib/components/header.svelte";
  import { fly } from "svelte/transition";
  import Navbar from "$lib/components/navbar.svelte";
</script>

<Header />
<main>
  <slot />
</main>
<Navbar />