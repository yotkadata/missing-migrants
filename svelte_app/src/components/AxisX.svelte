<script>
  import { get } from "svelte/store";

  export let yearHovered;
  export let xScale;
  export let height;

  $: ticks = xScale.ticks();

  // Filter ticks to include only January 1st dates
  $: januaryFirstTicks = ticks.filter(
    (date) => date.getMonth() === 0 && date.getDate() === 1
  );
</script>

<g class="axis x">
  {#each januaryFirstTicks as tick}
    <g
      class="tick"
      transform="translate({xScale(tick)}, 0)"
      on:mouseover={() => {
        yearHovered = tick.getFullYear();
      }}
      on:focus={() => {
        yearHovered = tick.getFullYear();
      }}
      on:mouseleave={() => {
        yearHovered = false;
      }}
    >
      <text x="3" y={height}>{tick.getFullYear()}</text>
      <line
        x1="0"
        x2="0"
        y1="0"
        y2={height}
        stroke="rgba(255, 255, 255, 0.1)"
      />
    </g>
  {/each}
</g>

<style>
  .tick text {
    font-size: 0.78125vw; /* 20px at 2560 */
    fill: rgba(255, 255, 255, 0.8);
    font-weight: 400;
  }
</style>
