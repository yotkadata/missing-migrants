<script>
  import { Circle2 } from "svelte-loading-spinners";

  export let colorOuter;
  export let colorCenter;
  export let colorInner;
  export let size;
</script>

<div class="loading-indicator">
  <div class="circle-wrapper">
    <Circle2 {colorOuter} {colorCenter} {colorInner} {size} />
    <p class="loading-text">Calculating positions ...</p>
  </div>
</div>

<style>
  .loading-indicator {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
  }

  .circle-wrapper {
    position: relative;
  }

  .loading-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin: 0;
    color: white;
    text-align: center;
    font-size: 0.625vw; /* 16px at 2560px */
  }
</style>
