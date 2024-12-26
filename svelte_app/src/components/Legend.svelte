<script>
  export let yScale;
  export let radiusScale;
  export let colorMapping;
  export let width;
  export let totals;
  export let formatNumber;
  export let calcVw;
  export let legendHovered;
  export let circleHovered;

  import { onMount } from "svelte";

  const groups = Object.keys(colorMapping);
  const bubbleLegend = [1000, 500, 100];

  // Get width of legend to calculate width of rects
  let gElement;
  let legendWidth;

  onMount(() => {
    legendWidth = gElement.getBBox().width;
  });

  // Calculate highest pct of totals excluding "Total"
  const maxTotal = Math.max(
    ...Object.keys(totals)
      .filter((group) => group !== "Total")
      .map((group) => totals[group].pct)
  );
</script>

<g class="legend" bind:this={gElement}>
  {#each groups as group}
    {#if group !== "Other"}
      <g
        class="legend-item"
        role="button"
        transform="translate({width + calcVw(60)}, {yScale(group)})"
        tabindex="0"
        on:mouseover={() => {
          circleHovered = null;
          legendHovered = group;
        }}
        on:focus={() => {
          circleHovered = null;
          legendHovered = group;
        }}
        on:mouseleave={() => {
          legendHovered = null;
        }}
      >
        <rect
          width={typeof legendWidth === "number" &&
          totals[group] &&
          typeof totals[group].pct === "number" &&
          typeof maxTotal === "number" &&
          maxTotal !== 0
            ? legendWidth * (totals[group].pct / maxTotal)
            : 0}
          height={calcVw(4)}
          fill={colorMapping[group]}
        />
        <text y={calcVw(22)} fill={colorMapping[group]}>{group}</text>
      </g>
    {/if}
  {/each}
</g>

<g
  class="legend-bubble"
  transform="translate({width + radiusScale(1000) + calcVw(60)}, {calcVw(-25)})"
>
  {#each bubbleLegend as bubble}
    <g class="bubble bubble-{bubble}">
      <circle cy={-radiusScale(bubble)} r={radiusScale(bubble)} />
      <line
        x1="0"
        x2={radiusScale(1000) + calcVw(50)}
        y1={-2 * radiusScale(bubble)}
        y2={-2 * radiusScale(bubble)}
      />
      <text
        x={radiusScale(1000) + calcVw(50)}
        y={-2 * radiusScale(bubble) + calcVw(4)}
        text-anchor="end"
        dominant-baseline="hanging"
      >
        {formatNumber(bubble)}
      </text>
    </g>
  {/each}
</g>

<style>
  .legend-item {
    font-size: 0.78125vw; /* 20px at 2560 */
  }
  .legend-bubble circle {
    fill: none;
    stroke: rgba(255, 255, 255, 0.5);
  }
  .legend-bubble text {
    font-size: 0.546875vw; /* 14px at 2560 */
    fill: rgba(255, 255, 255, 0.5);
  }
  .legend-bubble line {
    stroke-dasharray: 2;
    stroke: rgba(255, 255, 255, 0.5);
  }
</style>
