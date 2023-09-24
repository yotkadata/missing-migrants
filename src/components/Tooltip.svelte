<script>
  import { fly, fade } from "svelte/transition";
  import { timeFormat } from "d3";

  export let data;
  export let width;
  export let margin;
  export let radiusScale;
  export let formatNumber;
  export let colorMapping;

  let tooltipWidth;

  let xOffset = 5;
  let yOffset = -20;

  $: xPosition =
    data.x + tooltipWidth + margin.left + radiusScale(data.value) + xOffset >
    width
      ? data.x - tooltipWidth
      : data.x + margin.left + radiusScale(data.value) + xOffset;

  $: yPosition = data.y + margin.top - radiusScale(data.value) + yOffset;

  // Function to format dates
  const formatDate = timeFormat("%d %b %Y");
</script>

<div
  class="tooltip"
  style="position: absolute; top: {yPosition}px; left: {xPosition}px;"
  in:fly={{ y: 10, duration: 200, delay: 200 }}
  out:fade={{ duration: 600 }}
  bind:clientWidth={tooltipWidth}
>
  <div class="text">
    <p class="number-missing">
      {formatNumber(data.value)}
    </p>
    <p class="text-missing">Dead or missing</p>
    <p class="date">
      {formatDate(data.date)}
    </p>
    <p class="region" style="background-color: {colorMapping[data.group]}">
      {data.group}
    </p>
  </div>
</div>

<style>
  .tooltip {
    background-color: #fff;
    box-shadow: 2px 3px 8px rgba(0, 0, 0, 0.15);
    padding: 8px 6px;
    border-radius: 5%;
    pointer-events: none;
    align-items: center;
    transition: top 300ms ease, left 300ms ease;
  }
  .text {
    color: #000;
  }
  .number-missing {
    font-size: 2rem;
    font-weight: 800;
    text-align: right;
  }
  .text-missing {
    text-align: right;
  }
  .date {
    margin: 0.5rem 0;
  }
  .region {
    color: #fff;
    font-size: 0.8em;
    font-weight: 800;
    padding: 4px;
    text-transform: uppercase;
  }
</style>
