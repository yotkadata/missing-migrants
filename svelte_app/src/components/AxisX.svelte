<script>
  export let yearHovered;
  export let xScale;
  export let height;
  export let circleHovered;

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
        circleHovered = false;
      }}
      on:focus={() => {
        yearHovered = tick.getFullYear();
        circleHovered = false;
      }}
      on:mouseleave={() => {
        yearHovered = false;
      }}
    >
      <text
        x="3"
        y={height}
        class={yearHovered === tick.getFullYear() ? "hovered" : ""}
        >{tick.getFullYear()}</text
      >
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

  .tick text.hovered {
    fill: rgba(255, 255, 255, 1);
    font-weight: 800;
  }
</style>
