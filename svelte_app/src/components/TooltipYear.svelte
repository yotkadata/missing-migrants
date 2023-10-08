<script>
  export let yearHovered;
  export let width;
  export let height;
  export let calcVw;
  export let xScale;

  let tooltipWidth;
  let tooltipHeight;
  let xPosition;

  let yPosition = height;

  $: {
    if (
      xScale(new Date(yearHovered, 0, 0, 0, 0, 0, 0)) + tooltipWidth >
      width
    ) {
      // Position the tooltip at the right
      xPosition = width - tooltipWidth;
    } else {
      xPosition = xScale(new Date(yearHovered, 0, 0, 0, 0, 0, 0));
    }
  }

  $: console.log("yearHovered", yearHovered);
  $: console.log("xPosition", xPosition);
  $: console.log("tooltipWidth", tooltipWidth);
</script>

<div
  class="tooltip-year"
  style="position: absolute; top: {yPosition}px; left: {xPosition}px; width: {calcVw(
    800
  )}px;"
  bind:clientWidth={tooltipWidth}
  bind:clientHeight={tooltipHeight}
>
  Some Text
</div>

<style>
  .tooltip-year {
    background-color: rgba(255, 255, 255, 0.9);
    border: 2px solid rgba(255, 255, 255, 0.9);
    border-radius: 5px;
    padding: 1.5vw; /* 38px at 2560 */
    font-size: 1.25vw; /* 32px at 2560 */
    font-weight: 400;
    color: rgba(0, 0, 0, 0.8);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }
</style>
