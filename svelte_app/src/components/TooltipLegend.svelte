<script>
  import { fly, fade } from "svelte/transition";
  import BarChart from "$components/BarChart.svelte";

  export let data;
  export let dataYearly;
  export let totals;

  export let colorMapping;
  export let textColors;

  export let height;
  export let margin;

  export let formatNumber;
  export let formatPct;

  export let yScale;
  export let calcVw;

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
  ]}; width: {calcVw(800)}px;"
  in:fly={{ y: 10, duration: 200, delay: 200 }}
  out:fade={{ duration: 600 }}
  bind:clientWidth={tooltipWidth}
  bind:clientHeight={tooltipHeight}
>
  <div class="text">
    <p
      class="group"
      style="background-color: {colorMapping[data]}; color: {textColors[data]}"
    >
      {data}
    </p>
    <div class="flex-container">
      <div class="flex-item flex-item-left">
        <p class="number-missing">{formatNumber(totals[data].value)}</p>
        <p class="number-missing-text">dead or missing<br />since 2014</p>
      </div>
      <div class="flex-item flex-item-right">
        <p class="pct-missing">{formatPct(totals[data].pct / 100)}</p>
        <p class="pct-missing-text">of all registered<br />cases</p>
      </div>
    </div>
  </div>
  <BarChart
    data={dataYearly}
    region={data}
    {colorMapping}
    width={tooltipWidth}
    {formatNumber}
    {calcVw}
  />
</div>

<style>
  .tooltip {
    background-color: #fff;
    box-shadow: 0 0 0.15625vw rgba(255, 255, 255, 0.5);
    padding: 0;
    border-radius: 0 0 5% 5%;
    align-items: center;
    transition: top 300ms ease, left 300ms ease;
    z-index: 10;
    max-width: 31.25vw; /* 800px at 2560 */
    min-width: 11.71875vw; /* 300px at 2560 */
    word-wrap: break-word;
  }
  .flex-container {
    display: flex;
    justify-content: space-between;
    align-items: start;
  }
  .flex-item {
    flex: 1;
    padding: 0.625vw 0; /* 16px at 2560 */
  }
  .flex-item-left {
    text-align: center;
  }
  .flex-item-right {
    text-align: center;
  }
  .tooltip p {
    color: #000;
    font-size: 0.9375vw; /* 24px at 2560 */
    padding: 0.15625vw 0.625vw; /* 4px 16px at 2560 */
  }
  .tooltip p.group {
    font-weight: 800;
    padding: 0.625vw; /* 16px at 2560 */
    text-transform: uppercase;
  }
  .tooltip p.number-missing,
  .tooltip p.pct-missing {
    font-size: 1.875vw; /* 32px at 2560 */
    font-weight: 800;
    margin-top: 0.625vw; /* 16px at 2560 */
  }
  .tooltip p.number-missing-text,
  .tooltip p.pct-missing-text {
    margin-bottom: 0.625vw; /* 16px at 2560 */
  }
</style>
