<script>
  export let xScale;
  export let formatNumber;
  export let formatMonth;
  export let calcVw;
  export let thresholds;
</script>

<g class="thresholds">
  {#each thresholds as threshold}
    <g
      class="threshold"
      transform="translate({xScale(threshold.date)}, {calcVw(20)})"
    >
      <text class="number" x={calcVw(3)} y="0" dominant-baseline="hanging"
        >{formatNumber(threshold.threshold)}</text
      >
      <text
        class="date"
        x={calcVw(3)}
        y={calcVw(26)}
        dominant-baseline="hanging">{formatMonth(threshold.date)}</text
      >
      <line x1="0" x2="0" y1="0" y2={calcVw(60)} stroke="#fff" />
    </g>
  {/each}
</g>

<style>
  .thresholds text {
    font-family: Lato, sans-serif;
  }
  .thresholds .number {
    fill: rgba(255, 255, 255, 0.8);
    font-size: 0.78125vw; /* 20px at 2560 */
    font-weight: 700;
  }
  .thresholds .date {
    fill: rgba(255, 255, 255, 0.3);
    font-size: 0.625vw; /* 16px at 2560 */
  }
</style>
