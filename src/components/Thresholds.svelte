<script>
  export let xScale;

  import thresholds from "$data/data-migration-thresholds.json";

  // Convert date strings to Date objects
  thresholds.forEach((d) => {
    d.date = new Date(d.date);
  });

  // Function to format numbers
  const formatNumber = new Intl.NumberFormat("en-US", {
    style: "decimal",
  }).format;
</script>

<g class="thresholds">
  {#each thresholds as threshold}
    <g class="threshold" transform="translate({xScale(threshold.date)}, 0)">
      <text x="3" y="12">{formatNumber(threshold.threshold)}</text>
      <line x1="0" x2="0" y1="0" y2="30" stroke="red" />
    </g>
  {/each}
</g>

<style>
  .thresholds text {
    font-family: Lato, sans-serif;
    fill: rgba(255, 255, 255, 0.3);
    font-size: 1rem;
  }
</style>
