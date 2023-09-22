<script>
  export let yScale;
  export let radiusScale;
  export let colorMapping;
  export let width;
  export let height;

  const groups = Object.keys(colorMapping);
  const bubbleLegend = [1000, 500, 100];
</script>

<g class="legend">
  {#each groups as group}
    {#if group !== "Other"}
      <g class="legend-item" transform="translate(0, {yScale(group)})">
        <text x={width + 20} y="5" fill={colorMapping[group]}>{group}</text>
      </g>
    {/if}
  {/each}
</g>

<g
  class="legend-bubble"
  transform="translate({width + radiusScale(1000) + 20}, -25)"
>
  {#each bubbleLegend as bubble}
    <g class="bubble bubble-{bubble}">
      <circle cy={-radiusScale(bubble)} r={radiusScale(bubble)} />
      <line
        x1="0"
        x2={radiusScale(1000) + 50}
        y1={-2 * radiusScale(bubble)}
        y2={-2 * radiusScale(bubble)}
      />
      <text
        x={radiusScale(1000) + 50}
        y={-2 * radiusScale(bubble) + 4}
        text-anchor="end"
        dominant-baseline="hanging"
      >
        {bubble}
      </text>
    </g>
  {/each}
</g>

<style>
  .legend-bubble circle {
    fill: none;
    stroke: rgba(255, 255, 255, 0.5);
  }
  .legend-bubble text {
    font-size: 0.8rem;
    fill: rgba(255, 255, 255, 0.5);
  }
  .legend-bubble line {
    stroke-dasharray: 2;
    stroke: rgba(255, 255, 255, 0.5);
  }
</style>
