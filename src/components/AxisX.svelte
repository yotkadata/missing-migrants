<script>
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
    <g class="tick" transform="translate({xScale(tick)}, 0)">
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
