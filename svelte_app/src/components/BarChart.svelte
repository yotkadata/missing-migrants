<script>
  import { scaleLinear } from "d3-scale";

  export let data;
  export let width;
  export let colorMapping;
  export let region;
  width = 300;
  let height = parseInt((width / 16) * 9);

  let margin = {
    top: 20,
    right: 20,
    bottom: 30,
    left: 40,
  };

  $: innerWidth = width - margin.left - margin.right;
  $: innerHeight = height - margin.top - margin.bottom;

  // Extract years and values
  $: years = Object.keys(data).map((key) => parseInt(key));
  $: values = Object.values(data).map((value) => parseInt(value));

  // Write to array of objects
  $: chartData = years.map((year, index) => ({ year, value: values[index] }));

  $: xScale = scaleLinear()
    .domain([Math.min(...years), Math.max(...years)])
    .range([0, innerWidth - margin.right])
    .nice();

  $: yScale = scaleLinear()
    .domain([0, Math.max(...values)])
    .range([innerHeight, 0])
    .nice();

  $: barWidth = innerWidth / years.length;
  $: barGap = 4;
</script>

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
          <!-- 
              Grid Lines (skip first line since already present at 0) 
            -->
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
          x="-6"
          y={yScale(tick)}
        >
          {tick}
        </text>
      {/each}
    </g>

    <g class="bars">
      {#each chartData as barData}
        <rect
          x={xScale(barData.year) + barGap / 2}
          y={yScale(barData.value)}
          width={barWidth - barGap}
          height={yScale(0) - yScale(barData.value)}
          fill={colorMapping[region]}
        />
      {/each}
    </g>

    <!-- X-Axis -->
    <g class="axis x" transform="translate(0, {innerHeight})">
      <line stroke="black" x1="0" x2={innerWidth} />

      {#each years as year}
        <!-- X-Axis Ticks -->
        <line
          stroke="black"
          x1={xScale(year) + barWidth / 2}
          x2={xScale(year) + barWidth / 2}
          y1="1"
          y2="5"
        />

        <!-- X-Axis Tick Labels -->
        <text
          fill="black"
          text-anchor="middle"
          x={xScale(year) + barWidth / 2}
          y="20"
        >
          {"'" + year.toString().slice(-2)}
        </text>
      {/each}
    </g>
  </g>
</svg>

<style>
  .bar-chart {
    font-size: 0.78125vw; /* 20px at 2560 */
  }
</style>
