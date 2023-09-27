<script>
  import { fly, fade } from "svelte/transition";

  export let data;
  export let formatNumber;
  export let formatPct;
  export let colorMapping;
  export let totals;
  export let height;
  export let margin;
  export let yScale;

  let tooltipWidth;
  let tooltipHeight;
  let yPosition;

  let xPosition = margin.right;

  $: {
    if (yScale(data) + tooltipHeight > height) {
      // Position the tooltip at the bottom
      yPosition = height - tooltipHeight + margin.top;
    } else {
      yPosition = margin.top + yScale(data);
    }
  }
</script>

<div
  class="tooltip"
  style="position: absolute; top: {yPosition}px; right: {xPosition}px; border: 2px solid {colorMapping[
    data
  ]};"
  in:fly={{ y: 10, duration: 200, delay: 200 }}
  out:fade={{ duration: 600 }}
  bind:clientWidth={tooltipWidth}
  bind:clientHeight={tooltipHeight}
>
  <div class="text">
    <p class="group" style="background-color: {colorMapping[data]}">
      {data}
    </p>
    <p class="number-missing">{formatNumber(totals[data].value)}</p>
    <p class="text-missing">Dead or missing since 2014</p>
    <p class="pct-missing">
      {formatPct(totals[data].pct / 100)} of all dead/missing
    </p>
  </div>
</div>

<style>
  .tooltip {
    background-color: #fff;
    box-shadow: 0 0 0.15625vw rgba(255, 255, 255, 0.5);
    padding: 0;
    border-radius: 5%;
    align-items: center;
    transition: top 300ms ease, left 300ms ease;
    z-index: 10;
    max-width: 23.4375vw; /* 600px at 2560 */
    min-width: 11.71875vw; /* 300px at 2560 */
    word-wrap: break-word;
  }
  .tooltip p {
    color: #000;
    font-size: 0.78125vw; /* 20px at 2560 */
    padding: 0.15625vw 0.625vw; /* 4px 16px at 2560 */
  }
  .tooltip p.group {
    color: #f8f8f8;
    font-weight: 800;
    padding: 0.625vw; /* 16px at 2560 */
    text-transform: uppercase;
  }
  .tooltip p.number-missing {
    font-size: 1.25vw; /* 32px at 2560 */
    font-weight: 800;
    margin-top: 0.625vw; /* 16px at 2560 */
  }
  .tooltip p.pct-missing {
    margin-bottom: 0.625vw; /* 16px at 2560 */
  }
</style>
