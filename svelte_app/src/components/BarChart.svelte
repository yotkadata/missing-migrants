<script>
  import { scaleLinear } from "d3-scale";

  export let data;
  export let colorMapping;
  export let region;
  export let formatNumber;
  export let calcVw;

  let width;
  $: height = parseInt((width / 16) * 9);

  let margin = {
    top: calcVw(30),
    right: calcVw(30),
    bottom: calcVw(40),
    left: calcVw(70),
  };

  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  // Extract years and values
  $: years = Object.keys(data).map((key) => parseInt(key));
  $: values = Object.values(data).map((value) => parseInt(value));

  // Write to array of objects
  $: chartData = years.map((year, index) => ({ year, value: values[index] }));

  // We add 1 to get the last bar inside innerWidth the chart
  $: xScale = scaleLinear()
    .domain([Math.min(...years), Math.max(...years) + 1])
    .range([0, innerWidth - barGap])
    .nice();

  $: yScale = scaleLinear()
    .domain([0, Math.max(...values)])
    .range([innerHeight, 0])
    .nice();

  $: barGap = calcVw(12);
  // Calculate bar width based on gaps including
  // one at the beginning and one at the end
  $: barWidth = (innerWidth - (years.length + 1) * barGap) / years.length;
</script>

<div class="bar-chart-outer" bind:clientWidth={width}>
  <svg class="bar-chart" {width} {height}>
    <g
      class="bar-chart-inner"
      width={innerWidth}
      height={innerHeight}
      transform="translate({margin.left},{margin.top})"
    >
      <!-- Y-Axis and Grid Lines -->
      <g class="axis y" transform="translate(0,0)">
        {#each yScale.ticks(5) as tick}
          {#if tick !== 0}
            <!-- Grid Lines (skip first line since already present at 0) -->
            <line
              stroke="black"
              stroke-opacity="0.1"
              x1="0"
              x2={innerWidth}
              y1={yScale(tick)}
              y2={yScale(tick)}
            />
          {/if}

          <!-- Y-Axis Tick Labels -->
          <text
            fill="black"
            text-anchor="end"
            dominant-baseline="middle"
            x={calcVw(-6)}
            y={yScale(tick)}
          >
            {formatNumber(tick)}
          </text>
        {/each}
      </g>

      <g class="bars" transform="translate({barGap},0)">
        {#each chartData as barData}
          <rect
            x={xScale(barData.year)}
            y={yScale(barData.value)}
            width={barWidth}
            height={yScale(0) - yScale(barData.value)}
            fill={colorMapping[region]}
          />
        {/each}
      </g>

      <!-- X-Axis -->
      <g class="axis x" transform="translate(0, {innerHeight})">
        <line stroke="black" x1="0" x2={innerWidth} />

        <g class="axis-ticks" transform="translate({barGap + barWidth / 2}, 0)">
          {#each years as year}
            <!-- X-Axis Ticks -->
            <line
              stroke="black"
              x1={xScale(year)}
              x2={xScale(year)}
              y1={calcVw(1)}
              y2={calcVw(5)}
            />
          {/each}
        </g>
        <g
          class="axis-labels"
          transform="translate({barGap + barWidth / 2}, 0)"
        >
          {#each years as year}
            <!-- X-Axis Tick Labels -->
            <text
              fill="black"
              text-anchor="middle"
              x={xScale(year)}
              y={calcVw(25)}
            >
              {"'" + year.toString().slice(-2)}
            </text>
          {/each}
        </g>
      </g>
      <!-- Annotation for maximum value -->
      {#each chartData as datum}
        {#if datum.value === Math.max(...values)}
          <g class="annotate-max">
            <text
              fill="black"
              text-anchor="middle"
              dominant-baseline="text-bottom"
              x={xScale(datum.year) + barWidth / 2 + barGap}
              y={yScale(datum.value) - calcVw(10)}
            >
              {formatNumber(datum.value)}
            </text>
          </g>
        {/if}
      {/each}
    </g>
  </svg>
</div>

<style>
  .bar-chart {
    font-size: 0.78125vw; /* 20px at 2560 */
  }
  .annotate-max {
    font-weight: 600;
  }
</style>
