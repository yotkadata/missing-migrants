<script>
  export let xScale;

  import thresholds from "$data/data-migration-thresholds.json";
  import { timeFormat } from "d3";

  // Convert date strings to Date objects
  thresholds.forEach((d) => {
    d.date = new Date(d.date);
  });

  // Function to format numbers
  const formatNumber = new Intl.NumberFormat("en-US", {
    style: "decimal",
  }).format;

  // Function to format dates
  const formatDate = timeFormat("%b %Y");
</script>

<g class="thresholds">
  {#each thresholds as threshold}
    <g class="threshold" transform="translate({xScale(threshold.date)}, 0)">
      <text class="number" x="3" y="12"
        >{formatNumber(threshold.threshold)}</text
      >
      <text class="date" x="3" y="27">{formatDate(threshold.date)}</text>
      <line x1="0" x2="0" y1="0" y2="40" stroke="#fff" />
    </g>
  {/each}
</g>

<style>
  .thresholds text {
    font-family: Lato, sans-serif;
  }
  .thresholds .number {
    fill: rgba(255, 255, 255, 0.8);
    font-size: 1rem;
    font-weight: 700;
  }
  .thresholds .date {
    fill: rgba(255, 255, 255, 0.3);
    font-size: 0.8rem;
  }
</style>
