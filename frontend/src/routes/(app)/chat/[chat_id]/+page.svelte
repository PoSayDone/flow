<script>
  import { backIcon, sendIcon } from "$lib/assets/Appicons";
  import Icon from "$lib/components/icon.svelte";
  import { browser } from "$app/environment";

  //functions
  function nav_back() {
    if (browser) window.history.back();
  }
</script>

<div class="container">
  <div class="header">
    <div class="left-block">
      <button on:click={nav_back} class="back">
        <Icon
          viewBox={backIcon.viewBox}
          d={backIcon.d}
          size={"30"}
          stroke_width={"2"}
        />
      </button>
    </div>
    <div class="center-block">
      <span class="name">Никита, 19</span>
    </div>
    <div class="right-block">
      <img
        class="avatar"
        src="https://s3-alpha-sig.figma.com/img/023f/fdeb/e47da5ad29942101286011bd4ddc1251?Expires=1706486400&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=ofSpVq3VI5pACaCIjvgk1RFRdcrYGN6S2wsiQW-Nz55aQVZV9dr8MWXtQdVZpbJpeW8cejJ~qnO-9vQ7z~MNSLYsFdRmLQb~PMW927-GvgENXPCi29c~hfWIAfxKpFx9Bv1Bz--bRXPZUq1fZslBQxlzMNdPr23MixvVzlSAz1cVZVF~2z8lU9udRyUeaMtgTZJiKCCu~YAWNTM5PdRZyKr-jA3z3rBu7i~AUfY0j1uhI~0Pr1n8OK6F4Zyl00MeCv3RFG~FEUI608RDI3L-wUrCmCasjAc~BKJuvuDTfuNkWG7DyHKPCumTGwZ7ylPQ~fYGoCTUvjwDvGTjisD5Sw__"
        alt=""
      />
    </div>
  </div>
  <div class="messages">
    <div class="message from">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
    <div class="message to">Привет!</div>
  </div>
  <div class="message-input">
    <input type="text" />
    <button class="send" type="submit">
      <Icon
        viewBox={sendIcon.viewBox}
        d={sendIcon.d}
        size={"27"}
        stroke_width={"2"}
      />
    </button>
  </div>
</div>

<style lang="scss">
  .container {
    max-height: 100vh;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .left-block,
  .right-block {
    flex: 1; // возможность растягиваться
  }

  .header {
    display: flex;
    align-items: center;
    padding: 8px 20px;
    border-bottom: 1px solid #efeff4;
  }

  .left-block {
    display: flex;
    justify-content: start;
  }

  .back {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
    height: 30px;
    :global(path) {
      stroke: var(--primary);
    }
  }

  .center-block {
    margin: 0 auto;
  }

  .name {
    color: #000;
    text-align: center;
    leading-trim: both;
    text-edge: cap;
    font-family: "PP Pangram Sans Rounded";
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    line-height: 100%; /* 18px */
    letter-spacing: -0.27px;
  }

  .right-block {
    display: flex;
    justify-content: end;
  }

  .avatar {
    border-radius: 100%;
    width: 50px;
    height: 50px;
    overflow: hidden;
  }

  .messages {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow-y: scroll;
    padding: 30px 20px;
    gap: 10px;
  }

  .message {
    display: flex;
    max-width: 245px;
    padding: 10px 15px;
    flex-direction: column;
    align-items: flex-start;

    font-family: "PP Pangram Sans Rounded";
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: 120%; /* 16.8px */
    letter-spacing: -0.21px;
  }

  .message.from {
    align-self: end;
    background: var(--Secondary-blue, #2461ff);
    border-radius: 15px 15px 0px 15px;
    color: #fff;
  }

  .message.to {
    align-self: start;
    border-radius: 15px 15px 15px 0px;
    background: var(--light-mode-white-80, #efeff4);
    color: #000;
  }

  .message-input {
    display: flex;
    border-radius: 55px;
    border: 1px solid var(--light-mode-black-60, #cecece);
    min-height: 55px;
    align-items: center;
    margin: 10px 20px;
    input {
      flex: 1;
    }
  }

  .send {
    width: 45px;
    height: 45px;
    border-radius: 100%;
    background-color: #2461ff;
    margin-right: 5px;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
