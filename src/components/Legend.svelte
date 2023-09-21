<script>
  export let xScale;
  export let yScale;
  export let colorMapping;
  export let maxDate;
</script>

<g class="legend">
  {#each Object.keys(colorMapping) as group}
    {#if group !== "Other"}
      <g class="legend-item" transform="translate(0, {yScale(group)})">
        <text x={xScale(maxDate) + 20} y="5" fill={colorMapping[group]}
          >{group}</text
        >
      </g>
    {/if}
  {/each}
</g>
