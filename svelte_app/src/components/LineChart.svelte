<script>
  import { scaleBand, scaleLinear } from "d3-scale";
  import { line } from "d3-shape";

  // Receive plot data as prop.
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

  $: xScale = scaleBand().domain(years).range([0, innerWidth]);

  $: yScale = scaleLinear()
    .domain([0, Math.max(...values)])
    .range([innerHeight, 0])
    .nice();

  $: linePath = line()
    .x((d) => xScale(d.year))
    .y((d) => yScale(d.value));
</script>

<svg class="line-chart" {width} {height}>
  <g
    class="line-chart-inner"
    width={innerWidth}
    height={innerHeight}
    transform="translate({margin.left},{margin.top})"
  >
    <!-- X-Axis -->
    <g class="axis x" transform="translate(0, {innerHeight})">
      <line stroke="black" x1="0" x2={innerWidth} />

      {#each years as year}
        <!-- X-Axis Ticks -->
        <line
          stroke="black"
          x1={xScale(year)}
          x2={xScale(year)}
          y1="1"
          y2="5"
        />

        <!-- X-Axis Tick Labels for even years -->
        {#if year % 2 === 0}
          <text fill="black" text-anchor="middle" x={xScale(year)} y="20">
            {year}
          </text>
        {/if}
      {/each}
    </g>

    <!-- Y-Axis and Grid Lines -->
    <g class="axis y">
      {#each yScale.ticks(4) as tick}
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

          <!-- 
            Y-Axis Ticks. 
            Note: First tick is skipped since the x-axis already acts as a tick. 
          -->
          <line
            stroke="black"
            x1="0"
            x2="-6"
            y1={yScale(tick)}
            y2={yScale(tick)}
          />
        {/if}

        <!-- Y-Axis Tick Labels -->
        <text
          fill="black"
          text-anchor="end"
          dominant-baseline="middle"
          x="-9"
          y={yScale(tick)}
        >
          {tick}
        </text>
      {/each}
    </g>

    <path
      fill="none"
      stroke={colorMapping[region]}
      stroke-width="1.5"
      d={linePath(chartData)}
    />
  </g>
</svg>

<style>
  .line-chart {
    font-size: 0.78125vw; /* 20px at 2560 */
  }
</style>
