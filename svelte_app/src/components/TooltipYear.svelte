<script>
  import Treemap from "$components/Treemap.svelte";

  export let yearHovered;
  export let width;
  export let height;
  export let calcVw;
  export let xScale;
  export let yearTreemap;
  export let colorMapping;
  export let formatNumber;

  let tooltipWidth = calcVw(1200);
  let tooltipHeight = tooltipWidth;

  let toolTipMargin = {
    top: calcVw(10),
    right: calcVw(10),
    bottom: calcVw(10),
    left: calcVw(10),
  };

  let tooltipInnerWidth =
    tooltipWidth - toolTipMargin.left - toolTipMargin.right;
  let tooltipInnerHeight =
    tooltipHeight - toolTipMargin.top - toolTipMargin.bottom;

  let xPosition;
  let yPosition = height - tooltipHeight;

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

  let yearTreemapFiltered = {};

  // A reactive statement that watches for changes to `yearHovered`
  // and updates `filteredData` accordingly.
  $: filterDataByYear();

  function filterDataByYear() {
    const yearData = yearTreemap.children?.find(
      (child) => child.name === yearHovered.toString()
    );
    if (yearData) {
      yearTreemapFiltered = {
        name: yearTreemap.name,
        children: [yearData],
      };
    }
  }
</script>

<div
  class="tooltip-year"
  style="position: absolute; top: {yPosition}px; left: {xPosition}px; width: {tooltipWidth}px; height: {tooltipHeight}px;"
>
  <h2>{yearHovered}</h2>
  <Treemap
    data={yearTreemapFiltered}
    width={tooltipInnerWidth}
    height={tooltipInnerHeight}
    {colorMapping}
    {formatNumber}
  />
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
