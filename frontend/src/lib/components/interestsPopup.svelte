<script>
	import Chip from './chip.svelte';
</script>

<div class="container">
  <h1>Интересы</h1>
  <div class="interests">
    <Chip clickable={true} text="Хаха"/>
    <Chip clickable={true} text="Автомобили"/>
    <Chip clickable={true} text="Спорт"/>
    <Chip clickable={true} text="Искусство"/>
    <Chip clickable={true} text="Хаха"/>
    <Chip clickable={true} text="Хаха"/>
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

  .interests {
    width: 100%;
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
  }
</style>