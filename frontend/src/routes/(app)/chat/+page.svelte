<script lang="ts">
  import type { PageData } from "../$types";

  export let data: PageData;
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
    <div class="profile-picture">
      <img
        src="https://s3-alpha-sig.figma.com/img/023f/fdeb/e47da5ad29942101286011bd4ddc1251?Expires=1706486400&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=ofSpVq3VI5pACaCIjvgk1RFRdcrYGN6S2wsiQW-Nz55aQVZV9dr8MWXtQdVZpbJpeW8cejJ~qnO-9vQ7z~MNSLYsFdRmLQb~PMW927-GvgENXPCi29c~hfWIAfxKpFx9Bv1Bz--bRXPZUq1fZslBQxlzMNdPr23MixvVzlSAz1cVZVF~2z8lU9udRyUeaMtgTZJiKCCu~YAWNTM5PdRZyKr-jA3z3rBu7i~AUfY0j1uhI~0Pr1n8OK6F4Zyl00MeCv3RFG~FEUI608RDI3L-wUrCmCasjAc~BKJuvuDTfuNkWG7DyHKPCumTGwZ7ylPQ~fYGoCTUvjwDvGTjisD5Sw__"
        alt="profile-picture"
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
  .profile-picture {
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
