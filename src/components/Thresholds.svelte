<script>
  export let xScale;
  export let formatNumber;
  export let formatDate;

  import thresholds from "$data/data-migration-thresholds.json";

  // Convert date strings to Date objects
  thresholds.forEach((d) => {
    d.date = new Date(d.date);
  });
</script>

<g class="thresholds">
  {#each thresholds as threshold}
    <g class="threshold" transform="translate({xScale(threshold.date)}, 20)">
      <text class="number" x="3" y="0" dominant-baseline="hanging"
        >{formatNumber(threshold.threshold)}</text
      >
      <text class="date" x="3" y="18" dominant-baseline="hanging"
        >{formatDate(threshold.date)}</text
      >
      <line x1="0" x2="0" y1="0" y2="60" stroke="#fff" />
    </g>
  {/each}
</g>

<style>
  .thresholds text {
    font-family: Lato, sans-serif;
  }
  .thresholds .number {
    fill: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
    font-weight: 700;
  }
  .thresholds .date {
    fill: rgba(255, 255, 255, 0.3);
    font-size: 0.8rem;
  }
</style>
