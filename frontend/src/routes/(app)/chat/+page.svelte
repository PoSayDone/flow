<script lang="ts">
</script>

<div class="tabs">
  <a href="">
    <h1>Отклики</h1>
  </a>
  <a href="">
    <h1>Общие</h1>
  </a>
</div>
<div class="chats">
  <a href="/chat/1" class="chat">
    <div class="avatar">
      <img
        src="https://i.ibb.co/jLC2xRd/e47da5ad29942101286011bd4ddc1251.jpg"
        alt="avatar"
      />
    </div>
    <div class="rows">
      <div class="row">
        <h5>Никита, 18</h5>
      </div>
      <div class="row">
        <h6>
          Привет, я тоже хочу слетать в Австрию, на лыжах покататься. Уже есть
          виза,
        </h6>
      </div>
    </div>
  </a>
</div>

<style lang="scss">
  .tabs {
    display: flex;
    margin-bottom: 20px;
    gap: 12px;
    a {
      text-decoration: none;
      color: #000;
    }
  }

  .chat {
    display: flex;
    gap: 12px;
    align-items: center;
    text-decoration: none;
  }
  .avatar {
    flex-shrink: 0;
    width: 64px;
    height: 64px;
    border-radius: 100%;
    overflow: hidden;
    img {
      height: 100%;
    }
  }
  .rows {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  h5 {
    color: #000;
    font-family: "PP Pangram Sans Rounded";
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    line-height: 100%; /* 18px */
    letter-spacing: -0.27px;
  }
  h6 {
    text-wrap: wrap;
    /* Наборный текст */
    font-family: "PP Pangram Sans Rounded";
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 120%; /* 16.8px */
    letter-spacing: -0.56px;
    color: var(--fg-gray);
  }
</style>
